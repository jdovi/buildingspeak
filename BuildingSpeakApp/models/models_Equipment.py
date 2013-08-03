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

class Equipment(models.Model):
    """Model for all energy consuming
    Equipment.  Specific Equipment
    classes such as RooftopUnit inherit
    from this class.  Accepts photo and
    nameplate image files."""
    objects = InheritanceManager() #used with django-model-utils; query all Equipment subclasses together
    
    #relationships
    messages = models.ManyToManyField('Message')
    meters = models.ManyToManyField('Meter')
    buildings = models.ManyToManyField('Building')
    spaces = models.ManyToManyField('Space')
    readers = models.ManyToManyField('Reader')
    events = models.ManyToManyField('Event')
    schedule = models.ForeignKey('OperatingSchedule')

    
    #administrative info
    name = models.CharField(blank=True, max_length=200)
    equipment_type = models.CharField(blank=True, max_length=200,
                    help_text='equipment type identifier, e.g. Rooftop Unit, Pump, etc.',
                    choices=[('Rooftop Unit', 'Rooftop Unit'),
                             ('Pump', 'Pump')])
    location = models.CharField(blank=True, max_length=200)
    description = models.CharField(blank=True, max_length=200)
    
    #file-related attributes
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_equipment, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed equipment data')
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this equipment?')
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
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_equipment, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided equipment data')
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this equipment?')
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
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_equipment, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing equipment image')
    nameplate_file = models.FileField(null=True, blank=True, upload_to=nameplate_file_path_equipment, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing equipment nameplate image')
    #functions
    def update_universals(self):
        """No inputs.
        
        Reads primary consumption Readers and
        converts/sums into kBtu Readers."""
        pass
    def get_all_alerts(self, reverse_boolean):
        return sorted(self.messages.filter(message_type='Alert'), key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_messages(self, reverse_boolean):
        return sorted(self.messages.all(), key=attrgetter('when'), reverse=reverse_boolean)
    def __unicode__(self):
        return self.name
    def account_name_for_admin(self):
        if len(self.buildings.all()) == 0:
            answer = None
        else:
            answer = '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(self.buildings.all()[0].account.id,)), self.buildings.all()[0].account.name) #assumes all equips attached to only one account
        return answer
    account_name_for_admin.allow_tags = True
    account_name_for_admin.short_description = 'Account'
    def connected_buildings_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.buildings.all()])
    connected_buildings_for_admin.allow_tags = True
    connected_buildings_for_admin.short_description = 'Connected Buildings'
    def connected_spaces_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_space_change',args=(space.id,)), space.name) for space in self.spaces.all()])
    connected_spaces_for_admin.allow_tags = True
    connected_spaces_for_admin.short_description = 'Connected Spaces'
    def connected_meters_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meters.all()])
    connected_meters_for_admin.allow_tags = True
    connected_meters_for_admin.short_description = 'Connected Meters'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Equipment, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'Model Info',
                        subject = 'Model created.',
                        comment = 'This Equipment was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
            
            #universal energy units kBtu (for comparing multiple fuels on common unit basis)
            s = Reader(name='kBtuo',help_text='total: energy (kBtu) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='kBtup',help_text='total: energy (kBtu) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='kBtuc',help_text='total: energy (kBtu) calculated by models')
            s.save()
            self.readers.add(s)
            
            #---------------------------------------------------------------------observed
            #electricity
            s = Reader(name='ELCAo',help_text='electricity: current (A) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELVVo',help_text='electricity: voltage (V) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELPHo',help_text='electricity: phase (1,3) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELPFo',help_text='electricity: power factor (dimensionless) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELKWo',help_text='electricity: power (kW) observed by local sensors')
            s.save()
            self.readers.add(s)
            
            #natural gas
            s = Reader(name='NGINo',help_text='natural gas: input power (Btu/h) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGOUo',help_text='natural gas: delivered power (Btu/h) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGEFo',help_text='natural gas: thermal efficiency (dimensionless) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGFLo',help_text='natural gas: flow rate (ft^3/min) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGHVo',help_text='natural gas: heating value (Btu/ft^3) observed by local sensors')
            s.save()
            self.readers.add(s)
            
            #steam
            s = Reader(name='STHIo',help_text='steam: input enthalpy (Btu/lb) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STHOo',help_text='steam: output enthalpy (Btu/lb) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STBHo',help_text='steam: delivered power (Btu/h) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STFLo',help_text='steam: flow rate (lb/hr) observed by local sensors')
            s.save()
            self.readers.add(s)
            
            #chilled water
            s = Reader(name='CWFLo',help_text='chilled water: flow rate (gal/min) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTIo',help_text='chilled water: inlet temperature (' + u"\u00b0" + 'F) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTOo',help_text='chilled water: outlet temperature (' + u"\u00b0" + 'F) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTNo',help_text='chilled water: delivered power (tons) observed by local sensors')
            s.save()
            self.readers.add(s)
            
            #hot water
            s = Reader(name='HWFLo',help_text='hot water: flow rate (gal/min) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWTIo',help_text='hot water: inlet temperature (' + u"\u00b0" + 'F) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWTOo',help_text='hot water: outlet temperature (' + u"\u00b0" + 'F) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWBHo',help_text='hot water: delivered power (Btu/h) observed by local sensors')
            s.save()
            self.readers.add(s)
            
            #fuel oil
            s = Reader(name='FOBIo',help_text='fuel oil: input power (Btu/h) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOBOo',help_text='fuel oil: delivered power (Btu/h) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOEFo',help_text='fuel oil: thermal efficiency (dimensionless) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOFLo',help_text='fuel oil: flow rate (gal/min) observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOHVo',help_text='fuel oil: heating value (Btu/gal) observed by local sensors')
            s.save()
            self.readers.add(s)

            #---------------------------------------------------------------------provided
            #electricity
            s = Reader(name='ELCAp',help_text='electricity: current (A) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELVVp',help_text='electricity: voltage (V) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELPHp',help_text='electricity: phase (1,3) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELPFp',help_text='electricity: power factor (dimensionless) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELKWp',help_text='electricity: power (kW) provided by remote source')
            s.save()
            self.readers.add(s)
            
            #natural gas
            s = Reader(name='NGINp',help_text='natural gas: input power (Btu/h) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGOUp',help_text='natural gas: delivered power (Btu/h) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGEFp',help_text='natural gas: thermal efficiency (dimensionless) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGFLp',help_text='natural gas: flow rate (ft^3/min) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGHVp',help_text='natural gas: heating value (Btu/ft^3) provided by remote source')
            s.save()
            self.readers.add(s)
            
            #steam
            s = Reader(name='STHIp',help_text='steam: input enthalpy (Btu/lb) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STHOp',help_text='steam: output enthalpy (Btu/lb) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STBHp',help_text='steam: delivered power (Btu/h) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STFLp',help_text='steam: flow rate (lb/hr) provided by remote source')
            s.save()
            self.readers.add(s)
            
            #chilled water
            s = Reader(name='CWFLp',help_text='chilled water: flow rate (gal/min) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTIp',help_text='chilled water: inlet temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTOp',help_text='chilled water: outlet temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTNp',help_text='chilled water: delivered power (tons) provided by remote source')
            s.save()
            self.readers.add(s)
            
            #hot water
            s = Reader(name='HWFLp',help_text='hot water: flow rate (gal/min) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWTIp',help_text='hot water: inlet temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWTOp',help_text='hot water: outlet temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWBHp',help_text='hot water: delivered power (Btu/h) provided by remote source')
            s.save()
            self.readers.add(s)
            
            #fuel oil
            s = Reader(name='FOBIp',help_text='fuel oil: input power (Btu/h) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOBOp',help_text='fuel oil: delivered power (Btu/h) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOEFp',help_text='fuel oil: thermal efficiency (dimensionless) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOFLp',help_text='fuel oil: flow rate (gal/min) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOHVp',help_text='fuel oil: heating value (Btu/gal) provided by remote source')
            s.save()
            self.readers.add(s)

            #---------------------------------------------------------------------calculated
            #electricity
            s = Reader(name='ELCAc',help_text='electricity: current (A) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELVVc',help_text='electricity: voltage (V) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELPHc',help_text='electricity: phase (1,3) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELPFc',help_text='electricity: power factor (dimensionless) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='ELKWc',help_text='electricity: power (kW) calculated by models')
            s.save()
            self.readers.add(s)
            
            #natural gas
            s = Reader(name='NGINc',help_text='natural gas: input power (Btu/h) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGOUc',help_text='natural gas: delivered power (Btu/h) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGEFc',help_text='natural gas: thermal efficiency (dimensionless) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGFLc',help_text='natural gas: flow rate (ft^3/min) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='NGHVc',help_text='natural gas: heating value (Btu/ft^3) calculated by models')
            s.save()
            self.readers.add(s)
            
            #steam
            s = Reader(name='STHIc',help_text='steam: input enthalpy (Btu/lb) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STHOc',help_text='steam: output enthalpy (Btu/lb) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STBHc',help_text='steam: delivered power (Btu/h) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STFLc',help_text='steam: flow rate (lb/hr) calculated by models')
            s.save()
            self.readers.add(s)
            
            #chilled water
            s = Reader(name='CWFLc',help_text='chilled water: flow rate (gal/min) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTIc',help_text='chilled water: inlet temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTOc',help_text='chilled water: outlet temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='CWTNc',help_text='chilled water: delivered power (tons) calculated by models')
            s.save()
            self.readers.add(s)
            
            #hot water
            s = Reader(name='HWFLc',help_text='hot water: flow rate (gal/min) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWTIc',help_text='hot water: inlet temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWTOc',help_text='hot water: outlet temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='HWBHc',help_text='hot water: delivered power (Btu/h) calculated by models')
            s.save()
            self.readers.add(s)
            
            #fuel oil
            s = Reader(name='FOBIc',help_text='fuel oil: input power (Btu/h) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOBOc',help_text='fuel oil: delivered power (Btu/h) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOEFc',help_text='fuel oil: thermal efficiency (dimensionless) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOFLc',help_text='fuel oil: flow rate (gal/min) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='FOHVc',help_text='fuel oil: heating value (Btu/gal) calculated by models')
            s.save()
            self.readers.add(s)


        super(Equipment, self).save(*args, **kwargs)
        
    class Meta:
        app_label = 'BuildingSpeakApp'
