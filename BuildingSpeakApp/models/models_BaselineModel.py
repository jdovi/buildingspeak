## DEPRECATED 7/11/2013
## now using models_MeterModels.py
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


class BaselineModel(models.Model):
    """Regression model for use
    with monthly bill data."""
    
    model_type = models.CharField(blank=True, max_length=200,
                                    choices=[('1p','1p'),
                                             ('2p','2p'),
                                             ('2pc','2pc'),
                                             ('2ph','2ph'),
                                             ('3pc','3pc'),
                                             ('3ph','3ph'),
                                             ('4pc','4pc'),
                                             ('4ph','4ph'),
                                             ('5phc','5phc'),
                                             ('7phcx','7phcx'),
                                                         ])
    first_month = models.CharField(blank=True, max_length=10, help_text='first month of baseline period, MM/YYYY')
    last_month = models.CharField(blank=True, max_length=10, help_text='last month of baseline period, MM/YYYY')
    Tccp = models.FloatField(null=True, blank=True)
    Thcp = models.FloatField(null=True, blank=True)

    #relationships
    meter = models.ForeignKey('Meter', null=True)
    messages = models.ManyToManyField('Message')
    
    #model parameters
    beta00p = models.FloatField(null=True, blank=True)
    beta01p = models.FloatField(null=True, blank=True)
    beta02p = models.FloatField(null=True, blank=True)
    beta03p = models.FloatField(null=True, blank=True)
    beta04p = models.FloatField(null=True, blank=True)
    beta05p = models.FloatField(null=True, blank=True)
    beta06p = models.FloatField(null=True, blank=True)
    beta07p = models.FloatField(null=True, blank=True)
    beta08p = models.FloatField(null=True, blank=True)
    beta09p = models.FloatField(null=True, blank=True)
    beta10p = models.FloatField(null=True, blank=True)

    #model parameters' associated independent variable names
    beta00v = models.CharField(blank=True, max_length=200)
    beta01v = models.CharField(blank=True, max_length=200)
    beta02v = models.CharField(blank=True, max_length=200)
    beta03v = models.CharField(blank=True, max_length=200)
    beta04v = models.CharField(blank=True, max_length=200)
    beta05v = models.CharField(blank=True, max_length=200)
    beta06v = models.CharField(blank=True, max_length=200)
    beta07v = models.CharField(blank=True, max_length=200)
    beta08v = models.CharField(blank=True, max_length=200)
    beta09v = models.CharField(blank=True, max_length=200)
    beta10v = models.CharField(blank=True, max_length=200)

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
    def show_properties(self):
        print ('First Month = ' + self.first_month + '\n' + 'Last Month = ' + self.last_month + '\n' +
               'Tccp = ' + str(self.Tccp) + '\n' + 'Thcp = ' + str(self.Thcp) + '\n' +
               'Model Type = ' + self.model_type)
    def get_average_baseline_degree_days(self, Tccp=None, Thcp=None):
        """Return annual average
        monthly HDD and CDD."""
        try:
            if Tccp is None: Tccp = self.Tccp
            if Thcp is None: Thcp = self.Thcp
            df = self.get_baseline_df(Tccp=Tccp, Thcp=Thcp)
            df = df.sort_index()
            df_avg = df[0:12]
            for i in range(0,12):
                df_avg['CDD'][i:i+1] = df['CDD'][[x.month==df.index[i].month for x in df.index]].mean()
                df_avg['HDD'][i:i+1] = df['HDD'][[x.month==df.index[i].month for x in df.index]].mean()
            df_avg = df_avg.sort_index()
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='BaselineModel %s, get_average_baseline_degree_days failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df_avg = None
        return df_avg
         
    def get_baseline_df(self, Tccp=None, Thcp=None):
        """Return a dataframe for
        the baseline period of the
        BaselineModel, including
        CDD and HDD."""
        try:
            if Tccp is None: Tccp = self.Tccp
            if Thcp is None: Thcp = self.Thcp
            #df = self.meter.billingcycler_set.all()[0].get_billing_cycler_period_dataframe(first_month = self.first_month,
            #                                                                  last_month = self.last_month)
            df = self.meter.monther_set.get(name='BILLx').get_monther_period_dataframe(first_month = self.first_month,
                                                                              last_month = self.last_month)
            df = self.meter.weather_station.get_CDD_df(df, base_temp_CDD=Tccp)
            df = self.meter.weather_station.get_HDD_df(df, base_temp_HDD=Thcp)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='BaselineModel %s, get_baseline_df failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        return df
        
    def get_model_calc_dict(self):
        """Return dictionary of
        independent variable names
        and associated model parameter
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
        return [self.beta00p, self.beta01p, self.beta02p, self.beta03p, self.beta04p, self.beta05p,
                self.beta06p, self.beta07p, self.beta08p, self.beta09p, self.beta10p]
    def get_params_pvalue_list(self):
        return [self.beta00_p_value, self.beta01_p_value, self.beta02_p_value, self.beta03_p_value,
                self.beta04_p_value, self.beta05_p_value, self.beta06_p_value, self.beta07_p_value,
                self.beta08_p_value, self.beta09_p_value, self.beta10_p_value]
    def get_param_count(self):
        return sum([x is not None for x in self.get_params_list()])
    def get_max_param_p_value(self):
        return max(self.get_params_pvalue_list())
    def get_min_param(self):
        return min(self.get_params_list())
    def set_accept_score(self):
        self.acceptance_score = (
            1 * (-1*(self.adj_r_squared < 0.5) + 1*(self.adj_r_squared > 0.85)) +
            1 * (-1*(self.F_stat_p_value > 0.1) + 1*(self.F_stat_p_value < 0.01)) +
            1 * (-1*(self.get_max_param_p_value() > 0.1) + 1*(self.get_max_param_p_value() < 0.01)) +
            1 * (10 - self.get_param_count()) +
            1 * (min(0, np.sign(self.get_min_param())))  )
        return self.acceptance_score
        
    def run_test_battery(self):
        battery = {'1p': {'include_intercept': True, 'xnames': []},
                          '2pc': {'include_intercept': True, 'xnames': ['CDD/day']},
                          '2ph': {'include_intercept': True, 'xnames': ['HDD/day']}  }
        Tccp = Thcp = 65  #have to cycle through these in order to run battery
        for run in battery:
            df = self.get_baseline_df(Tccp, Thcp)
            df['Days'] = [(df['End Date'][i] - df['Start Date'][i]).days for i in range(0, len(df))]
            df['CDD/day'] = df['CDD']/df['Days']
            df['HDD/day'] = df['HDD']/df['Days']
            results = self.regress_data_print_results(df = df,
                                                      wnames = df['Days'],
                                                      xnames = run['xnames'],
                                                      yname = df['Consumption (act)'],
                                                      include_intercept = run['include_intercept'])
            battery[run]['acceptance_score'] = self.acceptance_score
        return battery
    def regress_data_print_results(self, df, wnames, xnames, yname, include_intercept=True):
        results = self.regress_data(df, wnames, xnames, yname, include_intercept)
        print results.summary()
        print 'acceptance score = ' + str(self.set_accept_score())
        return results
    def regress_data(self, df, wnames, xnames, yname, include_intercept=True):
        """regress_data(df, wname, xnames, yname)
        
        Create/update model based
        on provided dataframe, df, and
        column names:
          yname = str (e.g. 'kWh/day')
          xnames = list (e.g. ['HDD/day'])
          wname = list (e.g. ['Days'])
          
        For multiple independent
        variables, xnames = list."""

        try:
            if not(  min([x in df.columns for x in wnames]) and 
                     (len(xnames)==0 or min([x in df.columns for x in xnames])) and 
                     (yname in df.columns) ):
                raise ValueError
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='BaselineModel %s, regress_data function given improper inputs, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        else:
            try:
                df = df.sort_index()
                Y = df[yname].__array__()                   #create dependent variable vector; here only one
                X = df[xnames].__array__()                  #create independent variable(s) vector
                w = df[wnames].__array__()                   #create weighting vector, e.g. 'days in period'
                if include_intercept: X = sm.add_constant(X, prepend = True)      #beta[0] will be constant term when prepend=True
                results = sm.WLS(Y, X, weights = w).fit()
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Unable to run regression.',
                            comment='BaselineModel %s, regress_data function failed to run regression, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
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
                self.SSQres = np.dot(Y-results.fittedvalues, Y-results.fittedvalues)
                self.rmse = np.sqrt(self.SSQres/(self.n - self.p))
                self.cvrmse = self.rmse/self.Yavg
                self.F_stat = results.fvalue
                self.F_stat_p_value = results.f_pvalue
                s = pd.Series(results.resid)
                self.autocorr_coeff = np.sqrt( (s[1:].corr(s.shift(1)[1:]))**2 )
                
                
                self.nbe = np.sum(df['kWh/day']*df['Days']-results.fittedvalues*df['Days'])/np.sum(df['kWh/day']*df['Days'])
                
                self.first_month = str(df.index[0])
                self.last_month = str(df.index[-1])
                
                self.set_accept_score()
        return results

    def model_predict(self, res, exog=None, weights=None, alpha=0.05):
        """Adapted version of statsmodels
        wls_prediction_std function.  Usage:
            prstd, iv_l, iv_u = ...
              wls_prediction_std(results,
                                 exog = array([[1,17],[1,18],[1,19]]),
                                 weights = [32, 32, 32],
                                 alpha=0.05)

        
        ...calculate standard deviation and confidence interval for prediction

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
        alpha : float (default: alpha = 0.5)
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
                        comment='BaselineModel %s, model_predict function failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            predicted = predstd = interval_l = interval_u = None
        return predicted, predstd, interval_l, interval_u
        
    class Meta:
        app_label = 'BuildingSpeakApp'

