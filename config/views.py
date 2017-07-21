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
from django.views.generic import RedirectView, FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from django.contrib.auth import login
from symposion.sponsorship.forms import SponsorApplicationForm, Sponsor, forms
from symposion.speakers.forms import SpeakerForm
from symposion.speakers.models import Speaker
from symposion import views as symposion_views
from django.contrib.auth.models import User
from django.core.mail import send_mail
from account.views import LoginView
from account.forms import LoginUsernameForm
from account.decorators import login_required
from python_nigeria.tickets.models import Ticket,TicketSale

class LoginForm(LoginUsernameForm):
    username = forms.CharField(label=_("Username/Email"), max_length=30)
    authentication_fail_message = _("The Login/and or password you specified are not correct.")


class NewLoginView(LoginView):
    form_class = LoginForm


class NewSpeakerEditForm(SpeakerForm):
    """Add extra Validation to the SpeakerEdit form."""

    def clean_photo(self):
        """Make sure photo isn't greater than 600kb."""
        photo = self.cleaned_data['photo']
        photo_size = photo.size

        if photo_size > 600000:
            raise forms.ValidationError(
                _('The image size must not be more than 600kb '
                  'Please upload a smaller one.')
                )
        return photo


class NewSpeakerEditView(LoginRequiredMixin, FormView):
    """CBV Implementation of Symposions speaker_edit view."""
    form_class = NewSpeakerEditForm
    template_name = 'symposion/speakers/speaker_edit.html'

    def get_speaker(self, pk=None):
        """Get speaker by id or currently logged in user"""
        if pk is None:
            try:
                speaker = self.request.user.speaker_profile
            except Speaker.DoesNotExist:
                return redirect("speaker_create")
        else:
            if self.request.user.is_staff:
                speaker = get_object_or_404(Speaker, pk=pk)
            else:
                raise Http404()

        return speaker

    def get(self, request, pk=None, *args, **kwargs):
        speaker = self.get_speaker(pk=pk)

        form = self.form_class(instance=speaker)

        return render(request, "symposion/speakers/speaker_edit.html", {
            "speaker_form": form,
        })

    def post(self, request, pk=None, *args, **kwargs):
        speaker = self.get_speaker(pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=speaker)
        if form.is_valid():
            form.save()
            messages.success(request, "Speaker profile updated.")
            return redirect("dashboard")

        return render(request, "symposion/speakers/speaker_edit.html", {
            "speaker_form": form,
        })


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


@login_required
def dashboard(request):
    if request.session.get("pending-token"):
        return redirect("speaker_create_token",
                        request.session["pending-token"])
    orders = Ticket.objects.not_booked(request.user)
    my_ticket = TicketSale.objects.filter(user=request.user).first()
    return render(request, "dashboard.html",{"orders":orders,'my_ticket':my_ticket})
