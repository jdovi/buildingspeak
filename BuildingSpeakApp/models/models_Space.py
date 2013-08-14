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

class SpaceMeterApportionment(models.Model):
    """Intermediate model defining
    relationship of Meter to Space."""
    
    #relationships
    meter = models.ForeignKey('Meter')
    space = models.ForeignKey('Space')
    
    #attributes
    assigned_fraction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3,
                            help_text='fraction of meter consumption/demand/cost assigned to space')
    
    #functions
    def __unicode__(self):
        return str(self.meter.name + ' - ' + self.space.name)
    class Meta:
        app_label = 'BuildingSpeakApp'

class Space(models.Model):
    """Model for subspaces of
    Buildings.  Accepts image
    file of floorplan or view
    of space."""
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    building = models.ForeignKey('Building')
    messages = models.ManyToManyField('Message')
    readers = models.ManyToManyField('Reader')
    schedules = models.ManyToManyField('OperatingSchedule')
    meters = models.ManyToManyField('Meter', through='SpaceMeterApportionment')
    
    #file-related attributes
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_space, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed space data')
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this space?')
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
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_space, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided space data')
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this space?')
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
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_space, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing floorplan or general space image')
    
    #attributes
    square_footage = models.IntegerField(null=True, blank=True, help_text='floor area, SF')
    max_occupancy = models.IntegerField(null=True, blank=True, help_text='space occupancy limit')
    space_type = models.CharField(blank=True, max_length=200,
                                     choices=[('Automotive Facility', 'Automotive Facility'),
                                              ('Convention Center', 'Convention Center'),
                                              ('Courthouse', 'Courthouse'),
                                              ('Data Center', 'Data Center'),
                                              ('Dining: Bar Lounge/Leisure', 'Dining: Bar Lounge/Leisure'),
                                              ('Dining: Cafeteria/Fast Food', 'Dining: Cafeteria/Fast Food'),
                                              ('Dining: Family', 'Dining: Family'),
                                              ('Dormitory', 'Dormitory'),
                                              ('Excercise Center', 'Excercise Center'),
                                              ('Gymnasium', 'Gymnasium'),
                                              ('Health Care Clinic', 'Health Care Clinic'),
                                              ('Hospital', 'Hospital'),
                                              ('Hotel', 'Hotel'),
                                              ('Library', 'Library'),
                                              ('Manufacturing Facility', 'Manufacturing Facility'),
                                              ('Motel', 'Motel'),
                                              ('Movie Theater', 'Movie Theater'),
                                              ('Multi-Family Housing', 'Multi-Family Housing'),
                                              ('Multi-Purpose', 'Multi-Purpose'),
                                              ('Museum', 'Museum'),
                                              ('Office', 'Office'),
                                              ('Parking Garage', 'Parking Garage'),
                                              ('Penitentiary', 'Penitentiary'),
                                              ('Performing Arts Theater', 'Performing Arts Theater'),
                                              ('Police/Fire Station', 'Police/Fire Station'),
                                              ('Post Office', 'Post Office'),
                                              ('Religious Building', 'Religious Building'),
                                              ('Residential', 'Residential'),
                                              ('Retail', 'Retail'),
                                              ('School/University', 'School/University'),
                                              ('Sports Arena', 'Sports Arena'),
                                              ('Town Hall', 'Town Hall'),
                                              ('Transportation', 'Transportation'),
                                              ('Warehouse', 'Warehouse'),
                                              ('Workshop', 'Workshop'),
                                              ('Other', 'Other')])
    EIA_type = models.CharField(blank=True, max_length=200,
                                     choices=[('Education', 'Education'),
                                              ('Food Sales', 'Food Sales'),
                                              ('Food Service', 'Food Service'),
                                              ('Health Care - Inpatient', 'Health Care - Inpatient'),
                                              ('Health Care - Outpatient', 'Health Care - Outpatient'),
                                              ('Lodging', 'Lodging'),
                                              ('Mercantile - Retail (Other Than Mall)', 'Mercantile - Retail (Other Than Mall)'),
                                              ('Mercantile - Enclosed and Strip Malls', 'Mercantile - Enclosed and Strip Malls'),
                                              ('Office', 'Office'),
                                              ('Public Assembly', 'Public Assembly'),
                                              ('Public Order and Safety', 'Public Order and Safety'),
                                              ('Religious Worship', 'Religious Worship'),
                                              ('Service', 'Service'),
                                              ('Warehouse and Storage', 'Warehouse and Storage'),
                                              ('Other', 'Other')])
    ESPM_type = models.CharField(blank=True, max_length=200,
                                     choices=[('Bank/Financial Institution', 'Bank/Financial Institution'),
                                              ('Courthouse', 'Courthouse'),
                                              ('Data Center', 'Data Center'),
                                              ('Dormitory / Residence Hall', 'Dormitory / Residence Hall'),
                                              ('Hospital (General Medical and Surgical)', 'Hospital (General Medical and Surgical)'),
                                              ('Hotel', 'Hotel'),
                                              ('House of Worship', 'House of Worship'),
                                              ('K-12 School', 'K-12 School'),
                                              ('Medical Office', 'Medical Office'),
                                              ('Multifamily Housing', 'Multifamily Housing'),
                                              ('Municipal Wastewater Treatment Plant', 'Municipal Wastewater Treatment Plant'),
                                              ('Office', 'Office'),
                                              ('Other', 'Other'),
                                              ('Parking', 'Parking'),
                                              ('Retail Store', 'Retail Store'),
                                              ('Senior Care Facility', 'Senior Care Facility'),
                                              ('Supermarket', 'Supermarket'),
                                              ('Swimming Pool', 'Swimming Pool'),
                                              ('Warehouse (Refrigerated or Unrefrigerated)', 'Warehouse (Refrigerated or Unrefrigerated)'),
                                              ('Water Treatment and Distribution Utility', 'Water Treatment and Distribution Utility')])
    
    #functions
    def get_all_alerts(self, reverse_boolean):
        f = [self.messages.filter(message_type='Alert')]
        e = [x.messages.filter(message_type='Alert') for x in self.equipment_set.all()]
        m = [x.messages.filter(message_type='Alert') for x in self.meters.all()]
        layered_message_list = [e,m,f]
        flat_message_list = [item for sublist in layered_message_list for item in sublist]
        return sorted(flat_message_list, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_messages(self, reverse_boolean):
        f = [self.messages.all()]
        e = [x.messages.all() for x in self.equipment_set.all()]
        m = [x.messages.all() for x in self.meters.all()]
        layered_message_list = [e,m,f]
        flat_message_list = [item for sublist in layered_message_list for item in sublist]
        return sorted(flat_message_list, key=attrgetter('when'), reverse=reverse_boolean)
    def account_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(self.building.account.id,)), self.building.account.name)
    account_name_for_admin.allow_tags = True
    account_name_for_admin.short_description = 'Account'
    def building_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(self.building.id,)), self.building.name)
    building_name_for_admin.allow_tags = True
    building_name_for_admin.short_description = 'Building'
    def connected_equipments_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
    connected_equipments_for_admin.allow_tags = True
    connected_equipments_for_admin.short_description = 'Connected Equipments'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Space, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'Model Info',
                        subject = 'Model created.',
                        comment = 'This Space was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
            s = Reader(name='SOCCo',help_text='space occupancy observed by local sensors',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='SOCCp',help_text='space occupancy provided by remote source',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='SOCCc',help_text='space occupancy calculated by models',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
        super(Space, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'
