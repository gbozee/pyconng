from __future__ import unicode_literals
try:
    from io import StringIO
except:
    # Python 2
    from cStringIO import StringIO
import itertools
import logging
import os
import time
from zipfile import ZipFile, ZipInfo

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import login
from symposion.sponsorship.forms import SponsorApplicationForm, Sponsor, forms

from django.contrib.auth.models import User


class NewSponsorApplicationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewSponsorApplicationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sponsor
        fields = [
            "name",
            "external_url",
            "contact_name",
            "contact_email",
            "level"
        ]

    def save(self, commit=True):
        obj = super(NewSponsorApplicationForm, self).save(commit=False)
        user, _ = User.objects.get_or_create(
            username=obj.contact_name,email=obj.contact_email,
            defaults=dict(first_name=obj.name))
        obj.applicant = user
        if commit:
            obj.save()
        return obj


def sponsor_apply(request):
    params = {}
    user = request.user
    if user.is_authenticated():
        params.update({
            "initial": {
                "contact_name": user.get_full_name,
                "contact_email": user.email,
            }
        })

    if request.method == "POST":
        form = NewSponsorApplicationForm(request.POST, **params)
        if form.is_valid():
            sponsor = form.save()
            user = sponsor.applicant
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            if sponsor.sponsor_benefits.all():
                # Redirect user to sponsor_detail to give extra information.
                messages.success(request, _("Thank you for your sponsorship "
                                            "application. Please update your "
                                            "benefit details below."))
                return redirect("sponsor_detail", pk=sponsor.pk)
            else:
                messages.success(request, _("Thank you for your sponsorship "
                                            "application."))
                return redirect("dashboard")
    else:
        form = NewSponsorApplicationForm(**params)

    return render_to_response("symposion/sponsorship/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))
