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
    # url(r'^schedule/$', o_views.ScheduleConferenceView.as_view(), name='schedule_conference'),
    url(r'^$', o_views.HomePage.as_view(), name='home'),
    url(r'^account/login/$', o_views.NewLoginView.as_view(), name='account_login'),
    url(r'^speaker/edit/(?:(?P<pk>\d+)/)?$', o_views.NewSpeakerEditView.as_view(),
        name='speaker_edit'),
        url(r'^hijack/', include('hijack.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^contact/', include('contact_form.urls')),
    # url(r'^captcha/', include('captcha.urls')),
    url(r'^we-are-allowed/', include(admin.site.urls)),
    url(r'^tickets/', include("python_nigeria.tickets.urls", namespace="tickets"))
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
    url(r'^dashboard/', o_views.dashboard, name='dashboard'),
    url(r'^proposals/', include('symposion.proposals.urls')),
    # url(r'^reviews/section/(?P<section_slug>[\w\-]+)/all/$', o_views.review_section, {"reviewed": "all"}, name="review_section"),
    
    url(r'^reviews/', include('symposion.reviews.urls')),
    url(r'^schedule/', include('symposion.schedule.urls')),
    url(r'^speaker/', include('symposion.speakers.urls')),
    url(r'^sponsors/apply', o_views.sponsor_apply, name="sponsor_apply"),
    url(r'^sponsors/', include('symposion.sponsorship.urls')),
    url(r'^teams/', include('symposion.teams.urls')),
    url(r'^boxes/', include('pinax.boxes.urls')),
    url(r"^blog/manage/posts/create/$", o_views.ManageCreatePost.as_view(), name="manage_post_create"),
    url(r"^blog/manage/posts/(?P<post_pk>\d+)/update/$", o_views.ManageUpdatePost.as_view(), name="manage_post_update"),

    url(r'^blog/', include('pinax.blog.urls', namespace="pinax_blog")),
    url(r'^', include('pinax.pages.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
