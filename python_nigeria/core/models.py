from django.db import models
from config.utils import PayStack
from django.conf import settings


class Tickets(models.Model):
    ISSUED = 1
    PAYED = 2
    STATUS = (
        (ISSUED, 'issued'),
        (PAYED, 'payed'),

    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="tickets")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    made_payment = models.BooleanField(default=False)
    status = models.IntegerField(default=ISSUED, choices=STATUS)
    paystack_access_code = models.URLField(blank=True, null=True)
