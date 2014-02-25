from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
import socket

from BuildingSpeakApp.models import Account, Building, Space, Meter, Equipment, WeatherStation, EfficiencyMeasure, Monthling
from BuildingSpeakApp.models import UserSettingsForm, MeterDataUploadForm
from BuildingSpeakApp.models import get_model_key_value_pairs_as_nested_list, decimal_isnan, nan2zero
from BuildingSpeakApp.models import get_monthly_dataframe_as_table, get_df_as_table_with_formats

import json, stripe
from numpy import NaN
import numpy as np
import pandas as pd
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from tropo import Tropo, Session, Result
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from time import sleep
from pytz import UTC
from datetime import datetime
if 'heroku' in settings.DJANGO_ROOT:
    from rq import Queue
    from worker import conn


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_pk = settings.STRIPE_PUBLISHABLE_KEY

class ResultsMessage(object):
    """Used for generating user
    feedback messages that do
    not need to be stored as
    messages in the database."""
    id = 0
    subject = 'Success!'
    comment = ''
    
def time_test(request):
    t0 = timezone.now()
    account = Account.objects.all()[0] #get Account
    t1 = timezone.now()
    accounts = request.user.account_set.order_by('id') #get User's Accounts
    t2 = timezone.now()
    buildings = account.building_set.order_by('name') #get Account's Buildings
    t3 = timezone.now()
    spaces = Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name') #get Account's Spaces
    t4 = timezone.now()
    meters = account.meter_set.order_by('name') #get Account's Meters
    t5 = timezone.now()
    equipments = Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name') #get Account's Equipments
    t6 = timezone.now()
    measures = EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name') #get Account's Measures
    t7 = timezone.now()
    meter = Meter.objects.get(name='Eden I (electric)') #get Meter
    t8 = timezone.now()
    meter_df = meter.get_bill_data_period_dataframe() #get Meter's dataframe
    t9 = timezone.now()
    meter_monthlings = Monthling.objects.filter(monther=meter.monther_set.get(name='BILLx')) #get Meter's monthlings
    t10 = timezone.now()
    
    context = {
        'user':           request.user,
        'account':        account,
        'accounts':       accounts,
        'buildings':      buildings,
        'spaces':         spaces,
        'meters':         meters,
        'equipments':     equipments,
        'measures':       measures,
        'meter':          meter,
        'meter_df':       meter_df,
        'meter_monthlings': meter_monthlings,
        'results_set': [['get Account',             '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0)],
                        ["get User's Accounts",    '{0:,.0f}'.format((t2-t1).seconds*1000.0 + (t2-t1).microseconds/1000.0)],
                        ["get Account's Buildings",   '{0:,.0f}'.format((t3-t2).seconds*1000.0 + (t3-t2).microseconds/1000.0)],
                        ["get Account's Spaces",      '{0:,.0f}'.format((t4-t3).seconds*1000.0 + (t4-t3).microseconds/1000.0)],
                        ["get Account's Meters",      '{0:,.0f}'.format((t5-t4).seconds*1000.0 + (t5-t4).microseconds/1000.0)],
                        ["get Account's Equipments",  '{0:,.0f}'.format((t6-t5).seconds*1000.0 + (t6-t5).microseconds/1000.0)],
                        ["get Account's Measures",    '{0:,.0f}'.format((t7-t6).seconds*1000.0 + (t7-t6).microseconds/1000.0)],
                        ["get Meter",               '{0:,.0f}'.format((t8-t7).seconds*1000.0 + (t8-t7).microseconds/1000.0)],
                        ["get Meter's monthlings in pandas dataframe",       '{0:,.0f}'.format((t9-t8).seconds*1000.0 + (t9-t8).microseconds/1000.0)],
                        ["get Meter's monthlings directly",    '{0:,.0f}'.format((t10-t9).seconds*1000.0 + (t10-t9).microseconds/1000.0)],
                         ]
    }
    return render(request, 'buildingspeakapp/time_test.html', context)
    
def main(request):
    return render_to_response('buildingspeakapp/ajaxexample.html', context_instance=RequestContext(request))
    
def ajax(request):
#    if request.POST.has_key('client_response'):
#        x = request.POST['client_response']
#        y = socket.gethostbyname(x)
#        response_dict = {}
#        response_dict.update({'server_response': y })
#        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
#    else:
#        return render_to_response('buildingspeakapp/ajaxexample.html', context_instance=RequestContext(request))
    if request.POST.has_key('client_response'):
        x = request.POST['client_response']
        if x == 'first_script':
            sleep(10)
            response_dict = {}
            response_dict.update({'server_response': request.user.username })
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
        elif x == 'second_script':
            sleep(12)
            response_dict = {}
            response_dict.update({'server_response': 'abcd' })
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        return render_to_response('buildingspeakapp/ajaxexample.html', context_instance=RequestContext(request))

@login_required
def index(request):
    accounts = request.user.account_set.order_by('id')
    if len(accounts)==0:
        return HttpResponseRedirect('/user-account')
    else:
        return HttpResponseRedirect('/' + str(accounts[0].id))

@login_required
def user_account(request):
    current_user = request.user
    if request.method == 'POST': # If the form has been submitted...
        form = UserSettingsForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            if form.cleaned_data['image_file'] is None:
                if current_user.userprofile.image_file is None:
                    latest_image_file = None
                else:
                    latest_image_file = current_user.userprofile.image_file
            else:
                latest_image_file = form.cleaned_data['image_file']
            current_user.__setattr__('username', form.cleaned_data['username'])
            current_user.__setattr__('email', form.cleaned_data['email'])
            current_user.userprofile.__setattr__('mobile_phone', form.cleaned_data['mobile_phone'])
            current_user.userprofile.__setattr__('desk_phone', form.cleaned_data['desk_phone'])
            current_user.__setattr__('first_name', form.cleaned_data['first_name'])
            current_user.__setattr__('last_name', form.cleaned_data['last_name'])
            current_user.userprofile.__setattr__('organization', form.cleaned_data['organization'])
            current_user.userprofile.__setattr__('image_file', latest_image_file)
            form.initial['image_file'] = latest_image_file
            current_user.save()
            current_user.userprofile.save()
            m = ResultsMessage()
            m.comment = 'User settings have been updated.'
            reloading = True
    elif request.method == 'GET':
        if current_user.userprofile.image_file is None:
            latest_image_file = None
        else:
            latest_image_file = current_user.userprofile.image_file
        form = UserSettingsForm({'username': current_user.username,
                                 'email': current_user.email,
                                 'mobile_phone': current_user.userprofile.mobile_phone,
                                 'desk_phone': current_user.userprofile.desk_phone,
                                 'first_name': current_user.first_name,
                                 'last_name': current_user.last_name,
                                 'organization': current_user.userprofile.organization},
                                 {'image_file': latest_image_file})
        reloading = False
    context = {
        'user':     request.user,
        'accounts': request.user.account_set.order_by('id'),
        'form':     form, }
    if reloading: context['alerts'] = [m]
    return render(request, 'buildingspeakapp/user_account.html', context)
        
@login_required
def update_successful(request):
    context  = {'user': request.user}
    return render(request, 'buildingspeakapp/update_successful.html', context)

def application_error(request):
    context  = {'user': request.user}
    return render(request, 'buildingspeakapp/application_error.html', context)

@login_required
def account_detail(request, account_id):
    t0 = timezone.now()
    account = get_object_or_404(Account, pk=account_id)
    total_SF = account.building_set.all().aggregate(Sum('square_footage'))['square_footage__sum']
    
    account_attrs = get_model_key_value_pairs_as_nested_list(account)

    t1 = timezone.now()
    
    bldg_data = []
    for bldg in account.building_set.order_by('name'):
        month_curr = pd.Period(Monthling.objects.exclude(act_cost = Decimal(NaN))
                                                .filter(monther__meter__building = bldg)
                                                .latest('when')
                                                .when,
                               freq='M')                #latest month with non-NaN 'Cost (act)' data
        month_prev = month_curr - 1
        bldg_view_data_curr = bldg.get_building_view_meter_data(month_first = month_curr,
                                                                month_last = month_curr)
        if bldg_view_data_curr is None: bldg_view_data_curr = [False, False]
        bldg_view_data_prev = bldg.get_building_view_meter_data(month_first = month_prev,
                                                                month_last = month_prev)
        if bldg_view_data_prev is None: bldg_view_data_prev = [False, False]
        bldg_data.append([bldg,
                          bldg_view_data_curr[0],
                          bldg_view_data_curr[1],
                          month_curr.strftime('%b-%Y'),
                          bldg_view_data_prev[0],
                          bldg_view_data_prev[1],
                          month_prev.strftime('%b-%Y'),
                          ])
    
    t2 = timezone.now()

    month_first = pd.Period(timezone.now(),freq='M')-40     #first month in sequence
    month_last = month_first + 40+24                            #final month in sequence
    acct_view_data = account.get_account_view_meter_data(month_first=month_first,
                                                         month_last=month_last)
    t3 = timezone.now()
    five_year_data = account.get_account_view_five_year_data()
    t4 = timezone.now()
    if acct_view_data is None:
        meter_data = None
        pie_data = None
    else:
        meter_data = acct_view_data[0]
        pie_data = acct_view_data[1]
    #####Stripe testing
    t5 = timezone.now()
    if request.method == 'POST':
        print request.POST['stripeToken']
        try:
            stripe_customer = stripe.Customer.retrieve(account.stripe_customer_id)
            stripe_customer.card = request.POST['stripeToken']
            stripe_customer.save()
        except:
            stripe_customer = stripe.Customer.create(
                card = request.POST['stripeToken'],
                description = 'AccountID:' + str(account.id)
            )
            account.__setattr__('stripe_customer_id', stripe_customer.id)
            account.save()
    #####Stripe testing
    t6 = timezone.now()
    if (account.stripe_customer_id is not None) and (account.stripe_customer_id != ''):
        charge = stripe.Charge.create(
            amount = timezone.now().minute * 100,
            currency = 'usd',
            customer = account.stripe_customer_id,
            description = 'Account ' + str(account.id) + ': test payment $' + str(timezone.now().minute * 100)
            )
    t7 = timezone.now()
    context = {
        'user':           request.user,
        'account':        account,
        'accounts':       request.user.account_set.order_by('id'),
        'buildings':      account.building_set.order_by('name'),
        'spaces':         Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'meters':         account.meter_set.order_by('name'),
        'equipments':     Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'measures':       EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        
        'alerts':         account.get_all_alerts(reverse_boolean=True),
        'events':         account.get_all_events(reverse_boolean=True),
        'account_attrs':  account_attrs,
        'bldg_data':      bldg_data,
        'meter_data':     meter_data,
        'pie_data':       pie_data,
        'total_SF':       total_SF,
        'five_year_data': five_year_data,
        'motion_data_meters':       account.get_account_view_motion_table_meters(),
        'motion_data_fuels':        account.get_account_view_motion_table_fuels(),
        'motion_data_buildings':    account.get_account_view_motion_table_buildings(),
        'motion_data_spaces':       account.get_account_view_motion_table_spaces(),
        'stripe_pk':                stripe_pk,
        'results_set': [['get Account, SF, attrs',      '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0)],
                        ['bldg data curr/prev',         '{0:,.0f}'.format((t2-t1).seconds*1000.0 + (t2-t1).microseconds/1000.0)],
                        ['get Account view meter data', '{0:,.0f}'.format((t3-t2).seconds*1000.0 + (t3-t2).microseconds/1000.0)],
                        ['get Account 5yr data',        '{0:,.0f}'.format((t4-t3).seconds*1000.0 + (t4-t3).microseconds/1000.0)],
                        ['extracting results',          '{0:,.0f}'.format((t5-t4).seconds*1000.0 + (t5-t4).microseconds/1000.0)],
                        ['Stripe get/create customer',  '{0:,.0f}'.format((t6-t5).seconds*1000.0 + (t6-t5).microseconds/1000.0)],
                        ['Stripe create charge',        '{0:,.0f}'.format((t7-t6).seconds*1000.0 + (t7-t6).microseconds/1000.0)],
                        ],
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/account_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

@login_required
def building_detail(request, account_id, building_id):
    account = get_object_or_404(Account, pk=account_id)
    building = get_object_or_404(Building, pk=building_id)
    if account.pk <> building.account.pk:
        raise Http404

    building_attrs = get_model_key_value_pairs_as_nested_list(building)
    month_first = pd.Period(timezone.now(),freq='M')-40     #first month in sequence
    month_last = month_first + 40+24                            #final month in sequence
    
    bldg_view_data = building.get_building_view_meter_data(month_first=month_first,
                                                           month_last=month_last)
    five_year_data = building.get_building_view_five_year_data()
    
    if bldg_view_data is None:
        meter_data = None
        pie_data = None
    else:
        meter_data = bldg_view_data[0]
        pie_data = bldg_view_data[1]
        
    context = {
        'user':           request.user,
        'account':        account,
        'accounts':       request.user.account_set.order_by('id'),
        'buildings':      account.building_set.order_by('name'),
        'spaces':         Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'meters':         account.meter_set.order_by('name'),
        'equipments':     Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'measures':       EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),

        'alerts':         building.get_all_alerts(reverse_boolean=True),
        'events':         building.get_all_events(reverse_boolean=True),
        'building':             building,
        'building_measures':    EfficiencyMeasure.objects.filter(Q(equipments__buildings=building) | Q(meters__building=building)).distinct().order_by('name'),
        'building_spaces':      building.space_set.order_by('name'),
        'building_attrs':       building_attrs,
        'meter_data':           meter_data,
        'pie_data':             pie_data,
        'five_year_data':       five_year_data,
        'motion_data_meters':   building.get_building_view_motion_table_meters(),
        'motion_data_fuels':    building.get_building_view_motion_table_fuels(),
        'motion_data_spaces':   building.get_building_view_motion_table_spaces(),
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/building_detail.html'
        #template_name = 'buildingspeakapp/dashboard_test3.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

@login_required
def space_detail(request, account_id, space_id):
    account = get_object_or_404(Account, pk=account_id)
    space = get_object_or_404(Space, pk=space_id)
    if account.pk <> space.building.account.pk:
        raise Http404
        
    space_attrs = get_model_key_value_pairs_as_nested_list(space)
    month_first = pd.Period(timezone.now(),freq='M')-40     #first month in sequence
    month_last = month_first + 40 + 24                            #final month in sequence
    
    space_view_data = space.get_space_view_meter_data(month_first=month_first,
                                                      month_last=month_last)
    five_year_data = space.get_space_view_five_year_data()
    
    if space_view_data is None:
        meter_data = None
        pie_data = None
    else:
        meter_data = space_view_data[0]
        pie_data = space_view_data[1]
    
    context = {
        'user':           request.user,
        'account':        account,
        'accounts':       request.user.account_set.order_by('id'),
        'buildings':      account.building_set.order_by('name'),
        'spaces':         Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'meters':         account.meter_set.order_by('name'),
        'equipments':     Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'measures':       EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        
        'alerts':         space.get_all_alerts(reverse_boolean=True),
        'events':         space.get_all_events(reverse_boolean=True),
        'space':          space,
        'space_measures': EfficiencyMeasure.objects.filter(Q(equipments__spaces=space) | Q(meters__space=space)).distinct().order_by('name'),
        'space_attrs':    space_attrs,
        'meter_data':     meter_data,
        'pie_data':       pie_data,
        'five_year_data': five_year_data,
        'motion_data_meters':   space.get_space_view_motion_table_meters(),
        'motion_data_fuels':    space.get_space_view_motion_table_fuels(),
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/space_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

@login_required
def meter_detail(request, account_id, meter_id):
    #---check that we can access the account and meter and they go together
    account = get_object_or_404(Account, pk=account_id)
    meter = get_object_or_404(Meter, pk=meter_id)
    if account.pk <> meter.account.pk:
        raise Http404
    #---branching for POST vs. GET request
    if request.method == 'POST': # If the form has been submitted...
        form = MeterDataUploadForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            if form.cleaned_data['bill_data_file'] is None:
                if meter.bill_data_file is None:
                    latest_bill_data_file = None
                else:
                    latest_bill_data_file = meter.bill_data_file
            else:
                latest_bill_data_file = form.cleaned_data['bill_data_file']
            meter.__setattr__('bill_data_file', latest_bill_data_file)
            form.initial['bill_data_file'] = latest_bill_data_file
            meter.save()
            try:
                if 'heroku' in settings.DJANGO_ROOT:
                    q = Queue(connection=conn)
                    result = q.enqueue(meter.upload_bill_data)
                else:
                    meter.upload_bill_data()
                m = ResultsMessage()
                m.comment = 'Bill data has been uploaded.'
            except:
                m = ResultsMessage()
                m.subject = 'Error!'
                m.comment = 'Bill data upload failed.'
            reloading = True
    elif request.method == 'GET':
        if meter.bill_data_file is None:
            latest_bill_data_file = None
        else:
            latest_bill_data_file = meter.bill_data_file
        form = MeterDataUploadForm({}, {'bill_data_file': latest_bill_data_file})
        reloading = False
        
    
    meter_attrs = get_model_key_value_pairs_as_nested_list(meter)
    
    try:
        this_month = pd.Period(timezone.now(),freq='M')
        month_first = this_month - 36       #link user selection here
        month_last = this_month +36+24   #link user selection here
        
        #this dataframe provides the foundational meter dataset; if no data, skip everything
        bill_data = meter.get_bill_data_period_dataframe(first_month = month_first.strftime('%m/%Y'), 
                                                         last_month = month_last.strftime('%m/%Y'))
        if bill_data is None:
            totals_table = False
            ratios_table = False
            cost_by_month = False
            consumption_by_month = False
            demand_by_month = False
            kbtu_by_month = False
            kbtuh_by_month = False
            consumption_residual_plots = None  #iterables in templates need None
            peak_demand_residual_plots = None  #iterables in templates need None
            consumption_model_stats_table = False
            peak_demand_model_stats_table = False
            consumption_model_residuals_histogram = False
            peak_demand_model_residuals_histogram = False
            five_year_table_cost = None
            five_year_table_cons = None
            five_year_table_kBtu = None
            motion_data = None
        else:
            meter_data =        meter.get_meter_view_meter_data(bill_data = bill_data)
            model_data =        meter.get_meter_view_meter_model_data(bill_data = bill_data)
            five_year_data =    meter.get_meter_view_five_year_data(bill_data = bill_data)
            motion_data =       meter.get_meter_view_motion_table(bill_data = bill_data)
            if meter_data is None:
                totals_table = False
                ratios_table = False
                cost_by_month = False
                consumption_by_month = False
                demand_by_month = False
                kbtu_by_month = False
                kbtuh_by_month = False
            else:
                totals_table = meter_data[0]
                ratios_table = meter_data[1]
                cost_by_month = meter_data[2]
                consumption_by_month = meter_data[3]
                demand_by_month = meter_data[4]
                kbtu_by_month = meter_data[5]
                kbtuh_by_month = meter_data[6]
            if model_data is None:
                consumption_residual_plots = None  #iterables in templates need None
                peak_demand_residual_plots = None  #iterables in templates need None
                consumption_model_stats_table = False
                peak_demand_model_stats_table = False
                consumption_model_residuals_histogram = False
                peak_demand_model_residuals_histogram = False
            else:
                consumption_residual_plots = model_data[0]
                peak_demand_residual_plots = model_data[1]
                consumption_model_stats_table = model_data[2]
                peak_demand_model_stats_table = model_data[3]
                consumption_model_residuals_histogram = model_data[4]
                peak_demand_model_residuals_histogram = model_data[5]
            if five_year_data is None:
                five_year_table_cost = None
                five_year_table_cons = None
                five_year_table_kBtu = None
            else:
                five_year_table_cost = five_year_data[0]
                five_year_table_cons = five_year_data[1]
                five_year_table_kBtu = five_year_data[2]
    except:
        totals_table = False
        ratios_table = False
        cost_by_month = False
        consumption_by_month = False
        demand_by_month = False
        kbtu_by_month = False
        kbtuh_by_month = False
        consumption_residual_plots = None  #iterables in templates need None
        peak_demand_residual_plots = None  #iterables in templates need None
        consumption_model_stats_table = False
        peak_demand_model_stats_table = False
        consumption_model_residuals_histogram = False
        peak_demand_model_residuals_histogram = False
        five_year_table_cost = None
        five_year_table_cons = None
        five_year_table_kBtu = None
        motion_data = None
        
    context = {
        'user':           request.user,
        'account':        account,
        'accounts':       request.user.account_set.order_by('id'),
        'buildings':      account.building_set.order_by('name'),
        'spaces':         Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'meters':         account.meter_set.order_by('name'),
        'equipments':     Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'measures':       EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        
        'alerts':         meter.get_all_alerts(reverse_boolean=True),
        'events':         meter.get_all_events(reverse_boolean=True),
        'form':                     form,
        'meter':                    meter,
        'meter_attrs':              meter_attrs,

        'totals_table':             json.dumps(totals_table),
        'ratios_table':             json.dumps(ratios_table),
        'cost_by_month':           json.dumps(cost_by_month),
        'consumption_by_month':    json.dumps(consumption_by_month),
        'demand_by_month':         json.dumps(demand_by_month),
        'kbtu_by_month':           json.dumps(kbtu_by_month),
        'kbtuh_by_month':          json.dumps(kbtuh_by_month),

        'consumption_units':       json.dumps(meter.units.split(',')[1]),
        'demand_units':            json.dumps(meter.units.split(',')[0]),

        'consumption_residual_plots':           consumption_residual_plots,
        'peak_demand_residual_plots':           peak_demand_residual_plots,
        'consumption_model_stats_table':        json.dumps(consumption_model_stats_table),
        'peak_demand_model_stats_table':        json.dumps(peak_demand_model_stats_table),
        'consumption_model_residuals_histogram':    json.dumps(consumption_model_residuals_histogram),
        'peak_demand_model_residuals_histogram':    json.dumps(peak_demand_model_residuals_histogram),

        'five_year_table_cost':                     five_year_table_cost,
        'five_year_table_cons':                     five_year_table_cons,
        'five_year_table_kBtu':                     five_year_table_kBtu,

        'motion_data':                              motion_data,
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/meter_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    if reloading: context['alerts'] = [m]
    return render(request, template_name, context)

@login_required
def equipment_detail(request, account_id, equipment_id):
    account = get_object_or_404(Account, pk=account_id)
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if account.pk <> equipment.meters.all()[0].account.pk: 
        #need to close loophole here: Equipments not forced to single Account
        #here we assume only one so pick the first Meter we find and get its Account
        #could add code (here?) to confirm all connected meters share same Account and flag if not
        raise Http404

    equipment_attrs = get_model_key_value_pairs_as_nested_list(equipment)
        
    context = {
        'user':           request.user,
        'account':        account,
        'accounts':       request.user.account_set.order_by('id'),
        'buildings':      account.building_set.order_by('name'),
        'spaces':         Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'meters':         account.meter_set.order_by('name'),
        'equipments':     Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'measures':       EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),

        'alerts':         equipment.get_all_alerts(reverse_boolean=True),
        'events':         equipment.get_all_events(reverse_boolean=True),
        'equipment':      equipment,
        'equipment_attrs': equipment_attrs,
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/equipment_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

@login_required
def measure_detail(request, account_id, measure_id):
    #---check that we can access the account and meter and they go together
    account = get_object_or_404(Account, pk=account_id)
    measure = get_object_or_404(EfficiencyMeasure, pk=measure_id)
    if account.pk <> measure.meters.all()[0].account.pk: 
        #need to close loophole here: Measures not forced to single Account
        #here we assume only one so pick the first Meter we find and get its Account
        #could add code (here?) to confirm all connected meters share same Account and flag if not
        raise Http404
    
    measure_attrs = get_model_key_value_pairs_as_nested_list(measure)
    
    context = {
        'user':           request.user,
        'account':        account,
        'accounts':       request.user.account_set.order_by('id'),
        'buildings':      account.building_set.order_by('name'),
        'spaces':         Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'meters':         account.meter_set.order_by('name'),
        'equipments':     Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),
        'measures':       EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name'),

        'measure':              measure,
        'measure_attrs':        measure_attrs,
        'measure_buildings':    Building.objects.filter(Q(meters__efficiencymeasure=measure) | Q(equipment__efficiencymeasure=measure)).distinct().order_by('name'),
        'measure_spaces':       Space.objects.filter(Q(meters__efficiencymeasure=measure) | Q(equipment__efficiencymeasure=measure)).distinct().order_by('name'),

    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/measure_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

@login_required
def management(request):
    context = {
        'weather_stations':     WeatherStation.objects.all(),
        'accounts':             request.user.account_set.order_by('id'),
    }
    if request.user in User.objects.filter(is_active = True).filter(is_staff = True).filter(is_superuser = True):
        template_name = 'buildingspeakapp/management.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

@login_required
def docs(request):

    context = {
        'user':         request.user,
#        'accounts':     request.user.account_set.order_by('id'),
#        'meter_data':   meter_data,
#        'pie_data':     pie_data,
        'building':     Building.objects.get(pk=2),
#        'mydata':       mydata2,
#        'start_month':  start_month
    }
    template_name = 'buildingspeakapp/tropo_test.html'
    return render(request, template_name, context)


######-----------------------------------------------Tropo messaging views
@csrf_exempt
def tropo_index(request):
    """
    Tropo view to catch initial incoming SMS or
    voice and discard initial 'activating' SMS.
    """
    #capture session and extract caller ID, dropping leading country code if present
    s = Session(request.body)
    caller_id = s.fromaddress['id']
    if len(caller_id) == 11: caller_id = caller_id[1:]
    #create Tropo object that will be used to generate JSON responses to Tropo
    t = Tropo()
    #for SMS, must catch the very first text that activates the session and discard
    t.ask(attempts = 1, choices = "[ANY]", timeout = 60, name = "catch", say = "")
    #now that the first text is caught, move into the system via the tropo_entry function
    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/')
    t.on(event = 'incomplete', say = "Sorry, something's gone wrong. Please try again later or call support. Goodbye.")
    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later or call support. Goodbye.")
    return HttpResponse(t.RenderJson())

@csrf_exempt
def tropo_user(request, caller_id):
    """
    Primary entry point into Tropo views. Hangs up on
    caller IDs not found in BuildingSpeak.
    """
    t = Tropo()
    try:
        this_user = User.objects.get(userprofile__mobile_phone = caller_id)
        if this_user.first_name == '':
            their_name = this_user.username
        else:
            their_name = this_user.first_name
    except:
        this_user = 0
        t.say("I'm not authorized to speak to you. Goodbye.")
    else:
        if len(this_user.account_set.all()) == 0:
            t.say("Hey " + their_name + ". You're not assigned to any account, so I can't do much for you. Please call support to get assigned to your account.")
        elif this_user.account_set.count() == 1:
            t.ask(attempts = 2,
                  timeout = 30,
                  choices = 'Account, Building, Buildings, Meter, Meters, Space, Spaces, Equipment, Equipments, Measure, Measures',
                  say = "Hey " + their_name + ". I can discuss " + str(this_user.account_set.all()[0]) + " with you. Want info about the Account, Buildings, Meters, Spaces, Equipment, or Measures?")
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(this_user.account_set.all()[0].pk) + '/catch-topic/')
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
        elif this_user.account_set.count() < 4:
            t.ask(attempts = 2,
                  timeout = 30,
                  choices = "[1-6 DIGITS]",
                  say = "Hey " + their_name + ". You have access to " + str(this_user.account_set.count()) + " accounts. Please enter one of these Account ID numbers: " + "; ".join([str(i.id) + ') ' + str(i) for i in this_user.account_set.all()]) + ".")
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/catch-account/')
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
        elif this_user.account_set.count() >= 4:
            t.ask(attempts = 2,
                  timeout = 30,
                  choices = "[1-6 DIGITS]",
                  say = "Hey " + their_name + ". You have access to " + str(this_user.account_set.count()) + " accounts. Please enter the Account ID (1-6 digits) you wish to discuss.")
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/catch-account/')
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
    return HttpResponse(t.RenderJson())
    
@csrf_exempt
def tropo_catch_account(request, caller_id):
    print request.body
    r = Result(request.body)
    t = Tropo()
    actions = r._actions
    print actions
    if type(actions) is list:
        r_dict = actions[0]
    else:
        r_dict = actions
    print r_dict
    print r_dict['disposition']
    if r_dict['disposition'] != 'SUCCESS': #only process if previous ask was successful
        t.hangup()
    else:
        try:
            print 'ca3'
            this_user = User.objects.get(userprofile__mobile_phone = caller_id)
            print 'ca4'
            account_id = r.getValue()
            print 'ca4'
            account = get_object_or_404(Account, pk = account_id)
            print 'ca5'
            if account not in this_user.account_set.all(): raise ValueError
            print 'ca6'
            t.ask(attempts = 2,
                  timeout = 30,
                  choices = 'Account, Building, Buildings, Meter, Meters, Space, Spaces, Equipment, Equipments, Measure, Measures',
                  say = "Ok, we'll discuss " + str(account.name) + ". Want info about the Account, Buildings, Meters, Spaces, Equipment, or Measures?")
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + account_id + '/catch-topic/')
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
            print 'ca7'
        except:
            print 'ca8'
            t.say("I'm sorry. That's not a valid selection for you...")
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/')
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
    print 'ca9'
    return HttpResponse(t.RenderJson())
    
@csrf_exempt
def tropo_catch_topic(request, caller_id, account_id):
    print request.body
    r = Result(request.body)
    t = Tropo()
    actions = r._actions
    print actions
    if type(actions) is list:
        r_dict = actions[0]
    else:
        r_dict = actions
    print r_dict
    print r_dict['disposition']
    if r_dict['disposition'] != 'SUCCESS': #only process if previous ask was successful
        t.hangup()
    else:
        try:
            print 'ct03'
            topic = r.getValue()
            print 'ct04'
            topic = topic.lower()
            print 'ct05'
            if topic[-1] != 's': topic = topic + 's'
            print 'ct06'
            topic_lower_plural = topic
            print 'ct07'
            topic_lower_singular = topic[0:-1]
            print 'ct08'
            topic_capital_singular = topic[0:-1].capitalize()
            print 'ct09'
            topic_capital_plural = topic.capitalize()
            print 'ct10'
            
            account = get_object_or_404(Account, pk = account_id)
            print 'ct11'
        except:
            print 'ct12'
            t.say("I'm sorry. That's not a valid selection for you...")
            print 'ct13'
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/')
            print 'ct14'
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
        else:
            print 'ct15'
            if topic_lower_singular == 'account': #if account, we already know which account, skip ask/say and call next page
                print 'ct16'
                t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account.id) + '/accounts/' + str(account.id))
                print 'ct17'
                t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
            else:
                print 'ct18'
                if topic_lower_singular == 'building': existing_models = account.building_set.order_by('name')
                elif topic_lower_singular == 'space': existing_models = Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name')
                elif topic_lower_singular == 'meter': existing_models = account.meter_set.order_by('name')
                elif topic_lower_singular == 'equipment': existing_models = Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name')
                elif topic_lower_singular == 'measure': existing_models = EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name')
                
                print 'ct23'
                if existing_models.count() == 0: #if no models, loop back to pick different topic
                    print 'ct24'
                    t.ask(attempts = 2,
                          timeout = 30,
                          choices = 'Account, Building, Buildings, Meter, Meters, Space, Spaces, Equipment, Equipments, Measure, Measures',
                          say = "You don't have access to any " + topic_capital_plural + ". Please choose a different topic: Account, Buildings, Meters, Spaces, Equipment, or Measures?")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account.id) + '/catch-topic/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
                    print 'ct25'
                elif existing_models.count() == 1: #if ony 1 model, skip ask and pick that one
                    print 'ct26'
                    t.say("Ok, we'll discuss your " + topic_capital_singular + " named " + existing_models[0].name + "...")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account.id) + '/' + topic_lower_plural + '/catch-instance/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
                    print 'ct27'
                elif existing_models.count() < 4: #if < 3 models, show all and ask to pick one
                    print 'ct28'
                    t.ask(attempts = 2,
                          timeout = 30,
                          choices = "[1-6 DIGITS]",
                          say = "You have access to " + str(existing_models.count()) + " " + topic_capital_plural + ". Please enter one of these " + topic_capital_singular + " ID numbers: " + "; ".join([str(i.id) + ') ' + str(i.name) for i in existing_models]) + ".")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account.id) + '/' + topic_lower_plural + '/catch-instance/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
                    print 'ct29'
                elif existing_models.count() >= 4: #if >= 4 models, ask to enter ID number directly
                    print 'ct30'
                    t.ask(attempts = 2,
                          timeout = 30,
                          choices = "[1-6 DIGITS]",
                          say = "You have access to " + str(existing_models.count()) + " " + topic_capital_plural + ". Please enter the " + topic_capital_singular + " ID (1-6 digits) you wish to discuss.")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account.id) + '/' + topic_lower_plural + '/catch-instance/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
    print 'ct31'
    return HttpResponse(t.RenderJson())

@csrf_exempt
def tropo_catch_instance(request, caller_id, account_id, topic):
    print request.body
    r = Result(request.body)
    t = Tropo()
    actions = r._actions
    print actions
    if type(actions) is list:
        r_dict = actions[0]
    else:
        r_dict = actions
    print r_dict
    print r_dict['disposition']
    if r_dict['disposition'] != 'SUCCESS': #only process if previous ask was successful
        t.hangup()
    else:
        print 'ci3'
        topic_lower_plural = topic
        print 'ci4'
        topic_lower_singular = topic[0:-1]
        print 'ci5'
        topic_capital_singular = topic[0:-1].capitalize()
        print 'ci6'
        topic_capital_plural = topic.capitalize()
        print 'ci7'
        account = get_object_or_404(Account, pk = account_id)
        print 'ci8'
        
        if topic == 'accounts': #if accounts, we already knew which one, so we didn't ask and there's no r.getValue()
            print 'ci9'
            t.ask(attempts = 2,
                  timeout = 30,
                  choices = "[1 DIGIT]",
                  say = "Do you want 1) performance data or 2) " + topic_capital_singular + " information? (select 1 or 2)")
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account_id) + '/accounts/' + str(account_id) + '/catch-request-type/')
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
            print 'ci10'
        else:
            print 'ci11'
            if topic_lower_singular == 'building': existing_models = account.building_set.order_by('name')
            elif topic_lower_singular == 'space': existing_models = Space.objects.filter(Q(building__account=account) | Q(meters__account=account)).distinct().order_by('name')
            elif topic_lower_singular == 'meter': existing_models = account.meter_set.order_by('name')
            elif topic_lower_singular == 'equipment': existing_models = Equipment.objects.filter(Q(buildings__account=account) | Q(meters__account=account)).distinct().order_by('name')
            elif topic_lower_singular == 'measure': existing_models = EfficiencyMeasure.objects.filter(Q(equipments__buildings__account=account) | Q(meters__account=account)).distinct().order_by('name')
            print 'ci12'
            if existing_models.count() == 1: #if only one, don't retrieve r.getValue() because we didn't ask for anything
                print 'ci13'
                t.ask(attempts = 2,
                      timeout = 30,
                      choices = "[1 DIGIT]",
                      say = "Do you want 1) performance data or 2) " + topic_capital_singular + " information? (select 1 or 2)")
                t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account_id) + '/' + topic_lower_plural + '/' + str(existing_models[0].id) + '/catch-request-type/')
                t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
            elif existing_models.count() < 4: #if more than one, we had to ask, so retrieve the answer
                                              #follow structure of tropo_catch_topic, i.e. re-ask those questions if failed
                print 'ci14'
                try:
                    print 'ci15'
                    model_id = r.getValue()
                    print 'ci16'
                    print model_id
                    print existing_models
                    print [str(i) for i in existing_models]
                    if model_id not in [str(i.id) for i in existing_models]: raise ValueError
                    print 'ci17'
                    t.ask(attempts = 2,
                          timeout = 30,
                          choices = "[1 DIGIT]",
                          say = "Do you want 1) performance data or 2) " + topic_capital_singular + " information? (select 1 or 2)")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account_id) + '/' + topic_lower_plural + '/' + model_id + '/catch-request-type/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
                except:
                    print 'ci18'
                    t.ask(attempts = 2,
                          timeout = 30,
                          choices = "[1-6 DIGITS]",
                          say = "I'm sorry.  That's not a valid selection for you. Please enter one of these " + topic_capital_singular + " ID numbers: " + "; ".join([str(i.id) + ') ' + str(i.name) for i in existing_models]) + ".")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account.id) + '/' + topic_lower_plural + '/catch-instance/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
            elif existing_models.count() >= 4: #if more than one, we had to ask, so retrieve the answer
                                              #follow structure of tropo_catch_topic, i.e. re-ask those questions if failed
                try:
                    print 'ci19'
                    model_id = r.getValue()
                    print 'ci20'
                    if model_id not in [str(i.id) for i in existing_models]: raise ValueError
                    print 'ci21'
                    t.ask(attempts = 2,
                          timeout = 30,
                          choices = "[1 DIGIT]",
                          say = "Do you want 1) performance data or 2) " + topic_capital_singular + " information? (select 1 or 2)")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account_id) + '/' + topic_lower_plural + '/' + model_id + '/catch-request-type/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
                except:
                    print 'ci22'
                    t.ask(attempts = 2,
                          timeout = 30,
                          choices = "[1-6 DIGITS]",
                          say = "I'm sorry.  That's not a valid selection for you. Please enter the " + topic_capital_singular + " ID (1-6 digits) you wish to discuss.")
                    t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account.id) + '/' + topic_lower_plural + '/catch-instance/')
                    t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                    t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
        print 'ci23'
    return HttpResponse(t.RenderJson())

@csrf_exempt
def tropo_catch_request_type(request, caller_id, account_id, topic, model_id):
    print request.body
    r = Result(request.body)
    t = Tropo()
    actions = r._actions
    print actions
    if type(actions) is list:
        r_dict = actions[0]
    else:
        r_dict = actions
    print r_dict
    print r_dict['disposition']
    if r_dict['disposition'] != 'SUCCESS': #only process if previous ask was successful
        t.hangup()
    else:
        print 'crt3'
        topic_lower_plural = topic
        print 'crt4'
        topic_lower_singular = topic[0:-1]
        print 'crt5'
        topic_capital_singular = topic[0:-1].capitalize()
        print 'crt6'
        topic_capital_plural = topic.capitalize()
        
        try:
            print 'crt7'
            request_type = r.getValue()
            print 'crt8'
            if model_id not in [1,2,'1','2']: raise ValueError
            print 'crt9'
            if model_id in [1,'1']:
                print 'crt10'
                t.ask(attempts = 2,
                      timeout = 30,
                      choices = "[ANY]",
                      say = "Tell me the date range in the following month and year format: MM*YYYY*MM*YYYY.")
                t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account_id) + '/' + topic_lower_plural + '/' + model_id + '/request-type/' + request_type + '/catch-request/')
                t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
            elif model_id in [2,'2']:
                print 'crt11'
                t.ask(attempts = 2,
                      timeout = 30,
                      choices = "[ANY]",
                      say = "Tell me the name of the field whose value you want, or tell me 'all' (quotes not required).")
                t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account_id) + '/' + topic_lower_plural + '/' + model_id + '/request-type/' + request_type + '/catch-request/')
                t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
                t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
        except:
            print 'crt12'
            t.ask(attempts = 2,
                  timeout = 30,
                  choices = "[1 DIGIT]",
                  say = "I'm sorry.  That's not a valid selection for you. Please pick 1) performance data or 2) " + topic_capital_singular + " information.")
            t.on(event = 'continue', next = '/tropo/user/' + str(caller_id) + '/account/' + str(account_id) + '/' + topic_lower_plural + '/' + model_id + '/catch-request-type/')
            t.on(event = 'incomplete', say = "I'm sorry we're having trouble communicating on this one. Please call support or try again later. Goodbye.")
            t.on(event = 'error', say = "Sorry, something's gone wrong. Please try again later. Goodbye.")
            
    print 'crt13'
    return HttpResponse(t.RenderJson())
    
@csrf_exempt
def tropo_catch_request(request, caller_id, account_id, topic, model_id, request_type):
    t = Tropo()
    t.say("Good job!  You reached the end of the line!")
    return HttpResponse(t.RenderJson())