from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import (
    TemplateView, RedirectView, DetailView, FormView)
from django.http.response import JsonResponse
from django import forms
from django.conf import settings
from django.contrib import messages
import logging
from config.utils import PayStack
import json
# Create your views here.
from .models import (
    Ticket, TicketPrice, Coupon, TicketSale)
logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.core.mail import send_mail


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

    def validate_TRSC(self):
        data = self.cleaned_data['TRSC']
        remaining = TicketPrice.objects.remaining("Company")
        if remaining < data:
            raise forms.ValidationError("There is remaining {} Business Tickets left".format(
                remaining
            ))
        return data

    def validate_TRSS(self):
        data = self.cleaned_data['TRSS']
        remaining = TicketPrice.objects.remaining("Student")
        if remaining < data:
            raise forms.ValidationError("There is remaining {} Student Ticket(s) left".format(
                remaining
            ))
        return data

    def validate_TRSP(self):
        data = self.cleaned_data['TRSP']
        remaining = TicketPrice.objects.remaining("Personal")
        if remaining < data:
            raise forms.ValidationError("There is remaining {} Personal Tickets left".format(
                remaining
            ))
        return data

    def clean(self):
        cleaned_data = super(PurchaseForm, self).clean()
        company, student, personal = self.get_data(cleaned_data)
        if not company and not student and not personal:
            raise forms.ValidationError("Ticket Quantity must be inputed")
        if personal:
            data = cleaned_data['TRSP']
            remaining = Ticket.objects.remaining("Personal")
            if remaining < data:
                raise forms.ValidationError("There is remaining {} Personal Tickets left".format(
                    remaining
                ))
        if student:
            data = cleaned_data['TRSS']
            remaining = Ticket.objects.remaining("Student")
            if remaining < data:
                raise forms.ValidationError("There is remaining {} Student Ticket(s) left".format(
                    remaining
                ))
        if company:
            data = cleaned_data['TRSC']
            remaining = Ticket.objects.remaining("Company")
            if remaining < data:
                raise forms.ValidationError("There is remaining {} Business Tickets left".format(
                    remaining
                ))
        return cleaned_data

    def save(self, user, coupon=0):
        company, student, personal = self.get_data(self.cleaned_data)
        tickets = []
        for ticket in zip([company, student, personal], TicketPrice.create_ticket_types()):
            if ticket[0]:
                tick = Ticket.create(user=user, ticket_name=ticket[1].name)
                tick.quantity = ticket[0]
                tick.ticket_type = ticket[1]
                if tick.ticket_type.current_price:
                    tick.amount = tick.quantity * \
                        tick.ticket_type.current_price * (100 - coupon) / 100
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
        ticket_price = TicketPrice.objects.all()

        def amount(y):
            return [x.current_price for x in ticket_price if x.name == y][0]
        tickets = [
            {'data_fare': 'TRSS', 'amount': amount('Student')},
            {'data_fare': 'TRSP', 'amount': amount("Personal")},
            {'data_fare': 'TRSC', 'amount': amount("Company")}
        ]
        context.update(tickets=tickets)
        return context


class CheckoutView(TemplateView):
    template_name = 'tickets/checkout.html'

    def get(self, request, *args, **kwargs):
        self.item = get_object_or_404(Ticket, order=self.kwargs['order'])

        response = super(CheckoutView, self).get(request, *args, **kwargs)
        if self.item.status == Ticket.PAYED:
            messages.warning(
                self.request, "You have already paid for this ticket order")
            self.item.update_others()
            return redirect('dashboard')
        return response

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        if self.item.multiple_tickets:
            others = Ticket.objects.issued(self.request.user)
        else:
            others = [self.item]
        total = sum(x.amount for x in others)
        context.update(tickets=others, total=total, slug=others[0].pk,
                       public_key=settings.PAYSTACK_PUBLIC_KEY)
        return context


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = TicketSale
        fields = ['full_name', 'diet', 'tagline']

    def save(self, **kwargs):
        return super().save(commit=kwargs.get('commit', True))


class TicketDetailPage(DetailView):
    template_name = 'tickets/detail.html'
    model = Ticket
    pk_url_kwarg = 'order'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if not self.object.created_tickets:
            messages.error(request, "This ticket appears to be invalid")
            return redirect('dashboard')
        return result

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.object.ticketsale_set.select_related(
            'ticket__ticket_type').filter(user=self.request.user)
        if 'forms' not in kwargs:
            forms = [{'form': TicketEditForm(
                instance=x), 'ticket': x} for x in sales]
            context.update(tickets=forms)
        return context


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


class TicketCreateForm(forms.Form):
    full_name = forms.CharField()
    tagline = forms.CharField()
    diet = forms.ChoiceField(choices=(
        ('Omnivorous', 'Omnivorous'),
        ('Vegetarian', 'Vegetarian'),
        ('Others', 'Others'),))

    def save(self, ticket):
        if not ticket.created_tickets:
            return ticket.create_sales(**self.cleaned_data)
        return ticket


class CreateTicketview(DetailView):
    model = Ticket
    pk_url_kwarg = 'order'

    template_name = 'tickets/create.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            result = form.save(self.object)
            return redirect(reverse("tickets:detail", args=[result.pk]))
        messages.error(request, "There are errors with the form")
        return self.render_to_response(
            self.get_context_data(
                ticket_form=form
            ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not 'ticket_form' in kwargs:
            form = TicketCreateForm(initial={
                'full_name': self.object.full_name
            })
            context.update(ticket_form=form)
        return context


class TicketTransferForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        data = super().clean()
        if not User.objects.filter(email=data.get('email')).exists():
            self.add_error('email', "This email doesn't exist on the platform")
        return data

    def save(self, ticket=None):
        email = self.cleaned_data['email']
        old_owner = ticket.user
        email_user = User.objects.get(email=email)
        ticket.user = email_user
        ticket.save()
        # send email to new user on ticket
        send_mail(
            "Ticket Transfer",
            ("{} just trasfered a PyconNG {} ticket \n. "
             "Go to the dashboard to view details. \n"
             "{}.\n Ensure you update the ticket details.").format(old_owner.email, ticket.name,
                          "https://www.pycon.ng/dashboard"), 'noreply@pycon.ng', [email])
        return ticket


class SalesTicketView(RedirectView):
    query_string = True

    def get_object(self):
        return TicketSale.objects.get(pk=self.kwargs['pk'])

    def get_redirect_url(self, *args, **kwargs):
        self.object = self.get_object()
        request = self.request
        transfer = request.GET.get('transfer')
        print(request.GET)
        if transfer:
            form = TicketTransferForm(request.POST)
        else:
            form = TicketEditForm(request.POST, instance=self.object)
        if form.is_valid():
            result = form.save(ticket=self.object)
            if transfer:
                messages.success(request, "Ticket has be transfered to {}".format(
                    result.user.email
                ))
        else:
            print(form.errors)
            if transfer:
                messages.error(request,"The email doesn't exist")
            else:
                messages.error(
                    request, "Please ensure all fields in the form is filled.")
        return reverse('tickets:detail', args=[self.object.ticket.pk])
