#import dbarray
import numpy as np
import pandas as pd
from pytz import UTC
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


class MeterConsumptionModel(models.Model):
    """Regression model for use
    with monthly bill
    consumption data.
    
    Minimum first_month and
    last_month, then call
    set_best_model() function."""
    
    model_type = models.CharField(blank=True, max_length=200,
                                    choices=[('1p','1p'),
                                             ('2pc','2pc'),
                                             ('2ph','2ph'),
                                             ('3phc','3phc'),
                                             ('3phx','3phx'),
                                             ('3pcx','3pcx'),
                                             ('4phcx','4phcx'),
                                                         ])
    first_month = models.CharField(blank=True, max_length=10, help_text='first month of baseline period, MM/YYYY')
    last_month = models.CharField(blank=True, max_length=10, help_text='last month of baseline period, MM/YYYY')
    Tccp = models.FloatField(null=True, blank=True, help_text='model cooling change point temperature, ' + u"\u00b0" + 'F')
    Thcp = models.FloatField(null=True, blank=True, help_text='model heating change point temperature, ' + u"\u00b0" + 'F')
    prediction_alpha = models.FloatField(null=True, blank=True, default=0.10,
                                         help_text='alpha to set (1-alpha) confidence prediction intervals (default=0.10)')
    
    #relationships
    meter = models.ForeignKey('Meter', null=True)
    messages = models.ManyToManyField('Message')
    
    #model parameters
    beta00p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_00')
    beta01p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_01')
    beta02p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_02')
    beta03p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_03')
    beta04p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_04')
    beta05p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_05')
    beta06p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_06')
    beta07p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_07')
    beta08p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_08')
    beta09p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_09')
    beta10p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_10')

    #model parameters' associated independent variable names
    beta00v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_00')
    beta01v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_01')
    beta02v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_02')
    beta03v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_03')
    beta04v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_04')
    beta05v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_05')
    beta06v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_06')
    beta07v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_07')
    beta08v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_08')
    beta09v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_09')
    beta10v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_10')

    #model fit stats
    r_squared = models.FloatField(null=True, blank=True, help_text='R^2')
    adj_r_squared = models.FloatField(null=True, blank=True, help_text='adjusted R^2')
    p = models.FloatField(null=True, blank=True, help_text='number of parameters')
    df = models.FloatField(null=True, blank=True, help_text='degrees of freedom')
    Yavg = models.FloatField(null=True, blank=True, help_text='average of dependent variable')
    SSQres = models.FloatField(null=True, blank=True, help_text='sum of squares, residuals')

    rmse = models.FloatField(null=True, blank=True, help_text='root mean squared error')
    cvrmse = models.FloatField(null=True, blank=True, help_text='coefficient of variation of RMSE')
    nbe = models.FloatField(null=True, blank=True, help_text='net determination bias error')
    F_stat = models.FloatField(null=True, blank=True, help_text='F-statistic')
    F_stat_p_value = models.FloatField(null=True, blank=True, help_text='F-statistic p-value')
    autocorr_coeff = models.FloatField(null=True, blank=True, help_text='autocorrelation coefficient')
    acceptance_score = models.FloatField(null=True, blank=True, help_text='acceptance score used for ranking and selecting models')

    #beta00 stats
    beta00_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta00')
    beta00_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta00')
    beta00_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta00')
    beta00_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta00')
    #beta01 stats
    beta01_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta01')
    beta01_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta01')
    beta01_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta01')
    beta01_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta01')
    #beta02 stats
    beta02_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta02')
    beta02_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta02')
    beta02_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta02')
    beta02_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta02')
    #beta03 stats
    beta03_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta03')
    beta03_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta03')
    beta03_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta03')
    beta03_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta03')
    #beta04 stats
    beta04_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta04')
    beta04_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta04')
    beta04_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta04')
    beta04_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta04')
    #beta05 stats
    beta05_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta05')
    beta05_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta05')
    beta05_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta05')
    beta05_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta05')
    #beta06 stats
    beta06_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta06')
    beta06_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta06')
    beta06_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta06')
    beta06_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta06')
    #beta07 stats
    beta07_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta07')
    beta07_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta07')
    beta07_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta07')
    beta07_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta07')
    #beta08 stats
    beta08_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta08')
    beta08_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta08')
    beta08_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta08')
    beta08_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta08')
    #beta09 stats
    beta09_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta09')
    beta09_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta09')
    beta09_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta09')
    beta09_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta09')
    #beta10 stats
    beta10_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta10')
    beta10_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta10')
    beta10_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta10')
    beta10_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta10')
    
    #functions
    def get_model_residuals_as_table(self):
        """No inputs.
        
        Returns table of model residuals
        as list of lists for use in
        html template."""
        results = self.get_model()
        resid_table = [['Independent Variable', 'Residual']]
        resid_table.extend([[results.model.exog[:,1][i],results.resid[i]] for i in range(0,len(results.resid))])
        return resid_table
        
    def get_model_stats_as_table(self):
        """No inputs.
        
        Returns table of model stats
        as list of lists for use in
        html template."""
        stats_list = [ ['Parameter', 'Value'],
                       ['Model Type', str(self.model_type)],
                       ['Baseline Period', str(self.first_month + ' - ' + self.last_month)],
                       ['Change Point Temps (degrees F): cool,heat', str(self.Tccp) + ', ' + str(self.Thcp)],
                       ['Prediction Interval alpha', str(self.prediction_alpha)],
                       ['R-squared', str(self.r_squared)],
                       ['Adjusted R-squared', str(self.adj_r_squared)],
                       ['Number of Parameters', str(self.p)],
                       ['Degrees of Freedom', str(self.df)],
                       ['Average of Dependent Variable', str(self.Yavg)],
                       ['Sum of Squares, Residuals', str(self.SSQres)],
                       ['Root Mean Squared Error', str(self.rmse)],
                       ['Coeff. of Variation of RMSE', str(self.cvrmse)],
                       ['Net Determination Bias Error', str(self.nbe)],
                       ['F-statistic', str(self.F_stat)],
                       ['F-statistic p-value', str(self.F_stat_p_value)],
                       ['Autocorrelation Coefficient', str(self.autocorr_coeff)],
                       ['Acceptance Score', str(self.acceptance_score)] ]
        return stats_list
    
    def prep_df(self, df):
        """function(df)
        
        Returns, based on
        model type, the given
        dataframe with the
        additional columns
        needed to run model
        functions."""
        #for updates: look at set_best_model and add code as needed to ensure presence of
        #    needed columns for new models
        try:
            current_model = self.get_available_models()[1][self.model_type]
            if current_model['wname'] == ['Days']:
                df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
            if 'CDD (consumption)/day' in current_model['xnames']:
                df = df.drop(['CDD (consumption)'], axis = 1)
                df = self.meter.weather_station.get_CDD_df(df, self.Tccp)
                df.rename(columns={'CDD': 'CDD (consumption)'}, inplace = True)
                df['CDD (consumption)/day'] = df['CDD (consumption)']/df['Days']
            if 'HDD (consumption)/day' in current_model['xnames']:
                df = df.drop(['HDD (consumption)'], axis = 1)
                df = self.meter.weather_station.get_HDD_df(df, self.Thcp)
                df.rename(columns={'HDD': 'HDD (consumption)'}, inplace = True)
                df['HDD (consumption)/day'] = df['HDD (consumption)']/df['Days']
            if 'consumption/day' in current_model['yname']:
                df['consumption/day'] = df['Consumption (act)']/df['Days']
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterConsumptionModel %s, prep_df failed, returning original dataframe.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    
    def get_available_models(self):
        """No inputs.  Returns
        dictionary of supported
        model types."""
        model_dictionary = {
            '1p': {'include_intercept': True,
                   'wname': ['Days'],
                   'xnames': [],
                   'yname': ['consumption/day']},
            '2pc': {'include_intercept': True,
                    'wname': ['Days'],
                    'xnames': ['CDD (consumption)/day'],
                    'yname': ['consumption/day']},
            '2ph': {'include_intercept': True,
                    'wname': ['Days'],
                    'xnames': ['HDD (consumption)/day'],
                    'yname': ['consumption/day']}  }
        model_name_list = [x for x in model_dictionary]
        return [model_name_list, model_dictionary]
    def get_model_specs(self, model_type=None):
        """function(model_type=None)
        
        Returns variable names
        and parameter values
        for the given model or
        the calling model's set
        model type (if given is
        None).  These names are
        needed for modeling
        functions."""
        try:
            if model_type is None: model_type = self.model_type
            pred_alpha = self.prediction_alpha
            wname = self.get_available_models()[1][self.model_type]['wname']
            xnames = self.get_available_models()[1][self.model_type]['xnames']
            yname = self.get_available_models()[1][self.model_type]['yname']
            include_intercept = self.get_available_models()[1][self.model_type]['include_intercept']
            answer = [include_intercept, wname, xnames, yname, pred_alpha]
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='MeterConsumptionModel %s, get_model_specs failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            answer = None
        return answer
        
    def show_properties(self):
        """No inputs.  Prints
        first/last month,
        Tccp/Thcp, and type."""
        print ('First Month = ' + self.first_month + '\n' + 
               'Last Month = ' + self.last_month + '\n' +
               'Tccp = ' + str(self.Tccp) + '\n' + 
               'Thcp = ' + str(self.Thcp) + '\n' +
               'Model Type = ' + self.model_type)
    def get_average_baseline_degree_days(self, Tccp=None, Thcp=None):
        """function(Tccp=None, Thcp=None)
        
        Return annual average
        monthly HDD and CDD
        given change point 
        temperatures (defaults
        to model's temperatures)
        and baseline period as
        defined by model's first
        and last months."""
        try:
            if Tccp is None: Tccp = self.Tccp
            if Thcp is None: Thcp = self.Thcp
            df = self.get_baseline_df()
            df = df.drop(['CDD (consumption)', 'HDD (consumption)'], axis = 1)
            df = self.meter.weather_station.get_CDD_df(df, Tccp)
            df.rename(columns={'CDD': 'CDD (consumption)'}, inplace = True)
            df = self.meter.weather_station.get_HDD_df(df, Thcp)
            df.rename(columns={'HDD': 'HDD (consumption)'}, inplace = True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterConsumptionModel %s get_average_baseline_degree_days failed to calculate or load degree days into dataframe, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df_avg = None
        else:
            if len(df)<12:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='MeterConsumptionModel %s get_average_baseline_degree_days found less than 12-month baseline period, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df_avg = None
            else:
                df = df.sort_index()
                df_avg = df[0:12]
                for i in range(0,12):
                    df_avg['CDD (consumption)'][i:i+1] = df['CDD (consumption)'][[x.month==df.index[i].month for x in df.index]].mean()
                    df_avg['HDD (consumption)'][i:i+1] = df['HDD (consumption)'][[x.month==df.index[i].month for x in df.index]].mean()
                df_avg = df_avg.sort_index()
        return df_avg
         
    def get_baseline_df(self):
        """No inputs.  Return
        bill data dataframe
        for baseline period of
        MeterConsumptionModel."""
        if self.first_month is None or self.last_month is None:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Bad inputs.',
                        comment='MeterConsumptionModel %s, get_baseline_df given inappropriate first/last months for range, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:            
            try:
                df = self.meter.get_bill_data_period_dataframe(first_month = self.first_month,
                                                               last_month = self.last_month)
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Retrieve data failed.',
                            comment='MeterConsumptionModel %s, get_baseline_df failed, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df = None
        return df
        
    def get_model_calc_dict(self):
        """No inputs.  Return
        dictionary of
        independent variable
        names and associated
        model parameter
        values."""
        d = {}
        if self.beta00p is not None: d[self.beta00v] = self.beta00p
        if self.beta01p is not None: d[self.beta01v] = self.beta01p
        if self.beta02p is not None: d[self.beta02v] = self.beta02p
        if self.beta03p is not None: d[self.beta03v] = self.beta03p
        if self.beta04p is not None: d[self.beta04v] = self.beta04p
        if self.beta05p is not None: d[self.beta05v] = self.beta05p
        if self.beta06p is not None: d[self.beta06v] = self.beta06p
        if self.beta07p is not None: d[self.beta07v] = self.beta07p
        if self.beta08p is not None: d[self.beta08v] = self.beta08p
        if self.beta09p is not None: d[self.beta09v] = self.beta09p
        if self.beta10p is not None: d[self.beta10v] = self.beta10p
        return d
    
    def get_params_list(self):
        """No inputs.  Returns
        list of model parameter
        names (unused are None)."""
        return [self.beta00p, self.beta01p, self.beta02p, self.beta03p, self.beta04p, self.beta05p,
                self.beta06p, self.beta07p, self.beta08p, self.beta09p, self.beta10p]
    def get_params_pvalue_list(self):
        """No inputs.  Returns
        list of p-values
        (significance testing)
        for model parameters.
        
        Used in acceptance
        score to penalize
        models with
        insignificant model
        parameters."""
        return [self.beta00_p_value, self.beta01_p_value, self.beta02_p_value, self.beta03_p_value,
                self.beta04_p_value, self.beta05_p_value, self.beta06_p_value, self.beta07_p_value,
                self.beta08_p_value, self.beta09_p_value, self.beta10_p_value]
    def get_param_count(self):
        """No inputs.  Returns
        total count of used
        parameters in a model
        (inc. constant term)."""
        return sum([x is not None for x in self.get_params_list()])
    def get_max_param_p_value(self):
        """No inputs.  Returns
        highest significance
        test p-value of model
        parameters.
        
        Used in acceptance score
        to penalize models with
        insignificant model
        parameters."""
        return max(self.get_params_pvalue_list())
    def get_min_param(self):
        """No inputs.  Returns
        minimum model parameter
        value.
        
        Used in acceptance score
        to penalize negative
        model parameter values."""
        return min(self.get_params_list())
    def set_accept_score(self):
        """No inputs.  Returns
        a goodness of fit score
        based on statistical
        results of regression.
        
        Used to select the model
        appearing to be the most
        appropriate (not
        necessarily the most
        accurate or highest R^2)
        fit to the data."""
        self.acceptance_score = (
            1 * (-1*(self.adj_r_squared < 0.5) + 1*(self.adj_r_squared > 0.85)) +
            1 * (-1*(self.F_stat_p_value > 0.1) + 1*(self.F_stat_p_value < 0.01)) +
            1 * (-1*(self.get_max_param_p_value() > 0.1) + 1*(self.get_max_param_p_value() < 0.01)) +
            1 * (10 - self.get_param_count()) +
            1 * (min(0, np.sign(self.get_min_param())))  )
        return self.acceptance_score
        
    def set_best_model(self):
        """No inputs.  Runs
        through battery of
        model types at
        Tccp=Thcp=65 to find
        most appropriate model
        type.  Then runs through
        temperature range finding
        most appropriate change
        point temperatures."""
        
        available_models = self.get_available_models()
        track_runs = pd.DataFrame()
        track_Tccp = pd.DataFrame()
        track_Thcp = pd.DataFrame()
        best_run_results = None
        try:
            Tccp = Thcp = 65
            #not using prep_df, instead loading all needed columns once and then cycling through
            #as new models are added, need to add code here to make sure the new models are
            #    included in the search for the best fit model
            df = self.get_baseline_df()
            df = df.drop(['CDD (consumption)', 'HDD (consumption)'], axis = 1)
            df = self.meter.weather_station.get_CDD_df(df, Tccp)
            df.rename(columns={'CDD': 'CDD (consumption)'}, inplace = True)
            df = self.meter.weather_station.get_HDD_df(df, Thcp)
            df.rename(columns={'HDD': 'HDD (consumption)'}, inplace = True)
            df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
            df['CDD (consumption)/day'] = df['CDD (consumption)']/df['Days']
            df['HDD (consumption)/day'] = df['HDD (consumption)']/df['Days']
            df['consumption/day'] = df['Consumption (act)']/df['Days']
            #--------------------------------------------------------------------------
            df = df.sort_index()
            
            #first run through models to find best model type at constant change point temperatures
            for run in available_models[0]:
                try:
                    results = self.set_model_print_results(df = df,
                                            wname = available_models[1][run]['wname'],
                                            xnames = available_models[1][run]['xnames'],
                                            yname = available_models[1][run]['yname'],
                                            include_intercept = available_models[1][run]['include_intercept'])
                    if results is not None:
                        track_runs = track_runs.append(pd.DataFrame({'id': run,
                                                                     'Tccp': Tccp,
                                                                     'Thcp': Thcp,
                                                                     'acceptance_score': self.acceptance_score},
                                                                     index=[run + str(Tccp) + str(Thcp)]))
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Model run failed.',
                                comment='MeterConsumptionModel %s set_best_model failed on %s-%s-%s, function aborted.' % (self.id, run, str(Tccp), str(Thcp)))
                    m.save()
                    self.messages.add(m)
                    print m
            best_score = track_runs['acceptance_score'].max()
            if track_runs['acceptance_score'][track_runs['acceptance_score']==best_score].count() > 1:
                m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Non-unique result.',
                            comment='MeterConsumptionModel %s set_best_model found multiple models with the highest acceptance score.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            best_run = track_runs['acceptance_score'].idxmax()
            best_type = track_runs['id'][best_run]
            best_Tccp = best_Thcp = 65 #set here so final setting of best model can use; if needed, will be overwritten first
            
            #then, if model contains cooling term(s), find best Tccp
            if 'c' in best_type:
                try:
                    track_Tccp = pd.DataFrame()            
                    Thcp = 65
                    df = self.get_baseline_df()
                    df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
                    df['consumption/day'] = df['Consumption (act)']/df['Days']
                    df = df.drop(['HDD (consumption)'], axis = 1)
                    df = self.meter.weather_station.get_HDD_df(df, Thcp)
                    df.rename(columns={'HDD': 'HDD (consumption)'}, inplace = True)
                    df['HDD (consumption)/day'] = df['HDD (consumption)']/df['Days']
                    for Tccp in range(55, 96):
                        #must call/create here so that all wname, xnames, and ynames are in df-----
                        df = df.drop(['CDD (consumption)'], axis = 1)
                        df = self.meter.weather_station.get_CDD_df(df, Tccp)
                        df.rename(columns={'CDD': 'CDD (consumption)'}, inplace = True)
                        df['CDD (consumption)/day'] = df['CDD (consumption)']/df['Days']
                        #--------------------------------------------------------------------------
                        df = df.sort_index()
                        results = self.set_model_print_results(df = df,
                              wname = available_models[1][best_type]['wname'],
                              xnames = available_models[1][best_type]['xnames'],
                              yname = available_models[1][best_type]['yname'],
                              include_intercept = available_models[1][best_type]['include_intercept'])
                        track_Tccp = track_Tccp.append(pd.DataFrame({'Tccp': Tccp,
                                                                     'Thcp': Thcp,
                                                                     'adj_r_squared': self.adj_r_squared},
                                                                     index=[str(self.adj_r_squared) + str(Tccp) + str(Thcp)]))
                        best_Tccp_run = track_Tccp['adj_r_squared'].idxmax()
                        best_Tccp = track_Tccp['Tccp'][best_Tccp_run]
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Calculation failed.',
                                comment='MeterConsumptionModel %s set_best_model unable to calculate Tccp range, function aborted.' % (self.id))
                    m.save()
                    self.messages.add(m)
                    print m
            else:
                track_Tccp = None
                
            #then, if model contains heating term(s), find best Thcp
            if 'h' in best_type:
                try:
                    track_Thcp = pd.DataFrame()            
                    Tccp = 65
                    df = self.get_baseline_df()
                    df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
                    df['consumption/day'] = df['Consumption (act)']/df['Days']
                    df = df.drop(['CDD (consumption)'], axis = 1)
                    df = self.meter.weather_station.get_CDD_df(df, Tccp)
                    df.rename(columns={'CDD': 'CDD (consumption)'}, inplace = True)
                    for Thcp in range(55, 80):
                        #must call/create here so that all wname, xnames, and ynames are in df-----
                        df = df.drop(['HDD (consumption)'], axis = 1)
                        df = self.meter.weather_station.get_HDD_df(df, Thcp)
                        df.rename(columns={'HDD': 'HDD (consumption)'}, inplace = True)
                        df['HDD (consumption)/day'] = df['HDD (consumption)']/df['Days']
                        #--------------------------------------------------------------------------
                        df = df.sort_index()
                        results = self.set_model_print_results(df = df,
                              wname = available_models[1][best_type]['wname'],
                              xnames = available_models[1][best_type]['xnames'],
                              yname = available_models[1][best_type]['yname'],
                              include_intercept = available_models[1][best_type]['include_intercept'])
                        track_Thcp = track_Thcp.append(pd.DataFrame({'Tccp': Tccp,
                                                                     'Thcp': Thcp,
                                                                     'adj_r_squared': self.adj_r_squared},
                                                                     index=[str(self.adj_r_squared) + str(Tccp) + str(Thcp)]))
                        best_Thcp_run = track_Thcp['adj_r_squared'].idxmax()
                        best_Thcp = track_Thcp['Tccp'][best_Thcp_run]
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Calculation failed.',
                                comment='MeterConsumptionModel %s set_best_model unable to calculate Thcp range, function aborted.' % (self.id))
                    m.save()
                    self.messages.add(m)
                    print m
            else:
                track_Thcp = None

            #now run best model based on findings from code above
            #must call/create here so that all wname, xnames, and ynames are in df-----
            self.model_type = best_type
            self.Tccp = best_Tccp
            self.Thcp = best_Thcp
            df = self.get_baseline_df()
            df = self.prep_df(df)
            df = df.sort_index()
            best_run_results = self.set_model_print_results(df = df,
                              wname = available_models[1][best_type]['wname'],
                              xnames = available_models[1][best_type]['xnames'],
                              yname = available_models[1][best_type]['yname'],
                              include_intercept = available_models[1][best_type]['include_intercept'])
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Model update failed.',
                        comment='MeterConsumptionModel %s set_best_model failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        self.save()
        return track_runs, track_Tccp, track_Thcp, best_run_results
        
    def set_model_print_results(self, df, wname, xnames, yname, include_intercept=True):
        """function(df,wname,xnames,
                    yname,include_intercept=True)
        Regresses xnames independent
        variables against yname
        dependent variable with
        weighting factors wname,
        with indicator for whether
        to include constant term.
        Prints model summary and
        acceptance score.
        
        df = dataframe
        wname = list
        xnames = list
        yname = list
        inc._int. = bool."""
        try:
            results = self.set_model(df, wname, xnames, yname, include_intercept)
            print results.summary()
            print 'acceptance score = ' + str(self.set_accept_score())
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterConsumptionModel %s, set_model_print_results failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        return results
    def get_model(self):
        """No inputs. Returns
        model results object
        using model's current
        attributes."""
        try:
            if self.model_type is None: raise TypeError
            wname = self.get_available_models()[1][self.model_type]['wname']
            xnames = self.get_available_models()[1][self.model_type]['xnames']
            yname = self.get_available_models()[1][self.model_type]['yname']
            include_intercept = self.get_available_models()[1][self.model_type]['include_intercept']
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Model not set.',
                        comment='MeterConsumptionModel %s get_model failed because model is not set, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        else:
            try:
                df = self.get_baseline_df()
                df = self.prep_df(df)
                df = df.sort_index()

                #had trouble with Decimals vs. Floats, so converting for model functions
                Y = df[yname].applymap(float).__array__()                   #create dependent variable vector; here only one
                X = df[xnames].applymap(float).__array__()                  #create independent variable(s) vector
                w = df[wname].applymap(float).__array__()                   #create weighting vector, e.g. 'days in period'
                if include_intercept: X = sm.add_constant(X, prepend = True)      #beta[0] will be constant term when prepend=True
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Retrieve data failed.',
                            comment='MeterConsumptionModel %s, get_model function failed to prepare regression inputs, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                results = None
            else:
                try:
                    results = sm.WLS(Y, X, weights = w).fit()
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Unable to run regression.',
                                comment='MeterConsumptionModel %s, get_model function failed to run regression, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    results = None
        return results

    def set_model(self, df, wname, xnames, yname, include_intercept=True):
        """function(df,wname,xnames,
                    yname,include_intercept=True)
        Regresses xnames independent
        variables against yname
        dependent variable with
        weighting factors wname,
        with indicator for whether
        to include constant term.
        
        df = dataframe
        wname = list
        xnames = list
        yname = list
        inc._int. = bool."""
        try:
            if not(  min([x in df.columns for x in wname]) and 
                     (len(xnames)==0 or min([x in df.columns for x in xnames])) and 
                     min([x in df.columns for x in yname]) ):
                raise ValueError
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='MeterConsumptionModel %s, set_model function given improper inputs, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        else:
            try:
                df = df.sort_index()
                #had trouble with Decimals vs. Floats, so converting for model functions
                Y = df[yname].applymap(float).__array__()                   #create dependent variable vector; here only one
                X = df[xnames].applymap(float).__array__()                  #create independent variable(s) vector
                w = df[wname].applymap(float).__array__()                   #create weighting vector, e.g. 'days in period'
                if include_intercept: X = sm.add_constant(X, prepend = True)      #beta[0] will be constant term when prepend=True
                results = sm.WLS(Y, X, weights = w).fit()
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Unable to run regression.',
                            comment='MeterConsumptionModel %s, set_model function failed to run regression, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                results = None
            else:
                if len(results.params)>0: 
                    self.beta00p = results.params[0]
                    if include_intercept:
                        self.beta00v = 'constant'
                    else:
                        self.beta00v = xnames[0]
                    self.beta00_se = results.bse[0]
                    self.beta00_t_stat = results.tvalues[0]
                    self.beta00_p_value = results.pvalues[0]
                    self.beta00_95_conf_int = results.params[0] - results.conf_int(alpha=0.05)[0][0]
                if len(results.params)>1: 
                    self.beta01p = results.params[1]
                    if include_intercept:
                        self.beta01v = xnames[0]
                    else:
                        self.beta01v = xnames[1]
                    self.beta01_se = results.bse[1]
                    self.beta01_t_stat = results.tvalues[1]
                    self.beta01_p_value = results.pvalues[1]
                    self.beta01_95_conf_int = results.params[1] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>2:
                    self.beta02p = results.params[2]
                    if include_intercept:
                        self.beta02v = xnames[1]
                    else:
                        self.beta02v = xnames[2]
                    self.beta02_se = results.bse[2]
                    self.beta02_t_stat = results.tvalues[2]
                    self.beta02_p_value = results.pvalues[2]
                    self.beta02_95_conf_int = results.params[2] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>3:
                    self.beta03p = results.params[3]
                    if include_intercept:
                        self.beta03v = xnames[2]
                    else:
                        self.beta03v = xnames[3]
                    self.beta03_se = results.bse[3]
                    self.beta03_t_stat = results.tvalues[3]
                    self.beta03_p_value = results.pvalues[3]
                    self.beta03_95_conf_int = results.params[3] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>4: 
                    self.beta04p = results.params[4]
                    if include_intercept:
                        self.beta04v = xnames[3]
                    else:
                        self.beta04v = xnames[4]
                    self.beta04_se = results.bse[4]
                    self.beta04_t_stat = results.tvalues[4]
                    self.beta04_p_value = results.pvalues[4]
                    self.beta04_95_conf_int = results.params[4] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>5: 
                    self.beta05p = results.params[5]
                    if include_intercept:
                        self.beta05v = xnames[4]
                    else:
                        self.beta05v = xnames[5]
                    self.beta05_se = results.bse[5]
                    self.beta05_t_stat = results.tvalues[5]
                    self.beta05_p_value = results.pvalues[5]
                    self.beta05_95_conf_int = results.params[5] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>6: 
                    self.beta06p = results.params[6]
                    if include_intercept:
                        self.beta06v = xnames[5]
                    else:
                        self.beta06v = xnames[6]
                    self.beta06_se = results.bse[6]
                    self.beta06_t_stat = results.tvalues[6]
                    self.beta06_p_value = results.pvalues[6]
                    self.beta06_95_conf_int = results.params[6] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>7: 
                    self.beta07p = results.params[7]
                    if include_intercept:
                        self.beta07v = xnames[6]
                    else:
                        self.beta07v = xnames[7]
                    self.beta07_se = results.bse[7]
                    self.beta07_t_stat = results.tvalues[7]
                    self.beta07_p_value = results.pvalues[7]
                    self.beta07_95_conf_int = results.params[7] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>8: 
                    self.beta08p = results.params[8]
                    if include_intercept:
                        self.beta08v = xnames[7]
                    else:
                        self.beta08v = xnames[8]
                    self.beta08_se = results.bse[8]
                    self.beta08_t_stat = results.tvalues[8]
                    self.beta08_p_value = results.pvalues[8]
                    self.beta08_95_conf_int = results.params[8] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>9: 
                    self.beta09p = results.params[9]
                    if include_intercept:
                        self.beta09v = xnames[8]
                    else:
                        self.beta09v = xnames[9]
                    self.beta09_se = results.bse[9]
                    self.beta09_t_stat = results.tvalues[9]
                    self.beta09_p_value = results.pvalues[9]
                    self.beta09_95_conf_int = results.params[9] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>10: 
                    self.beta10p = results.params[10]
                    if include_intercept:
                        self.beta10v = xnames[9]
                    else:
                        self.beta10v = xnames[10]
                    self.beta10_se = results.bse[10]
                    self.beta10_t_stat = results.tvalues[10]
                    self.beta10_p_value = results.pvalues[10]
                    self.beta10_95_conf_int = results.params[10] - results.conf_int(alpha=0.05)[1][1]
                
                self.p = len(results.params)
                self.n = len(df)
                self.df = len(df) - self.p
                self.Yavg = np.average(Y)
    
                self.r_squared = results.rsquared
                self.adj_r_squared = results.rsquared_adj
                self.SSQres = np.dot((Y.transpose()-results.fittedvalues)[0], (Y.transpose()-results.fittedvalues)[0])
                self.rmse = np.sqrt(self.SSQres/(self.n - self.p))
                self.cvrmse = self.rmse/self.Yavg
                self.F_stat = results.fvalue
                self.F_stat_p_value = results.f_pvalue
                s = pd.Series(results.resid)
                self.autocorr_coeff = np.sqrt( (s[1:].corr(s.shift(1)[1:]))**2 )
                
                
                self.nbe = np.sum(df[yname[0]].apply(float)*df[wname[0]].apply(float)-results.fittedvalues*df[wname[0]].apply(float))/np.sum(df[yname[0]].apply(float)*df[wname[0]].apply(float))
                
                self.first_month = df.index[0].strftime('%m/%Y')
                self.last_month = df.index[-1].strftime('%m/%Y')
                
                self.set_accept_score()
        self.save()
        return results

    def model_predict(self, res, exog=None, weights=None, alpha=0.10):
        """function(res,exog=None,weights=None,alpha=0.10)
        
        Adapted version of statsmodels
        wls_prediction_std function.
        Usage:
         predicted, prstd, iv_l, iv_u = ...
           function(results,
                    exog = array([[1,17],[1,18],[1,19]]),
                    weights = [32, 32, 32],
                    alpha=0.10)
        
        
        Calculate standard deviation
        and confidence interval for
        prediction.
        
        applies to WLS and OLS, not to general GLS,
        that is independently but not identically distributed observations
        
        Parameters
        ----------
        res : regression result instance
            results of WLS or OLS regression required attributes see notes
        exog : array_like (optional)
            exogenous variables for points to predict
        weights : scalar or array_like (optional)
            weights as defined for WLS (inverse of variance of observation)
        alpha : float (default: alpha = 0.10)
            confidence level for two-sided hypothesis
    
        Returns
        -------
        predstd : array_like, 1d
            standard error of prediction
            same length as rows of exog
        interval_l, interval_u : array_like
            lower und upper confidence bounds
    
        Notes
        -----
        The result instance needs to have at least the following
        res.model.predict() : predicted values or
        res.fittedvalues : values used in estimation
        res.cov_params() : covariance matrix of parameter estimates
    
        If exog is 1d, then it is interpreted as one observation,
        i.e. a row vector."""
        
        try:
            covb = res.cov_params()
            if exog is None:
                exog = res.model.exog
                predicted = res.fittedvalues
            else:
                exog = np.atleast_2d(exog)
                if covb.shape[1] != exog.shape[1]:
                    raise ValueError('wrong shape of exog')
                predicted = res.model.predict(res.params, exog)
        
            if weights is None:
                weights = res.model.weights
            
            predvar = res.mse_resid/weights + (exog * np.dot(covb, exog.T).T).sum(1)
            predstd = np.sqrt(predvar)
            tppf = stats.t.isf(alpha/2., res.df_resid)
            interval_u = predicted + tppf * predstd
            interval_l = predicted - tppf * predstd
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterConsumptionModel %s, model_predict function failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            predicted = predstd = interval_l = interval_u = None
        return predicted, predstd, interval_l, interval_u
    
    def model_predict_df(self, df, wname, xnames, include_intercept=True, alpha=0.10):
        """function(df,wname,xnames,
                    include_intercept=True,
                    alpha=0.10)
        Uses current model settings
        to retrieve CDD/HDD for df,
        calls get_model to
        retrieve results object,
        and creates appropriately
        formatted exog and weights
        arrays for passing to
        model_predict function."""

        try:
            df = df.sort_index()
            df = self.prep_df(df)

            #had trouble with Decimals vs. Floats, so converting for model functions
            X = df[xnames].applymap(float).__array__()                  #create independent variable(s) vector
            w = df[wname].applymap(float).__array__().flatten()                   #create weighting vector, e.g. 'days in period'
            if include_intercept: X = sm.add_constant(X, prepend = True)      #beta[0] will be constant term when prepend=True
            results = self.get_model()
            predicted_norm, predstd_norm, interval_l_norm, interval_u_norm = self.model_predict(res=results, exog=X, weights=w, alpha=alpha)
            predicted = predicted_norm * w
            predstd = predstd_norm * w
            interval_l = interval_l_norm * w
            interval_u = interval_u_norm * w
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterConsumptionModel %s, model_predict_df unable to calculate predictions, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        return predicted, predstd, interval_l, interval_u
        
    def current_model_predict_df(self, df):
        """function(df)
        
        Uses current model settings
        to construct needed inputs
        and call model_predict_df
        function."""

        try:
            df = self.prep_df(df)
            pred_alpha = self.prediction_alpha
            wname = self.get_available_models()[1][self.model_type]['wname']
            xnames = self.get_available_models()[1][self.model_type]['xnames']
            include_intercept = self.get_available_models()[1][self.model_type]['include_intercept']
            predicted, predstd, interval_l, interval_u = self.model_predict_df(df, wname, xnames, include_intercept, pred_alpha)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterConsumptionModel %s, current_model_predict_df unable to calculate predictions, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            predicted = predstd = interval_l = interval_u = None
        return predicted, predstd, interval_l, interval_u
    class Meta:
        app_label = 'BuildingSpeakApp'

class MeterPeakDemandModel(models.Model):
    """Regression model for use
    with monthly bill peak
    demand data.
    
    Minimum first_month and
    last_month, then call
    set_best_model() function."""
    
    model_type = models.CharField(blank=True, max_length=200,
                                    choices=[('1p','1p'),
                                             ('2pc','2pc'),
                                             ('2ph','2ph'),
                                             ('3phc','3phc'),
                                             ('3phx','3phx'),
                                             ('3pcx','3pcx'),
                                             ('4phcx','4phcx'),
                                                         ])
    first_month = models.CharField(blank=True, max_length=10, help_text='first month of baseline period, MM/YYYY')
    last_month = models.CharField(blank=True, max_length=10, help_text='last month of baseline period, MM/YYYY')
    Tccp = models.FloatField(null=True, blank=True, help_text='model cooling change point temperature, ' + u"\u00b0" + 'F')
    Thcp = models.FloatField(null=True, blank=True, help_text='model heating change point temperature, ' + u"\u00b0" + 'F')
    prediction_alpha = models.FloatField(null=True, blank=True, default=0.10,
                                         help_text='alpha to set (1-alpha) confidence prediction intervals (default=0.10)')
    
    #relationships
    meter = models.ForeignKey('Meter', null=True)
    messages = models.ManyToManyField('Message')
    
    #model parameters
    beta00p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_00')
    beta01p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_01')
    beta02p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_02')
    beta03p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_03')
    beta04p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_04')
    beta05p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_05')
    beta06p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_06')
    beta07p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_07')
    beta08p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_08')
    beta09p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_09')
    beta10p = models.FloatField(null=True, blank=True, help_text='value of parameter beta_10')

    #model parameters' associated independent variable names
    beta00v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_00')
    beta01v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_01')
    beta02v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_02')
    beta03v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_03')
    beta04v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_04')
    beta05v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_05')
    beta06v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_06')
    beta07v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_07')
    beta08v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_08')
    beta09v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_09')
    beta10v = models.CharField(blank=True, max_length=200, help_text='name of parameter beta_10')

    #model fit stats
    r_squared = models.FloatField(null=True, blank=True, help_text='R^2')
    adj_r_squared = models.FloatField(null=True, blank=True, help_text='adjusted R^2')
    p = models.FloatField(null=True, blank=True, help_text='number of parameters')
    df = models.FloatField(null=True, blank=True, help_text='degrees of freedom')
    Yavg = models.FloatField(null=True, blank=True, help_text='average of dependent variable')
    SSQres = models.FloatField(null=True, blank=True, help_text='sum of squares, residuals')

    rmse = models.FloatField(null=True, blank=True, help_text='root mean squared error')
    cvrmse = models.FloatField(null=True, blank=True, help_text='coefficient of variation of RMSE')
    nbe = models.FloatField(null=True, blank=True, help_text='net determination bias error')
    F_stat = models.FloatField(null=True, blank=True, help_text='F-statistic')
    F_stat_p_value = models.FloatField(null=True, blank=True, help_text='F-statistic p-value')
    autocorr_coeff = models.FloatField(null=True, blank=True, help_text='autocorrelation coefficient')
    acceptance_score = models.FloatField(null=True, blank=True, help_text='acceptance score used for ranking and selecting models')

    #beta00 stats
    beta00_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta00')
    beta00_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta00')
    beta00_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta00')
    beta00_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta00')
    #beta01 stats
    beta01_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta01')
    beta01_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta01')
    beta01_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta01')
    beta01_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta01')
    #beta02 stats
    beta02_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta02')
    beta02_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta02')
    beta02_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta02')
    beta02_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta02')
    #beta03 stats
    beta03_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta03')
    beta03_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta03')
    beta03_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta03')
    beta03_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta03')
    #beta04 stats
    beta04_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta04')
    beta04_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta04')
    beta04_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta04')
    beta04_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta04')
    #beta05 stats
    beta05_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta05')
    beta05_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta05')
    beta05_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta05')
    beta05_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta05')
    #beta06 stats
    beta06_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta06')
    beta06_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta06')
    beta06_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta06')
    beta06_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta06')
    #beta07 stats
    beta07_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta07')
    beta07_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta07')
    beta07_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta07')
    beta07_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta07')
    #beta08 stats
    beta08_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta08')
    beta08_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta08')
    beta08_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta08')
    beta08_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta08')
    #beta09 stats
    beta09_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta09')
    beta09_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta09')
    beta09_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta09')
    beta09_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta09')
    #beta10 stats
    beta10_se = models.FloatField(null=True, blank=True, help_text='standard error of coefficient, beta10')
    beta10_t_stat = models.FloatField(null=True, blank=True, help_text='t-statistic, beta10')
    beta10_p_value = models.FloatField(null=True, blank=True, help_text='p-value, beta10')
    beta10_95_conf_int = models.FloatField(null=True, blank=True, help_text='95%% confidence half-interval, beta10')
    
    #functions
    def get_model_residuals_as_table(self): ######need to add column for each ind. variable
        """No inputs.
        
        Returns table of model residuals
        as list of lists for use in
        html template."""
        results = self.get_model()
        resid_table = [['Independent Variable', 'Residual']]
        resid_table.extend([[results.model.exog[:,0][i],results.resid[i]] for i in range(0,len(results.resid))])
        return resid_table

    def get_model_stats_as_table(self):
        """No inputs.
        
        Returns table of model stats
        as list of lists for use in
        html template."""
        stats_list = [ ['Parameter', 'Value'],
                       ['Model Type', str(self.model_type)],
                       ['Baseline Period', str(self.first_month + ' - ' + self.last_month)],
                       ['Change Point Temps (degrees F): cool,heat', str(self.Tccp) + ', ' + str(self.Thcp)],
                       ['Prediction Interval alpha', str(self.prediction_alpha)],
                       ['R-squared', str(self.r_squared)],
                       ['Adjusted R-squared', str(self.adj_r_squared)],
                       ['Number of Parameters', str(self.p)],
                       ['Degrees of Freedom', str(self.df)],
                       ['Average of Dependent Variable', str(self.Yavg)],
                       ['Sum of Squares, Residuals', str(self.SSQres)],
                       ['Root Mean Squared Error', str(self.rmse)],
                       ['Coeff. of Variation of RMSE', str(self.cvrmse)],
                       ['Net Determination Bias Error', str(self.nbe)],
                       ['F-statistic', str(self.F_stat)],
                       ['F-statistic p-value', str(self.F_stat_p_value)],
                       ['Autocorrelation Coefficient', str(self.autocorr_coeff)],
                       ['Acceptance Score', str(self.acceptance_score)] ]
        return stats_list

    def prep_df(self, df):
        """function(df)
        
        Returns, based on
        model type, the given
        dataframe with the
        additional columns
        needed to run model
        functions."""
        #for updates: look at set_best_model and add code as needed to ensure presence of
        #    needed columns for new models
        try:
            current_model = self.get_available_models()[1][self.model_type]
            if current_model['wname'] == ['Days']:
                df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
            if 'CDD (peak demand)/day' in current_model['xnames']:
                df = df.drop(['CDD (peak demand)'], axis = 1)
                df = self.meter.weather_station.get_CDD_df(df, self.Tccp)
                df.rename(columns={'CDD': 'CDD (peak demand)'}, inplace = True)
                df['CDD (peak demand)/day'] = df['CDD (peak demand)']/df['Days']
            if 'HDD (peak demand)/day' in current_model['xnames']:
                df = df.drop(['HDD (peak demand)'], axis = 1)
                df = self.meter.weather_station.get_HDD_df(df, self.Thcp)
                df.rename(columns={'HDD': 'HDD (peak demand)'}, inplace = True)
                df['HDD (peak demand)/day'] = df['HDD (peak demand)']/df['Days']
            if 'peak demand/day' in current_model['yname']:
                df['peak demand/day'] = df['Peak Demand (act)']/df['Days']
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterPeakDemandModel %s, prep_df failed, returning original dataframe.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    
    def get_available_models(self):
        """No inputs.  Returns
        dictionary of supported
        model types."""
        model_dictionary = {
            '1p': {'include_intercept': True,
                   'wname': ['Days'],
                   'xnames': [],
                   'yname': ['peak demand/day']},
            '2pc': {'include_intercept': True,
                    'wname': ['Days'],
                    'xnames': ['CDD (peak demand)/day'],
                    'yname': ['peak demand/day']},
            '2ph': {'include_intercept': True,
                    'wname': ['Days'],
                    'xnames': ['HDD (peak demand)/day'],
                    'yname': ['peak demand/day']}  }
        model_name_list = [x for x in model_dictionary]
        return [model_name_list, model_dictionary]
    def get_model_specs(self, model_type=None):
        """function(model_type=None)
        
        Returns variable names
        and parameter values
        for the given model or
        the calling model's set
        model type (if given is
        None).  These names are
        needed for modeling
        functions."""
        try:
            if model_type is None: model_type = self.model_type
            pred_alpha = self.prediction_alpha
            wname = self.get_available_models()[1][self.model_type]['wname']
            xnames = self.get_available_models()[1][self.model_type]['xnames']
            yname = self.get_available_models()[1][self.model_type]['yname']
            include_intercept = self.get_available_models()[1][self.model_type]['include_intercept']
            answer = [include_intercept, wname, xnames, yname, pred_alpha]
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='MeterPeakDemandModel %s, get_model_specs failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            answer = None
        return answer
        
    def show_properties(self):
        """No inputs.  Prints
        first/last month,
        Tccp/Thcp, and type."""
        print ('First Month = ' + self.first_month + '\n' + 
               'Last Month = ' + self.last_month + '\n' +
               'Tccp = ' + str(self.Tccp) + '\n' + 
               'Thcp = ' + str(self.Thcp) + '\n' +
               'Model Type = ' + self.model_type)
    def get_average_baseline_degree_days(self, Tccp=None, Thcp=None):
        """function(Tccp=None, Thcp=None)
        
        Return annual average
        monthly HDD and CDD
        given change point 
        temperatures (defaults
        to model's temperatures)
        and baseline period as
        defined by model's first
        and last months."""
        try:
            if Tccp is None: Tccp = self.Tccp
            if Thcp is None: Thcp = self.Thcp
            df = self.get_baseline_df()
            df = df.drop(['CDD (peak demand)', 'HDD (peak demand)'], axis = 1)
            df = self.meter.weather_station.get_CDD_df(df, Tccp)
            df.rename(columns={'CDD': 'CDD (peak demand)'}, inplace = True)
            df = self.meter.weather_station.get_HDD_df(df, Thcp)
            df.rename(columns={'HDD': 'HDD (peak demand)'}, inplace = True)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterPeakDemandModel %s get_average_baseline_degree_days failed to calculate or load degree days into dataframe, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df_avg = None
        else:
            if len(df)<12:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='MeterPeakDemandModel %s get_average_baseline_degree_days found less than 12-month baseline period, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df_avg = None
            else:
                df = df.sort_index()
                df_avg = df[0:12]
                for i in range(0,12):
                    df_avg['CDD (peak demand)'][i:i+1] = df['CDD (peak demand)'][[x.month==df.index[i].month for x in df.index]].mean()
                    df_avg['HDD (peak demand)'][i:i+1] = df['HDD (peak demand)'][[x.month==df.index[i].month for x in df.index]].mean()
                df_avg = df_avg.sort_index()
        return df_avg
         
    def get_baseline_df(self):
        """No inputs.  Return
        bill data dataframe
        for baseline period of
        MeterPeakDemandModel."""
        if self.first_month is None or self.last_month is None:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Bad inputs.',
                        comment='MeterPeakDemandModel %s, get_baseline_df given inappropriate first/last months for range, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:            
            try:
                df = self.meter.get_bill_data_period_dataframe(first_month = self.first_month,
                                                               last_month = self.last_month)
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Retrieve data failed.',
                            comment='MeterPeakDemandModel %s, get_baseline_df failed, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df = None
        return df
        
    def get_model_calc_dict(self):
        """No inputs.  Return
        dictionary of
        independent variable
        names and associated
        model parameter
        values."""
        d = {}
        if self.beta00p is not None: d[self.beta00v] = self.beta00p
        if self.beta01p is not None: d[self.beta01v] = self.beta01p
        if self.beta02p is not None: d[self.beta02v] = self.beta02p
        if self.beta03p is not None: d[self.beta03v] = self.beta03p
        if self.beta04p is not None: d[self.beta04v] = self.beta04p
        if self.beta05p is not None: d[self.beta05v] = self.beta05p
        if self.beta06p is not None: d[self.beta06v] = self.beta06p
        if self.beta07p is not None: d[self.beta07v] = self.beta07p
        if self.beta08p is not None: d[self.beta08v] = self.beta08p
        if self.beta09p is not None: d[self.beta09v] = self.beta09p
        if self.beta10p is not None: d[self.beta10v] = self.beta10p
        return d
    
    def get_params_list(self):
        """No inputs.  Returns
        list of model parameter
        names (unused are None)."""
        return [self.beta00p, self.beta01p, self.beta02p, self.beta03p, self.beta04p, self.beta05p,
                self.beta06p, self.beta07p, self.beta08p, self.beta09p, self.beta10p]
    def get_params_pvalue_list(self):
        """No inputs.  Returns
        list of p-values
        (significance testing)
        for model parameters.
        
        Used in acceptance
        score to penalize
        models with
        insignificant model
        parameters."""
        return [self.beta00_p_value, self.beta01_p_value, self.beta02_p_value, self.beta03_p_value,
                self.beta04_p_value, self.beta05_p_value, self.beta06_p_value, self.beta07_p_value,
                self.beta08_p_value, self.beta09_p_value, self.beta10_p_value]
    def get_param_count(self):
        """No inputs.  Returns
        total count of used
        parameters in a model
        (inc. constant term)."""
        return sum([x is not None for x in self.get_params_list()])
    def get_max_param_p_value(self):
        """No inputs.  Returns
        highest significance
        test p-value of model
        parameters.
        
        Used in acceptance score
        to penalize models with
        insignificant model
        parameters."""
        return max(self.get_params_pvalue_list())
    def get_min_param(self):
        """No inputs.  Returns
        minimum model parameter
        value.
        
        Used in acceptance score
        to penalize negative
        model parameter values."""
        return min(self.get_params_list())
    def set_accept_score(self):
        """No inputs.  Returns
        a goodness of fit score
        based on statistical
        results of regression.
        
        Used to select the model
        appearing to be the most
        appropriate (not
        necessarily the most
        accurate or highest R^2)
        fit to the data."""
        self.acceptance_score = (
            1 * (-1*(self.adj_r_squared < 0.5) + 1*(self.adj_r_squared > 0.85)) +
            1 * (-1*(self.F_stat_p_value > 0.1) + 1*(self.F_stat_p_value < 0.01)) +
            1 * (-1*(self.get_max_param_p_value() > 0.1) + 1*(self.get_max_param_p_value() < 0.01)) +
            1 * (10 - self.get_param_count()) +
            1 * (min(0, np.sign(self.get_min_param())))  )
        return self.acceptance_score
        
    def set_best_model(self):
        """No inputs.  Runs
        through battery of
        model types at
        Tccp=Thcp=65 to find
        most appropriate model
        type.  Then runs through
        temperature range finding
        most appropriate change
        point temperatures."""
        
        available_models = self.get_available_models()
        track_runs = pd.DataFrame()
        track_Tccp = pd.DataFrame()
        track_Thcp = pd.DataFrame()
        best_run_results = None
        try:
            Tccp = Thcp = 65
            #not using prep_df, instead loading all needed columns once and then cycling through
            #as new models are added, need to add code here to make sure the new models are
            #    included in the search for the best fit model
            df = self.get_baseline_df()
            df = df.drop(['CDD (peak demand)', 'HDD (peak demand)'], axis = 1)
            df = self.meter.weather_station.get_CDD_df(df, Tccp)
            df.rename(columns={'CDD': 'CDD (peak demand)'}, inplace = True)
            df = self.meter.weather_station.get_HDD_df(df, Thcp)
            df.rename(columns={'HDD': 'HDD (peak demand)'}, inplace = True)
            df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
            df['CDD (peak demand)/day'] = df['CDD (peak demand)']/df['Days']
            df['HDD (peak demand)/day'] = df['HDD (peak demand)']/df['Days']
            df['peak demand/day'] = df['Peak Demand (act)']/df['Days']
            #--------------------------------------------------------------------------
            df = df.sort_index()
            
            #first run through models to find best model type at constant change point temperatures
            for run in available_models[0]:
                try:
                    results = self.set_model_print_results(df = df,
                                            wname = available_models[1][run]['wname'],
                                            xnames = available_models[1][run]['xnames'],
                                            yname = available_models[1][run]['yname'],
                                            include_intercept = available_models[1][run]['include_intercept'])
                    if results is not None:
                        track_runs = track_runs.append(pd.DataFrame({'id': run,
                                                                     'Tccp': Tccp,
                                                                     'Thcp': Thcp,
                                                                     'acceptance_score': self.acceptance_score},
                                                                     index=[run + str(Tccp) + str(Thcp)]))
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Model run failed.',
                                comment='MeterPeakDemandModel %s set_best_model failed on %s-%s-%s, function aborted.' % (self.id, run, str(Tccp), str(Thcp)))
                    m.save()
                    self.messages.add(m)
                    print m
            best_score = track_runs['acceptance_score'].max()
            if track_runs['acceptance_score'][track_runs['acceptance_score']==best_score].count() > 1:
                m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Non-unique result.',
                            comment='MeterPeakDemandModel %s set_best_model found multiple models with the highest acceptance score.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            best_run = track_runs['acceptance_score'].idxmax()
            best_type = track_runs['id'][best_run]
            best_Tccp = best_Thcp = 65 #set here so final setting of best model can use; if needed, will be overwritten first
            
            #then, if model contains cooling term(s), find best Tccp
            if 'c' in best_type:
                try:
                    track_Tccp = pd.DataFrame()            
                    Thcp = 65
                    df = self.get_baseline_df()
                    df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
                    df['peak demand/day'] = df['Peak Demand (act)']/df['Days']
                    df = df.drop(['HDD (peak demand)'], axis = 1)
                    df = self.meter.weather_station.get_HDD_df(df, Thcp)
                    df.rename(columns={'HDD': 'HDD (peak demand)'}, inplace = True)
                    df['HDD (peak demand)/day'] = df['HDD (peak demand)']/df['Days']
                    for Tccp in range(55, 96):
                        #must call/create here so that all wname, xnames, and ynames are in df-----
                        df = df.drop(['CDD (peak demand)'], axis = 1)
                        df = self.meter.weather_station.get_CDD_df(df, Tccp)
                        df.rename(columns={'CDD': 'CDD (peak demand)'}, inplace = True)
                        df['CDD (peak demand)/day'] = df['CDD (peak demand)']/df['Days']
                        #--------------------------------------------------------------------------
                        df = df.sort_index()
                        results = self.set_model_print_results(df = df,
                              wname = available_models[1][best_type]['wname'],
                              xnames = available_models[1][best_type]['xnames'],
                              yname = available_models[1][best_type]['yname'],
                              include_intercept = available_models[1][best_type]['include_intercept'])
                        track_Tccp = track_Tccp.append(pd.DataFrame({'Tccp': Tccp,
                                                                     'Thcp': Thcp,
                                                                     'adj_r_squared': self.adj_r_squared},
                                                                     index=[str(self.adj_r_squared) + str(Tccp) + str(Thcp)]))
                        best_Tccp_run = track_Tccp['adj_r_squared'].idxmax()
                        best_Tccp = track_Tccp['Tccp'][best_Tccp_run]
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Calculation failed.',
                                comment='MeterPeakDemandModel %s set_best_model unable to calculate Tccp range, function aborted.' % (self.id))
                    m.save()
                    self.messages.add(m)
                    print m
            else:
                track_Tccp = None
                
            #then, if model contains heating term(s), find best Thcp
            if 'h' in best_type:
                try:
                    track_Thcp = pd.DataFrame()            
                    Tccp = 65
                    df = self.get_baseline_df()
                    df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
                    df['peak demand/day'] = df['Peak Demand (act)']/df['Days']
                    df = df.drop(['CDD (peak demand)'], axis = 1)
                    df = self.meter.weather_station.get_CDD_df(df, Tccp)
                    df.rename(columns={'CDD': 'CDD (peak demand)'}, inplace = True)
                    for Thcp in range(55, 80):
                        #must call/create here so that all wname, xnames, and ynames are in df-----
                        df = df.drop(['HDD (peak demand)'], axis = 1)
                        df = self.meter.weather_station.get_HDD_df(df, Thcp)
                        df.rename(columns={'HDD': 'HDD (peak demand)'}, inplace = True)
                        df['HDD (peak demand)/day'] = df['HDD (peak demand)']/df['Days']
                        #--------------------------------------------------------------------------
                        df = df.sort_index()
                        results = self.set_model_print_results(df = df,
                              wname = available_models[1][best_type]['wname'],
                              xnames = available_models[1][best_type]['xnames'],
                              yname = available_models[1][best_type]['yname'],
                              include_intercept = available_models[1][best_type]['include_intercept'])
                        track_Thcp = track_Thcp.append(pd.DataFrame({'Tccp': Tccp,
                                                                     'Thcp': Thcp,
                                                                     'adj_r_squared': self.adj_r_squared},
                                                                     index=[str(self.adj_r_squared) + str(Tccp) + str(Thcp)]))
                        best_Thcp_run = track_Thcp['adj_r_squared'].idxmax()
                        best_Thcp = track_Thcp['Tccp'][best_Thcp_run]
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Calculation failed.',
                                comment='MeterPeakDemandModel %s set_best_model unable to calculate Thcp range, function aborted.' % (self.id))
                    m.save()
                    self.messages.add(m)
                    print m
            else:
                track_Thcp = None

            #now run best model based on findings from code above
            #must call/create here so that all wname, xnames, and ynames are in df-----
            self.model_type = best_type
            self.Tccp = best_Tccp
            self.Thcp = best_Thcp
            df = self.get_baseline_df()
            df = self.prep_df(df)
            df = df.sort_index()
            best_run_results = self.set_model_print_results(df = df,
                              wname = available_models[1][best_type]['wname'],
                              xnames = available_models[1][best_type]['xnames'],
                              yname = available_models[1][best_type]['yname'],
                              include_intercept = available_models[1][best_type]['include_intercept'])
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Model update failed.',
                        comment='MeterPeakDemandModel %s set_best_model failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        self.save()
        return track_runs, track_Tccp, track_Thcp, best_run_results
        
    def set_model_print_results(self, df, wname, xnames, yname, include_intercept=True):
        """function(df,wname,xnames,
                    yname,include_intercept=True)
        Regresses xnames independent
        variables against yname
        dependent variable with
        weighting factors wname,
        with indicator for whether
        to include constant term.
        Prints model summary and
        acceptance score.
        
        df = dataframe
        wname = list
        xnames = list
        yname = list
        inc._int. = bool."""
        try:
            results = self.set_model(df, wname, xnames, yname, include_intercept)
            print results.summary()
            print 'acceptance score = ' + str(self.set_accept_score())
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterPeakDemandModel %s, set_model_print_results failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        return results
    def get_model(self):
        """No inputs. Returns
        model results object
        using model's current
        attributes."""
        try:
            if self.model_type is None: raise TypeError
            wname = self.get_available_models()[1][self.model_type]['wname']
            xnames = self.get_available_models()[1][self.model_type]['xnames']
            yname = self.get_available_models()[1][self.model_type]['yname']
            include_intercept = self.get_available_models()[1][self.model_type]['include_intercept']
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Model not set.',
                        comment='MeterPeakDemandModel %s get_model failed because model is not set, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        else:
            try:
                df = self.get_baseline_df()
                df = self.prep_df(df)
                df = df.sort_index()

                #had trouble with Decimals vs. Floats, so converting for model functions
                Y = df[yname].applymap(float).__array__()                   #create dependent variable vector; here only one
                X = df[xnames].applymap(float).__array__()                  #create independent variable(s) vector
                w = df[wname].applymap(float).__array__()                   #create weighting vector, e.g. 'days in period'
                if include_intercept: X = sm.add_constant(X, prepend = True)      #beta[0] will be constant term when prepend=True
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Retrieve data failed.',
                            comment='MeterPeakDemandModel %s, get_model function failed to prepare regression inputs, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                results = None
            else:
                try:
                    results = sm.WLS(Y, X, weights = w).fit()
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Unable to run regression.',
                                comment='MeterPeakDemandModel %s, get_model function failed to run regression, function aborted.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    results = None
        return results

    def set_model(self, df, wname, xnames, yname, include_intercept=True):
        """function(df,wname,xnames,
                    yname,include_intercept=True)
        Regresses xnames independent
        variables against yname
        dependent variable with
        weighting factors wname,
        with indicator for whether
        to include constant term.
        
        df = dataframe
        wname = list
        xnames = list
        yname = list
        inc._int. = bool."""
        try:
            if not(  min([x in df.columns for x in wname]) and 
                     (len(xnames)==0 or min([x in df.columns for x in xnames])) and 
                     min([x in df.columns for x in yname]) ):
                raise ValueError
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='MeterPeakDemandModel %s, set_model function given improper inputs, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        else:
            try:
                df = df.sort_index()
                #had trouble with Decimals vs. Floats, so converting for model functions
                Y = df[yname].applymap(float).__array__()                   #create dependent variable vector; here only one
                X = df[xnames].applymap(float).__array__()                  #create independent variable(s) vector
                w = df[wname].applymap(float).__array__()                   #create weighting vector, e.g. 'days in period'
                if include_intercept: X = sm.add_constant(X, prepend = True)      #beta[0] will be constant term when prepend=True
                results = sm.WLS(Y, X, weights = w).fit()
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Unable to run regression.',
                            comment='MeterPeakDemandModel %s, set_model function failed to run regression, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                results = None
            else:
                if len(results.params)>0: 
                    self.beta00p = results.params[0]
                    if include_intercept:
                        self.beta00v = 'constant'
                    else:
                        self.beta00v = xnames[0]
                    self.beta00_se = results.bse[0]
                    self.beta00_t_stat = results.tvalues[0]
                    self.beta00_p_value = results.pvalues[0]
                    self.beta00_95_conf_int = results.params[0] - results.conf_int(alpha=0.05)[0][0]
                if len(results.params)>1: 
                    self.beta01p = results.params[1]
                    if include_intercept:
                        self.beta01v = xnames[0]
                    else:
                        self.beta01v = xnames[1]
                    self.beta01_se = results.bse[1]
                    self.beta01_t_stat = results.tvalues[1]
                    self.beta01_p_value = results.pvalues[1]
                    self.beta01_95_conf_int = results.params[1] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>2:
                    self.beta02p = results.params[2]
                    if include_intercept:
                        self.beta02v = xnames[1]
                    else:
                        self.beta02v = xnames[2]
                    self.beta02_se = results.bse[2]
                    self.beta02_t_stat = results.tvalues[2]
                    self.beta02_p_value = results.pvalues[2]
                    self.beta02_95_conf_int = results.params[2] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>3:
                    self.beta03p = results.params[3]
                    if include_intercept:
                        self.beta03v = xnames[2]
                    else:
                        self.beta03v = xnames[3]
                    self.beta03_se = results.bse[3]
                    self.beta03_t_stat = results.tvalues[3]
                    self.beta03_p_value = results.pvalues[3]
                    self.beta03_95_conf_int = results.params[3] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>4: 
                    self.beta04p = results.params[4]
                    if include_intercept:
                        self.beta04v = xnames[3]
                    else:
                        self.beta04v = xnames[4]
                    self.beta04_se = results.bse[4]
                    self.beta04_t_stat = results.tvalues[4]
                    self.beta04_p_value = results.pvalues[4]
                    self.beta04_95_conf_int = results.params[4] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>5: 
                    self.beta05p = results.params[5]
                    if include_intercept:
                        self.beta05v = xnames[4]
                    else:
                        self.beta05v = xnames[5]
                    self.beta05_se = results.bse[5]
                    self.beta05_t_stat = results.tvalues[5]
                    self.beta05_p_value = results.pvalues[5]
                    self.beta05_95_conf_int = results.params[5] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>6: 
                    self.beta06p = results.params[6]
                    if include_intercept:
                        self.beta06v = xnames[5]
                    else:
                        self.beta06v = xnames[6]
                    self.beta06_se = results.bse[6]
                    self.beta06_t_stat = results.tvalues[6]
                    self.beta06_p_value = results.pvalues[6]
                    self.beta06_95_conf_int = results.params[6] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>7: 
                    self.beta07p = results.params[7]
                    if include_intercept:
                        self.beta07v = xnames[6]
                    else:
                        self.beta07v = xnames[7]
                    self.beta07_se = results.bse[7]
                    self.beta07_t_stat = results.tvalues[7]
                    self.beta07_p_value = results.pvalues[7]
                    self.beta07_95_conf_int = results.params[7] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>8: 
                    self.beta08p = results.params[8]
                    if include_intercept:
                        self.beta08v = xnames[7]
                    else:
                        self.beta08v = xnames[8]
                    self.beta08_se = results.bse[8]
                    self.beta08_t_stat = results.tvalues[8]
                    self.beta08_p_value = results.pvalues[8]
                    self.beta08_95_conf_int = results.params[8] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>9: 
                    self.beta09p = results.params[9]
                    if include_intercept:
                        self.beta09v = xnames[8]
                    else:
                        self.beta09v = xnames[9]
                    self.beta09_se = results.bse[9]
                    self.beta09_t_stat = results.tvalues[9]
                    self.beta09_p_value = results.pvalues[9]
                    self.beta09_95_conf_int = results.params[9] - results.conf_int(alpha=0.05)[1][1]
                if len(results.params)>10: 
                    self.beta10p = results.params[10]
                    if include_intercept:
                        self.beta10v = xnames[9]
                    else:
                        self.beta10v = xnames[10]
                    self.beta10_se = results.bse[10]
                    self.beta10_t_stat = results.tvalues[10]
                    self.beta10_p_value = results.pvalues[10]
                    self.beta10_95_conf_int = results.params[10] - results.conf_int(alpha=0.05)[1][1]
                
                self.p = len(results.params)
                self.n = len(df)
                self.df = len(df) - self.p
                self.Yavg = np.average(Y)
    
                self.r_squared = results.rsquared
                self.adj_r_squared = results.rsquared_adj
                self.SSQres = np.dot((Y.transpose()-results.fittedvalues)[0], (Y.transpose()-results.fittedvalues)[0])
                self.rmse = np.sqrt(self.SSQres/(self.n - self.p))
                self.cvrmse = self.rmse/self.Yavg
                self.F_stat = results.fvalue
                self.F_stat_p_value = results.f_pvalue
                s = pd.Series(results.resid)
                self.autocorr_coeff = np.sqrt( (s[1:].corr(s.shift(1)[1:]))**2 )
                
                
                self.nbe = np.sum(df[yname[0]].apply(float)*df[wname[0]].apply(float)-results.fittedvalues*df[wname[0]].apply(float))/np.sum(df[yname[0]].apply(float)*df[wname[0]].apply(float))
                
                self.first_month = df.index[0].strftime('%m/%Y')
                self.last_month = df.index[-1].strftime('%m/%Y')
                
                self.set_accept_score()
        self.save()
        return results

    def model_predict(self, res, exog=None, weights=None, alpha=0.10):
        """function(res,exog=None,weights=None,alpha=0.10)
        
        Adapted version of statsmodels
        wls_prediction_std function.
        Usage:
         predicted, prstd, iv_l, iv_u = ...
           function(results,
                    exog = array([[1,17],[1,18],[1,19]]),
                    weights = [32, 32, 32],
                    alpha=0.10)
        
        
        Calculate standard deviation
        and confidence interval for
        prediction.
        
        applies to WLS and OLS, not to general GLS,
        that is independently but not identically distributed observations
        
        Parameters
        ----------
        res : regression result instance
            results of WLS or OLS regression required attributes see notes
        exog : array_like (optional)
            exogenous variables for points to predict
        weights : scalar or array_like (optional)
            weights as defined for WLS (inverse of variance of observation)
        alpha : float (default: alpha = 0.10)
            confidence level for two-sided hypothesis
    
        Returns
        -------
        predstd : array_like, 1d
            standard error of prediction
            same length as rows of exog
        interval_l, interval_u : array_like
            lower und upper confidence bounds
    
        Notes
        -----
        The result instance needs to have at least the following
        res.model.predict() : predicted values or
        res.fittedvalues : values used in estimation
        res.cov_params() : covariance matrix of parameter estimates
    
        If exog is 1d, then it is interpreted as one observation,
        i.e. a row vector."""
        
        try:
            covb = res.cov_params()
            if exog is None:
                exog = res.model.exog
                predicted = res.fittedvalues
            else:
                exog = np.atleast_2d(exog)
                if covb.shape[1] != exog.shape[1]:
                    raise ValueError('wrong shape of exog')
                predicted = res.model.predict(res.params, exog)
        
            if weights is None:
                weights = res.model.weights
            
            predvar = res.mse_resid/weights + (exog * np.dot(covb, exog.T).T).sum(1)
            predstd = np.sqrt(predvar)
            tppf = stats.t.isf(alpha/2., res.df_resid)
            interval_u = predicted + tppf * predstd
            interval_l = predicted - tppf * predstd
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterPeakDemandModel %s, model_predict function failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            predicted = predstd = interval_l = interval_u = None
        return predicted, predstd, interval_l, interval_u
    
    def model_predict_df(self, df, wname, xnames, include_intercept=True, alpha=0.10):
        """function(df,wname,xnames,
                    include_intercept=True,
                    alpha=0.10)
        Uses current model settings
        to retrieve CDD/HDD for df,
        calls get_model to
        retrieve results object,
        and creates appropriately
        formatted exog and weights
        arrays for passing to
        model_predict function."""

        try:
            df = df.sort_index()
            df = self.prep_df(df)

            #had trouble with Decimals vs. Floats, so converting for model functions
            X = df[xnames].applymap(float).__array__()                  #create independent variable(s) vector
            w = df[wname].applymap(float).__array__().flatten()                   #create weighting vector, e.g. 'days in period'
            if include_intercept: X = sm.add_constant(X, prepend = True)      #beta[0] will be constant term when prepend=True
            results = self.get_model()
            predicted_norm, predstd_norm, interval_l_norm, interval_u_norm = self.model_predict(res=results, exog=X, weights=w, alpha=alpha)
            predicted = predicted_norm * w
            predstd = predstd_norm * w
            interval_l = interval_l_norm * w
            interval_u = interval_u_norm * w
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterPeakDemandModel %s, model_predict_df unable to calculate predictions, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            results = None
        return predicted, predstd, interval_l, interval_u
        
    def current_model_predict_df(self, df):
        """function(df)
        
        Uses current model settings
        to construct needed inputs
        and call model_predict_df
        function."""

        try:
            df = self.prep_df(df)
            pred_alpha = self.prediction_alpha
            wname = self.get_available_models()[1][self.model_type]['wname']
            xnames = self.get_available_models()[1][self.model_type]['xnames']
            include_intercept = self.get_available_models()[1][self.model_type]['include_intercept']
            predicted, predstd, interval_l, interval_u = self.model_predict_df(df, wname, xnames, include_intercept, pred_alpha)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='MeterPeakDemandModel %s, current_model_predict_df unable to calculate predictions, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            predicted = predstd = interval_l = interval_u = None
        return predicted, predstd, interval_l, interval_u
    class Meta:
        app_label = 'BuildingSpeakApp'
