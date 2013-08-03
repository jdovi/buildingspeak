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
from models_Reader_ing import Reader

class Account(models.Model):
    """Model for customer.  Accepts
    image logo file.  Parents
    Buildings and Meters."""
    name = models.CharField(max_length=200)
    account_type = models.CharField(blank=True, max_length=200,
                                    choices=[('Commercial', 'Commercial'),
                                             ('Industrial', 'Industrial'),
                                             ('Residential', 'Residential')])
    
    #relationships
    messages = models.ManyToManyField('Message')
    users = models.ManyToManyField(User)
    readers = models.ManyToManyField('Reader')
    events = models.ManyToManyField('Event')
    schedules = models.ManyToManyField('OperatingSchedule')

    
    #file-related attributes
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_account, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed account data')
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this account?')
    observed_file_skiprows = models.IntegerField(null=True, blank=True, help_text='number of rows before data header row (will be skipped when reading data)')
    observed_file_column_for_indexing = models.IntegerField(null=True, blank=True, help_text='column number of time stamp data to use for indexing')
    observed_file_time_zone = models.CharField(blank=True, max_length=200,
                    help_text='time zone compatible with pytz module, default=US/Eastern',
                    default='US/Eastern')
    observed_file_GMT_offset = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2,
                    help_text='GMT/UTC offset as decimal number used to adjust hour values read in from data file',
                    default=Decimal(-5))
    observed_file_adjusts_for_DST = models.BooleanField(blank=True,
                    help_text='dates in data file are always already adjusted for DST?',
                    default=False)
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_account, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided account data')
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this account?')
    provided_file_skiprows = models.IntegerField(null=True, blank=True, help_text='number of rows before data header row (will be skipped when reading data)')
    provided_file_column_for_indexing = models.IntegerField(null=True, blank=True, help_text='column number of time stamp data to use for indexing')
    provided_file_time_zone = models.CharField(blank=True, max_length=200,
                    help_text='time zone compatible with pytz module, default=US/Eastern',
                    default='US/Eastern')
    provided_file_GMT_offset = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2,
                    help_text='GMT/UTC offset as decimal number used to adjust hour values read in from data file',
                    default=Decimal(-5))
    provided_file_adjusts_for_DST = models.BooleanField(blank=True,
                    help_text='dates in data file are always already adjusted for DST?',
                    default=False)
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_account, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing account image')
    
    #single value attributes
    street_address = models.CharField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=200)
    state = models.CharField(blank=True, max_length=2)
    zip_code = models.CharField(blank=True, max_length=10)
    launch_date = models.DateTimeField(null=True, blank=True)

    first_name = models.CharField(blank=True, max_length=200)
    last_name = models.CharField(blank=True, max_length=200)
    title = models.CharField(blank=True, max_length=200)
    email = models.EmailField(blank=True, max_length=75)
    phone = models.CharField(blank=True, max_length=20)

    status = models.CharField(blank=True, max_length=200,
                              choices=[('Active', 'Active'),
                                       ('Closed', 'Closed'),
                                       ('Delinquent', 'Delinquent'),
                                       ('Inactive', 'Inactive')])
    monthly_payment = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2,
                                          help_text='total monthly payment due')
    last_invoice_date = models.DateTimeField(null=True, blank=True,
                                             help_text='date last invoice sent')
    last_paid_date = models.DateTimeField(null=True, blank=True,
                                          help_text='date last payment received')
    next_invoice_date = models.DateTimeField(null=True, blank=True,
                                             help_text='date next invoice scheduled to be sent')
    bill_addressee = models.CharField(blank=True, max_length=200,
                                      help_text='person to whom invoice is sent/addressed')
    bill_email_address = models.EmailField(blank=True, max_length=75,
                                           help_text='email address where invoice should be sent')
    bill_street_address = models.CharField(blank=True, max_length=200)
    bill_city = models.CharField(blank=True, max_length=200)
    bill_state = models.CharField(blank=True, max_length=2)
    bill_zip_code = models.CharField(blank=True, max_length=10)
    bill_to_email = models.BooleanField(blank=True, default=True,
                        help_text='send invoice as email attachment?')
    bill_to_location = models.BooleanField(blank=True, default=True,
                        help_text='send hard copy invoice to mailing address?')
    
    #functions
    def get_all_alerts(self, reverse_boolean):
        a = [self.messages.filter(message_type='Alert')]
        b = [x.messages.filter(message_type='Alert') for x in self.building_set.all()]
        e = [x.messages.filter(message_type='Alert') for x in self.account_equipments()]
        m = [x.messages.filter(message_type='Alert') for x in self.meter_set.all()]
        f_0 = [x.space_set.all() for x in self.building_set.all()]
        f_0 = [item for sublist in f_0 for item in sublist]
        f = [x.messages.filter(message_type='Alert') for x in f_0]
        layered_message_list = [a,b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_messages(self, reverse_boolean):
        a = self.messages.all()
        b = [x.messages.all() for x in self.building_set.all()]
        e = [x.messages.all() for x in self.account_equipments()]
        m = [x.messages.all() for x in self.meter_set.all()]
        f_0 = [x.space_set.all() for x in self.building_set.all()]
        f_0 = [item for sublist in f_0 for item in sublist]
        f = [x.messages.all() for x in f_0]
        layered_message_list = [a,b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def __unicode__(self):
        return self.name
    def connected_buildings_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
    connected_buildings_for_admin.allow_tags = True
    connected_buildings_for_admin.short_description = 'Connected Buildings'
    def connected_meters_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
    connected_meters_for_admin.allow_tags = True
    connected_meters_for_admin.short_description = 'Connected Meters'
    def connected_equipments_for_admin(self):
        equiplist = [bldg.equipment_set.all() for bldg in self.building_set.all()]
        equiplist = [item for sublist in equiplist for item in sublist]
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in equiplist])
    connected_equipments_for_admin.allow_tags = True
    connected_equipments_for_admin.short_description = 'Connected Equipments'
    def account_equipments(self):
        i = []
        for j in [x.equipment_set.all() for x in self.building_set.all()]:
            i.extend(j)
        return i
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Account, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'Model Info',
                        subject = 'Model created.',
                        comment = 'This Account was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
        super(Account, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'
