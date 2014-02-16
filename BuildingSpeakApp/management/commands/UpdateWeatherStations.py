from django.core.management.base import BaseCommand

import pandas as pd
from pytz import UTC
from datetime import datetime

from django.utils import timezone

from BuildingSpeakApp.models import WeatherStation


class Command(BaseCommand):

    def handle(self, *args, **options):

        for ws in WeatherStation.objects.all():
            try:
                required_days = [i.strftime('%Y-%m-%d') for i in pd.date_range(start = datetime(2009, 1, 1, tzinfo = UTC),
                                                                               end = timezone.now())]
                stored_days = ws.get_list_of_days()
                days_to_load = [i for i in required_days if i not in stored_days]
                for j in days_to_load:
                    result = ws.load_weather_day(UTC.localize(datetime.strptime(j,'%Y-%m-%d')))
            except:
                print 'Failed to completely update WeatherStation %s.' % ws.name
            else:
                print 'Updated WeatherStation %s.' % ws.name