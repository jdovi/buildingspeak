from django.conf.urls import patterns, url
from django.conf import settings

from BuildingSpeakApp import views

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
    url(r'^(?P<account_id>\d+)_1/$', views.account_detail_1, name='account_detail_1'),

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

    url(r'^tropo/index/$', views.tropo_index, name='tropo_index'),
    url(r'^tropo/user/(?P<caller_id>\d+)/$', views.tropo_user, name='tropo_user'),
    url(r'^tropo/user/(?P<caller_id>\d+)/catch-account/$',
        views.tropo_catch_account, name='tropo_catch_account'),
    url(r'^tropo/user/(?P<caller_id>\d+)/account/(?P<account_id>\d+)/catch-topic/$',
        views.tropo_catch_topic, name='tropo_catch_topic'),
    url(r'^tropo/user/(?P<caller_id>\d+)/account/(?P<account_id>\d+)/(?P<topic>[a-z]+)/catch-instance/$',
        views.tropo_catch_instance, name='tropo_catch_instance'),
    url(r'^tropo/user/(?P<caller_id>\d+)/account/(?P<account_id>\d+)/(?P<topic>[a-z]+)/(?P<model_id>\d+)/catch-request-type/$',
        views.tropo_catch_request_type, name='tropo_catch_request_type'),
    url(r'^tropo/user/(?P<caller_id>\d+)/account/(?P<account_id>\d+)/(?P<topic>[a-z]+)/(?P<model_id>\d+)/request-type/(?P<request_type>[1-2]+)/catch-request/$',
        views.tropo_catch_request, name='tropo_catch_request'),
    
    url(r'^ajaxexample$', views.main, name='main'),
    url(r'^ajaxexample_json$', views.ajax, name='ajax'),
    url(r'^time_test$', views.time_test, name='time_test'),

)

