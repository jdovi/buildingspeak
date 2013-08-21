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
from operator import itemgetter, attrgetter
from djorm_pgarray.fields import ArrayField
from model_utils.managers import InheritanceManager
from storages.backends.s3boto import S3BotoStorage
from django.contrib.auth.models import User

from models_functions import *
from models_Message import Message

class UserProfile(models.Model):
    """Model for storing extra
    fields for Users."""
    organization = models.CharField(blank=True, max_length=200)
    
    #relationships
    messages = models.ManyToManyField('Message')
    user = models.OneToOneField(User)
    
    #file-related attributes
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_user, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing user image')
    
    #functions
    def user_for_admin(self):
        user_name_value = self.user.username
        if user_name_value is None: user_name_value = '(empty)'
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_userprofile_change',args=(self.user.id,)), user_name_value)
    user_for_admin.allow_tags = True
    user_for_admin.short_description = 'Username (from User)'
    def user_id_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:auth_user_change',args=(self.user.id,)), str(self.user.id))
    user_id_for_admin.allow_tags = True
    user_id_for_admin.short_description = 'User'
    def __unicode__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        if self.id is None:
            super(UserProfile, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'Model Info',
                        subject = 'Model created.',
                        comment = 'This UserProfile was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
        super(UserProfile, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'
