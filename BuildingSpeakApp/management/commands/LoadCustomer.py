from django.core.management.base import BaseCommand

from pytz import UTC
from decimal import Decimal
from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User

from BuildingSpeak.settings import STATIC_URL

from BuildingSpeakApp.models import UserProfile, Account, Building, Space, Meter
from BuildingSpeakApp.models import SpaceMeterApportionment, BuildingMeterApportionment
from BuildingSpeakApp.models import EfficiencyMeasure, EMMeterApportionment, EMEquipmentApportionment
from BuildingSpeakApp.models import WeatherStation, Utility
from BuildingSpeakApp.models import GeneralConsumption
from BuildingSpeakApp.models import set_file_field



class Command(BaseCommand):

    def handle(self, *args, **options):

    ###---Users
        try:
            userJD = User.objects.get(username = 'jdovi')       #loaded to add to all new accounts
            userDA = User.objects.get(username = 'dashley')     #loaded to add to all new accounts
            
            user1 = User(
                username = 'jdovi1',
                password = 'lastlostleast',
                first_name = 'Jesse',
                last_name = 'Dovi',
                email = 'jesse@dovimotors.com',
                is_active = True,
                is_staff = False,
                is_superuser = False,
                )
            user1.save()
        except:
            print 'Failed to create new Users.'
        else:
            print 'Created new Users.'
            
    ###---UserProfiles
        try:
            userprofile1 = UserProfile(
                user = user1,
                organization = 'Dovi Motors Inc. - COR'
                )
            userprofile1.save()
            #post-creation actions
            #--load image file
            set_file_field(userprofile1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/default.jpg')
        except:
            print 'Failed to create new UserProfiles.'
        else:
            print 'Created new UserProfiles.'
            
    ###---Account
        try:
            acct1 = Account(
                name = 'Dovi Motors Inc. - COR',
                account_type = 'Commercial',
                street_address = '263 Tompkins St',
                city = 'Cortland',
                state = 'NY',
                zip_code = '13045',
                launch_date = timezone.now(),
                first_name = 'Jesse',
                last_name = 'Dovi',
                title = 'Owner',
                email = 'jesse@dovimotors.com',
                phone = '607-756-2801',
                status = 'Active',
                monthly_payment = Decimal(0.0),
                )
            acct1.save()
            
            #post-creation actions
            #--attach users
            acct1.users.add(user1)
            acct1.users.add(userJD)
            acct1.users.add(userDA)
            
            #--load image file
            set_file_field(acct1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/default.jpg')
        except:
            print 'Failed to create new Accounts.'
        else:
            print 'Created new Accounts.'
        
    ###---Buildings
        try:
            ws = WeatherStation.objects.get(name = 'Cortland, NY')
            
            bldg1 = Building(
                name = 'Main Building',
                building_type = 'Automotive Facility',
                EIA_type = 'Mercantile - Retail (Other Than Mall)',
                ESPM_type = 'Retail Store',
                account = acct1,
                weather_station = ws,
                street_address = '263 Tompkins St',
                city = 'Cortland',
                state = 'NY',
                zip_code = '13045',
                age = 1950,
                square_footage = Decimal(8401),
                stories = 1,
                max_occupancy = None,
                first_name = 'Jesse',
                last_name = 'Dovi',
                title = 'Owner',
                email = 'jesse@dovimotors.com',
                phone = '607-756-2801',
                )
            bldg1.save()
    
            #post-creation actions
            #--load image file
            set_file_field(bldg1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/BuildingImages/main.JPG')
            
            bldg2 = Building(
                name = 'Body Shop',
                building_type = 'Automotive Facility',
                EIA_type = 'Warehouse and Storage',
                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
                account = acct1,
                weather_station = ws,
                street_address = '263 Tompkins St',
                city = 'Cortland',
                state = 'NY',
                zip_code = '13045',
                age = 1975,
                square_footage = Decimal(2800),
                stories = 1,
                max_occupancy = None,
                first_name = 'Jesse',
                last_name = 'Dovi',
                title = 'Owner',
                email = 'jesse@dovimotors.com',
                phone = '607-756-2801',
                )
            bldg2.save()
            
            #post-creation actions:
            #--load image file
            set_file_field(bldg2,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/BuildingImages/body.JPG')
        except:
            print 'Failed to create new Buildings.'
        else:
            print 'Created new Buildings.'
        
    ###---Spaces
        try:
            space1 = Space(
                name = 'Showroom',
                building = bldg1,
                square_footage = Decimal(4000),
                max_occupancy = None,
                space_type = 'Automotive Facility',
                EIA_type = 'Mercantile - Retail (Other Than Mall)',
                ESPM_type = 'Retail Store',
                )
            space1.save()
            #post-creation actions:
            #--load image file
            set_file_field(space1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            space2 = Space(
                name = 'Repair Shop',
                building = bldg1,
                square_footage = Decimal(4401),
                max_occupancy = None,
                space_type = 'Automotive Facility',
                EIA_type = 'Warehouse and Storage',
                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
                )
            space2.save()
            #post-creation actions:
            #--load image file
            set_file_field(space2,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
        except:
            print 'Failed to create new Spaces.'
        else:
            print 'Created new Spaces.'
            
    ###---Meters
        try:
            u1 = Utility.objects.get(name = 'National Grid')
            u2 = Utility.objects.get(name = 'Hess Energy Marketing')
            u3 = Utility.objects.get(name = 'NYSEG')
            u4 = Utility.objects.get(name = 'WATERXXXXXX')
            
            r1 = GeneralConsumption(name = 'National Grid - Dovi Motors',
                                    utility = u1,
                                    rate_type = 'moving average',
                                    moving_average_window_length = 6)
            r1.save()
            r2 = GeneralConsumption(name = 'Hess Energy Marketing - Dovi Motors',
                                    utility = u2,
                                    rate_type = 'moving average',
                                    moving_average_window_length = 6)
            r2.save()
            r3 = GeneralConsumption(name = 'NYSEG - Dovi Motors',
                                    utility = u3,
                                    rate_type = 'moving average',
                                    moving_average_window_length = 6)
            r3.save()
            r4 = GeneralConsumption(name = 'WATERXXXX - Dovi Motors',
                                    utility = u4,
                                    rate_type = 'moving average',
                                    moving_average_window_length = 6)
            r4.save()
            
            meter1 = Meter(
                name = 'Main Building (electric)',
                utility_type = 'electricity',
                location = 'Side of bldg inside parts cage',
                serves = 'all of main building',
                units = 'kW,kWh',
                weather_station = ws,
                utility = u2,
                rate_schedule = r2,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '05036-74100',
                utility_meter_number = '05542682',
                )
            meter1.save()
            #post-creation actions:
            #--load image files
            set_file_field(meter1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/Main_Meter.JPG')
            set_file_field(meter1,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/Main_Meter.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(meter1,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/main-electric.csv')
            try:
                meter1.upload_bill_data(create_models_if_nonexistent=True)
            except:
                print 'Failed to upload data for Meter %s.' % str(meter1.id)
            meter1.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = meter1,
                                              building = bldg1,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = meter1,
                                           space = space2,
                                           assigned_fraction = Decimal(0.4))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = meter1,
                                           space = space1,
                                           assigned_fraction = Decimal(0.6))
            sma2.save()
            
            meter2 = Meter(
                name = 'Body Shop (electric)',
                utility_type = 'electricity',
                location = 'East side of the body shop',
                serves = 'Body Shop',
                units = 'kW,kWh',
                weather_station = ws,
                utility = u2,
                rate_schedule = r2,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '05036-74100',
                utility_meter_number = '34264564',
                )
            meter2.save()
            #post-creation actions:
            #--load image files
            set_file_field(meter2,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/Body_Meter.JPG')
            set_file_field(meter2,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/Body_Meter.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(meter2,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/body-electric.csv')
            try:
                meter2.upload_bill_data(create_models_if_nonexistent = True)
            except:
                print 'Failed to upload data for Meter %s.' % str(meter2.id)
            meter2.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = meter2,
                                              building = bldg2,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            
            
            
            meter3 = Meter(
                name = 'Main Building (natural gas)',
                utility_type = 'natural gas',
                location = 'unknown',
                serves = 'Main bldg heating and domestic hot water',
                units = 'ccf/h,ccf',
                weather_station = ws,
                utility = u3,
                rate_schedule = r3,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '1001-0074-630',
                utility_meter_number = '06079962',
                )
            meter3.save()
            #post-creation actions:
            #--load image files
            set_file_field(meter3,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/default_meter_image.png')
            set_file_field(meter3,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/default_meter_image.png')
            #--load bill data file, possibly create meter models
            set_file_field(meter3,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/main-gas.csv')
            try:
                meter3.upload_bill_data(create_models_if_nonexistent = True)
            except:
                print 'Failed to upload data for Meter %s.' % str(meter3.id)
            meter3.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = meter3,
                                              building = bldg1,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = meter3,
                                           space = space2,
                                           assigned_fraction = Decimal(0.6))
            sma1.save()
            sma1 = SpaceMeterApportionment(meter = meter3,
                                           space = space1,
                                           assigned_fraction = Decimal(0.4))
            sma1.save()
            
            meter4 = Meter(
                name = 'Body Shop (natural gas)',
                utility_type = 'natural gas',
                location = 'unknown',
                serves = 'Body Shop heating and domestic hot water',
                units = 'ccf/h,ccf',
                weather_station = ws,
                utility = u3,
                rate_schedule = r3,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '1001-0631-181',
                utility_meter_number = '0C263464',
                )
            meter4.save()
            #post-creation actions:
            #--load image files
            set_file_field(meter4,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/default_meter_image.png')
            set_file_field(meter4,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/default_meter_image.png')
            #--load bill data file, possibly create meter models
            set_file_field(meter4,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/body-gas.csv')
            try:
                meter4.upload_bill_data(create_models_if_nonexistent = True)
            except:
                print 'Failed to upload data for Meter %s.' % str(meter4.id)
            meter4.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = meter4,
                                              building = bldg2,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            
            
            meter5 = Meter(
                name = 'Main Building (water)',
                utility_type = 'domestic water',
                location = 'unknown',
                serves = 'unknown',
                units = 'gpm,gal',
                weather_station = ws,
                utility = u4,
                rate_schedule = r4,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '316',
                utility_meter_number = 'unknown',
                )
            meter5.save()
            #post-creation actions:
            #--load image files
            set_file_field(meter5,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MainWater_Meter.JPG')
            set_file_field(meter5,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MainWater_Meter.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(meter5,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/main-water.csv')
            try:
                meter5.upload_bill_data(create_models_if_nonexistent = True)
            except:
                print 'Failed to upload data for Meter %s.' % str(meter5.id)
            meter5.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = meter5,
                                              building = bldg1,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = meter5,
                                           space = space1,
                                           assigned_fraction = Decimal(.5))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = meter5,
                                           space = space2,
                                           assigned_fraction = Decimal(.5))
            sma2.save()
            
            meter6 = Meter(
                name = 'Body Shop (water)',
                utility_type = 'domestic water',
                location = 'unknown',
                serves = 'unknown',
                units = 'gpm,gal',
                weather_station = ws,
                utility = u4,
                rate_schedule = r4,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '315',
                utility_meter_number = 'unknown',
                )
            meter6.save()
            #post-creation actions:
            #--load image files
            set_file_field(meter6,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/BodyWater_Meter.JPG')
            set_file_field(meter6,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/BodyWater_Meter.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(meter6,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/body-water.csv')
            try:
                meter6.upload_bill_data(create_models_if_nonexistent = True)
            except:
                print 'Failed to upload data for Meter %s.' % str(meter6.id)
            meter6.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = meter6,
                                              building = bldg2,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()            


        except:
            print 'Failed to create new Meters.'
        else:
            print 'Created new Meters.'


