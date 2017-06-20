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
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.views.generic import RedirectView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import login
from symposion.sponsorship.forms import SponsorApplicationForm, Sponsor, forms

from django.contrib.auth.models import User
from django.core.mail import send_mail
from account.views import LoginView
from account.forms import LoginUsernameForm


class LoginForm(LoginUsernameForm):
    username = forms.CharField(label=_("Username/Email"), max_length=30)
    authentication_fail_message = _("The Login/and or password you specified are not correct.")


class NewLoginView(LoginView):
    form_class = LoginForm


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
            username=obj.contact_name, email=obj.contact_email,
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
            send_mail("New Sponsor Application",
                      ("A new sponsor just applied\n %s"
                       "%s \n %s") % (sponsor.contact_name, sponsor.contact_email, sponsor.level),
                      "noreply@pycon.ng", ["hello@pycon.ng"])
            send_mail("[Pycon NG] Thanks for being a Sponsor",
                      ("Thank you for choosing to sponsor Pycon NG. \n You "
                       "should be contacted shortly by the Sponsorship team. "
                       "\n"), "no_reply@pycon.ng", [sponsor.contact_email])
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


class HomeRedirectView(RedirectView):
    permanent = False
    pattern_name = 'home'
    query_string = True
