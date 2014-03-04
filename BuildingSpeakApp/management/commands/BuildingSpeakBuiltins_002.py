from django.core.management.base import BaseCommand

import urllib
from decimal import Decimal

from django.core.files import File

from BuildingSpeak.settings import STATIC_URL

from BuildingSpeakApp.models import WeatherStation, Utility


class Command(BaseCommand):

    def handle(self, *args, **options):
    ###---WeatherStations
        try:
            ws1 = WeatherStation(
                name = 'Cortland, NY',
                description = '',
                latitude = Decimal(42.601165),
                longitude = Decimal(-76.180506),
                tz_name = 'US/Eastern',
                )
            ws1.save()
        except:
            print 'Failed to create new WeatherStations.'
        else:
            print 'Created new WeatherStations.'
        
    ###---Utilitys
        try:
            util1 = Utility(
                name = 'National Grid',
                )
            util1.save()
            #post-creation actions
            #--load image file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_002/nationalgridlogo.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            util1.__setattr__('image_file', file_obj)
            util1.save()
            
            util2 = Utility(
                name = 'Hess Energy Marketing',
                )
            util2.save()
            #post-creation actions
            #--load image file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_002/hess_logo.png'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            util2.__setattr__('image_file', file_obj)
            util2.save()

            util3 = Utility(
                name = 'NYSEG',
                )
            util3.save()
            #post-creation actions
            #--load image file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_002/nyseg.gif'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            util3.__setattr__('image_file', file_obj)
            util3.save()

        except:
            print 'Failed to create new Utilities.'
        else:
            print 'Created new Utilities.'

