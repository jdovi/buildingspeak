#import dbarray
import pandas as pd
import numpy as np
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
from models_monthlies import Monther

class Meter(models.Model):
    """Model for any fuel or water
    consumption measuring device.
    Supports all fuel types and units
    supported by ES Portfolio Manager.
    Accepts photo and nameplate image
    files and bill data text file."""
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
    serves = models.CharField(blank=True, max_length=200,
                              help_text = 'short description of buildings or areas served')
    units = models.CharField(blank=True, max_length=200, help_text='units of measurement (rate,amount)',
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
    weather_station = models.ForeignKey('WeatherStation')
    utility = models.ForeignKey('Utility')
    rate_schedule = models.ForeignKey('RateSchedule')
    account = models.ForeignKey('Account')
    messages = models.ManyToManyField('Message')
    readers = models.ManyToManyField('Reader')
    schedules = models.ManyToManyField('OperatingSchedule')
    
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
    bill_data_file = models.FileField(null=True, blank=True, upload_to=bill_data_file_path_meter, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to text file containing monthly bill data; must be formatted correctly')
    bill_data_import = models.BooleanField(blank=True, default=False,
                    help_text='import bill data?')

    #single value atrributes
    make = models.CharField(blank=True, max_length=200, help_text='manufacturer of meter')
    model = models.CharField(blank=True, max_length=200, help_text='model number of meter')
    serial_number = models.CharField(blank=True, max_length=200, help_text='serial number of meter')
    utility_account_number = models.CharField(blank=True, max_length=200, help_text='account number with provider')
    utility_meter_number = models.CharField(blank=True, max_length=200, help_text='provider''s meter number')
    
    #functions
    def get_all_events(self, reverse_boolean):
        return sorted(self.messages.filter(message_type='Event'), key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_alerts(self, reverse_boolean):
        return sorted(self.messages.filter(message_type='Alert'), key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_messages(self, reverse_boolean):
        return sorted(self.messages.all(), key=attrgetter('when'), reverse=reverse_boolean)
    def update_monthers(self):
        """No inputs.
        
        Updates Meter's Reader-based Monthers.
        NOT WRITTEN YET."""
        pass
    def get_all_savings(self, df):
        """function(df)
        
        Given dataframe with
        monthly index, returns
        dataframe with new
        columns for the sums
        from all attached
        EfficiencyMeasures for
        consumption, demand,
        their deltas, and
        cost savings.
        
        WARNING: only adds 
        measures with same
        utility type and
        units as Meter!"""
        try:
            df['Consumption Savings_sum'] = Decimal(0.0)
            df['Peak Demand Savings_sum'] = Decimal(0.0)
            df['Consumption Savings_sum_delta'] = Decimal(0.0)
            df['Peak Demand Savings_sum_delta'] = Decimal(0.0)
            df['Cost Savings_sum'] = Decimal(0.0)
            
            if len(self.emmeterapportionment_set.all()) > 0:
                for emma in self.emmeterapportionment_set.all():
                    if ( (emma.efficiency_measure.utility_type == self.utility_type) and
                         (emma.efficiency_measure.units == self.units)  ):
                        df = emma.efficiency_measure.get_savings_df(df=df)
                        df['Consumption Savings_sum'] = df['Consumption Savings_sum'] + df['Consumption Savings']
                        df['Peak Demand Savings_sum'] = df['Peak Demand Savings_sum'] + df['Peak Demand Savings']
                        df['Consumption Savings_sum_delta'] = df['Consumption Savings_sum'] + df['Consumption Savings']*emma.efficiency_measure.percent_uncertainty
                        df['Peak Demand Savings_sum_delta'] = df['Peak Demand Savings_sum'] + df['Peak Demand Savings']*emma.efficiency_measure.percent_uncertainty
                        df['Cost Savings_sum'] = df['Cost Savings_sum'] + df['Cost Savings']
                    df = df.drop(['Cost Savings', 'Peak Demand Savings', 'Consumption Savings'], axis = 1)
            df.rename(columns={'Cost Savings_sum': 'Cost (esave)',
                               'Peak Demand Savings_sum': 'Peak Demand (esave)',
                               'Consumption Savings_sum': 'Consumption (esave)',
                               'Peak Demand Savings_sum_delta': 'Peak Demand (esave delta)',
                               'Consumption Savings_sum_delta': 'Consumption (esave delta)'}, inplace = True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='EfficiencyMeasure %s get_savings_df failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    def get_bill_data_period_dataframe(self, first_month='', last_month=''):
        """function(first_month,last_month)
            (optional inputs)
            
        Takes mm/yyyy strings and returns
        a dataframe of bill data for that
        range."""
        mdf = self.monther_set.get(name='BILLx').get_monther_period_dataframe(first_month=first_month, last_month=last_month)
        if mdf is None:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='Meter %s get_bill_data_period_dataframe function found no bill data, aborting and returning None.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return mdf
    def get_dataframe_as_table(self, df, columnlist):
        """function(df,columnlist)
        
        Takes dataframe and a list
        of column names to include
        in the output.  Index put
        in first column as Month."""
        r = []
        try:
            r.append(columnlist)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='Meter %s received non-list during get_dataframe_as_table function, aborting and returning empty list.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df_dec = df
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Retrieve data failed.',
                            comment='Meter %s failed to load dataframe during get_dataframe_as_table function, aborting and returning empty list.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            else:
                if (df_dec is None) or (len(df_dec)==0):
                    m = Message(when=timezone.now(),
                                message_type='Code Warning',
                                subject='No data.',
                                comment='Meter %s found no bill data to load during get_dataframe_as_table function, aborting and returning empty list.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                else:
                    try:
                        if 'Start Date' in df_dec.columns and 'End Date' in df_dec.columns:
                            df_dec_numbers = df_dec.columns.drop(['Start Date','End Date'])
                        elif 'Start Date' in df_dec.columns:
                            df_dec_numbers = df_dec.columns.drop(['Start Date'])
                        elif 'End Date' in df_dec.columns:
                            df_dec_numbers = df_dec.columns.drop(['End Date'])
                        else:
                            df_dec_numbers = df_dec.columns
                        df = df_dec[df_dec_numbers].applymap(lambda x: float(x)) #convert Decimal to float
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Data manipulation failed.',
                                    comment='Meter %s failed to convert decimals to floats during get_dataframe_as_table function, aborting and returning empty list.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                    else:
                        if not(min([x in df.columns for x in columnlist[1:]])):
                            m = Message(when=timezone.now(),
                                        message_type='Code Error',
                                        subject='Function received bad arguments.',
                                        comment='Meter %s received request for columns that are not in dataframe during get_dataframe_as_table function, aborting and returning empty list.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                        else:
                            try:
                                df = df.sort_index()
                                for i in range(0,len(df)):
                                    r_1 = [str(df.index[i])]
                                    r_j = []
                                    for j in columnlist[1:]:
                                        r_j.append(df[j][i])
                                    r_1.extend(r_j)
                                    r.append(r_1)
                            except:
                                m = Message(when=timezone.now(),
                                            message_type='Code Error',
                                            subject='Unable to create table.',
                                            comment='Meter %s failed to create table during get_dataframe_as_table function, aborting and returning empty list.' % self.id)
                                m.save()
                                self.messages.add(m)
                                print m
        return r
    def upload_bill_data(self, file_location=0):
        """Input:
            [file_location]
                (default: MeterInstance.bill_data_url)
        
        Reads Bill Data File and loads into
        Meter's BILLx Monther, respecting any
        pre-existing data unless Overwrite
        column in Bill Data File indicates
        otherwise."""
        if not(file_location): file_location = self.bill_data_file.url
        success = success_a = success_b = None
        try:
            readbd = pd.read_csv(file_location,
                                 skiprows=0,
                                 usecols=['Overwrite', 'Start Date', 'End Date', 'Billing Demand',
                                          'Peak Demand', 'Consumption', 'Cost'],
                                 dtype={'Billing Demand': np.float, 'Peak Demand': np.float,
                                        'Consumption': np.float, 'Cost': np.float})
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='File not found.',
                        comment='Meter %s failed on upload_bill_data function when attempting to read Bill Data File.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = False
        else:
            try:
                if (('Start Date' in readbd.columns) and ('End Date' in readbd.columns) and
                    ('Billing Demand' in readbd.columns) and ('Peak Demand' in readbd.columns) and
                    ('Consumption' in readbd.columns) and ('Cost' in readbd.columns) and
                    (len(readbd)>0) ):
                    readbd['Start Date'] = readbd['Start Date'].apply(pd.to_datetime) + timedelta(hours=11,minutes=11,seconds=11) #add hours/mins/secs to avoid crossing day boundary when adjusting timezones
                    readbd['End Date'] = readbd['End Date'].apply(pd.to_datetime) + timedelta(hours=11,minutes=11,seconds=11) #add hours/mins/secs to avoid crossing day boundary when adjusting timezones
                    readbd['Start Date'] = readbd['Start Date'].apply(UTC.localize)
                    readbd['End Date'] = readbd['End Date'].apply(UTC.localize)
                    readbd['Billing Demand'] = readbd['Billing Demand'].apply(Decimal)
                    readbd['Peak Demand'] = readbd['Peak Demand'].apply(Decimal)
                    readbd['Consumption'] = readbd['Consumption'].apply(Decimal)
                    readbd['Cost'] = readbd['Cost'].apply(Decimal)
                    if 'Overwrite' not in readbd.columns:
                        readbd['Overwrite'] = 0
                    else:
                        readbd['Overwrite'] = readbd['Overwrite'].apply(int)
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Model update failed.',
                            comment='Meter %s upload_bill_data function failed to pre-process incoming data, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = False
            else:
                try:
                    t = [self.assign_period_datetime(dates=[readbd['Start Date'][i],
                                                            readbd['End Date'][i]]) for i in range(0,len(readbd))]
                    if None in t: raise TypeError
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Model update failed.',
                                comment='Meter %s upload_bill_data function failed at assign_period_datetime, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    success = False
                else:
                    try:
                        readbd.index = pd.PeriodIndex(t, freq='M')
                        readbd = readbd.sort_index()
                        
                        #check if incoming data is self consistent in the Start(i)=End(i-1)+1
                        contiguous_check = (readbd['End Date'].shift(1) + timedelta(days=1)) == readbd['Start Date']
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Model update failed.',
                                    comment='Meter %s, upload_bill_data unable to check contiguity, function aborted.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                        success = False
                    else:
                        if False in contiguous_check[1:].values: #1st is always False due to shift, but if other False then abort
                            m = Message(when=timezone.now(),
                                        message_type='Code Error',
                                        subject='Function received bad arguments.',
                                        comment='Meter %s, upload_bill_data given non-contiguous data, function aborted.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                            success = False
                        else:
                            try:
                                readbd['Exists'] = readbd.index
                                storedbd = self.monther_set.get(name='BILLx').get_monther_period_dataframe()
                                if storedbd is None or len(storedbd)<1:
                                    readbd['Exists'] = 0
                                else:
                                    readbd['Exists'] = readbd['Exists'].apply(lambda lamvar: lamvar in storedbd.index)
                                
                                #ignore data that Exists but not(Overwrite)
                                #load data that not(Exists)
                                readbd_a = readbd[readbd['Exists']==0]
                                if len(readbd_a)>0:
                                    readbd_a.rename(columns={'Billing Demand': 'Billing Demand (act)',
                                                              'Peak Demand': 'Peak Demand (act)',
                                                              'Consumption': 'Consumption (act)',
                                                              'Cost': 'Cost (act)'}, inplace = True)
                                    readbd_a = self.monther_set.get(name='BILLx').create_calculated_columns(readbd_a)
                                    success_a = self.monther_set.get(name='BILLx').load_monther_period_dataframe(readbd_a)
                                    if not success_a: raise TypeError
                            except:
                                m = Message(when=timezone.now(),
                                            message_type='Code Error',
                                            subject='Model update failed.',
                                            comment='Meter %s upload_bill_data failed to load new data, function aborted.' % self.id)
                                m.save()
                                self.messages.add(m)
                                print m
                                success_a = False
                            else:
                                try:
                                    #retrieve and overwrite data that Exists and Overwrite
                                    readbd_b = readbd[(readbd['Exists']==1) & (readbd['Overwrite']==1)]
                                    if len(readbd_b)>0:
                                        for i in range(0,len(readbd_b)):
                                            try:
                                                month_i = None #setting here to avoid error in Except block
                                                month_i = readbd_b.index[i]
                                                per_date = UTC.localize(month_i.to_timestamp() + timedelta(days=10,hours=11,minutes=11,seconds=11))
                                                mlg = Monthling.objects.filter(monther=self.monther_set.get(name='BILLx')).get(when=per_date)
                                                if mlg is None: raise TypeError
                                                mlg.__setattr__('start_date',readbd_b['Start Date'][i])
                                                mlg.__setattr__('end_date',readbd_b['End Date'][i])
                                                mlg.__setattr__('act_billing_demand',readbd_b['Billing Demand'][i])
                                                mlg.__setattr__('act_peak_demand',readbd_b['Peak Demand'][i])
                                                mlg.__setattr__('act_consumption',readbd_b['Consumption'][i])
                                                mlg.__setattr__('act_cost',readbd_b['Cost'][i])
                                                mlg.flush_calculated_data()
                                                mlg.save()
                                                month_i = None #resetting to avoid carrying over incorrectly
                                                success_b = True #set True if at least one mlg is loaded
                                            except:
                                                m = Message(when=timezone.now(),
                                                            message_type='Code Error',
                                                            subject='Model update failed.',
                                                            comment='Meter %s upload_bill_data failed to overwrite existing month %s, function aborted.' % (self.id, str(month_i)))
                                                m.save()
                                                self.messages.add(m)
                                                print m
                                except:
                                    m = Message(when=timezone.now(),
                                                message_type='Code Error',
                                                subject='Model update failed.',
                                                comment='Meter %s upload_bill_data failed to overwrite existing data, function aborted.' % self.id)
                                    m.save()
                                    self.messages.add(m)
                                    print m
                                    success_b = False
        return max(success, success_a, success_b)

    def bill_data_calc_kbtu(self, df):
        """function(df)
        
        Computes kBtu and kBtuh to
        go with Consumption and
        Peak Demand columns for
        all groups (base, exp, etc.)
        of Meter's BILLx Monther."""
        try:
            df.rename(columns={'Consumption (act)': 'Consumption',
                               'Peak Demand (act)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (act)','kBtuh Peak Demand (act)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (act)',
                               'Peak Demand': 'Peak Demand (act)',
                               'kBtu Consumption': 'kBtu Consumption (act)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (act)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (act)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m

        try:
            df.rename(columns={'Consumption (asave)': 'Consumption',
                               'Peak Demand (asave)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (asave)','kBtuh Peak Demand (asave)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (asave)',
                               'Peak Demand': 'Peak Demand (asave)',
                               'kBtu Consumption': 'kBtu Consumption (asave)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (asave)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (asave)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m

        try:
            df.rename(columns={'Consumption (base delta)': 'Consumption',
                               'Peak Demand (base delta)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (base delta)','kBtuh Peak Demand (base delta)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (base delta)',
                               'Peak Demand': 'Peak Demand (base delta)',
                               'kBtu Consumption': 'kBtu Consumption (base delta)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (base delta)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (base delta)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m

        try:
            df.rename(columns={'Consumption (base)': 'Consumption',
                               'Peak Demand (base)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (base)','kBtuh Peak Demand (base)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (base)',
                               'Peak Demand': 'Peak Demand (base)',
                               'kBtu Consumption': 'kBtu Consumption (base)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (base)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (base)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m

        try:
            df.rename(columns={'Consumption (esave delta)': 'Consumption',
                               'Peak Demand (esave delta)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (esave delta)','kBtuh Peak Demand (esave delta)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (esave delta)',
                               'Peak Demand': 'Peak Demand (esave delta)',
                               'kBtu Consumption': 'kBtu Consumption (esave delta)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (esave delta)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (esave delta)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m

        try:
            df.rename(columns={'Consumption (esave)': 'Consumption',
                               'Peak Demand (esave)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (esave)','kBtuh Peak Demand (esave)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (esave)',
                               'Peak Demand': 'Peak Demand (esave)',
                               'kBtu Consumption': 'kBtu Consumption (esave)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (esave)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (esave)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m

        try:
            df.rename(columns={'Consumption (exp delta)': 'Consumption',
                               'Peak Demand (exp delta)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (exp delta)','kBtuh Peak Demand (exp delta)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (exp delta)',
                               'Peak Demand': 'Peak Demand (exp delta)',
                               'kBtu Consumption': 'kBtu Consumption (exp delta)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (exp delta)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (exp delta)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m

        try:
            df.rename(columns={'Consumption (exp)': 'Consumption',
                               'Peak Demand (exp)': 'Peak Demand'}, inplace=True)
            df = df.drop(['kBtu Consumption (exp)','kBtuh Peak Demand (exp)'], axis=1)
            result = self.add_kBtu_kBtuh(df, self.utility_type, self.units)
            if result is not None: df = result
            df.rename(columns={'Consumption': 'Consumption (exp)',
                               'Peak Demand': 'Peak Demand (exp)',
                               'kBtu Consumption': 'kBtu Consumption (exp)',
                               'kBtuh Peak Demand': 'kBtuh Peak Demand (exp)'}, inplace=True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_kbtu failed on (exp)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            
        return df

    def bill_data_calc_dd(self, df):
        """function(df)
        
        Computes degree days based
        on meter models attached
        to Meter's BILLx Monther."""
        try:
            if self.monther_set.get(name='BILLx').consumption_model is None:
                raise ValueError
            elif self.monther_set.get(name='BILLx').consumption_model.Tccp is None:
                raise ValueError
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Missing data.',
                    comment='Meter %s missing MeterConsumptionModel or its Tccp on bill_data_calc_dd, unable to calculate CDD (consumption).' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df = self.weather_station.get_CDD_df(df, self.monther_set.get(name='BILLx').consumption_model.Tccp)
                df = df.drop(['CDD (consumption)'], axis = 1)
                df.rename(columns={'CDD': 'CDD (consumption)'}, inplace = True)
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_dd unable to calculate CDD (consumption) and rename column.' % self.id)
                m.save()
                self.messages.add(m)
                print m
        
        try:
            if self.monther_set.get(name='BILLx').consumption_model is None:
                raise ValueError
            elif self.monther_set.get(name='BILLx').consumption_model.Thcp is None:
                raise ValueError
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Missing data.',
                    comment='Meter %s missing MeterConsumptionModel or its Thcp on bill_data_calc_dd, unable to calculate HDD (consumption).' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df = self.weather_station.get_HDD_df(df, self.monther_set.get(name='BILLx').consumption_model.Thcp)
                df = df.drop(['HDD (consumption)'], axis = 1)
                df.rename(columns={'HDD': 'HDD (consumption)'}, inplace = True)
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_dd unable to calculate HDD (consumption) and rename column.' % self.id)
                m.save()
                self.messages.add(m)
                print m

        try:
            if self.monther_set.get(name='BILLx').peak_demand_model is None:
                raise ValueError
            elif self.monther_set.get(name='BILLx').peak_demand_model.Tccp is None:
                raise ValueError
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Missing data.',
                    comment='Meter %s missing MeterPeakDemandModel or its Tccp on bill_data_calc_dd, unable to calculate CDD (peak demand).' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df = self.weather_station.get_CDD_df(df, self.monther_set.get(name='BILLx').peak_demand_model.Tccp)
                df = df.drop(['CDD (peak demand)'], axis = 1)
                df.rename(columns={'CDD': 'CDD (peak demand)'}, inplace = True)
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_dd unable to calculate CDD (peak demand) and rename column.' % self.id)
                m.save()
                self.messages.add(m)
                print m
        
        try:
            if self.monther_set.get(name='BILLx').peak_demand_model is None:
                raise ValueError
            elif self.monther_set.get(name='BILLx').peak_demand_model.Thcp is None:
                raise ValueError
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Missing data.',
                    comment='Meter %s missing MeterPeakDemandModel or its Thcp on bill_data_calc_dd, unable to calculate HDD (peak demand).' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df = self.weather_station.get_HDD_df(df, self.monther_set.get(name='BILLx').peak_demand_model.Thcp)
                df = df.drop(['HDD (peak demand)'], axis = 1)
                df.rename(columns={'HDD': 'HDD (peak demand)'}, inplace = True)
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_dd unable to calculate HDD (peak demand) and rename column.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                
        return df

    def bill_data_calc_baseline(self, df):
        """function(df)
        
        Computes (base) and (base
        delta) from meter models
        attached to Meter's BILLx
        Monther."""
        try:
            check = (self.monther_set.get(name='BILLx').peak_demand_model is not None)
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Warning',
                    subject='Missing data.',
                    comment='Meter %s missing MeterPeakDemandModel on bill_data_calc_baseline, unable to calculate Peak Demand (base, base delta).' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            if check:
                try:
                    predicted,stderror,lower_bound,upper_bound = self.monther_set.get(name='BILLx').peak_demand_model.current_model_predict_df(df=df)
                    df['Peak Demand (base)'] = predicted
                    df['Peak Demand (base delta)'] = predicted - lower_bound
                except:
                    m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='Meter %s bill_data_calc_baseline unable to calculate Peak Demand (base, base delta).' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                
        try:
            check = (self.monther_set.get(name='BILLx').consumption_model is not None)
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Warning',
                    subject='Missing data.',
                    comment='Meter %s missing MeterConsumptionModel on bill_data_calc_baseline, unable to calculate Consumption (base, base delta).' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            if check:
                try:
                    predicted,stderror,lower_bound,upper_bound = self.monther_set.get(name='BILLx').consumption_model.current_model_predict_df(df=df)
                    df['Consumption (base)'] = predicted
                    df['Consumption (base delta)'] = predicted - lower_bound
                except:
                    m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='Meter %s bill_data_calc_baseline unable to calculate Consumption (base, base delta).' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
        df[['Consumption (base)','Consumption (base delta)','Peak Demand (base)','Peak Demand (base delta)']] = df[['Consumption (base)','Consumption (base delta)','Peak Demand (base)','Peak Demand (base delta)']].applymap(Decimal)
        return df

    def bill_data_calc_savings(self, df):
        """function(df)
        
        Computes savings (esave)
        from efficiency measures
        attached to Meter and
        stores on BILLx Monther."""
        try:
            df = df.drop(['Cost (esave)','Peak Demand (esave)','Consumption (esave)',
                          'Peak Demand (esave delta)','Consumption (esave delta)'], axis = 1)
            df = self.get_all_savings(df=df)
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Warning',
                    subject='Calculation failed.',
                    comment='Meter %s bill_data_calc_savings unable to calculate Consumption and Peak Demand (esave).' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
        
    def bill_data_calc_dependents(self, df):
        """function(df)
        
        Computes (asave), (exp),
        and (exp delta) values
        of BILLx Monther. Needs
        (base), (esave), and
        (act) to compute."""
        try:
            df['Peak Demand (exp)'] = df['Peak Demand (base)'] - df['Peak Demand (esave)']
            df['Consumption (exp)'] = df['Consumption (base)'] - df['Consumption (esave)']
            df['Peak Demand (asave)'] = df['Peak Demand (base)'] - df['Peak Demand (act)']
            df['Consumption (asave)'] = df['Consumption (base)'] - df['Consumption (act)']
            df['Peak Demand (exp delta)'] = df['Peak Demand (base delta)'] - df['Peak Demand (esave delta)']
            df['Consumption (exp delta)'] = df['Consumption (base delta)'] - df['Consumption (esave delta)']
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Warning',
                    subject='Calculation failed.',
                    comment='Meter %s bill_data_calc_dependents unable to calculate (exp)s, (asave)s, and (exp delta)s.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df

    def bill_data_calc_costs(self, df):
        """function(df)
        
        Computes costs for BILLx
        Monther. Needs all
        Consumptions and Demands
        to compute."""
        try:
            check = (self.rate_schedule is None)
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Warning',
                    subject='Missing data.',
                    comment='Meter %s bill_data_calc_costs unable to retrieve rate schedule.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df.rename(columns={'Consumption (base)': 'Consumption',
                                   'Peak Demand (base)': 'Peak Demand'},inplace=True)
                df['Cost (base)'] = self.rate_schedule.as_child().get_cost_df(df=df)['Calculated Cost']
                df.rename(columns={'Consumption': 'Consumption (base)',
                                   'Peak Demand': 'Peak Demand (base)'},inplace=True)
                df.rename(columns={'Consumption (exp)': 'Consumption',
                                   'Peak Demand (exp)': 'Peak Demand'},inplace=True)
                df['Cost (exp)'] = self.rate_schedule.as_child().get_cost_df(df=df)['Calculated Cost']
                df.rename(columns={'Consumption': 'Consumption (exp)',
                                   'Peak Demand': 'Peak Demand (exp)'},inplace=True)
                df['Cost (esave)'] = df['Cost (base)'] - df['Cost (exp)']
                df['Cost (asave)'] = df['Cost (base)'] - df['Cost (act)']
                
                df['Consumption'] = df['Consumption (base)'] - df['Consumption (base delta)']
                df['Peak Demand'] = df['Peak Demand (base)'] - df['Peak Demand (base delta)']
                df['Cost (base delta)'] = (df['Cost (base)'] -
                                            self.rate_schedule.as_child().get_cost_df(df=df)['Calculated Cost'])
                                            
                df['Consumption'] = df['Consumption (esave)'] - df['Consumption (esave delta)']
                df['Peak Demand'] = df['Peak Demand (esave)'] - df['Peak Demand (esave delta)']
                df['Cost (esave delta)'] = (df['Cost (esave)'] -
                                            self.rate_schedule.as_child().get_cost_df(df=df)['Calculated Cost'])
    
                df = df.drop(['Consumption', 'Peak Demand'], axis = 1)
                
                df['Cost (exp delta)'] = df['Cost (base delta)'] - df['Cost (esave delta)']
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Warning',
                        subject='Calculation failed.',
                        comment='Meter %s bill_data_calc_costs unable to calculate costs.' % self.id)
                m.save()
                self.messages.add(m)
                print m
        return df
        
    def assign_period_datetime(self, time_series=[], dates=[]):
        """Inputs:
            time_series or
            dates (list of start/end
                    pandas Timestamps)
            
        Returns datetime of first day of
        most frequently occurring month in
        a given time series spanning 25-35
        days to use as basis for Period."""
        
        #raise error if empty inputs
        try:
            #pandas 0.10 to 0.11 changed use of Datetimes and Timedeltas
            #conversion of Timestamp to Datetime was needed because
            #cannot seem to add Timedelta to Timestamp like you can add
            #Timedelta to Datetime
            dates[0] = datetime(year=dates[0].year, month=dates[0].month,
                                day=dates[0].day, hour=dates[0].hour)
            dates[1] = datetime(year=dates[1].year, month=dates[1].month,
                                day=dates[1].day, hour=dates[1].hour)
            (len(time_series)==0 and len(dates)<>2) or type(dates[0])<>datetime or type(dates[1])<>datetime
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='Unexpected inputs passed to assign_period_datetime function on meter %s.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            answer = None
        else:
            if (len(time_series)==0 and len(dates)<>2) or type(dates[0])<>datetime or type(dates[1])<>datetime:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Function received bad arguments.',
                            comment='Unexpected inputs passed to assign_period_datetime function on meter %s.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                answer = None
            else:
                try:
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
                                    subject='Function received bad arguments.',
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
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Calculation failed.',
                                comment='Meter %s failed at assign_period_datetime, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    answer = None
        return answer
    
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
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
                                subject='Matching fuel units not found.',
                                comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel units, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Matching fuel type not found.',
                            comment='Meter %s failed on add_kBtu_kBtuh function, unable to find matching fuel type, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            result = df.sort_index()
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
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
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_rateschedule_change',args=(self.rate_schedule.id,)), self.rate_schedule.name)
    rate_schedule_name_for_admin.allow_tags = True
    rate_schedule_name_for_admin.short_description = 'Rate Schedule'
    def weather_station_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_weatherstation_change',args=(self.weather_station.id,)), self.weather_station.name)
    weather_station_name_for_admin.allow_tags = True
    weather_station_name_for_admin.short_description = 'Weather Station'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Meter, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'Model Info',
                        subject = 'Model created.',
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
            
            mthr = Monther(meter=self,name='MNTHo',help_text='monthly values observed by local sensors')
            mthr.save()
            mthr = Monther(meter=self,name='MNTHp',help_text='monthly values provided by remote source (e.g. utility company)')
            mthr.save()
            mthr = Monther(meter=self,name='MNTHc',help_text='monthly values calculated by models')
            mthr.save()
            mthr = Monther(meter=self,name='BILLx',help_text='monthly values from utility bill')
            mthr.save()
        if self.bill_data_import:
            super(Meter, self).save(*args, **kwargs)
            self.update_bill_data()
        super(Meter, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'
