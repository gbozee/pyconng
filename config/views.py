from __future__ import unicode_literals
import datetime
import pytz
from django.utils import timezone
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
from django.views.generic import RedirectView, FormView, TemplateView
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
from python_nigeria.tickets.models import Ticket, TicketSale
from symposion.reviews.views import (
    access_not_permitted, get_object_or_404, ProposalBase,
    ProposalSection, proposals_generator, ReviewAssignment
)
from symposion.sponsorship.models import Sponsor


@login_required
def review_section(request, section_slug, assigned=False, reviewed="all"):

    if not request.user.has_perm("reviews.can_review_%s" % section_slug):
        return access_not_permitted(request)

    section = get_object_or_404(ProposalSection, section__slug=section_slug)
    queryset = ProposalBase.objects.filter(kind__section=section.section)\
        .select_related('speaker')

    if assigned:
        assignments = ReviewAssignment.objects.filter(user=request.user)\
            .values_list("proposal__id")
        queryset = queryset.filter(id__in=assignments)

    # passing reviewed in from reviews.urls and out to review_list for
    # appropriate template header rendering
    if reviewed == "all":
        queryset = queryset.select_related("result").select_subclasses()
        reviewed = "all_reviews"
    elif reviewed == "reviewed":
        queryset = queryset.filter(reviews__user=request.user)
        reviewed = "user_reviewed"
    else:
        queryset = queryset.exclude(reviews__user=request.user).exclude(
            speaker__user=request.user)
        reviewed = "user_not_reviewed"

    proposals = proposals_generator(request, queryset)

    ctx = {
        "proposals": proposals,
        "section": section,
        "reviewed": reviewed,
    }

    return render(request, "symposion/reviews/review_list.html", ctx)


class LoginForm(LoginUsernameForm):
    username = forms.CharField(label=_("Username/Email"), max_length=30)
    authentication_fail_message = _("The Login/and or password you specified are not correct.")


class NewLoginView(LoginView):
    form_class = LoginForm


class NewSpeakerEditForm(SpeakerForm):
    """Add extra Validation to the SpeakerEdit form."""
    class Meta(SpeakerForm.Meta):
        help_texts = {
            'biography': _("A little bit about you.  Edit using "
                           "<a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' "
                           "target='_blank'>"
                           "Markdown</a>.")
        }

    def clean_photo(self):
        """Make sure photo isn't greater than 600kb."""
        photo = self.cleaned_data.get('photo')
        if photo:
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

from captcha.fields import ReCaptchaField

class NewSponsorApplicationForm(forms.ModelForm):
    captcha = ReCaptchaField()
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
    my_ticket = TicketSale.objects.filter(user=request.user)
    deadline = datetime.datetime(2017, 7, 29, 11, 59, 00, 00, pytz.UTC)
    difference = deadline - timezone.now()
    overide = request.user.email in ["pyconnigeria@pycon.ng"]
    can_submit = difference.days > 0 or overide
    return render(request, "dashboard.html", {"orders": orders, 'my_ticket': my_ticket,
                                              'can_submit': can_submit})


class HomePage(TemplateView):
    template_name = 'pre-conference.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        xx = Sponsor.objects.select_related('image_link').exclude(image_link=None).all()
        sponsors = [{"url": x.external_url, 'image': x.image_link.image} for x in xx]

        context.update(sponsors=sponsors)
        return context
