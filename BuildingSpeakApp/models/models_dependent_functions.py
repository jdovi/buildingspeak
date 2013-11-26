#import dbarray
import math
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
from django.core.files.base import ContentFile
from django.db.models.loading import get_model
from django.db.models import Model
from django.db.models import Q


from models_Message import Message
from models_Account import Account
from models_Building import Building, BuildingMeterApportionment
from models_EfficiencyMeasure import EfficiencyMeasure, EMMeterApportionment, EMEquipmentApportionment
from models_Equipment import Equipment
from models_Space import Space, SpaceMeterApportionment
from models_Meter import Meter
from models_MeterModels import MeterConsumptionModel, MeterPeakDemandModel
from models_RateSchedules import RateSchedule, KnowsChild
from models_Reader_ing import Reader
from models_RooftopUnit import RooftopUnit
from models_schedules import UnitSchedule, OperatingSchedule
from models_Utility import Utility
from models_WeatherStation import WeatherStation



def nan2zero(x):
    y = x
    if math.isnan(x): y = Decimal(0)
    return y
    
def get_df_as_table_with_formats(df, columndict, index_name, transpose_bool):
    """function(df,columndict,index_name, transpose_bool)
    
    Takes dataframe, dict of column names and
    functions to apply to those columns, a 
    name for the index column, and a boolean
    indicating whether the df should be 
    transposed prior to converting into a list
    of lists.
    """
    r = []
    try:
        if transpose_bool:
            s = [index_name]
            s.extend([col for col in df.index])
            r.append(s)
        else:
            r.append([col for col in columndict])
    except:
        print 'Received non-dict during get_df_as_table_with_formats function, aborting and returning empty list.'
    else:
        if (df is None) or (len(df)==0):
            print 'Found no data to load during get_df_as_table_with_formats function, aborting and returning empty list.'
        else:
            try:
                for col in columndict:
                    df[col] = df[col].apply(columndict[col])
            except:
                print 'Failed to apply functions during get_df_as_table_with_formats function, aborting and returning empty list.'
            else:
                if not(min([x in df.columns for x in columndict])):
                    print 'Received request for columns that are not in dataframe during get_df_as_table_with_formats function, aborting and returning empty list.'
                else:
                    try:
                        if transpose_bool: 
                            df = df.transpose()
                            for i in range(0,len(columndict)):
                                r_1 = [str(df.index[i])]
                                r_j = []
                                for j in df.columns:
                                    r_j.append(df[j][i])
                                r_1.extend(r_j)
                                r.append(r_1)
                        else:
                            for i in range(0,len(df)):
                                r_1 = [str(df.index[i])]
                                r_j = []
                                for j in columndict:
                                    r_j.append(df[j][i])
                                r_1.extend(r_j)
                                r.append(r_1)
                            
                    except:
                        print 'Failed to create table during get_df_as_table_with_formats function, aborting and returning empty list.'
    return r

def get_monthly_dataframe_as_table(df, columnlist):
    """function(df,columnlist)
    
    Takes dataframe and a list
    of column names to include
    in the output.  Index put
    in first column as Month."""
    r = []
    try:
        r.append(columnlist)
    except:
        print 'Received non-list during get_monthly_dataframe_as_table function, aborting and returning empty list.'
    else:
        try:
            df_dec = df
        except:
            print 'Failed to load dataframe during get_monthly_dataframe_as_table function, aborting and returning empty list.'
        else:
            if (df_dec is None) or (len(df_dec)==0):
                print 'Found no data to load during get_monthly_dataframe_as_table function, aborting and returning empty list.'
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
                    print 'Failed to convert decimals to floats during get_monthly_dataframe_as_table function, aborting and returning empty list.'
                else:
                    if not(min([x in df.columns for x in columnlist[1:]])):
                        print 'Received request for columns that are not in dataframe during get_monthly_dataframe_as_table function, aborting and returning empty list.'
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
                            print 'Failed to create table during get_monthly_dataframe_as_table function, aborting and returning empty list.'
    return r

def get_default_units(utility_type):
    """function(utility_type)
        utility_type = from Meter options
        
    Given the utility type, returns
    the default units for that type."""
    try:
        sf = {
                    'electricity':      'kW,kWh',
                    'natural gas':      'therms/h,therms',
                    'steam':            'lb/h,lb',
                    'hot water':        'MMBtuh,MMBtu',
                    'chilled water':    'tons,ton-h',
                    'kerosene':         'gpm,gal',
                    'fuel oil (1,2,4), diesel':     'gpm,gal',
                    'fuel oil (5,6)':               'gpm,gal',
                    'propane and liquid propane':   'gpm,gal',
                    'coal (anthracite)':    'ton(wt)/h,tons(wt)',
                    'coal (bituminous)':    'ton(wt)/h,tons(wt)',
                    'coke':     'ton(wt)/h,tons(wt)',
                    'wood':     'ton(wt)/h,tons(wt)',
                    'other':    'kBtuh,kBtu'}
        units = sf[utility_type]
    except:
        print 'Function get_default_units failed, aborting and returning None.'
        units = None
    return units
    
def convert_units_sum_meters(utility_type, units, list_of_meters, first_month='', last_month=''):
    """function(utility_type, units, list_of_meters, first_month, last_month)
        utility_type/units = from Meter options
        list = Meter objects
        first/last_month = mm/yyyy strings for date range
        
    Given the type, units and mm/yyyy
    month strings and a list of Meters,
    function retrieves dataframes, 
    converts units, and sums peak
    demand and consumption in all 
    dataframes."""
    try:
        if len([type(x.id) for x in list_of_meters if type(x.id) is not int]) > 0:
            raise AttributeError
    except:
        print 'Function convert_units_sum_meters given non-model input, aborting and returning None.'
        df_sum = None
    else:
        try:
            if units not in ['kW,kWh','therms/h,therms','gpm,gal',
                             'kBtuh,kBtu','MMBtuh,MMBtu','Btuh,Btu',
                             'tons,ton-h','MW,MWh','cf/m,cf','ccf/h,ccf',
                             'kcf/h,kcf','MMcf/h,MMcf','m^3/h,m^3',
                             'lb/h,lb','klb/h,klb','MMlb/h,MMlb',
                             'lpm,lit','ton(wt)/h,tons(wt)',
                             'lbs(wt)/h,lbs(wt)','klbs(wt)/h,klbs(wt)',
                             'MMlbs(wt)/h,MMlbs(wt)']:
                raise AttributeError
            if utility_type not in ['electricity',
                                    'natural gas',
                                    #'domestic water', Note: not energy units!
                                    'chilled water',
                                    'hot water',
                                    'steam',
                                    'fuel oil (1,2,4), diesel',
                                    'fuel oil (5,6)',
                                    'kerosene',
                                    'propane and liquid propane',
                                    'coal (anthracite)',
                                    'coal (bituminous)',
                                    'coke',
                                    'wood',
                                    'other']:
                raise AttributeError
        except:
            print 'Function convert_units_sum_meters given bad utility_type or units input, aborting and returning None.'
            df_sum = None
        else:
            try:
                sf = {
                    'electricity':              {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'kW,kWh': Decimal(3.412),
                                                'MW,MWh': Decimal(3412)},
                    'natural gas':              {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'cf/m,cf': Decimal(1.029),
                                                'ccf/h,ccf': Decimal(102.9),
                                                'kcf/h,kcf': Decimal(1029),
                                                'MMcf/h,MMcf': Decimal(1029000),
                                                'therms/h,therms': Decimal(100),
                                                'm^3/h,m^3': Decimal(36.339)},
                    'steam':                    {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'lb/h,lb': Decimal(1.194),
                                                'klb/h,klb': Decimal(1194),
                                                'MMlb/h,MMlb': Decimal(1194000),
                                                'therms/h,therms': Decimal(100)},
                    'hot water':                {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'therms/h,therms': Decimal(100)},
                    'chilled water':            {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'tons,ton-h': Decimal(12)},
                    'kerosene':                 {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'gpm,gal': Decimal(135),
                                                'lpm,lit': Decimal(35.1)},
                    'fuel oil (1,2,4), diesel': {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'gpm,gal': Decimal(138.6905),
                                                'lpm,lit': Decimal(36.060)},
                    'fuel oil (5,6)':           {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'gpm,gal': Decimal(149.6905),
                                                'lpm,lit': Decimal(38.920)},
                    'propane and liquid propane': {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'cf/m,cf': Decimal(2.5185),
                                                'kcf/h,kcf': Decimal(2518.5),
                                                'gpm,gal': Decimal(91.6476),
                                                'lpm,lit': Decimal(23.828)},
                    'coal (anthracite)':        {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'ton(wt)/h,tons(wt)': Decimal(25090),
                                                'lbs(wt)/h,lbs(wt)': Decimal(12.545),
                                                'klbs(wt)/h,klbs(wt)': Decimal(12545),
                                                'MMlbs(wt)/h,MMlbs(wt)': Decimal(12545000)},
                    'coal (bituminous)':        {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'ton(wt)/h,tons(wt)': Decimal(24930),
                                                'lbs(wt)/h,lbs(wt)': Decimal(12.465),
                                                'klbs(wt)/h,klbs(wt)': Decimal(12465),
                                                'MMlbs(wt)/h,MMlbs(wt)': Decimal(12465000)},
                    'coke':                     {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'ton(wt)/h,tons(wt)': Decimal(24800),
                                                'lbs(wt)/h,lbs(wt)': Decimal(12.4),
                                                'klbs(wt)/h,klbs(wt)': Decimal(12400),
                                                'MMlbs(wt)/h,MMlbs(wt)': Decimal(12400000)},
                    'wood':                     {'kBtuh,kBtu': Decimal(1),
                                                'MMBtuh,MMBtu': Decimal(1000),
                                                'ton(wt)/h,tons(wt)': Decimal(15380)},
                    'other':                    {'kBtuh,kBtu': Decimal(1)}}
                column_list_convert =  ['Billing Demand (act)',
                                'Billing Demand (asave)',
                                'Billing Demand (base delta)',
                                'Billing Demand (base)',
                                'Billing Demand (esave delta)',
                                'Billing Demand (esave)',
                                'Billing Demand (exp delta)',
                                'Billing Demand (exp)',
                                'Consumption (act)',
                                'Consumption (asave)',
                                'Consumption (base delta)',
                                'Consumption (base)',
                                'Consumption (esave delta)',
                                'Consumption (esave)',
                                'Consumption (exp delta)',
                                'Consumption (exp)',
                                'Peak Demand (act)',
                                'Peak Demand (asave)',
                                'Peak Demand (base delta)',
                                'Peak Demand (base)',
                                'Peak Demand (esave delta)',
                                'Peak Demand (esave)',
                                'Peak Demand (exp delta)',
                                'Peak Demand (exp)']
                column_list_sum = ['Billing Demand (act)',
                                'Billing Demand (asave)',
                                'Billing Demand (base delta)',
                                'Billing Demand (base)',
                                'Billing Demand (esave delta)',
                                'Billing Demand (esave)',
                                'Billing Demand (exp delta)',
                                'Billing Demand (exp)',
                                'Consumption (act)',
                                'Consumption (asave)',
                                'Consumption (base delta)',
                                'Consumption (base)',
                                'Consumption (esave delta)',
                                'Consumption (esave)',
                                'Consumption (exp delta)',
                                'Consumption (exp)',
                                'Cost (act)',
                                'Cost (asave)',
                                'Cost (base delta)',
                                'Cost (base)',
                                'Cost (esave delta)',
                                'Cost (esave)',
                                'Cost (exp delta)',
                                'Cost (exp)',
                                'Peak Demand (act)',
                                'Peak Demand (asave)',
                                'Peak Demand (base delta)',
                                'Peak Demand (base)',
                                'Peak Demand (esave delta)',
                                'Peak Demand (esave)',
                                'Peak Demand (exp delta)',
                                'Peak Demand (exp)',
                                'kBtu Consumption (act)',
                                'kBtu Consumption (asave)',
                                'kBtu Consumption (base delta)',
                                'kBtu Consumption (base)',
                                'kBtu Consumption (esave delta)',
                                'kBtu Consumption (esave)',
                                'kBtu Consumption (exp delta)',
                                'kBtu Consumption (exp)',
                                'kBtuh Peak Demand (act)',
                                'kBtuh Peak Demand (asave)',
                                'kBtuh Peak Demand (base delta)',
                                'kBtuh Peak Demand (base)',
                                'kBtuh Peak Demand (esave delta)',
                                'kBtuh Peak Demand (esave)',
                                'kBtuh Peak Demand (exp delta)',
                                'kBtuh Peak Demand (exp)']
                meter_data_lists = [[x.utility_type,x.units,x.get_bill_data_period_dataframe(first_month=first_month,last_month=last_month)] for x in list_of_meters]
                for i,meter in enumerate(meter_data_lists):
                    meter_df = meter[2]
                    for col in column_list_convert:
                        meter_df[col] = meter_df[col] * sf[meter[0]][meter[1]] / sf[utility_type][units]
                    meter_data_lists[i][2] = meter_df
                df_sum = meter_data_lists[0][2]
                for meter in meter_data_lists[1:]:
                    for col in column_list_sum:
                        df_sum[col] = df_sum[col].add(meter[2][col],fill_value=0)
            except:
                print 'Function convert_units_sum_meters failed to compute sum, aborting and returning None.'
                df_sum = None
    return df_sum
    
def get_model_key_value_pairs_as_nested_list(mymodel):
    """Returns list of lists containing key-value
    pairs of all of a model's fields."""
    m_list = [['Attribute', 'Value']]
    try:
        if type(mymodel.id) is not int:
            raise AttributeError
    except:
        print 'Function get_model_key_value_pairs_as_nested_list given non-model input, aborting and returning empty list.'
        m_list = []
    else:
        try:
            for z in mymodel._meta.get_all_field_names():
                try:
                    if str(mymodel.__getattribute__(z)) == '':
                        val = '-'
                    else:
                        val = str(mymodel.__getattribute__(z))
                    m_list.append([str(z.replace('_',' ')), val])
                except AttributeError:
                    pass
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='Object %s of type %s unable to retrieve list of lists of its key-value pairs, aborting and returning empty list.' % (mymodel.id, mymodel.__class__()))
            m.save()
            mymodel.messages.add(m)
            print m
            m_list = []
    return m_list

def import_template_path(instance, filename):
    return 'BuildingSpeak Import Template.xlsx'
def upload_model_data_path(instance, filename):
    return 'uploaded_' + timezone.now().strftime('%Y-%m-%d_%H-%M') + '_' + filename
def upload_processed_file_path(instance, filename):
    return 'uploaded_' + timezone.now().strftime('%Y-%m-%d_%H-%M') + '_processed.xlsx'
class ManagementAction(models.Model):
    """Model for running management
    commands from the admin portal.
    Check a function box to have that
    function run when the model is
    saved from the admin."""
    name = models.CharField(max_length=200, default='Click this link to perform management actions')
    create_a_new_import_file = models.BooleanField(blank=True, default=False,
                                                   verbose_name='Create a new import file?')
    import_file = models.FileField(null=True, blank=True,
                                   upload_to=import_template_path,
                                   storage=S3BotoStorage(location='management_files'),
                                   help_text='link to import template')
    load_model_data = models.BooleanField(blank=True, default=False,
                                verbose_name='Upload new models or model relationships?')
    model_data_file_for_upload = models.FileField(null=True, blank=True,
                                   upload_to=upload_model_data_path,
                                   storage=S3BotoStorage(location='management_files'),
                                  help_text='upload file containing model data or relationships here')
    processed_file = models.FileField(null=True, blank=True,
                                   upload_to=upload_processed_file_path,
                                   storage=S3BotoStorage(location='management_files'),
                                   help_text='processed file containing model data with IDs')
    #relationships
    messages = models.ManyToManyField('Message')

    #functions
    def latest_messages_for_admin(self):
        if self.messages.count > 0:
            c = min(15, self.messages.count()) #--show the most recent up to 15 messages
            t = [x.when for x in self.messages.order_by('when')]
            v = [x for x in self.messages.order_by('when')]
            s = pd.Series(v, index = t)
            s = s.sort_index()
            s = s[-1:-(c+1):-1]
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_message_change',args=(message.id,)), message.subject) for message in s])
    latest_messages_for_admin.allow_tags = True
    latest_messages_for_admin.short_description = 'Recent Messages'
    def swap(self,x,c,y):
        """func(x,c,y)
        swap y for x when x is c"""
        if x == c:
            z = y
        else:
            z = x
        return z
    def swapid(self,x):
        """func(x)
        if x is a Model,
        returns x.id"""
        if issubclass(x.__class__, Model):
            z = x.id
        else:
            z = x
        return z

    def load_model_data_file(self):
        #this block is for new models; does not yet check like it needs to
        #need to identify difference between existing and new
        modeltypes = ['Account','WeatherStation','OperatingSchedule','Utility',
                      'Building','RateSchedule','Meter','Equipment','Space',
                      'Event','Reader','RooftopUnit','UnitSchedule']
        try:
            self.model_data_file_for_upload.open()
            self.model_data_file_for_upload.close()
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Open model data file failed.',
                        comment='ManagementAction unable to load new model data, function aborted.')
            m.save()
            self.messages.add(m)
            print m
        else:
            try:    #---this block creates a dataframe for each sheet and dumps into dict
                self.model_data_file_for_upload.open()
                uploaded_file = pd.ExcelFile(self.model_data_file_for_upload)
                data = {}
                for modeltype in modeltypes:
                    data[modeltype] = uploaded_file.parse(modeltype, index_col = None)
                self.model_data_file_for_upload.close()
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Parse uploaded file to dataframe failed.',
                            comment='ManagementAction unable to parse uploaded file, aborting.')
                m.save()
                self.messages.add(m)
                print m
            else:   #---identifies field names of FKs on other models for a given model type
                    #---e.g. Buildings and Meters have FK to Account through the attribute "account"
                relationdict = {'Account':{'Building':'account',
                                           'Meter':'account'},
                                'WeatherStation':{'Building':'weather_station',
                                                  'Meter':'weather_station'},
                                'OperatingSchedule':{'Equipment':'schedule',
                                                     'RooftopUnit':'schedule'},
                                'Utility':{'RateSchedule':'utility',
                                           'Meter':'utility'},
                                'RateSchedule':{'Meter':'rate_schedule'},
                                'Building':{'Space':'building'}}
                #---first load all models that already exist and are used as FKs for other models
                for modeltype in relationdict:
                    try:
                        modelclass = get_model('BuildingSpeakApp',modeltype)
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Retrieve class failed.',
                                    comment='ManagementAction unable to retrieve class type %s, aborting and moving to next class type.' % modeltype)
                        m.save()
                        self.messages.add(m)
                        print m
                    else:
                        try:
                            for df in relationdict[modeltype]:  #---relationdict tells us where FK relations are that we need to visit
                                if ( (df in data) and
                                     (len(data[df][relationdict[modeltype][df] + '_value']) > 0)  ):
                                    #---forcing dtype to not be float (if all floats or ints, pandas will create a float dtype and not allow dumping a model instance)
                                    data[df][relationdict[modeltype][df] + '_value'] = data[df][relationdict[modeltype][df] + '_value'].astype('object')
                                    for i in range(0,len(data[df][relationdict[modeltype][df] + '_value'])):
                                        id_value = data[df][relationdict[modeltype][df] + '_value'][i:i+1][0]
                                        if type(id_value) is float:     #---if id_value is integer (pandas makes them floats), it already exists, so load it
                                            try:
                                                model_i = modelclass.objects.get(pk = id_value)
                                            except:
                                                m = Message(when=timezone.now(),
                                                            message_type='Code Error',
                                                            subject='Retrieve model failed.',
                                                            comment='ManagementAction unable to retrieve %s %s on row %d, aborting and moving to next row.' % (modeltype, str(id_value), i))
                                                m.save()
                                                self.messages.add(m)
                                                print m
                                            else:
                                                try:
                                                    data[df][relationdict[modeltype][df] + '_value'][i:i+1][0] = model_i
                                                except:
                                                    m = Message(when=timezone.now(),
                                                                message_type='Code Error',
                                                                subject='Swap model for string PK failed.',
                                                                comment='ManagementAction unable to replace PK with %s %d on row %d, aborting and moving to next row.' % (modeltype, id_value, i))
                                                    m.save()
                                                    self.messages.add(m)
                                                    print m
                        except:
                            m = Message(when=timezone.now(),
                                        message_type='Code Error',
                                        subject='Swap models for string PKs failed.',
                                        comment='ManagementAction unable to replace PKs with model instances, aborting and moving on; note that some models in uploaded sheet requiring these models to be loaded will fail.')
                            m.save()
                            self.messages.add(m)
                            print m
                #---step through loading all new models for modeltype, then move to next type
                for modeltype in modeltypes:
                    try:
                        modelclass = get_model('BuildingSpeakApp',modeltype)
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Retrieve class failed.',
                                    comment='ManagementAction unable to retrieve class type %s, aborting and moving to next class type.' % modeltype)
                        m.save()
                        self.messages.add(m)
                        print m
                    else:
                        data[modeltype]['id_value'] = data[modeltype]['id_value'].astype('object') #---forcing dtype to not be float (if all floats or ints, pandas will create a float dtype and not allow dumping a model instance)
                        modeldf = data[modeltype]        #---extract the modeltype's dataframe
                        for i in range(0,len(modeldf)):  #---loop through all rows; each row is a model
                            id_value = data[modeltype]['id_value'][i:i+1][0]    #---get integer model ID
                            if type(id_value) is float:     #---if id_value is integer (pandas makes them floats), it already exists, so load it
                                try:
                                    existingmodel = modelclass.objects.get(pk = id_value)
                                except:
                                    m = Message(when=timezone.now(),
                                                message_type='Code Error',
                                                subject='Retrieve model failed.',
                                                comment='ManagementAction unable to retrieve %s %d on row %d that should exist according to uploaded file, aborting and moving to next row.' % (modeltype, id_value, i))
                                    m.save()
                                    self.messages.add(m)
                                    print m
                                else:
                                    try:   #---extract field names and values, then morph to dict for loading
                                        fields = modeldf[modeldf.columns[0::2]][i:i+1]
                                        values = modeldf[modeldf.columns[1::2]][i:i+1]
                                        m = pd.Series(values.values[0], index = fields)
                                        md = m[(m.notnull()) & (m.index<>'id')].to_dict()
                                        for k, v in md.items():
                                            existingmodel.__setattr__(k, v)  #---update existing model
                                        existingmodel.save()
                                    except:
                                        m = Message(when=timezone.now(),
                                                    message_type='Code Error',
                                                    subject='Model update failed.',
                                                    comment='ManagementAction unable to update %s %d on row %d, aborting and moving to next row.' % (modeltype, id_value, i))
                                        m.save()
                                        self.messages.add(m)
                                        print m
                                    else:
                                        try:    #---then overwrite integer model ID (id_value) wherever it appears
                                            data[modeltype]['id_value'][i:i+1][0] = existingmodel #---overwrite integer model ID with model instance
                                            if modeltype in relationdict:
                                                for df in relationdict[modeltype]:  #---relationdict tells us where FK relations are that we need to visit
                                                    if len(data[df][relationdict[modeltype][df] + '_value']) > 0:
                                                        data[df][relationdict[modeltype][df] + '_value'] = data[df][relationdict[modeltype][df] + '_value'].apply(self.swap,**{'c':id_value,'y':existingmodel})
                                        except:
                                            m = Message(when=timezone.now(),
                                                        message_type='Code Error',
                                                        subject='Swap model for string PK failed.',
                                                        comment='ManagementAction unable to swap models for integer PKs after loading %s %d on row %d of uploaded sheet, aborting and moving to next row.' % (modeltype, id_value, i))
                                            m.save()
                                            self.messages.add(m)
                                            print m
                                        else:
                                            m = Message(when=timezone.now(),
                                                        message_type='Code Success',
                                                        subject='Loaded and/or updated model.',
                                                        comment='ManagementAction loaded and, if necessary, updated %s %d on row %d of uploaded sheet, moving to next row.' % (modeltype, id_value, i))
                                            m.save()
                                            self.messages.add(m)
                                            print m
                            elif type(id_value) is unicode:#---if id_value is unicode, it's new, so create it
                                try:    #---extract field names and values, then morph to dict for loading
                                    fields = modeldf[modeldf.columns[0::2]][i:i+1]
                                    values = modeldf[modeldf.columns[1::2]][i:i+1]
                                    m = pd.Series(values.values[0], index = fields)
                                    md = m[(m.notnull()) & (m.index<>'id')].to_dict()
                                    newmodel = modelclass(**md)
                                    newmodel.save()
                                except:
                                    m = Message(when=timezone.now(),
                                                message_type='Code Error',
                                                subject='Model load failed.',
                                                comment='ManagementAction unable to load %s on row %d of uploaded sheet, aborting and moving to next row.' % (modeltype, i))
                                    m.save()
                                    self.messages.add(m)
                                    print m
                                else:
                                    if newmodel.id is not None:
                                        m = Message(when=timezone.now(),
                                                    message_type='Code Success',
                                                    subject='Model created.',
                                                    comment='ManagementAction successfully created %s %d from row %d of uploaded sheet, moving on.' % (modeltype, newmodel.id, i))
                                        m.save()
                                        self.messages.add(m)
                                        print m
                                        c = data[modeltype]['id_value'][i:i+1][0]   #---capture string name
                                        data[modeltype]['id_value'][i:i+1][0] = newmodel #---overwrite string name with model instance
                                        try:    #---then overwrite string name (c) wherever else it appears
                                            if modeltype in relationdict:
                                                for df in relationdict[modeltype]:  #---relationdict tells us where FK relations are that we need to visit
                                                    if len(data[df][relationdict[modeltype][df] + '_value']) > 0:
                                                        data[df][relationdict[modeltype][df] + '_value'] = data[df][relationdict[modeltype][df] + '_value'].apply(self.swap,**{'c':c,'y':newmodel})
                                        except:
                                            m = Message(when=timezone.now(),
                                                        message_type='Code Error',
                                                        subject='Swap model for string name failed.',
                                                        comment='ManagementAction unable to swap models for string names after creating %s on row %d of uploaded sheet, aborting and moving to next row.' % (modeltype, i))
                                            m.save()
                                            self.messages.add(m)
                                            print m
                                    else:
                                        m = Message(when=timezone.now(),
                                                    message_type='Code Error',
                                                    subject='Model save failed.',
                                                    comment='ManagementAction attempt to save %s from row %d of uploaded sheet did not return an ID, moving to next row.' % (modeltype, i))
                                        m.save()
                                        self.messages.add(m)
                                        print m
                            else:
                                m = Message(when=timezone.now(),
                                            message_type='Code Error',
                                            subject='Function received bad arguments.',
                                            comment='ManagementAction received a PK from %s row %d of uploaded sheet that was neither float (int) nor unicode, aborting and moving to next row.' % (modeltype, i))
                                m.save()
                                self.messages.add(m)
                                print m
                                    
                #---now all models have been loaded
                #---now replace models with their IDs for storing in "_processed" Excel file
                try:
                    for modeltype in modeltypes:
                        if modeltype in relationdict:
                            for df in relationdict[modeltype]:  #now replace models with id's
                                if len(data[df][relationdict[modeltype][df] + '_value']) > 0:
                                    data[df][relationdict[modeltype][df] + '_value'] = data[df][relationdict[modeltype][df] + '_value'].apply(self.swapid)
                        if len(data[modeltype]['id_value']) > 0:
                            data[modeltype]['id_value'] = data[modeltype]['id_value'].apply(self.swapid)
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Swap string PKs for models failed.',
                                comment='ManagementAction unable to replace models with model IDs for exporting revised load file, aborting, though models should have still been created.')
                    m.save()
                    self.messages.add(m)
                    print m
                else:
                    try:
                        filename = 'temp_processed.xlsx'
                        writer = pd.ExcelWriter(filename)
                        for modeltype in modeltypes:
                            data[modeltype].to_excel(writer, sheet_name = modeltype)
                        writer.save()
                        astring = open(filename,'rb').read()
                        mycontent = ContentFile(astring)
                        self.load_model_data = False
                        self.processed_file.save(name = filename, content = mycontent, save = False)
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Write processed file failed.',
                                    comment='ManagementAction unable to write revised load file, aborting, though models should have still been created.')
                        m.save()
                        self.messages.add(m)
                        print m
                    else:
                        m = Message(when=timezone.now(),
                                    message_type='Code Success',
                                    subject='Created processed file.',
                                    comment='ManagementAction successfully created and stored a processed file containing original model data plus new model IDs.')
                        m.save()
                        self.messages.add(m)
                        print m
                        
        self.load_model_data = False
    
    def create_import_template_file(self):
        try:
            filename = 'BuildingSpeak Import File.xlsx'
            writer = pd.ExcelWriter(filename)
        
    #        m2ms_Account = [i.name for i in Account._meta.many_to_many]
            fields_Account = [i.name for i in Account._meta.fields]
    #        m2ms_WeatherStation = [i.name for i in WeatherStation._meta.many_to_many]
            fields_WeatherStation = [i.name for i in WeatherStation._meta.fields]
    #        m2ms_OperatingSchedule = [i.name for i in OperatingSchedule._meta.many_to_many]
            fields_OperatingSchedule = [i.name for i in OperatingSchedule._meta.fields]
    #        m2ms_Utility = [i.name for i in Utility._meta.many_to_many]
            fields_Utility = [i.name for i in Utility._meta.fields]
    #        m2ms_Building = [i.name for i in Building._meta.many_to_many]
            fields_Building = [i.name for i in Building._meta.fields]
    #        m2ms_RateSchedule = [i.name for i in RateSchedule._meta.many_to_many]
            fields_RateSchedule = [i.name for i in RateSchedule._meta.fields]
    #        m2ms_Meter = [i.name for i in Meter._meta.many_to_many]
            fields_Meter = [i.name for i in Meter._meta.fields]
    #        m2ms_Equipment = [i.name for i in Equipment._meta.many_to_many]
            fields_Equipment = [i.name for i in Equipment._meta.fields]
    #        m2ms_Space = [i.name for i in Space._meta.many_to_many]
            fields_Space = [i.name for i in Space._meta.fields]
    #        m2ms_Reader = [i.name for i in Reader._meta.many_to_many]
            fields_Reader = [i.name for i in Reader._meta.fields]
    #        m2ms_RooftopUnit = [i.name for i in RooftopUnit._meta.many_to_many]
            fields_RooftopUnit = [i.name for i in RooftopUnit._meta.fields]
    #        m2ms_UnitSchedule = [i.name for i in UnitSchedule._meta.many_to_many]
            fields_UnitSchedule = [i.name for i in UnitSchedule._meta.fields]
        
            df_Account = pd.DataFrame()
            for i in fields_Account:
                df_Account[i] = None
                df_Account[i + '_value'] = None
    #        for i in m2ms_Account:
    #            df_Account[i] = None
    #            df_Account[i + '_value'] = None
            df_Account.to_excel(writer, sheet_name='Account')
            
            df_WeatherStation = pd.DataFrame()
            for i in fields_WeatherStation:
                df_WeatherStation[i] = None
                df_WeatherStation[i + '_value'] = None
    #        for i in m2ms_WeatherStation:
    #            df_WeatherStation[i] = None
    #            df_WeatherStation[i + '_value'] = None
            df_WeatherStation.to_excel(writer, sheet_name='WeatherStation')
            
            df_OperatingSchedule = pd.DataFrame()
            for i in fields_OperatingSchedule:
                df_OperatingSchedule[i] = None
                df_OperatingSchedule[i + '_value'] = None
    #        for i in m2ms_OperatingSchedule:
    #            df_OperatingSchedule[i] = None
    #            df_OperatingSchedule[i + '_value'] = None
            df_OperatingSchedule.to_excel(writer, sheet_name='OperatingSchedule')
            
            df_Utility = pd.DataFrame()
            for i in fields_Utility:
                df_Utility[i] = None
                df_Utility[i + '_value'] = None
    #        for i in m2ms_Utility:
    #            df_Utility[i] = None
    #            df_Utility[i + '_value'] = None
            df_Utility.to_excel(writer, sheet_name='Utility')
            
            df_Building = pd.DataFrame()
            for i in fields_Building:
                df_Building[i] = None
                df_Building[i + '_value'] = None
    #        for i in m2ms_Building:
    #            df_Building[i] = None
    #            df_Building[i + '_value'] = None
            df_Building.to_excel(writer, sheet_name='Building')
            
            df_RateSchedule = pd.DataFrame()
            for i in fields_RateSchedule:
                df_RateSchedule[i] = None
                df_RateSchedule[i + '_value'] = None
    #        for i in m2ms_RateSchedule:
    #            df_RateSchedule[i] = None
    #            df_RateSchedule[i + '_value'] = None
            df_RateSchedule.to_excel(writer, sheet_name='RateSchedule')
            
            df_Meter = pd.DataFrame()
            for i in fields_Meter:
                df_Meter[i] = None
                df_Meter[i + '_value'] = None
    #        for i in m2ms_Meter:
    #            df_Meter[i] = None
    #            df_Meter[i + '_value'] = None
            df_Meter.to_excel(writer, sheet_name='Meter')
            
            df_Equipment = pd.DataFrame()
            for i in fields_Equipment:
                df_Equipment[i] = None
                df_Equipment[i + '_value'] = None
    #        for i in m2ms_Equipment:
    #            df_Equipment[i] = None
    #            df_Equipment[i + '_value'] = None
            df_Equipment.to_excel(writer, sheet_name='Equipment')
            
            df_Space = pd.DataFrame()
            for i in fields_Space:
                df_Space[i] = None
                df_Space[i + '_value'] = None
    #        for i in m2ms_Space:
    #            df_Space[i] = None
    #            df_Space[i + '_value'] = None
            df_Space.to_excel(writer, sheet_name='Space')
            
            df_Reader = pd.DataFrame()
            for i in fields_Reader:
                df_Reader[i] = None
                df_Reader[i + '_value'] = None
    #        for i in m2ms_Reader:
    #            df_Reader[i] = None
    #            df_Reader[i + '_value'] = None
            df_Reader.to_excel(writer, sheet_name='Reader')
            
            df_RooftopUnit = pd.DataFrame()
            for i in fields_RooftopUnit:
                df_RooftopUnit[i] = None
                df_RooftopUnit[i + '_value'] = None
    #        for i in m2ms_RooftopUnit:
    #            df_RooftopUnit[i] = None
    #            df_RooftopUnit[i + '_value'] = None
            df_RooftopUnit.to_excel(writer, sheet_name='RooftopUnit')
            
            df_UnitSchedule = pd.DataFrame()
            for i in fields_UnitSchedule:
                df_UnitSchedule[i] = None
                df_UnitSchedule[i + '_value'] = None
    #        for i in m2ms_UnitSchedule:
    #            df_UnitSchedule[i] = None
    #            df_UnitSchedule[i + '_value'] = None
            df_UnitSchedule.to_excel(writer, sheet_name='UnitSchedule')
            
            writer.save()
    
            astring=open(filename,'rb').read()
            mycontent = ContentFile(astring)
            self.create_a_new_import_file = False
            self.import_file.save(name=filename, content=mycontent, save=False)
            m = Message(when=timezone.now(),
                        message_type='Code Success',
                        subject='Created upload template.',
                        comment='ManagementAction successfully created new upload template file.')
            m.save()
            self.messages.add(m)
            print m
            self.create_a_new_import_file = False
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Create upload template failed.',
                        comment='ManagementAction unable to create new upload template file, function aborted.')
            m.save()
            self.messages.add(m)
            print m
            self.create_a_new_import_file = False
            self.save()
            
    def save(self, *args, **kwargs):
        if self.create_a_new_import_file:
            self.create_import_template_file()
            super(ManagementAction, self).save(*args, **kwargs)
        if self.load_model_data:
            super(ManagementAction, self).save(*args, **kwargs)
            self.load_model_data_file()
        if not(self.create_a_new_import_file) and not(self.load_model_data):
            super(ManagementAction, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'


def update_readers(modelinstance):
    """Function to update all Readers
    on given Account, Building,
    Space, Meter, or Equipment model."""
    try:
        modeltype = modelinstance.__repr__()[1:].partition(':')[0]
    except:
        m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Function received bad arguments.',
                    comment='Model %s of type %s given to update_readers function, expected Account, Building, Space, Meter, or Equipment, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
        m.save()
        modelinstance.messages.add(m)
        print m
    else:
        if modeltype not in ['Account', 'Building', 'Space', 'Meter', 'Equipment']:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='Model %s of type %s given to update_readers function, expected Account, Building, Space, Meter, or Equipment, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
            m.save()
            modelinstance.messages.add(m)
            print m
        else:
            if modelinstance.observed_file_track:
                try:
                    df = pd.read_csv(modelinstance.observed_file.url,
                                     skiprows=modelinstance.observed_file_skiprows,
                                     parse_dates=True,
                                     index_col=modelinstance.observed_file_column_for_indexing)
                except:
                    m = Message(when=timezone.now(),
                               message_type='Code Error',
                               subject='File not found.',
                               comment='observed_file of model %s of type %s not found by update_readers function, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                    m.save()
                    modelinstance.messages.add(m)
                    print m
                else:
                    try:
                        df = df.sort_index()
                        df.index = df.index - timedelta(hours=float(modelinstance.observed_file_GMT_offset))
                        df.index = df.index.tz_localize('UTC')
                    except:
                        m = Message(when=timezone.now(),
                                   message_type='Code Error',
                                   subject='Adjust dataframe index failed.',
                                   comment='Failed to adjust index of observed_file dataframe of model %s of type %s in update_readers function, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                        m.save()
                        modelinstance.messages.add(m)
                        print m
                    else:
                        column_headers = df.columns
                        df.columns = range(0,len(df.columns))
                        try:
                            for r in modelinstance.readers.filter(source=1).filter(active=True):
                                try:
                                    rts = r.get_reader_time_series()
                                    rts = rts.sort_index()
                                    if len(df[r.column_index]) < 1:  #nothing to add, so abort
                                        m = Message(when=timezone.now(),
                                                   message_type='Code Warning',
                                                   subject='No data.',
                                                   comment='No new data found for Reader %s of provided_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                        m.save()
                                        modelinstance.messages.add(m)
                                        r.messages.add(m)
                                        print m                                    
                                    elif len(rts) < 1: #nothing existing, so add all new stuff
                                        r.load_reader_time_series(df[r.column_index])
                                        r.column_header = column_headers[r.column_index]
                                        r.save()
                                        m = Message(when=timezone.now(),
                                                   message_type='Code Success',
                                                   subject='Updated model.',
                                                   comment='Successfully updated Reader %s of provided_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                        m.save()
                                        modelinstance.messages.add(m)
                                        r.messages.add(m)
                                        print m
                                    else: #existing and new, only load in more recent
                                        r.load_reader_time_series(df[r.column_index][df.index > rts.index[-1]])
                                        r.column_header = column_headers[r.column_index]
                                        r.save()
                                        m = Message(when=timezone.now(),
                                                   message_type='Code Success',
                                                   subject='Updated model.',
                                                   comment='Successfully updated Reader %s of provided_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                        m.save()
                                        modelinstance.messages.add(m)
                                        r.messages.add(m)
                                        print m
                                except:
                                    m = Message(when=timezone.now(),
                                               message_type='Code Error',
                                               subject='Update model failed.',
                                               comment='Failed to update Reader %s of observed_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                    m.save()
                                    modelinstance.messages.add(m)
                                    print m
                        except:
                            m = Message(when=timezone.now(),
                                       message_type='Code Error',
                                       subject='Update readers failed.',
                                       comment='Failed to update readers of observed_file of model %s of type %s in update_readers function, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                            m.save()
                            modelinstance.messages.add(m)
                            print m
                        else:
                            m = Message(when=timezone.now(),
                                       message_type='Code Success',
                                       subject='Updated readers.',
                                       comment='Successfully updated readers of observed_file of model %s of type %s, except as noted by other code messages.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                            m.save()
                            modelinstance.messages.add(m)
                            print m
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='No observed_file being tracked.',
                            comment='No observed_file being tracked for model %s of type %s, update_readers function moving on.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                m.save()
                modelinstance.messages.add(m)
                print m
            if modelinstance.provided_file_track:
                try:
                    df = pd.read_csv(modelinstance.provided_file.url,
                                     skiprows=modelinstance.provided_file_skiprows,
                                     parse_dates=True,
                                     index_col=modelinstance.provided_file_column_for_indexing)
                except:
                    m = Message(when=timezone.now(),
                               message_type='Code Error',
                               subject='File not found.',
                               comment='Provided_file of model %s of type %s not found by update_readers function, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                    m.save()
                    modelinstance.messages.add(m)
                    print m
                else:
                    try:
                        df = df.sort_index()
                        df.index = df.index - timedelta(hours=float(modelinstance.provided_file_GMT_offset))
                        df.index = df.index.tz_localize('UTC')
                    except:
                        m = Message(when=timezone.now(),
                                   message_type='Code Error',
                                   subject='Adjust dataframe index failed.',
                                   comment='Failed to adjust index of provided_file dataframe of model %s of type %s in update_readers function, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                        m.save()
                        modelinstance.messages.add(m)
                        print m
                    else:
                        column_headers = df.columns
                        df.columns = range(0,len(df.columns))
                        try:
                            for r in modelinstance.readers.filter(source=2).filter(active=True):
                                try:
                                    rts = r.get_reader_time_series()
                                    rts = rts.sort_index()
                                    if len(df[r.column_index]) < 1:  #nothing to add, so abort
                                        m = Message(when=timezone.now(),
                                                   message_type='Code Warning',
                                                   subject='No data.',
                                                   comment='No new data found for Reader %s of provided_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                        m.save()
                                        modelinstance.messages.add(m)
                                        r.messages.add(m)
                                        print m                                    
                                    elif len(rts) < 1: #nothing existing, so add all new stuff
                                        r.load_reader_time_series(df[r.column_index])
                                        r.column_header = column_headers[r.column_index]
                                        r.save()
                                        m = Message(when=timezone.now(),
                                                   message_type='Code Success',
                                                   subject='Updated model.',
                                                   comment='Successfully updated Reader %s of provided_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                        m.save()
                                        modelinstance.messages.add(m)
                                        r.messages.add(m)
                                        print m
                                    else: #existing and new, only load in more recent
                                        r.load_reader_time_series(df[r.column_index][df.index > rts.index[-1]])
                                        r.column_header = column_headers[r.column_index]
                                        r.save()
                                        m = Message(when=timezone.now(),
                                                   message_type='Code Success',
                                                   subject='Updated model.',
                                                   comment='Successfully updated Reader %s of provided_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                        m.save()
                                        modelinstance.messages.add(m)
                                        r.messages.add(m)
                                        print m
                                except:
                                    m = Message(when=timezone.now(),
                                               message_type='Code Error',
                                               subject='Update model failed.',
                                               comment='Failed to update Reader %s of provided_file of model %s of type %s in update_readers function, continuing to next Reader.' % (r.id, modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                                    m.save()
                                    modelinstance.messages.add(m)
                                    print m
                        except:
                            m = Message(when=timezone.now(),
                                       message_type='Code Error',
                                       subject='Update readers failed.',
                                       comment='Failed to update readers of provided_file of model %s of type %s in update_readers function, function aborted.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                            m.save()
                            modelinstance.messages.add(m)
                            print m
                        else:
                            m = Message(when=timezone.now(),
                                       message_type='Code Success',
                                       subject='Updated readers.',
                                       comment='Successfully updated readers of provided_file of model %s of type %s, except as noted by other code messages.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                            m.save()
                            modelinstance.messages.add(m)
                            print m
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='No provided file being tracked.',
                            comment='No provided_file being tracked for model %s of type %s, update_readers function moving on.' % (modelinstance.id, modelinstance.__repr__()[1:].partition(':')[0]))
                m.save()
                modelinstance.messages.add(m)
                print m


#################
def temp_func(building):
    this_month = pd.Period(timezone.now(),freq='M')
    
    #if there are no meters, skip all meter data calcs
    if len(building.meters.all()) < 1:
        meter_data = None
    else:
        column_list_sum = ['Billing Demand (act)',
                        'Billing Demand (asave)',
                        'Billing Demand (base delta)',
                        'Billing Demand (base)',
                        'Billing Demand (esave delta)',
                        'Billing Demand (esave)',
                        'Billing Demand (exp delta)',
                        'Billing Demand (exp)',
                        'Consumption (act)',
                        'Consumption (asave)',
                        'Consumption (base delta)',
                        'Consumption (base)',
                        'Consumption (esave delta)',
                        'Consumption (esave)',
                        'Consumption (exp delta)',
                        'Consumption (exp)',
                        'Cost (act)',
                        'Cost (asave)',
                        'Cost (base delta)',
                        'Cost (base)',
                        'Cost (esave delta)',
                        'Cost (esave)',
                        'Cost (exp delta)',
                        'Cost (exp)',
                        'Peak Demand (act)',
                        'Peak Demand (asave)',
                        'Peak Demand (base delta)',
                        'Peak Demand (base)',
                        'Peak Demand (esave delta)',
                        'Peak Demand (esave)',
                        'Peak Demand (exp delta)',
                        'Peak Demand (exp)',
                        'kBtu Consumption (act)',
                        'kBtu Consumption (asave)',
                        'kBtu Consumption (base delta)',
                        'kBtu Consumption (base)',
                        'kBtu Consumption (esave delta)',
                        'kBtu Consumption (esave)',
                        'kBtu Consumption (exp delta)',
                        'kBtu Consumption (exp)',
                        'kBtuh Peak Demand (act)',
                        'kBtuh Peak Demand (asave)',
                        'kBtuh Peak Demand (base delta)',
                        'kBtuh Peak Demand (base)',
                        'kBtuh Peak Demand (esave delta)',
                        'kBtuh Peak Demand (esave)',
                        'kBtuh Peak Demand (exp delta)',
                        'kBtuh Peak Demand (exp)']
        #meter_data is what will be passed to the template
        meter_data = []
        
        #meter_dict holds all info and dataframes for each utility type, starting with Total non-water
        meter_dict = {'Total Building Energy': {'name': 'Total Building Energy',
                                                'costu': 'USD',
                                                'consu': 'kBtu',
                                                'pdu': 'kBtuh',
                                                'df': convert_units_sum_meters(
                                                        'other', 
                                                        'kBtuh,kBtu', 
                                                        building.meters.filter(~Q(utility_type = 'domestic water')), 
                                                        first_month=(this_month-12).strftime('%m/%Y'), 
                                                        last_month=this_month.strftime('%m/%Y') )
                                                } }
        
        #now cycle through all utility types present in this building, get info and dataframes
        for utype in sorted(set([x.utility_type for x in building.meters.all()])):
            utype = str(utype)
            meter_dict[utype] = {}
            meter_dict[utype]['name'] = utype
            meter_dict[utype]['costu'] = 'USD'
            meter_dict[utype]['consu'] = get_default_units(utype).split(',')[1]
            meter_dict[utype]['pdu'] = get_default_units(utype).split(',')[0]
            meter_dict[utype]['df'] = convert_units_sum_meters(
                                        utype,
                                        get_default_units(utype),
                                        building.meters.filter(utility_type=utype),
                                        first_month=(this_month-12).strftime('%m/%Y'), 
                                        last_month=this_month.strftime('%m/%Y'))
        
        #cycle through the meter_dict and pass to list meter_data, converting dataframes to tables
        for utype in meter_dict:
            dfsum = meter_dict[utype]['df']
            dfsum[column_list_sum] = dfsum[column_list_sum].applymap(nan2zero)
            meter_data.append(
                         [meter_dict[utype]['name'],
                          meter_dict[utype]['costu'],
                          meter_dict[utype]['consu'],
                          meter_dict[utype]['pdu'],
                          get_monthly_dataframe_as_table(df=dfsum,
                                                         columnlist=['Month','Cost (base)','Cost (exp)','Cost (esave)','Cost (act)','Cost (asave)']),
                          get_monthly_dataframe_as_table(df=dfsum,
                                                         columnlist=['Month','Consumption (base)','Consumption (exp)','Consumption (esave)','Consumption (act)','Consumption (asave)']),
                          get_monthly_dataframe_as_table(df=dfsum,
                                                         columnlist=['Month','Peak Demand (base)','Peak Demand (exp)','Peak Demand (esave)','Peak Demand (act)','Peak Demand (asave)']),
                          'placeholder_for_metrics_table'])
        
            
        if len(meter_data) < 1:
            meter_data = None
        else:
            pass #if necessary, weed out empty tables here
    return meter_dict,meter_data

####################
