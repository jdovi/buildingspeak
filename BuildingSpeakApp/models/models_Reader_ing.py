import pandas as pd
from django.db import models
from django.core import urlresolvers
from decimal import Decimal

from models_functions import *

class Reader(models.Model):
    """Attributes:
        name, help_text, active, source,
        column_index, column_header,
        expected_min, expected_max
        
    Model of sensor used to track some
    parameter.  Contains a set of Readings.
    
    Functions:
        get_reader_time_series
        load_reader_time_series"""
    
    name = models.CharField(blank=True, max_length=200)  #convention is four letter acronym + o/p/c
    help_text = models.CharField(blank=True, max_length=200)
    active = models.BooleanField(blank=True,
                   help_text='is this Reader currently being tracked by a data file?')
    source = models.IntegerField(null=True, blank=True,choices=[(1,1),(2,2),(3,3)],
                   help_text='data file source: 1 = observed, 2 = provided, 3 = calculated')
    column_index = models.IntegerField(null=True, blank=True,
                   help_text='column number in data file, excluding index column; used during Reader data loading')
    column_header = models.CharField(blank=True, max_length=200,
                   help_text='column header from data file, dumped here during Reader data loading, for reference only')
    expected_min = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                   help_text='lower limit (measured data below this value will be rejected and flagged)')
    expected_max = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                   help_text='upper limit (measured data above this value will be rejected and flagged)')
    #relationships
    messages = models.ManyToManyField('Message')
    #functions
    def __unicode__(self):
        return self.name
    def connected_models_for_admin(self):
        equiplist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
        acctlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(acct.id,)), acct.name) for acct in self.account_set.all()])
        bldglist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
        meterlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
        spacelist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_space_change',args=(space.id,)), space.name) for space in self.space_set.all()])
        return ''.join([equiplist,acctlist,bldglist,meterlist,spacelist])
    connected_models_for_admin.allow_tags = True
    connected_models_for_admin.short_description = 'Connected Models'
    def get_reader_time_series(self):
        """No inputs.
        
        Returns timeseries of Reader's data."""
        
        t = [x.when for x in self.reading_set.order_by('when')]
        v = [x.value for x in self.reading_set.order_by('when')]
        s = pd.Series(v,index=t)
        s = s.sort_index()
        return s
    def load_reader_time_series(self, time_series):
        """Inputs:
            timeseries
            
        Loads given timeseries into Reader by
        creating Readings attached to Reader.
        
        WARNING: probably need to put logic
        here to check for integer and convert
        to float or straight to Decimal!"""
        
        for i,v in enumerate(time_series):
            r = Reading(when=time_series.index[i],
                        value=Decimal(v),
                        reader=self)
            r.save()
    class Meta:
        app_label = 'BuildingSpeakApp'
    
class Reading(models.Model):
    """Attributes:
        when, value
        
    Model to record a single data point.
    Must attach to a Reader."""
    
    when = models.DateTimeField()
    value = models.DecimalField(max_digits=20, decimal_places=3)
    #relationships
    reader = models.ForeignKey('Reader')
    #functions
    def __unicode__(self):
        return str(self.value)
    class Meta:
        app_label = 'BuildingSpeakApp'
