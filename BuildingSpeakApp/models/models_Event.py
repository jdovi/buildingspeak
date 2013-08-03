#Deprecated 05/28/2013.

#deprecating this model in favor of a combined Message/Event model since
#Event model is so similar to Message model.


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

from models_functions import *

class Event(models.Model):
    """Attributes:
        name, description, when
        
    Model to track relevant events that
    impact other models."""
    
    name = models.CharField(blank=True, max_length=200)
    description = models.CharField(blank=True, max_length=200)
    when = models.DateTimeField(null=True, blank=True)
    #functions
    def __unicode__(self):
        return self.name
    class Meta:
        app_label = 'BuildingSpeakApp'
