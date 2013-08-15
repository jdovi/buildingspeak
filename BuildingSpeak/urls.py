from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# these url patterns point to the different apps loaded on this set
urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    # url(r'^$', 'BuildingSpeak.views.home', name='home'),
    url(r'', include('BuildingSpeakApp.urls')),
    url(r'^django-rq/', include('django_rq.urls')),
)
