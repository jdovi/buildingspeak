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
