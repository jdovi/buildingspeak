from numpy import NaN
from django.db import models
from django.utils import timezone
from decimal import Decimal

from models_functions import *
from models_Message import Message
from models_RateSchedules import RateSchedule, RateScheduleRider


class GAPowerPandL(RateSchedule):
    use_input_billing_demand = models.BooleanField(blank=True, default=True,
                    help_text='use input Billing Demand instead of Calculated Billing Demand?')
    basic_service_charge = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='monthly basic service charge',
                              default=Decimal(0.0))
    tax_percentage = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=7,
                              help_text='tax percentage applied to grand total',
                              default=Decimal(0.08))
                              
    tier1 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='tier 1 limit: consumption < (X times billing demand)',
                              default=Decimal(0.0))
    tier1a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 1a limit: X kWh',
                              default=Decimal(0.0))
    tier1b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 1b limit: X kWh',
                              default=Decimal(0.0))
    tier1c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 1c limit: X kWh',
                              default=Decimal(0.0))
    tier1d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 1d limit: X kWh',
                              default=Decimal(0.0))
    
    tier2 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='tier 2 limit: consumption < (X times billing demand)',
                              default=Decimal(0.0))
    tier2a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 2a limit: X kWh (relative to tier 2 limit)',
                              default=Decimal(0.0))
    tier2b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 2b limit: X kWh (relative to tier 2 limit)',
                              default=Decimal(0.0))
    tier2c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 2c limit: X kWh (relative to tier 2 limit)',
                              default=Decimal(0.0))
    tier2d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 2d limit: X kWh (relative to tier 2 limit)',
                              default=Decimal(0.0))

    tier3 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='tier 3 limit: consumption < (X times billing demand)',
                              default=Decimal(0.0))
    tier3a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 3a: first X kWh (relative to tier 3 limit)',
                              default=Decimal(0.0))
    tier3b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 3b: next X kWh (relative to tier 3 limit)',
                              default=Decimal(0.0))
    tier3c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 3c: next X kWh (relative to tier 3 limit)',
                              default=Decimal(0.0))
    tier3d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 3d: over X kWh (relative to tier 3 limit)',
                              default=Decimal(0.0))

    tier4 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='tier 4 limit: consumption < (X times billing demand)',
                              default=Decimal(0.0))
    tier4a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 4a: first X kWh (relative to tier 4 limit)',
                              default=Decimal(0.0))
    tier4b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 4b: next X kWh (relative to tier 4 limit)',
                              default=Decimal(0.0))
    tier4c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 4c: next X kWh (relative to tier 4 limit)',
                              default=Decimal(0.0))
    tier4d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='subtier 4d: over X kWh (relative to tier 4 limit)',
                              default=Decimal(0.0))
    
    rate1a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 1a',
                              default=Decimal(0.0))
    rate1b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 1b',
                              default=Decimal(0.0))
    rate1c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 1c',
                              default=Decimal(0.0))
    rate1d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 1d',
                              default=Decimal(0.0))

    rate2a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 2a',
                              default=Decimal(0.0))
    rate2b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 2b',
                              default=Decimal(0.0))
    rate2c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 2c',
                              default=Decimal(0.0))
    rate2d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 2d',
                              default=Decimal(0.0))

    rate3a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 3a',
                              default=Decimal(0.0))
    rate3b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 3b',
                              default=Decimal(0.0))
    rate3c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 3c',
                              default=Decimal(0.0))
    rate3d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 3d',
                              default=Decimal(0.0))

    rate4a = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 4a',
                              default=Decimal(0.0))
    rate4b = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 4b',
                              default=Decimal(0.0))
    rate4c = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 4c',
                              default=Decimal(0.0))
    rate4d = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kWh for tier 4d',
                              default=Decimal(0.0))

    excess_kW_threshold = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='billing demand over which extra charges apply',
                              default=Decimal(0.0))
    excess_kW_rate = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/kW for excess billing demand',
                              default=Decimal(0.0))
    
    window_minutes = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='minutes window for calculating billing demand',
                              default=Decimal(0.0))
    
    summer_start_month = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='integer for first summer on-peak month (1-12)',
                              default=Decimal(0.0))
    summer_end_month = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='integer for last summer on-peak month (1-12)',
                              default=Decimal(0.0))
    winter_start_month = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='integer for first winter off-peak month (1-12)',
                              default=Decimal(0.0))
    winter_end_month = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='integer for last winter off-peak month (1-12)',
                              default=Decimal(0.0))
    
    billing_demand_sliding_month_window = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='number of previous months to use in calculating billing demand',
                              default=Decimal(0.0))
    summer_summer_threshold = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='% for highest actual demand in previous summer months when calculating summer month billing demand',
                              default=Decimal(0.0))
    summer_winter_threshold = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='% for highest actual demand in previous winter months when calculating summer month billing demand',
                              default=Decimal(0.0))
    winter_summer_threshold = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='% for highest actual demand in previous summer months when calculating winter month billing demand',
                              default=Decimal(0.0))
    winter_winter_threshold = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='% for highest actual demand in previous winter months when calculating winter month billing demand',
                              default=Decimal(0.0))
    
    #these three based on Determination of Billing Demand section of GA Power PLS-8
    contract_minimum_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='contract minimum billing demand used for calculating billing demand',
                              default=Decimal(0.0))
    minimum_fraction_contract_capacity = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='minimum fraction of total contract capacity used for calculating billing demand',
                              default=Decimal(0.0))
    absolute_minimum_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='fixed value minimum demand used for calculating billing demand',
                              default=Decimal(0.0))
    
    lim_service_sliding_month_window = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='number of previous months to use in calculating limitation of service',
                              default=Decimal(0.0))
    limitation_of_service_max_kW = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='kW limit for service',
                              default=Decimal(999999.0))
    limitation_of_service_min_kW = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='kW minimum for service',
                              default=Decimal(0.0))
    limitation_of_service_winter_percent = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='limit of service % for current or previous demand in winter months',
                              default=Decimal(0.0))
    limitation_of_service_summer_percent = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='limit of service % for current or previous demand in summer months',
                              default=Decimal(0.0))

    #functions expected by superclass RateSchedule
    def __unicode__(self):
        return self.name
    def get_cost_df(self, df, billx=None):
        """function(df, billx=None)
        
        Given dataframe with monthly
        index and Peak Demand and
        Consumption, along with a
        BILLx Monther whose data
        will be retrieved for use
        in calculating billing
        demand from historical data,
        returns dataframe with
        Calculated Cost and Billing
        Demand columns."""
        try:
            if self.use_input_billing_demand and ('Billing Demand' not in df.columns): raise TypeError
            if self.use_input_billing_demand:
                if Decimal(NaN) not in df['Billing Demand']:
                    df['Calculated Billing Demand'] = df['Billing Demand']  #if using input, this is 1st choice
                else:
                    df['Calculated Billing Demand'] = df['Peak Demand']     #if NaNs, then this is 2nd choice
            else:
                df = self.get_billing_demand_df(df = df, billx = billx)     #if not using input, must calculate it with historical data from billx
            if 'Calculated Billing Demand' not in df.columns: raise TypeError
            df['Billing Demand'] = df['Calculated Billing Demand']
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Calculation failed.',
                    comment='GAPowerPandL %s get_cost_df unable to calculate billing demand, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                print 'check1'
                'Billing Demand' in df.columns
                'Consumption' in df.columns
                df['k1'] = [min(df['Billing Demand'][i]*self.tier1,df['Consumption'][i]) for i in range(0,len(df))]
                df['k2'] = [min(df['Billing Demand'][i]*(self.tier2-self.tier1),df['Consumption'][i]-df['k1'][i]) for i in range(0,len(df))]
                df['k3'] = [min(df['Billing Demand'][i]*(self.tier3-self.tier2),df['Consumption'][i]-df['k1'][i]-df['k2'][i]) for i in range(0,len(df))]
                df['k4'] = [min(df['Billing Demand'][i]*(self.tier4-self.tier3),df['Consumption'][i]-df['k1'][i]-df['k2'][i]-df['k3'][i]) for i in range(0,len(df))]
                print 'check2'
                df['k1a'] = [min(df['k1'][i],self.tier1a) for i in range(0,len(df))]
                df['k1b'] = [min(df['k1'][i]-df['k1a'][i],self.tier1b-self.tier1a) for i in range(0,len(df))]
                df['k1c'] = [min(df['k1'][i]-df['k1a'][i]-df['k1b'][i],self.tier1c-self.tier1b) for i in range(0,len(df))]
                df['k1d'] = [min(df['k1'][i]-df['k1a'][i]-df['k1b'][i]-df['k1c'][i],self.tier1d-self.tier1c) for i in range(0,len(df))]
                print 'check3'
                df['k2a'] = [min(df['k2'][i],self.tier2a) for i in range(0,len(df))]
                df['k2b'] = [min(df['k2'][i]-df['k2a'][i],self.tier2b-self.tier2a) for i in range(0,len(df))]
                df['k2c'] = [min(df['k2'][i]-df['k2a'][i]-df['k2b'][i],self.tier2c-self.tier2b) for i in range(0,len(df))]
                df['k2d'] = [min(df['k2'][i]-df['k2a'][i]-df['k2b'][i]-df['k2c'][i],self.tier2d-self.tier2c) for i in range(0,len(df))]
                print 'check4'
                df['k3a'] = [min(df['k3'][i],self.tier3a) for i in range(0,len(df))]
                df['k3b'] = [min(df['k3'][i]-df['k3a'][i],self.tier3b-self.tier3a) for i in range(0,len(df))]
                df['k3c'] = [min(df['k3'][i]-df['k3a'][i]-df['k3b'][i],self.tier3c-self.tier3b) for i in range(0,len(df))]
                df['k3d'] = [min(df['k3'][i]-df['k3a'][i]-df['k3b'][i]-df['k3c'][i],self.tier3d-self.tier3c) for i in range(0,len(df))]
                print 'check5'
                df['k4a'] = [min(df['k4'][i],self.tier4a) for i in range(0,len(df))]
                df['k4b'] = [min(df['k4'][i]-df['k4a'][i],self.tier4b-self.tier4a) for i in range(0,len(df))]
                df['k4c'] = [min(df['k4'][i]-df['k4a'][i]-df['k4b'][i],self.tier4c-self.tier4b) for i in range(0,len(df))]
                df['k4d'] = [min(df['k4'][i]-df['k4a'][i]-df['k4b'][i]-df['k4c'][i],self.tier4d-self.tier4c) for i in range(0,len(df))]
                print 'check6'
                df['checksum'] = (  df['k1a'] + df['k1b'] + df['k1c'] + df['k1d'] +
                                    df['k2a'] + df['k2b'] + df['k2c'] + df['k2d'] +
                                    df['k3a'] + df['k3b'] + df['k3c'] + df['k3d'] +
                                    df['k4a'] + df['k4b'] + df['k4c'] + df['k4d']   )
                sum1 = df['checksum'].sum()
                sum2 = df['Consumption'].sum()
                print 'check7'
                if not(sum1 == Decimal(0) and sum2 == Decimal(0)):
                    if min(sum1,sum2)/max(sum1,sum2) < Decimal(0.999):
                        m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Calculation failed.',
                                comment='GAPowerPandL %s get_cost_df computed tier consumptions that do not sum to total consumption, function aborted.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                        raise TypeError
                print 'check8'
                df['Consumption Cost'] = (  df['k1a']*self.rate1a + df['k1b']*self.rate1b +
                                            df['k1c']*self.rate1c + df['k1d']*self.rate1d +
                                            df['k2a']*self.rate2a + df['k2b']*self.rate2b +
                                            df['k2c']*self.rate2c + df['k2d']*self.rate2d +
                                            df['k3a']*self.rate3a + df['k3b']*self.rate3b +
                                            df['k3c']*self.rate3c + df['k3d']*self.rate3d +
                                            df['k4a']*self.rate4a + df['k4b']*self.rate4b +
                                            df['k4c']*self.rate4c + df['k4d']*self.rate4d   )
                print 'check9'
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Warning',
                        subject='Calculation failed.',
                        comment='GAPowerPandL %s get_cost_df unable to calculate consumption charges, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            else:
                try:
                    df['Excess Demand'] = Decimal(0.0)
                    df['Excess Demand Cost'] = Decimal(0.0)
                    #--seems the straight per kW charge is only for calculating a minimum bill
                    #--thus the following two lines don't belong here but would be used in a 
                    #----different function to compare the default calculated cost against
                    #----the minimum monthly bill from paragraph A. of the rate schedule
                    #df['Excess Demand'] = [max(df['Calculated Billing Demand'][i] - self.excess_kW_threshold, Decimal(0.0)) for i in range(0,len(df))]
                    #df['Excess Demand Cost'] = df['Excess Demand'] * self.excess_kW_rate
                except:
                    m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='GAPowerPandL %s get_cost_df unable to calculate excess demand charges, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                else:
                    try:
                        df['Basic Service Cost'] = self.basic_service_charge
                    except:
                        m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Calculation failed.',
                                comment='GAPowerPandL %s get_cost_df unable to calculate base charges, function aborted.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                    else:
                        try:
                            df['Base Revenue Cost'] = df['Consumption Cost'] + df['Basic Service Cost']
                            df['Base Revenue Riders Cost'] = Decimal(0.0)
                            for base_rider in self.riders.all(): #can't use filter because of child class usage
                                if base_rider.as_child().apply_to_base_revenue or base_rider.as_child().apply_to_consumption: #must instead check here to pull only base rev riders first
                                    df[base_rider.as_child().name] = base_rider.as_child().get_cost_df(df)['Rider Cost']
                                    df['Base Revenue Riders Cost'] = df['Base Revenue Riders Cost'] + base_rider.as_child().get_cost_df(df)['Rider Cost']
                            df['Total Revenue Cost'] = df['Base Revenue Cost'] + df['Base Revenue Riders Cost']
                            df['Total Revenue Riders Cost'] = Decimal(0.0)
                            for total_rider in self.riders.all(): #can't use filter because of child class usage
                                if total_rider.as_child().apply_to_total_revenue: #must instead check here to pull only total rev riders
                                    df[total_rider.as_child().name] = total_rider.as_child().get_cost_df(df)['Rider Cost']
                                    df['Total Revenue Riders Cost'] = df['Total Revenue Riders Cost'] + total_rider.as_child().get_cost_df(df)['Rider Cost']
                        except:
                            m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Calculation failed.',
                                    comment='GAPowerPandL %s get_cost_df unable to calculate rider charges, function aborted.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                        else:
                            df['Calculated Cost'] = (  df['Basic Service Cost'] + df['Excess Demand Cost'] +
                                                       df['Consumption Cost'] + df['Base Revenue Riders Cost'] +
                                                       df['Total Revenue Riders Cost'] 
                                                       ) * (Decimal(1.0) + self.tax_percentage)
        return df
    def is_eligible(self, df):
        return self.pass_limitation_of_service(df=df)
    def get_billing_demand_df(self, df, billx):
        """function(df, billx)
        
        Given dataframe with
        monthly index, Peak
        Demand, and Consumption,
        returns dataframe with new
        column of Calculated
        Billing Demand."""
        try:
            summer_months = self.get_summer_months()
            winter_months = self.get_winter_months()
            df['Calculated Billing Demand'] = Decimal(0.0)
            df = df.sort_index()
            billxdf = billx.get_monther_period_dataframe()
            billxdf = billxdf.sort_index()
            df_window = billxdf[max(0,len(billxdf)-int(self.billing_demand_sliding_month_window)):]
            
            for i in range(0,len(df)):
                summer_peaks = df_window['Peak Demand (act)'][[x.month in summer_months for x in df_window['End Date']]]
                if len(summer_peaks)==0:
                    summer_max = 0
                else:
                    summer_max = summer_peaks.max()
                winter_peaks = df_window['Peak Demand (act)'][[x.month in winter_months for x in df_window['End Date']]]
                if len(winter_peaks)==0:
                    winter_max = 0
                else:
                    winter_max = winter_peaks.max()
                
                if df['End Date'][i].month in summer_months: #might normally use df.index[i].month but GAPower uses meter read date
                    df['Calculated Billing Demand'][i:i+1] = max_with_NaNs([
                            df['Peak Demand (act)'][i],
                            self.summer_summer_threshold * summer_max,
                            self.summer_winter_threshold * winter_max,
                            self.contract_minimum_demand,
                            self.minimum_fraction_contract_capacity * self.excess_kW_threshold,
                            self.absolute_minimum_demand  ])
                if df['End Date'][i].month in winter_months:
                    df['Calculated Billing Demand'][i:i+1] = max_with_NaNs([
                            self.winter_summer_threshold * summer_max,
                            self.winter_winter_threshold * winter_max,
                            self.contract_minimum_demand,
                            self.minimum_fraction_contract_capacity * self.excess_kW_threshold,
                            self.absolute_minimum_demand  ])
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Calculation failed.',
                    comment='GAPowerPandL %s get_billing_demand_df unable to calculate billing demand, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    
    #functions specific to this subclass rate schedule
    def get_winter_months(self):
        """No inputs.  Returns
        list of winter month
        indices 1-12."""
        try:
            if self.winter_end_month == Decimal(0.0) or self.winter_start_month == Decimal(0.0):
                raise TypeError
            if self.winter_end_month < self.winter_start_month:
                winter_months = range(1,self.winter_end_month+1)
                b = range(self.winter_start_month,13)
                winter_months.extend(b)
            else:
                winter_months = range(self.winter_start_month,self.winter_end_month+1)
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Calculation failed.',
                    comment='GAPowerPandL %s get_winter_months failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            winter_months = None
        return winter_months
    def get_summer_months(self):
        """No inputs.  Returns
        list of summer month
        indices 1-12."""
        try:
            if self.summer_end_month == Decimal(0.0) or self.summer_start_month == Decimal(0.0):
                raise TypeError
            if self.summer_end_month < self.summer_start_month:
                summer_months = range(1,self.summer_end_month+1)
                b = range(self.summer_start_month,13)
                summer_months.extend(b)
            else:
                summer_months = range(self.summer_start_month,self.summer_end_month+1)
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Calculation failed.',
                    comment='GAPowerPandL %s get_summer_months failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            summer_months = None
        return summer_months
    def pass_limitation_of_service(self, df):
        """function(df)
        
        Given dataframe of Peak
        Demands, returns boolean
        indicating whether monthly
        demands satisfy rate
        schedule's limitation of
        service. Returns None if
        too few months given.
        """
        
        try:
            if ( df['Peak Demand'].count() < self.lim_service_sliding_month_window or
                 Decimal(NaN) in df['Peak Demand'].sort_index()[-1:-13:-1] ):
                m = Message(when=timezone.now(),
                        message_type='Code Warning',
                        subject='Missing data.',
                        comment='GAPowerPandL %s pass_limitation_of_service given too few peak demands, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                answer = None
            else:
                summer_months = self.get_summer_months()
                limit_1 = self.limitation_of_service_winter_percent * df['Peak Demand'][[x.month not in summer_months for x in df['End Date']]].max()
                limit_2 = self.limitation_of_service_summer_percent * df['Peak Demand'][[x.month in summer_months for x in df['End Date']]].max()
                answer = ( (max_with_NaNs([limit_1, limit_2]) < self.limitation_of_service_max_kW) and
                           (max_with_NaNs([limit_1, limit_2]) > self.limitation_of_service_min_kW) )
        except:
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='GAPowerPandL %s pass_limitation_of_service unable to calculate, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                answer = None
        return answer

    class Meta:
        app_label = 'BuildingSpeakApp'

class GAPowerRider(RateScheduleRider):
    percent_of_base_revenue = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=9,
                    default=Decimal(0.0),help_text='percent of base revenue (0.0-1.0)')
    percent_of_total_revenue = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=9,
                    default=Decimal(0.0),help_text='percent of total revenue (0.0-1.0)')
    summer_cost_per_kWh = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=7,
                    help_text='summer $/kWh rate (Jun-Sep)')
    winter_cost_per_kWh = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=7,
                    help_text='winter $/kWh rate (Oct-May)')

    apply_to_base_revenue = models.BooleanField(blank=True, default=False,
                    help_text='apply to base revenue?')
    apply_to_total_revenue = models.BooleanField(blank=True, default=False,
                    help_text='apply to total revenue?')
    apply_to_consumption = models.BooleanField(blank=True, default=False,
                    help_text='apply to consumption?')

    def __unicode__(self):
        return self.name
    def get_cost_df(self, df):
        try:
            if self.apply_to_base_revenue:
                df['Rider Cost'] = df['Base Revenue Cost'] * self.percent_of_base_revenue
            elif self.apply_to_total_revenue:
                df['Rider Cost'] = df['Total Revenue Cost'] * self.percent_of_total_revenue
            elif self.apply_to_consumption:
                for i in range(0,len(df)):
                    if df['End Date'][i].month in [6,7,8,9]:
                        df['Rider Cost'][i:i+1] = df['Consumption'][i:i+1] * self.summer_cost_per_kWh
                    elif df['End Date'][i].month in [1,2,3,4,5,10,11,12]:
                        df['Rider Cost'][i:i+1] = df['Consumption'][i:i+1] * self.winter_cost_per_kWh
                    else:
                        raise TypeError
            else:
                raise TypeError
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Calculation failed.',
                    comment='GAPowerRider %s get_cost_df failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    
    class Meta:
        app_label = 'BuildingSpeakApp'
