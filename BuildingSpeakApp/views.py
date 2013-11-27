# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from BuildingSpeakApp.models import Account, Building, Meter, Equipment, WeatherStation, EfficiencyMeasure
from BuildingSpeakApp.models import Space, Monthling
from BuildingSpeakApp.models import UserSettingsForm, MeterDataUploadForm, WeatherDataUploadForm, Message
from BuildingSpeakApp.models import get_model_key_value_pairs_as_nested_list, convert_units_sum_meters
from BuildingSpeakApp.models import get_default_units, get_monthly_dataframe_as_table, nan2zero
from BuildingSpeakApp.models import get_df_as_table_with_formats, convert_units_single_value

import math
import json
import numpy as np
import pandas as pd
from django.utils import timezone
from decimal import Decimal
from django.forms.models import modelform_factory
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.core.mail import send_mail
#from rq import Queue
#from worker import conn

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
        return HttpResponseRedirect('/' + str(accounts[0].id))

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

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    
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
    this_month = pd.Period(timezone.now(),freq='M')
    month_first = this_month - 36   #link user selection here
    month_last = this_month         #link user selection here
    
    #if there are no meters, skip all meter data calcs
    if len(building.meters.all()) < 1:
        meter_data = None
        pie_data = None
    else:
        column_list_sum = ['Billing Demand (act)',
                        'Billing Demand (asave)',
                        'Billing Demand (base delta)',
                        'Billing Demand (base)',
                        'Billing Demand (esave delta)',
                        'Billing Demand (esave)',
                        'Billing Demand (exp delta)',
                        'Billing Demand (exp)',
                        'Consumption (act)',
                        'Consumption (asave)',
                        'Consumption (base delta)',
                        'Consumption (base)',
                        'Consumption (esave delta)',
                        'Consumption (esave)',
                        'Consumption (exp delta)',
                        'Consumption (exp)',
                        'Cost (act)',
                        'Cost (asave)',
                        'Cost (base delta)',
                        'Cost (base)',
                        'Cost (esave delta)',
                        'Cost (esave)',
                        'Cost (exp delta)',
                        'Cost (exp)',
                        'Peak Demand (act)',
                        'Peak Demand (asave)',
                        'Peak Demand (base delta)',
                        'Peak Demand (base)',
                        'Peak Demand (esave delta)',
                        'Peak Demand (esave)',
                        'Peak Demand (exp delta)',
                        'Peak Demand (exp)',
                        'kBtu Consumption (act)',
                        'kBtu Consumption (asave)',
                        'kBtu Consumption (base delta)',
                        'kBtu Consumption (base)',
                        'kBtu Consumption (esave delta)',
                        'kBtu Consumption (esave)',
                        'kBtu Consumption (exp delta)',
                        'kBtu Consumption (exp)',
                        'kBtuh Peak Demand (act)',
                        'kBtuh Peak Demand (asave)',
                        'kBtuh Peak Demand (base delta)',
                        'kBtuh Peak Demand (base)',
                        'kBtuh Peak Demand (esave delta)',
                        'kBtuh Peak Demand (esave)',
                        'kBtuh Peak Demand (exp delta)',
                        'kBtuh Peak Demand (exp)']
        #meter_data is what will be passed to the template
        meter_data = []
        utility_groups = ['Total Building Energy']
        utility_groups.extend(sorted(set([str(x.utility_type) for x in building.meters.all()])))
        
        #meter_dict holds all info and dataframes for each utility group, starting with Total non-water
        meter_dict = {'Total Building Energy': {'name': 'Total Building Energy',
                                                'costu': 'USD',
                                                'consu': 'kBtu',
                                                'pdu': 'kBtuh',
                                                'df': convert_units_sum_meters(
                                                        'other', 
                                                        'kBtuh,kBtu', 
                                                        building.meters.filter(~Q(utility_type = 'domestic water')), 
                                                        first_month=month_first.strftime('%m/%Y'), 
                                                        last_month=month_last.strftime('%m/%Y') )
                                                } }
        
        #cycle through all utility types present in this building, get info and dataframes
        for utype in sorted(set([str(x.utility_type) for x in building.meters.all()])):
            utype = str(utype)
            meter_dict[utype] = {}
            meter_dict[utype]['name'] = utype
            meter_dict[utype]['costu'] = 'USD'
            meter_dict[utype]['consu'] = get_default_units(utype).split(',')[1]
            meter_dict[utype]['pdu'] = get_default_units(utype).split(',')[0]
            meter_dict[utype]['df'] = convert_units_sum_meters(
                                        utype,
                                        get_default_units(utype),
                                        building.meters.filter(utility_type=utype),
                                        first_month=month_first.strftime('%m/%Y'), 
                                        last_month=month_last.strftime('%m/%Y'))
        
        #now that dataframes are available, create data tables for each utility type, inc. Total
        for utype in utility_groups:
            #additional column names to be created; these are manipulations of the stored data
            cost =              '$'
            cost_per_day =      '$/day'
            cost_per_sf =       '$/SF'
            consumption =                   meter_dict[utype]['consu']
            consumption_per_day =           meter_dict[utype]['consu'] + '/day'
            consumption_per_sf =            meter_dict[utype]['consu'] + '/SF'
            cost_per_consumption = '$/' +   meter_dict[utype]['consu']
            
            bill_data = meter_dict[utype]['df']
            bill_data['Days'] = [(bill_data['End Date'][i] - bill_data['Start Date'][i]).days+1 for i in range(0, len(bill_data))]
            
            #now we create the additional columns to manipulate the stored data for display to user
            bill_data[cost] = bill_data['Cost (act)']
            bill_data[cost_per_day] = bill_data['Cost (act)'] / bill_data['Days']
            bill_data[cost_per_sf] = bill_data['Cost (act)'] / building.square_footage
            bill_data[consumption] = bill_data['Consumption (act)']
            bill_data[consumption_per_day] = bill_data['Consumption (act)'] / bill_data['Days']
            bill_data[consumption_per_sf] = bill_data['Consumption (act)'] / building.square_footage
            bill_data[cost_per_consumption] = bill_data['Cost (act)'] / bill_data['Consumption (act)']
            
            #totals and useful ratios table calculations
            #first we construct a dataframe of the right length with only the columns we want
            bill_data_totals = bill_data[[cost,
                                       cost_per_day,
                                       cost_per_sf,
                                       consumption,
                                       consumption_per_day,
                                       consumption_per_sf,
                                       cost_per_consumption]][-1:-14:-1]
            #this column will get populated and then used to sort after we've jumped from Periods to Jan,Feb,etc.
            bill_data_totals['Month Integer'] = 99

            #now we loop through the 12 months and overwrite the old values with summations over all occurrences
            #    of a given month, and then we replace the index with text values Jan, Feb, etc.
            for i in range(0,12):
                bill_data_totals[cost][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
                bill_data_totals[cost_per_day][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / Decimal(0.0 + bill_data['Days'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum())
                bill_data_totals[cost_per_sf][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / building.square_footage
                bill_data_totals[consumption][i:i+1] = bill_data['Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
                bill_data_totals[consumption_per_day][i:i+1] = bill_data['Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / Decimal(0.0 + bill_data['Days'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum())
                bill_data_totals[consumption_per_sf][i:i+1] = bill_data['Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / building.square_footage
                bill_data_totals[cost_per_consumption][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum() / bill_data['Consumption (act)'][[x.month==bill_data_totals.index[i].month for x in bill_data.index]].sum()
                bill_data_totals['Month Integer'][i:i+1] = bill_data_totals.index[i].month
            bill_data_totals = bill_data_totals.sort(columns='Month Integer')
            bill_data_totals.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', 'Annual']

            #now we add the Annual row, which will be a column if and when we transpose
            bill_data_totals[cost]['Annual'] =                  bill_data['Cost (act)'].sum()
            bill_data_totals[cost_per_day]['Annual'] =          bill_data['Cost (act)'].sum() / Decimal(0.0 + bill_data['Days'].sum())
            bill_data_totals[cost_per_sf]['Annual'] =           bill_data['Cost (act)'].sum() / building.square_footage
            bill_data_totals[consumption]['Annual'] =           bill_data['Consumption (act)'].sum()
            bill_data_totals[consumption_per_day]['Annual'] =   bill_data['Consumption (act)'].sum() / Decimal(0.0 + bill_data['Days'].sum())
            bill_data_totals[consumption_per_sf]['Annual'] =    bill_data['Consumption (act)'].sum() / building.square_footage
            bill_data_totals[cost_per_consumption]['Annual'] =  bill_data['Cost (act)'].sum() / bill_data['Consumption (act)'].sum()
            
            #no longer needed once we've sorted
            bill_data_totals = bill_data_totals.drop(['Month Integer'],1)
        
            #totals table only has values as opposed to ratios, so we pull relevant columns and set format
            totals_table_df = bill_data_totals[[cost,consumption]]
            totals_column_dict = {cost: lambda x: '${:,.2f}'.format(x),
                                  consumption: lambda x: '{:,.0f}'.format(x)}
            totals_table = get_df_as_table_with_formats(df = totals_table_df,
                                                        columndict = totals_column_dict,
                                                        index_name = 'Metric',
                                                        transpose_bool = True)
        
            #ratios table only has ratios as opposed to totals, so we pull relevant columns and set format
            ratios_table_df = bill_data_totals[[cost_per_day,cost_per_sf,consumption_per_day,consumption_per_sf,cost_per_consumption]]
            ratios_column_dict = {cost_per_day: lambda x: '${:,.2f}'.format(x),
                                  cost_per_sf: lambda x: '${:,.2f}'.format(x),
                                  consumption_per_day: lambda x: '{:,.0f}'.format(x),
                                  consumption_per_sf: lambda x: '{:,.1f}'.format(x),
                                  cost_per_consumption: lambda x: '${:,.2f}'.format(x)}
            ratios_table = get_df_as_table_with_formats(df = ratios_table_df,
                                                        columndict = ratios_column_dict,
                                                        index_name = 'Metric',
                                                        transpose_bool = True)
            meter_dict[utype]['totals'] = totals_table
            meter_dict[utype]['ratios'] = ratios_table
            
        #cycle through the meter_dict and pass to list meter_data, converting dataframes to tables
        for utype in meter_dict:
            dfsum = meter_dict[utype]['df']
            dfsum[column_list_sum] = dfsum[column_list_sum].applymap(nan2zero)
            meter_data.append(
                         [meter_dict[utype]['name'],
                          meter_dict[utype]['costu'],
                          meter_dict[utype]['consu'],
                          meter_dict[utype]['pdu'],
                          get_monthly_dataframe_as_table(df=dfsum,
                                                         columnlist=['Month','Cost (base)','Cost (exp)','Cost (esave)','Cost (act)','Cost (asave)']),
                          get_monthly_dataframe_as_table(df=dfsum,
                                                         columnlist=['Month','Consumption (base)','Consumption (exp)','Consumption (esave)','Consumption (act)','Consumption (asave)']),
                          get_monthly_dataframe_as_table(df=dfsum,
                                                         columnlist=['Month','Peak Demand (base)','Peak Demand (exp)','Peak Demand (esave)','Peak Demand (act)','Peak Demand (asave)']),
                          meter_dict[utype]['totals'],
                          meter_dict[utype]['ratios']])
        
        
        if len(meter_data) < 1:
            meter_data = None
        else:
            pass #if necessary, weed out empty tables here
        
        #getting pie chart data; cost data includes all Meters; kBtu data excludes domestic water Meters
        pie_cost_by_meter =     [['Meter','Cost']]
        pie_cost_by_type =      [['Utility Type','Cost']]
        pie_kBtu_by_meter =     [['Meter','kBtu']]
        pie_kBtu_by_type =      [['Utility Type','kBtu']]
        
        #for breakdown by Meter, cycle through all Meters and exclude domestic water from kBtu calcs
        for meter in building.meters.all():
            cost_sum = Monthling.objects.filter(monther=meter.monther_set.get(name='BILLx')).filter(when__gte=month_first.to_timestamp(how='S')).filter(when__lte=month_last.to_timestamp(how='E')).aggregate(Sum('act_cost'))['act_cost__sum']
            if cost_sum is None or np.isnan(float(cost_sum)): cost_sum = Decimal('0.0') #pulling directly from db may return None, whereas df's return zeros
            pie_cost_by_meter.append([str(meter.name) + ' - ' + str(meter.utility_type), float(cost_sum)])
            if meter.utility_type != 'domestic water':
                kBtu_sum = Monthling.objects.filter(monther=meter.monther_set.get(name='BILLx')).filter(when__gte=month_first.to_timestamp(how='S')).filter(when__lte=month_last.to_timestamp(how='E')).aggregate(Sum('act_kBtu_consumption'))['act_kBtu_consumption__sum']
                if kBtu_sum is None or np.isnan(float(kBtu_sum)): kBtu_sum = Decimal('0.0') #pulling directly from db may return None, whereas df's return zeros
                pie_kBtu_by_meter.append([str(meter.name) + ' - ' + str(meter.utility_type), float(kBtu_sum)])
        
        #for breakdown by utility type, cycle through all utility groups and exclude domestic water from kBtu calcs
        for utype in utility_groups:
            if utype != 'Total Building Energy':
                pie_cost_by_type.append([utype, float(meter_dict[utype]['df']['Cost (act)'].sum())])
                if utype != 'domestic water':
                    pie_kBtu_by_type.append([utype, float(meter_dict[utype]['df']['kBtu Consumption (act)'].sum())])
        pie_data = [[pie_cost_by_meter, pie_cost_by_type, pie_kBtu_by_meter, pie_kBtu_by_type]]
            
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
        'building_attrs':       building_attrs,
        'meter_data':           meter_data,
        'pie_data':             pie_data,
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/building_detail.html'
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
    this_month = pd.Period(timezone.now(),freq='M')
    month_first = this_month - 36       #link user selection here
    month_last = this_month    #link user selection here

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
#                q = Queue(connection=conn)
#                result = q.enqueue(meter.upload_bill_data)
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
