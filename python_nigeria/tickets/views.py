from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView, DetailView, FormView
from django.http.response import JsonResponse
from django import forms
from django.conf import settings
from django.contrib import messages
import logging
from config.utils import PayStack
import json

# Create your views here.
from .models import Ticket, TicketPrice, Coupon, TicketSale

logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.core.mail import send_mail


class TicketHomeView(TemplateView):
    template_name = "tickets/home.html"

    def get_context_data(self, **kwargs):
        context = super(TicketHomeView, self).get_context_data(**kwargs)
        tickets = TicketPrice.objects.filter(
            name__in=["Company", "Personal", "Student", "Tutorial"]
        )
        ticket_types = [
            {
                **x.ticket_details,
                "current_price": x.current_price,
                "early_price": x.early_price,
                "amount": x.amount,
                # "early_bird": False,
                "early_bird": x.early_bird_remaining(),
            }
            for x in tickets if x.current_price
        ]
        ticket_types = sorted(ticket_types, key=lambda x: x["current_price"])

        context.update({"plans": ticket_types})
        return context


def intermediate_purchase(request):
    selected = request.GET.get("selected_plan")
    request.session["selected_plan"] = selected
    return redirect("tickets:purchase")


class PurchaseForm(forms.Form):
    # Student = forms.IntegerField(required=False)
    Company = forms.IntegerField(required=False)
    Personal = forms.IntegerField(required=False)
    Tutorial = forms.IntegerField(required=False)
    coupon = forms.CharField(required=False)

    def determine_cost(self, name, value=0):
        ticket_price = TicketPrice.objects.get(name__icontains=name)
        return (ticket_price, ticket_price * value)

    def selected_tickets(self):
        considered = [
            x for x, y in self.cleaned_data.items() if x != "coupon" and int(y) > 0
        ]
        return considered

    def get_coupon_value(self):
        result = Coupon.objects.filter(
            value__iexact=self.cleaned_data["coupon"], expired=False
        ).first()
        return result

    def get_total(self, ticket, user):
        return ticket.get_total()
        # if ticket.multiple_tickets:
        #     others = Ticket.objects.issued(user)
        # else:
        #     others = [ticket]
        # total = sum(x.amount for x in others)
        # return total

    def save(self, user):
        tickets_selected = self.selected_tickets()
        tickets = []
        coupon = self.get_coupon_value()
        Ticket.objects.filter(status=Ticket.ISSUED, user_id=user.id).delete()
        for ticket in tickets_selected:
            tick = Ticket.create(user=user, ticket_name=ticket)
            tick.quantity = self.cleaned_data[ticket]
            _type = TicketPrice.objects.get(name=ticket)
            tick.ticket_type = _type
            if tick.ticket_type.current_price:
                percentage = 0
                print(coupon)
                if coupon:
                    percentage = coupon.percentage
                    print(percentage)
                tick.amount = (
                    tick.quantity
                    * tick.ticket_type.current_price
                    * (100 - percentage)
                    / 100
                )
                print(tick.amount)
                if coupon:
                    tick.coupon_usage = coupon
                tick.save()
                tickets.append(tick)
        if len(tickets) > 1:
            Ticket.objects.filter(pk__in=[x.pk for x in tickets]).update(
                multiple_tickets=True
            )
        Ticket.objects.filter(pk__in=[x.pk for x in tickets]).update(
            related=tickets[0].pk
        )
        tk = Ticket.objects.get(pk=tickets[0].pk)
        return tickets[0], self.get_total(tk, user)


class PurchaseView(TemplateView):
    template_name = "tickets/purchase.html"

    def coupon_value(self, coupon):
        if coupon:
            result = Coupon.objects.filter(value__iexact=coupon, expired=False).first()
            if result.usages.count() <= result.number_of_usage:
                return result
            else:
                result.expired = True
                result.save()
        return None

    def post(self, request, *args, **kwargs):
        logger.info(request.body)
        data = json.loads(request.body)
        request.session.pop("selected_plan", None)
        # {'coupon': '', 'tickets': {'Student': '0', 'Personal': '0', 'Company': '2', 'Tutorial': '0'}}
        form = PurchaseForm({**data["tickets"], "coupon": data.get("coupon")})
        if form.is_valid():
            helper, total = form.save(request.user)
            return JsonResponse({"order": helper.pk, "total": float(total)})
        return JsonResponse({"error": form.errors})

    def get_context_data(self, **kwargs):
        context = super(PurchaseView, self).get_context_data(**kwargs)
        tickets = TicketPrice.objects.filter(
            name__in=["Company", "Personal", "Tutorial"]
        )
        ticket_types = [
            {
                "ticket_details": x.ticket_details,
                "name": x.name,
                "current_price": x.current_price,
            }
            for x in tickets
        ]

        # ticket_price = TicketPrice.objects.all()
        def amount(y):
            return [x["current_price"] for x in ticket_types if x["name"] == y][0]

        tickets = [
            # {
            #     "name": "Student ticket",
            #     "short_name": "Student",
            #     "amount": amount("Student"),
            # },
            {
                "name": "Personal ticket",
                "short_name": "Personal",
                "amount": amount("Personal"),
            },
            {
                "name": "Corporate ticket",
                "short_name": "Company",
                "amount": amount("Company"),
            },
            {
                "name": "Tutorial ticket",
                "short_name": "Tutorial",
                "amount": amount("Tutorial"),
            },
        ]
        context.update(
            tickets=tickets,
            public_key=settings.PAYSTACK_PUBLIC_KEY,
            default_plan=self.request.session.get("selected_plan"),
        )
        return context


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = TicketSale
        fields = ["full_name", "diet", "tagline"]

    def save(self, **kwargs):
        return super().save(commit=kwargs.get("commit", True))


class TicketDetailPage(DetailView):
    template_name = "tickets/detail.html"
    model = Ticket
    pk_url_kwarg = "order"

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if not self.object.created_tickets:
            messages.error(request, "This ticket appears to be invalid")
            return redirect("dashboard")
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.object.ticketsale_set.select_related("ticket__ticket_type").filter(
            user=self.request.user
        )
        if "forms" not in kwargs:
            forms = [{"form": TicketEditForm(instance=x), "ticket": x} for x in sales]
            context.update(tickets=forms)
        return context


def valid_coupons(request):
    value = request.GET.get("value")
    if value:
        result = Coupon.objects.filter(value__iexact=value, expired=False).first()
        if result:
            if result.is_valid():
                return JsonResponse({"status": result.percentage})
    return JsonResponse({"status": 0})


def purchase_complete(request, order):
    d = get_object_or_404(Ticket, pk=order)
    if d.status == Ticket.PAYED:
        # sales = d.ticketsale_set.select_related("ticket__ticket_type").filter(
        #     user=request.user
        # )
        count = Ticket.objects.filter(status=Ticket.PAYED, related=order).count()
        return render(
            request, "tickets/purchase-complete.html", {"ticket": d, "count": count}
        )
    messages.error(request, "Oops! You haven't made any payment yet")
    return redirect("tickets:purchase")


def validate_paystack_ref(request, order, code):
    v = PayStack().validate_transaction(code)
    d = get_object_or_404(Ticket, pk=order)
    if v:
        d.update_wallet_and_notify_admin(v["amount_paid"])
        messages.info(request, "Transaction Payment Successful!")
        return JsonResponse({"status": True})
    else:
        d = d.change_order()
        return JsonResponse({"status": False, "order": d.order})


def paystack_webhook(request):
    return JsonResponse(json.dumps(request.POST), safe=False)


class PaystackCallBackView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        x = self.request.POST
        logger.info(x)
        print(x)
        d = get_object_or_404(Ticket, pk=kwargs.get("order"))

        y = self.request.GET.get("trxref")
        if y:
            v = PayStack().validate_transaction(y)
            if v:
                d.update_wallet_and_notify_admin(v["amount_paid"])
                messages.info(self.request, "Transaction Payment Successful!")
                return reverse("dashboard")

        messages.error(
            self.request,
            "Sorry there was an error in this transaction. contact info@tuteria.com",
        )
        d = d.change_order()
        return reverse("tickets:checkout_view", args=[d.order])


class TicketCreateForm(forms.Form):
    full_name = forms.CharField()
    tagline = forms.CharField()
    diet = forms.ChoiceField(
        choices=(
            ("Omnivorous", "Omnivorous"),
            ("Vegetarian", "Vegetarian"),
            ("Others", "Others"),
        )
    )

    def save(self, ticket):
        if not ticket.created_tickets:
            return ticket.create_sales(**self.cleaned_data)
        return ticket


class CreateTicketview(DetailView):
    model = Ticket
    pk_url_kwarg = "order"

    template_name = "tickets/create.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            result = form.save(self.object)
            return redirect(reverse("tickets:detail", args=[result.pk]))
        messages.error(request, "There are errors with the form")
        return self.render_to_response(self.get_context_data(ticket_form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not "ticket_form" in kwargs:
            form = TicketCreateForm(initial={"full_name": self.object.full_name})
            context.update(ticket_form=form)
        return context


class TicketTransferForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        data = super().clean()
        if not User.objects.filter(email=data.get("email")).exists():
            self.add_error("email", "This email doesn't exist on the platform")
        return data

    def save(self, ticket=None):
        email = self.cleaned_data["email"]
        old_owner = ticket.user
        email_user = User.objects.get(email=email)
        ticket.user = email_user
        ticket.save()
        # send email to new user on ticket
        send_mail(
            "Ticket Transfer",
            (
                "{} just trasfered a PyconNG {} ticket \n. "
                "Go to the dashboard to view details. \n"
                "{}.\n Ensure you update the ticket details."
            ).format(old_owner.email, ticket.name, "https://www.pycon.ng/dashboard"),
            "noreply@pycon.ng",
            [email],
        )
        return ticket


class SalesTicketView(RedirectView):
    query_string = True

    def get_object(self):
        return TicketSale.objects.get(pk=self.kwargs["pk"])

    def get_redirect_url(self, *args, **kwargs):
        self.object = self.get_object()
        request = self.request
        transfer = request.GET.get("transfer")
        print(request.GET)
        if transfer:
            form = TicketTransferForm(request.POST)
        else:
            form = TicketEditForm(request.POST, instance=self.object)
        if form.is_valid():
            result = form.save(ticket=self.object)
            if transfer:
                messages.success(
                    request, "Ticket has be transfered to {}".format(result.user.email)
                )
        else:
            print(form.errors)
            if transfer:
                messages.error(request, "The email doesn't exist")
            else:
                messages.error(
                    request, "Please ensure all fields in the form is filled."
                )
        return reverse("tickets:detail", args=[self.object.ticket.pk])

