import logging
import pandas as pd
from pytz import UTC
from numpy import NaN
from django.db import models
from django.utils import timezone
from django.core import urlresolvers
from decimal import Decimal
from datetime import timedelta
from django.db.models import Max, Min

from models_functions import *
from models_Message import Message

logger = logging.getLogger(__name__)

class Monther(models.Model):
    """No attributes.
    
    Stores Monthlings.  Must attach to
    Meter.
    
    Functions:
        get_monther_period_dataframe
        load_monther_period_dataframe"""
    
    name = models.CharField(blank=True, max_length=200)  #convention is four letter acronym + o/p/c
    help_text = models.CharField(blank=True, max_length=200)

    #relationships
    messages = models.ManyToManyField('Message', blank=True)
    meter = models.ForeignKey('Meter')
    consumption_model = models.ForeignKey('MeterConsumptionModel', null=True, blank=True)
    peak_demand_model = models.ForeignKey('MeterPeakDemandModel', null=True, blank=True)
    
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
        t0 = timezone.now()
        try:
            mlg_set = self.monthling_set.all()
            if mlg_set.count() == 0:
                m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Nothing to return.',
                            comment='Monther %s, get_monther_period_dataframe called when no Monthlings present.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df = None
            else:
                min_month = pd.Period(mlg_set.aggregate(Min('when'))['when__min'], freq='M')
                max_month = pd.Period(mlg_set.aggregate(Max('when'))['when__max'], freq='M')
                if first_month == '':
                    first_month = pd.Period(min_month, freq='M')
                else:
                    first_month = pd.Period(first_month, freq='M')
                if last_month == '':
                    last_month = pd.Period(max_month, freq='M')
                else:
                    last_month = pd.Period(last_month, freq='M')
                
                first_month_n = first_month.year + first_month.month/100.0
                last_month_n = last_month.year + last_month.month/100.0
                min_month_n = min_month.year + min_month.month/100.0
                max_month_n = max_month.year + max_month.month/100.0
                if last_month_n < first_month_n: #then switch them
                    first_month,first_month_n,last_month,last_month_n = last_month,last_month_n,first_month,first_month_n
        except:
            m = Message(when=timezone.now(),
                          message_type='Code Error',
                          subject='Unable to calculate range.',
                          comment='Monther %s get_monther_period_dataframe failed to determine data range.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:
            try: #here we give as much data in the requested range as we have, unless there isn't any
                if (last_month_n < min_month_n) or (first_month_n > max_month_n): raise ValueError
                elif (max_month_n >= last_month_n >= min_month_n) and (first_month_n < min_month_n):
                    first_month = min_month
                elif (max_month_n >= last_month_n >= min_month_n) and (min_month_n <= first_month_n <= max_month_n):
                    pass
                elif (last_month_n > max_month_n) and (min_month_n <= first_month_n <= max_month_n):
                    last_month = max_month
                elif (first_month_n <= min_month_n) and (last_month_n >= max_month_n):
                    first_month = min_month
                    last_month = max_month
            except:
                m = Message(when=timezone.now(),
                              message_type='Code Warning',
                              subject='Requested data range does not exist.',
                              comment='Monther %s get_monther_period_dataframe given range where no data exists.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df = None
            else:
                try:
                    t1 = (first_month.to_timestamp()+timedelta(days=10,hours=11,minutes=11,seconds=11)).tz_localize(UTC)
                    t2 = (last_month.to_timestamp()+timedelta(days=10,hours=11,minutes=11,seconds=11)).tz_localize(UTC)

                    mlg_set_filtered = mlg_set.filter(when__gte=t1).filter(when__lte=t2).order_by('when')

                    t = [x.when for x in mlg_set_filtered]
                    start_date = pd.Series([x.start_date for x in mlg_set_filtered],index=t)
                    end_date = pd.Series([x.end_date for x in mlg_set_filtered],index=t)
                    
                    cdd_peak_demand = pd.Series([x.cdd_peak_demand for x in mlg_set_filtered],index=t)
                    hdd_peak_demand = pd.Series([x.hdd_peak_demand for x in mlg_set_filtered],index=t)
                    cdd_consumption = pd.Series([x.cdd_consumption for x in mlg_set_filtered],index=t)
                    hdd_consumption = pd.Series([x.hdd_consumption for x in mlg_set_filtered],index=t)
        
                    base_bdm = pd.Series([x.base_billing_demand for x in mlg_set_filtered],index=t)
                    base_pdm = pd.Series([x.base_peak_demand for x in mlg_set_filtered],index=t)
                    base_con = pd.Series([x.base_consumption for x in mlg_set_filtered],index=t)
                    base_kpd = pd.Series([x.base_kBtuh_peak_demand for x in mlg_set_filtered],index=t)
                    base_kco = pd.Series([x.base_kBtu_consumption for x in mlg_set_filtered],index=t)
                    base_dol = pd.Series([x.base_cost for x in mlg_set_filtered],index=t)
        
                    exp_bdm = pd.Series([x.exp_billing_demand for x in mlg_set_filtered],index=t)
                    exp_pdm = pd.Series([x.exp_peak_demand for x in mlg_set_filtered],index=t)
                    exp_con = pd.Series([x.exp_consumption for x in mlg_set_filtered],index=t)
                    exp_kpd = pd.Series([x.exp_kBtuh_peak_demand for x in mlg_set_filtered],index=t)
                    exp_kco = pd.Series([x.exp_kBtu_consumption for x in mlg_set_filtered],index=t)
                    exp_dol = pd.Series([x.exp_cost for x in mlg_set_filtered],index=t)
        
                    act_bdm = pd.Series([x.act_billing_demand for x in mlg_set_filtered],index=t)
                    act_pdm = pd.Series([x.act_peak_demand for x in mlg_set_filtered],index=t)
                    act_con = pd.Series([x.act_consumption for x in mlg_set_filtered],index=t)
                    act_kpd = pd.Series([x.act_kBtuh_peak_demand for x in mlg_set_filtered],index=t)
                    act_kco = pd.Series([x.act_kBtu_consumption for x in mlg_set_filtered],index=t)
                    act_dol = pd.Series([x.act_cost for x in mlg_set_filtered],index=t)
        
                    esave_bdm = pd.Series([x.esave_billing_demand for x in mlg_set_filtered],index=t)
                    esave_pdm = pd.Series([x.esave_peak_demand for x in mlg_set_filtered],index=t)
                    esave_con = pd.Series([x.esave_consumption for x in mlg_set_filtered],index=t)
                    esave_kpd = pd.Series([x.esave_kBtuh_peak_demand for x in mlg_set_filtered],index=t)
                    esave_kco = pd.Series([x.esave_kBtu_consumption for x in mlg_set_filtered],index=t)
                    esave_dol = pd.Series([x.esave_cost for x in mlg_set_filtered],index=t)
        
                    asave_bdm = pd.Series([x.asave_billing_demand for x in mlg_set_filtered],index=t)
                    asave_pdm = pd.Series([x.asave_peak_demand for x in mlg_set_filtered],index=t)
                    asave_con = pd.Series([x.asave_consumption for x in mlg_set_filtered],index=t)
                    asave_kpd = pd.Series([x.asave_kBtuh_peak_demand for x in mlg_set_filtered],index=t)
                    asave_kco = pd.Series([x.asave_kBtu_consumption for x in mlg_set_filtered],index=t)
                    asave_dol = pd.Series([x.asave_cost for x in mlg_set_filtered],index=t)
        
                    base_bdm_d = pd.Series([x.base_billing_demand_delta for x in mlg_set_filtered],index=t)
                    base_pdm_d = pd.Series([x.base_peak_demand_delta for x in mlg_set_filtered],index=t)
                    base_con_d = pd.Series([x.base_consumption_delta for x in mlg_set_filtered],index=t)
                    base_kpd_d = pd.Series([x.base_kBtuh_peak_demand_delta for x in mlg_set_filtered],index=t)
                    base_kco_d = pd.Series([x.base_kBtu_consumption_delta for x in mlg_set_filtered],index=t)
                    base_dol_d = pd.Series([x.base_cost_delta for x in mlg_set_filtered],index=t)
        
                    exp_bdm_d = pd.Series([x.exp_billing_demand_delta for x in mlg_set_filtered],index=t)
                    exp_pdm_d = pd.Series([x.exp_peak_demand_delta for x in mlg_set_filtered],index=t)
                    exp_con_d = pd.Series([x.exp_consumption_delta for x in mlg_set_filtered],index=t)
                    exp_kpd_d = pd.Series([x.exp_kBtuh_peak_demand_delta for x in mlg_set_filtered],index=t)
                    exp_kco_d = pd.Series([x.exp_kBtu_consumption_delta for x in mlg_set_filtered],index=t)
                    exp_dol_d = pd.Series([x.exp_cost_delta for x in mlg_set_filtered],index=t)
        
                    esave_bdm_d = pd.Series([x.esave_billing_demand_delta for x in mlg_set_filtered],index=t)
                    esave_pdm_d = pd.Series([x.esave_peak_demand_delta for x in mlg_set_filtered],index=t)
                    esave_con_d = pd.Series([x.esave_consumption_delta for x in mlg_set_filtered],index=t)
                    esave_kpd_d = pd.Series([x.esave_kBtuh_peak_demand_delta for x in mlg_set_filtered],index=t)
                    esave_kco_d = pd.Series([x.esave_kBtu_consumption_delta for x in mlg_set_filtered],index=t)
                    esave_dol_d = pd.Series([x.esave_cost_delta for x in mlg_set_filtered],index=t)
    
                    df = pd.DataFrame({
                                        'Start Date' : start_date,
                                        'End Date' : end_date,
                                        
                                        'CDD (peak demand)' : cdd_peak_demand,
                                        'HDD (peak demand)' : hdd_peak_demand,
                                        'CDD (consumption)' : cdd_consumption,
                                        'HDD (consumption)' : hdd_consumption,
        
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
                    df = df.sort_index()
                except:
                    m = Message(when=timezone.now(),
                                  message_type='Code Error',
                                  subject='Unable to retrieve data.',
                                  comment='Monther %s get_monther_period_dataframe unable to retrieve data.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    df = None
        t1 = timezone.now()
        logger.debug('get_monther_period_dataframe %s' % '{0:,.0f}'.format((t1-t0).seconds*1000.0 + (t1-t0).microseconds/1000.0))
        return df
        
    def create_missing_required_columns(self, df):
        """Inputs:
            df
              (columns:Start Date, End Date,
                 Billing Demand,Peak Demand,
                 Consumption, Cost)
        
        Adds empty necessary columns to
        load df into Monthlings via
        load_monther_period_dataframe."""
        
        if 'Billing Demand (asave)' not in df.columns:          df['Billing Demand (asave)'] = Decimal(NaN)
        if 'Cost (asave)' not in df.columns:                    df['Cost (asave)'] = Decimal(NaN)
        if 'Peak Demand (asave)' not in df.columns:             df['Peak Demand (asave)'] = Decimal(NaN)
        if 'Consumption (asave)' not in df.columns:             df['Consumption (asave)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (asave)' not in df.columns:       df['kBtuh Peak Demand (asave)'] = Decimal(NaN)
        if 'kBtu Consumption (asave)' not in df.columns:        df['kBtu Consumption (asave)'] = Decimal(NaN)
        if 'Billing Demand (esave)' not in df.columns:          df['Billing Demand (esave)'] = Decimal(NaN)
        if 'Cost (esave)' not in df.columns:                    df['Cost (esave)'] = Decimal(NaN)
        if 'Peak Demand (esave)' not in df.columns:             df['Peak Demand (esave)'] = Decimal(NaN)
        if 'Consumption (esave)' not in df.columns:             df['Consumption (esave)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (esave)' not in df.columns:       df['kBtuh Peak Demand (esave)'] = Decimal(NaN)
        if 'kBtu Consumption (esave)' not in df.columns:        df['kBtu Consumption (esave)'] = Decimal(NaN)
        if 'Billing Demand (base)' not in df.columns:           df['Billing Demand (base)'] = Decimal(NaN)
        if 'Cost (base)' not in df.columns:                     df['Cost (base)'] = Decimal(NaN)
        if 'Peak Demand (base)' not in df.columns:              df['Peak Demand (base)'] = Decimal(NaN)
        if 'Consumption (base)' not in df.columns:              df['Consumption (base)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (base)' not in df.columns:        df['kBtuh Peak Demand (base)'] = Decimal(NaN)
        if 'kBtu Consumption (base)' not in df.columns:         df['kBtu Consumption (base)'] = Decimal(NaN)
        if 'Billing Demand (exp)' not in df.columns:            df['Billing Demand (exp)'] = Decimal(NaN)
        if 'Cost (exp)' not in df.columns:                      df['Cost (exp)'] = Decimal(NaN)
        if 'Peak Demand (exp)' not in df.columns:               df['Peak Demand (exp)'] = Decimal(NaN)
        if 'Consumption (exp)' not in df.columns:               df['Consumption (exp)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (exp)' not in df.columns:         df['kBtuh Peak Demand (exp)'] = Decimal(NaN)
        if 'kBtu Consumption (exp)' not in df.columns:          df['kBtu Consumption (exp)'] = Decimal(NaN)
        if 'Billing Demand (esave delta)' not in df.columns:    df['Billing Demand (esave delta)'] = Decimal(NaN)
        if 'Cost (esave delta)' not in df.columns:              df['Cost (esave delta)'] = Decimal(NaN)
        if 'Peak Demand (esave delta)' not in df.columns:       df['Peak Demand (esave delta)'] = Decimal(NaN)
        if 'Consumption (esave delta)' not in df.columns:       df['Consumption (esave delta)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (esave delta)' not in df.columns: df['kBtuh Peak Demand (esave delta)'] = Decimal(NaN)
        if 'kBtu Consumption (esave delta)' not in df.columns:  df['kBtu Consumption (esave delta)'] = Decimal(NaN)
        if 'Billing Demand (base delta)' not in df.columns:     df['Billing Demand (base delta)'] = Decimal(NaN)
        if 'Cost (base delta)' not in df.columns:               df['Cost (base delta)'] = Decimal(NaN)
        if 'Peak Demand (base delta)' not in df.columns:        df['Peak Demand (base delta)'] = Decimal(NaN)
        if 'Consumption (base delta)' not in df.columns:        df['Consumption (base delta)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (base delta)' not in df.columns:  df['kBtuh Peak Demand (base delta)'] = Decimal(NaN)
        if 'kBtu Consumption (base delta)' not in df.columns:   df['kBtu Consumption (base delta)'] = Decimal(NaN)
        if 'Billing Demand (exp delta)' not in df.columns:      df['Billing Demand (exp delta)'] = Decimal(NaN)
        if 'Cost (exp delta)' not in df.columns:                df['Cost (exp delta)'] = Decimal(NaN)
        if 'Peak Demand (exp delta)' not in df.columns:         df['Peak Demand (exp delta)'] = Decimal(NaN)
        if 'Consumption (exp delta)' not in df.columns:         df['Consumption (exp delta)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (exp delta)' not in df.columns:   df['kBtuh Peak Demand (exp delta)'] = Decimal(NaN)
        if 'kBtu Consumption (exp delta)' not in df.columns:    df['kBtu Consumption (exp delta)'] = Decimal(NaN)
        if 'kBtuh Peak Demand (act)' not in df.columns:         df['kBtuh Peak Demand (act)'] = Decimal(NaN)
        if 'kBtu Consumption (act)' not in df.columns:          df['kBtu Consumption (act)'] = Decimal(NaN)
        if 'CDD (peak demand)' not in df.columns:               df['CDD (peak demand)'] = Decimal(NaN)
        if 'HDD (peak demand)' not in df.columns:               df['HDD (peak demand)'] = Decimal(NaN)
        if 'CDD (consumption)' not in df.columns:               df['CDD (consumption)'] = Decimal(NaN)
        if 'HDD (consumption)' not in df.columns:               df['HDD (consumption)'] = Decimal(NaN)
        return df.sort_index()
        
    def load_monther_period_dataframe(self, df):
        """Inputs:
            df
              (columns:Start Date, End Date,
                 Billing Demand,Peak Demand,
                 Consumption, kBtuh Peak Demand,
                 kBtu Consumption, Cost --
                 versions act, exp, base,
                 asave, esave; +deltas)
        
        Loads given dataframe into Monther
        by adding Monthlings, checking to
        ensure addition of new Monthlings
        will maintain date contiguity.
        
        Aimed at loading new date ranges.
        Calling functions should handle
        overwriting of existing data, cf.
        Meter model's upload_bill_data
        function."""
        try:
            if (('Start Date' in df.columns) and ('End Date' in df.columns) and
                ('Billing Demand (asave)' in df.columns) and ('Cost (asave)' in df.columns) and
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
                ('CDD (peak demand)' in df.columns) and ('HDD (peak demand)' in df.columns) and
                ('CDD (consumption)' in df.columns) and ('HDD (consumption)' in df.columns) and
                (len(df)>0) and (type(df.index)==pd.tseries.period.PeriodIndex)  ):
                df = df.sort_index()
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='Monther %s, load_monther_period_dataframe given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = False
        else:
            try:
                storedbd = self.get_monther_period_dataframe()
                if storedbd is None:
                    checkbd = df
                else:
                    checkbd = pd.concat([df,storedbd])
                    checkbd = checkbd.sort_index()
                    
                #check if combined data would be contiguous before loading into Monthlings
                contiguous_check = (checkbd['End Date'].shift(1) + timedelta(days=1)) == checkbd['Start Date']
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Model update failed.',
                            comment='Monther %s, load_monther_period_dataframe unable to check contiguity, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = False
            else:
                if False in contiguous_check[1:].values: #1st is always False due to shift, but if other False then abort
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Function received bad arguments.',
                                comment='Monther %s, load_monther_period_dataframe given data not contiguous with existing data, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    success = False
                else:
                    try:
                        for i in range(0,len(df)):
                            per_date = UTC.localize(df.index[i].to_timestamp() + timedelta(days=10,hours=11,minutes=11,seconds=11)) #add days/hours/mins/secs to avoid crossing month boundary when adjusting timezones
                            if df['Start Date'][i].tzinfo is None:
                                start_i = UTC.localize(df['Start Date'][i])
                            else:
                                start_i = df['Start Date'][i]
                            if df['End Date'][i].tzinfo is None:
                                end_i = UTC.localize(df['End Date'][i])
                            else:
                                end_i = df['End Date'][i]
                            mlg = Monthling(
                                    when = per_date,
                                    start_date = start_i,
                                    end_date = end_i,
                                    
                                    cdd_peak_demand = Decimal(df['CDD (peak demand)'][i]),
                                    hdd_peak_demand = Decimal(df['HDD (peak demand)'][i]),
                                    cdd_consumption = Decimal(df['CDD (consumption)'][i]),
                                    hdd_consumption = Decimal(df['HDD (consumption)'][i]),
        
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
        return success
    class Meta:
        app_label = 'BuildingSpeakApp'
    
class Monthling(models.Model):
    """Attributes:
        when, start_date, end_date,
        billing_demand, peak_demand,
        consumption, kBtuh_peak_demand,
        kBtu_consumption, cost
        
    A 'monthly Reading' model used to track
    key meter parameters including monthly
    costs.  Must attach to Monther."""
    
    when = models.DateTimeField(help_text='datetime representation of month, with day/hour/min/sec set to 11 to avoid crossing month boundary when converting from UTC to local time')
    start_date = models.DateTimeField(null=True, blank=True, help_text='datetime representation of start day, with hour/min/sec set to 11 to avoid crossing day boundary when converting from UTC to local time')
    end_date = models.DateTimeField(null=True, blank=True, help_text='datetime representation of end day, with hour/min/sec set to 11 to avoid crossing day boundary when converting from UTC to local time')

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
    def flush_calculated_data(self):
        """No inputs. For overwriting
        existing monthlings with new
        bill data. Clears all fields
        except when, start_date,
        end_date, act_peak_demand,
        act_billing_demand, act_cost,
        act_consumption."""
        self.__setattr__('hdd_peak_demand',Decimal(NaN))
        self.__setattr__('cdd_peak_demand',Decimal(NaN))
        self.__setattr__('hdd_consumption',Decimal(NaN))
        self.__setattr__('cdd_consumption',Decimal(NaN))
        
        self.__setattr__('act_kBtuh_peak_demand',Decimal(NaN))
        self.__setattr__('act_kBtu_consumption',Decimal(NaN))

        self.__setattr__('base_billing_demand',Decimal(NaN))
        self.__setattr__('base_peak_demand',Decimal(NaN))
        self.__setattr__('base_consumption',Decimal(NaN))
        self.__setattr__('base_kBtuh_peak_demand',Decimal(NaN))
        self.__setattr__('base_kBtu_consumption',Decimal(NaN))
        self.__setattr__('base_cost',Decimal(NaN))
    
        self.__setattr__('base_billing_demand_delta',Decimal(NaN))
        self.__setattr__('base_peak_demand_delta',Decimal(NaN))
        self.__setattr__('base_consumption_delta',Decimal(NaN))
        self.__setattr__('base_kBtuh_peak_demand_delta',Decimal(NaN))
        self.__setattr__('base_kBtu_consumption_delta',Decimal(NaN))
        self.__setattr__('base_cost_delta',Decimal(NaN))
        
        self.__setattr__('exp_billing_demand',Decimal(NaN))
        self.__setattr__('exp_peak_demand',Decimal(NaN))
        self.__setattr__('exp_consumption',Decimal(NaN))
        self.__setattr__('exp_kBtuh_peak_demand',Decimal(NaN))
        self.__setattr__('exp_kBtu_consumption',Decimal(NaN))
        self.__setattr__('exp_cost',Decimal(NaN))
    
        self.__setattr__('exp_billing_demand_delta',Decimal(NaN))
        self.__setattr__('exp_peak_demand_delta',Decimal(NaN))
        self.__setattr__('exp_consumption_delta',Decimal(NaN))
        self.__setattr__('exp_kBtuh_peak_demand_delta',Decimal(NaN))
        self.__setattr__('exp_kBtu_consumption_delta',Decimal(NaN))
        self.__setattr__('exp_cost_delta',Decimal(NaN))
    
        self.__setattr__('esave_billing_demand',Decimal(NaN))
        self.__setattr__('esave_peak_demand',Decimal(NaN))
        self.__setattr__('esave_consumption',Decimal(NaN))
        self.__setattr__('esave_kBtuh_peak_demand',Decimal(NaN))
        self.__setattr__('esave_kBtu_consumption',Decimal(NaN))
        self.__setattr__('esave_cost',Decimal(NaN))
    
        self.__setattr__('esave_billing_demand_delta',Decimal(NaN))
        self.__setattr__('esave_peak_demand_delta',Decimal(NaN))
        self.__setattr__('esave_consumption_delta',Decimal(NaN))
        self.__setattr__('esave_kBtuh_peak_demand_delta',Decimal(NaN))
        self.__setattr__('esave_kBtu_consumption_delta',Decimal(NaN))
        self.__setattr__('esave_cost_delta',Decimal(NaN))
    
        self.__setattr__('asave_billing_demand',Decimal(NaN))
        self.__setattr__('asave_peak_demand',Decimal(NaN))
        self.__setattr__('asave_consumption',Decimal(NaN))
        self.__setattr__('asave_kBtuh_peak_demand',Decimal(NaN))
        self.__setattr__('asave_kBtu_consumption',Decimal(NaN))
        self.__setattr__('asave_cost',Decimal(NaN))
        
    class Meta:
        app_label = 'BuildingSpeakApp'

