# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from . import views
urlpatterns = [
    # Examples:
    # url(r'^404$', TemplateView.as_view(template_name='500.html'), name='404'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.TicketHomeView.as_view(), name='home'),
    url(r'^purchase/$', views.PurchaseView.as_view(), name='purchase'),
    url(r'^detail/$', views.TicketDetailPage.as_view(), name="detail"),
]
