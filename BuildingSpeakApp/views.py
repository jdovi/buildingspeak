# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from BuildingSpeakApp.models import Account, Building, Meter, Equipment, WeatherStation, EfficiencyMeasure
from BuildingSpeakApp.models import Space
from BuildingSpeakApp.models import UserSettingsForm, MeterDataUploadForm, WeatherDataUploadForm, Message
from BuildingSpeakApp.models import get_model_key_value_pairs_as_nested_list, convert_units_sum_meters
import json
import numpy as np
import pandas as pd
from django.utils import timezone
from decimal import Decimal
from django.forms.models import modelform_factory
from django.contrib.auth.models import User
from django.db.models import Q
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
    
    meter_data = [[str(x.utility_type),str(x.units),x.get_dataframe_as_table(df=x.get_bill_data_period_dataframe(),
                                                                       columnlist=['Month',
                                                                           'Cost (base)',
                                                                           'Cost (exp)',
                                                                           'Cost (esave)',
                                                                           'Cost (act)',
                                                                           'Cost (asave)'])] for x in building.meters.filter(utility_type='electricity')]
    if len(meter_data) == 1:
        meter_data = False
    else:
        meter_data = [x for x in meter_data if len(x[2])>1]
    
#    tt = [['Month','Cost (base)','Cost (exp)'],['2008-09',5,15],['2008-10',6,16]]
#    meter_data = [['electricity','kW,kWh',tt],['electricity','kW,kWh',tt],['electricity','kW,kWh',tt]]
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
    
    bill_data = meter.get_bill_data_period_dataframe(first_month=(this_month-12).strftime('%m/%Y'), last_month=this_month.strftime('%m/%Y')).sort_index() ######use # of months here!!!!!!!!!!!!!!!!!!!
    cost_per_consumption = '$/' + meter.units.split(',')[1]
    cost_per_peak_demand = '$/' + meter.units.split(',')[0]
    consumption_per_day = meter.units.split(',')[1] + '/day'
    bill_data['Days'] = [(bill_data['End Date'][i] - bill_data['Start Date'][i]).days for i in range(0, len(bill_data))]
    
    bill_data[cost_per_consumption] = bill_data['Cost (act)'] / bill_data['Consumption (act)']
    bill_data[cost_per_peak_demand] = bill_data['Cost (act)'] / bill_data['Peak Demand (act)']
    bill_data['$/day'] = bill_data['Cost (act)'] / bill_data['Days']
    bill_data[consumption_per_day] = bill_data['Consumption (act)'] / bill_data['Days']
    
    bill_data_avg = bill_data[[cost_per_consumption,cost_per_peak_demand,'$/day',consumption_per_day]][-1:-13:-1]
    bill_data_avg['Month Integer'] = 99
    for i in range(0,12):
        bill_data_avg[cost_per_consumption][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum() / bill_data['Consumption (act)'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum()
        bill_data_avg[cost_per_peak_demand][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum() / bill_data['Peak Demand (act)'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum()
        bill_data_avg['$/day'][i:i+1] = bill_data['Cost (act)'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum() / Decimal(1.0 + bill_data['Days'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum())
        bill_data_avg[consumption_per_day][i:i+1] = bill_data['Consumption (act)'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum() / Decimal(1.0 + bill_data['Days'][[x.month==bill_data_avg.index[i].month for x in bill_data.index]].sum())
        bill_data_avg['Month Integer'][i:i+1] = bill_data_avg.index[i].month
    bill_data_avg = bill_data_avg.sort(columns='Month Integer')
    bill_data_avg.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    bill_data_avg = bill_data_avg.drop(['Month Integer'],1)
    bill_data_avg = bill_data_avg.transpose()
    bill_data_avg['Annual'] = [bill_data['Cost (act)'].sum() / bill_data['Consumption (act)'].sum(),
                                     bill_data['Cost (act)'].sum() / bill_data['Peak Demand (act)'].sum(),
                                     bill_data['Cost (act)'].sum() / Decimal(1.0 + bill_data['Days'].sum()),
                                     bill_data['Consumption (act)'].sum() / Decimal(1.0 + bill_data['Days'].sum())]
    useful_metrics_by_month = meter.get_dataframe_as_table(df=bill_data_avg, columnlist=['Metric','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', 'Annual'])
    if len(useful_metrics_by_month) == 1: useful_metrics_by_month = False
    
    cost_by_month = meter.get_dataframe_as_table(df=bill_data, columnlist=['Month',
                                                                           'Cost (base)',
                                                                           'Cost (exp)',
                                                                           'Cost (esave)',
                                                                           'Cost (act)',
                                                                           'Cost (asave)'])
    if len(cost_by_month) == 1: cost_by_month = False
    consumption_by_month = meter.get_dataframe_as_table(df=bill_data, columnlist=['Month',
                                                                                  'Consumption (base)',
                                                                                  'Consumption (exp)',
                                                                                  'Consumption (esave)',
                                                                                  'Consumption (act)',
                                                                                  'Consumption (asave)'])
    if len(consumption_by_month) == 1: consumption_by_month = False
    demand_by_month = meter.get_dataframe_as_table(df=bill_data, columnlist=['Month',
                                                                             'Peak Demand (base)',
                                                                             'Peak Demand (exp)',
                                                                             'Peak Demand (esave)',
                                                                             'Peak Demand (act)',
                                                                             'Peak Demand (asave)'])
    if len(demand_by_month) == 1: demand_by_month = False
    kbtu_by_month = meter.get_dataframe_as_table(df=bill_data, columnlist=['Month',
                                                                                  'kBtu Consumption (base)',
                                                                                  'kBtu Consumption (exp)',
                                                                                  'kBtu Consumption (esave)',
                                                                                  'kBtu Consumption (act)',
                                                                                  'kBtu Consumption (asave)'])
    if len(kbtu_by_month) == 1: kbtu_by_month = False
    kbtuh_by_month = meter.get_dataframe_as_table(df=bill_data, columnlist=['Month',
                                                                             'kBtuh Peak Demand (base)',
                                                                             'kBtuh Peak Demand (exp)',
                                                                             'kBtuh Peak Demand (esave)',
                                                                             'kBtuh Peak Demand (act)',
                                                                             'kBtuh Peak Demand (asave)'])
    if len(kbtuh_by_month) == 1: kbtuh_by_month = False
    
    consumption_model_stats_table = meter.monther_set.get(name='BILLx').consumption_model.get_model_stats_as_table()
    peak_demand_model_stats_table = meter.monther_set.get(name='BILLx').peak_demand_model.get_model_stats_as_table()
    
    consumption_model_residuals_table = meter.monther_set.get(name='BILLx').consumption_model.get_residuals_and_indvars_as_table()
    peak_demand_model_residuals_table = meter.monther_set.get(name='BILLx').peak_demand_model.get_residuals_and_indvars_as_table()
    
    consumption_model_residuals = [x[0] for x in consumption_model_residuals_table[1:]]
    peak_demand_model_residuals = [x[0] for x in peak_demand_model_residuals_table[1:]]
    ccount,cdiv = np.histogram(consumption_model_residuals)
    pcount,pdiv = np.histogram(peak_demand_model_residuals)
    consumption_model_residuals_histogram = [['Bins', 'Frequency']]
    peak_demand_model_residuals_histogram = [['Bins', 'Frequency']]
    consumption_model_residuals_histogram.extend([[cdiv[i],float(ccount[i])] for i in range(0,len(ccount))])
    peak_demand_model_residuals_histogram.extend([[pdiv[i],float(pcount[i])] for i in range(0,len(pcount))])

    consumption_residual_plot_pairs = [[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    if len(consumption_model_residuals_table[0]) > 1: #if there are any independent variables, need to construct column pairs
        for i in range(1,len(consumption_model_residuals_table[0])):
            consumption_residual_plot_pairs[i-1] = [[x[i],x[0]] for x in consumption_model_residuals_table]
    peak_demand_residual_plot_pairs = [[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]],[[0]]]
    if len(peak_demand_model_residuals_table[0]) > 1: #if there are any independent variables, need to construct column pairs
        for i in range(1,len(peak_demand_model_residuals_table[0])):
            peak_demand_residual_plot_pairs[i-1] = [[x[i],x[0]] for x in peak_demand_model_residuals_table]
    
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
        'form':                    form,
        'meter':                   meter,
        'meter_attrs':              meter_attrs,
        'useful_metrics_by_month': json.dumps(useful_metrics_by_month),
        'cost_by_month':           json.dumps(cost_by_month),
        'consumption_by_month':    json.dumps(consumption_by_month),
        'demand_by_month':         json.dumps(demand_by_month),
        'kbtu_by_month':           json.dumps(kbtu_by_month),
        'kbtuh_by_month':          json.dumps(kbtuh_by_month),
        'consumption_units':       json.dumps(meter.units.split(',')[1]),
        'demand_units':            json.dumps(meter.units.split(',')[0]),
        'consumption_model_stats_table':    json.dumps(consumption_model_stats_table),
        'peak_demand_model_stats_table':    json.dumps(peak_demand_model_stats_table),
        'consumption_model_residuals_table0':    json.dumps(consumption_residual_plot_pairs[0]),
        'peak_demand_model_residuals_table0':    json.dumps(peak_demand_residual_plot_pairs[0]),
        'consumption_model_residuals_table1':    json.dumps(consumption_residual_plot_pairs[1]),
        'peak_demand_model_residuals_table1':    json.dumps(peak_demand_residual_plot_pairs[1]),
        'consumption_model_residuals_table2':    json.dumps(consumption_residual_plot_pairs[2]),
        'peak_demand_model_residuals_table2':    json.dumps(peak_demand_residual_plot_pairs[2]),
        'consumption_model_residuals_table3':    json.dumps(consumption_residual_plot_pairs[3]),
        'peak_demand_model_residuals_table3':    json.dumps(peak_demand_residual_plot_pairs[3]),
        'consumption_model_residuals_table4':    json.dumps(consumption_residual_plot_pairs[4]),
        'peak_demand_model_residuals_table4':    json.dumps(peak_demand_residual_plot_pairs[4]),
        'consumption_model_residuals_table5':    json.dumps(consumption_residual_plot_pairs[5]),
        'peak_demand_model_residuals_table5':    json.dumps(peak_demand_residual_plot_pairs[5]),
        'consumption_model_residuals_table6':    json.dumps(consumption_residual_plot_pairs[6]),
        'peak_demand_model_residuals_table6':    json.dumps(peak_demand_residual_plot_pairs[6]),
        'consumption_model_residuals_table7':    json.dumps(consumption_residual_plot_pairs[7]),
        'peak_demand_model_residuals_table7':    json.dumps(peak_demand_residual_plot_pairs[7]),
        'consumption_model_residuals_table8':    json.dumps(consumption_residual_plot_pairs[8]),
        'peak_demand_model_residuals_table8':    json.dumps(peak_demand_residual_plot_pairs[8]),
        'consumption_model_residuals_table9':    json.dumps(consumption_residual_plot_pairs[9]),
        'peak_demand_model_residuals_table9':    json.dumps(peak_demand_residual_plot_pairs[9]),
        'consumption_model_indvar0':             json.dumps(consumption_residual_plot_pairs[0][0][0]),
        'peak_demand_model_indvar0':             json.dumps(peak_demand_residual_plot_pairs[0][0][0]),
        'consumption_model_indvar1':    json.dumps(consumption_residual_plot_pairs[1][0][0]),
        'peak_demand_model_indvar1':    json.dumps(peak_demand_residual_plot_pairs[1][0][0]),
        'consumption_model_indvar2':    json.dumps(consumption_residual_plot_pairs[2][0][0]),
        'peak_demand_model_indvar2':    json.dumps(peak_demand_residual_plot_pairs[2][0][0]),
        'consumption_model_indvar3':    json.dumps(consumption_residual_plot_pairs[3][0][0]),
        'peak_demand_model_indvar3':    json.dumps(peak_demand_residual_plot_pairs[3][0][0]),
        'consumption_model_indvar4':    json.dumps(consumption_residual_plot_pairs[4][0][0]),
        'peak_demand_model_indvar4':    json.dumps(peak_demand_residual_plot_pairs[4][0][0]),
        'consumption_model_indvar5':    json.dumps(consumption_residual_plot_pairs[5][0][0]),
        'peak_demand_model_indvar5':    json.dumps(peak_demand_residual_plot_pairs[5][0][0]),
        'consumption_model_indvar6':    json.dumps(consumption_residual_plot_pairs[6][0][0]),
        'peak_demand_model_indvar6':    json.dumps(peak_demand_residual_plot_pairs[6][0][0]),
        'consumption_model_indvar7':    json.dumps(consumption_residual_plot_pairs[7][0][0]),
        'peak_demand_model_indvar7':    json.dumps(peak_demand_residual_plot_pairs[7][0][0]),
        'consumption_model_indvar8':    json.dumps(consumption_residual_plot_pairs[8][0][0]),
        'peak_demand_model_indvar8':    json.dumps(peak_demand_residual_plot_pairs[8][0][0]),
        'consumption_model_indvar9':    json.dumps(consumption_residual_plot_pairs[9][0][0]),
        'peak_demand_model_indvar9':    json.dumps(peak_demand_residual_plot_pairs[9][0][0]),
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
