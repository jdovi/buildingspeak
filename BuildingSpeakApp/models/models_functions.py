#import dbarray
import math
import numpy as np
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
    
def convert_units_single_value(n_value, n_utility, n_units, x_utility, x_units):
    """function(n_value, n_utility, n_units, x_utility, x_units)
    n_value =   Decimal
    n_utility = n_value's utility type (from Meter options)
    n_units =   n_value's units        (from Meter options)
    x_utility = desired utility type   (from Meter options)
    x_units =   desired units          (from Meter options)
    
    Given an energy quantity and its type
    and units, returns a value converted
    to the desired type and units. Units
    options are those available to Meter
    models."""
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
        converted_number = n_value * sf[n_utility][n_units] / sf[x_utility][x_units]
    except:
        print 'Function convert_units_single_value failed, aborting and returning None.'
        converted_number = None
    return converted_number

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
def data_file_path_space(instance, filename):
    return '/'.join(['%06d' % instance.building.account.pk,
                     'buildings',
                     '%06d' % instance.building.pk + '_' + instance.building.name,
                     'spaces',
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
def image_file_path_userprofile(instance, filename):
    return '/'.join(['user_profiles',
                     '%06d' % instance.pk,
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
def image_file_path_space(instance, filename):
    return '/'.join(['%06d' % instance.building.account.pk,
                     'buildings',
                     '%06d' % instance.building.pk + '_' + instance.building.name,
                     'space',
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

#these are helper functions used in development, have minimal if any error checking and validation
def assign_period_datetime(time_series=[], dates=[]):
    """Inputs:
        time_series or
        dates (list of start/end datetimes)
        
    Returns datetime of first day of
    most frequently occurring month in
    a given time series spanning 25-35
    days to use as basis for Period."""
    
    #raise error if empty inputs
    if (len(time_series)==0 and len(dates)<>2) or type(dates[0])<>datetime or type(dates[1])<>datetime:
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

def load_monthly_csv(file_loc):
    readbd = pd.read_csv(file_loc,
                         skiprows=0,
                         usecols=['Start Date', 'End Date', 'Billing Demand',
                                  'Peak Demand', 'Consumption', 'Cost'],
                         dtype={'Billing Demand': np.float, 'Peak Demand': np.float,
                                'Consumption': np.float, 'Cost': np.float})
    readbd['Start Date'] = readbd['Start Date'].apply(pd.to_datetime) + timedelta(hours=11,minutes=11,seconds=11) #add hours/mins/secs to avoid crossing day boundary when adjusting timezones
    readbd['End Date'] = readbd['End Date'].apply(pd.to_datetime) + timedelta(hours=11,minutes=11,seconds=11) #add hours/mins/secs to avoid crossing day boundary when adjusting timezones
    readbd['Start Date'] = readbd['Start Date'].apply(UTC.localize)
    readbd['End Date'] = readbd['End Date'].apply(UTC.localize)
    readbd['Billing Demand'] = readbd['Billing Demand'].apply(Decimal)
    readbd['Peak Demand'] = readbd['Peak Demand'].apply(Decimal)
    readbd['Consumption'] = readbd['Consumption'].apply(Decimal)
    readbd['Cost'] = readbd['Cost'].apply(Decimal)
    t = [assign_period_datetime(dates=[readbd['Start Date'][i],
                                       readbd['End Date'][i]]) for i in range(0,len(readbd))]
    readbd.index = pd.PeriodIndex(t, freq='M')
    return readbd