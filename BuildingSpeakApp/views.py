# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from BuildingSpeakApp.models import Account, Building, Space, Meter, Equipment, WeatherStation, EfficiencyMeasure
from BuildingSpeakApp.models import UserSettingsForm, MeterDataUploadForm, WeatherDataUploadForm
from BuildingSpeakApp.models import get_model_key_value_pairs_as_nested_list, decimal_isnan, nan2zero
from BuildingSpeakApp.models import get_monthly_dataframe_as_table, get_df_as_table_with_formats

import json, jsonpickle
import numpy as np
import pandas as pd
from pytz import UTC
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.core.mail import send_mail
from tropo import Tropo, Session
from django.views.decorators.csrf import csrf_exempt
from rq import Queue
from worker import conn

class ResultsMessage(object):
    """Used for generating user
    feedback messages that do
    not need to be stored as
    messages in the database."""
    id = 0
    subject = 'Success!'
    comment = ''
    
@login_required
def index(request):
    accounts = request.user.account_set.order_by('id')
    if len(accounts)==0:
        return HttpResponseRedirect('/user-account')
    else:
        #return HttpResponseRedirect('/' + str(accounts[0].id))
        return HttpResponseRedirect('/tropo_test')

@login_required
def user_account(request):
#    try:
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
#    except:
#        return HttpResponseRedirect('/application-error')
        
@login_required
def update_successful(request):
    context  = {'user': request.user}
    return render(request, 'buildingspeakapp/update_successful.html', context)

def application_error(request):
    context  = {'user': request.user}
    return render(request, 'buildingspeakapp/application_error.html', context)

@csrf_exempt
def tropo_test_index(request):
    print 'index1'
    t = Tropo()
    print 'index2'
    t.call(to="+16782815256", network = "SMS")
    print 'index3'
    t.say(["Made it to index."])
    print 'index4'
    return HttpResponse(t.RenderJson())
    
@csrf_exempt
def tropo_test_result(request):
    print 'result1'
    t = Tropo()
    print 'result2'
    t.call(to="+16782815256", network = "SMS")
    print 'result3'
    t.say(["Made it to response."])
    print 'result4'
    return HttpResponse(t.RenderJson())
    
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

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    total_SF = account.building_set.all().aggregate(Sum('square_footage'))['square_footage__sum']
    
    account_attrs = get_model_key_value_pairs_as_nested_list(account)
    month_curr = pd.Period(timezone.now(),freq='M')-39 #current month, final month in sequence
    month_prev = month_curr - 1                     #previous month, first in sequence
    
    bldg_data = []
    for bldg in account.building_set.order_by('name'):
        bldg_view_data_curr = bldg.get_building_view_meter_data(month_first = month_curr,
                                                                month_last = month_curr)
        if bldg_view_data_curr is None: bldg_view_data_curr = [False, False]
        bldg_view_data_prev = bldg.get_building_view_meter_data(month_first = month_prev,
                                                                month_last = month_prev)
        if bldg_view_data_prev is None: bldg_view_data_prev = [False, False]
        bldg_data.append([bldg,
                          bldg_view_data_curr[0],
                          bldg_view_data_curr[1],
                          bldg_view_data_prev[0],
                          bldg_view_data_prev[1],
                          ])

    month_first = pd.Period(timezone.now(),freq='M')-40     #first month in sequence
    month_last = month_first + 40                            #final month in sequence
    acct_view_data = account.get_account_view_meter_data(month_first=month_first,
                                                         month_last=month_last)
    five_year_data = account.get_account_view_five_year_data()

    if acct_view_data is None:
        meter_data = None
        pie_data = None
    else:
        meter_data = acct_view_data[0]
        pie_data = acct_view_data[1]
    
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
    month_last = month_first + 40                            #final month in sequence
    
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
    month_last = month_first + 40                            #final month in sequence
    
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
                q = Queue(connection=conn)
                result = q.enqueue(meter.upload_bill_data)
#                meter.upload_bill_data()
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
    this_month = pd.Period(timezone.now(),freq='M')
    month_first = this_month - 36       #link user selection here
    month_last = this_month    #link user selection here
    
    #this dataframe provides the foundational meter dataset; if no data, skip everything
    bill_data = meter.get_bill_data_period_dataframe(first_month=month_first.strftime('%m/%Y'), last_month=month_last.strftime('%m/%Y')) ######use # of months here!!!!!!!!!!!!!!!!!!!
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
    else:
        bill_data = bill_data.sort_index()
        #additional column names to be created; these are manipulations of the stored data
        cost_per_consumption = '$/' + meter.units.split(',')[1]
        consumption_per_day = meter.units.split(',')[1] + '/day'
        consumption = meter.units.split(',')[1]
        consumption_kBtu = 'kBtu'
        cost = '$'
        cost_per_day = '$/day'
        cost_per_kBtu = '$/kBtu'
        kBtu_per_day = 'kBtu/day'
        bill_data['Days'] = [(bill_data['End Date'][i] - bill_data['Start Date'][i]).days+1 for i in range(0, len(bill_data))]
        
        #now we create the additional columns to manipulate the stored data for display to user
        bill_data[cost_per_consumption] = bill_data['Cost (act)'] / bill_data['Consumption (act)']
        bill_data[cost_per_day] = bill_data['Cost (act)'] / bill_data['Days']
        bill_data[cost] = bill_data['Cost (act)']
        bill_data[consumption_per_day] = bill_data['Consumption (act)'] / bill_data['Days']
        bill_data[consumption] = bill_data['Consumption (act)']
        bill_data[consumption_kBtu] = bill_data['kBtu Consumption (act)']
        bill_data[cost_per_kBtu] = bill_data['Cost (act)'] / bill_data['kBtu Consumption (act)']
        bill_data[kBtu_per_day] = bill_data['kBtu Consumption (act)'] / bill_data['Days']
        
        #totals and useful ratios table calculations
        #first we construct a dataframe of the right length with only the columns we want
        bill_data_totals = bill_data[[consumption_per_day,
                                   cost_per_day,
                                   cost_per_consumption,
                                   consumption_kBtu,
                                   consumption,
                                   cost,
                                   cost_per_kBtu,
                                   kBtu_per_day]][-1:-14:-1]
        #this column will get populated and then used to sort after we've jumped from Periods to Jan,Feb,etc.
        bill_data_totals['Month Integer'] = 99
        
        #now we loop through the 12 months and overwrite the old values with summations over all occurrences
        #    of a given month, and then we replace the index with text values Jan, Feb, etc.
        for i in range(0,12):
            bill_data_totals[cost_per_consumption][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / bill_data['Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
            bill_data_totals[cost_per_day][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / Decimal(0.0 + bill_data['Days'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum())
            bill_data_totals[cost][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
            bill_data_totals[consumption_per_day][i:i+1] = bill_data['Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / Decimal(0.0 + bill_data['Days'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum())
            bill_data_totals[consumption][i:i+1] = bill_data['Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
            bill_data_totals[consumption_kBtu][i:i+1] = bill_data['kBtu Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
            bill_data_totals[cost_per_kBtu][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / bill_data['kBtu Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
            bill_data_totals[kBtu_per_day][i:i+1] = bill_data['kBtu Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / Decimal(0.0 + bill_data['Days'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum())
            bill_data_totals['Month Integer'][i:i+1] = bill_data_totals.index[i].month
        bill_data_totals = bill_data_totals.sort(columns='Month Integer')
        bill_data_totals.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', 'Annual']
        
        #now we add the Annual row, which will be a column if and when we transpose
        bill_data_totals[cost_per_consumption]['Annual'] = bill_data['Cost (act)'].sum() / bill_data['Consumption (act)'].sum()
        bill_data_totals[cost_per_day]['Annual'] =         bill_data['Cost (act)'].sum() / Decimal(0.0 + bill_data['Days'].sum())
        bill_data_totals[cost]['Annual'] =                  bill_data['Cost (act)'].sum()
        bill_data_totals[consumption_per_day]['Annual'] =  bill_data['Consumption (act)'].sum() / Decimal(0.0 + bill_data['Days'].sum())
        bill_data_totals[consumption]['Annual'] =          bill_data['Consumption (act)'].sum()
        bill_data_totals[consumption_kBtu]['Annual'] =     bill_data['kBtu Consumption (act)'].sum()
        bill_data_totals[cost_per_kBtu]['Annual'] = bill_data['Cost (act)'].sum() / bill_data['kBtu Consumption (act)'].sum()
        bill_data_totals[kBtu_per_day]['Annual'] =  bill_data['kBtu Consumption (act)'].sum() / Decimal(0.0 + bill_data['Days'].sum())
        
        #no longer needed once we've sorted
        bill_data_totals = bill_data_totals.drop(['Month Integer'],1)
        
        #totals table only has values as opposed to ratios, so we pull relevant columns and set format
        totals_table_df = bill_data_totals[[cost,consumption,consumption_kBtu]]
        totals_column_dict = {cost: lambda x: '${:,.2f}'.format(x),
                              consumption: lambda x: '{:,.0f}'.format(x),
                              consumption_kBtu: lambda x: '{:,.0f}'.format(x)}
        totals_table = get_df_as_table_with_formats(df = totals_table_df,
                                                    columndict = totals_column_dict,
                                                    index_name = 'Metric',
                                                    transpose_bool = True)
    
        #ratios table only has ratios as opposed to totals, so we pull relevant columns and set format
        ratios_table_df = bill_data_totals[[cost_per_consumption,consumption_per_day,cost_per_day,cost_per_kBtu,kBtu_per_day]]
        ratios_column_dict = {cost_per_consumption: lambda x: '${:,.2f}'.format(x),
                              consumption_per_day: lambda x: '{:,.0f}'.format(x),
                              cost_per_day: lambda x: '${:,.2f}'.format(x),
                              cost_per_kBtu: lambda x: '${:,.2f}'.format(x),
                              kBtu_per_day: lambda x: '{:,.0f}'.format(x)}
        ratios_table = get_df_as_table_with_formats(df = ratios_table_df,
                                                    columndict = ratios_column_dict,
                                                    index_name = 'Metric',
                                                    transpose_bool = True)
        
        #now create monthly charts if data exists; set to False for template if no data
        cost_by_month = get_monthly_dataframe_as_table(df=bill_data, columnlist=['Month','Cost (base)','Cost (exp)','Cost (esave)','Cost (act)','Cost (asave)'])
        if len(cost_by_month) == 1: cost_by_month = False
        consumption_by_month = get_monthly_dataframe_as_table(df=bill_data, columnlist=['Month','Consumption (base)','Consumption (exp)','Consumption (esave)','Consumption (act)','Consumption (asave)'])
        if len(consumption_by_month) == 1: consumption_by_month = False
        demand_by_month = get_monthly_dataframe_as_table(df=bill_data, columnlist=['Month','Peak Demand (base)','Peak Demand (exp)','Peak Demand (esave)','Peak Demand (act)','Peak Demand (asave)'])
        if len(demand_by_month) == 1: demand_by_month = False
        kbtu_by_month = get_monthly_dataframe_as_table(df=bill_data, columnlist=['Month','kBtu Consumption (base)','kBtu Consumption (exp)','kBtu Consumption (esave)','kBtu Consumption (act)','kBtu Consumption (asave)'])
        if len(kbtu_by_month) == 1: kbtu_by_month = False
        kbtuh_by_month = get_monthly_dataframe_as_table(df=bill_data, columnlist=['Month','kBtuh Peak Demand (base)','kBtuh Peak Demand (exp)','kBtuh Peak Demand (esave)','kBtuh Peak Demand (act)','kBtuh Peak Demand (asave)'])
        if len(kbtuh_by_month) == 1: kbtuh_by_month = False
        
        #pull model stats and residuals if model exists; set False if no model but None for vars iterated over in template
        if meter.monther_set.get(name='BILLx').consumption_model is None:
            consumption_model_stats_table = False
            consumption_model_residuals_table = False
            consumption_model_residuals_histogram = False
            consumption_residual_plots = None
        else:
            consumption_model_stats_table = meter.monther_set.get(name='BILLx').consumption_model.get_model_stats_as_table()
            consumption_model_residuals_table = meter.monther_set.get(name='BILLx').consumption_model.get_residuals_and_indvars_as_table()
            consumption_model_residuals = [x[0] for x in consumption_model_residuals_table[1:]]
            ccount,cdiv = np.histogram(consumption_model_residuals)
            consumption_model_residuals_histogram = [['Bins', 'Frequency']]
            consumption_model_residuals_histogram.extend([[cdiv[i],float(ccount[i])] for i in range(0,len(ccount))])
            if len(consumption_model_residuals_table[0]) > 1: #if there are any independent variables, need to construct column pairs
                consumption_residual_plots = []
                for i in range(1,len(consumption_model_residuals_table[0])):
                    consumption_residual_plots.append([consumption_model_residuals_table[0][i],[[x[i],x[0]] for x in consumption_model_residuals_table]])
            else:
                consumption_residual_plots = None
            
        #pull model stats and residuals if model exists; set False if no model but None for vars iterated over in template
        if meter.monther_set.get(name='BILLx').peak_demand_model is None:
            peak_demand_model_stats_table = False
            peak_demand_model_residuals_table = False
            peak_demand_model_residuals_histogram = False
            peak_demand_residual_plots = None
        else:
            peak_demand_model_stats_table = meter.monther_set.get(name='BILLx').peak_demand_model.get_model_stats_as_table()    
            peak_demand_model_residuals_table = meter.monther_set.get(name='BILLx').peak_demand_model.get_residuals_and_indvars_as_table()
            peak_demand_model_residuals = [x[0] for x in peak_demand_model_residuals_table[1:]]
            pcount,pdiv = np.histogram(peak_demand_model_residuals)
            peak_demand_model_residuals_histogram = [['Bins', 'Frequency']]
            peak_demand_model_residuals_histogram.extend([[pdiv[i],float(pcount[i])] for i in range(0,len(pcount))])
            if len(peak_demand_model_residuals_table[0]) > 1: #if there are any independent variables, need to construct column pairs
                peak_demand_residual_plots = []
                for i in range(1,len(peak_demand_model_residuals_table[0])):
                    peak_demand_residual_plots.append([peak_demand_model_residuals_table[0][i],[[x[i],x[0]] for x in peak_demand_model_residuals_table]])
            else:
                peak_demand_residual_plots = None

    #-----------------------------------5yr graph calculations
    month_curr = pd.Period(timezone.now(), freq='M')
    year_curr = month_curr.year
    mi = pd.Period(year = year_curr-3, month = 1, freq = 'M')
    mf = pd.Period(year = year_curr+1, month = 12, freq = 'M')
    df = meter.get_bill_data_period_dataframe(first_month = mi.strftime('%m/%Y'),
                                              last_month = mf.strftime('%m/%Y'))
    five_years = pd.DataFrame(df, index = pd.period_range(start = mi, end = mf, freq = 'M'))
    five_years = five_years.sort_index()
    first_calc_month = five_years.index[five_years['Cost (act)'].apply(decimal_isnan)][0]
    last_act_month = first_calc_month - 1
    
    five_years = five_years[['Cost (act)','Cost (exp)','Consumption (act)','Consumption (exp)',
                             'kBtu Consumption (act)','kBtu Consumption (exp)','CDD (consumption)',
                             'HDD (consumption)']].applymap(nan2zero)
    five_years = five_years[['Cost (act)','Cost (exp)','Consumption (act)','Consumption (exp)',
                             'kBtu Consumption (act)','kBtu Consumption (exp)','CDD (consumption)',
                             'HDD (consumption)']].applymap(float)
    
    five_year_table_cost = [['Year','Cost (act)','Cost (exp)','CDD (consumption)','HDD (consumption)']]
    five_year_table_cost.append([str(five_years.index[0].year),
                            five_years['Cost (act)'][0:12].sum(),
                            0,
                            five_years['CDD (consumption)'][0:12].sum(),
                            five_years['HDD (consumption)'][0:12].sum()
                            ])
    five_year_table_cost.append([str(five_years.index[12].year),
                            five_years['Cost (act)'][12:24].sum(),
                            0,
                            five_years['CDD (consumption)'][12:24].sum(),
                            five_years['HDD (consumption)'][12:24].sum()
                            ])
    five_year_table_cost.append([str(five_years.index[24].year),
                            five_years['Cost (act)'][24:36].sum(),
                            0,
                            five_years['CDD (consumption)'][24:36].sum(),
                            five_years['HDD (consumption)'][24:36].sum()
                            ])
    five_year_table_cost.append([str(five_years.index[36].year),
                            five_years['Cost (act)'][36:last_act_month].sum(),
                            five_years['Cost (exp)'][first_calc_month:48].sum(),
                            five_years['CDD (consumption)'][36:48].sum(),
                            five_years['HDD (consumption)'][36:48].sum()
                            ])
    five_year_table_cost.append([str(five_years.index[48].year),
                            0,
                            five_years['Cost (exp)'][48:60].sum(),
                            five_years['CDD (consumption)'][48:60].sum(),
                            five_years['HDD (consumption)'][48:60].sum()
                            ])
    
    five_year_table_cons = [['Year','Consumption (act)','Consumption (exp)','CDD (consumption)','HDD (consumption)']]
    five_year_table_cons.append([str(five_years.index[0].year),
                            five_years['Consumption (act)'][0:12].sum(),
                            0,
                            five_years['CDD (consumption)'][0:12].sum(),
                            five_years['HDD (consumption)'][0:12].sum()
                            ])
    five_year_table_cons.append([str(five_years.index[12].year),
                            five_years['Consumption (act)'][12:24].sum(),
                            0,
                            five_years['CDD (consumption)'][12:24].sum(),
                            five_years['HDD (consumption)'][12:24].sum()
                            ])
    five_year_table_cons.append([str(five_years.index[24].year),
                            five_years['Consumption (act)'][24:36].sum(),
                            0,
                            five_years['CDD (consumption)'][24:36].sum(),
                            five_years['HDD (consumption)'][24:36].sum()
                            ])
    five_year_table_cons.append([str(five_years.index[36].year),
                            five_years['Consumption (act)'][36:last_act_month].sum(),
                            five_years['Consumption (exp)'][first_calc_month:48].sum(),
                            five_years['CDD (consumption)'][36:48].sum(),
                            five_years['HDD (consumption)'][36:48].sum()
                            ])
    five_year_table_cons.append([str(five_years.index[48].year),
                            0,
                            five_years['Consumption (exp)'][48:60].sum(),
                            five_years['CDD (consumption)'][48:60].sum(),
                            five_years['HDD (consumption)'][48:60].sum()
                            ])

    five_year_table_kBtu = [['Year','kBtu Consumption (act)','kBtu Consumption (exp)','CDD (consumption)','HDD (consumption)']]
    five_year_table_kBtu.append([str(five_years.index[0].year),
                            five_years['kBtu Consumption (act)'][0:12].sum(),
                            0,
                            five_years['CDD (consumption)'][0:12].sum(),
                            five_years['HDD (consumption)'][0:12].sum()
                            ])
    five_year_table_kBtu.append([str(five_years.index[12].year),
                            five_years['kBtu Consumption (act)'][12:24].sum(),
                            0,
                            five_years['CDD (consumption)'][12:24].sum(),
                            five_years['HDD (consumption)'][12:24].sum()
                            ])
    five_year_table_kBtu.append([str(five_years.index[24].year),
                            five_years['kBtu Consumption (act)'][24:36].sum(),
                            0,
                            five_years['CDD (consumption)'][24:36].sum(),
                            five_years['HDD (consumption)'][24:36].sum()
                            ])
    five_year_table_kBtu.append([str(five_years.index[36].year),
                            five_years['kBtu Consumption (act)'][36:last_act_month].sum(),
                            five_years['kBtu Consumption (exp)'][first_calc_month:48].sum(),
                            five_years['CDD (consumption)'][36:48].sum(),
                            five_years['HDD (consumption)'][36:48].sum()
                            ])
    five_year_table_kBtu.append([str(five_years.index[48].year),
                            0,
                            five_years['kBtu Consumption (exp)'][48:60].sum(),
                            five_years['CDD (consumption)'][48:60].sum(),
                            five_years['HDD (consumption)'][48:60].sum()
                            ])
    
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
        'motion_data':                              meter.get_meter_view_motion_table(),
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
