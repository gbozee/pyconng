# -*- coding: utf-8 -*-
from django.conf import settings
from symposion.proposals.models import ProposalSection


def consts(request):
    sections = []
    for section in ProposalSection.objects.all():
        if request.user.has_perm("reviews.can_review_%s" % section.section.slug):
            sections.append(section)
    # categories = Category.objects.annotate(count=Count('skill')).prefetch_related('skill_set')
    return dict(
        SITE_NAME='Pycon',
        title='Python Nigeria Conference',
        development=True,
        THEME_CONTACT_EMAIL=settings.THEME_CONTACT_EMAIL,
        # review_sections=sections,
    )