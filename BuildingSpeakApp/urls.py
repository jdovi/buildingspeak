from django.conf.urls import patterns, include, url

from BuildingSpeakApp import views
from rtropo.views import message_received

# these url patterns deal only with BuildingSpeakApp/ web requests
# each app has its own urls.py file, which is called by the site's urls.py file
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^user-account$', views.user_account, name='user_account'),
    url(r'^update-successful$', views.update_successful, name='update_successful'),
    url(r'^application-error$', views.application_error, name='application_error'),
    url(r'^(?P<account_id>\d+)/$', views.account_detail, name='account_detail'),
    url(r'^(?P<account_id>\d+)/buildings/(?P<building_id>\d+)$', views.building_detail,
        name='building_detail'),
    url(r'^(?P<account_id>\d+)/spaces/(?P<space_id>\d+)$', views.space_detail,
        name='space_detail'),
    url(r'^(?P<account_id>\d+)/meters/(?P<meter_id>\d+)$', views.meter_detail,
        name='meter_detail'),
    url(r'^(?P<account_id>\d+)/equipments/(?P<equipment_id>\d+)$', views.equipment_detail,
        name='equipment_detail'),
    url(r'^(?P<account_id>\d+)/measures/(?P<measure_id>\d+)$', views.measure_detail,
        name='measure_detail'),
    url(r'^management/$', views.management, name='management'),
    url(r'^tropo_test_text/$', views.tropo_test_text, name='tropo_test_text'),
    url(r'^tropo_test_voice/$', views.tropo_test_voice, name='tropo_test_voice'),
    url(r"^tropo/$", message_received, kwargs={'backend_name': 'my-tropo-backend'},
        name='tropo'),
)
