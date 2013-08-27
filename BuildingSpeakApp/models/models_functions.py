#import dbarray
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