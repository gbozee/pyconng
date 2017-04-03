# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from symposion import views as symposion_views
from django.views import defaults as default_views
from . import views as o_views

urlpatterns = [
    # Examples:
    # url(r'^404$', TemplateView.as_view(template_name='500.html'), name='404'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^home/$', TemplateView.as_view(template_name='home.html'), name='home_page'),
    url(r'^home/$', o_views.HomeRedirectView.as_view(), name='home_page'),
    url(r'^$', TemplateView.as_view(
        template_name='pre-conference.html'), name='home'),
    url(r'^account/', include('account.urls')),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [
    # Your stuff: custom urls includes go here
    url(r'^dashboard/', symposion_views.dashboard, name='dashboard'),
    url(r'^proposals/', include('symposion.proposals.urls')),
    url(r'^reviews/', include('symposion.reviews.urls')),
    # url(r'^schedule/', include('symposion.schedule.urls')),
    url(r'^speaker/', include('symposion.speakers.urls')),
    url(r'^sponsors/apply', o_views.sponsor_apply, name="sponsor_apply"),
    url(r'^sponsors/', include('symposion.sponsorship.urls')),
    url(r'^teams/', include('symposion.teams.urls')),

    url(r'^boxes/', include('pinax.boxes.urls')),
    url(r'^blog/', include('pinax.blog.urls', namespace="pinax_blog")),
    url(r'^', include('pinax.pages.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
