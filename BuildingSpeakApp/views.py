# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from BuildingSpeakApp.models import Account, Building, Meter, Equipment, WeatherStation
from BuildingSpeakApp.models import UserSettingsForm, MeterUploadForm, Message
import json
from decimal import Decimal
from django.forms.models import modelform_factory
from django.contrib.auth.models import User
from rq import Queue
from worker import conn

class SuccessMessage(object):
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
            m = SuccessMessage()
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

@login_required
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

@login_required
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

    if request.method == 'POST': # If the form has been submitted...
        form = MeterUploadForm(request.POST, request.FILES) # A form bound to the POST data
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
            q = Queue(connection=conn)
            result = q.enqueue(meter.upload_bill_data)            
            m = SuccessMessage()
            m.comment = 'Bill data has been uploaded.'
            reloading = True
    elif request.method == 'GET':
        if meter.bill_data_file is None:
            latest_bill_data_file = None
        else:
            latest_bill_data_file = meter.bill_data_file
        form = MeterUploadForm({}, {'bill_data_file': latest_bill_data_file})
        reloading = False
    context = {
        'user':                 request.user,
        'form':                 form,
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

@login_required
def management(request):
    context = {
        'weather_stations':      WeatherStation.objects.all(),
    }
    if request.user in User.objects.filter(is_active = True).filter(is_staff = True).filter(is_superuser = True):
        template_name = 'buildingspeakapp/management.html'
    else:
        template_name = 'buildingspeakapp/access_denied.html'
    return render(request, template_name, context)
