from numpy import NaN
from django.db import models
from django.utils import timezone
from decimal import Decimal

from models_functions import *
from models_Message import Message
from models_RateSchedules import RateSchedule, RateScheduleRider


class XXXX(RateSchedule):
    use_input_billing_demand = models.BooleanField(blank=True, default=True,
                    help_text='use input Billing Demand instead of Calculated Billing Demand?')
    basic_service_charge = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='monthly basic service charge',
                              default=Decimal(0.0))
    tax_percentage = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=7,
                              help_text='tax percentage applied to grand total',
                              default=Decimal(0.08))
                              

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
            
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Error',
                    subject='Calculation failed.',
                    comment='XXXXX %s get_cost_df unable to calculate billing demand, function aborted.' % self.id)
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
        try:
            
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

    class Meta:
        app_label = 'BuildingSpeakApp'

class RRRRR(RateScheduleRider):
    percent_of_base_revenue = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=9,
                    default=Decimal(0.0),help_text='percent of base revenue (0.0-1.0)')
    percent_of_total_revenue = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=9,
                    default=Decimal(0.0),help_text='percent of total revenue (0.0-1.0)')

    def __unicode__(self):
        return self.name
    def get_cost_df(self, df):
        try:
            
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
