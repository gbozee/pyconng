from django.db import models
from config.utils import PayStack, generate_code
from django.conf import settings
from django.utils import timezone
from django.db import transaction

class Coupon(models.Model):
    value = models.CharField(max_length=10)
    expired = models.BooleanField(default=False)
    number_of_usage = models.IntegerField(default=1)
    percentage = models.IntegerField(default=5)

    def is_valid(self):
        return self.usages.count() < self.number_of_usage and not self.expired


class TicketPriceQuerySet(models.QuerySet):
    def with_tickets_purchased(self):
        return self.filter(ticket__status=Ticket.PAYED).annotate(purchased_count=models.Sum('ticket__quantity'))
        # return self.annotate(purchased_count=models.Sum('ticket__quantity'))


class TicketPrice(models.Model):
    name = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    early_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    early_price_count = models.IntegerField(default=0)
    regular_count = models.IntegerField(default=0)
    objects = TicketPriceQuerySet.as_manager()

    EARLY_BIRD = {
        'Company': {"amount": 12000, "count": 5},
        'Personal': {"amount": 6000, "count": 10},
        'Student': {"amount": 3000, "count": 5}
    }
    REGULAR = {
        'Company': {"amount": 20000, "count": 60},
        'Personal': {"amount": 10000, "count": 120},
        'Student': {"amount": 4000, "count": 20},
    }
    URL = {
        "Company":{
                "name": "CORPORATE Package",
                "short_name": "Corporate",
                "style":"",
                "url": "/static/designs/img/tickets/coporate.svg",
                "description":"For the working class who are python experts in the industry",
                "early_price": 10000,
                "price": 20000,
            },
        'Personal':{
                "name": "Individual Package",
                "short_name": "Individual",
                "url": "/static/designs/img/tickets/female-logo.png",
                "style": "width:200px;",
                "description": "For hobbyist python developers and interested individuals",
                "early_price": 6000,
                "price": 10000,
            },
        "Student":{
                "name": "Student Package",
                "short_name":"Student",
                "style":"",
                "url": "/static/designs/img/tickets/student-package@2x.png",
                "description":"For pupils, undergraduate students interested in Python",
                "early_price": 3000,
                "price": 4000,
            },
    }

    def __str__(self):
        return self.name

    @property
    def ticket_details(self):
        return self.URL[self.name]

    @property
    def current_price(self):
        current_count = Ticket.objects.ticket_type_purchased_count(
            self.name, self.early_price_count
        )
        if current_count:
            return self.early_price
        current_count = Ticket.objects.ticket_type_purchased_count(
            self.name, self.regular_count + self.early_price_count
        )
        if current_count:
            return self.amount
        return None

    @classmethod
    def populate_count_price(cls):
        for o in cls.objects.filter(name__in=['Company','Personal',"Student"]):
            if o.early_price == 0:
                record = dict(cls.EARLY_BIRD)[o.name]
                o.early_price = record['amount']
                o.early_price_count = record['count']
                regular = dict(cls.REGULAR)[o.name]
                o.regular_count = regular['count']
                o.amount = regular['amount']
                o.save()

    @classmethod
    def create_ticket_types(cls):
        company, _ = cls.objects.get_or_create(name='Company')
        personal, _ = cls.objects.get_or_create(name='Personal')
        student, _ = cls.objects.get_or_create(name='Student')
        paetron,_ = cls.objects.get_or_create(name="Paetron")
        return company, student, personal,paetron


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

    def ticket_type_purchased_count(self, _type, condition):
        query = self.filter(status=Ticket.PAYED)\
            .filter(ticket_type__name=_type)\
            .aggregate(count=models.Sum('quantity'))['count'] or 0
        return query < condition

    def remaining(self, _type_name):
        tt = TicketPrice.objects.get(name=_type_name)
        count = self.filter(ticket_type__name=_type_name, status=Ticket.PAYED)\
            .aggregate(
                purchased_count=models.Sum('quantity'))['purchased_count'] or 0
        return tt.early_price_count + tt.regular_count - count

    def not_booked(self, user):
        return self.filter(user=user, status=Ticket.PAYED).annotate(cc=models.Count('ticketsale'))\
            .filter(cc=0)


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
    created_tickets = models.BooleanField(default=False)
    coupon_usage = models.ForeignKey(Coupon,related_name='usages',null=True,blank=True)

    @property
    def full_name(self):
        full_name = "%s %s" % (self.user.first_name, self.user.last_name)
        return full_name.strip()

    def __str__(self):
        return self.pk

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


    @transaction.atomic
    def create_sales(self, **kwargs):
        for x in range(self.quantity):
            w = TicketSale(**kwargs)
            w.ticket = self
            w.user = self.user
            w.save()
        self.created_tickets = True
        self.save()
        return self

class TicketSale(models.Model):
    ticket = models.ForeignKey(Ticket)
    full_name = models.CharField(max_length=150)
    diet = models.CharField(max_length=30, choices=(
        ('Omnivorous', 'Omnivorous'),
        ('Vegetarian', 'Vegetarian'),
        ('Others', 'Others'),), default="Omnivorous")
    tagline = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="assigned_tickets")


    @property
    def name(self):
        return self.ticket.ticket_type.name

    @property
    def the_ticket_id(self):
        return "%04d" % self.pk