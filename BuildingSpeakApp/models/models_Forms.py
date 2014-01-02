#import dbarray
import pandas as pd
from pytz import UTC
from numpy import NaN
from django.db import models
from croniter import croniter
from django.utils import timezone
from django.core import urlresolvers
from decimal import getcontext, Decimal
from datetime import datetime, timedelta
from djorm_pgarray.fields import ArrayField
from model_utils.managers import InheritanceManager
from storages.backends.s3boto import S3BotoStorage
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models.loading import get_model
from django.db.models import Model
from django import forms

from models_functions import *
from models_WeatherStation import WeatherStation
from models_Meter import Meter

class UserSettingsForm(forms.Form):
    """Form to set BuildingSpeak
    user login info."""
    username = forms.CharField(required=False, max_length=30)
    email = forms.EmailField(required=False)
    mobile_phone = forms.CharField(required=False, max_length=20)
    desk_phone = forms.CharField(required=False, max_length=20)
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)
    organization = forms.CharField(required=False, max_length=30)
    image_file = forms.FileField(required=False)
    
class MeterDataUploadForm(forms.Form):
    """Form to upload Meter bill
    data from Excel file."""
    bill_data_file = forms.FileField(required=False)
    meter = forms.ChoiceField(required=False,
                              choices=[(str(mtr.id) + ' - ' + mtr.name, mtr.id) for mtr in Meter.objects.all()])
    
class WeatherDataUploadForm(forms.Form):
    """Form to upload weather
    data file for Weather Station."""
    weather_data_file = forms.FileField(required=False)
    weather_station = forms.ChoiceField(choices=[(str(ws.id) + ' - ' + ws.name, ws.id) for ws in WeatherStation.objects.all()])
    