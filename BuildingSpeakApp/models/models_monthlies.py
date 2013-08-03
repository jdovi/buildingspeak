#import dbarray
import numpy as np
import pandas as pd
from pytz import UTC
from pytz import timezone as tz
from numpy import NaN
from scipy import stats
import statsmodels.api as sm
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

class BillingCycler(models.Model):
    """No attributes.
    
    Stores BillingCycles.  Must attach to
    Meter.
    
    Functions:
        get_billing_cycler_period_dataframe
        load_billing_cycler_period_dataframe"""
    #relationships
    meter = models.ForeignKey('Meter')
    messages = models.ManyToManyField('Message')
    #functions
    def meter_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(self.meter.id,)), self.meter.name)
    meter_for_admin.allow_tags = True
    meter_for_admin.short_description = 'Meter'
    def billing_cycles_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_billingcycle_change',args=(bcyc.id,)), bcyc.period_date) for bcyc in self.billingcycle_set.order_by('when')])
    billing_cycles_for_admin.allow_tags = True
    billing_cycles_for_admin.short_description = 'Billing Cycles'
    def get_billing_cycler_period_dataframe(self, first_month='', last_month=''):
        """Optional inputs:
              first_month
              last_month
                  as 'mm/yyyy'
        
        Returns BillingCycler's dataframe."""
        
        if self.billingcycle_set.count() == 0:
            m = Message(when=timezone.now(),
                                      message_type='Code Warning',
                                      subject='Nothing to return.',
                                      comment='BillingCycler %s, get_billing_cycler_period_dataframe called when no BillingCycles present.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:
            pdates = pd.Series([x.period_date for x in self.billingcycle_set.order_by('period_date')])
            sdates = pd.Series([x.start_date for x in self.billingcycle_set.order_by('period_date')],
                                index = pdates)
            edates = pd.Series([x.end_date for x in self.billingcycle_set.order_by('period_date')],
                                index = pdates)
            df = pd.DataFrame({'Start Date' : sdates,
                               'End Date' : edates})
            df.index = df.index.to_period(freq='M')
            df = df.sort_index()
            
            dfa = df.index[0]
            dfz = df.index[-1]
            if first_month == '': first_month = dfa
            if last_month == '': last_month = dfz
            if (pd.Period(first_month, freq='M') - dfa < 0) or (pd.Period(last_month, freq='M') - dfz > 0):
                m = Message(when=timezone.now(),
                                          message_type='Code Warning',
                                          subject='Out of range.',
                                          comment='BillingCycler %s get_billing_cycler_period_dataframe given date request outside available data date range.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df = None
            else:
                df = df[first_month:last_month]
        return df
    
    def load_billing_cycler_period_dataframe(self, df):
        """Inputs: 
            dataframe (in BillingCycler format)
            
        Stores the provided dataframe in
        itself by adding BillingCycles.
        Each new Start Date must be +1
        day from the previous End Date."""
        
        if (('Start Date' in df.columns) and (len(df)>0) and
            ('End Date' in df.columns)   and (type(df.index)==pd.tseries.period.PeriodIndex)):
            df = df.sort_index()
            contiguous_check = (df['End Date'].shift(1) + timedelta(days=1)) == df['Start Date'] #start check on month 2
            if False in contiguous_check[1:].values: #1st is always False due to shift, but if other False then abort
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Function received bad arguments.',
                            comment='BillingCycler %s, load_billing_cycler_period_dataframe function given noncontiguous billing cycles, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = False
            else:
                self.billingcycle_set.all().delete()
                for i in range(0,len(df)):
                    per_date = UTC.localize(df.index[i].to_timestamp() + timedelta(days=10,hours=11,minutes=11,seconds=11)) #add days/hours/mins/secs to avoid crossing month boundary when adjusting timezones
                    bc = BillingCycle(
                            period_date = per_date,
                            start_date = UTC.localize(df['Start Date'][i] + timedelta(hours=11,minutes=11,seconds=11)), #add hours/mins/secs to avoid crossing day boundary when adjusting timezones
                            end_date = UTC.localize(df['End Date'][i] + timedelta(hours=11,minutes=11,seconds=11)), #add hours/mins/secs to avoid crossing day boundary when adjusting timezones
                            billingcycler = self)
                    bc.save()
                m = Message(when=timezone.now(),
                            message_type='Code Success',
                            subject='Model updated.',
                            comment='Loaded dataframe into BillingCycler %s.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = True
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='BillingCycler %s, load_billing_cycler_period_dataframe given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = False
        return success
    class Meta:
        app_label = 'BuildingSpeakApp'
    
class BillingCycle(models.Model):
    """Attributes (all datetimes):
        period_date
        start_date
        end_date
        
    Stores billing cycle start/end dates
    and date representing period.  Must
    attach to BillingCycler."""
    
    period_date = models.DateTimeField(help_text='datetime representation of month, with day/hour/min/sec set to 11 to avoid crossing month boundary when converting from UTC to local time')  #date used to represent pandas Period
    start_date = models.DateTimeField(help_text='datetime representation of day, with hour/min/sec set to 11 to avoid crossing day boundary when converting from UTC to local time')
    end_date = models.DateTimeField(help_text='datetime representation of day, with hour/min/sec set to 11 to avoid crossing day boundary when converting from UTC to local time')
    #relationships
    billingcycler = models.ForeignKey('BillingCycler')
    messages = models.ManyToManyField('Message')
    #functions
    def billing_cycler_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_billingcycler_change',args=(self.billingcycler.id,)), 'BillingCycler')
    billing_cycler_for_admin.allow_tags = True
    billing_cycler_for_admin.short_description = 'Billing Cycler'

    class Meta:
        app_label = 'BuildingSpeakApp'

class Monther(models.Model):
    """No attributes.
    
    Stores Monthlings.  Must attach to
    Meter.  Matches BillingCycler's
    periods.
    
    Functions:
        get_monther_period_dataframe
        load_monther_period_dataframe"""
    
    name = models.CharField(blank=True, max_length=200)  #convention is four letter acronym + o/p/c
    help_text = models.CharField(blank=True, max_length=200)

    #relationships
    events = models.ManyToManyField('Event')
    messages = models.ManyToManyField('Message')
    meter = models.ForeignKey('Meter')
    consumption_model = models.ForeignKey('MeterConsumptionModel', null=True)
    peak_demand_model = models.ForeignKey('MeterPeakDemandModel', null=True)
    
    #functions
    def meter_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(self.meter.id,)), self.meter.name)
    meter_for_admin.allow_tags = True
    meter_for_admin.short_description = 'Meter'
    def monthlings_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_monthling_change',args=(mntg.id,)), mntg.when) for mntg in self.monthling_set.order_by('when')])
    monthlings_for_admin.allow_tags = True
    monthlings_for_admin.short_description = 'Monthlings'
    def __unicode__(self):
        return self.name
    def get_monther_period_dataframe(self,  first_month='', last_month=''):
        """Optional inputs:
              first_month
              last_month
                  as 'mm/yyyy'
        
        Returns Monther's dataframe."""
        
        if self.monthling_set.count() == 0:
            m = Message(when=timezone.now(),
                        message_type='Code Warning',
                        subject='Nothing to return.',
                        comment='Monther %s, get_monther_period_dataframe called when no Monthlings present.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:
            t = [x.when for x in self.monthling_set.order_by('when')]
            cdd_peak_demand = pd.Series([x.cdd_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            hdd_peak_demand = pd.Series([x.hdd_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            cdd_consumption = pd.Series([x.cdd_consumption for x in self.monthling_set.order_by('when')],index=t)
            hdd_consumption = pd.Series([x.hdd_consumption for x in self.monthling_set.order_by('when')],index=t)

            base_bdm = pd.Series([x.base_billing_demand for x in self.monthling_set.order_by('when')],index=t)
            base_pdm = pd.Series([x.base_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            base_con = pd.Series([x.base_consumption for x in self.monthling_set.order_by('when')],index=t)
            base_kpd = pd.Series([x.base_kBtuh_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            base_kco = pd.Series([x.base_kBtu_consumption for x in self.monthling_set.order_by('when')],index=t)
            base_dol = pd.Series([x.base_cost for x in self.monthling_set.order_by('when')],index=t)

            exp_bdm = pd.Series([x.exp_billing_demand for x in self.monthling_set.order_by('when')],index=t)
            exp_pdm = pd.Series([x.exp_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            exp_con = pd.Series([x.exp_consumption for x in self.monthling_set.order_by('when')],index=t)
            exp_kpd = pd.Series([x.exp_kBtuh_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            exp_kco = pd.Series([x.exp_kBtu_consumption for x in self.monthling_set.order_by('when')],index=t)
            exp_dol = pd.Series([x.exp_cost for x in self.monthling_set.order_by('when')],index=t)

            act_bdm = pd.Series([x.act_billing_demand for x in self.monthling_set.order_by('when')],index=t)
            act_pdm = pd.Series([x.act_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            act_con = pd.Series([x.act_consumption for x in self.monthling_set.order_by('when')],index=t)
            act_kpd = pd.Series([x.act_kBtuh_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            act_kco = pd.Series([x.act_kBtu_consumption for x in self.monthling_set.order_by('when')],index=t)
            act_dol = pd.Series([x.act_cost for x in self.monthling_set.order_by('when')],index=t)

            esave_bdm = pd.Series([x.esave_billing_demand for x in self.monthling_set.order_by('when')],index=t)
            esave_pdm = pd.Series([x.esave_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            esave_con = pd.Series([x.esave_consumption for x in self.monthling_set.order_by('when')],index=t)
            esave_kpd = pd.Series([x.esave_kBtuh_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            esave_kco = pd.Series([x.esave_kBtu_consumption for x in self.monthling_set.order_by('when')],index=t)
            esave_dol = pd.Series([x.esave_cost for x in self.monthling_set.order_by('when')],index=t)

            asave_bdm = pd.Series([x.asave_billing_demand for x in self.monthling_set.order_by('when')],index=t)
            asave_pdm = pd.Series([x.asave_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            asave_con = pd.Series([x.asave_consumption for x in self.monthling_set.order_by('when')],index=t)
            asave_kpd = pd.Series([x.asave_kBtuh_peak_demand for x in self.monthling_set.order_by('when')],index=t)
            asave_kco = pd.Series([x.asave_kBtu_consumption for x in self.monthling_set.order_by('when')],index=t)
            asave_dol = pd.Series([x.asave_cost for x in self.monthling_set.order_by('when')],index=t)

            base_bdm_d = pd.Series([x.base_billing_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            base_pdm_d = pd.Series([x.base_peak_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            base_con_d = pd.Series([x.base_consumption_delta for x in self.monthling_set.order_by('when')],index=t)
            base_kpd_d = pd.Series([x.base_kBtuh_peak_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            base_kco_d = pd.Series([x.base_kBtu_consumption_delta for x in self.monthling_set.order_by('when')],index=t)
            base_dol_d = pd.Series([x.base_cost_delta for x in self.monthling_set.order_by('when')],index=t)

            exp_bdm_d = pd.Series([x.exp_billing_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            exp_pdm_d = pd.Series([x.exp_peak_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            exp_con_d = pd.Series([x.exp_consumption_delta for x in self.monthling_set.order_by('when')],index=t)
            exp_kpd_d = pd.Series([x.exp_kBtuh_peak_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            exp_kco_d = pd.Series([x.exp_kBtu_consumption_delta for x in self.monthling_set.order_by('when')],index=t)
            exp_dol_d = pd.Series([x.exp_cost_delta for x in self.monthling_set.order_by('when')],index=t)

            esave_bdm_d = pd.Series([x.esave_billing_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            esave_pdm_d = pd.Series([x.esave_peak_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            esave_con_d = pd.Series([x.esave_consumption_delta for x in self.monthling_set.order_by('when')],index=t)
            esave_kpd_d = pd.Series([x.esave_kBtuh_peak_demand_delta for x in self.monthling_set.order_by('when')],index=t)
            esave_kco_d = pd.Series([x.esave_kBtu_consumption_delta for x in self.monthling_set.order_by('when')],index=t)
            esave_dol_d = pd.Series([x.esave_cost_delta for x in self.monthling_set.order_by('when')],index=t)

            df = pd.DataFrame({
                                'CDD_peak_demand' : cdd_peak_demand,
                                'HDD_peak_demand' : hdd_peak_demand,
                                'CDD_consumption' : cdd_consumption,
                                'HDD_consumption' : hdd_consumption,

                                'Billing Demand (base)' : base_bdm,
                                'Peak Demand (base)' : base_pdm,
                                'Consumption (base)' : base_con,
                                'kBtuh Peak Demand (base)' : base_kpd,
                                'kBtu Consumption (base)' : base_kco,
                                'Cost (base)' : base_dol,

                                'Billing Demand (exp)' : exp_bdm,
                                'Peak Demand (exp)' : exp_pdm,
                                'Consumption (exp)' : exp_con,
                                'kBtuh Peak Demand (exp)' : exp_kpd,
                                'kBtu Consumption (exp)' : exp_kco,
                                'Cost (exp)' : exp_dol,

                                'Billing Demand (act)' : act_bdm,
                                'Peak Demand (act)' : act_pdm,
                                'Consumption (act)' : act_con,
                                'kBtuh Peak Demand (act)' : act_kpd,
                                'kBtu Consumption (act)' : act_kco,
                                'Cost (act)' : act_dol,

                                'Billing Demand (esave)' : esave_bdm,
                                'Peak Demand (esave)' : esave_pdm,
                                'Consumption (esave)' : esave_con,
                                'kBtuh Peak Demand (esave)' : esave_kpd,
                                'kBtu Consumption (esave)' : esave_kco,
                                'Cost (esave)' : esave_dol,

                                'Billing Demand (asave)' : asave_bdm,
                                'Peak Demand (asave)' : asave_pdm,
                                'Consumption (asave)' : asave_con,
                                'kBtuh Peak Demand (asave)' : asave_kpd,
                                'kBtu Consumption (asave)' : asave_kco,
                                'Cost (asave)' : asave_dol,

                                'Billing Demand (base delta)' : base_bdm_d,
                                'Peak Demand (base delta)' : base_pdm_d,
                                'Consumption (base delta)' : base_con_d,
                                'kBtuh Peak Demand (base delta)' : base_kpd_d,
                                'kBtu Consumption (base delta)' : base_kco_d,
                                'Cost (base delta)' : base_dol_d,

                                'Billing Demand (exp delta)' : exp_bdm_d,
                                'Peak Demand (exp delta)' : exp_pdm_d,
                                'Consumption (exp delta)' : exp_con_d,
                                'kBtuh Peak Demand (exp delta)' : exp_kpd_d,
                                'kBtu Consumption (exp delta)' : exp_kco_d,
                                'Cost (exp delta)' : exp_dol_d,

                                'Billing Demand (esave delta)' : esave_bdm_d,
                                'Peak Demand (esave delta)' : esave_pdm_d,
                                'Consumption (esave delta)' : esave_con_d,
                                'kBtuh Peak Demand (esave delta)' : esave_kpd_d,
                                'kBtu Consumption (esave delta)' : esave_kco_d,
                                'Cost (esave delta)' : esave_dol_d,
                                })
            df.index = df.index.to_period(freq='M')

            dfa = df.index[0]
            dfz = df.index[-1]
            if first_month == '': first_month = dfa
            if last_month == '': last_month = dfz
            if (pd.Period(first_month, freq='M') - dfa < 0) or (pd.Period(last_month, freq='M') - dfz > 0):
                m = Message(when=timezone.now(),
                                          message_type='Code Warning',
                                          subject='Out of range.',
                                          comment='Monther %s get_monther_period_dataframe given date request outside available data date range.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df = None
            else:
                df = df[first_month:last_month]
                df = df.sort_index()
        return df
    def load_monther_period_dataframe(self, df):
        """Inputs:
            df
              (columns:Billing Demand,Peak Demand,
                 Consumption, kBtuh Peak Demand,
                 kBtu Consumption, Cost --
                 versions act, exp, base,
                 asave, esave; +deltas)
        
        Loads given dataframe into Monther
        by adding Monthlings. Calling
        function should ensure match with
        BillingCycler periods."""

        if (('Billing Demand (asave)' in df.columns) and ('Cost (asave)' in df.columns) and
            ('Peak Demand (asave)' in df.columns) and ('Consumption (asave)' in df.columns) and
            ('kBtuh Peak Demand (asave)' in df.columns) and ('kBtu Consumption (asave)' in df.columns) and
            ('Billing Demand (esave)' in df.columns) and ('Cost (esave)' in df.columns) and
            ('Peak Demand (esave)' in df.columns) and ('Consumption (esave)' in df.columns) and
            ('kBtuh Peak Demand (esave)' in df.columns) and ('kBtu Consumption (esave)' in df.columns) and
            ('Billing Demand (base)' in df.columns) and ('Cost (base)' in df.columns) and
            ('Peak Demand (base)' in df.columns) and ('Consumption (base)' in df.columns) and
            ('kBtuh Peak Demand (base)' in df.columns) and ('kBtu Consumption (base)' in df.columns) and
            ('Billing Demand (exp)' in df.columns) and ('Cost (exp)' in df.columns) and
            ('Peak Demand (exp)' in df.columns) and ('Consumption (exp)' in df.columns) and
            ('kBtuh Peak Demand (exp)' in df.columns) and ('kBtu Consumption (exp)' in df.columns) and
            ('Billing Demand (esave delta)' in df.columns) and ('Cost (esave delta)' in df.columns) and
            ('Peak Demand (esave delta)' in df.columns) and ('Consumption (esave delta)' in df.columns) and
            ('kBtuh Peak Demand (esave delta)' in df.columns) and ('kBtu Consumption (esave delta)' in df.columns) and
            ('Billing Demand (base delta)' in df.columns) and ('Cost (base delta)' in df.columns) and
            ('Peak Demand (base delta)' in df.columns) and ('Consumption (base delta)' in df.columns) and
            ('kBtuh Peak Demand (base delta)' in df.columns) and ('kBtu Consumption (base delta)' in df.columns) and
            ('Billing Demand (exp delta)' in df.columns) and ('Cost (exp delta)' in df.columns) and
            ('Peak Demand (exp delta)' in df.columns) and ('Consumption (exp delta)' in df.columns) and
            ('kBtuh Peak Demand (exp delta)' in df.columns) and ('kBtu Consumption (exp delta)' in df.columns) and
            ('Billing Demand (act)' in df.columns) and ('Cost (act)' in df.columns) and
            ('Peak Demand (act)' in df.columns) and ('Consumption (act)' in df.columns) and
            ('kBtuh Peak Demand (act)' in df.columns) and ('kBtu Consumption (act)' in df.columns) and
            ('CDD_peak_demand' in df.columns) and ('HDD_peak_demand' in df.columns) and
            ('CDD_consumption' in df.columns) and ('HDD_consumption' in df.columns) and
            (len(df)>0) and (type(df.index)==pd.tseries.period.PeriodIndex)  ):
            df = df.sort_index()
            self.monthling_set.all().delete()
            try:
                for i in range(0,len(df)):
                    per_date = UTC.localize(df.index[i].to_timestamp() + timedelta(days=10,hours=11,minutes=11,seconds=11)) #add days/hours/mins/secs to avoid crossing month boundary when adjusting timezones
                    mlg = Monthling(
                            when = per_date,
                            cdd_peak_demand = Decimal(df['CDD_peak_demand'][i]),
                            hdd_peak_demand = Decimal(df['HDD_peak_demand'][i]),
                            cdd_consumption = Decimal(df['CDD_consumption'][i]),
                            hdd_consumption = Decimal(df['HDD_consumption'][i]),
                            base_billing_demand = Decimal(df['Billing Demand (base)'][i]),
                            base_peak_demand = Decimal(df['Peak Demand (base)'][i]),
                            base_consumption = Decimal(df['Consumption (base)'][i]),
                            base_kBtuh_peak_demand = Decimal(df['kBtuh Peak Demand (base)'][i]),
                            base_kBtu_consumption = Decimal(df['kBtu Consumption (base)'][i]),
                            base_cost = Decimal(df['Cost (base)'][i]),
                            exp_billing_demand = Decimal(df['Billing Demand (exp)'][i]),
                            exp_peak_demand = Decimal(df['Peak Demand (exp)'][i]),
                            exp_consumption = Decimal(df['Consumption (exp)'][i]),
                            exp_kBtuh_peak_demand = Decimal(df['kBtuh Peak Demand (exp)'][i]),
                            exp_kBtu_consumption = Decimal(df['kBtu Consumption (exp)'][i]),
                            exp_cost = Decimal(df['Cost (exp)'][i]),
                            act_billing_demand = Decimal(df['Billing Demand (act)'][i]),
                            act_peak_demand = Decimal(df['Peak Demand (act)'][i]),
                            act_consumption = Decimal(df['Consumption (act)'][i]),
                            act_kBtuh_peak_demand = Decimal(df['kBtuh Peak Demand (act)'][i]),
                            act_kBtu_consumption = Decimal(df['kBtu Consumption (act)'][i]),
                            act_cost = Decimal(df['Cost (act)'][i]),
                            esave_billing_demand = Decimal(df['Billing Demand (esave)'][i]),
                            esave_peak_demand = Decimal(df['Peak Demand (esave)'][i]),
                            esave_consumption = Decimal(df['Consumption (esave)'][i]),
                            esave_kBtuh_peak_demand = Decimal(df['kBtuh Peak Demand (esave)'][i]),
                            esave_kBtu_consumption = Decimal(df['kBtu Consumption (esave)'][i]),
                            esave_cost = Decimal(df['Cost (esave)'][i]),
                            asave_billing_demand = Decimal(df['Billing Demand (asave)'][i]),
                            asave_peak_demand = Decimal(df['Peak Demand (asave)'][i]),
                            asave_consumption = Decimal(df['Consumption (asave)'][i]),
                            asave_kBtuh_peak_demand = Decimal(df['kBtuh Peak Demand (asave)'][i]),
                            asave_kBtu_consumption = Decimal(df['kBtu Consumption (asave)'][i]),
                            asave_cost = Decimal(df['Cost (asave)'][i]),

                            base_billing_demand_delta = Decimal(df['Billing Demand (base delta)'][i]),
                            base_peak_demand_delta = Decimal(df['Peak Demand (base delta)'][i]),
                            base_consumption_delta = Decimal(df['Consumption (base delta)'][i]),
                            base_kBtuh_peak_demand_delta = Decimal(df['kBtuh Peak Demand (base delta)'][i]),
                            base_kBtu_consumption_delta = Decimal(df['kBtu Consumption (base delta)'][i]),
                            base_cost_delta = Decimal(df['Cost (base delta)'][i]),
                            exp_billing_demand_delta = Decimal(df['Billing Demand (exp delta)'][i]),
                            exp_peak_demand_delta = Decimal(df['Peak Demand (exp delta)'][i]),
                            exp_consumption_delta = Decimal(df['Consumption (exp delta)'][i]),
                            exp_kBtuh_peak_demand_delta = Decimal(df['kBtuh Peak Demand (exp delta)'][i]),
                            exp_kBtu_consumption_delta = Decimal(df['kBtu Consumption (exp delta)'][i]),
                            exp_cost_delta = Decimal(df['Cost (exp delta)'][i]),
                            esave_billing_demand_delta = Decimal(df['Billing Demand (esave delta)'][i]),
                            esave_peak_demand_delta = Decimal(df['Peak Demand (esave delta)'][i]),
                            esave_consumption_delta = Decimal(df['Consumption (esave delta)'][i]),
                            esave_kBtuh_peak_demand_delta = Decimal(df['kBtuh Peak Demand (esave delta)'][i]),
                            esave_kBtu_consumption_delta = Decimal(df['kBtu Consumption (esave delta)'][i]),
                            esave_cost_delta = Decimal(df['Cost (esave delta)'][i]),

                            monther = self)
                    mlg.save()
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Model update failed.',
                            comment='Monther %s load_monther_period_dataframe unable to create and save all Monthlings.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = False
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Success',
                            subject='Model updated.',
                            comment='Loaded dataframe into Monther %s.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = True
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='Monther %s, load_monther_period_dataframe given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = False
        return success
    class Meta:
        app_label = 'BuildingSpeakApp'
    
class Monthling(models.Model):
    """Attributes:
        when, billing_demand, peak_demand,
        consumption, kBtuh_peak_demand,
        kBtu_consumption, cost
        
    A 'monthly Reading' model used to track
    key meter parameters including monthly
    costs.  Must attach to Monther."""
    
    when = models.DateTimeField(help_text='datetime representation of month, with day/hour/min/sec set to 11 to avoid crossing month boundary when converting from UTC to local time')
    hdd_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    cdd_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    hdd_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    cdd_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    
    base_billing_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_kBtuh_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_kBtu_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_cost = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)

    base_billing_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_peak_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_consumption_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_kBtuh_peak_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_kBtu_consumption_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    base_cost_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    
    exp_billing_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_kBtuh_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_kBtu_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_cost = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)

    exp_billing_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_peak_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_consumption_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_kBtuh_peak_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_kBtu_consumption_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    exp_cost_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)

    act_billing_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    act_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    act_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    act_kBtuh_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    act_kBtu_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    act_cost = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)

    esave_billing_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_kBtuh_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_kBtu_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_cost = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)

    esave_billing_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_peak_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_consumption_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_kBtuh_peak_demand_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_kBtu_consumption_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    esave_cost_delta = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)

    asave_billing_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    asave_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    asave_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    asave_kBtuh_peak_demand = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    asave_kBtu_consumption = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)
    asave_cost = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3)


    #relationships
    monther = models.ForeignKey('Monther')
    events = models.ManyToManyField('Event')
    #functions
    def monther_id_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_monther_change',args=(self.monther.id,)), self.monther.id)
    monther_id_for_admin.allow_tags = True
    monther_id_for_admin.short_description = 'Monther ID'
    def monther_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_monther_change',args=(self.monther.id,)), self.monther.name)
    monther_for_admin.allow_tags = True
    monther_for_admin.short_description = 'Monther Name'
    def __unicode__(self):
        return str(self.when)
    class Meta:
        app_label = 'BuildingSpeakApp'

