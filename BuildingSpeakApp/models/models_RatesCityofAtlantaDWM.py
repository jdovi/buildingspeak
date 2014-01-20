from django.db import models
from django.utils import timezone
from decimal import Decimal

from models_functions import *
from models_Message import Message
from models_RateSchedules import RateSchedule


class CityOfATLWWW(RateSchedule):
    base_charge = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='monthly base charge',
                              default=Decimal(0.0))
    tax_percentage = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=7,
                              help_text='tax percentage applied to grand total',
                              default=Decimal(0.00))
                              
    tier1 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='tier 1 limit: 0 < consumption < X',
                              default=Decimal(0.0))
    tier2 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='tier 2 limit: tier 1 <= consumption < X',
                              default=Decimal(0.0))
    tier3 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='tier 3 limit: tier 2 <= consumption < X',
                              default=Decimal(0.0))
    rate1 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/ccf for tier 1',
                              default=Decimal(0.0))
    rate2 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/ccf for tier 2',
                              default=Decimal(0.0))
    rate3 = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/ccf for tier 3',
                              default=Decimal(0.0))
    security_surcharge = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='$/ccf for security surcharge',
                              default=Decimal(0.0))


    #functions expected by superclass RateSchedule
    def __unicode__(self):
        return self.name
    def get_cost_df(self, df):
        """function(df)
        
        Given dataframe with monthly
        index and Peak Demand and
        Consumption, returns dataframe
        with Calculated Cost column."""
        try:
            df['k1'] = [min(self.tier1,df['Consumption'][i]) for i in range(0,len(df))]
            df['k2'] = [min(self.tier2-self.tier1,df['Consumption'][i]-df['k1'][i]) for i in range(0,len(df))]
            df['k3'] = [min(self.tier3-self.tier2,df['Consumption'][i]-df['k1'][i]-df['k2'][i]) for i in range(0,len(df))]
            
            df['checksum'] = df['k1'] + df['k2'] + df['k3']
            sum1 = df['checksum'].sum()
            sum2 = df['Consumption'].sum()
            if min(sum1,sum2)/max(sum1,sum2) < Decimal(0.999):
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='CityOfATLWWW %s get_cost_df computed tier consumptions that do not sum to total consumption, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                raise TypeError
            
            df['Consumption Cost'] = df['k1']*self.rate1 + df['k2']*self.rate2 + df['k3']*self.rate3
        except:
            m = Message(when=timezone.now(),
                    message_type='Code Warning',
                    subject='Calculation failed.',
                    comment='CityOfATLWWW %s get_cost_df unable to calculate consumption charges, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df['Base Cost'] = self.base_charge
            except:
                m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='CityOfATLWWW %s get_cost_df unable to calculate base charges, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            else:
                try:
                    df['Security Surcharge Cost'] = df['Consumption'] * self.security_surcharge
                except:
                    m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='CityOfATLWWW %s get_cost_df unable to calculate rider charges, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                else:
                    df['Calculated Cost'] = (  df['Base Cost'] + df['Consumption Cost'] + 
                                               df['Security Surcharge Cost']
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
