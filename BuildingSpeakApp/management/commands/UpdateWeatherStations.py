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
                newest_date = ws.get_newest_date()
                if newest_date is None: newest_date = datetime(2011, 1, 1, tzinfo = UTC)
                date_range = pd.date_range(start = newest_date,
                                           end = timezone.now())
                list_of_days = [i.to_datetime() for i in date_range]
                for j in list_of_days:
                    result = ws.load_weather_day(j)
                    if result and j.day == 1: print 'Running %s for Weather Station %s.' % (j.strftime('%Y-%m-%d'), ws.name)
            except:
                print 'Failed to completely update WeatherStation %s.' % ws.name
