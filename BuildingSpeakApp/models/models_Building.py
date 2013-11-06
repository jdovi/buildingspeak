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

class BuildingMeterApportionment(models.Model):
    """Intermediate model defining
    relationship of Meter to Building."""
    
    #relationships
    meter = models.ForeignKey('Meter')
    building = models.ForeignKey('Building')
    
    #attributes
    assigned_fraction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3,
                        help_text='fraction of meter consumption/demand/cost assigned to building')
    
    #functions
    def __unicode__(self):
        return str(self.meter.name + ' - ' + self.building.name)
    class Meta:
        app_label = 'BuildingSpeakApp'

class Building(models.Model):
    """Model for Buildings.  Accepts
    image logo file.  Parents Spaces."""
    name = models.CharField(max_length=200)
    building_type = models.CharField(blank=True, max_length=200,
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
    
    #relationships
    account = models.ForeignKey('Account')
    weather_station = models.ForeignKey('WeatherStation')
    meters = models.ManyToManyField('Meter', through='BuildingMeterApportionment')
    messages = models.ManyToManyField('Message')
    readers = models.ManyToManyField('Reader')
    schedules = models.ManyToManyField('OperatingSchedule')

    
    #file-related attributes
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_building, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed building data')
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this building?')
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
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_building, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided building data')
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this building?')
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
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_building, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing building image')
    
    #single value attributes
    street_address = models.CharField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=200)
    state = models.CharField(blank=True, max_length=2)
    zip_code = models.CharField(blank=True, max_length=10)

    age = models.IntegerField(null=True, blank=True)
    square_footage = models.IntegerField(null=True, blank=True)
    stories = models.IntegerField(null=True, blank=True)
    max_occupancy = models.IntegerField(null=True, blank=True, help_text='building occupancy limit')

    first_name = models.CharField(blank=True, max_length=200)
    last_name = models.CharField(blank=True, max_length=200)
    title = models.CharField(blank=True, max_length=200)
    email = models.EmailField(blank=True, max_length=75)
    phone = models.CharField(blank=True, max_length=20)
    
   
    #functions
    def get_all_events(self, reverse_boolean):
        b = [self.messages.filter(message_type='Event').order_by('-when')]
        e = [x.messages.filter(message_type='Event').order_by('-when') for x in self.equipment_set.all()]
        m = [x.messages.filter(message_type='Event').order_by('-when') for x in self.meters.all()]
        f = [x.messages.filter(message_type='Event').order_by('-when') for x in self.space_set.all()]
        layered_message_list = [b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_alerts(self, reverse_boolean):
        b = [self.messages.filter(message_type='Alert').order_by('-when')]
        e = [x.messages.filter(message_type='Alert').order_by('-when') for x in self.equipment_set.all()]
        m = [x.messages.filter(message_type='Alert').order_by('-when') for x in self.meters.all()]
        f = [x.messages.filter(message_type='Alert').order_by('-when') for x in self.space_set.all()]
        layered_message_list = [b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_messages(self, reverse_boolean):
        b = [self.messages.all()]
        e = [x.messages.all() for x in self.equipment_set.all()]
        m = [x.messages.all() for x in self.meters.all()]
        f = [x.messages.all() for x in self.space_set.all()]
        layered_message_list = [b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def __unicode__(self):
        return self.name + ' - ' + self.street_address
    def account_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(self.account.id,)), self.account.name)
    account_for_admin.allow_tags = True
    account_for_admin.short_description = 'Account'
    def weather_station_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_weatherstation_change',args=(self.weather_station.id,)), self.weather_station.name)
    weather_station_for_admin.allow_tags = True
    weather_station_for_admin.short_description = 'Weather Station'
    def connected_meters_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meters.all()])
    connected_meters_for_admin.allow_tags = True
    connected_meters_for_admin.short_description = 'Connected Meters'
    def connected_equipments_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
    connected_equipments_for_admin.allow_tags = True
    connected_equipments_for_admin.short_description = 'Connected Equipments'
    def connected_spaces_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_space_change',args=(space.id,)), space.name) for space in self.space_set.all()])
    connected_spaces_for_admin.allow_tags = True
    connected_spaces_for_admin.short_description = 'Connected Spaces'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Building, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'Model Info',
                        subject = 'Model created.',
                        comment = 'This Building was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
            s = Reader(name='BOCCo',help_text='building occupancy observed by local sensors',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='BOCCp',help_text='building occupancy provided by remote source',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='BOCCc',help_text='building occupancy calculated by models',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
        super(Building, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'
