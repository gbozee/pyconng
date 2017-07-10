# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import pytz
from django.conf.urls import include, url

from .import views

urlpatterns = [
    url(regex=r'online-payment/(?P<tutor_slug>[\w.@+-]+)/(?P<slug>[\w.@+-]+)/$',
        view=views.OnlinePaymentRedirectView.as_view(),
        name='dollar_online_payment'),
    url(regex=r'client-payment-completed/(?P<order>[\w.@+-]+)/$',
        view=csrf_exempt(views.ClientPaymentCompletedView.as_view()),
        name='request_complete_redirect'),
    url(regex=r'client-payment-cancelled/(?P<order>[\w.@+-]+)/$',
        view=csrf_exempt(views.FailedPaymentRedirectView.as_view()),
        name='request_cancelled_redirect'),
    
]
