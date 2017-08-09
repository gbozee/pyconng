from django.db import models
from symposion.sponsorship.models import Sponsor
class SponsorImage(models.Model):
    sponsor = models.OneToOneField(Sponsor, related_name='image_link')
    image = models.ImageField(upload_to="sponsors")