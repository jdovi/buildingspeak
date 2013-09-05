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

from models_functions import *
from models_Message import Message
from models_RateSchedules import RateSchedule, RateScheduleRider


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
    def get_cost_df(self, df):
        """function(df)
        
        Given dataframe with monthly
        index and Peak Demand and
        Consumption, returns dataframe
        with Calculated Cost column."""
        try:
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
