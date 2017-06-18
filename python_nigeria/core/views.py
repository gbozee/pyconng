from django.contrib import messages
from django.views.generic import (
    FormView, RedirectView,
    TemplateView)
from config.utils import PayStack
import logging

logger = logging.getLogger(__name__)


@login_required
def validate_paystack_ref(request, order, code):
    v = PayStack().validate_transaction(code)
    if v:
        try:
            d = services.DepositMoneyService(order)\
                .paystack_validation(v['amount_paid'])
            a = wallet_service.WalletService(request.user.id)
            a.update_paystack_auth_code(v['authorization_code'])
            return JsonResponse({'status': True})
        except services.error_exception():
            d = services.SingleRequestService(order)
            d.pay_processing_fee()
            return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})


def paystack_webhook(request):
    return JsonResponse(json.dumps(request.POST), safe=False)


class PaystackAuthorizationView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        if self.request.GET.get('ttype') == 'processing_fee':
            self.service = services.SingleRequestService(kwargs['order'])
        else:
            self.service = services.DepositMoneyService(kwargs['order'])
        response, outcome = self.service.paystack_payment_outcome(self.request)
        if outcome:
            if self.request.GET.get('ttype') != 'processing_fee':
                messages.error(
                    self.request, "Sorry This Transaction Failed. Please Try again or use other payment options")
        return response


class OnlinePaymentRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        try:
            req = services.SingleRequestService(slug=kwargs['slug'])
            url = req.create_online_booking(kwargs['tutor_slug'])
        except ObjectDoesNotExist:
            raise Http404('No Request matches the given query.')
        user = self.login_user(req.get_user())
        booking_url = "%s" % (reverse('request_payment_page', args=[url]),)

        if user is not None:
            return booking_url
        if self.request.user.is_authenticated():
            return booking_url
        return "%s?redirect_url=%s" % (reverse('account_login'), booking_url)

    def login_user(self, user):
        # log in the user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return user


class ClientPaymentCompletedView(RedirectView):
    permanent = False
    query_string = True
    #

    def get_redirect_url(self, *args, **kwargs):
        status, message_txt = services.DepositMoneyService.generic_payment_outcome(
            self.request, **kwargs
        )
        if status:
            messages.info(self.request, message_txt)
            return reverse("users:revenue_transactions")
        messages.error(self.request, message_txt)
        return reverse("request_payment_page", args=[kwargs['order']])


class FailedPaymentRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        print(self.request.POST)
        messages.error(self.request, "Sorry the payment was cancelled")
        return reverse('request_payment_page', args=[kwargs['order']])


class PaystackCallBackView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        x = self.request.POST
        logger.info(x)
        print(x)
        y = self.request.GET.get('trxref')
        if y:
            v = utils.PayStack().validate_transaction(y)
            if v:
                try:
                    d = services.DepositMoneyService(kwargs.get('order'))
                    d.notify_admin_of_payments_made(condition=True, **v)
                    messages.info(
                        self.request, "Transaction Payment Successful!")
                    return reverse('users:revenue_transactions')
                except ObjectDoesNotExist:
                    d = services.SingleRequestService(kwargs.get('order'))
                    d.pay_processing_fee()
                    messages.info(
                        self.request, "Processing Fee Payment Successful!")
                    return reverse('processing_fee_completed', args=[kwargs.get('order')])
        messages.error(
            self.request, "Sorry there was an error in this transaction. contact info@tuteria.com")
        return reverse('request_payment_page', args=[kwargs.get('order')])
