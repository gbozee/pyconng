# -*- coding: utf-8 -*-
from django.conf import settings
def consts(request):
    # categories = Category.objects.annotate(count=Count('skill')).prefetch_related('skill_set')
    return dict(
        SITE_NAME='Pycon',
        title='Python Nigeria Conference',
        development=True,
        THEME_CONTACT_EMAIL=settings.THEME_CONTACT_EMAIL,
    )