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
from operator import itemgetter, attrgetter
from djorm_pgarray.fields import ArrayField
from model_utils.managers import InheritanceManager
from storages.backends.s3boto import S3BotoStorage
from django.contrib.auth.models import User
from django.db.models import Q, Sum

from models_functions import *
from models_Message import Message
from models_Reader_ing import Reader
from models_monthlies import Monthling

class SpaceMeterApportionment(models.Model):
    """Intermediate model defining
    relationship of Meter to Space."""
    
    #relationships
    meter = models.ForeignKey('Meter')
    space = models.ForeignKey('Space')
    
    #attributes
    assigned_fraction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3,
                            help_text='fraction of meter consumption/demand/cost assigned to space')
    
    #functions
    def __unicode__(self):
        return str(self.meter.name + ' - ' + self.space.name)
    class Meta:
        app_label = 'BuildingSpeakApp'

class Space(models.Model):
    """Model for subspaces of
    Buildings.  Accepts image
    file of floorplan or view
    of space."""
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    building = models.ForeignKey('Building')
    messages = models.ManyToManyField('Message')
    readers = models.ManyToManyField('Reader')
    schedules = models.ManyToManyField('OperatingSchedule')
    meters = models.ManyToManyField('Meter', through='SpaceMeterApportionment')
    
    #file-related attributes
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_space, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed space data')
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this space?')
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
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_space, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided space data')
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this space?')
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
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_space, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing floorplan or general space image')
    
    #attributes
    square_footage = models.IntegerField(null=True, blank=True, help_text='floor area, SF')
    max_occupancy = models.IntegerField(null=True, blank=True, help_text='space occupancy limit')
    space_type = models.CharField(blank=True, max_length=200,
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
    
    #functions
    def get_space_view_meter_data(self, month_first, month_last):
        """function(month_first, month_last)
        month_first/month_last = Periods(freq='M')
        
        Returns meter data for Space's views
        in a list: [meter_data, pie_data]."""
        #if there are no meters, skip all meter data calcs
        try:
            first_month = month_first.strftime('%m/%Y')
            last_month = month_last.strftime('%m/%Y')
            
            if len(self.meters.all()) < 1:
                result = None
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
                utility_groups = ['Total Space Energy']
                utility_groups.extend(sorted(set([str(x.utility_type) for x in self.meters.all()])))
                
                #meter_dict holds all info and dataframes for each utility group, starting with Total non-water
                meter_dict = {'Total Space Energy': {'name': 'Total Space Energy',
                                                        'costu': 'USD',
                                                        'consu': 'kBtu',
                                                        'pdu': 'kBtuh',
                                                        'df': convert_units_sum_meters(
                                                                'other', 
                                                                'kBtuh,kBtu', 
                                                                self.meters.filter(~Q(utility_type = 'domestic water')), 
                                                                first_month=first_month, 
                                                                last_month=last_month )
                                                        } }
                
                #cycle through all utility types present in this building, get info and dataframes
                for utype in sorted(set([str(x.utility_type) for x in self.meters.all()])):
                    utype = str(utype)
                    meter_dict[utype] = {}
                    meter_dict[utype]['name'] = utype
                    meter_dict[utype]['costu'] = 'USD'
                    meter_dict[utype]['consu'] = get_default_units(utype).split(',')[1]
                    meter_dict[utype]['pdu'] = get_default_units(utype).split(',')[0]
                    meter_dict[utype]['df'] = convert_units_sum_meters(
                                                utype,
                                                get_default_units(utype),
                                                self.meters.filter(utility_type=utype),
                                                first_month=first_month, 
                                                last_month=last_month)
                
                #remove all utility types for which no data was found (returned df is None)
                temp = [meter_dict.__delitem__(x) for x in meter_dict.keys() if meter_dict[x]['df'] is None]

                #now that dataframes are available, create data tables for each utility type, inc. Total
                for utype in meter_dict.keys():
                    #additional column names to be created; these are manipulations of the stored data
                    cost =              '$'
                    cost_per_day =      '$/day'
                    cost_per_sf =       '$/SF'
                    consumption =                   meter_dict[utype]['consu']
                    consumption_per_day =           meter_dict[utype]['consu'] + '/day'
                    consumption_per_sf =            meter_dict[utype]['consu'] + '/SF'
                    cost_per_consumption = '$/' +   meter_dict[utype]['consu']
                    
                    bill_data = meter_dict[utype]['df']
                    bill_data['Days'] = [(bill_data['End Date'][i] - bill_data['Start Date'][i]).days+1 for i in range(0, len(bill_data))]
                    
                    #now we create the additional columns to manipulate the stored data for display to user
                    bill_data[cost] = bill_data['Cost (act)']
                    bill_data[cost_per_day] = bill_data['Cost (act)'] / bill_data['Days']
                    bill_data[cost_per_sf] = bill_data['Cost (act)'] / self.square_footage
                    bill_data[consumption] = bill_data['Consumption (act)']
                    bill_data[consumption_per_day] = bill_data['Consumption (act)'] / bill_data['Days']
                    bill_data[consumption_per_sf] = bill_data['Consumption (act)'] / self.square_footage
                    bill_data[cost_per_consumption] = bill_data['Cost (act)'] / bill_data['Consumption (act)']
                    
                    #totals and useful ratios table calculations
                    #first we construct the dataframe we want
                    bill_data_totals = pd.DataFrame(columns = [cost,cost_per_day,cost_per_sf,consumption,consumption_per_day,consumption_per_sf,cost_per_consumption],
                                                    index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', 'Annual'])
                    #this column will get populated and then used to sort after we've jumped from Periods to Jan,Feb,etc.
                    bill_data_totals['Month Integer'] = range(1,14)
        
                    #now we loop through the 12 months and overwrite the old values with summations over all occurrences
                    #    of a given month, and then we replace the index with text values Jan, Feb, etc.
                    for m in bill_data_totals.index:
                        i = bill_data_totals['Month Integer'][m]
                        if i in [j.month for j in bill_data.index]:
                            bill_data_totals[cost][m] = bill_data['Cost (act)'][[x.month==i for x in bill_data.index]].sum()
                            bill_data_totals[cost_per_day][m] = bill_data['Cost (act)'][[x.month==i for x in bill_data.index]].sum() / Decimal(0.0 + bill_data['Days'][[x.month==i for x in bill_data.index]].sum())
                            bill_data_totals[cost_per_sf][m] = bill_data['Cost (act)'][[x.month==i for x in bill_data.index]].sum() / self.square_footage
                            bill_data_totals[consumption][m] = bill_data['Consumption (act)'][[x.month==i for x in bill_data.index]].sum()
                            bill_data_totals[consumption_per_day][m] = bill_data['Consumption (act)'][[x.month==i for x in bill_data.index]].sum() / Decimal(0.0 + bill_data['Days'][[x.month==i for x in bill_data.index]].sum())
                            bill_data_totals[consumption_per_sf][m] = bill_data['Consumption (act)'][[x.month==i for x in bill_data.index]].sum() / self.square_footage
                            bill_data_totals[cost_per_consumption][m] = bill_data['Cost (act)'][[x.month==i for x in bill_data.index]].sum() / bill_data['Consumption (act)'][[x.month==i for x in bill_data.index]].sum()
                        else:
                            bill_data_totals[cost][m] = Decimal(NaN)
                            bill_data_totals[cost_per_day][m] = Decimal(NaN)
                            bill_data_totals[cost_per_sf][m] = Decimal(NaN)
                            bill_data_totals[consumption][m] = Decimal(NaN)
                            bill_data_totals[consumption_per_day][m] = Decimal(NaN)
                            bill_data_totals[consumption_per_sf][m] = Decimal(NaN)
                            bill_data_totals[cost_per_consumption][m] = Decimal(NaN)
                    bill_data_totals = bill_data_totals.sort(columns='Month Integer')
                    bill_data_totals.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', 'Annual']
        
                    #now we add the Annual row, which will be a column if and when we transpose
                    bill_data_totals[cost]['Annual'] =                  bill_data['Cost (act)'].sum()
                    bill_data_totals[cost_per_day]['Annual'] =          bill_data['Cost (act)'].sum() / Decimal(0.0 + bill_data['Days'].sum())
                    bill_data_totals[cost_per_sf]['Annual'] =           bill_data['Cost (act)'].sum() / self.square_footage
                    bill_data_totals[consumption]['Annual'] =           bill_data['Consumption (act)'].sum()
                    bill_data_totals[consumption_per_day]['Annual'] =   bill_data['Consumption (act)'].sum() / Decimal(0.0 + bill_data['Days'].sum())
                    bill_data_totals[consumption_per_sf]['Annual'] =    bill_data['Consumption (act)'].sum() / self.square_footage
                    bill_data_totals[cost_per_consumption]['Annual'] =  bill_data['Cost (act)'].sum() / bill_data['Consumption (act)'].sum()
                    
                    #no longer needed once we've sorted
                    bill_data_totals = bill_data_totals.drop(['Month Integer'],1)
                
                    #totals table only has values as opposed to ratios, so we pull relevant columns and set format
                    totals_table_df = bill_data_totals[[cost,consumption]]
                    totals_column_dict = {cost: lambda x: '${:,.2f}'.format(x),
                                          consumption: lambda x: '{:,.0f}'.format(x)}
                    totals_table = get_df_as_table_with_formats(df = totals_table_df,
                                                                columndict = totals_column_dict,
                                                                index_name = 'Metric',
                                                                transpose_bool = True)
                
                    #ratios table only has ratios as opposed to totals, so we pull relevant columns and set format
                    ratios_table_df = bill_data_totals[[cost_per_day,cost_per_sf,consumption_per_day,consumption_per_sf,cost_per_consumption]]
                    ratios_column_dict = {cost_per_day: lambda x: '${:,.2f}'.format(x),
                                          cost_per_sf: lambda x: '${:,.2f}'.format(x),
                                          consumption_per_day: lambda x: '{:,.0f}'.format(x),
                                          consumption_per_sf: lambda x: '{:,.1f}'.format(x),
                                          cost_per_consumption: lambda x: '${:,.2f}'.format(x)}
                    ratios_table = get_df_as_table_with_formats(df = ratios_table_df,
                                                                columndict = ratios_column_dict,
                                                                index_name = 'Metric',
                                                                transpose_bool = True)
                    meter_dict[utype]['totals'] = totals_table
                    meter_dict[utype]['ratios'] = ratios_table
                    
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
                                  meter_dict[utype]['totals'],
                                  meter_dict[utype]['ratios']])
                
                
                if len(meter_data) < 1:
                    meter_data = None
                else:
                    pass #if necessary, weed out empty tables here
                
                #getting pie chart data; cost data includes all Meters; kBtu data excludes domestic water Meters
                pie_cost_by_meter =     [['Meter','Cost']]
                pie_cost_by_type =      [['Utility Type','Cost']]
                pie_kBtu_by_meter =     [['Meter','kBtu']]
                pie_kBtu_by_type =      [['Utility Type','kBtu']]
                
                #for breakdown by Meter, cycle through all Meters and exclude domestic water from kBtu calcs
                for meter in self.meters.all():
                    cost_sum = Monthling.objects.filter(monther=meter.monther_set.get(name='BILLx')).filter(when__gte=month_first.to_timestamp(how='S').tz_localize(tz=UTC)).filter(when__lte=month_last.to_timestamp(how='E').tz_localize(tz=UTC)).aggregate(Sum('act_cost'))['act_cost__sum']
                    if cost_sum is None or np.isnan(float(cost_sum)): cost_sum = Decimal('0.0') #pulling directly from db may return None, whereas df's return zeros
                    pie_cost_by_meter.append([str(meter.name) + ' - ' + str(meter.utility_type), float(cost_sum)])
                    if meter.utility_type != 'domestic water':
                        kBtu_sum = Monthling.objects.filter(monther=meter.monther_set.get(name='BILLx')).filter(when__gte=month_first.to_timestamp(how='S').tz_localize(tz=UTC)).filter(when__lte=month_last.to_timestamp(how='E').tz_localize(tz=UTC)).aggregate(Sum('act_kBtu_consumption'))['act_kBtu_consumption__sum']
                        if kBtu_sum is None or np.isnan(float(kBtu_sum)): kBtu_sum = Decimal('0.0') #pulling directly from db may return None, whereas df's return zeros
                        pie_kBtu_by_meter.append([str(meter.name) + ' - ' + str(meter.utility_type), float(kBtu_sum)])
                
                #for breakdown by utility type, cycle through all utility groups and exclude domestic water from kBtu calcs
                for utype in meter_dict.keys():
                    if utype != 'Total Space Energy':
                        pie_cost_by_type.append([utype, float(meter_dict[utype]['df']['Cost (act)'].sum())])
                        if utype != 'domestic water':
                            pie_kBtu_by_type.append([utype, float(meter_dict[utype]['df']['kBtu Consumption (act)'].sum())])
                pie_data = [[pie_cost_by_meter, pie_cost_by_type, pie_kBtu_by_meter, pie_kBtu_by_type]]
                result = [meter_data, pie_data]            
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='Space %s failed on get_space_view_meter_data function, returning None.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            result = None
        return result
    def __unicode__(self):
        return self.name
    def get_all_events(self, reverse_boolean):
        b = [self.messages.filter(message_type='Event').order_by('-when')]
        e = [x.messages.filter(message_type='Event').order_by('-when') for x in self.equipment_set.all()]
        m = [x.messages.filter(message_type='Event').order_by('-when') for x in self.meters.all()]
        f = [x.messages.filter(message_type='Event').order_by('-when') for x in [self.building]]
        layered_message_list = [b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_alerts(self, reverse_boolean):
        b = [self.messages.filter(message_type='Alert').order_by('-when')]
        e = [x.messages.filter(message_type='Alert').order_by('-when') for x in self.equipment_set.all()]
        m = [x.messages.filter(message_type='Alert').order_by('-when') for x in self.meters.all()]
        f = [x.messages.filter(message_type='Alert').order_by('-when') for x in [self.building]]
        layered_message_list = [b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_messages(self, reverse_boolean):
        b = [self.messages.all()]
        e = [x.messages.all() for x in self.equipment_set.all()]
        m = [x.messages.all() for x in self.meters.all()]
        f = [x.messages.all() for x in [self.building]]
        layered_message_list = [b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def account_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(self.building.account.id,)), self.building.account.name)
    account_name_for_admin.allow_tags = True
    account_name_for_admin.short_description = 'Account'
    def building_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(self.building.id,)), self.building.name)
    building_name_for_admin.allow_tags = True
    building_name_for_admin.short_description = 'Building'
    def connected_equipments_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
    connected_equipments_for_admin.allow_tags = True
    connected_equipments_for_admin.short_description = 'Connected Equipments'
    def save(self, *args, **kwargs):
        if self.id is None:
            super(Space, self).save(*args, **kwargs)
            tnow = timezone.now()
            m = Message(when = tnow,
                        message_type = 'Model Info',
                        subject = 'Model created.',
                        comment = 'This Space was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
            s = Reader(name='SOCCo',help_text='space occupancy observed by local sensors',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='SOCCp',help_text='space occupancy provided by remote source',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
            s = Reader(name='SOCCc',help_text='space occupancy calculated by models',expected_min=Decimal(0.0))
            s.save()
            self.readers.add(s)
        super(Space, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'
