from django.conf.urls import patterns, include, url
from django.contrib import admin
from timezone_field.fields import TimeZoneField
from django.views.generic import TemplateView

urlpatterns = [

    # Examples:
    # url(r'^$', 'pyconng.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^proposals/', include('symposion.proposals.urls')),
    url(r'^reviews/', include('symposion.reviews.urls')),
    url(r'^schedule/', include('symposion.schedule.urls')),
    url(r'^speaker/', include('symposion.speakers.urls')),
    url(r'^sponsors/', include('symposion.sponsorship.urls')),
    url(r'^teams/', include('symposion.teams.urls')),

]