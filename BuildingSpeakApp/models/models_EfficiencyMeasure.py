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
from operator import itemgetter, attrgetter
from djorm_pgarray.fields import ArrayField
from model_utils.managers import InheritanceManager
from storages.backends.s3boto import S3BotoStorage
from django.contrib.auth.models import User

from models_functions import *
from models_Message import Message
from models_Meter import Meter
from models_Equipment import Equipment
from models_WeatherStation import WeatherStation

class EMMeterApportionment(models.Model):
    """Intermediate model defining
    relationship of EfficiencyMeasure
    to Meter."""
    
    #relationships
    meter = models.ForeignKey('Meter')
    efficiency_measure = models.ForeignKey('EfficiencyMeasure')
    
    #attributes
    assigned_fraction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3,
                        help_text='fraction of efficiency measure consumption/demand/cost savings assigned to meter')
    
    #functions
    def __unicode__(self):
        return str(self.meter.name + ' - ' + self.efficiency_measure.name)
    class Meta:
        app_label = 'BuildingSpeakApp'

class EMEquipmentApportionment(models.Model):
    """Intermediate model defining
    relationship of EfficiencyMeasure
    to Equipment."""
    
    #relationships
    equipment = models.ForeignKey('Equipment')
    efficiency_measure = models.ForeignKey('EfficiencyMeasure')
    
    #attributes
    assigned_fraction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3,
                        help_text='fraction of efficiency measure consumption/demand/cost savings assigned to equipment')
    
    #functions
    def __unicode__(self):
        return str(self.equipment.name + ' - ' + self.efficiency_measure.name)
    class Meta:
        app_label = 'BuildingSpeakApp'

class EfficiencyMeasure(models.Model):
    """Model for efficiency
    measures. Connect to
    Meters and Equipments."""
    name = models.CharField(blank=True, max_length=200)
    when = models.DateTimeField(null=True, blank=True)

    annual_consumption_savings = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                                                     help_text='expected total annual consumption savings',
                                                     default=Decimal(0.0))
    peak_demand_savings = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                                              help_text='expected maximum peak demand savings',
                                              default=Decimal(0.0))
    annual_cost_savings = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                                              help_text='expected annual cost savings (will be ignored in favor of RateSchedule calculations)',
                                              default=Decimal(0.0))
    percent_uncertainty = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='uncertainty percentage in annual savings numbers',
                              default=Decimal(0.01))
    
    percent_cool = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='fraction of savings correlated with CDD',
                              default=Decimal(0.0))
    percent_heat = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='fraction of savings correlated with HDD',
                              default=Decimal(0.0))
    percent_flat = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='fraction of savings assumed constant each day',
                              default=Decimal(0.0))
    percent_fixed = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='fraction of savings assumed constant each month',
                              default=Decimal(0.0))

    utility_type = models.CharField(blank=True, max_length=200,
                                    choices=[('electricity','electricity'),
                                             ('natural gas','natural gas'),
                                             ('domestic water','domestic water'),
                                             ('chilled water','chilled water'),
                                             ('hot water','hot water'),
                                             ('steam','steam'),
                                             ('fuel oil (1,2,4), diesel','fuel oil (1,2,4), diesel'),
                                             ('fuel oil (5,6)','fuel oil (5,6)'),
                                             ('kerosene','kerosene'),
                                             ('propane and liquid propane','propane and liquid propane'),
                                             ('coal (anthracite)','coal (anthracite)'),
                                             ('coal (bituminous)','coal (bituminous)'),
                                             ('coke','coke'),
                                             ('wood','wood'),
                                             ('other','other')])
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

    #these shouldn't be set directly; they're set via apportion_savings function    
    jan_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected January consumption savings')
    feb_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected February consumption savings')
    mar_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected March consumption savings')
    apr_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected April consumption savings')
    may_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected May consumption savings')
    jun_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected June consumption savings')
    jul_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected July consumption savings')
    aug_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected August consumption savings')
    sep_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected September consumption savings')
    oct_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected October consumption savings')
    nov_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected November consumption savings')
    dec_cons = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected December consumption savings')

    jan_peak = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected January peak demand savings')
    feb_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected February peak demand savings')
    mar_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected March peak demand savings')
    apr_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected April peak demand savings')
    may_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected May peak demand savings')
    jun_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected June peak demand savings')
    jul_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected July peak demand savings')
    aug_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected August peak demand savings')
    sep_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected September peak demand savings')
    oct_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected October peak demand savings')
    nov_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected November peak demand savings')
    dec_peak= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected December peak demand savings')

    jan_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected January cost savings')
    feb_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected February cost savings')
    mar_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected March cost savings')
    apr_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected April cost savings')
    may_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected May cost savings')
    jun_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected June cost savings')
    jul_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected July cost savings')
    aug_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected August cost savings')
    sep_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected September cost savings')
    oct_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected October cost savings')
    nov_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected November cost savings')
    dec_cost= models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=3,
                              help_text='expected December cost savings')
    
    #relationships
    messages = models.ManyToManyField('Message')
    meters = models.ManyToManyField('Meter', through='EMMeterApportionment')
    equipments = models.ManyToManyField('Equipment', through='EMEquipmentApportionment')
    weather_station = models.ForeignKey('WeatherStation')

    #functions
    def show_measure(self):
        """No inputs.  Prints
        measure properties."""
        print_string = ('name = ' + self.name + '\n' +
                'when = ' + self.when.strftime('%Y-%m-%d_%H-%M') + '\n' +
                'annual consumption savings = ' + str(self.annual_consumption_savings) + '\n' +
                'peak demand savings = ' + str(self.peak_demand_savings) + '\n' +
                'annual cost savings = ' + str(self.annual_cost_savings) + '\n' +
                '% cooling related = ' + str(self.percent_cool) + '\n' +
                '% heating related = ' + str(self.percent_heat) + '\n' +
                '% flat (daily) = ' + str(self.percent_flat) + '\n' +
                '% fixed (monthly) = ' + str(self.percent_fixed) + '\n' +
                'utility type = ' + self.utility_type + '\n' +
                'utility units = ' + self.units)
        print print_string
        return print_string
    def apportion_savings(self, Tccp=None, Thcp=None):
        """Converts annual savings
        amounts from model into
        monthly amounts based on
        percent cool, heat, and
        flat values."""
        
        try:
            df = pd.DataFrame({'Days': [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]},
                             index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
            if Tccp is None: Tccp = 65.0
            if Thcp is None: Thcp = 65.0
            dd = self.weather_station.get_average_monthly_degree_days(Tccp, Thcp)
            df['CDD'] = dd['CDD']
            df['HDD'] = dd['HDD']
            
            df['flat'] = (df['Days']/365.0).apply(Decimal) * self.percent_flat
            df['cool'] = (df['CDD']/df['CDD'].sum()).apply(Decimal) * self.percent_cool
            df['heat'] = (df['HDD']/df['HDD'].sum()).apply(Decimal) * self.percent_heat
            numlist = [1.0/12.0, 1.0/12.0, 1.0/12.0, 1.0/12.0, 1.0/12.0, 1.0/12.0, 
                                     1.0/12.0, 1.0/12.0, 1.0/12.0, 1.0/12.0, 1.0/12.0, 1.0/12.0]
            df['fixed'] = pd.Series([float(self.percent_fixed) * x for x in numlist], index=df.index).apply(Decimal)
            
            self.jan_cons = (df['flat'][0] + df['heat'][0] + df['cool'][0] + df['fixed'][0]) * self.annual_consumption_savings
            self.feb_cons = (df['flat'][1] + df['heat'][1] + df['cool'][1] + df['fixed'][1]) * self.annual_consumption_savings
            self.mar_cons = (df['flat'][2] + df['heat'][2] + df['cool'][2] + df['fixed'][2]) * self.annual_consumption_savings
            self.apr_cons = (df['flat'][3] + df['heat'][3] + df['cool'][3] + df['fixed'][3]) * self.annual_consumption_savings
            self.may_cons = (df['flat'][4] + df['heat'][4] + df['cool'][4] + df['fixed'][4]) * self.annual_consumption_savings
            self.jun_cons = (df['flat'][5] + df['heat'][5] + df['cool'][5] + df['fixed'][5]) * self.annual_consumption_savings
            self.jul_cons = (df['flat'][6] + df['heat'][6] + df['cool'][6] + df['fixed'][6]) * self.annual_consumption_savings
            self.aug_cons = (df['flat'][7] + df['heat'][7] + df['cool'][7] + df['fixed'][7]) * self.annual_consumption_savings
            self.sep_cons = (df['flat'][8] + df['heat'][8] + df['cool'][8] + df['fixed'][8]) * self.annual_consumption_savings
            self.oct_cons = (df['flat'][9] + df['heat'][9] + df['cool'][9] + df['fixed'][9]) * self.annual_consumption_savings
            self.nov_cons = (df['flat'][10] + df['heat'][10] + df['cool'][10] + df['fixed'][10]) * self.annual_consumption_savings
            self.dec_cons = (df['flat'][11] + df['heat'][11] + df['cool'][11] + df['fixed'][11]) * self.annual_consumption_savings

            self.jan_peak = (df['flat'][0] + df['heat'][0] + df['cool'][0] + df['fixed'][0]) * self.peak_demand_savings
            self.feb_peak = (df['flat'][1] + df['heat'][1] + df['cool'][1] + df['fixed'][1]) * self.peak_demand_savings
            self.mar_peak = (df['flat'][2] + df['heat'][2] + df['cool'][2] + df['fixed'][2]) * self.peak_demand_savings
            self.apr_peak = (df['flat'][3] + df['heat'][3] + df['cool'][3] + df['fixed'][3]) * self.peak_demand_savings
            self.may_peak = (df['flat'][4] + df['heat'][4] + df['cool'][4] + df['fixed'][4]) * self.peak_demand_savings
            self.jun_peak = (df['flat'][5] + df['heat'][5] + df['cool'][5] + df['fixed'][5]) * self.peak_demand_savings
            self.jul_peak = (df['flat'][6] + df['heat'][6] + df['cool'][6] + df['fixed'][6]) * self.peak_demand_savings
            self.aug_peak = (df['flat'][7] + df['heat'][7] + df['cool'][7] + df['fixed'][7]) * self.peak_demand_savings
            self.sep_peak = (df['flat'][8] + df['heat'][8] + df['cool'][8] + df['fixed'][8]) * self.peak_demand_savings
            self.oct_peak = (df['flat'][9] + df['heat'][9] + df['cool'][9] + df['fixed'][9]) * self.peak_demand_savings
            self.nov_peak = (df['flat'][10] + df['heat'][10] + df['cool'][10] + df['fixed'][10]) * self.peak_demand_savings
            self.dec_peak = (df['flat'][11] + df['heat'][11] + df['cool'][11] + df['fixed'][11]) * self.peak_demand_savings

            self.jan_cost = (df['flat'][0] + df['heat'][0] + df['cool'][0] + df['fixed'][0]) * self.annual_cost_savings
            self.feb_cost = (df['flat'][1] + df['heat'][1] + df['cool'][1] + df['fixed'][1]) * self.annual_cost_savings
            self.mar_cost = (df['flat'][2] + df['heat'][2] + df['cool'][2] + df['fixed'][2]) * self.annual_cost_savings
            self.apr_cost = (df['flat'][3] + df['heat'][3] + df['cool'][3] + df['fixed'][3]) * self.annual_cost_savings
            self.may_cost = (df['flat'][4] + df['heat'][4] + df['cool'][4] + df['fixed'][4]) * self.annual_cost_savings
            self.jun_cost = (df['flat'][5] + df['heat'][5] + df['cool'][5] + df['fixed'][5]) * self.annual_cost_savings
            self.jul_cost = (df['flat'][6] + df['heat'][6] + df['cool'][6] + df['fixed'][6]) * self.annual_cost_savings
            self.aug_cost = (df['flat'][7] + df['heat'][7] + df['cool'][7] + df['fixed'][7]) * self.annual_cost_savings
            self.sep_cost = (df['flat'][8] + df['heat'][8] + df['cool'][8] + df['fixed'][8]) * self.annual_cost_savings
            self.oct_cost = (df['flat'][9] + df['heat'][9] + df['cool'][9] + df['fixed'][9]) * self.annual_cost_savings
            self.nov_cost = (df['flat'][10] + df['heat'][10] + df['cool'][10] + df['fixed'][10]) * self.annual_cost_savings
            self.dec_cost = (df['flat'][11] + df['heat'][11] + df['cool'][11] + df['fixed'][11]) * self.annual_cost_savings
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='EfficiencyMeasure %s apportion_savings failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            self.save()
    def get_savings_dictionary(self):
        """No inputs.  Returns
        dictionary of consumption,
        demand, and cost savings
        by month number (1-12)."""
        d = {}
        d['1'] = {'Cost Savings': self.jan_cost,
                  'Consumption Savings': self.jan_cons,
                  'Peak Demand Savings': self.jan_peak}
        d['2'] = {'Cost Savings': self.feb_cost,
                  'Consumption Savings': self.feb_cons,
                  'Peak Demand Savings': self.feb_peak}
        d['3'] = {'Cost Savings': self.mar_cost,
                  'Consumption Savings': self.mar_cons,
                  'Peak Demand Savings': self.mar_peak}
        d['4'] = {'Cost Savings': self.apr_cost,
                  'Consumption Savings': self.apr_cons,
                  'Peak Demand Savings': self.apr_peak}
        d['5'] = {'Cost Savings': self.may_cost,
                  'Consumption Savings': self.may_cons,
                  'Peak Demand Savings': self.may_peak}
        d['6'] = {'Cost Savings': self.jun_cost,
                  'Consumption Savings': self.jun_cons,
                  'Peak Demand Savings': self.jun_peak}
        d['7'] = {'Cost Savings': self.jul_cost,
                  'Consumption Savings': self.jul_cons,
                  'Peak Demand Savings': self.jul_peak}
        d['8'] = {'Cost Savings': self.aug_cost,
                  'Consumption Savings': self.aug_cons,
                  'Peak Demand Savings': self.aug_peak}
        d['9'] = {'Cost Savings': self.sep_cost,
                  'Consumption Savings': self.sep_cons,
                  'Peak Demand Savings': self.sep_peak}
        d['10'] = {'Cost Savings': self.oct_cost,
                  'Consumption Savings': self.oct_cons,
                  'Peak Demand Savings': self.oct_peak}
        d['11'] = {'Cost Savings': self.nov_cost,
                  'Consumption Savings': self.nov_cons,
                  'Peak Demand Savings': self.nov_peak}
        d['12'] = {'Cost Savings': self.dec_cost,
                  'Consumption Savings': self.dec_cons,
                  'Peak Demand Savings': self.dec_peak}
        return d
        
    def get_savings_df(self,df):
        """function(df)
        
        Given dataframe with
        monthly index, returns
        dataframe with new
        columns for consumption
        savings, peak demand
        savings, and cost
        savings."""
        try:
            d = self.get_savings_dictionary()
            df['Consumption Savings'] = Decimal(0.0)
            df['Peak Demand Savings'] = Decimal(0.0)
            df['Cost Savings'] = Decimal(0.0)
            for i in df.index:
                df['Consumption Savings'][i:i+1] = d[str(i.month)]['Consumption Savings']
                df['Peak Demand Savings'][i:i+1] = d[str(i.month)]['Peak Demand Savings']
                df['Cost Savings'][i:i+1] = d[str(i.month)]['Cost Savings']
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='EfficiencyMeasure %s get_savings_df failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    
    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'BuildingSpeakApp'
