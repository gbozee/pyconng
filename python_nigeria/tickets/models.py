from django.db import models
from config.utils import PayStack, generate_code
from django.conf import settings
from django.utils import timezone


class Coupon(models.Model):
    value = models.CharField(max_length=10)
    expired = models.BooleanField(default=False)
    percentage = models.IntegerField(default=5)


class TicketPrice(models.Model):
    name = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

    @classmethod
    def create_ticket_types(cls):
        company, _ = cls.objects.get_or_create(name='Company')
        personal, _ = cls.objects.get_or_create(name='Personal')
        student, _ = cls.objects.get_or_create(name='Student')
        return company, student, personal


class TicketQuerySet(models.QuerySet):
    def issued(self, user=None):
        if user:
            return self.filter(
                user=user, multiple_tickets=True, status=Ticket.ISSUED)
        return self

    def update_payment(self):
        return self.update(
            date_paid=timezone.now(), 
            status=Ticket.PAYED, made_payment=True)


class Ticket(models.Model):
    ISSUED = 1
    PAYED = 2
    STATUS = (
        (ISSUED, 'issued'),
        (PAYED, 'payed'),
    )
    objects = TicketQuerySet.as_manager()
    order = models.CharField(max_length=12, primary_key=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="tickets")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date_paid = models.DateTimeField(null=True)
    made_payment = models.BooleanField(default=False)
    status = models.IntegerField(default=ISSUED, choices=STATUS)
    paystack_access_code = models.URLField(blank=True, null=True)
    ticket_type = models.ForeignKey(TicketPrice, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    multiple_tickets = models.BooleanField(default=False)

    @staticmethod
    def create(user=None, **kwargs):
        """If client is placing the request for the first time create else return an instance of the previous
        creation"""
        order = generate_code(Ticket)
        ticket_type__name = kwargs.get('ticket_name')
        previous_issued = Ticket.objects.filter(
            user_id=user.id, status=Ticket.ISSUED, ticket_type__name=ticket_type__name).first()
        if previous_issued is None:
            obj, is_new = Ticket.objects.get_or_create(
                user_id=user.id,
                status=Ticket.ISSUED,
                order=order
            )
        else:
            obj = previous_issued
            if not obj.order:
                obj.order = order
                obj.save()
        order1 = obj.order
        return Ticket.objects.filter(order=order1).first()

    def update_wallet_and_notify_admin(self, full_payment):
        new_amount = full_payment
        others = Ticket.objects.issued(self.user).values_list('pk', flat=True)
        if self.pk in others:
            Ticket.objects.filter(pk__in=others).update_payment()
        Ticket.objects.filter(pk=self.pk).update_payment()

    def change_order(self):
        old_ticket = self.order
        self.order = generate_code(Ticket)
        self.save()
        Ticket.objects.filter(order=old_ticket).all().delete()
        return self

    def update_others(self):
        data = Ticket.objects.filter(
            user=self.user, multiple_tickets=True).values_list('pk', flat=True)
        if self.pk in data:
            Ticket.objects.filter(
                user=self.user, multiple_tickets=True).update(status=self.PAYED)
