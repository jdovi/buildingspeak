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

class UnitSchedule(models.Model):
    """Subunit of OperatingSchedule used
    to represent a repeating schedule
    conducive to cron representation.
    These are combined via superposition
    to create OperatingSchedules."""
    name = models.CharField(max_length=200)
    
    #relationships
    messages = models.ManyToManyField('Message')

    #attributes
#    day_of_week_list = dbarray.TextArrayField(null=True, blank=True)
#    month_list = dbarray.TextArrayField(null=True, blank=True)
#    day_of_month_list = dbarray.TextArrayField(null=True, blank=True)
#    hour_list = dbarray.TextArrayField(null=True, blank=True)
#    minute_list = dbarray.TextArrayField(null=True, blank=True)
    cron_string = models.CharField(null=True, blank=True, max_length=200)
    day_of_week_list = ArrayField(blank=True, null=True, dbtype='text')
    month_list = ArrayField(blank=True, null=True, dbtype='text')
    day_of_month_list = ArrayField(blank=True, null=True, dbtype='text')
    hour_list = ArrayField(blank=True, null=True, dbtype='text')
    minute_list = ArrayField(blank=True, null=True, dbtype='text')
    
    #functions
    def set_cron(self, croniterinput):
        try:
            cron_iter_obj = croniter(croniterinput)
        except Exception:
            print 'UnitSchedule reset failed, likely due to invalid syntax of inputs.'
        self.cron_string = croniterinput
        
        self.minute_list = [str(x) for x in cron_iter_obj.expanded[0]]
        self.hour_list = [str(x) for x in cron_iter_obj.expanded[1]]
        self.day_of_month_list = [str(x) for x in cron_iter_obj.expanded[2]]
        self.month_list = [str(x) for x in cron_iter_obj.expanded[3]]
        self.day_of_week_list = [str(x) for x in cron_iter_obj.expanded[4]]

    def check_minute(self,dt):
        if self.minute_list == ['*']:
            answer = True
        else:
            answer = str(dt.minute) in self.minute_list
        return answer
    def check_hour(self,dt):
        if self.hour_list == ['*']:
            answer = True
        else:
            answer = str(dt.hour) in self.hour_list
        return answer
    def check_day_of_month(self,dt):
        if self.day_of_month_list == ['*']:
            answer = True
        else:
            answer = str(dt.day) in self.day_of_month_list
        return answer
    def check_month(self,dt):
        if self.month_list == ['*']:
            answer = True
        else:
            answer = str(dt.month) in self.month_list
        return answer
    def check_day_of_week(self,dt):
        if dt.weekday() == 6:  #need if block to address datetime using Mon=0, Sun=6
            daynum = str(0)
        else:
            daynum = str(dt.weekday()+1)
        if self.day_of_week_list == ['*']:
            answer = True
        else:
            answer = daynum in self.day_of_week_list
        return answer

    def check(self,dt):
        answer = (self.check_minute(dt) and self.check_hour(dt) and 
                  self.check_day_of_month(dt) and self.check_month(dt) and
                  self.check_day_of_week(dt))
        return answer
        
    def get_current_year_8760_list(self): #returns an 8760 profile based on the current year in UTC
        cron_iter_obj = croniter('0 * * * *',datetime(timezone.now().year-1,12,31,23))
        schedule_array = []
        for i in range(0,8760):
            schedule_array.append(self.check(cron_iter_obj.get_next(datetime)))
        return schedule_array
        
    def get_annual_operating_hours_count(self):
        return sum(self.get_current_year_8760_list())
        
    def __unicode__(self):
        return self.name

    def connected_operating_schedules_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_operatingschedule_change',args=(opsch.id,)), opsch.name) for opsch in self.operatingschedule_set.all()])
    connected_operating_schedules_for_admin.allow_tags = True
    connected_operating_schedules_for_admin.short_description = 'Connected Operating Schedules'

    def save(self, *args, **kwargs):
        try:
            cron_iter_obj = croniter(self.cron_string)
        except Exception:
            print 'UnitSchedule reset failed, likely due to invalid syntax of inputs.'
        
        self.minute_list = [str(x) for x in cron_iter_obj.expanded[0]]
        self.hour_list = [str(x) for x in cron_iter_obj.expanded[1]]
        self.day_of_month_list = [str(x) for x in cron_iter_obj.expanded[2]]
        self.month_list = [str(x) for x in cron_iter_obj.expanded[3]]
        self.day_of_week_list = [str(x) for x in cron_iter_obj.expanded[4]]
        super(UnitSchedule, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'

class OperatingSchedule(models.Model):
    """General purpose schedule model.
    Comprised of UnitSchedules that
    are cron based.  Only the abstract
    representation is stored; get_
    current_year_8760_list function
    provides hourly schedule."""
    name = models.CharField(max_length=200)
    
    #relationships
    messages = models.ManyToManyField('Message')
    units = models.ManyToManyField('UnitSchedule')

    #attributes


    #functions
    def unit_schedules_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_unitschedule_change',args=(unitsch.id,)), unitsch.name) for unitsch in self.units.all()])
    unit_schedules_for_admin.allow_tags = True
    unit_schedules_for_admin.short_description = 'Unit Schedules'
    def connected_models_for_admin(self):
        equiplist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
        acctlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(acct.id,)), acct.name) for acct in self.account_set.all()])
        bldglist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
        meterlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
        spacelist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_space_change',args=(space.id,)), space.name) for space in self.space_set.all()])
        return ''.join([equiplist,acctlist,bldglist,meterlist,spacelist])
    connected_models_for_admin.allow_tags = True
    connected_models_for_admin.short_description = 'Connected Models'
    def check(self,dt):
        return max([x.check(dt) for x in self.units.all()])
    def get_current_year_8760_list(self):
        cron_iter_obj = croniter('0 * * * *',datetime(timezone.now().year-1,12,31,23))
        schedule_array = []
        for i in range(0,8760):
            schedule_array.append(self.check(cron_iter_obj.get_next(datetime)))
        return schedule_array

    def __unicode__(self):
        return self.name
    class Meta:
        app_label = 'BuildingSpeakApp'
