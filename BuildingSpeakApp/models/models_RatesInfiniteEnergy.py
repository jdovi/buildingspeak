from django.db import models
from django.utils import timezone
from decimal import Decimal

from models_functions import *
from models_Message import Message
from models_RateSchedules import RateSchedule


class InfiniteEnergyGAGas(RateSchedule):
    basic_service_charge = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='monthly basic service charge',
                              default=Decimal(0.0))
    tax_percentage = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=7,
                              help_text='tax percentage applied to grand total',
                              default=Decimal(0.08))
                              
    therm_rate = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/therm rate',
                              default=Decimal(0.0))

    #functions expected by superclass RateSchedule
    def __unicode__(self):
        return self.name
    def get_cost_df(self, df, billx=None):
        """function(df)
        
        Given dataframe with monthly
        index and Peak Demand and
        Consumption, returns dataframe
        with Calculated Cost column."""
        try:
            df['Billing Demand'] = df['Billing Demand'].apply(Decimal)
            df['Peak Demand'] = df['Peak Demand'].apply(Decimal)
            df['Consumption'] = df['Consumption'].apply(Decimal)

            df['Consumption Cost'] = df['Consumption']*self.therm_rate
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Warning',
                    subject='Calculation failed.',
                    comment='InfiniteEnergyGAGas %s get_cost_df unable to calculate consumption charges, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df['Base Cost'] = self.basic_service_charge
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='InfiniteEnergyGAGas %s get_cost_df unable to calculate base charges, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            else:
                df['Calculated Cost'] = (  df['Base Cost'] + df['Consumption Cost']
                                               ) * (Decimal(1.0) + self.tax_percentage)
        return df
    def is_eligible(self, df):
        """Not used.  Returns True."""
        return True
    def get_billing_demand_df(self, df):
        """Not used. Returns df."""
        return df
    
    class Meta:
        app_label = 'BuildingSpeakApp'
