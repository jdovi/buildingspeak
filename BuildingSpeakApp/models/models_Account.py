import logging
import pandas as pd
from pytz import UTC
from numpy import NaN
from django.db import models
from django.utils import timezone
from django.core import urlresolvers
from decimal import Decimal
from datetime import timedelta
from operator import attrgetter
from storages.backends.s3boto import S3BotoStorage
from django.contrib.auth.models import User
from django.db.models import Q, Sum

from models_functions import *
from models_Message import Message
from models_monthlies import Monthling
from models_Space import Space
from models_Meter import Meter

logger = logging.getLogger(__name__)

class Account(models.Model):
    """
    Customer Account model.
    """
    
    #: Name of Account as str.
    name = models.CharField(max_length=200)
    #: Type of Account as str. Options: Commercial, Industrial, Residential.
    account_type = models.CharField(blank=True, max_length=200,
                                    choices=[('Commercial', 'Commercial'),
                                             ('Industrial', 'Industrial'),
                                             ('Residential', 'Residential')])
    
    #relationships
    #: ManyToMany relationship to Message.
    messages = models.ManyToManyField('Message', blank=True)
    #: ManyToMany relationship to User.
    users = models.ManyToManyField(User, blank=True)
    #: ManyToMany relationship to Reader.
    readers = models.ManyToManyField('Reader', blank=True)
    #: ManyToMany relationship to OperatingSchedule.
    schedules = models.ManyToManyField('OperatingSchedule', blank=True)

    
    #file-related attributes
    #: File: Link to file containing observed Account data.
    observed_file = models.FileField(null=True, blank=True, upload_to=data_file_path_account, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing observed account data')
    #: Boolean: Track an observed data file for this Account? Default: False.
    observed_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track an observed data file for this account?')
    #: Int: Number of rows before data header row in observed data file (will be skipped when reading data).
    observed_file_skiprows = models.IntegerField(null=True, blank=True, help_text='number of rows before data header row (will be skipped when reading data)')
    #: Int: Column number of time stamp data to use for indexing observed data file.
    observed_file_column_for_indexing = models.IntegerField(null=True, blank=True, help_text='column number of time stamp data to use for indexing')
    #: Str: Time zone of observed data file, compatible with pytz module.  Default: US/Eastern.
    observed_file_time_zone = models.CharField(blank=True, max_length=200,
                    help_text='time zone compatible with pytz module, default=US/Eastern',
                    default='US/Eastern')
    #: Decimal: GMT/UTC offset as decimal number used to adjust hour values read in from observed data file. Default: -5.
    observed_file_GMT_offset = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2,
                    help_text='GMT/UTC offset as decimal number used to adjust hour values read in from data file',
                    default=Decimal(-5))
    #: Boolean: Dates in observed data file are always already adjusted for DST? Default: False.
    observed_file_adjusts_for_DST = models.BooleanField(blank=True,
                    help_text='dates in data file are always already adjusted for DST?',
                    default=False)

    #: File: Link to file containing provided Account data.
    provided_file = models.FileField(null=True, blank=True, upload_to=data_file_path_account, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing provided account data')
    #: Boolean: Track an provided data file for this Account? Default: False.
    provided_file_track = models.BooleanField(blank=True, default=False,
                    help_text='track a provided data file for this account?')
    #: Int: Number of rows before data header row in provided data file (will be skipped when reading data).
    provided_file_skiprows = models.IntegerField(null=True, blank=True, help_text='number of rows before data header row (will be skipped when reading data)')
    #: Int: Column number of time stamp data to use for indexing provided data file.
    provided_file_column_for_indexing = models.IntegerField(null=True, blank=True, help_text='column number of time stamp data to use for indexing')
    #: Str: Time zone of provided data file, compatible with pytz module.  Default: US/Eastern.
    provided_file_time_zone = models.CharField(blank=True, max_length=200,
                    help_text='time zone compatible with pytz module, default=US/Eastern',
                    default='US/Eastern')
    #: Decimal: GMT/UTC offset as decimal number used to adjust hour values read in from provided data file. Default: -5.
    provided_file_GMT_offset = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2,
                    help_text='GMT/UTC offset as decimal number used to adjust hour values read in from data file',
                    default=Decimal(-5))
    #: Boolean: Dates in provided data file are always already adjusted for DST? Default: False.
    provided_file_adjusts_for_DST = models.BooleanField(blank=True,
                    help_text='dates in data file are always already adjusted for DST?',
                    default=False)
    #: File: Link to file containing Account image.
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_account, 
                    storage=S3BotoStorage(location='user_data_files'),
                    help_text='link to file containing account image')
    
    #single value attributes
    #: Str: Street address of Account.
    street_address = models.CharField(blank=True, max_length=200)
    #: Str: City of Account.
    city = models.CharField(blank=True, max_length=200)
    #: Str: State of Account.
    state = models.CharField(blank=True, max_length=2)
    #: Str: Zip code for Account.
    zip_code = models.CharField(blank=True, max_length=10)
    #: DateTime: Date Account was created. 
    launch_date = models.DateTimeField(null=True, blank=True)

    #: Str: Account contact first name.
    first_name = models.CharField(blank=True, max_length=200)
    #: Str: Account contact last name.
    last_name = models.CharField(blank=True, max_length=200)
    #: Str: Account contact title.
    title = models.CharField(blank=True, max_length=200)
    #: Email: Account contact email address.
    email = models.EmailField(blank=True, max_length=75)
    #: Str: Account contact phone number.
    phone = models.CharField(blank=True, max_length=20)

    #: Str: Account status.  Options: Active, Closed, Delinquent, Inactive.
    status = models.CharField(blank=True, max_length=200,
                              choices=[('Active', 'Active'),
                                       ('Closed', 'Closed'),
                                       ('Delinquent', 'Delinquent'),
                                       ('Inactive', 'Inactive')])
    #: Decimal: Total monthly Account payment amount (USD).
    monthly_payment = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2,
                                          help_text='total monthly payment due')
    #: Str: Stripe's customer.id for this Account.
    stripe_customer_id = models.CharField(blank=True, max_length=100)
    
    #functions
    def get_account_view_motion_table_buildings(self, acct_meter_data):
        """
        No inputs. Returns table for motion chart on
        Account's detail view, using most recent 10
        years of meter data.
        
        :returns: List of lists with the following
        columns: Building Name, Date, Cost, kBtu, CDD,
        HDD, Cost/SF, kBtu/SF, Cost/kBtu, Building Type.
        """
        t0 = timezone.now()
        month_curr = pd.Period(timezone.now(), freq='M')
        mistr = (month_curr-120).strftime('%m/%Y')
        mfstr = month_curr.strftime('%m/%Y')
        
        result = [['Building Name','Date','Cost (act)','kBtu Consumption (act)','CDD (consumption)','HDD (consumption)','Cost/SF','kBtu/SF','Cost/kBtu','Building Type']]
        
        for bldg in self.building_set.all():
            bldg_meter_data = [m for m in acct_meter_data if bldg.id in m[6]]
            bldg_df = convert_units_sum_meters(
                                        'other',
                                        'kBtuh,kBtu',
                                        bldg_meter_data,
                                        [6, bldg.id],
                                        first_month = mistr, 
                                        last_month = mfstr)
            if bldg_df is not None:
                bldg_df['Cost/SF'] = bldg_df['Cost (act)']/bldg.square_footage
                bldg_df['kBtu/SF'] = bldg_df['kBtu Consumption (act)']/bldg.square_footage
                bldg_df['Cost/kBtu'] = bldg_df['Cost (act)']/bldg_df['kBtu Consumption (act)'].replace(to_replace = 0, value = Decimal(NaN)) #need to avoid DIV/0 error
                bldg_df[['Cost/SF',
                         'kBtu/SF',
                         'Cost/kBtu']] = bldg_df[['Cost/SF',
                                                  'kBtu/SF',
                                                  'Cost/kBtu']].applymap(nan2zero)
                bldg_table = get_df_motion_table(bldg_df,
                                                  ['Building', str(bldg.name)],
                                                  lambda x:(x.to_timestamp(how='S')+timedelta(hours=11)).tz_localize(tz=UTC).to_datetime().isoformat(),
                                                  ['Cost (act)','kBtu Consumption (act)','CDD (consumption)','HDD (consumption)','Cost/SF','kBtu/SF','Cost/kBtu','Building Type'],
                                                  {'Building Type': str(bldg.building_type)})
                for i in bldg_table[1:]:
                    result.append(i)
        t1 = timezone.now()
        logger.debug('get_account_view_motion_table_buildings %s' % '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0))
        return result
    def get_account_view_motion_table_spaces(self, acct_meter_data):
        """
        No inputs. Returns table for motion chart on
        Account's detail view, using most recent 10
        years of meter data.
        
        :returns: List of lists with the following
        columns: Space Name, Date, Cost, kBtu, CDD,
        HDD, Cost/SF, kBtu/SF, Cost/kBtu, Space Type,
        Building Name.
        """
        t0 = timezone.now()
        month_curr = pd.Period(timezone.now(), freq='M')
        mistr = (month_curr-120).strftime('%m/%Y')
        mfstr = month_curr.strftime('%m/%Y')
        
        result = [['Space Name','Date','Cost (act)','kBtu Consumption (act)','CDD (consumption)','HDD (consumption)','Cost/SF','kBtu/SF','Cost/kBtu','Space Type','Building']]
        space_set = Space.objects.filter(Q(building__account=self) | Q(meters__account=self)).distinct().order_by('name')
        
        for space in space_set:
            space_meter_data = [m for m in acct_meter_data if space.id in m[7]]
            space_df = convert_units_sum_meters(
                                        'other',
                                        'kBtuh,kBtu',
                                        space_meter_data,
                                        [7, space.id],
                                        first_month = mistr, 
                                        last_month = mfstr)
            if space_df is not None:
                space_df['Cost/SF'] = space_df['Cost (act)']/space.square_footage
                space_df['kBtu/SF'] = space_df['kBtu Consumption (act)']/space.square_footage
                space_df['Cost/kBtu'] = space_df['Cost (act)']/space_df['kBtu Consumption (act)'].replace(to_replace = 0, value = Decimal(NaN)) #need to avoid DIV/0 error
                space_df[['Cost/SF',
                          'kBtu/SF',
                          'Cost/kBtu']] = space_df[['Cost/SF',
                                                    'kBtu/SF',
                                                    'Cost/kBtu']].applymap(nan2zero)
                space_table = get_df_motion_table(space_df,
                                                  ['Space', str(space.name)],
                                                  lambda x:(x.to_timestamp(how='S')+timedelta(hours=11)).tz_localize(tz=UTC).to_datetime().isoformat(),
                                                  ['Cost (act)','kBtu Consumption (act)','CDD (consumption)','HDD (consumption)','Cost/SF','kBtu/SF','Cost/kBtu','Space Type','Building'],
                                                  {'Space Type': str(space.space_type),'Building': str(space.building.name)})
                for i in space_table[1:]:
                    result.append(i)
        t1 = timezone.now()
        logger.debug('get_account_view_motion_table_spaces %s' % '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0))
        return result
    def get_account_view_motion_table_fuels(self, acct_meter_data):
        """
        No inputs. Returns table for motion chart on
        Account's detail view, using most recent 10
        years of meter data.
        
        :returns: List of lists with the following
        columns: Utility Type, Date, Cost, kBtu, CDD,
        HDD, Cost/SF, kBtu/SF, Cost/kBtu.
        """
        t0 = timezone.now()
        month_curr = pd.Period(timezone.now(), freq='M')
        mistr = (month_curr-120).strftime('%m/%Y')
        mfstr = month_curr.strftime('%m/%Y')
        total_SF = self.building_set.all().aggregate(Sum('square_footage'))['square_footage__sum']
        
        utility_groups = []
        utility_groups.extend(sorted(set([str(x.utility_type) for x in self.meter_set.all()])))
        result = [['Utility Type','Date','Cost (act)','kBtu Consumption (act)','CDD (consumption)','HDD (consumption)','Cost/SF','kBtu/SF','Cost/kBtu']]

        for utype in utility_groups:
            utype_df = convert_units_sum_meters(
                                        utype,
                                        get_default_units(utype),
                                        [m for m in acct_meter_data if m[0] == utype],
                                        None,
                                        first_month = mistr, 
                                        last_month = mfstr)
            if utype_df is not None:
                utype_df['Cost/SF'] = utype_df['Cost (act)']/total_SF
                utype_df['kBtu/SF'] = utype_df['kBtu Consumption (act)']/total_SF
                utype_df['Cost/kBtu'] = utype_df['Cost (act)']/utype_df['kBtu Consumption (act)'].replace(to_replace = 0, value = Decimal(NaN)) #need to avoid DIV/0 error
                utype_df[['Cost/SF',
                          'kBtu/SF',
                          'Cost/kBtu']] = utype_df[['Cost/SF',
                                                    'kBtu/SF',
                                                    'Cost/kBtu']].applymap(nan2zero)
                utype_table = get_df_motion_table(utype_df,
                                                  ['Utility Type', str(utype)],
                                                  lambda x:(x.to_timestamp(how='S')+timedelta(hours=11)).tz_localize(tz=UTC).to_datetime().isoformat(),
                                                  ['Cost (act)','kBtu Consumption (act)','CDD (consumption)','HDD (consumption)','Cost/SF','kBtu/SF','Cost/kBtu'])
                for i in utype_table[1:]:
                    result.append(i)
        t1 = timezone.now()
        logger.debug('get_account_view_motion_table_fuels %s' % '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0))
        return result
    def get_account_view_motion_table_meters(self, acct_meter_data):
        """
        No inputs. Returns table for motion chart on
        Account's detail view.  List of lists
        with the following columns: MeterName,
        Date, Cost, kBtu, CDD, HDD, UtilityType.
        """
        t0 = timezone.now()
        result = [['Meter','Date','Cost (act)','kBtu Consumption (act)','CDD (consumption)','HDD (consumption)','Utility Type']]
        for meter in acct_meter_data:
            meter_table = get_meter_view_motion_table(name = str(meter[4]), bill_data = meter[2])
            if meter_table is not None and len(meter_table) > 1:
                for i in meter_table[1:]:
                    i.append(str(meter[0]))
                    result.append(i)
        t1 = timezone.now()
        logger.debug('get_account_view_motion_table_meters %s' % '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0))
        return result
    def get_account_view_five_year_data(self, acct_meter_data):
        """No inputs.
        
        Returns meter data for Account's stacked
        5yr bar charts."""
        t0 = timezone.now()
        #if there are no meters, skip all meter data calcs
        try:
            month_curr = pd.Period(timezone.now(), freq='M')
            year_curr = month_curr.year
            mi = pd.Period(year = year_curr-3, month = 1, freq = 'M')
            mf = pd.Period(year = year_curr+1, month = 12, freq = 'M')
            mistr = mi.strftime('%m/%Y')
            mfstr = mf.strftime('%m/%Y')
            total_SF = self.building_set.all().aggregate(Sum('square_footage'))['square_footage__sum']
            
            if len(acct_meter_data) < 1:
                five_year_data = None
            else:
                #five year stacked_data is what will be passed to the template
                five_year_data = []
                utility_groups = ['Account Total']
                utility_types = sorted(set([str(x[0]) for x in acct_meter_data]))
                utility_groups.extend(utility_types)
                
                #meter_dict holds all info and dataframes for each utility group, starting with Total
                #note that water is included for Cost, so Cons/PD can never be used here but kBtu/kBtuh can
                meter_dict = {'Account Total': {'name': 'Account Total',
                                                        'costu': 'USD',
                                                        'consu': 'kBtu',
                                                        'pdu': 'kBtuh',
                                                        'df': convert_units_sum_meters(
                                                                'other', 
                                                                'kBtuh,kBtu', 
                                                                acct_meter_data,
                                                                None,
                                                                first_month=mistr, 
                                                                last_month=mfstr )
                                                        } }
                
                #cycle through all utility types present in this account, get info and dataframes
                for utype in utility_types:
                    utype = str(utype)
                    meter_dict[utype] = {}
                    meter_dict[utype]['name'] = utype
                    meter_dict[utype]['costu'] = 'USD'
                    meter_dict[utype]['consu'] = get_default_units(utype).split(',')[1]
                    meter_dict[utype]['pdu'] = get_default_units(utype).split(',')[0]
                    meter_dict[utype]['df'] = convert_units_sum_meters(
                                                utype,
                                                get_default_units(utype),
                                                [m for m in acct_meter_data if m[0] == utype],
                                                None,
                                                first_month=mistr, 
                                                last_month=mfstr)
                
                #remove all utility types for which no data was found (returned df is None)
                temp = [meter_dict.__delitem__(x) for x in meter_dict.keys() if meter_dict[x]['df'] is None]

                #now that dataframes are available, create data tables for each utility type, inc. Total
                for utype in meter_dict.keys():
                    five_years = pd.DataFrame(meter_dict[utype]['df'], index = pd.period_range(start = mi, end = mf, freq = 'M'))
                    five_years = five_years.sort_index()
                    
                    for i in range(len(five_years)-1,-1,-1):
                        if (not(decimal_isnan(five_years['Cost (act)'][i])) and
                            five_years['Cost (act)'][i] != Decimal(0) ):
                            print utype,i,five_years.index[i],five_years['Cost (act)'][i]
                            last_act_month_cost = five_years.index[i]
                            first_calc_month_cost = last_act_month_cost + 1
                            break
                    for i in range(len(five_years)-1,-1,-1):
                        if not(decimal_isnan(five_years['Consumption (act)'][i])):
                            last_act_month_cons = five_years.index[i]
                            first_calc_month_cons = last_act_month_cons + 1
                            break
                    
                    five_years = five_years[['Cost (act)','Cost (exp)','Consumption (act)','Consumption (exp)',
                                             'CDD (consumption)','HDD (consumption)']].applymap(nan2zero)
                    five_years = five_years[['Cost (act)','Cost (exp)','Consumption (act)','Consumption (exp)',
                                             'CDD (consumption)','HDD (consumption)']].applymap(float)
                    
                    #cost table
                    five_year_table_cost = [['Year','Cost (act)','Cost (exp)','CDD (consumption)','HDD (consumption)']]
                    five_year_table_cost.append([str(five_years.index[0].year),
                                            five_years['Cost (act)'][0:12].sum(),
                                            0,
                                            five_years['CDD (consumption)'][0:12].sum(),
                                            five_years['HDD (consumption)'][0:12].sum()
                                            ])
                    five_year_table_cost.append([str(five_years.index[12].year),
                                            five_years['Cost (act)'][12:24].sum(),
                                            0,
                                            five_years['CDD (consumption)'][12:24].sum(),
                                            five_years['HDD (consumption)'][12:24].sum()
                                            ])
                    five_year_table_cost.append([str(five_years.index[24].year),
                                            five_years['Cost (act)'][24:36].sum(),
                                            0,
                                            five_years['CDD (consumption)'][24:36].sum(),
                                            five_years['HDD (consumption)'][24:36].sum()
                                            ])
                    five_year_table_cost.append([str(five_years.index[36].year),
                                            five_years['Cost (act)'][five_years.index[36]:last_act_month_cost].sum(),
                                            five_years['Cost (exp)'][first_calc_month_cost:five_years.index[47]].sum(),
                                            five_years['CDD (consumption)'][36:48].sum(),
                                            five_years['HDD (consumption)'][36:48].sum()
                                            ])
                    five_year_table_cost.append([str(five_years.index[48].year),
                                            0,
                                            five_years['Cost (exp)'][48:60].sum(),
                                            five_years['CDD (consumption)'][48:60].sum(),
                                            five_years['HDD (consumption)'][48:60].sum()
                                            ])
                    
                    #cost/SF table
                    five_year_table_costSF = [['Year','Cost (act)','Cost (exp)','CDD (consumption)','HDD (consumption)']]
                    five_year_table_costSF.append([str(five_years.index[0].year),
                                            five_years['Cost (act)'][0:12].sum()/total_SF,
                                            0,
                                            five_years['CDD (consumption)'][0:12].sum(),
                                            five_years['HDD (consumption)'][0:12].sum()
                                            ])
                    five_year_table_costSF.append([str(five_years.index[12].year),
                                            five_years['Cost (act)'][12:24].sum()/total_SF,
                                            0,
                                            five_years['CDD (consumption)'][12:24].sum(),
                                            five_years['HDD (consumption)'][12:24].sum()
                                            ])
                    five_year_table_costSF.append([str(five_years.index[24].year),
                                            five_years['Cost (act)'][24:36].sum()/total_SF,
                                            0,
                                            five_years['CDD (consumption)'][24:36].sum(),
                                            five_years['HDD (consumption)'][24:36].sum()
                                            ])
                    five_year_table_costSF.append([str(five_years.index[36].year),
                                            five_years['Cost (act)'][five_years.index[36]:last_act_month_cost].sum()/total_SF,
                                            five_years['Cost (exp)'][first_calc_month_cost:five_years.index[47]].sum()/total_SF,
                                            five_years['CDD (consumption)'][36:48].sum(),
                                            five_years['HDD (consumption)'][36:48].sum()
                                            ])
                    five_year_table_costSF.append([str(five_years.index[48].year),
                                            0,
                                            five_years['Cost (exp)'][48:60].sum()/total_SF,
                                            five_years['CDD (consumption)'][48:60].sum(),
                                            five_years['HDD (consumption)'][48:60].sum()
                                            ])
                    
                    #consumption table
                    five_year_table_cons = [['Year','Consumption (act)','Consumption (exp)','CDD (consumption)','HDD (consumption)']]
                    five_year_table_cons.append([str(five_years.index[0].year),
                                            five_years['Consumption (act)'][0:12].sum(),
                                            0,
                                            five_years['CDD (consumption)'][0:12].sum(),
                                            five_years['HDD (consumption)'][0:12].sum()
                                            ])
                    five_year_table_cons.append([str(five_years.index[12].year),
                                            five_years['Consumption (act)'][12:24].sum(),
                                            0,
                                            five_years['CDD (consumption)'][12:24].sum(),
                                            five_years['HDD (consumption)'][12:24].sum()
                                            ])
                    five_year_table_cons.append([str(five_years.index[24].year),
                                            five_years['Consumption (act)'][24:36].sum(),
                                            0,
                                            five_years['CDD (consumption)'][24:36].sum(),
                                            five_years['HDD (consumption)'][24:36].sum()
                                            ])
                    five_year_table_cons.append([str(five_years.index[36].year),
                                            five_years['Consumption (act)'][five_years.index[36]:last_act_month_cons].sum(),
                                            five_years['Consumption (exp)'][first_calc_month_cons:five_years.index[47]].sum(),
                                            five_years['CDD (consumption)'][36:48].sum(),
                                            five_years['HDD (consumption)'][36:48].sum()
                                            ])
                    five_year_table_cons.append([str(five_years.index[48].year),
                                            0,
                                            five_years['Consumption (exp)'][48:60].sum(),
                                            five_years['CDD (consumption)'][48:60].sum(),
                                            five_years['HDD (consumption)'][48:60].sum()
                                            ])

                    #consumption/SF table
                    five_year_table_consSF = [['Year','Consumption (act)','Consumption (exp)','CDD (consumption)','HDD (consumption)']]
                    five_year_table_consSF.append([str(five_years.index[0].year),
                                            five_years['Consumption (act)'][0:12].sum()/total_SF,
                                            0,
                                            five_years['CDD (consumption)'][0:12].sum(),
                                            five_years['HDD (consumption)'][0:12].sum()
                                            ])
                    five_year_table_consSF.append([str(five_years.index[12].year),
                                            five_years['Consumption (act)'][12:24].sum()/total_SF,
                                            0,
                                            five_years['CDD (consumption)'][12:24].sum(),
                                            five_years['HDD (consumption)'][12:24].sum()
                                            ])
                    five_year_table_consSF.append([str(five_years.index[24].year),
                                            five_years['Consumption (act)'][24:36].sum()/total_SF,
                                            0,
                                            five_years['CDD (consumption)'][24:36].sum(),
                                            five_years['HDD (consumption)'][24:36].sum()
                                            ])
                    five_year_table_consSF.append([str(five_years.index[36].year),
                                            five_years['Consumption (act)'][five_years.index[36]:last_act_month_cons].sum()/total_SF,
                                            five_years['Consumption (exp)'][first_calc_month_cons:five_years.index[47]].sum()/total_SF,
                                            five_years['CDD (consumption)'][36:48].sum(),
                                            five_years['HDD (consumption)'][36:48].sum()
                                            ])
                    five_year_table_consSF.append([str(five_years.index[48].year),
                                            0,
                                            five_years['Consumption (exp)'][48:60].sum()/total_SF,
                                            five_years['CDD (consumption)'][48:60].sum(),
                                            five_years['HDD (consumption)'][48:60].sum()
                                            ])
                    
                    five_year_data.append(
                                 [meter_dict[utype]['name'],
                                  meter_dict[utype]['costu'],
                                  meter_dict[utype]['consu'],
                                  meter_dict[utype]['pdu'],
                                  five_year_table_cost,
                                  five_year_table_costSF,
                                  five_year_table_cons,
                                  five_year_table_consSF])

                if len(five_year_data) < 1:
                    five_year_data = None
                else:
                    pass #if necessary, weed out empty tables here
                
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='Account %s failed on get_account_view_five_year_data function, returning None.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            five_year_data = None
        t1 = timezone.now()
        logger.debug('get_account_view_five_year_data %s' % '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0))
        return five_year_data

    def get_account_view_meter_data(self, month_first, month_last, acct_meter_data):
        """
        Returns tables of summed meter data for a given date range.
        
        :argument month_first: The first desired month.
        :type month_first: Period(freq='M')
        :argument month_last: The last desired month.
        :type month_last: Period(freq='M')
        :returns: Meter data for Account's views in a list: [meter_data, pie_data].
        
        """
        t0 = timezone.now()
        #if there are no meters, skip all meter data calcs
        try:
            first_month = month_first.strftime('%m/%Y')
            last_month = month_last.strftime('%m/%Y')
            
            total_SF = self.building_set.all().aggregate(Sum('square_footage'))['square_footage__sum']
            
            if len(acct_meter_data) < 1:
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
                utility_groups = ['Account Total']
                utility_types = sorted(set([str(x[0]) for x in acct_meter_data]))
                utility_groups.extend(utility_types)
                
                #meter_dict holds all info and dataframes for each utility group, starting with Total
                #note that water is included for Cost, so Cons/PD can never be used here but kBtu/kBtuh can
                meter_dict = {'Account Total': {'name': 'Account Total',
                                                        'costu': 'USD',
                                                        'consu': 'kBtu',
                                                        'pdu': 'kBtuh',
                                                        'df': convert_units_sum_meters(
                                                                'other', 
                                                                'kBtuh,kBtu', 
                                                                acct_meter_data,
                                                                None,
                                                                first_month=first_month, 
                                                                last_month=last_month )
                                                        } }
                
                #cycle through all utility types present in this account, get info and dataframes
                for utype in utility_types:
                    utype = str(utype)
                    meter_dict[utype] = {}
                    meter_dict[utype]['name'] = utype
                    meter_dict[utype]['costu'] = 'USD'
                    meter_dict[utype]['consu'] = get_default_units(utype).split(',')[1]
                    meter_dict[utype]['pdu'] = get_default_units(utype).split(',')[0]
                    meter_dict[utype]['df'] = convert_units_sum_meters(
                                                utype,
                                                get_default_units(utype),
                                                [m for m in acct_meter_data if m[0] == utype],
                                                None,
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
                    bill_data[cost_per_sf] = bill_data['Cost (act)'] / total_SF
                    bill_data[consumption] = bill_data['Consumption (act)']
                    bill_data[consumption_per_day] = bill_data['Consumption (act)'] / bill_data['Days']
                    bill_data[consumption_per_sf] = bill_data['Consumption (act)'] / total_SF
                    bill_data[cost_per_consumption] = bill_data['Cost (act)'] / bill_data['Consumption (act)'].replace(to_replace = 0, value = Decimal(NaN)) #need to avoid DIV/0 error
                    
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
                            cost_months = [x.month==i and not(decimal_isnan(bill_data['Cost (act)'][x])) for x in bill_data.index]
                            cons_months = [x.month==i and not(decimal_isnan(bill_data['Consumption (act)'][x])) for x in bill_data.index]
                            
                            sum_cons =      bill_data['Consumption (act)'][cons_months].sum()
                            sum_days_cost = Decimal(float(bill_data['Days'][cost_months].sum()))
                            sum_days_cons = Decimal(float(bill_data['Days'][cons_months].sum()))
                            
                            if sum_cons ==      Decimal(0.0): sum_cons = Decimal(NaN)
                            if sum_days_cost == Decimal(0.0): sum_days_cost = Decimal(NaN)
                            if sum_days_cons == Decimal(0.0): sum_days_cons = Decimal(NaN)
                            
                            bill_data_totals[cost][m] = bill_data['Cost (act)'][cost_months].sum()
                            bill_data_totals[cost_per_day][m] = bill_data['Cost (act)'][cost_months].sum() / sum_days_cost
                            bill_data_totals[cost_per_sf][m] = bill_data['Cost (act)'][cost_months].sum() / total_SF
                            bill_data_totals[consumption][m] = bill_data['Consumption (act)'][cons_months].sum()
                            bill_data_totals[consumption_per_day][m] = bill_data['Consumption (act)'][cons_months].sum() / sum_days_cons
                            bill_data_totals[consumption_per_sf][m] = bill_data['Consumption (act)'][cons_months].sum() / total_SF
                            bill_data_totals[cost_per_consumption][m] = bill_data['Cost (act)'][cost_months].sum() / sum_cons
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
                    cost_months = [not(decimal_isnan(bill_data['Cost (act)'][x])) for x in bill_data.index]
                    cons_months = [not(decimal_isnan(bill_data['Consumption (act)'][x])) for x in bill_data.index]
                    
                    sum_cons =      bill_data['Consumption (act)'][cons_months].sum()
                    sum_days_cost = Decimal(float(bill_data['Days'][cost_months].sum()))
                    sum_days_cons = Decimal(float(bill_data['Days'][cons_months].sum()))
                    
                    if sum_cons ==      Decimal(0.0): sum_cons = Decimal(NaN)
                    if sum_days_cost == Decimal(0.0): sum_days_cost = Decimal(NaN)
                    if sum_days_cons == Decimal(0.0): sum_days_cons = Decimal(NaN)
                    
                    bill_data_totals[cost]['Annual'] =                  bill_data['Cost (act)'][cost_months].sum()
                    bill_data_totals[cost_per_day]['Annual'] =          bill_data['Cost (act)'][cost_months].sum() / sum_days_cost
                    bill_data_totals[cost_per_sf]['Annual'] =           bill_data['Cost (act)'][cost_months].sum() / total_SF
                    bill_data_totals[consumption]['Annual'] =           bill_data['Consumption (act)'][cons_months].sum()
                    bill_data_totals[consumption_per_day]['Annual'] =   bill_data['Consumption (act)'][cons_months].sum() / sum_days_cons
                    bill_data_totals[consumption_per_sf]['Annual'] =    bill_data['Consumption (act)'][cons_months].sum() / total_SF
                    bill_data_totals[cost_per_consumption]['Annual'] =  bill_data['Cost (act)'][cost_months].sum() / sum_cons
                    
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
                pies_by_meter =         [['Meter','Cost','kBtu','Utility Type']]
                
                #for breakdown by Meter, cycle through all Meters and exclude domestic water from kBtu calcs
                for meter in acct_meter_data:
                    cost_sum = Monthling.objects.filter(monther=Meter.objects.get(id=meter[3]).monther_set.get(name='BILLx')).filter(when__gte=month_first.to_timestamp(how='S').tz_localize(tz=UTC)).filter(when__lte=month_last.to_timestamp(how='E').tz_localize(tz=UTC)).exclude(act_cost=Decimal(NaN)).aggregate(Sum('act_cost'))['act_cost__sum']
                    if cost_sum is None or np.isnan(float(cost_sum)): cost_sum = Decimal('0.0') #pulling directly from db may return None, whereas df's return zeros
                    pie_cost_by_meter.append([str(meter[4]) + ' - ' + str(meter[0]), float(cost_sum)])
                    if meter[0] != 'domestic water':
                        kBtu_sum = Monthling.objects.filter(monther=Meter.objects.get(id=meter[3]).monther_set.get(name='BILLx')).filter(when__gte=month_first.to_timestamp(how='S').tz_localize(tz=UTC)).filter(when__lte=month_last.to_timestamp(how='E').tz_localize(tz=UTC)).exclude(act_kBtu_consumption=Decimal(NaN)).aggregate(Sum('act_kBtu_consumption'))['act_kBtu_consumption__sum']
                        if kBtu_sum is None or np.isnan(float(kBtu_sum)): kBtu_sum = Decimal('0.0') #pulling directly from db may return None, whereas df's return zeros
                        pie_kBtu_by_meter.append([str(meter[4]) + ' - ' + str(meter[0]), float(kBtu_sum)])
                        pies_by_meter.append([str(meter[4]) + ' - ' + str(meter[0]), float(cost_sum), float(kBtu_sum), str(meter[0])])
                
                #for breakdown by utility type, cycle through all utility groups and exclude domestic water from kBtu calcs
                for utype in meter_dict.keys():
                    if utype != 'Account Total':
                        pie_cost_by_type.append([utype, float(meter_dict[utype]['df']['Cost (act)'].sum())])
                        if utype != 'domestic water':
                            pie_kBtu_by_type.append([utype, float(meter_dict[utype]['df']['kBtu Consumption (act)'].sum())])
                pie_data = [[pie_cost_by_meter, pie_cost_by_type, pie_kBtu_by_meter, pie_kBtu_by_type, pies_by_meter]]
                result = [meter_data, pie_data]            
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='Account %s failed on get_account_view_meter_data function, returning None.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            result = None
        t1 = timezone.now()
        logger.debug('get_account_view_meter_data %s' % '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0))
        return result
    def get_all_events(self, reverse_boolean):
        a = [self.messages.filter(message_type='Event')]
        b = [x.messages.filter(message_type='Event') for x in self.building_set.all()]
        e = [x.messages.filter(message_type='Event') for x in self.account_equipments()]
        m = [x.messages.filter(message_type='Event') for x in self.meter_set.all()]
        f_0 = [x.space_set.all() for x in self.building_set.all()]
        f_0 = [item for sublist in f_0 for item in sublist]
        f = [x.messages.filter(message_type='Event') for x in f_0]
        layered_message_list = [a,b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_alerts(self, reverse_boolean):
        a = [self.messages.filter(message_type='Alert')]
        b = [x.messages.filter(message_type='Alert') for x in self.building_set.all()]
        e = [x.messages.filter(message_type='Alert') for x in self.account_equipments()]
        m = [x.messages.filter(message_type='Alert') for x in self.meter_set.all()]
        f_0 = [x.space_set.all() for x in self.building_set.all()]
        f_0 = [item for sublist in f_0 for item in sublist]
        f = [x.messages.filter(message_type='Alert') for x in f_0]
        layered_message_list = [a,b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
    def get_all_messages(self, reverse_boolean):
        a = self.messages.all()
        bldg_set = self.building_set.all()
        b = [x.messages.all() for x in bldg_set]
        e = [x.messages.all() for x in self.account_equipments()]
        m = [x.messages.all() for x in self.meter_set.all()]
        f_0 = [x.space_set.all() for x in bldg_set]
        f_0 = [item for sublist in f_0 for item in sublist]
        f = [x.messages.all() for x in f_0]
        layered_message_list = [a,b,e,m,f]
        flat1 = [item for sublist in layered_message_list for item in sublist]
        flat2 = [item for sublist in flat1 for item in sublist]
        return sorted(flat2, key=attrgetter('when'), reverse=reverse_boolean)
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
                        message_type = 'Model Info',
                        subject = 'Model created.',
                        comment = 'This Account was created on %s.' % tnow)
            m.save()
            self.messages.add(m)
        super(Account, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'
