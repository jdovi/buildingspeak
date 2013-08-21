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

class UserSettingsForm(forms.Form):
    """Form to set BuildingSpeak
    user login info."""
    username = forms.CharField(required=False, max_length=30)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)
    organization = forms.CharField(required=False, max_length=30)
    image_file = forms.FileField(required=False)