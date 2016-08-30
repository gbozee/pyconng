from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from symposion import views as symposion_views

urlpatterns = [

    # Examples:
    # url(r'^$', 'pyconng.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^account/', include('account.urls')),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^admin/', include(admin.site.urls)),

]

# symposion urls 
urlpatterns += [
    url(r'^dashboard/', symposion_views.dashboard, name='dashboard'),
    url(r'^proposals/', include('symposion.proposals.urls')),
    url(r'^reviews/', include('symposion.reviews.urls')),
    url(r'^schedule/', include('symposion.schedule.urls')),
    url(r'^speaker/', include('symposion.speakers.urls')),
    url(r'^sponsors/', include('symposion.sponsorship.urls')),
    url(r'^teams/', include('symposion.teams.urls')),
]

# Pinax urls
urlpatterns += [
    url(r'^boxes/', include('pinax.boxes.urls')),
    # url(r'^blog/', include('pinax.blog.urls')),
    url(r'^', include('pinax.pages.urls')),
]