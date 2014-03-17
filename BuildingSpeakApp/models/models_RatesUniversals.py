from numpy import NaN
from django.db import models
from django.utils import timezone
from decimal import Decimal

from models_functions import *
from models_Message import Message
from models_RateSchedules import RateSchedule, RateScheduleRider


class GeneralConsumption(RateSchedule):
    rate_type = models.CharField(blank=True, max_length=200,
                                 choices=[('fixed $/unit','fixed $/unit'),
                                          ('same-month average','same-month average'),
                                          ('moving average','moving average'),])
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
    rate_per_unit = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=7, help_text='$/unit consumption')
    moving_average_window_length = models.IntegerField(null=True, blank=True, help_text='number of months in moving average')
    max_number_same_months = models.IntegerField(null=True, blank=True, help_text='number of previous same-months to include')
    
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
            if self.rate_type == 'fixed $/unit':
                df['Calculated Cost'] = df['Consumption'] * self.rate_per_unit
            elif self.rate_type == 'same-month average':
                if billx is not None:
                    billxdf = billx.get_monther_period_dataframe()
                else:
                    billxdf = None
                if billxdf is not None: billxdf = billxdf.sort_index()
                combined_df = pd.concat([df, billxdf])
                combined_df = combined_df.sort_index()
                combined_df = combined_df[max(0,len(combined_df)-self.max_number_same_months*12):]
                if len(combined_df) < 12: raise ValueError
                
                avg_rates = {}
                for i in range(1,13):
                    avg_rates[i] = (combined_df['Cost (act)'][[m.month==i for m in combined_df.index]].sum() /
                                    combined_df['Consumption (act)'][[m.month==i for m in combined_df.index]].sum() )
                    #actuals used to calculate rates, but generic Consumption used elsewhere as it will
                    #be various versions (base, exp, etc.) as Meter cycles through them to calculate
                    #costs on all of them
                
                df['month number'] = df.index.map(lambda i: i.month)
                df['avg rate'] = df['month number'].apply(lambda i: avg_rates[i])
                df['Calculated Cost'] = df['Consumption'] * df['avg rate']
            elif self.rate_type == 'moving average':
                if billx is not None:
                    billxdf = billx.get_monther_period_dataframe()
                else:
                    billxdf = None
                if billxdf is not None: billxdf = billxdf.sort_index()
                combined_df = pd.concat([df, billxdf])
                combined_df = combined_df.sort_index()
                
                #need to remove forecasted months first in order to use Consumption(act) and Cost(act)
                combined_df['Cost (act) is NaN'] = combined_df['Cost (act)'].apply(decimal_isnan)
                combined_df['Consumption (act) is NaN'] = combined_df['Consumption (act)'].apply(decimal_isnan)
                temp = [[combined_df['Cost (act) is NaN'][i],
                         combined_df['Consumption (act) is NaN'][i]] for i in range(0,len(combined_df))]
                combined_df['IsNotForecasted'] = [not(i[0] and i[1]) for i in temp]
                combined_df = combined_df[combined_df['IsNotForecasted']]

                combined_df = combined_df[max(0,len(combined_df)-self.moving_average_window_length):]
                if len(combined_df) < 1:
                    m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Calculation failed.',
                            comment='GeneralConsumption %s get_cost_df found no data in moving average window, costs set to NaNs.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    df['Calculated Cost'] = Decimal(NaN)
                else:
                    df['Calculated Cost'] = df['Consumption'] * combined_df['Cost (act)'].sum() / combined_df['Consumption (act)'].sum()
                    #actuals used to calculate rates, but generic Consumption used elsewhere as it will
                    #be various versions (base, exp, etc.) as Meter cycles through them to calculate
                    #costs on all of them
                
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Calculation failed.',
                    comment='GeneralConsumption %s get_cost_df unable to calculate costs, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    def is_eligible(self, df):
        pass
    def get_billing_demand_df(self, df, billx):
        """function(df, billx)
        
        Given dataframe with
        monthly index, Peak
        Demand, and Consumption,
        returns dataframe with new
        column of Calculated
        Billing Demand."""
        pass    

    #functions specific to this subclass rate schedule

    class Meta:
        app_label = 'BuildingSpeakApp'

