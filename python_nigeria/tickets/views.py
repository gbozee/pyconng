from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.http.response import JsonResponse
from django import forms
from django.conf import settings
from django.contrib import messages
import logging
from config.utils import PayStack
import json
# Create your views here.
from .models import Ticket, TicketPrice, Coupon
logger = logging.getLogger(__name__)


class TicketHomeView(TemplateView):
    template_name = 'tickets/home.html'


class PurchaseForm(forms.Form):
    TRSC = forms.IntegerField(required=False)
    TRSS = forms.IntegerField(required=False)
    TRSP = forms.IntegerField(required=False)

    def get_data(self, cleaned_data):
        company = cleaned_data.get('TRSC')
        student = cleaned_data.get('TRSS')
        personal = cleaned_data.get('TRSP')
        return company, student, personal

    def clean(self):
        cleaned_data = super(PurchaseForm, self).clean()
        company, student, personal = self.get_data(cleaned_data)
        if not company and not student and not personal:
            raise forms.ValidationError("Ticket Quantity must be inputed")
        return cleaned_data

    def save(self, user, coupon=0):
        company, student, personal = self.get_data(self.cleaned_data)
        tickets = []
        for ticket in zip([company, student, personal], TicketPrice.create_ticket_types()):
            if ticket[0]:
                tick = Ticket.create(user=user, ticket_name=ticket[1].name)
                tick.quantity = ticket[0]
                tick.ticket_type = ticket[1]
                tick.amount = tick.quantity * \
                    tick.ticket_type.amount * (100 - coupon) / 100
                tick.save()
                tickets.append(tick)
        if len(tickets) > 1:
            Ticket.objects.filter(pk__in=[x.pk for x in tickets]).update(
                multiple_tickets=True
            )
        return tickets[0]


class PurchaseView(TemplateView):
    template_name = 'tickets/purchase.html'

    def coupon_value(self, coupon):
        if coupon:
            result = Coupon.objects.filter(value__icontains=coupon).first()
            return result.percentage
        return 0

    def post(self, request, *args, **kwargs):
        logger.info(request.POST)
        print(request.POST)
        form = PurchaseForm(request.POST)
        if form.is_valid():
            coupon = request.POST.get('coupon')
            c_value = self.coupon_value(coupon)
            helper = form.save(request.user, c_value)
            return redirect('tickets:checkout_view', helper.pk)
        messages.error(request, form.errors)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(PurchaseView, self).get_context_data(**kwargs)
        tickets = [
            {'data_fare': 'TRSS', 'amount': 130},
            {'data_fare': 'TRSP', 'amount': 375},
            {'data_fare': 'TRSC', 'amount': 677.10}
        ]
        context.update(tickets=tickets)
        return context


class CheckoutView(TemplateView):
    template_name = 'tickets/checkout.html'

    def get(self, request, *args, **kwargs):
        self.item = get_object_or_404(Ticket, order=self.kwargs['order'])
        
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        if self.item.status == Ticket.PAYED:
            messages.warning(self.request, "You have already paid for this ticket order")
            self.item.update_others()
            return redirect('dashboard')
        return response

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        if self.item.multiple_tickets:
            others =  Ticket.objects.issued(self.request.user)
        else:
            others = [self.item]
        total = sum(x.amount for x in others)
        context.update(tickets=others, total=total, slug=others[0].pk,
                       public_key=settings.PAYSTACK_PUBLIC_KEY)
        return context


class TicketDetailPage(TemplateView):
    template_name = 'tickets/detail.html'


def valid_coupons(request):
    value = request.GET.get('value')
    if value:
        result = Coupon.objects.filter(value__icontains=value).first()
        if result:
            return JsonResponse({'status': result.percentage})
    return JsonResponse({'status': 0})


def validate_paystack_ref(request, order, code):
    v = PayStack().validate_transaction(code)
    d = get_object_or_404(Ticket, pk=order)
    if v:
        d.update_wallet_and_notify_admin(v['amount_paid'])
        messages.info(request, "Transaction Payment Successful!")
        return JsonResponse({'status': True})
    else:
        d = d.change_order()
        return JsonResponse({'status': False, "order": d.order})


def paystack_webhook(request):
    return JsonResponse(json.dumps(request.POST), safe=False)


class PaystackCallBackView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        x = self.request.POST
        logger.info(x)
        print(x)
        d = get_object_or_404(Ticket, pk=kwargs.get('order'))

        y = self.request.GET.get('trxref')
        if y:
            v = PayStack().validate_transaction(y)
            if v:
                d.update_wallet_and_notify_admin(v['amount_paid'])
                messages.info(
                    self.request, "Transaction Payment Successful!")
                return reverse('dashboard')

        messages.error(
            self.request, "Sorry there was an error in this transaction. contact info@tuteria.com")
        d = d.change_order()
        return reverse('tickets:checkout_view', args=[d.order])
