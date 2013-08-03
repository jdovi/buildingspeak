#import dbarray
import pandas as pd
from pytz import UTC
from numpy import NaN
from croniter import croniter
from django.db import models
from django.utils import timezone
from django.core import urlresolvers
from decimal import getcontext, Decimal
from datetime import datetime, timedelta
from djorm_pgarray.fields import ArrayField
from model_utils.managers import InheritanceManager
from storages.backends.s3boto import S3BotoStorage
from django.contrib.auth.models import User

#-------------------------------------------global functions and settings
def make_pandas_data_frame(list_of_series, series_names=[]):
    """make pandas DataFrame from a list of series and optional
       list of series names"""
    series_dict = {}
    #have to use counter because list_of_series.index(s) doesn't work
    if len(series_names)==0:
        for i,s in enumerate(list_of_series):
            series_dict[i] = s
    else:
        for i,s in enumerate(list_of_series):
            series_dict[series_names[i]] = s
    df = pd.DataFrame(series_dict)
    return df
# these functions used to set upload_to variables passed to data file FileField attributes
def data_file_path_equipment(instance, filename):
    return '/'.join(['%06d' % instance.buildings.all()[0].account.pk,
                     'equipments',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def data_file_path_account(instance, filename):
    return '/'.join(['%06d' % instance.pk,
                     filename])
def data_file_path_building(instance, filename):
    return '/'.join(['%06d' % instance.account.pk,
                     'buildings',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def data_file_path_meter(instance, filename):
    return '/'.join(['%06d' % instance.account.pk,
                     'meters',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def bill_data_file_path_meter(instance, filename):
    return '/'.join(['%06d' % instance.account.pk,
                     'meters',
                     '%06d' % instance.pk + '_' + instance.name,
                     'bill_data_files',
                     filename])
def data_file_path_floor(instance, filename):
    return '/'.join(['%06d' % instance.building.account.pk,
                     'buildings',
                     '%06d' % instance.building.pk + '_' + instance.building.name,
                     'floors',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def rate_file_path_rate_schedule(instance, filename):
    return '/'.join(['%06d' % instance.utility.pk,
                     'rate_schedules',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])

# these functions used to set upload_to variables passed to image file FileField attributes
def image_file_path_equipment(instance, filename):
    return '/'.join(['%06d' % instance.buildings.all()[0].account.pk,
                     'equipments',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def image_file_path_account(instance, filename):
    return '/'.join(['%06d' % instance.pk,
                     filename])
def image_file_path_building(instance, filename):
    return '/'.join(['%06d' % instance.account.pk,
                     'buildings',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def image_file_path_meter(instance, filename):
    return '/'.join(['%06d' % instance.account.pk,
                     'meters',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def image_file_path_floor(instance, filename):
    return '/'.join(['%06d' % instance.building.account.pk,
                     'buildings',
                     '%06d' % instance.building.pk + '_' + instance.building.name,
                     'floors',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def image_file_path_utility(instance, filename):
    return '/'.join(['%06d' % instance.pk,
                     filename])

# these functions used to set upload_to variables passed to nameplate file FileField attributes
def nameplate_file_path_equipment(instance, filename):
    return '/'.join(['%06d' % instance.buildings.all()[0].account.pk,
                     'equipments',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])
def nameplate_file_path_meter(instance, filename):
    return '/'.join(['%06d' % instance.account.pk,
                     'meters',
                     '%06d' % instance.pk + '_' + instance.name,
                     filename])



#-----------------------------------------------------models
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
    events = models.ManyToManyField('Event')
    messages = models.ManyToManyField('Message')
    #functions
    def __unicode__(self):
        return self.name
    def connected_models_for_admin(self):
        equiplist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
        acctlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(acct.id,)), acct.name) for acct in self.account_set.all()])
        bldglist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
        meterlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
        floorlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_floor_change',args=(floor.id,)), floor.name) for floor in self.floor_set.all()])
        return ''.join([equiplist,acctlist,bldglist,meterlist,floorlist])
    connected_models_for_admin.allow_tags = True
    connected_models_for_admin.short_description = 'Connected Models'
    def get_reader_time_series(self):
        """No inputs.
        
        Returns timeseries of Reader's data."""
        
        t = [x.when for x in self.reading_set.all()]
        v = [x.value for x in self.reading_set.all()]
        return pd.Series(v,index=t)
    def load_reader_time_series(self, time_series):
        """Inputs:
            timeseries
            
        Loads given timeseries into Reader by
        creating Readings attached to Reader."""
        
        for i,v in enumerate(time_series):
            r = Reading(when=time_series.index[i],
                        value=Decimal(v),
                        reader=self)
            r.save()
    
class Reading(models.Model):
    """Attributes:
        when, value
        
    Model to record a single data point.
    Must attach to a Reader."""
    
    when = models.DateTimeField()
    value = models.DecimalField(max_digits=20, decimal_places=3)
    #relationships
    reader = models.ForeignKey('Reader')
    events = models.ManyToManyField('Event')
    #functions
    def __unicode__(self):
        return str(self.value)

class Monther(models.Model):
    """No attributes.
    
    Stores Monthlings.  Must attach to
    Meter.  Matches BillingCycler's
    periods.
    
    Functions:
        get_monther_period_dataframe
        load_monther_period_dataframe"""
    
    name = models.CharField(blank=True, max_length=200)  #convention is four letter acronym + o/p/c
    help_text = models.CharField(blank=True, max_length=200)
    #relationships
    events = models.ManyToManyField('Event')
    messages = models.ManyToManyField('Message')
    meter = models.ForeignKey('Meter')
    #functions
    def __unicode__(self):
        return self.name
    def get_monther_period_dataframe(self):
        """No inputs.
        
        Returns Monther's dataframe."""
        
        if self.monthling_set.count() == 0:
            m = Message(when=timezone.now(),
                        message_type='Code Warning',
                        subject='nothing to return',
                        comment='Monther %s, get_monther_period_dataframe called when no Monthlings present.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:
            t = [x.when for x in self.monthling_set.all()]
            bdm = pd.Series([x.billing_demand for x in self.monthling_set.all()],index=t)
            pdm = pd.Series([x.peak_demand for x in self.monthling_set.all()],index=t)
            con = pd.Series([x.consumption for x in self.monthling_set.all()],index=t)
            kpd = pd.Series([x.kBtuh_peak_demand for x in self.monthling_set.all()],index=t)
            kco = pd.Series([x.kBtu_consumption for x in self.monthling_set.all()],index=t)
            dol = pd.Series([x.cost for x in self.monthling_set.all()],index=t)
            df = pd.DataFrame({'Billing Demand' : bdm,
                               'Peak Demand' : pdm,
                               'Consumption' : con,
                               'kBtuh Peak Demand' : kpd,
                               'kBtu Consumption' : kco,
                               'Cost' : dol})
            df.index = df.index.to_period(freq='M')
            df = df.sort_index()
        return df
    def load_monther_period_dataframe(self, df):
        """Inputs:
            df
              (columns:Billing Demand,Peak Demand,
                 Consumption, kBtuh Peak Demand,
                 kBtu Consumption, Cost)
        
        Loads given dataframe into Monther
        by adding Monthlings. Calling
        function should ensure match with
        BillingCycler periods."""

        if (('Billing Demand' in df.columns) and ('Cost' in df.columns) and
            ('Peak Demand' in df.columns) and ('Consumption' in df.columns) and
            ('kBtuh Peak Demand' in df.columns) and ('kBtu Consumption' in df.columns) and
            (len(df)>0) and (type(df.index)==pd.tseries.period.PeriodIndex) ):
            df = df.sort_index()
            self.monthling_set.all().delete()
            for i in range(0,len(df)):
                per_date = df.index[i].to_timestamp()
                if per_date.tzinfo is None:
                            per_date = UTC.localize(per_date)
                mlg = Monthling(
                        when = per_date,
                        billing_demand = Decimal(df['Billing Demand'][i]),
                        peak_demand = Decimal(df['Peak Demand'][i]),
                        consumption = Decimal(df['Consumption'][i]),
                        kBtuh_peak_demand = Decimal(df['kBtuh Peak Demand'][i]),
                        kBtu_consumption = Decimal(df['kBtu Consumption'][i]),
                        cost = Decimal(df['Cost'][i]),
                        monther = self)
                mlg.save()
            m = Message(when=timezone.now(),
                        message_type='Code Success',
                        subject='model updated',
                        comment='Loaded dataframe into Monther %s.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = True
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='expected condition failed',
                        comment='Monther %s, load_monther_period_dataframe given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = False
        return success
    
class Monthling(models.Model):
    """Attributes:
        when, billing_demand, peak_demand,
        consumption, kBtuh_peak_demand,
        kBtu_consumption, cost
        
    A 'monthly Reading' model used to track
    key meter parameters including monthly
    costs.  Must attach to Monther."""
    
    when = models.DateTimeField()
    billing_demand = models.DecimalField(max_digits=20, decimal_places=3)
    peak_demand = models.DecimalField(max_digits=20, decimal_places=3)
    consumption = models.DecimalField(max_digits=20, decimal_places=3)
    kBtuh_peak_demand = models.DecimalField(max_digits=20, decimal_places=3)
    kBtu_consumption = models.DecimalField(max_digits=20, decimal_places=3)
    cost = models.DecimalField(max_digits=20, decimal_places=3)
    #relationships
    monther = models.ForeignKey('Monther')
    events = models.ManyToManyField('Event')
    #functions
    def __unicode__(self):
        return str(self.value)

class BillingCycler(models.Model):
    """No attributes.
    
    Stores BillingCycles.  Must attach to
    Meter.
    
    Functions:
        get_billing_cycler_period_dataframe
        load_billing_cycler_period_dataframe"""
    #relationships
    meter = models.ForeignKey('Meter')
    messages = models.ManyToManyField('Message')
    #functions
    def meter_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(self.meter.id,)), self.meter.name)
    meter_for_admin.allow_tags = True
    meter_for_admin.short_description = 'Meter'
    def billing_cycles_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_billingcycle_change',args=(bcyc.id,)), 'BillingCycle') for bcyc in self.billingcycle_set.all()])
    billing_cycles_for_admin.allow_tags = True
    billing_cycles_for_admin.short_description = 'Billing Cycles'
    def get_billing_cycler_period_dataframe(self):
        """No inputs.
        
        Returns BillingCycler's dataframe."""
        
        if self.billingcycle_set.count() == 0:
            m = Message(when=timezone.now(),
                                      message_type='Code Warning',
                                      subject='nothing to return',
                                      comment='BillingCycler %s, get_billing_cycler_period_dataframe called when no BillingCycles present.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:
            pdates = pd.Series([x.period_date for x in self.billingcycle_set.all()])
            sdates = pd.Series([x.start_date for x in self.billingcycle_set.all()],
                                index = pdates)
            edates = pd.Series([x.end_date for x in self.billingcycle_set.all()],
                                index = pdates)
            df = pd.DataFrame({'Start Date' : sdates,
                               'End Date' : edates})
            df.index = df.index.to_period(freq='M')
            df = df.sort_index()
        return df
    def load_billing_cycler_period_dataframe(self, df):
        """Inputs: 
            dataframe (in BillingCycler format)
            
        Stores the provided dataframe in
        itself by adding BillingCycles.
        Each new Start Date must be the
        same as the previous End Date."""
        
        if (('Start Date' in df.columns) and (len(df)>0) and
            ('End Date' in df.columns)   and (type(df.index)==pd.tseries.period.PeriodIndex)):
            df = df.sort_index()
            contiguous_check = df['End Date'].shift(1) == df['Start Date'] #start check on month 2
            if False in contiguous_check[1:].values: #1st is always False due to shift, but if other False then abort
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='noncontiguous billing cycle dates',
                            comment='BillingCycler %s, load_billing_cycler_period_dataframe function given noncontiguous billing cycles, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = False
            else:
                self.billingcycle_set.all().delete()
                for i in range(0,len(df)):
                    per_date = df.index[i].to_timestamp()
                    if per_date.tzinfo is None:
                                per_date = UTC.localize(per_date)
                    bc = BillingCycle(
                            period_date = per_date,
                            start_date = df['Start Date'][i],
                            end_date = df['End Date'][i],
                            billingcycler = self)
                    bc.save()
                m = Message(when=timezone.now(),
                            message_type='Code Success',
                            subject='model updated',
                            comment='Loaded dataframe into BillingCycler %s.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = True
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='expected condition failed',
                        comment='BillingCycler %s, load_billing_cycler_period_dataframe given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = False
        return success
    
class BillingCycle(models.Model):
    """Attributes (all datetimes):
        period_date
        start_date
        end_date
        
    Stores billing cycle start/end dates
    and date representing period.  Must
    attach to BillingCycler."""
    
    period_date = models.DateTimeField()  #date used to represent pandas Period
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    #relationships
    billingcycler = models.ForeignKey('BillingCycler')
    messages = models.ManyToManyField('Message')
    #functions
    def billing_cycler_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_billingcycler_change',args=(self.billingcycler.id,)), 'BillingCycler')
    billing_cycler_for_admin.allow_tags = True
    billing_cycler_for_admin.short_description = 'Billing Cycler'
    
class Message(models.Model):
    #Message class used to store all BuildingSpeak messages
    #use "object.messages.all()" to retrieve entire message log for a given object
    #use "object.messages.filter(field1 = value1)" to retrieve a subset of object's message log
    #use "object.messages.add(newmessage)" to add a Message to an object,
    #       where newmessage = Message(...set attributes here...)
    #message_type options: Code Warning, Code Error, User
    """Inputs:
        when = datetime
        message_type = string
        subject = string
        comment = text
        notes = text (staff notes entered via admin)
        
    Message may be attached to any BuildingSpeak
    model.  Used for capturing errors and 
    warnings during code execution as well as
    notifications to users."""
    
    when = models.DateTimeField(null=True)
    dismissed = models.DateTimeField(null=True)
    message_type = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    comment = models.TextField()
    notes = models.TextField(blank=True)
    def __unicode__(self):
        return ': '.join([self.message_type,self.subject,self.comment])
    
class Event(models.Model):
    """Attributes:
        name, description, when
        
    Model to track relevant events that
    impact other models."""
    
    name = models.CharField(blank=True, max_length=200)
    description = models.CharField(blank=True, max_length=200)
    when = models.DateTimeField()
    #functions
    def __unicode__(self):
        return self.name

class Unit_Schedule(models.Model):
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
            print 'Unit_Schedule reset failed, likely due to invalid syntax of inputs.'
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

    def save(self, *args, **kwargs):
        try:
            cron_iter_obj = croniter(self.cron_string)
        except Exception:
            print 'Unit_Schedule reset failed, likely due to invalid syntax of inputs.'
        
        self.minute_list = [str(x) for x in cron_iter_obj.expanded[0]]
        self.hour_list = [str(x) for x in cron_iter_obj.expanded[1]]
        self.day_of_month_list = [str(x) for x in cron_iter_obj.expanded[2]]
        self.month_list = [str(x) for x in cron_iter_obj.expanded[3]]
        self.day_of_week_list = [str(x) for x in cron_iter_obj.expanded[4]]
        super(Unit_Schedule, self).save(*args, **kwargs)

class Operating_Schedule(models.Model):
    name = models.CharField(max_length=200)
    
    #relationships
    messages = models.ManyToManyField('Message')
    units = models.ManyToManyField('Unit_Schedule')

    #attributes


    #functions
    def unit_schedules_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_unit_schedule_change',args=(unitsch.id,)), unitsch.name) for unitsch in self.units.all()])
    unit_schedules_for_admin.allow_tags = True
    unit_schedules_for_admin.short_description = 'Unit Schedules'
    def connected_models_for_admin(self):
        equiplist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
        acctlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(acct.id,)), acct.name) for acct in self.account_set.all()])
        bldglist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
        meterlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
        floorlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_floor_change',args=(floor.id,)), floor.name) for floor in self.floor_set.all()])
        return ''.join([equiplist,acctlist,bldglist,meterlist,floorlist])
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

class Account(models.Model):
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
    schedules = models.ManyToManyField('Operating_Schedule')

    
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
    def update_readers(self):
        if self.observed_file_track:
            df = pd.read_csv(self.observed_file.url,
                             skiprows=self.observed_file_skiprows,
                             parse_dates=True,
                             index_col=self.observed_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.observed_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=1).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
        if self.provided_file_track:
            df = pd.read_csv(self.provided_file.url,
                             skiprows=self.provided_file_skiprows,
                             parse_dates=True,
                             index_col=self.provided_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.provided_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=2).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
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
                        message_type = 'notification',
                        subject = 'Account created',
                        comment = 'This Account was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
        super(Account, self).save(*args, **kwargs)
        
        
class Building(models.Model):
    name = models.CharField(max_length=200)
    building_type = models.CharField(blank=True, max_length=200,
                                     choices=[('Office', 'Office'),
                                              ('Warehouse', 'Warehouse')])
    
    #relationships
    account = models.ForeignKey(Account)
    meters = models.ManyToManyField('Meter') #need way to apply fraction if one meter serves >1 bldg
    messages = models.ManyToManyField('Message')
    readers = models.ManyToManyField('Reader')
    events = models.ManyToManyField('Event')
    schedules = models.ManyToManyField('Operating_Schedule')

    
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
    def update_readers(self):
        if self.observed_file_track:
            df = pd.read_csv(self.observed_file.url,
                             skiprows=self.observed_file_skiprows,
                             parse_dates=True,
                             index_col=self.observed_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.observed_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=1).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
        if self.provided_file_track:
            df = pd.read_csv(self.provided_file.url,
                             skiprows=self.provided_file_skiprows,
                             parse_dates=True,
                             index_col=self.provided_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.provided_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=2).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
    def __unicode__(self):
        return self.street_address
    def account_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(self.account.id,)), self.account.name)
    account_for_admin.allow_tags = True
    account_for_admin.short_description = 'Account'
    def connected_meters_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meters.all()])
    connected_meters_for_admin.allow_tags = True
    connected_meters_for_admin.short_description = 'Connected Meters'
    def connected_equipments_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
    connected_equipments_for_admin.allow_tags = True
    connected_equipments_for_admin.short_description = 'Connected Equipments'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Building, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'notification',
                        subject = 'Building created',
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

class Floor(models.Model):
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    building = models.ForeignKey(Building)
    messages = models.ManyToManyField('Message')
    readers = models.ManyToManyField('Reader')
    events = models.ManyToManyField('Event')
    schedules = models.ManyToManyField('Operating_Schedule')

    
    #file-related attributes
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_floor, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed floor data')
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this floor?')
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
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_floor, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided floor data')
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this floor?')
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
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_floor, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing floorplan image')
    
    #attributes
    square_footage = models.IntegerField(null=True, blank=True, help_text='floor area, SF')
    max_occupancy = models.IntegerField(null=True, blank=True, help_text='floor occupancy limit')
    
    #functions
    def building_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(self.building.id,)), self.building.name)
    building_name_for_admin.allow_tags = True
    building_name_for_admin.short_description = 'Building'
    def building_type_for_admin(self):
        return self.building.building_type
    building_type_for_admin.allow_tags = True
    building_type_for_admin.short_description = 'Building Type'
    def connected_equipments_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
    connected_equipments_for_admin.allow_tags = True
    connected_equipments_for_admin.short_description = 'Connected Equipments'
    def update_readers(self):
        if self.observed_file_track:
            df = pd.read_csv(self.observed_file.url,
                             skiprows=self.observed_file_skiprows,
                             parse_dates=True,
                             index_col=self.observed_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.observed_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=1).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
        if self.provided_file_track:
            df = pd.read_csv(self.provided_file.url,
                             skiprows=self.provided_file_skiprows,
                             parse_dates=True,
                             index_col=self.provided_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.provided_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=2).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Floor, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'notification',
                        subject = 'Floor created',
                        comment = 'This Floor was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
            s = Reader(name='FOCCo',help_text='floor occupancy observed by local sensors',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='FOCCp',help_text='floor occupancy provided by remote source',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='FOCCc',help_text='floor occupancy calculated by models',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
        super(Floor, self).save(*args, **kwargs)

class Meter(models.Model):
    name = models.CharField(max_length=200)
    utility_type = models.CharField(blank=True, max_length=200,
                                    choices=[('electricity','electricity'),
                                             ('natural gas','natural gas'),
                                             ('domestic water','domestic water'),
                                             ('chilled water','chilled water'),
                                             ('hot water','hot water'),
                                             ('steam','steam'),
                                             ('fuel oil (1,2,4), diesel','fuel oil (1,2,4), diesel'),
                                             ('fuel oil (5,6)','fuel oil (5,6)'),
                                             ('kerosene','kerosene'),
                                             ('propane and liquid propane','propane and liquid propane'),
                                             ('coal (anthracite)','coal (anthracite)'),
                                             ('coal (bituminous)','coal (bituminous)'),
                                             ('coke','coke'),
                                             ('wood','wood'),
                                             ('other','other')])
    location = models.CharField(blank=True, max_length=200)
    units = models.CharField(blank=True, max_length=200, help_text='units of measurement (power,energy)',
                                    choices=[('kW,kWh','kW,kWh'),
                                             ('therms/h,therms','therms/h,therms'),
                                             ('gpm,gal','gpm,gal'),
                                             ('kBtuh,kBtu','kBtuh,kBtu'),
                                             ('MMBtuh,MMBtu','MMBtuh,MMBtu'),
                                             ('Btuh,Btu','Btuh,Btu'),
                                             ('tons,ton-h','tons,ton-h'),
                                             ('MW,MWh','MW,MWh'),
                                             ('cf/m,cf','cf/m,cf'),
                                             ('ccf/h,ccf','ccf/h,ccf'),
                                             ('kcf/h,kcf','kcf/h,kcf'),
                                             ('MMcf/h,MMcf','MMcf/h,MMcf'),
                                             ('m^3/h,m^3','m^3/h,m^3'),
                                             ('lb/h,lb','lb/h,lb'),
                                             ('klb/h,klb','klb/h,klb'),
                                             ('MMlb/h,MMlb','MMlb/h,MMlb'),
                                             ('lpm,lit','lpm,lit'),
                                             ('ton(wt)/h,tons(wt)','ton(wt)/h,tons(wt)'),
                                             ('lbs(wt)/h,lbs(wt)','lbs(wt)/h,lbs(wt)'),
                                             ('klbs(wt)/h,klbs(wt)','klbs(wt)/h,klbs(wt)'),
                                             ('MMlbs(wt)/h,MMlbs(wt)','MMlbs(wt)/h,MMlbs(wt)')])
    
    #relationships
    utility = models.ForeignKey('Utility')
    rate_schedule = models.ForeignKey('Rate_Schedule')
    account = models.ForeignKey(Account)
    messages = models.ManyToManyField('Message')
    readers = models.ManyToManyField('Reader')
    events = models.ManyToManyField('Event')
    schedules = models.ManyToManyField('Operating_Schedule')
    
    #file-related attributes
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_meter, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed meter data')
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this meter?')
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
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_meter, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided meter data')
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this meter?')
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
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_meter, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing meter image')
    nameplate_file = models.FileField(null=True, blank=True, upload_to=nameplate_file_path_meter, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing meter nameplate image')
#    billing_cycle_file = models.FileField(null=True, blank=True, upload_to=data_file_path_meter, 
#                    storage=S3BotoStorage(location='user_data_files'),
#                    help_text='link to text file containing billing cycle start and end dates; must be formatted correctly')
    bill_data_file = models.FileField(null=True, blank=True, upload_to=bill_data_file_path_meter, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to text file containing monthly bill data; must be formatted correctly')

    #single value atrributes
    make = models.CharField(blank=True, max_length=200, help_text='manufacturer of meter')
    model = models.CharField(blank=True, max_length=200, help_text='model number of meter')
    serial_number = models.CharField(blank=True, max_length=200, help_text='serial number of meter')
    
    #functions
    def get_billing_cycler_period_dataframe(self):
        """No inputs.
        
        Returns the Meter's BillingCycler's dataframe."""
        return self.billingcycler_set.get(meter=self).get_billing_cycler_period_dataframe()
    def update_monthers(self):
        """No inputs.
        
        Updates Meter's Reader-based Monthers.
        NOT WRITTEN YET."""
        pass
    def get_bill_data_period_dataframe(self):
        return self.monther_set.get(name='BILLp').get_monther_period_dataframe()
    def update_bill_data(self, file_location=0):
        """Input:
            [file_location]
                (default: MeterInstance.bill_data_url)
        
        Reads Bill Data File and loads into
        Meter's BILLp Monther, respecting any
        pre-existing data unless Overwrite
        column in Bill Data File indicates
        otherwise."""
        if not(file_location): file_location = self.bill_data_file.url
        
        try:
            readbd = pd.read_csv(file_location,
                                 skiprows=0,
                                 usecols=['Overwrite', 'Start Date', 'End Date', 'Billing Demand',
                                          'Peak Demand', 'Consumption', 'Cost'])
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='file not found',
                        comment='Meter %s failed on update_bill_data function when attempting to read Bill Data File.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            if (('Start Date' in readbd.columns) and ('End Date' in readbd.columns) and
                ('Billing Demand' in readbd.columns) and ('Peak Demand' in readbd.columns) and
                ('Consumption' in readbd.columns) and ('Cost' in readbd.columns) and
                (len(readbd)>0) ):
                readbd['Start Date'] = readbd['Start Date'].apply(pd.to_datetime)
                readbd['End Date'] = readbd['End Date'].apply(pd.to_datetime)
                readbd['Start Date'] = readbd['Start Date'].apply(UTC.localize)
                readbd['End Date'] = readbd['End Date'].apply(UTC.localize)
                readbd['Billing Demand'] = readbd['Billing Demand'].apply(Decimal)
                readbd['Peak Demand'] = readbd['Peak Demand'].apply(Decimal)
                readbd['Consumption'] = readbd['Consumption'].apply(Decimal)
                readbd['Cost'] = readbd['Cost'].apply(Decimal)
                t = [self.assign_period_datetime(dates=[readbd['Start Date'][i],
                                                        readbd['End Date'][i]]) for i in range(0,len(readbd))]
                if None in t:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='unable to assign',
                                comment='Meter %s failed on update_bill_data function at assign_period_datetime function, Bill Data File does not have appropriate dates.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                else:
                    readbd.index = pd.PeriodIndex(t, freq='M')
                    
                    storedbc = self.billingcycler_set.get(meter=self).get_billing_cycler_period_dataframe()
                    if storedbc is None:
                        newbc = readbd[['Start Date','End Date']] #no logic required, keep all rows for storage
                        newbc = newbc.sort_index()
                    else:
                        #the approach here was used because dataframe.combine_first fails when a df only has one row
                        #boolean vector for "is period not in stored billing cycler?"
                        notinstoredbc = [readbd.index[i] not in storedbc.index for i in range(0,len(readbd))]
                        #boolean vector for "overwrite?; use Overwrite from file, otherwise set all to False
                        try:
                            overwrite = [(True and b or False) and True for b in readbd['Overwrite'].values]
                        except:
                            overwrite = [False for b in readbd['Start Date'].values]
                        v = [] #we want to exclude periods in readbd that are in storedbc but have overwrite = 0
                        for i in range(0,len(notinstoredbc)):
                            v.append(notinstoredbc[i] or overwrite[i])
                        keepfromreadbd = readbd[['Start Date','End Date']][v] #readbd's 'never-stored' and 'to-be-overwritten' periods
                        keepfromstored = storedbc[[storedbc.index[i] not in keepfromreadbd.index for i in range(0,len(storedbc))]]
                        #now combine with keepfromstored
                        if len(keepfromstored)==0 and len(keepfromreadbd)>0:
                            newbc = keepfromreadbd
                        elif len(keepfromstored)>0 and len(keepfromreadbd)==0:
                            newbc = keepfromstored
                            m = Message(when=timezone.now(),
                                    message_type='Code Warning',
                                    subject='no new Billing Cycles to load',
                                    comment='Meter %s found no new Billing Cycles during update_bill_data function.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                        elif len(keepfromstored)>0 and len(keepfromreadbd)>0:
                            newbc = pd.concat([keepfromreadbd, keepfromstored])
                        else:
                            newbc = keepfromstored
                            m = Message(when=timezone.now(),
                                    message_type='Code Warning',
                                    subject='no new Billing Cycles to load',
                                    comment='Meter %s found no new Billing Cycles during update_bill_data function.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                        newbc = newbc.sort_index()
                    
                    storedbd = self.monther_set.get(name='BILLp').get_monther_period_dataframe()
                    if storedbd is None:
                        newbd = readbd[['Billing Demand', 'Peak Demand', 'Consumption', 'Cost']] #no logic required, keep all rows for storage
                        newbd = newbd.sort_index()
                    else:
                        #the approach here was used because dataframe.combine_first fails when a df only has one row
                        #boolean vector for "is period not in stored bill data?"
                        notinstoredbd = [readbd.index[i] not in storedbd.index for i in range(0,len(readbd))]
                        #boolean vector for "overwrite?; use Overwrite from file, otherwise set all to False
                        try:
                            overwrite = [(True and b or False) and True for b in readbd['Overwrite'].values]
                        except:
                            overwrite = [False for b in readbd['Start Date'].values]
                        v = [] #we want to exclude periods in readbd that are in storedbd but have overwrite = 0
                        for i in range(0,len(notinstoredbd)):
                            v.append(notinstoredbd[i] or overwrite[i])
                        keepfromreadbd = readbd[['Billing Demand', 'Peak Demand', 'Consumption', 'Cost']][v] #readbd's 'never-stored' and 'to-be-overwritten' periods
                        keepfromstored = storedbd[[storedbd.index[i] not in keepfromreadbd.index for i in range(0,len(storedbd))]]
                        #now combine with keepfromstored
                        if len(keepfromstored)==0 and len(keepfromreadbd)>0:
                            newbd = keepfromreadbd
                        elif len(keepfromstored)>0 and len(keepfromreadbd)==0:
                            newbd = keepfromstored
                            m = Message(when=timezone.now(),
                                    message_type='Code Warning',
                                    subject='no new Bill Data to load',
                                    comment='Meter %s found no new Bill Data during update_bill_data function.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                        elif len(keepfromstored)>0 and len(keepfromreadbd)>0:
                            newbd = pd.concat([keepfromreadbd, keepfromstored])
                        else:
                            newbd = keepfromstored
                            m = Message(when=timezone.now(),
                                    message_type='Code Warning',
                                    subject='no new Bill Data to load',
                                    comment='Meter %s found no new Bill Data during update_bill_data function.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                        newbd = newbd.sort_index()
                    
                    if len(newbc)>0:
                        success = self.billingcycler_set.get(meter=self).load_billing_cycler_period_dataframe(newbc)
                        if success: #only check success, if failed, BillingCycler will report error
                            m = Message(when=timezone.now(),
                                    message_type='Code Success',
                                    subject='updated Billing Cycler',
                                    comment='Meter %s updated its Billing Cycler.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                            
                            #this whole block moved under first 'success' block so that if periods
                            #don't line up and load_billing_cycler_period_dataframe failes, we
                            #don't run load_monther_period_dataframe (which doesn't have the
                            #contiguous dates check)
                            if len(newbd)>0:
                                success = self.add_kBtu_kBtuh(newbd,self.utility_type,self.units)
                                if success is not None: #only check success, if failed, convert function will report error
                                    success = self.monther_set.get(name='BILLp').load_monther_period_dataframe(newbd)
                                    if success:
                                        m = Message(when=timezone.now(),
                                                message_type='Code Success',
                                                subject='updated BILLp Monther',
                                                comment='Meter %s updated its BILLp Monther.' % self.id)
                                        m.save()
                                        self.messages.add(m)
                                        print m
                                    else:
                                        m = Message(when=timezone.now(),
                                                message_type='Code Error',
                                                subject='failed to update BILLp Monther',
                                                comment='Meter %s was unable to update its BILLp Monther.' % self.id)
                                        m.save()
                                        self.messages.add(m)
                                        print m
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='expected contents not found',
                            comment='Meter %s failed on update_bill_data function, Bill Data File does not have appropriate data.' % self.id)
                m.save()
                self.messages.add(m)
                print m
        
    def update_billing_cycler(self, file_location):
        """Input: file_location
        
        Reads Billing Cycle File and loads into
        Meter's BillingCycler, respecting any
        pre-existing data unless Overwrite
        column in Billing Cycle File indicates
        otherwise."""
        try:
            readbc = pd.read_csv(file_location,
                                 skiprows=0,
                                 usecols=['Overwrite', 'Start Date', 'End Date'])
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='file not found',
                        comment='Meter %s failed on update_billing_cycler function when attempting to read Billing Cycle File.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            if (len(readbc)>0) and ('Start Date' in readbc.columns) and ('End Date' in readbc.columns):
                readbc['Start Date'] = readbc['Start Date'].apply(pd.to_datetime)
                readbc['End Date'] = readbc['End Date'].apply(pd.to_datetime)
                readbc['Start Date'] = readbc['Start Date'].apply(UTC.localize)
                readbc['End Date'] = readbc['End Date'].apply(UTC.localize)
                t = [self.assign_period_datetime(dates=[readbc['Start Date'][i],
                                                        readbc['End Date'][i]]) for i in range(0,len(readbc))]
                if None in t:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='unable to assign',
                                comment='Meter %s failed on update_billing_cycler function at assign_period_datetime function, Billing Cycle File does not have appropriate data.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                else:
                    readbc.index = pd.PeriodIndex(t, freq='M')
                    
                    storedbc = self.billingcycler_set.get(meter=self).get_billing_cycler_period_dataframe()
                    if storedbc is None:
                        newbc = readbc[['Start Date','End Date']] #no logic required, keep all of readbc for storage
                        newbc = newbc.sort_index()
                    else:
                        #the approach here was used because dataframe.combine_first fails when a df only has one row
                        #boolean vector for "is period not in stored billing cycler?"
                        notinstoredbc = [readbc.index[i] not in storedbc.index for i in range(0,len(readbc))]
                        #boolean vector for "overwrite?; use Overwrite from file, otherwise set all to False
                        try:
                            overwrite = [(True and b or False) and True for b in readbc['Overwrite'].values]
                        except:
                            overwrite = [False for b in readbc['Start Date'].values]
                        v = [] #we want to exclude periods in readbc that are in storedbc but have overwrite = 0
                        for i in range(0,len(notinstoredbc)):
                            v.append(notinstoredbc[i] or overwrite[i])
                        readbc = readbc[v] #readbc now has only 'never-stored' and 'to-be-overwritten' periods
                        keepfromstored = storedbc[[storedbc.index[i] not in readbc.index for i in range(0,len(storedbc))]]
                        newbc = pd.concat([readbc[['Start Date','End Date']], keepfromstored])
                        newbc = newbc.sort_index()
                    success = self.billingcycler_set.get(meter=self).load_billing_cycler_period_dataframe(newbc)
                    if success:
                        m = Message(when=timezone.now(),
                                message_type='Code Success',
                                subject='updated Billing Cycler',
                                comment='Meter %s updated its Billing Cycler.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                    else:
                        m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='failed to update Billing Cycler',
                                comment='Meter %s was unable to update its Billing Cycler.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='expected contents not found',
                            comment='Meter %s failed on update_billing_cycler function, Billing Cycle File does not have appropriate data.' % self.id)
                m.save()
                self.messages.add(m)
                print m
        
    def assign_period_datetime(self, time_series=[], dates=[]):
        """Inputs:
            time_series or
            dates (list of start/end datetimes)
            
        Returns datetime of first day of
        most frequently occurring month in
        a given time series spanning 25-35
        days to use as basis for Period."""
        
        #raise error if empty inputs
        if (len(time_series)==0 and len(dates)<>2) or type(dates[0])<>datetime or type(dates[1])<>datetime:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='unexpected inputs',
                        comment='Unexpected inputs passed to assign_period_datetime function on meter %s.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            answer = None
        else:
            #need to pull 3 times in case 3 months are represented
            if len(dates)==2:
                t=[dates[0],
                   (dates[1]-dates[0])/2 + dates[0],
                   dates[1]]
            if len(time_series)>0:
                t=[time_series.index[0],
                   time_series.index[len(time_series)/2],
                   time_series.index[-1]]
            #raise error if number of days is outside range
            if (t[2]-t[0]).days < 25 or (t[2]-t[0]).days > 35:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='unexpected inputs',
                            comment='Passed %s days to assign_period_datetime on meter %s, expecting [25,35].' % ((t[2]-t[0]).days,self.id))
                m.save()
                self.messages.add(m)
                print m
                answer = None
            else:
                i = {t[0].month:0, t[1].month:1, t[2].month:2}
                m = [t[0].month, t[1].month, t[2].month]
                y = [t[0].year, t[1].year, t[2].year]
                c = [0, 0, 0]
                j = t[0]
                while j < t[2]:
                    c[i[j.month]] = c[i[j.month]] + 1
                    j = j + timedelta(days=1)
                answer = datetime(year=y[c.index(max(c))], month=m[c.index(max(c))], day=1, tzinfo=UTC)
        return answer
    
    def update_readers(self):
        if self.observed_file_track:
            df = pd.read_csv(self.observed_file.url,
                             skiprows=self.observed_file_skiprows,
                             parse_dates=True,
                             index_col=self.observed_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.observed_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=1).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
        if self.provided_file_track:
            df = pd.read_csv(self.provided_file.url,
                             skiprows=self.provided_file_skiprows,
                             parse_dates=True,
                             index_col=self.provided_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.provided_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=2).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
    def add_kBtu_kBtuh(self, df, fuel_type, units):
        """Inputs:
            dataframe
                (columns: Peak Demand,Consumption)
            fuel_type
                (e.g. MeterInstance.utility_type)
            units
                (e.g. MeterInstance.units)
            
        Returns dataframe with columns of
        kBtuh and kBtu."""
        fuels=['electricity','natural gas','domestic water','chilled water','hot water',
                 'steam','fuel oil (1,2,4), diesel','fuel oil (5,6)','kerosene',
                 'propane and liquid propane','coal (anthracite)','coal (bituminous)',
                 'coke','wood','other']
        unitchoices=['kW,kWh','therms/h,therms','gpm,gal','kBtuh,kBtu','MMBtuh,MMBtu',
                     'Btuh,Btu','tons,ton-h','MW,MWh','cf/m,cf','ccf/h,ccf','kcf/h,kcf',
                     'MMcf/h,MMcf','m^3/h,m^3','lb/h,lb','klb/h,klb','MMlb/h,MMlb',
                     'lpm,lit','ton(wt)/h,tons(wt)','lbs(wt)/h,lbs(wt)','klbs(wt)/h,klbs(wt)',
                     'MMlbs(wt)/h,MMlbs(wt)']
        if ( (len(df)>0) and ('Peak Demand' in df.columns) and ('Consumption' in df.columns) and
            (fuel_type in fuels) and (units in unitchoices) ):
            if fuel_type == 'electricity':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'kW,kWh':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(3.412)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(3.412)
                elif units == 'MW,MWh':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(3412.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(3412.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'natural gas':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'cf/m,cf':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60.0 * 1.029)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.029)
                elif units == 'ccf/h,ccf':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(102.9)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(102.9)
                elif units == 'kcf/h,kcf':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1029.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1029.0)
                elif units == 'MMcf/h,MMcf':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1029000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1029000.0)
                elif units == 'therms/h,therms':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(100.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(100.0)
                elif units == 'm^3/h,m^3':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(36.339)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(36.339)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'domestic water':
                if units == 'gpm,gal':
                    df['kBtuh Peak Demand'] = NaN
                    df['kBtu Consumption'] = NaN
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'steam':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'lb/h,lb':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.194)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.194)
                elif units == 'klb/h,klb':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1194.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1194.0)
                elif units == 'MMlb/h,MMlb':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1194000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1194000.0)
                elif units == 'therms/h,therms':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(100.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(100.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'hot water':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'therms/h,therms':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(100.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(100.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'chilled water':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'tons,ton-h':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'kerosene':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'gpm,gal':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 135.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(135.0)
                elif units == 'lpm,lit':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 35.1)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(35.1)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'fuel oil (1,2,4), diesel':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'gpm,gal':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 138.6905)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(138.6905)
                elif units == 'lpm,lit':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 36.060)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(36.060)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'fuel oil (5,6)':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'gpm,gal':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 149.6905)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(149.6905)
                elif units == 'lpm,lit':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 38.920)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(38.920)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'propane and liquid propane':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'cf/m,cf':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 2.5185)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(2.5185)
                elif units == 'kcf/h,kcf':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(2518.5)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(2518.5)
                elif units == 'gpm,gal':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 91.6476)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(91.6476)
                elif units == 'lpm,lit':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(60 * 23.828)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(23.828)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'coal (anthracite)':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'ton(wt)/h,tons(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(25090.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(25090.0)
                elif units == 'lbs(wt)/h,lbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12.545)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12.545)
                elif units == 'klbs(wt)/h,klbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12545.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12545.0)
                elif units == 'MMlbs(wt)/h,MMlbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12545000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12545000.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'coal (bituminous)':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'ton(wt)/h,tons(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(24930.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(24930.0)
                elif units == 'lbs(wt)/h,lbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12.465)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12.465)
                elif units == 'klbs(wt)/h,klbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12465.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12465.0)
                elif units == 'MMlbs(wt)/h,MMlbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12465000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12465000.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'coke':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'ton(wt)/h,tons(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(24800.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(24800.0)
                elif units == 'lbs(wt)/h,lbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12.4)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12.4)
                elif units == 'klbs(wt)/h,klbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12400.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12400.0)
                elif units == 'MMlbs(wt)/h,MMlbs(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(12400000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(12400000.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'wood':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                elif units == 'MMBtuh,MMBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1000.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1000.0)
                elif units == 'ton(wt)/h,tons(wt)':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(15380.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(15380.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            elif fuel_type == 'other':
                if units == 'kBtuh,kBtu':
                    df['kBtuh Peak Demand'] = df['Peak Demand'] * Decimal(1.0)
                    df['kBtu Consumption'] = df['Consumption'] * Decimal(1.0)
                else:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='matching fuel units not found',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='matching fuel type not found',
                            comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel type, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            result = df.sort_index()
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='expected inputs not found',
                        comment='Meter %s failed on add_kBtu_kBtuh function, unexpected input data, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            result = None
        return result
    def __unicode__(self):
        return self.name
    def account_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(self.account.id,)), self.account.name)
    account_name_for_admin.allow_tags = True
    account_name_for_admin.short_description = 'Account'
    def connected_building_names_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
    connected_building_names_for_admin.allow_tags = True
    connected_building_names_for_admin.short_description = 'Connected Buildings'
    def connected_equipment_names_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
    connected_equipment_names_for_admin.allow_tags = True
    connected_equipment_names_for_admin.short_description = 'Connected Equipment'
    def utility_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_utility_change',args=(self.utility.id,)), self.utility.name)
    utility_name_for_admin.allow_tags = True
    utility_name_for_admin.short_description = 'Provider'
    def rate_schedule_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_rate_schedule_change',args=(self.rate_schedule.id,)), self.rate_schedule.name)
    rate_schedule_name_for_admin.allow_tags = True
    rate_schedule_name_for_admin.short_description = 'Rate Schedule'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Meter, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'notification',
                        subject = 'Meter created',
                        comment = 'This Meter was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
            
            s = Reader(name='READo',help_text='meter readings observed by local sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='READp',help_text='meter readings provided by remote source (e.g. utility company)')
            s.save()
            self.readers.add(s)
            s = Reader(name='READc',help_text='meter readings calculated by models')
            s.save()
            self.readers.add(s)
            
            b = BillingCycler(meter=self)
            b.save()
            mthr = Monther(meter=self,name='MNTHo',help_text='monthly values observed by local sensors')
            mthr.save()
            mthr = Monther(meter=self,name='MNTHp',help_text='monthly values provided by remote source (e.g. utility company)')
            mthr.save()
            mthr = Monther(meter=self,name='MNTHc',help_text='monthly values calculated by models')
            mthr.save()
            mthr = Monther(meter=self,name='BILLp',help_text='monthly values from utility bill')
            mthr.save()            
        super(Meter, self).save(*args, **kwargs)

class Utility(models.Model):
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    messages = models.ManyToManyField('Message')
    events = models.ManyToManyField('Event')
    
    #file-related attributes
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_utility, 
                    storage=S3BotoStorage(location='utility_files'),
                    help_text='link to utility logo file')

    #functions
    def rate_schedules_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_rate_schedule_change',args=(rs.id,)), rs.name) for rs in self.rate_schedule_set.all()])
    rate_schedules_for_admin.allow_tags = True
    rate_schedules_for_admin.short_description = 'Rates'
    def __unicode__(self):
        return self.name

class Rate_Schedule(models.Model):
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    utility = models.ForeignKey('Utility')
    messages = models.ManyToManyField('Message')
    events = models.ManyToManyField('Event')
    
    #file-related attributes
    rate_file = models.FileField(null=True, blank=True, upload_to=rate_file_path_rate_schedule, 
                    storage=S3BotoStorage(location='utility_files'),
                    help_text='link to rate schedule file')
    
    #functions
    def utility_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_utility_change',args=(self.utility.id,)), self.utility.name)
    utility_name_for_admin.allow_tags = True
    utility_name_for_admin.short_description = 'Provider'
    def __unicode__(self):
        return self.name
    def get_cost(self, time_series):
        cost = time_series * 2
        return cost
    
    #need to add attributes to capture rate schedule info
    #maybe abstract this one and allow creation of specific rate schedules as needed
    #would need to try to add generic functions that would exist on all subclasses                
                    
class Equipment(models.Model):
    objects = InheritanceManager() #used with django-model-utils; query all Equipment subclasses together
    
    #relationships
    messages = models.ManyToManyField('Message')
    meters = models.ManyToManyField('Meter')
    buildings = models.ManyToManyField('Building')
    floors = models.ManyToManyField('Floor')
    readers = models.ManyToManyField('Reader')
    events = models.ManyToManyField('Event')
    schedule = models.ForeignKey('Operating_Schedule')

    
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
    def update_readers(self):
        """No inputs.
        
        Loads data from observed and provided
        tracker files into Readers."""
        
        if self.observed_file_track:
            df = pd.read_csv(self.observed_file.url,
                             skiprows=self.observed_file_skiprows,
                             parse_dates=True,
                             index_col=self.observed_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.observed_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=1).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
        if self.provided_file_track:
            df = pd.read_csv(self.provided_file.url,
                             skiprows=self.provided_file_skiprows,
                             parse_dates=True,
                             index_col=self.provided_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.provided_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=2).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
    def __unicode__(self):
        return self.name
    def account_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(self.buildings.all()[0].account.id,)), self.buildings.all()[0].account.name) #assumes all equips attached to only one account
    account_name_for_admin.allow_tags = True
    account_name_for_admin.short_description = 'Account'
    def connected_buildings_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.buildings.all()])
    connected_buildings_for_admin.allow_tags = True
    connected_buildings_for_admin.short_description = 'Connected Buildings'
    def connected_floors_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_floor_change',args=(floor.id,)), floor.name) for floor in self.floors.all()])
    connected_floors_for_admin.allow_tags = True
    connected_floors_for_admin.short_description = 'Connected Floors'
    def connected_meters_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meters.all()])
    connected_meters_for_admin.allow_tags = True
    connected_meters_for_admin.short_description = 'Connected Meters'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Equipment, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'notification',
                        subject = 'Equipment created',
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
        
#    class Meta:
#        abstract = True
    
class RooftopUnit(Equipment):
    class Meta:
        verbose_name = 'Rooftop Unit'
    #relationships
    
    #nameplate data
    age = models.IntegerField(null=True, blank=True, 
                                  help_text='Rooftop Unit: age, yrs')
    make = models.CharField(blank=True, max_length=200, help_text='Rooftop Unit: manufacturer')
    model = models.CharField(blank=True, max_length=200, help_text='Rooftop Unit: model number')
    serial_number = models.CharField(blank=True, max_length=200, help_text='Rooftop Unit: serial number')
    nameplate_tons = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                   help_text='Rooftop Unit: nameplate cooling capacity, tons')
    nameplate_EER = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3,
                                  help_text='Rooftop Unit: nameplate cooling efficiency, (EER)')
    nameplate_MBH_in = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                     help_text='Rooftop Unit: nameplate natural gas heating input, MBH')
    nameplate_MBH_out = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                      help_text='Rooftop Unit: nameplate natural gas heating output, MBH')
    nameplate_ng_eta = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=3,
                                  help_text='Rooftop Unit: nameplate natural gas heating efficiency, ()')
    nameplate_V = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: nameplate voltage, V')
    nameplate_phase = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                 help_text='Rooftop Unit: nameplate phase, (1,3)')
    nameplate_pf = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                 help_text='Rooftop Unit: nameplate power factor, ()')
    nameplate_RFC = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                 help_text='Rooftop Unit: nameplate refrigerant charge, lbs')
    nameplate_c1_QTY = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 1 nameplate quantity, ()')
    nameplate_c1_RLA = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 1 nameplate current (RLA), A')
    nameplate_c1_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 1 nameplate phase, (1,3)')
    nameplate_c2_QTY = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 2 nameplate quantity, ()')
    nameplate_c2_RLA = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 2 nameplate current (RLA), A')
    nameplate_c2_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 2 nameplate phase, (1,3)')
    nameplate_c3_QTY = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 3 nameplate quantity, ()')
    nameplate_c3_RLA = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 3 nameplate current (RLA), A')
    nameplate_c3_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 3 nameplate phase, (1,3)')
    nameplate_c3_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: compressor 3 nameplate phase, (1,3)')
    nameplate_e1_QTY = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: evaporator fan 1 nameplate quantity, ()')
    nameplate_e1_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: evaporator fan 1 nameplate phase, (1,3)')
    nameplate_e1_FLA = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: evaporator fan 1 nameplate current (FLA), A')
    nameplate_e2_QTY = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: evaporator fan 2 nameplate quantity, ()')
    nameplate_e2_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: evaporator fan 2 nameplate phase, (1,3)')
    nameplate_e2_FLA = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: evaporator fan 2 nameplate current (FLA), A')
    nameplate_f1_QTY = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: condenser fan 1 nameplate quantity, ()')
    nameplate_f1_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: condenser fan 1 nameplate phase, (1,3)')
    nameplate_f1_FLA = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: condenser fan 1 nameplate current (FLA), A')
    nameplate_f2_QTY = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: condenser fan 2 nameplate quantity, ()')
    nameplate_f2_PH = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: condenser fan 2 nameplate phase, (1,3)')
    nameplate_f2_FLA = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                                help_text='Rooftop Unit: condenser fan 2 nameplate current (FLA), A')
    #constants
    dP_fan_max = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: max supply fan pressure gain, iwg')
    dP_fan_min = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: min supply fan pressure gain, iwg')
    SAF_max = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: max supply fan flow rate, CFM')
    SAF_min = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: min supply fan flow rate, CFM')
    speed_min = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: min VFD speed ratio {n}, ()',
                            default=Decimal(0.2))
    T_max = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: upper temperature bound, ' + u"\u00b0" + 'F',
                            default=Decimal(150))
    T_min = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: lower temperature bound, ' + u"\u00b0" + 'F',
                            default=Decimal(-50))
    #parameters
    d = ArrayField(blank=True, null=True, dbtype='decimal',
                            help_text='Rooftop Unit: VFD efficiency curve coefficients, [d0, d1, d2]')
    m = ArrayField(blank=True, null=True, dbtype='decimal',
                            help_text='Rooftop Unit: motor efficiency curve coefficients, [m0, m1, m2, m3]')
    f = ArrayField(blank=True, null=True, dbtype='decimal',
                            help_text='Rooftop Unit: fan curve coefficients, [f0, f1, f2]')
    e = ArrayField(blank=True, null=True, dbtype='decimal',
                            help_text='Rooftop Unit: fan efficiency curve coefficients, [e0, e1, e2]')
    #setpoint values
    SCOC = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: occupied cooling setpoint, ' + u"\u00b0" + 'F',
                            default=Decimal(72))
    SCUN = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: unoccupied cooling setpoint, ' + u"\u00b0" + 'F',
                            default=Decimal(80))
    SHOC = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: occupied heating setpoint, ' + u"\u00b0" + 'F',
                            default=Decimal(68))
    SHUN = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: unoccupied heating setpoint, ' + u"\u00b0" + 'F',
                            default=Decimal(60))
    SRFC = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3,
                            help_text='Rooftop Unit: fully charged refrigerant pressure, lbs')
    #functions
    def connected_buildings_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.buildings.all()])
    connected_buildings_for_admin.allow_tags = True
    connected_buildings_for_admin.short_description = 'Connected Buildings'
    def connected_floors_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_floor_change',args=(floor.id,)), floor.name) for floor in self.floors.all()])
    connected_floors_for_admin.allow_tags = True
    connected_floors_for_admin.short_description = 'Connected Floors'
    def connected_meters_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meters.all()])
    connected_meters_for_admin.allow_tags = True
    connected_meters_for_admin.short_description = 'Connected Meters'    
    def save(self, *args, **kwargs):
        if self.id is None:
            super(RooftopUnit, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'notification',
                        subject = 'Rooftop Unit created',
                        comment = 'This Rooftop Unit was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
            
            #----------------------------------------------------------------observed
            #states
            s = Reader(name='SADBo',help_text='Rooftop Unit: supply air dry bulb temperature (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SARHo',help_text='Rooftop Unit: supply air relative humidity (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SAFLo',help_text='Rooftop Unit: supply air flow rate (CFM) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SADPo',help_text='Rooftop Unit: supply air pressure (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='RADBo',help_text='Rooftop Unit: return air dry bulb temperature (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='RARHo',help_text='Rooftop Unit: return air relative humidity (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='RAFLo',help_text='Rooftop Unit: return air flow rate (CFM) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='RADPo',help_text='Rooftop Unit: return air pressure (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='OADBo',help_text='Rooftop Unit: outside air dry bulb temperature (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='OARHo',help_text='Rooftop Unit: outside air relative humidity (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='OAFLo',help_text='Rooftop Unit: outside air flow rate (CFM) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='OADPo',help_text='Rooftop Unit: outside air pressure (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='MADBo',help_text='Rooftop Unit: mixed air dry bulb temperature (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='MARHo',help_text='Rooftop Unit: mixed air relative humidity (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='MAFLo',help_text='Rooftop Unit: mixed air flow rate (CFM) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='MADPo',help_text='Rooftop Unit: mixed air pressure (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPDBo',help_text='Rooftop Unit: space dry bulb temperature (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPRHo',help_text='Rooftop Unit: space relative humidity (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPDPo',help_text='Rooftop Unit: space air pressure (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='FIDPo',help_text='Rooftop Unit: filter pressure drop (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='CCDPo',help_text='Rooftop Unit: cooling coil pressure drop (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SFDPo',help_text='Rooftop Unit: supply fan pressure gain (iwg) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SFEFo',help_text='Rooftop Unit: supply fan efficiency (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SMEFo',help_text='Rooftop Unit: supply fan motor efficiency (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SVFDo',help_text='Rooftop Unit: supply fan VFD efficiency (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='RFCHo',help_text='Rooftop Unit: refrigerant charge (lbs) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='TONSo',help_text='Rooftop Unit: delivered cooling (tons) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='BTUHo',help_text='Rooftop Unit: delivered heating (btu/h) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='CEERo',help_text='Rooftop Unit: cooling efficiency (EER) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='HEFFo',help_text='Rooftop Unit: heating efficiency (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='VFDNo',help_text='Rooftop Unit: VFD speed ratio {n} (0-1.0) observed by sensors')
            s.save()
            self.readers.add(s)

            #setpoint arrays
            s = Reader(name='SCOCo',help_text='Rooftop Unit: occupied cooling setpoints (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SCUNo',help_text='Rooftop Unit: unoccupied cooling setpoints (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SHOCo',help_text='Rooftop Unit: occupied heating setpoints (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SHUNo',help_text='Rooftop Unit: unoccupied heating setpoints (' + u"\u00b0" + 'F) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='SRFCo',help_text='Rooftop Unit: fully charged refrigerant pressures (lbs) observed by sensors')
            s.save()
            self.readers.add(s)

            #status
            s = Reader(name='STONo',help_text='Rooftop Unit: unit status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC1o',help_text='Rooftop Unit: compressor 1 status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC2o',help_text='Rooftop Unit: compressor 2 status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC3o',help_text='Rooftop Unit: compressor 3 status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STH1o',help_text='Rooftop Unit: heating 1 status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STH2o',help_text='Rooftop Unit: heating 2 status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STECo',help_text='Rooftop Unit: economizer status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STODo',help_text='Rooftop Unit: outdoor air damper status (% open) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STSFo',help_text='Rooftop Unit: supply fan status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STRFo',help_text='Rooftop Unit: return fan status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STF1o',help_text='Rooftop Unit: condenser fan 1 status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            s = Reader(name='STF2o',help_text='Rooftop Unit: condenser fan 2 status (1/0) observed by sensors')
            s.save()
            self.readers.add(s)
            #----------------------------------------------------------------provided
            #states
            s = Reader(name='SADBp',help_text='Rooftop Unit: supply air dry bulb temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SARHp',help_text='Rooftop Unit: supply air relative humidity (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SAFLp',help_text='Rooftop Unit: supply air flow rate (CFM) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SADPp',help_text='Rooftop Unit: supply air pressure (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='RADBp',help_text='Rooftop Unit: return air dry bulb temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='RARHp',help_text='Rooftop Unit: return air relative humidity (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='RAFLp',help_text='Rooftop Unit: return air flow rate (CFM) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='RADPp',help_text='Rooftop Unit: return air pressure (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='OADBp',help_text='Rooftop Unit: outside air dry bulb temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='OARHp',help_text='Rooftop Unit: outside air relative humidity (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='OAFLp',help_text='Rooftop Unit: outside air flow rate (CFM) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='OADPp',help_text='Rooftop Unit: outside air pressure (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='MADBp',help_text='Rooftop Unit: mixed air dry bulb temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='MARHp',help_text='Rooftop Unit: mixed air relative humidity (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='MAFLp',help_text='Rooftop Unit: mixed air flow rate (CFM) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='MADPp',help_text='Rooftop Unit: mixed air pressure (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPDBp',help_text='Rooftop Unit: space dry bulb temperature (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPRHp',help_text='Rooftop Unit: space relative humidity (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPDPp',help_text='Rooftop Unit: space air pressure (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='FIDPp',help_text='Rooftop Unit: filter pressure drop (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='CCDPp',help_text='Rooftop Unit: cooling coil pressure drop (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SFDPp',help_text='Rooftop Unit: supply fan pressure gain (iwg) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SFEFp',help_text='Rooftop Unit: supply fan efficiency (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SMEFp',help_text='Rooftop Unit: supply fan motor efficiency (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SVFDp',help_text='Rooftop Unit: supply fan VFD efficiency (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='RFCHp',help_text='Rooftop Unit: refrigerant charge (lbs) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='TONSp',help_text='Rooftop Unit: delivered cooling (tons) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='BTUHp',help_text='Rooftop Unit: delivered heating (btu/h) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='CEERp',help_text='Rooftop Unit: cooling efficiency (EER) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='HEFFp',help_text='Rooftop Unit: heating efficiency (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='VFDNp',help_text='Rooftop Unit: VFD speed ratio {n} (0-1.0) provided by remote source')
            s.save()
            self.readers.add(s)

            #setpoint arrays
            s = Reader(name='SCOCp',help_text='Rooftop Unit: occupied cooling setpoints (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SCUNp',help_text='Rooftop Unit: unoccupied cooling setpoints (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SHOCp',help_text='Rooftop Unit: occupied heating setpoints (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SHUNp',help_text='Rooftop Unit: unoccupied heating setpoints (' + u"\u00b0" + 'F) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='SRFCp',help_text='Rooftop Unit: fully charged refrigerant pressures (lbs) provided by remote source')
            s.save()
            self.readers.add(s)

            #status
            s = Reader(name='STONp',help_text='Rooftop Unit: unit status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC1p',help_text='Rooftop Unit: compressor 1 status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC2p',help_text='Rooftop Unit: compressor 2 status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC3p',help_text='Rooftop Unit: compressor 3 status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STH1p',help_text='Rooftop Unit: heating 1 status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STH2p',help_text='Rooftop Unit: heating 2 status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STECp',help_text='Rooftop Unit: economizer status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STODp',help_text='Rooftop Unit: outdoor air damper status (% open) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STSFp',help_text='Rooftop Unit: supply fan status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STRFp',help_text='Rooftop Unit: return fan status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STF1p',help_text='Rooftop Unit: condenser fan 1 status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            s = Reader(name='STF2p',help_text='Rooftop Unit: condenser fan 2 status (1/0) provided by remote source')
            s.save()
            self.readers.add(s)
            #----------------------------------------------------------------calculated
            #states
            s = Reader(name='SADBc',help_text='Rooftop Unit: supply air dry bulb temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SARHc',help_text='Rooftop Unit: supply air relative humidity (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SAFLc',help_text='Rooftop Unit: supply air flow rate (CFM) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SADPc',help_text='Rooftop Unit: supply air pressure (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='RADBc',help_text='Rooftop Unit: return air dry bulb temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='RARHc',help_text='Rooftop Unit: return air relative humidity (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='RAFLc',help_text='Rooftop Unit: return air flow rate (CFM) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='RADPc',help_text='Rooftop Unit: return air pressure (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='OADBc',help_text='Rooftop Unit: outside air dry bulb temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='OARHc',help_text='Rooftop Unit: outside air relative humidity (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='OAFLc',help_text='Rooftop Unit: outside air flow rate (CFM) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='OADPc',help_text='Rooftop Unit: outside air pressure (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='MADBc',help_text='Rooftop Unit: mixed air dry bulb temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='MARHc',help_text='Rooftop Unit: mixed air relative humidity (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='MAFLc',help_text='Rooftop Unit: mixed air flow rate (CFM) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='MADPc',help_text='Rooftop Unit: mixed air pressure (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPDBc',help_text='Rooftop Unit: space dry bulb temperature (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPRHc',help_text='Rooftop Unit: space relative humidity (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SPDPc',help_text='Rooftop Unit: space air pressure (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='FIDPc',help_text='Rooftop Unit: filter pressure drop (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='CCDPc',help_text='Rooftop Unit: cooling coil pressure drop (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SFDPc',help_text='Rooftop Unit: supply fan pressure gain (iwg) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SFEFc',help_text='Rooftop Unit: supply fan efficiency (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SMEFc',help_text='Rooftop Unit: supply fan motor efficiency (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SVFDc',help_text='Rooftop Unit: supply fan VFD efficiency (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='RFCHc',help_text='Rooftop Unit: refrigerant charge (lbs) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='TONSc',help_text='Rooftop Unit: delivered cooling (tons) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='BTUHc',help_text='Rooftop Unit: delivered heating (btu/h) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='CEERc',help_text='Rooftop Unit: cooling efficiency (EER) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='HEFFc',help_text='Rooftop Unit: heating efficiency (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='VFDNc',help_text='Rooftop Unit: VFD speed ratio {n} (0-1.0) calculated by models')
            s.save()
            self.readers.add(s)

            #setpoint arrays
            s = Reader(name='SCOCc',help_text='Rooftop Unit: occupied cooling setpoints (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SCUNc',help_text='Rooftop Unit: unoccupied cooling setpoints (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SHOCc',help_text='Rooftop Unit: occupied heating setpoints (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SHUNc',help_text='Rooftop Unit: unoccupied heating setpoints (' + u"\u00b0" + 'F) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='SRFCc',help_text='Rooftop Unit: fully charged refrigerant pressures (lbs) calculated by models')
            s.save()
            self.readers.add(s)

            #status
            s = Reader(name='STONc',help_text='Rooftop Unit: unit status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC1c',help_text='Rooftop Unit: compressor 1 status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC2c',help_text='Rooftop Unit: compressor 2 status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STC3c',help_text='Rooftop Unit: compressor 3 status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STH1c',help_text='Rooftop Unit: heating 1 status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STH2c',help_text='Rooftop Unit: heating 2 status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STECc',help_text='Rooftop Unit: economizer status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STODc',help_text='Rooftop Unit: outdoor air damper status (% open) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STSFc',help_text='Rooftop Unit: supply fan status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STRFc',help_text='Rooftop Unit: return fan status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STF1c',help_text='Rooftop Unit: condenser fan 1 status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            s = Reader(name='STF2c',help_text='Rooftop Unit: condenser fan 2 status (1/0) calculated by models')
            s.save()
            self.readers.add(s)
            
        super(RooftopUnit, self).save(*args, **kwargs)

class TestEquip(models.Model):
    objects = InheritanceManager() #used with django-model-utils; query all Equipment subclasses together
    
    #relationships
    readers = models.ManyToManyField('Reader')

    
    #administrative info
    name = models.CharField(blank=True, max_length=200)
    observed_file = models.FileField(null=True, blank=True, upload_to='testmodels', 
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
    #functions
    def update_readers(self):
        if self.observed_file_track:
            df = pd.read_csv(self.observed_file.url,
                             skiprows=self.observed_file_skiprows,
                             parse_dates=True,
                             index_col=self.observed_file_column_for_indexing)
            df.index = df.index - timedelta(hours=float(self.observed_file_GMT_offset))
            df.index = df.index.tz_localize('UTC')
            column_headers = df.columns
            df.columns = range(0,len(df.columns))
            for r in self.readers.filter(source=1).filter(active=True):
                r.load_reader_time_series(df[r.column_index])
                r.column_header = column_headers[r.column_index]
                r.save()
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.id is None:
            super(TestEquip, self).save(*args, **kwargs)
            s = Reader(name='kW',help_text='electricity: power (kW) observed by local sensors')
            s.save()
            self.readers.add(s)
            
        super(TestEquip, self).save(*args, **kwargs)

    
class BuildingSpeakError(Exception):
    """Base exception class for BuildingSpeak"""
    pass
class BuildingSpeakWarning(Exception):
    """Base warning class for BuildingSpeak"""
    pass

#    try:
#        f = open(arg, 'r')
#    except IOError:
#        print 'cannot open', arg
#    else:
#        print arg, 'has', len(f.readlines()), 'lines'
#        f.close()
#dra: use else clause to execute things associated with the try clause
#can have "except (RuntimeError, TypeError, NameError):" to catch multiple errors
#use "except MyError as e:" and then can access error attributes in except code





#Field types 
# AutoField
# BigIntegerField
# BooleanField
# CharField
# CommaSeparatedIntegerField
# DateField
# DateTimeField
# DecimalField
# EmailField
# FileField
# FilePathField
# FloatField
# ImageField
# IntegerField
# IPAddressField
# GenericIPAddressField
# NullBooleanField
# PositiveIntegerField
# PositiveSmallIntegerField
# SlugField
# SmallIntegerField
# TextField
# TimeField
# URLField
