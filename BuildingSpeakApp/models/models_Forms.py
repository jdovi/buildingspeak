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
    