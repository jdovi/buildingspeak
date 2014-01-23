from django.core.management.base import BaseCommand

from decimal import Decimal
from BuildingSpeakApp.models import WeatherStation

class Command(BaseCommand):

    def handle(self, *args, **options):

        ATLdw = WeatherStation(
            name = 'ATL - downtown west',
            description = '1300 Joseph Boone Blvd, Atlanta, GA 30314',
            latitude = Decimal(33.7637360),
            longitude = Decimal(-84.4301300),
            tz_name = 'US/Eastern',
            )
        ATLdw.save()
        
        #post-creation actions: run command to load weather data