#import dbarray
import pandas as pd
from pytz import UTC
from django_rq import job
from pytz import timezone as tz
from numpy import NaN, float64, int, float, int64
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
from models_ForecastIO import Forecastio

def upload_weather_data_file_path(instance, filename):
    return '/'.join(['%06d' % instance.pk + '_' + instance.name,
                     'uploaded_' + timezone.now().strftime('%Y-%m-%d_%H-%M') + '_' + filename])

class WeatherStation(models.Model):
    """Model for geographical
    location for which weather
    data is stored.  Parents
    WeatherDataPoints."""
    name = models.CharField(max_length=200)
    description = models.CharField(blank=True, max_length=200,
                                   help_text='description of location')
    latitude = models.DecimalField(max_digits=10, decimal_places=7,
                    help_text='latitude of location')
    longitude = models.DecimalField(max_digits=10, decimal_places=7,
                    help_text='longitude of location')
    tz_name = models.CharField(blank=True, max_length=200,
                                   help_text='name of timezone, e.g. US/Eastern',
                                   verbose_name='Timezone')
    weather_data_import = models.BooleanField(blank=True, default=False,
                    help_text='import weather data?')
    weather_data_upload_file = models.FileField(null=True, blank=True, upload_to=upload_weather_data_file_path, 
                    storage=S3BotoStorage(location='user_data_files/weather_stations'),
                    help_text='link to text file containing monthly bill data; must be formatted correctly')
    #relationships
    messages = models.ManyToManyField('Message')

    
    #functions
    def get_newest_date(self):
        try:
            result = self.weatherdatapoint_set.order_by('time')[self.weatherdatapoint_set.order_by('time').count()-1]
        except:
            result = None
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='WeatherStation %s get_newest_date failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return result
    def get_oldest_date(self):
        try:
            result = self.weatherdatapoint_set.order_by('time')[0]
        except:
            result = None
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Retrieve data failed.',
                        comment='WeatherStation %s get_oldest_date failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return result
    def get_average_monthly_degree_days(self, Tccp, Thcp):
        """Return annual average
        monthly HDD and CDD for
        as much data as is
        available up to the
        most recent 3 years."""
        try:
            oldest = max(self.weatherdatapoint_set.order_by('time')[0].time,
                         timezone.now()-timedelta(hours=24*365*3))
            newest = min(self.weatherdatapoint_set.order_by('time').reverse()[0].time,
                         timezone.now())
            df = pd.DataFrame({'Start Date': datetime(2000,1,1,tzinfo=UTC),
                               'End Date': datetime(2000,1,1,tzinfo=UTC)},
                              index = pd.period_range(oldest, newest, freq='M'))
            for i in range(0,len(df)):
                df['Start Date'][i:i+1] = df.index[i].start_time
                df['End Date'][i:i+1] = df.index[i].end_time
            df = self.get_HDD_df(df, base_temp_HDD=Thcp)
            df = self.get_CDD_df(df, base_temp_CDD=Tccp)
            df = df.sort_index()
            df_avg = df[-1:-13:-1]
            df_avg = df_avg.sort_index()
            df_avg['Month Integer'] = 99
            for i in range(0,12):
                df_avg['CDD'][i:i+1] = df['CDD'][[x.month==df_avg.index[i].month for x in df.index]].mean()
                df_avg['HDD'][i:i+1] = df['HDD'][[x.month==df_avg.index[i].month for x in df.index]].mean()
                df_avg['Month Integer'][i:i+1] = df_avg.index[i].month
            df_avg = df_avg.sort(columns='Month Integer')
            df_avg.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Calculation failed.',
                        comment='WeatherStation %s, get_average_monthly_degree_days failed, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df_avg = None
        return df_avg
        
    def get_CDD_df(self, df, base_temp_CDD):
        """Inputs:
            df (dataframe with Start
                Date, End Date)
            base_temp_CDD
        
        Returns dataframe with new
        CDD column containing CDD
        for each row from given
        Start and End Dates. NaN
        values indicate no weather
        data obtained in a given
        period."""
        
        if (('Start Date' in df.columns) and ('End Date' in df.columns) and (len(df)>0) ):
            try:
                df['CDD'] = Decimal(NaN)
                df = df.sort_index()
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='WeatherStation %s unable to initialize empty CDD series in get_CDD_df, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            else:
                for i in range(0,len(df)):
                    try:
                        df['CDD'][i:i+1] = self.get_CDD(start_date = df['Start Date'][i],
                                                    end_date = df['End Date'][i],
                                                    base_temp = base_temp_CDD)[0]
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Calculation failed.',
                                    comment='WeatherStation %s unable to calculate CDD in get_CDD_df for %s-%s, function aborted.' % (self.id, df['Start Date'][i].strftime('%m/%d/%Y'), df['End Date'][i].strftime('%m/%d/%Y')))
                        m.save()
                        self.messages.add(m)
                        print m
                df = df.sort_index()
                if max(df['CDD'].apply(lambda x: x.is_nan())) and min(df['CDD'].apply(lambda x: x.is_nan())):
                    m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Calculations failed.',
                            comment='WeatherStation %s calculated all NaNs for CDDs in get_CDD_df.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                elif max(df['CDD'].apply(lambda x: x.is_nan())) and not(min(df['CDD'].apply(lambda x: x.is_nan()))):
                    m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Some calculations failed.',
                            comment='WeatherStation %s calculated some NaNs for CDDs in get_CDD_df.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                elif not(max(df['CDD'].apply(lambda x: x.is_nan()))) and not(min(df['CDD'].apply(lambda x: x.is_nan()))):
                    m = Message(when=timezone.now(),
                            message_type='Code Success',
                            subject='Calculations completed.',
                            comment='WeatherStation %s successfully calculated non-NaN CDDs in get_CDD_df.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='WeatherStation %s, get_CDD_df given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    def get_HDD_df(self, df, base_temp_HDD):
        """Inputs:
            df (dataframe with Start
                Date, End Date)
            base_temp_HDD
        
        Returns dataframe with new
        HDD column containing HDD
        for each row from given
        Start and End Dates. NaN
        values indicate no weather
        data obtained in a given
        period."""
        
        if (('Start Date' in df.columns) and ('End Date' in df.columns) and (len(df)>0) ):
            try:
                df['HDD'] = Decimal(NaN)
                df = df.sort_index()
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Calculation failed.',
                            comment='WeatherStation %s unable to initialize empty HDD series in get_HDD_df, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
            else:
                for i in range(0,len(df)):
                    try:
                        df['HDD'][i:i+1] = self.get_HDD(start_date = df['Start Date'][i],
                                                    end_date = df['End Date'][i],
                                                    base_temp = base_temp_HDD)[0]
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Calculation failed.',
                                    comment='WeatherStation %s unable to calculate HDD in get_HDD_df for %s-%s, function aborted.' % (self.id, df['Start Date'][i].strftime('%m/%d/%Y'), df['End Date'][i].strftime('%m/%d/%Y')))
                        m.save()
                        self.messages.add(m)
                        print m
                df = df.sort_index()
                if max(df['HDD'].apply(lambda x: x.is_nan())) and min(df['HDD'].apply(lambda x: x.is_nan())):
                    m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Calculations failed.',
                            comment='WeatherStation %s calculated all NaNs for HDDs in get_HDD_df.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                elif max(df['HDD'].apply(lambda x: x.is_nan())) and not(min(df['HDD'].apply(lambda x: x.is_nan()))):
                    m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Some calculations failed.',
                            comment='WeatherStation %s calculated some NaNs for HDDs in get_HDD_df.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                elif not(max(df['HDD'].apply(lambda x: x.is_nan()))) and not(min(df['HDD'].apply(lambda x: x.is_nan()))):
                    m = Message(when=timezone.now(),
                            message_type='Code Success',
                            subject='Calculations completed.',
                            comment='WeatherStation %s successfully calculated non-NaN HDDs in get_HDD_df.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
        else:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='WeatherStation %s, get_HDD_df given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
        return df
    def fill_temperature_gaps(self, s):
        """Inputs: s (temp. series)
        
        Takes series of hourly
        temperatures, fills gaps
        by searching forward and
        backward by 24 hours to
        find first non-NaN value."""
        try:
            if not ( isinstance(s, pd.core.series.TimeSeries) and (len(s) > 0) ):
                raise TypeError
            s = s.sort_index()
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='WeatherStation %s fill_temperature_gaps given bad inputs, aborting function.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            result = None
        else:
            i_min = 0
            i_max = len(s)
            for i in range(0,i_max):
                if s[i] is NaN:
                    j = 1
                    z = 1
                    x = 1
                    while (  x and ((i-24*j >= i_min) or (i+24*j < i_max))  ):
                        if (i+24*j < i_max) and z == 1:
                            if s[i+24*j*z] is not NaN:
                                s[i] = s[i+24*j*z]
                                x = 0
                        elif (i-24*j >= i_min) and z == -1:
                            if s[i+24*j*z] is not NaN:
                                s[i] = s[i+24*j*z]
                                x = 0
                        if z == -1:
                            j = j + 1
                            z = -z
                        else:
                            z = -z
            result = s
            result = result.sort_index()
        return result
    def get_CDD(self, start_date, end_date, base_temp):
        """Inputs:
            start_date (datetime)
            end_date   (datetime)
            base_temp  (float, int, or decimal)
        
        Calls WeatherStation's dataframe
        and slices relevant time frame,
        then computes and returns CDD.
        Calls gap filler to interpolate
        and replace NaNs."""
        try:
            if not (  isinstance(start_date, datetime) and
                      isinstance(end_date, datetime) and
                      end_date > start_date and
                      type(base_temp) in [float, int, float64, int64]  ):
                raise TypeError
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='WeatherStation %s, get_CDD given bad inputs, aborting function.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            result = None
        else:
            try:
                df = self.get_station_dataframe(start = start_date, end = end_date)
                df = df.sort_index()
                df = df['temperature']
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Retrieve data failed.',
                            comment='WeatherStation %s, get_CDD failed to retrieve station dataframe, aborting function.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                result = None
            else:
                try:
                    df = df.reindex(pd.date_range(start = start_date,
                                                    end = end_date,
                                                    freq = 'h'),
                                    fill_value = NaN)
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Reindex failed.',
                                comment='WeatherStation %s get_CDD failed to reindex dataframe (possible non-unique index) for %s-%s, aborting function.' % (self.id, start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')))
                    m.save()
                    self.messages.add(m)
                    print m
                    result = None
                else:
                    try:
                        df_filled = self.fill_temperature_gaps(df)
                        if len(df_filled) < 1:
                            raise TypeError
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Action failed.',
                                    comment='WeatherStation %s get_CDD unable to retrieve from fill_temperature_gaps function, aborting.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                        result = None                   
                    else:
                        if len(df_filled) == 0:
                            m = Message(when=timezone.now(),
                                        message_type='Code Warning',
                                        subject='No data.',
                                        comment='WeatherStation %s has no data in the timeframe requested, nothing to return.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                            result = None                   
                        else:
                            try:
                                cdd = Decimal(sum([max(float(x)-float(base_temp),0)/24 for x in df_filled]))
                                df_hours = (df_filled.index[-1]-df_filled.index[0]).days*24 + (df_filled.index[-1]-df_filled.index[0]).seconds/3600
                                timeframe_hours = (end_date - start_date).days*24 + (end_date - start_date).seconds/3600
                                result = [cdd, df_hours, timeframe_hours]
                            except:
                                m = Message(when=timezone.now(),
                                            message_type='Code Error',
                                            subject='Calculation failed.',
                                            comment='WeatherStation %s, get_CDD failed to compute CDD, aborting function.' % self.id)
                                m.save()
                                self.messages.add(m)
                                print m
                                result = None
                            else:
                                if (abs(result[1] - result[2]) / float(result[2])) > 0.01:
                                    m = Message(when=timezone.now(),
                                                message_type='Code Warning',
                                                subject='Missing data.',
                                                comment='Number of hours WeatherStation %s get_CDD used to compute CDD was more than 1%% different than number of hours between the provided start and end dates, CDD may be inaccurate.' % self.id)
                                    m.save()
                                    self.messages.add(m)
                                    print m
        return result
    def get_HDD(self, start_date, end_date, base_temp):
        """Inputs:
            start_date (datetime)
            end_date   (datetime)
            base_temp  (float, int, or decimal)
        
        Calls WeatherStation's dataframe
        and slices relevant time frame,
        then computes and returns HDD.
        Calls gap filler to interpolate
        and replace NaNs."""
        try:
            if not (  isinstance(start_date, datetime) and
                      isinstance(end_date, datetime) and
                      end_date > start_date and
                      type(base_temp) in [float, int, float64, int64]  ):
                raise TypeError
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='WeatherStation %s, get_HDD given bad inputs, aborting function.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            result = None
        else:
            try:
                df = self.get_station_dataframe(start = start_date, end = end_date)
                df = df.sort_index()
                df = df['temperature']
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Retrieve data failed.',
                            comment='WeatherStation %s, get_HDD failed to retrieve station dataframe, aborting function.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                result = None
            else:
                try:
                    df = df.reindex(pd.date_range(start = start_date,
                                                    end = end_date,
                                                    freq = 'h'),
                                    fill_value = NaN)
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Error',
                                subject='Reindex failed.',
                                comment='WeatherStation %s get_HDD failed to reindex dataframe (possible non-unique index) for %s-%s, aborting function.' % (self.id, start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')))
                    m.save()
                    self.messages.add(m)
                    print m
                    result = None
                else:
                    try:
                        df_filled = self.fill_temperature_gaps(df)
                        if len(df_filled) < 1:
                            raise TypeError
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Action failed.',
                                    comment='WeatherStation %s get_HDD unable to retrieve from fill_temperature_gaps function, aborting.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                        result = None                   
                    else:
                        if len(df_filled) == 0:
                            m = Message(when=timezone.now(),
                                        message_type='Code Warning',
                                        subject='No data.',
                                        comment='WeatherStation %s has no data in the timeframe requested, nothing to return.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                            result = None                   
                        else:
                            try:
                                hdd = Decimal(sum([max(float(base_temp)-float(x),0)/24 for x in df_filled]))
                                df_hours = (df_filled.index[-1]-df_filled.index[0]).days*24 + (df_filled.index[-1]-df_filled.index[0]).seconds/3600
                                timeframe_hours = (end_date - start_date).days*24 + (end_date - start_date).seconds/3600
                                result = [hdd, df_hours, timeframe_hours]
                            except:
                                m = Message(when=timezone.now(),
                                            message_type='Code Error',
                                            subject='Calculation failed.',
                                            comment='WeatherStation %s, get_HDD failed to compute HDD, aborting function.' % self.id)
                                m.save()
                                self.messages.add(m)
                                print m
                                result = None
                            else:
                                if (abs(result[1] - result[2]) / float(result[2])) > 0.01:
                                    m = Message(when=timezone.now(),
                                                message_type='Code Warning',
                                                subject='Missing data.',
                                                comment='Number of hours WeatherStation %s get_HDD used to compute HDD was more than 1%% different than number of hours between the provided start and end dates, HDD may be inaccurate.' % self.id)
                                    m.save()
                                    self.messages.add(m)
                                    print m
        return result
    def map_decimal(self, x):
        """Map Decimal to Ints/Floats."""
        if type(x) in [float,int,float64,int64]: x = Decimal(float(x))
        return x
    def purge_nones(self, x):
        """Swap NaN for None."""
        if x is None: x = NaN
        return x
    def purge_nones_str(self, x):
        """Swap empty string for None."""
        if x is None: x = ''
        return x
    def __unicode__(self):
        return self.name
    def connected_buildings_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
    connected_buildings_for_admin.allow_tags = True
    connected_buildings_for_admin.short_description = 'Connected Buildings'
    def connected_meters_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
    connected_meters_for_admin.allow_tags = True
    connected_meters_for_admin.short_description = 'Connected Meters'
    def missing_hours_for_admin(self):
        """Missing hours
        in weather data."""
        try:
            start_date = self.get_oldest_date().time
            end_date = self.get_newest_date().time
            if (start_date is None) or (end_date is None):
                answer = 'Data not found.'
            else:
                wdpts = self.get_station_dataframe(start = start_date, end = end_date)
                wdpts['blank'] = 1
                wdpts = wdpts['blank']
                wdpts = wdpts.sort_index()
                full_set = wdpts.reindex(pd.date_range(start = start_date, end = end_date, freq = 'h'),
                                         fill_value = NaN)
                missing_hours = full_set[pd.isnull(full_set)['blank']]
                answer = '<br>'.join([str(x) for x in missing_hours.index])
        except:
            answer = 'Unable to retrieve.'
        return answer
    missing_hours_for_admin.allow_tags = True
    missing_hours_for_admin.short_description = 'Missing Hours'
    def number_of_missing_hours_for_admin(self):
        """Number of missing hours
        in weather data."""
        try:
            start_date = self.get_oldest_date().time
            end_date = self.get_newest_date().time
            if (start_date is None) or (end_date is None):
                answer = 'Data not found.'
            else:
                num_wdpts = len(self.get_station_dataframe(start = start_date, end = end_date))
                num_hours = len(pd.date_range(start = start_date, end = end_date, freq = 'h'))
                answer = str(num_hours - num_wdpts)
        except:
            answer = 'Unable to calculate.'
        return answer
    number_of_missing_hours_for_admin.short_description = '# Missing Hours'
    def newest_data_point_for_admin(self):
        """Return newest datapoint's time."""
        dplist = self.weatherdatapoint_set.order_by('time')
        if len(dplist)<1:
            result = 'no weather data'
        else:
            datapoint = self.weatherdatapoint_set.order_by('time')[-1]
            result = '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_weatherdatapoint_change',args=(datapoint.id,)), str(datapoint.time))
        return result
    newest_data_point_for_admin.allow_tags = True
    newest_data_point_for_admin.short_description = 'Newest WeatherDataPoint'
    def oldest_data_point_for_admin(self):
        """Return oldest datapoint's time."""
        dplist = self.weatherdatapoint_set.order_by('time')
        if len(dplist)<1:
            result = 'no weather data'
        else:
            datapoint = self.weatherdatapoint_set.order_by('time')[0]
            result = '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_weatherdatapoint_change',args=(datapoint.id,)), str(datapoint.time))
        return result
    oldest_data_point_for_admin.allow_tags = True
    oldest_data_point_for_admin.short_description = 'Oldest WeatherDataPoint'
    def get_station_dataframe(self, start=[], end=[]):
        """Inputs:
            start (datetime, optional)
            end   (datetime, optional)
        
        Returns WeatherStation's dataframe
        of all WeatherDataPoints or those
        in the time frame requested."""
        try:
            if (start == []) and (end <> []):
                if not (isinstance(end,datetime)):
                    raise TypeError
                start = datetime(2000,1,1,0,tzinfo=UTC)
            elif (start <> []) and (end == []):
                if not (isinstance(start,datetime)):
                    raise TypeError
                end = datetime(2100,1,1,0,tzinfo=UTC)
            elif (start <> []) and (end <> []):
                if not (isinstance(start,datetime) and isinstance(end,datetime)):
                    raise TypeError
            elif (start == []) and (end == []):
                start = datetime(2000,1,1,0,tzinfo=UTC)
                end = datetime(2100,1,1,0,tzinfo=UTC)
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='WeatherStation %s, get_station_dataframe given improper inputs, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            df = None
        else:
            if self.weatherdatapoint_set.count() == 0:
                m = Message(when=timezone.now(),
                            message_type='Code Warning',
                            subject='Nothing to return.',
                            comment='WeatherStation %s, get_station_dataframe called when no WeatherDataPoints present.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                df = None
            else:
                try: #seems rounding sometimes causes end date to raise "NonExistentTimeError," fixed by removing 1 second
                    wdps = self.weatherdatapoint_set.filter(time__lt=end).filter(time__gte=start).order_by('time')
                except:
                    try:
                        wdps = self.weatherdatapoint_set.filter(time__lt=end-timedelta(seconds=1)).filter(time__gte=start).order_by('time')
                    except:
                        try:
                            wdps = self.weatherdatapoint_set.filter(time__lt=end).filter(time__gte=start-timedelta(seconds=1)).order_by('time')
                        except:
                            try:
                                wdps = self.weatherdatapoint_set.filter(time__lt=end-timedelta(seconds=1)).filter(time__gte=start-timedelta(seconds=1)).order_by('time')
                            except:
                                m = Message(when=timezone.now(),
                                            message_type='Code Error',
                                            subject='Unable to retrieve data.',
                                            comment='WeatherStation %s, get_station_dataframe unable to retrieve weather data points, function aborted.' % self.id)
                                m.save()
                                self.messages.add(m)
                                print m
                if wdps is not None:
                    t = pd.Series([x.time for x in wdps])
                    summary = pd.Series([x.summary for x in wdps],index=t)
                    icon = pd.Series([x.icon for x in wdps],index=t)
                    sunriseTime = pd.Series([x.sunriseTime for x in wdps],index=t)
                    sunsetTime = pd.Series([x.sunsetTime for x in wdps],index=t)
                    precipIntensity = pd.Series([x.precipIntensity for x in wdps],index=t)
                    precipIntensityMax = pd.Series([x.precipIntensityMax for x in wdps],index=t)
                    precipIntensityMaxTime = pd.Series([x.precipIntensityMaxTime for x in wdps],index=t)
                    precipProbability = pd.Series([x.precipProbability for x in wdps],index=t)
                    precipType = pd.Series([x.precipType for x in wdps],index=t)
                    precipAccumulation = pd.Series([x.precipAccumulation for x in wdps],index=t)
                    temperature = pd.Series([x.temperature for x in wdps],index=t)
                    temperatureMin = pd.Series([x.temperatureMin for x in wdps],index=t)
                    temperatureMinTime = pd.Series([x.temperatureMinTime for x in wdps],index=t)
                    temperatureMax = pd.Series([x.temperatureMax for x in wdps],index=t)
                    temperatureMaxTime = pd.Series([x.temperatureMaxTime for x in wdps],index=t)
                    dewPoint = pd.Series([x.dewPoint for x in wdps],index=t)
                    windSpeed = pd.Series([x.windSpeed for x in wdps],index=t)
                    windBearing = pd.Series([x.windBearing for x in wdps],index=t)
                    cloudCover = pd.Series([x.cloudCover for x in wdps],index=t)
                    humidity = pd.Series([x.humidity for x in wdps],index=t)
                    pressure = pd.Series([x.pressure for x in wdps],index=t)
                    visibility = pd.Series([x.visibility for x in wdps],index=t)
                    ozone = pd.Series([x.ozone for x in wdps],index=t)
                    df = pd.DataFrame({'summary' : summary,
                                       'icon' : icon,
                                       'sunriseTime' : sunriseTime,
                                       'sunsetTime' : sunsetTime,
                                       'precipIntensity' : precipIntensity,
                                       'precipIntensityMax' : precipIntensityMax,
                                       'precipIntensityMaxTime' : precipIntensityMaxTime,
                                       'precipProbability' : precipProbability,
                                       'precipType' : precipType,
                                       'precipAccumulation' : precipAccumulation,
                                       'temperature' : temperature,
                                       'temperatureMin' : temperatureMin,
                                       'temperatureMinTime' : temperatureMinTime,
                                       'temperatureMax' : temperatureMax,
                                       'temperatureMaxTime' : temperatureMaxTime,
                                       'dewPoint' : dewPoint,
                                       'windSpeed' : windSpeed,
                                       'windBearing' : windBearing,
                                       'cloudCover' : cloudCover,
                                       'humidity' : humidity,
                                       'pressure' : pressure,
                                       'visibility' : visibility,
                                       'ozone' : ozone,})
                    df = df.sort_index()
                else:
                    df = None
        return df
    def load_station_dataframe(self, df):
        """Inputs:
            df (columns match ForecastIO datapoint)
        
        Loads given dataframe into WeatherStation
        by adding WeatherDataPoints. Index
        should contain continuous, unique
        datetimes and be tz-aware in UTC."""

        try:
            (min([x in df.columns for x in ['summary','icon','sunriseTime','sunsetTime',
                                               'precipIntensity','precipIntensityMax',
                                               'precipIntensityMaxTime','precipProbability',
                                               'precipType','precipAccumulation','temperature',
                                               'temperatureMin','temperatureMinTime',
                                               'temperatureMax','temperatureMaxTime','dewPoint',
                                               'windSpeed','windBearing','cloudCover','humidity',
                                               'pressure','visibility','ozone']]) and
                (len(df)>0) and (df.index.tzinfo is UTC))
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Function received bad arguments.',
                        comment='WeatherStation %s, load_station_dataframe given improper dataframe input, function aborted.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = False
        else:
            if (min([x in df.columns for x in ['summary','icon','sunriseTime','sunsetTime',
                                               'precipIntensity','precipIntensityMax',
                                               'precipIntensityMaxTime','precipProbability',
                                               'precipType','precipAccumulation','temperature',
                                               'temperatureMin','temperatureMinTime',
                                               'temperatureMax','temperatureMaxTime','dewPoint',
                                               'windSpeed','windBearing','cloudCover','humidity',
                                               'pressure','visibility','ozone']]) and
                (len(df)>0) and (df.index.tzinfo is UTC)):
                df = df.sort_index()
                dfexist = self.get_station_dataframe()
                if dfexist is None:
                    dfexist = pd.DataFrame()
                    m = Message(when=timezone.now(),
                                message_type='Code Warning',
                                subject='No data found.',
                                comment='Found no existing weather data points for WeatherStation %s running load_station_dataframe function, continuing to load provided dataframe.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    success = False
                for i in range(0,len(df)):
                    try:
                        if df.index[i] not in dfexist.index:
                            wdp = WeatherDataPoint(
                                    time = df.index[i],
                                    summary = df['summary'][i],
                                    icon = df['icon'][i],
                                    sunriseTime = df['sunriseTime'][i],
                                    sunsetTime = df['sunsetTime'][i],
                                    precipIntensity = df['precipIntensity'][i],
                                    precipIntensityMax = df['precipIntensityMax'][i],
                                    precipIntensityMaxTime = df['precipIntensityMaxTime'][i],
                                    precipProbability = df['precipProbability'][i],
                                    precipType = df['precipType'][i],
                                    precipAccumulation = df['precipAccumulation'][i],
                                    temperature = df['temperature'][i],
                                    temperatureMin = df['temperatureMin'][i],
                                    temperatureMinTime = df['temperatureMinTime'][i],
                                    temperatureMax = df['temperatureMax'][i],
                                    temperatureMaxTime = df['temperatureMaxTime'][i],
                                    dewPoint = df['dewPoint'][i],
                                    windSpeed = df['windSpeed'][i],
                                    windBearing = df['windBearing'][i],
                                    cloudCover = df['cloudCover'][i],
                                    humidity = df['humidity'][i],
                                    pressure = df['pressure'][i],
                                    visibility = df['visibility'][i],
                                    ozone = df['ozone'][i],
                                    weather_station = self)
                            wdp.save()
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Model update failed.',
                                    comment='Unable to create WeatherDataPoint %s during load_station_dataframe function for WeatherStation %s, moving to next row.' % (str(df.index[i]), self.id))
                        m.save()
                        self.messages.add(m)
                        print m
                        success = False
                    else:
                        m = Message(when=timezone.now(),
                                    message_type='Code Success',
                                    subject='Model updated.',
                                    comment='Loaded WeatherDataPoint %s into WeatherStation %s.' % (str(df.index[i]), self.id))
                        m.save()
                        self.messages.add(m)
                        print m
                        success = True                        
            else:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Function received bad arguments.',
                            comment='WeatherStation %s, load_station_dataframe given improper dataframe input, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = False
        return success
    def load_weather_day(self, date):
        """Input: date (datetime)
        
        Retrieves the given day's
        hourly and daily data
        points from ForecastIO
        and loads into station."""
        try:
            try:
                checktype = isinstance(date,datetime)
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Function received bad arguments.',
                            comment='WeatherStation %s, load_weather_day function given non-datetime input, function aborted.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = False
            else:
                if checktype:
                    try:
                        forecast = Forecastio("10b931b8efd054dfd24502d9de6477ed")
                        result = forecast.loadForecast(self.latitude,self.longitude, time=date, units='us', lazy=True)
                        hourlypts = forecast.getHourly()
                        dailypt = forecast.getDaily()
                    except:
                        m = Message(when=timezone.now(),
                                    message_type='Code Error',
                                    subject='Retrieve data failed.',
                                    comment='WeatherStation %s, load_weather_day function unable to access weather data from Forecast API, function aborted.' % self.id)
                        m.save()
                        self.messages.add(m)
                        print m
                        success = False
                    else:
                        if len(hourlypts.data) < 1 or len(dailypt.data) < 1:
                            m = Message(when=timezone.now(),
                                        message_type='Code Warning',
                                        subject='No data found.',
                                        comment='WeatherStation %s load_weather_day function found no data from Forecast API for day %s, function aborted.' % (self.id, str(date)))
                            m.save()
                            self.messages.add(m)
                            print m
                            success = False
                        else:
                            try:
                                rawtimes = [x.time for x in hourlypts.data]
                                station_timezone = tz(self.tz_name)
                                utc_tz_aware_times = [station_timezone.localize(x).astimezone(UTC) for x in rawtimes]
                                t = pd.Series(utc_tz_aware_times)
                                summary = pd.Series([x.summary for x in hourlypts.data],index=t)
                                icon = pd.Series([x.icon for x in hourlypts.data],index=t)
                                precipIntensity = pd.Series([x.precipIntensity for x in hourlypts.data],index=t)
                                precipProbability = pd.Series([x.precipProbablility for x in hourlypts.data],index=t) #sic - it's misspelled on their end
                                precipType = pd.Series([x.precipType for x in hourlypts.data],index=t)
                                temperature = pd.Series([x.temperature for x in hourlypts.data],index=t)
                                dewPoint = pd.Series([x.dewPoint for x in hourlypts.data],index=t)
                                windSpeed = pd.Series([x.windspeed for x in hourlypts.data],index=t)
                                windBearing = pd.Series([x.windbaring for x in hourlypts.data],index=t) #sic - it's misspelled on their end
                                cloudCover = pd.Series([x.cloudcover for x in hourlypts.data],index=t)
                                humidity = pd.Series([x.humidity for x in hourlypts.data],index=t)
                                pressure = pd.Series([x.pressure for x in hourlypts.data],index=t)
                                visibility = pd.Series([x.visbility for x in hourlypts.data],index=t) #sic - it's misspelled on their end
                                ozone = pd.Series([x.ozone for x in hourlypts.data],index=t)
                                
                                x = pd.Series(t,index=t)
                                
                                sunriseTime = pd.Series(x,index=t)
                                sunsetTime = pd.Series(x,index=t)
                                precipIntensityMax = pd.Series(x,index=t)
                                precipIntensityMaxTime = pd.Series(x,index=t)
                                precipAccumulation = pd.Series(x,index=t)
                                temperatureMin = pd.Series(x,index=t)
                                temperatureMinTime = pd.Series(x,index=t)
                                temperatureMax = pd.Series(x,index=t)
                                temperatureMaxTime = pd.Series(x,index=t)
        
        #                        sunriseTime = sunriseTime.map(lambda x: UTC.localize(dailypt.data[0].sunriseTime))
        #                        sunsetTime = sunsetTime.map(lambda x: UTC.localize(dailypt.data[0].sunsetTime))
        #                        precipIntensityMax = precipIntensityMax.map(lambda x: dailypt.data[0].precipIntensityMax)
        #                        precipIntensityMaxTime = precipIntensityMaxTime.map(lambda x: UTC.localize(datetime.fromtimestamp(int(dailypt.data[0].precipIntensityMaxTime))))
        #                        precipAccumulation = precipAccumulation.map(lambda x: dailypt.data[0].precipAccumulation)
        #                        temperatureMin = temperatureMin.map(lambda x: dailypt.data[0].temperatureMin)
        #                        temperatureMinTime = temperatureMinTime.map(lambda x: UTC.localize(datetime.fromtimestamp(int(dailypt.data[0].temperatureMinTime))))
        #                        temperatureMax = temperatureMax.map(lambda x: dailypt.data[0].temperatureMax)
        #                        temperatureMaxTime = temperatureMaxTime.map(lambda x: UTC.localize(datetime.fromtimestamp(int(dailypt.data[0].temperatureMaxTime))))
        
                                
                                if dailypt.data[0].sunriseTime is not None:
                                    sunriseTime = sunriseTime.map(lambda x: UTC.localize(dailypt.data[0].sunriseTime))
                                else:
                                    sunriseTime = sunriseTime.map(lambda x: None)
                                    
                                if dailypt.data[0].sunsetTime is not None:
                                    sunsetTime = sunsetTime.map(lambda x: UTC.localize(dailypt.data[0].sunsetTime))
                                else:
                                    sunsetTime = sunsetTime.map(lambda x: None)
                                
                                if dailypt.data[0].precipIntensityMax is not None:
                                    precipIntensityMax = precipIntensityMax.map(lambda x: dailypt.data[0].precipIntensityMax)
                                else:
                                    precipIntensityMax = precipIntensityMax.map(lambda x: None)
                                
                                if dailypt.data[0].precipIntensityMaxTime is not None:
                                    precipIntensityMaxTime = precipIntensityMaxTime.map(lambda x: UTC.localize(datetime.fromtimestamp(int(dailypt.data[0].precipIntensityMaxTime))))
                                else:
                                    precipIntensityMaxTime = precipIntensityMaxTime.map(lambda x: None)
                                
                                if dailypt.data[0].precipAccumulation is not None:
                                    precipAccumulation = precipAccumulation.map(lambda x: dailypt.data[0].precipAccumulation)
                                else:
                                    precipAccumulation = precipAccumulation.map(lambda x: None)
                                
                                if dailypt.data[0].temperatureMin is not None:
                                    temperatureMin = temperatureMin.map(lambda x: dailypt.data[0].temperatureMin)
                                else:
                                    temperatureMin = temperatureMin.map(lambda x: None)
                                
                                if dailypt.data[0].temperatureMinTime is not None:
                                    temperatureMinTime = temperatureMinTime.map(lambda x: UTC.localize(datetime.fromtimestamp(int(dailypt.data[0].temperatureMinTime))))
                                else:
                                    temperatureMinTime = temperatureMinTime.map(lambda x: None)
                                
                                if dailypt.data[0].temperatureMax is not None:
                                    temperatureMax = temperatureMax.map(lambda x: dailypt.data[0].temperatureMax)
                                else:
                                    temperatureMax = temperatureMax.map(lambda x: None)
                                
                                if dailypt.data[0].temperatureMaxTime is not None:
                                    temperatureMaxTime = temperatureMaxTime.map(lambda x: UTC.localize(datetime.fromtimestamp(int(dailypt.data[0].temperatureMaxTime))))
                                else:
                                    temperatureMaxTime = temperatureMaxTime.map(lambda x: None)
                                
                                
                                df = pd.DataFrame({'summary' : summary,
                                                   'icon' : icon,
                                                   'sunriseTime' : sunriseTime,
                                                   'sunsetTime' : sunsetTime,
                                                   'precipIntensity' : precipIntensity,
                                                   'precipIntensityMax' : precipIntensityMax,
                                                   'precipIntensityMaxTime' : precipIntensityMaxTime,
                                                   'precipProbability' : precipProbability,
                                                   'precipType' : precipType,
                                                   'precipAccumulation' : precipAccumulation,
                                                   'temperature' : temperature,
                                                   'temperatureMin' : temperatureMin,
                                                   'temperatureMinTime' : temperatureMinTime,
                                                   'temperatureMax' : temperatureMax,
                                                   'temperatureMaxTime' : temperatureMaxTime,
                                                   'dewPoint' : dewPoint,
                                                   'windSpeed' : windSpeed,
                                                   'windBearing' : windBearing,
                                                   'cloudCover' : cloudCover,
                                                   'humidity' : humidity,
                                                   'pressure' : pressure,
                                                   'visibility' : visibility,
                                                   'ozone' : ozone},
                                                   index = t)
                                df = df.tz_convert('UTC')
                                df = df.sort_index()
                                df = df.applymap(self.map_decimal)
                            except:
                                m = Message(when=timezone.now(),
                                            message_type='Code Error',
                                            subject='Create dataframe failed.',
                                            comment='WeatherStation %s, load_weather_day function unable to create dataframe of retrieved weather data, function aborted.' % self.id)
                                m.save()
                                self.messages.add(m)
                                print m
                                success = False
                            else:
                                loadsuccess = self.load_station_dataframe(df)
                                if loadsuccess:
                                    m = Message(when=timezone.now(),
                                                message_type='Code Success',
                                                subject='Model updated.',
                                                comment='WeatherStation %s, load_weather_day successfully loaded the following weather day: %s.' % (self.id, str(date)))
                                    m.save()
                                    self.messages.add(m)
                                    print m
                                    success = True
                                else:
                                    m = Message(when=timezone.now(),
                                                message_type='Code Error',
                                                subject='Model update failed.',
                                                comment='WeatherStation %s, load_weather_day unable to load the following weather day: %s.' % (self.id, str(date)))
                                    m.save()
                                    self.messages.add(m)
                                    print m
                                    success = False
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='Model update failed.',
                        comment='WeatherStation %s, load_weather_day unable to load the following weather day: %s.' % (self.id, str(date)))
            m.save()
            self.messages.add(m)
            print m
            success = False
        return success
    
    @job
    def load_weather_file(self, file_location=0):
        """Inputs: filelocation
            (optional, default S3 upload)
        
        Upload Excel file with
        day dates to load into 
        WeatherStation."""
        
        if not(file_location): file_location = self.weather_data_upload_file.url
        
        try:
            readbd = pd.read_csv(file_location,
                                 skiprows=0,
                                 usecols=['Days'])
        except:
            m = Message(when=timezone.now(),
                        message_type='Code Error',
                        subject='File not found.',
                        comment='WeatherStation %s failed on load_weather_file function when attempting to read uploaded weather data file.' % self.id)
            m.save()
            self.messages.add(m)
            print m
            success = None
        else:
            try:
                readbd['Days'] = readbd['Days'].apply(pd.to_datetime)   #make datetime
                local_tz = tz(self.tz_name)                  #create tz object
                readbd['Days'] = readbd['Days'].apply(local_tz.localize)#make datetimes tz-aware
                readbd['Days'] = readbd['Days'].apply(lambda x: x.astimezone(UTC)) #convert to UTC
            except:
                m = Message(when=timezone.now(),
                            message_type='Code Error',
                            subject='Expected contents not found.',
                            comment='WeatherStation %s failed on load_weather_file function, uploaded file does not have appropriate data.' % self.id)
                m.save()
                self.messages.add(m)
                print m
                success = None
            else:
                try:
                    storedbc = self.get_station_dataframe()
                except:
                    m = Message(when=timezone.now(),
                                message_type='Code Warning',
                                subject='No existing data.',
                                comment='WeatherStation %s had no existing data during load_weather_file function.' % self.id)
                    m.save()
                    self.messages.add(m)
                    print m
                    success = None
                else:
                    if storedbc is None:
                        try:
                            for d in readbd['Days'].values:
                                success = self.load_weather_day(d)
                        except:
                            m = Message(when=timezone.now(),
                                        message_type='Code Error',
                                        subject='Unable to load data.',
                                        comment='WeatherStation %s failed to load weather data during load_weather_file function.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                            success = None
                    else:
                        try:
                            storedbc_days = [x.date() for x in storedbc.index]
                            for d in readbd['Days'].values:
                                if d.date() not in storedbc_days: success = self.load_weather_day(d)
                        except:
                            m = Message(when=timezone.now(),
                                        message_type='Code Error',
                                        subject='Unable to load data.',
                                        comment='WeatherStation %s failed to load weather data during load_weather_file function.' % self.id)
                            m.save()
                            self.messages.add(m)
                            print m
                            success = None
        self.weather_data_import = False
        return success
    def save(self, *args, **kwargs):
        if self.weather_data_import:
            super(WeatherStation, self).save(*args, **kwargs)
            self.load_weather_file()
        super(WeatherStation, self).save(*args, **kwargs)
    class Meta:
        app_label = 'BuildingSpeakApp'


class WeatherDataPoint(models.Model):
    """Model for storing weather
    data point info from Forecast
    API."""
    time = models.DateTimeField(blank=True,null=True,help_text='UTC time at which weather data point occurs.')
    summary = models.CharField(null=True,blank=True, max_length=200,
                help_text='A human-readable text summary of this data point.')
    icon = models.CharField(null=True,blank=True, max_length=200,
                help_text='A machine-readable text summary of this data point, suitable for selecting an icon for display. If defined, this property will have one of the following values: clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day, or partly-cloudy-night. (Developers should ensure that a sensible default is defined, as additional values, such as hail, thunderstorm, or tornado, may be defined in the future.)')
    sunriseTime = models.DateTimeField(blank=True,null=True,help_text='Only defined on daily data points.')
    sunsetTime = models.DateTimeField(blank=True,null=True,help_text='Only defined on daily data points.')
    precipIntensity = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value representing the average expected intensity (in inches of liquid water per hour) of precipitation occurring at the given time conditional on probability (that is, assuming any precipitation occurs at all). A very rough guide is that a value of 0 corresponds to no precipitation, 0.002 corresponds to very light sprinkling, 0.017 corresponds to light precipitation, 0.1 corresponds to moderate precipitation, and 0.4 corresponds to very heavy precipitation.')
    precipIntensityMax = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='Only defined on daily data points, numerical values representing the maximumum expected intensity of precipitation on the given day in inches of liquid water per hour.')
    precipIntensityMaxTime = models.DateTimeField(blank=True,null=True)
    precipProbability = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='Only defined on daily data points, time at which precipIntensityMax occurs.')
    precipType = models.CharField(null=True,blank=True, max_length=200,
                help_text='A string representing the type of precipitation occurring at the given time; if defined, this property will have one of the following values: rain, snow, sleet (which applies to each of freezing rain, ice pellets, and wintery mix), or hail; if precipIntensity is zero, then this property will not be defined.')
    precipAccumulation = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='Only defined on daily data points, the amount of snowfall accumulation expected to occur on the given day; if no accumulation is expected, this property will not be defined.')
    temperature = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='Not defined on daily data points, a numerical value representing the temperature at the given time in degrees Fahrenheit.')
    temperatureMin = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='Only defined on daily data points, numerical value representing the minimum temperature on the given day in degrees Fahrenheit.')
    temperatureMinTime = models.DateTimeField(blank=True,null=True,help_text='Time temperatureMin occurs.')
    temperatureMax = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='Only defined on daily data points, numerical value representing the maximum temperature on the given day in degrees Fahrenheit.')
    temperatureMaxTime = models.DateTimeField(blank=True,null=True,help_text='Time temperatureMax occurs.')
    dewPoint = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value representing the dew point at the given time in degrees Fahrenheit.')
    windSpeed = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value representing the wind speed in miles per hour.')
    windBearing = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value representing the direction that the wind is coming from in degrees, with true north at 0 degrees and progressing clockwise; if windSpeed is zero, then this value will not be defined.')
    cloudCover = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value between 0 and 1 (inclusive) representing the percentage of sky occluded by clouds: 0 corresponds to clear sky, 0.4 to scattered clouds, 0.75 to broken cloud cover, and 1 to completely overcast skies.')
    humidity = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value between 0 and 1 (inclusive) representing the relative humidity.')
    pressure = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value representing the sea-level air pressure in millibars.')
    visibility = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value representing the average visibility in miles, capped at 10 miles.')
    ozone = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=3,
                help_text='A numerical value representing the columnar density of total atmospheric ozone at the given time in Dobson units.')
    
    
    #relationships
    weather_station = models.ForeignKey('WeatherStation')
    
    #functions
    def weather_station_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_weatherstation_change',args=(self.weather_station.id,)), self.weather_station.name)
    weather_station_for_admin.allow_tags = True
    weather_station_for_admin.short_description = 'Weather Station'
    def __unicode__(self):
        return str(self.time)

    class Meta:
        app_label = 'BuildingSpeakApp'
