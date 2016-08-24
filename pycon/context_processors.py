# -*- coding: utf-8 -*-

def consts(request):
    # categories = Category.objects.annotate(count=Count('skill')).prefetch_related('skill_set')
    return dict(
        SITE_NAME='Pycon',
        title='Python Nigeria Conference',
        development=True,
    )