# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from BuildingSpeakApp.models import Account, Building, Meter, Equipment
import json
from decimal import Decimal
from django.forms.models import modelform_factory
from django.contrib.auth.models import User


@login_required
def index(request):
#    accounts = request.user.account_set.order_by('id')
#    return redirect('/' + str(accounts[0].id))
    context = {}
    accounts = request.user.account_set.order_by('id')
    if len(accounts)==0:
        template_name = 'buildingspeakapp/my_account.html'
    else:
        template_name = request.user.account_set.order_by('id')
    return render(request, template_name, context)

@login_required
def user_account(request):
    UserAccountForm = modelform_factory(User)
    if request.method == 'POST': # If the form has been submitted...
        form = UserAccountForm(request.POST, instance=request.user) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            calling_user = form.save()
            calling_user.save()
            return HttpResponseRedirect('/update-successful.html') # Redirect after POST
    else:
        form = UserAccountForm(instance=request.user) # An unbound form
    context = {
        'user':     request.user,
        'accounts': request.user.account_set.order_by('id'),
        'form':     form, }
    return render(request, 'buildingspeakapp/user_account.html', context)

def update_successful(request):
    context  = {'user': request.user}
    return render(request, 'buildingspeakapp/update_successful.html', context)

@login_required
def my_account(request):
    context  = {'user': request.user}
    return render(request, 'buildingspeakapp/my_account.html', context)

def account_detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    x = []
    x.extend(account.account_equipments())
    equipcount = len(x)
    account_dict = {}    
    for z in account._meta.get_all_field_names():
        try:
            account_dict[z.replace('_',' ')] = account.__getattribute__(z)
        except AttributeError:
            pass
    
    context = {
        'account':      account,
        'accounts':     request.user.account_set.order_by('id'),
        'equipcount':   equipcount,
        'account_dict': account_dict,
        'alerts':       account.get_all_alerts(reverse_boolean=True)
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/account_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

def building_detail(request, account_id, building_id):
    account = get_object_or_404(Account, pk=account_id)
    building = get_object_or_404(Building, pk=building_id)
    if account.pk <> building.account.pk:
        raise Http404
    building_dict = {}    
    for z in building._meta.get_all_field_names():
        try:
            building_dict[z.replace('_',' ')] = building.__getattribute__(z)
        except AttributeError:
            pass
    context = {
        'building':        building,
        'building_dict':   building_dict,
        'accounts':        request.user.account_set.order_by('id'),
        'account':         building.account,
        'thirty_days_ago': (datetime.now() + timedelta(-30)),
        'alerts':          building.get_all_alerts(reverse_boolean=True)
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/building_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

def meter_detail(request, account_id, meter_id):
    account = get_object_or_404(Account, pk=account_id)
    meter = get_object_or_404(Meter, pk=meter_id)
    if account.pk <> meter.account.pk:
        raise Http404
    meter_dict = {}    
    for z in meter._meta.get_all_field_names():
        try:
            meter_dict[z.replace('_',' ')] = meter.__getattribute__(z)
        except AttributeError:
            pass
    cost_by_month = meter.get_dataframe_as_table(['Month','Cost (exp)','Cost (act)'])
    if len(cost_by_month) == 1: cost_by_month = False
    consumption_by_month = meter.get_dataframe_as_table(['Month','Consumption (exp)','Consumption (act)'])
    if len(consumption_by_month) == 1: consumption_by_month = False
    demand_by_month = meter.get_dataframe_as_table(['Month','Peak Demand (exp)','Peak Demand (act)'])
    if len(demand_by_month) == 1: demand_by_month = False
    context = {
        'account':              account,
        'accounts':             request.user.account_set.order_by('id'),
        'meter':                meter,
        'meter_dict':           meter_dict,
        'alerts':               meter.get_all_alerts(reverse_boolean=True),
        'cost_by_month':        json.dumps(cost_by_month),
        'consumption_by_month': json.dumps(consumption_by_month),
        'demand_by_month':      json.dumps(demand_by_month),
        'consumption_units':    json.dumps(meter.units.split(',')[1]),
        'demand_units':         json.dumps(meter.units.split(',')[0])
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/meter_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

def equipment_detail(request, account_id, equipment_id):
    account = get_object_or_404(Account, pk=account_id)
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if account.pk <> equipment.meters.all()[0].account.pk: 
        #need to close loophole here: Equipments not forced to single Account
        #here we assume only one so pick the first Meter we find and get its Account
        #could add code (here?) to confirm all connected meters share same Account and flag if not
        raise Http404
    equipment_dict = {}    
    for z in equipment._meta.get_all_field_names():
        try:
            equipment_dict[z.replace('_',' ')] = equipment.__getattribute__(z)
        except AttributeError:
            pass
    context = {
        'account':        account,
        'accounts':       request.user.account_set.order_by('id'),
        'equipment':      equipment,
        'equipment_dict': equipment_dict,
        'alerts':         equipment.get_all_alerts(reverse_boolean=True)
    }
    user_account_IDs = [str(x.pk) for x in request.user.account_set.all()]
    if account_id in user_account_IDs:
        template_name = 'buildingspeakapp/equipment_detail.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)

