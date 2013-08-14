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

class Utility(models.Model):
    """Model for utility providers.  Accepts
    logo image file.  Parents Rate Schedules."""
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    messages = models.ManyToManyField('Message')
    
    #file-related attributes
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_utility, 
                    storage=S3BotoStorage(location='utility_files'),
                    help_text='link to utility logo file')

    #functions
    def rate_schedules_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_rateschedule_change',args=(rs.id,)), rs.name) for rs in self.rateschedule_set.all()])
    rate_schedules_for_admin.allow_tags = True
    rate_schedules_for_admin.short_description = 'Rates'
    def __unicode__(self):
        return self.name
    class Meta:
        app_label = 'BuildingSpeakApp'
