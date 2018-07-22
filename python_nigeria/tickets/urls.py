# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Examples:
    # url(r'^404$', TemplateView.as_view(template_name='500.html'), name='404'),
    # url(r'^blog/', include('blog.urls')),
    url(r"^$", views.TicketHomeView.as_view(), name="home"),
    url(r"^selected-plan$", views.intermediate_purchase, name="selected-plan"),
    url(r"^coupons$", views.valid_coupons, name="coupons"),
    url(
        r"^purchase/$",
        login_required(csrf_exempt(views.PurchaseView.as_view())),
        name="purchase",
    ),
    url(
        r"^purchase-complete/(?P<order>[\w.@+-]+)/$",
        login_required(views.purchase_complete),
        name="purchase-complete",
    ),
    # url(r'^checkout/(?P<order>[\w.@+-]+)/$', views.CheckoutView.as_view(), name='checkout_view'),
    # url(r'^checkout/(?P<order>[\w.@+-]+)/$', login_required(views.CheckoutView.as_view()), name='checkout_view'),
    url(
        r"^detail/(?P<order>[\w.@+-]+)/$",
        login_required(views.TicketDetailPage.as_view()),
        name="detail",
    ),
    url(
        r"^create/(?P<order>[\w.@+-]+)/$",
        login_required(views.CreateTicketview.as_view()),
        name="create_ticket",
    ),
    url(
        r"^sales/(?P<pk>\d+)/$",
        login_required(views.SalesTicketView.as_view()),
        name="sales",
    ),
    url(
        r"^paystack/webhook",
        view=csrf_exempt(views.paystack_webhook),
        name="p_stack_webhook",
    ),
    url(
        r"^paystack/callback/$",
        view=csrf_exempt(views.paystack_webhook),
        name="p_stack_callback",
    ),
    url(
        r"^paystack/callback/(?P<order>[\w.@+-]+)/$",
        view=csrf_exempt(views.PaystackCallBackView.as_view()),
        name="callback_paystack",
    ),
    url(
        r"^paystack/validate/(?P<order>[\w.@+-]+)/(?P<code>[\w.@+-]+)$",
        view=login_required(views.validate_paystack_ref),
        name="validate_paystack",
    ),
]
