from django import template
from django.contrib.admin.views.main import SEARCH_VAR
from django.contrib.sites.models import Site

register = template.Library()


@register.filter(name='add_attributes')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    if field:
        return field.as_widget(attrs=attrs)
    return ''
