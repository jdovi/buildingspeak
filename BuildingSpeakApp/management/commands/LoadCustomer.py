from django.core.management.base import BaseCommand

import urllib
from pytz import UTC
from decimal import Decimal
from datetime import datetime

from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import User
from django.db.models import Max, Min, Q, Sum

from BuildingSpeak.settings import STATIC_URL

from BuildingSpeakApp.models import UserProfile, Account, Building, Space, Meter, Equipment
from BuildingSpeakApp.models import PackageUnit
from BuildingSpeakApp.models import MeterConsumptionModel, MeterPeakDemandModel
from BuildingSpeakApp.models import SpaceMeterApportionment, BuildingMeterApportionment
from BuildingSpeakApp.models import EfficiencyMeasure, EMMeterApportionment, EMEquipmentApportionment
from BuildingSpeakApp.models import WeatherStation, Utility
from BuildingSpeakApp.models import GAPowerPandL, InfiniteEnergyGAGas, CityOfATLWWW


class Command(BaseCommand):

    def handle(self, *args, **options):

#    ###---Users
#        try:
#            userJD = User.objects.get(username = 'jdovi')       #loaded to add to all new accounts
#            userDA = User.objects.get(username = 'dashley')     #loaded to add to all new accounts
#            
#            user1 = User(
#                username = 'smucker',
#                password = 'lastlostleast',
#                first_name = 'Steve',
#                last_name = 'Smucker',
#                email = 'smucker@cityofrefugeatl.org',
#                is_active = True,
#                is_staff = False,
#                is_superuser = False,
#                )
#            user1.save()
#        except:
#            print 'Failed to create new Users.'
#        
#    ###---UserProfiles
#        try:
#            userprofile1 = UserProfile(
#                user = user1,
#                organization = 'Town of Refuge, Inc. - ATL'
#                )
#            userprofile1.save()
#            #post-creation actions
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/UserImages/default_user_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            userprofile1.__setattr__('image_file', file_obj)
#            userprofile1.save()
#        except:
#            print 'Failed to create new UserProfiles.'
#        
#    ###---Account
#        try:
#            acct1 = Account(
#                name = 'Town of Refuge, Inc. - ATL',
#                account_type = 'Commercial',
#                street_address = '1300 Joseph Boone Blvd',
#                city = 'Atlanta',
#                state = 'GA',
#                zip_code = '30314',
#                launch_date = timezone.now(),
#                first_name = 'Steve',
#                last_name = 'Smucker',
#                title = 'Director of Maintenance',
#                email = 'smucker@cityofrefugeatl.org',
#                phone = '404-713-6994',
#                status = 'Active',
#                monthly_payment = Decimal(0.0),
#                )
#            acct1.save()
#            
#            #post-creation actions
#            #--attach users
#            acct1.users.add(User.objects.get(username = 'smucker'))
#            acct1.users.add(userJD)
#            acct1.users.add(userDA)
#            
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/AccountImage_CityOfRefuge.gif'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            acct1.__setattr__('image_file', file_obj)
#            acct1.save()
#        except:
#            print 'Failed to create new Accounts.'
#        
#    ###---Buildings
#        try:
#            ws = WeatherStation.objects.get(name = 'ATL - downtown west')
#            
#            East = Building(
#                name = 'East Bldg',
#                building_type = 'Multi-Purpose',
#                EIA_type = 'Other',
#                ESPM_type = 'Other',
#                account = acct1,
#                weather_station = ws,
#                street_address = '1300 Joseph Boone Blvd',
#                city = 'Atlanta',
#                state = 'GA',
#                zip_code = '30314',
#                age = 2004,
#                square_footage = 49800,
#                stories = 1,
#                max_occupancy = None,
#                first_name = 'Steve',
#                last_name = 'Smucker',
#                title = 'Director of Maintenance',
#                email = 'smucker@cityofrefugeatl.org',
#                phone = '404-713-6994',
#                )
#            East.save()
#    
#            #post-creation actions
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/BuildingImages/BuildingImage_EastBldg.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            East.__setattr__('image_file', file_obj)
#            East.save()
#            
#            West = Building(
#                name = 'West Bldg',
#                building_type = 'Multi-Purpose',
#                EIA_type = 'Other',
#                ESPM_type = 'Other',
#                account = acct1,
#                weather_station = ws,
#                street_address = '1300 Joseph Boone Blvd',
#                city = 'Atlanta',
#                state = 'GA',
#                zip_code = '30314',
#                age = 2004,
#                square_footage = 152000,
#                stories = 1,
#                max_occupancy = None,
#                first_name = 'Steve',
#                last_name = 'Smucker',
#                title = 'Director of Maintenance',
#                email = 'smucker@cityofrefugeatl.org',
#                phone = '404-713-6994',
#                )
#            West.save()
#            
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/BuildingImages/BuildingImage_WestBldg.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            West.__setattr__('image_file', file_obj)
#            West.save()
#        except:
#            print 'Failed to create new Buildings.'
#        
#    ###---Spaces
#        try:
#            EdenI_space = Space(
#                name = 'Eden I',
#                building = West,
#                square_footage = 36000,
#                max_occupancy = None,
#                space_type = 'Dormitory',
#                EIA_type = 'Lodging',
#                ESPM_type = 'Dormitory / Residence Hall',
#                )
#            EdenI_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            EdenI_space.__setattr__('image_file', file_obj)
#            EdenI_space.save()
#            
#            kitchen_space = Space(
#                name = '180 Kitchen',
#                building = East,
#                square_footage = 4500,
#                max_occupancy = None,
#                space_type = 'Dining: Family',
#                EIA_type = 'Food Service',
#                ESPM_type = 'Other',
#                )
#            kitchen_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kitchen_space.__setattr__('image_file', file_obj)
#            kitchen_space.save()
#            
#            dining_space = Space(
#                name = 'Dining Area',
#                building = East,
#                square_footage = 11500,
#                max_occupancy = None,
#                space_type = 'Dining: Family',
#                EIA_type = 'Food Service',
#                ESPM_type = 'Other',
#                )
#            dining_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            dining_space.__setattr__('image_file', file_obj)
#            dining_space.save()
#            
#            compATL_space = Space(
#                name = 'Compassion ATL',
#                building = West,
#                square_footage = 36000,
#                max_occupancy = None,
#                space_type = 'Warehouse',
#                EIA_type = 'Warehouse and Storage',
#                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
#                )
#            compATL_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/SpaceImage_compATL.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            compATL_space.__setattr__('image_file', file_obj)
#            compATL_space.save()
#            
#            EdenII_space = Space(
#                name = 'Eden II',
#                building = East,
#                square_footage = 9700,
#                max_occupancy = None,
#                space_type = 'Dormitory',
#                EIA_type = 'Lodging',
#                ESPM_type = 'Dormitory / Residence Hall',
#                )
#            EdenII_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            EdenII_space.__setattr__('image_file', file_obj)
#            EdenII_space.save()
#            
#            dorms_space = Space(
#                name = 'Dorms',
#                building = East,
#                square_footage = 11000,
#                max_occupancy = None,
#                space_type = 'Dormitory',
#                EIA_type = 'Lodging',
#                ESPM_type = 'Dormitory / Residence Hall',
#                )
#            dorms_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            dorms_space.__setattr__('image_file', file_obj)
#            dorms_space.save()
#            
#            gym_space = Space(
#                name = 'Gym',
#                building = East,
#                square_footage = 8700,
#                max_occupancy = None,
#                space_type = 'Gymnasium',
#                EIA_type = 'Education',
#                ESPM_type = 'K-12 School',
#                )
#            gym_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/SpaceImage_gym.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gym_space.__setattr__('image_file', file_obj)
#            gym_space.save()
#            
#            clinic_space = Space(
#                name = 'Clinic',
#                building = West,
#                square_footage = 8700,
#                max_occupancy = None,
#                space_type = 'Health Care Clinic',
#                EIA_type = 'Health Care - Outpatient',
#                ESPM_type = 'Medical Office',
#                )
#            clinic_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            clinic_space.__setattr__('image_file', file_obj)
#            clinic_space.save()
#            
#            offices_space = Space(
#                name = 'Offices',
#                building = West,
#                square_footage = 10400,
#                max_occupancy = None,
#                space_type = 'Office',
#                EIA_type = 'Office',
#                ESPM_type = 'Office',
#                )
#            offices_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            offices_space.__setattr__('image_file', file_obj)
#            offices_space.save()
#            
#            playground_space = Space(
#                name = 'Playground',
#                building = West,
#                square_footage = 4800,
#                max_occupancy = None,
#                space_type = 'Gymnasium',
#                EIA_type = 'Education',
#                ESPM_type = 'K-12 School',
#                )
#            playground_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            playground_space.__setattr__('image_file', file_obj)
#            playground_space.save()
#            
#            school_space = Space(
#                name = 'CORE',
#                building = East,
#                square_footage = 4400,
#                max_occupancy = None,
#                space_type = 'School/University',
#                EIA_type = 'Education',
#                ESPM_type = 'K-12 School',
#                )
#            school_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/SpaceImage_school.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            school_space.__setattr__('image_file', file_obj)
#            school_space.save()
#            
#            unfinished_space = Space(
#                name = 'Unfinished',
#                building = West,
#                square_footage = 44100,
#                max_occupancy = None,
#                space_type = 'Warehouse',
#                EIA_type = 'Warehouse and Storage',
#                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
#                )
#            unfinished_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            unfinished_space.__setattr__('image_file', file_obj)
#            unfinished_space.save()
#            
#            newschool_space = Space(
#                name = 'Bright Futures',
#                building = West,
#                square_footage = 7000,
#                max_occupancy = None,
#                space_type = 'School/University',
#                EIA_type = 'Education',
#                ESPM_type = 'K-12 School',
#                )
#            newschool_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            newschool_space.__setattr__('image_file', file_obj)
#            newschool_space.save()
#            
#            newchurch_space = Space(
#                name = 'Church',
#                building = West,
#                square_footage = 5000,
#                max_occupancy = None,
#                space_type = 'Religious Building',
#                EIA_type = 'Religious Worship',
#                ESPM_type = 'House of Worship',
#                )
#            newchurch_space.save()
#            #post-creation actions:
#            #--load image file
#            file_url = STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            newchurch_space.__setattr__('image_file', file_obj)
#            newchurch_space.save()
#        except:
#            print 'Failed to create new Spaces.'        
#        
#    ###---Meters
#        try:
#            gpc = Utility.objects.get(name = 'Georgia Power Company')
#            infe = Utility.objects.get(name = 'Infinite Energy')
#            atlw = Utility.objects.get(name = 'City of Atlanta, Dept. of Watershed Mgmt.')
#            
#            atlwww = CityOfATLWWW.objects.get(name = 'Water and Wastewater 2012')
#            infebizgas = InfiniteEnergyGAGas.objects.get(name = 'Fixed Business Rate')
#            gpc_pls8_sec_in = GAPowerPandL.objects.get(name = 'GPC-PLS-8-secondary-inside')
#            gpc_plm8_sec_in = GAPowerPandL.objects.get(name = 'GPC-PLM-8-secondary-inside')
#            #gpc_gs7 = GAPowerGS.objects.get(name = 'GPC-GS-7') #####NEED TO MAKE
#            #gpc_toueo7 = GAPowerTOU.objects.get(name = 'GPC-TOU-EO-7') #####NEED TO MAKE
#            #gpc_tougsd7 = GAPowerTOU.objects.get(name = 'GPC-TOU-GSD-7') #####NEED TO MAKE
#            
#            east_main = Meter(
#                name = 'East Bldg (electric)',
#                utility_type = 'electricity',
#                location = 'loading dock area of bldg',
#                serves = 'all of East Bldg except Eden II',
#                units = 'kW,kWh',
#                weather_station = ws,
#                utility = gpc,
##                rate_schedule = gpc_toueo7,
#                rate_schedule = gpc_plm8_sec_in,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '6126898026',
#                utility_meter_number = '3081617',
#                )
#            east_main.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EastMain.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            east_main.__setattr__('image_file', file_obj)
#            east_main.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EastMain.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            east_main.__setattr__('nameplate_file', file_obj)
#            east_main.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            east_main.__setattr__('bill_data_file', file_obj)
#            east_main.save()
#            east_main.upload_bill_data(create_models_if_nonexistent=True)
#            east_main.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = east_main,
#                                              building = East,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = east_main,
#                                           space = kitchen_space,
#                                           assigned_fraction = Decimal(0.3))
#            sma1.save()
#            sma2 = SpaceMeterApportionment(meter = east_main,
#                                           space = dining_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma2.save()
#            sma3 = SpaceMeterApportionment(meter = east_main,
#                                           space = dorms_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma3.save()
#            sma4 = SpaceMeterApportionment(meter = east_main,
#                                           space = gym_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma4.save()
#            sma5 = SpaceMeterApportionment(meter = east_main,
#                                           space = school_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma5.save()
#    
#            
#            e1 = Meter(
#                name = 'Eden I (electric)',
#                utility_type = 'electricity',
#                location = 'northwest corner of West Bldg',
#                serves = 'Eden I',
#                units = 'kW,kWh',
#                weather_station = ws,
#                utility = gpc,
#                rate_schedule = gpc_plm8_sec_in,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '0437031108',
#                utility_meter_number = '3081619',
#                )
#            e1.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EdenI.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            e1.__setattr__('image_file', file_obj)
#            e1.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EdenI.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            e1.__setattr__('nameplate_file', file_obj)
#            e1.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            e1.__setattr__('bill_data_file', file_obj)
#            e1.save()
#            e1.upload_bill_data(create_models_if_nonexistent = True)
#            e1.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = e1,
#                                              building = West,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = e1,
#                                           space = EdenI_space,
#                                           assigned_fraction = Decimal(1.0))
#            sma1.save()
#            
#            
#            e2 = Meter(
#                name = 'Eden II (electric)',
#                utility_type = 'electricity',
#                location = 'northwest corner of East Bldg',
#                serves = 'Eden II',
#                units = 'kW,kWh',
#                weather_station = ws,
#                utility = gpc,
#                rate_schedule = gpc_plm8_sec_in,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '3244865006',
#                utility_meter_number = '3179180',
#                )
#            e2.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EdenII.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            e2.__setattr__('image_file', file_obj)
#            e2.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EdenII.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            e2.__setattr__('nameplate_file', file_obj)
#            e2.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            e2.__setattr__('bill_data_file', file_obj)
#            e2.save()
#            e2.upload_bill_data(create_models_if_nonexistent = True)
#            e2.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = e2,
#                                              building = East,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = e2,
#                                           space = EdenII_space,
#                                           assigned_fraction = Decimal(1.0))
#            sma1.save()
#            
#            wh = Meter(
#                name = 'West Bldg south (electric)',
#                utility_type = 'electricity',
#                location = 'just south of Offices entrance on West Bldg',
#                serves = 'Offices and Compassion ATL',
#                units = 'kW,kWh',
#                weather_station = ws,
#                utility = gpc,
##                rate_schedule = gpc_toueo7,
#                rate_schedule = gpc_plm8_sec_in,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '6168898017',
#                utility_meter_number = '3081618',
#                )
#            wh.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Warehouse.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            wh.__setattr__('image_file', file_obj)
#            wh.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Warehouse.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            wh.__setattr__('nameplate_file', file_obj)
#            wh.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            wh.__setattr__('bill_data_file', file_obj)
#            wh.save()
#            wh.upload_bill_data(create_models_if_nonexistent = True)
#            wh.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = wh,
#                                              building = West,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = wh,
#                                           space = compATL_space,
#                                           assigned_fraction = Decimal(0.3))
#            sma1.save()
#            sma2 = SpaceMeterApportionment(meter = wh,
#                                           space = unfinished_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma2.save()
#            sma3 = SpaceMeterApportionment(meter = wh,
#                                           space = offices_space,
#                                           assigned_fraction = Decimal(0.5))
#            sma3.save()
#            
#            newschool = Meter(
#                name = 'New School (electric)',
#                utility_type = 'electricity',
#                location = 'south of Eden I entrance on West Bldg',
#                serves = 'Playground and unfinished area between Eden I and Clinic',
#                units = 'kW,kWh',
#                weather_station = ws,
#                utility = gpc,
##                rate_schedule = gpc_gs7,
#                rate_schedule = gpc_plm8_sec_in,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '6147898017',
#                utility_meter_number = '3081616',
#                )
#            newschool.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_NewSchool.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            newschool.__setattr__('image_file', file_obj)
#            newschool.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_NewSchool.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            newschool.__setattr__('nameplate_file', file_obj)
#            newschool.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            newschool.__setattr__('bill_data_file', file_obj)
#            newschool.save()
#            newschool.upload_bill_data(create_models_if_nonexistent = True)
#            newschool.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = newschool,
#                                              building = West,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = newschool,
#                                           space = playground_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma1.save()
#            sma2 = SpaceMeterApportionment(meter = newschool,
#                                           space = newschool_space,
#                                           assigned_fraction = Decimal(0.7))
#            sma2.save()
#            sma3 = SpaceMeterApportionment(meter = newschool,
#                                           space = newchurch_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma3.save()
#            
#            clinic = Meter(
#                name = 'Clinic (electric)',
#                utility_type = 'electricity',
#                location = 'north of covered Clinic entrance on West Bldg',
#                serves = 'Clinic',
#                units = 'kW,kWh',
#                weather_station = ws,
#                utility = gpc,
#                rate_schedule = gpc_pls8_sec_in,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '1816415005',
#                utility_meter_number = '3046324',
#                )
#            clinic.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Clinic.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            clinic.__setattr__('image_file', file_obj)
#            clinic.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Clinic.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            clinic.__setattr__('nameplate_file', file_obj)
#            clinic.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            clinic.__setattr__('bill_data_file', file_obj)
#            clinic.save()
#            clinic.upload_bill_data(create_models_if_nonexistent = True)
#            clinic.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = clinic,
#                                              building = West,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = clinic,
#                                           space = clinic_space,
#                                           assigned_fraction = Decimal(1.0))
#            sma1.save()
#            
#            gas1290 = Meter(
#                name = 'East Bldg (natural gas)',
#                utility_type = 'natural gas',
#                location = 'unknown',
#                serves = 'East Bldg heating and domestic hot water',
#                units = 'therms/h,therms',
#                weather_station = ws,
#                utility = infe,
#                rate_schedule = infebizgas,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '9401260170',
#                utility_meter_number = '000537796',
#                )
#            gas1290.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EastGas.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gas1290.__setattr__('image_file', file_obj)
#            gas1290.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EastGas.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gas1290.__setattr__('nameplate_file', file_obj)
#            gas1290.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gas1290.__setattr__('bill_data_file', file_obj)
#            gas1290.save()
#            gas1290.upload_bill_data(create_models_if_nonexistent = True)
#            gas1290.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = gas1290,
#                                              building = East,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = gas1290,
#                                           space = dorms_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma1.save()
#            sma2 = SpaceMeterApportionment(meter = gas1290,
#                                           space = kitchen_space,
#                                           assigned_fraction = Decimal(0.4))
#            sma2.save()
#            sma3 = SpaceMeterApportionment(meter = gas1290,
#                                           space = dining_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma3.save()
#            sma4 = SpaceMeterApportionment(meter = gas1290,
#                                           space = gym_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma4.save()
#            sma5 = SpaceMeterApportionment(meter = gas1290,
#                                           space = school_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma5.save()
#            sma6 = SpaceMeterApportionment(meter = gas1290,
#                                           space = EdenII_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma6.save()
#            
#            gas1300 = Meter(
#                name = 'West Bldg (natural gas)',
#                utility_type = 'natural gas',
#                location = 'unknown',
#                serves = 'West Bldg heating and domestic hot water',
#                units = 'therms/h,therms',
#                weather_station = ws,
#                utility = infe,
#                rate_schedule = infebizgas,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '8783526395',
#                utility_meter_number = '003008386',
#                )
#            gas1300.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_WestGas.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gas1300.__setattr__('image_file', file_obj)
#            gas1300.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_WestGas.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gas1300.__setattr__('nameplate_file', file_obj)
#            gas1300.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gas1300.__setattr__('bill_data_file', file_obj)
#            gas1300.save()
#            gas1300.upload_bill_data(create_models_if_nonexistent = True)
#            gas1300.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = gas1300,
#                                              building = West,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = gas1300,
#                                           space = playground_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma1.save()
#            sma2 = SpaceMeterApportionment(meter = gas1300,
#                                           space = newschool_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma2.save()
#            sma3 = SpaceMeterApportionment(meter = gas1300,
#                                           space = newchurch_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma3.save()
#            sma4 = SpaceMeterApportionment(meter = gas1300,
#                                           space = EdenI_space,
#                                           assigned_fraction = Decimal(0.3))
#            sma4.save()
#            sma5 = SpaceMeterApportionment(meter = gas1300,
#                                           space = clinic_space,
#                                           assigned_fraction = Decimal(0.15))
#            sma5.save()
#            sma6 = SpaceMeterApportionment(meter = gas1300,
#                                           space = offices_space,
#                                           assigned_fraction = Decimal(0.15))
#            sma6.save()
#            
#            simpson1290 = Meter(
#                name = '1290 Simpson (water)',
#                utility_type = 'domestic water',
#                location = 'unknown',
#                serves = 'unknown',
#                units = 'gpm,gal',
#                weather_station = ws,
#                utility = atlw,
#                rate_schedule = atlwww,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '11-2487.301',
#                utility_meter_number = 'NE51964675',
#                )
#            simpson1290.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Simpson1290.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            simpson1290.__setattr__('image_file', file_obj)
#            simpson1290.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Simpson1290.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            simpson1290.__setattr__('nameplate_file', file_obj)
#            simpson1290.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            simpson1290.__setattr__('bill_data_file', file_obj)
#            simpson1290.save()
#            simpson1290.upload_bill_data(create_models_if_nonexistent = True)
#            simpson1290.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = simpson1290,
#                                              building = East,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = simpson1290,
#                                           space = kitchen_space,
#                                           assigned_fraction = Decimal(0.7))
#            sma1.save()
#            sma2 = SpaceMeterApportionment(meter = simpson1290,
#                                           space = EdenII_space,
#                                           assigned_fraction = Decimal(0.3))
#            sma2.save()
#            
#            boone1300 = Meter(
#                name = '1300 Boone (water)',
#                utility_type = 'domestic water',
#                location = 'unknown',
#                serves = 'unknown',
#                units = 'gpm,gal',
#                weather_station = ws,
#                utility = atlw,
#                rate_schedule = atlwww,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '12-9779.302',
#                utility_meter_number = 'NE049764661',
#                )
#            boone1300.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Boone1300.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            boone1300.__setattr__('image_file', file_obj)
#            boone1300.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Boone1300.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            boone1300.__setattr__('nameplate_file', file_obj)
#            boone1300.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            boone1300.__setattr__('bill_data_file', file_obj)
#            boone1300.save()
#            boone1300.upload_bill_data(create_models_if_nonexistent = True)
#            boone1300.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = boone1300,
#                                              building = West,
#                                              assigned_fraction = Decimal(1.0))
#            bma1.save()
#            #--connect to spaces
#            sma1 = SpaceMeterApportionment(meter = simpson1290,
#                                           space = EdenI_space,
#                                           assigned_fraction = Decimal(0.5))
#            sma1.save()
#            sma2 = SpaceMeterApportionment(meter = simpson1290,
#                                           space = clinic_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma2.save()
#            sma3 = SpaceMeterApportionment(meter = simpson1290,
#                                           space = newschool_space,
#                                           assigned_fraction = Decimal(0.2))
#            sma3.save()
#            sma4 = SpaceMeterApportionment(meter = simpson1290,
#                                           space = offices_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma4.save()
#            sma5 = SpaceMeterApportionment(meter = simpson1290,
#                                           space = compATL_space,
#                                           assigned_fraction = Decimal(0.1))
#            sma5.save()
#
#            simpson1300 = Meter(
#                name = '1300 Simpson (water)',
#                utility_type = 'domestic water',
#                location = 'unknown',
#                serves = 'fire service',
#                units = 'gpm,gal',
#                weather_station = ws,
#                utility = atlw,
#                rate_schedule = atlwww,
#                account = acct1,
#                make = 'unknown',
#                model = 'unknown',
#                serial_number = 'unknown',
#                utility_account_number = '0155559301',
#                utility_meter_number = 'unknown',
#                )
#            simpson1300.save()
#            #post-creation actions:
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Simpson1300.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            simpson1300.__setattr__('image_file', file_obj)
#            simpson1300.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Simpson1300.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            simpson1300.__setattr__('nameplate_file', file_obj)
#            simpson1300.save()
#            #--load bill data file, possibly create meter models
#            file_url = STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            simpson1300.__setattr__('bill_data_file', file_obj)
#            simpson1300.save()
#            simpson1300.upload_bill_data(create_models_if_nonexistent = True)
#            simpson1300.save()
#            #--connect to buildings
#            bma1 = BuildingMeterApportionment(meter = simpson1300,
#                                              building = East,
#                                              assigned_fraction = Decimal(0.5))
#            bma1.save()
#            bma2 = BuildingMeterApportionment(meter = simpson1300,
#                                              building = West,
#                                              assigned_fraction = Decimal(0.5))
#            bma2.save()
#
#        except:
#            print 'Failed to create new Meters.'
#
#    ###---Equipment
#        try:
#            off01 = PackageUnit(name = 'OFF-01',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'Bankhead',
#                                age = None,
#                                make = 'Trane',
#                                model = 'YCD048C3L0BA',
#                                serial_number = 'J161427170',
#                                nameplate_tons = 4.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 90.0,
#                                nameplate_MBH_out = 72.9,
#                                nameplate_ng_eta = 0.81,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 14.8,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 4.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 2.1,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            off01.save()
#            #post-creation actions:
#            #--connect to buildings
#            off01.buildings.add(West)
#            #--connect to spaces
#            off01.spaces.add(offices_space)
#            #--connect to meters
#            off01.meters.add(wh)        #electric
#            off01.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-01-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off01.__setattr__('image_file', file_obj)
#            off01.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-01-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off01.__setattr__('nameplate_file', file_obj)
#            off01.save()
#
#            off02 = PackageUnit(name = 'OFF-02',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'Kim, foyer/hall/Simpson/bathrooms',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'GCS16-1353-270-7Y',
#                                serial_number = '5692C00479',
#                                nameplate_tons = 10.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 270.0,
#                                nameplate_MBH_out = 216.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 17.3,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 10.6,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 2.1,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            off02.save()
#            #post-creation actions:
#            #--connect to buildings
#            off02.buildings.add(West)
#            #--connect to spaces
#            off02.spaces.add(offices_space)
#            #--connect to meters
#            off02.meters.add(wh)        #electric
#            off02.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-02-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off02.__setattr__('image_file', file_obj)
#            off02.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-02-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off02.__setattr__('nameplate_file', file_obj)
#            off02.save()
#
#            off03 = PackageUnit(name = 'OFF-03',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'Kids Cave',
#                                age = None,
#                                make = 'Payne',
#                                model = '588ANW030080ACAD',
#                                serial_number = '2196G10899',
#                                nameplate_tons = 2.5,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 80.0,
#                                nameplate_MBH_out = 64.8,
#                                nameplate_ng_eta = 0.81,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 1,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 14.4,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 2.0,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            off03.save()
#            #post-creation actions:
#            #--connect to buildings
#            off03.buildings.add(West)
#            #--connect to spaces
#            off03.spaces.add(offices_space)
#            #--connect to meters
#            off03.meters.add(wh)        #electric
#            off03.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-03-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off03.__setattr__('image_file', file_obj)
#            off03.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-03-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off03.__setattr__('nameplate_file', file_obj)
#            off03.save()
#
#            off04 = PackageUnit(name = 'OFF-04',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'offices behind R.C./hall',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'HP29-036-1Y',
#                                serial_number = '5899A 15307',
#                                nameplate_tons = 3.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 11.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.1,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            off04.save()
#            #post-creation actions:
#            #--connect to buildings
#            off04.buildings.add(West)
#            #--connect to spaces
#            off04.spaces.add(offices_space)
#            #--connect to meters
#            off04.meters.add(wh)       #electric
#            off04.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-04-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off04.__setattr__('image_file', file_obj)
#            off04.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-04-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off04.__setattr__('nameplate_file', file_obj)
#            off04.save()
#
#            off05 = PackageUnit(name = 'OFF-05',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'Bruce/conference room/Seth/Resource Center',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511--',
#                                serial_number = '1704G10322',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            off05.save()
#            #post-creation actions:
#            #--connect to buildings
#            off05.buildings.add(West)
#            #--connect to spaces
#            off05.spaces.add(offices_space)
#            #--connect to meters
#            off05.meters.add(wh)       #electric
#            off05.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-05-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off05.__setattr__('image_file', file_obj)
#            off05.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-05-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off05.__setattr__('nameplate_file', file_obj)
#            off05.save()
#
#            off06 = PackageUnit(name = 'OFF-06',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'Pharmacy',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'KGA048S4DH1G',
#                                serial_number = '5610M05717',
#                                nameplate_tons = 4.0,
#                                nameplate_EER = 11.0,
#                                nameplate_MBH_in = 150.0,
#                                nameplate_MBH_out = 120.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 6.2,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 2.0,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.1,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            off06.save()
#            #post-creation actions:
#            #--connect to buildings
#            off06.buildings.add(West)
#            #--connect to spaces
#            off06.spaces.add(offices_space)
#            #--connect to meters
#            off05.meters.add(wh)       #electric
#            off06.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-06-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off06.__setattr__('image_file', file_obj)
#            off06.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-06-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            off06.__setattr__('nameplate_file', file_obj)
#            off06.save()
#
#            cli01 = PackageUnit(name = 'CLI-01',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'back hall exam rooms',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'KGA036S4DM1G',
#                                serial_number = '5610J08145',
#                                nameplate_tons = 3.0,
#                                nameplate_EER = 10.7,
#                                nameplate_MBH_in = 105.0,
#                                nameplate_MBH_out = 84.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 5.8,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 2.0,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.1,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            cli01.save()
#            #post-creation actions:
#            #--connect to buildings
#            cli01.buildings.add(West)
#            #--connect to spaces
#            cli01.spaces.add(clinic_space)
#            #--connect to meters
#            cli01.meters.add(clinic)    #electric
#            cli01.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-01-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli01.__setattr__('image_file', file_obj)
#            cli01.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-01-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli01.__setattr__('nameplate_file', file_obj)
#            cli01.save()
#
#            cli02 = PackageUnit(name = 'CLI-02',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'left hall/dental/reception',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'KGA048S4DH1G',
#                                serial_number = '5610M05716',
#                                nameplate_tons = 4.0,
#                                nameplate_EER = 11.0,
#                                nameplate_MBH_in = 150.0,
#                                nameplate_MBH_out = 120.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 6.2,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 2.0,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.1,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            cli02.save()
#            #post-creation actions:
#            #--connect to buildings
#            cli02.buildings.add(West)
#            #--connect to spaces
#            cli02.spaces.add(clinic_space)
#            #--connect to meters
#            cli02.meters.add(clinic)    #electric
#            cli02.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-02-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli02.__setattr__('image_file', file_obj)
#            cli02.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-02-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli02.__setattr__('nameplate_file', file_obj)
#            cli02.save()
#
#            cli03 = PackageUnit(name = 'CLI-03',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'waiting area/front bathroom',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'KGA060S4DH2G',
#                                serial_number = '5610G15564',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = 11.2,
#                                nameplate_MBH_in = 150.0,
#                                nameplate_MBH_out = 120.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 8.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 2.5,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.3,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            cli03.save()
#            #post-creation actions:
#            #--connect to buildings
#            cli03.buildings.add(West)
#            #--connect to spaces
#            cli03.spaces.add(clinic_space)
#            #--connect to meters
#            cli03.meters.add(clinic)    #electric
#            cli03.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-03-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli03.__setattr__('image_file', file_obj)
#            cli03.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-03-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli03.__setattr__('nameplate_file', file_obj)
#            cli03.save()
#
#            cli04 = PackageUnit(name = 'CLI-04',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'conference room/counseling room',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'KGA048S4DH1G',
#                                serial_number = '5610F07737',
#                                nameplate_tons = 4.0,
#                                nameplate_EER = 11.0,
#                                nameplate_MBH_in = 150.0,
#                                nameplate_MBH_out = 120.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 6.2,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 2.0,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.1,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            cli04.save()
#            #post-creation actions:
#            #--connect to buildings
#            cli04.buildings.add(West)
#            #--connect to spaces
#            cli04.spaces.add(clinic_space)
#            #--connect to meters
#            cli04.meters.add(clinic)    #electric
#            cli04.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-04-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli04.__setattr__('image_file', file_obj)
#            cli04.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-04-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli04.__setattr__('nameplate_file', file_obj)
#            cli04.save()
#
#            cli05 = PackageUnit(name = 'CLI-05',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'offices/back bathrooms/break room',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'KGA060S4DH2G',
#                                serial_number = '5610G05233',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = 11.2,
#                                nameplate_MBH_in = 150.0,
#                                nameplate_MBH_out = 120.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 8.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 2.5,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.3,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            cli05.save()
#            #post-creation actions:
#            #--connect to buildings
#            cli05.buildings.add(West)
#            #--connect to spaces
#            cli05.spaces.add(clinic_space)
#            #--connect to meters
#            cli05.meters.add(clinic)    #electric
#            cli05.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-05-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli05.__setattr__('image_file', file_obj)
#            cli05.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-05-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            cli05.__setattr__('nameplate_file', file_obj)
#            cli05.save()
#
#            ev101 = PackageUnit(name = 'EV1-01',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'left offices/hall',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'TGA150S2BM1G',
#                                serial_number = '5608G15333',
#                                nameplate_tons = 11.5,
#                                nameplate_EER = 9.5,
#                                nameplate_MBH_in = 180.0,
#                                nameplate_MBH_out = 144.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 9.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 7.6,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev101.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev101.buildings.add(West)
#            #--connect to spaces
#            ev101.spaces.add(EdenI_space)
#            #--connect to meters
#            ev101.meters.add(e1)        #electric
#            ev101.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-01-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev101.__setattr__('image_file', file_obj)
#            ev101.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-01-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev101.__setattr__('nameplate_file', file_obj)
#            ev101.save()
#
#            ev102 = PackageUnit(name = 'EV1-02',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'back left hall/dorms',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'TGA150S2BM1G',
#                                serial_number = '5608G05219',
#                                nameplate_tons = 11.5,
#                                nameplate_EER = 9.5,
#                                nameplate_MBH_in = 180.0,
#                                nameplate_MBH_out = 144.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 9.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 7.6,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev102.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev102.buildings.add(West)
#            #--connect to spaces
#            ev102.spaces.add(EdenI_space)
#            #--connect to meters
#            ev102.meters.add(e1)        #electric
#            ev102.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-02-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev102.__setattr__('image_file', file_obj)
#            ev102.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-02-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev102.__setattr__('nameplate_file', file_obj)
#            ev102.save()
#
#            ev103 = PackageUnit(name = 'EV1-03',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'common area/FML',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'TGA090S2BM1G',
#                                serial_number = '5608F06581',
#                                nameplate_tons = 7.5,
#                                nameplate_EER = 10.1,
#                                nameplate_MBH_in = 180.0,
#                                nameplate_MBH_out = 144.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 6.4,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 3.4,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.3,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev103.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev103.buildings.add(West)
#            #--connect to spaces
#            ev103.spaces.add(EdenI_space)
#            #--connect to meters
#            ev103.meters.add(e1)        #electric
#            ev103.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-03-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev103.__setattr__('image_file', file_obj)
#            ev103.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-03-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev103.__setattr__('nameplate_file', file_obj)
#            ev103.save()
#
#            ev104 = PackageUnit(name = 'EV1-04',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'back right hall',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'TGA102S2BM1G',
#                                serial_number = '5607M01370',
#                                nameplate_tons = 8.3,
#                                nameplate_EER = 10.1,
#                                nameplate_MBH_in = 180.0,
#                                nameplate_MBH_out = 144.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 7.1,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 3.4,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.3,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev104.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev104.buildings.add(West)
#            #--connect to spaces
#            ev104.spaces.add(EdenI_space)
#            #--connect to meters
#            ev104.meters.add(e1)        #electric
#            ev104.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-04-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev104.__setattr__('image_file', file_obj)
#            ev104.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-04-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev104.__setattr__('nameplate_file', file_obj)
#            ev104.save()
#
#            ev105 = PackageUnit(name = 'EV1-05',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'right hall',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'TGA150S2BM1G',
#                                serial_number = '5608H01253',
#                                nameplate_tons = 11.5,
#                                nameplate_EER = 9.5,
#                                nameplate_MBH_in = 180.0,
#                                nameplate_MBH_out = 144.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 9.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 7.6,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev105.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev105.buildings.add(West)
#            #--connect to spaces
#            ev105.spaces.add(EdenI_space)
#            #--connect to meters
#            ev105.meters.add(e1)        #electric
#            ev105.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-05-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev105.__setattr__('image_file', file_obj)
#            ev105.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-05-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev105.__setattr__('nameplate_file', file_obj)
#            ev105.save()
#
#            ev106 = PackageUnit(name = 'EV1-06',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'common area',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'TGA090S2BM1G',
#                                serial_number = '5608811495',
#                                nameplate_tons = 7.5,
#                                nameplate_EER = 10.1,
#                                nameplate_MBH_in = 180.0,
#                                nameplate_MBH_out = 144.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 6.4,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 3.4,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.3,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev106.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev106.buildings.add(West)
#            #--connect to spaces
#            ev106.spaces.add(EdenI_space)
#            #--connect to meters
#            ev106.meters.add(e1)        #electric
#            ev106.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-06-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev106.__setattr__('image_file', file_obj)
#            ev106.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-06-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev106.__setattr__('nameplate_file', file_obj)
#            ev106.save()
#
#            ev107 = PackageUnit(name = 'EV1-07',
#                                equipment_type = 'Package Unit',
#                                location = 'West Bldg rooftop',
#                                description = '',
#                                serves = 'Fulton County offices',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TMD008-A-501',
#                                serial_number = '2004G20670',
#                                nameplate_tons = 7.5,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 125.0,
#                                nameplate_MBH_out = 100.0,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 14.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.8,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 2,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev107.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev107.buildings.add(West)
#            #--connect to spaces
#            ev107.spaces.add(EdenI_space)
#            #--connect to meters
#            ev107.meters.add(e1)        #electric
#            ev107.meters.add(gas1300)   #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-07-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev107.__setattr__('image_file', file_obj)
#            ev107.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-07-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev107.__setattr__('nameplate_file', file_obj)
#            ev107.save()
#
#            ev201 = PackageUnit(name = 'EV2-01',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'Room 3',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'THA048S2BN1G',
#                                serial_number = '5609B01178',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = None,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = None,
#                                nameplate_f1_PH = None,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev201.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev201.buildings.add(East)
#            #--connect to spaces
#            ev201.spaces.add(EdenII_space)
#            #--connect to meters
#            ev201.meters.add(e2)            #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-01-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev201.__setattr__('image_file', file_obj)
#            ev201.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-01-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev201.__setattr__('nameplate_file', file_obj)
#            ev201.save()
#
#            ev202 = PackageUnit(name = 'EV2-02',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'Room 4',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'THA036S2BN1G',
#                                serial_number = '5609B04467',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = None,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = None,
#                                nameplate_f1_PH = None,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev202.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev202.buildings.add(East)
#            #--connect to spaces
#            ev202.spaces.add(EdenII_space)
#            #--connect to meters
#            ev202.meters.add(e2)            #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-02-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev202.__setattr__('image_file', file_obj)
#            ev202.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-02-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev202.__setattr__('nameplate_file', file_obj)
#            ev202.save()
#
#            ev203 = PackageUnit(name = 'EV2-03',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'Common Area',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'THA036S2BN1G',
#                                serial_number = '5609C09237',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 480.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 4.5,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = None,
#                                nameplate_f1_PH = None,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev203.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev203.buildings.add(East)
#            #--connect to spaces
#            ev203.spaces.add(EdenII_space)
#            #--connect to meters
#            ev203.meters.add(e2)            #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-03-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev203.__setattr__('image_file', file_obj)
#            ev203.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-03-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev203.__setattr__('nameplate_file', file_obj)
#            ev203.save()
#
#            ev204 = PackageUnit(name = 'EV2-04',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'Room 2',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'THA060S2BN1G',
#                                serial_number = '5609B04220',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = None,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = None,
#                                nameplate_f1_PH = None,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev204.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev204.buildings.add(East)
#            #--connect to spaces
#            ev204.spaces.add(EdenII_space)
#            #--connect to meters
#            ev204.meters.add(e2)            #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-04-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev204.__setattr__('image_file', file_obj)
#            ev204.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-04-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev204.__setattr__('nameplate_file', file_obj)
#            ev204.save()
#
#            ev205 = PackageUnit(name = 'EV2-05',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'Room 1/hall',
#                                age = None,
#                                make = 'Lennox',
#                                model = 'THA048S2BN1G',
#                                serial_number = '5609B01179',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = None,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = None,
#                                nameplate_f1_PH = None,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            ev205.save()
#            #post-creation actions:
#            #--connect to buildings
#            ev205.buildings.add(East)
#            #--connect to spaces
#            ev205.spaces.add(EdenII_space)
#            #--connect to meters
#            ev205.meters.add(e2)            #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-05-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev205.__setattr__('image_file', file_obj)
#            ev205.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-05-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            ev205.__setattr__('nameplate_file', file_obj)
#            ev205.save()
#
#            vgd01 = PackageUnit(name = 'VGD-01',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'EV II overflow',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TCDA07A2A5A0A0A0',
#                                serial_number = '4510G10082',
#                                nameplate_tons = 5.8,
#                                nameplate_EER = 11.0,
#                                nameplate_MBH_in = 72.0,
#                                nameplate_MBH_out = 59.0,
#                                nameplate_ng_eta = 0.82,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 19.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 7.5,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            vgd01.save()
#            #post-creation actions:
#            #--connect to buildings
#            vgd01.buildings.add(East)
#            #--connect to spaces
#            vgd01.spaces.add(dorms_space)
#            #--connect to meters
#            vgd01.meters.add(east_main)    #electric
#            vgd01.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-01-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd01.__setattr__('image_file', file_obj)
#            vgd01.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-01-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd01.__setattr__('nameplate_file', file_obj)
#            vgd01.save()
#
#            vgd02 = PackageUnit(name = 'VGD-02',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'left visiting group',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TCDA07A2A5A0A0A0',
#                                serial_number = '4510G10083',
#                                nameplate_tons = 5.8,
#                                nameplate_EER = 11.0,
#                                nameplate_MBH_in = 72.0,
#                                nameplate_MBH_out = 59.0,
#                                nameplate_ng_eta = 0.82,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 19.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 7.5,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            vgd02.save()
#            #post-creation actions:
#            #--connect to buildings
#            vgd02.buildings.add(East)
#            #--connect to spaces
#            vgd02.spaces.add(dorms_space)
#            #--connect to meters
#            vgd02.meters.add(east_main)    #electric
#            vgd02.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-02-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd02.__setattr__('image_file', file_obj)
#            vgd02.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-02-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd02.__setattr__('nameplate_file', file_obj)
#            vgd02.save()
#
#            vgd03 = PackageUnit(name = 'VGD-03',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'right visiting group/sanctuary',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TCDA07A2A5A0A0A0',
#                                serial_number = '4510G10079',
#                                nameplate_tons = 5.8,
#                                nameplate_EER = 11.0,
#                                nameplate_MBH_in = 72.0,
#                                nameplate_MBH_out = 59.0,
#                                nameplate_ng_eta = 0.82,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 19.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 7.5,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            vgd03.save()
#            #post-creation actions:
#            #--connect to buildings
#            vgd03.buildings.add(East)
#            #--connect to spaces
#            vgd03.spaces.add(dorms_space)
#            #--connect to meters
#            vgd03.meters.add(east_main)    #electric
#            vgd03.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-03-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd03.__setattr__('image_file', file_obj)
#            vgd03.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-03-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd03.__setattr__('nameplate_file', file_obj)
#            vgd03.save()
#
#            vgd04 = PackageUnit(name = 'VGD-04',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'lounge/sanctuary',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TCDA07A2A5A0A0A0',
#                                serial_number = '4510G10084',
#                                nameplate_tons = 5.8,
#                                nameplate_EER = 11.0,
#                                nameplate_MBH_in = 72.0,
#                                nameplate_MBH_out = 59.0,
#                                nameplate_ng_eta = 0.82,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 19.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 7.5,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            vgd04.save()
#            #post-creation actions:
#            #--connect to buildings
#            vgd04.buildings.add(East)
#            #--connect to spaces
#            vgd04.spaces.add(dorms_space)
#            #--connect to meters
#            vgd04.meters.add(east_main)    #electric
#            vgd04.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-04-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd04.__setattr__('image_file', file_obj)
#            vgd04.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-04-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            vgd04.__setattr__('nameplate_file', file_obj)
#            vgd04.save()
#
#            kdh01 = PackageUnit(name = 'KDH-01',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'dining behind bay',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '2207G50292',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh01.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh01.buildings.add(East)
#            #--connect to spaces
#            kdh01.spaces.add(kitchen_space)
#            kdh01.spaces.add(dining_space)
#            #--connect to meters
#            kdh01.meters.add(east_main)    #electric
#            kdh01.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-01-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh01.__setattr__('image_file', file_obj)
#            kdh01.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-01-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh01.__setattr__('nameplate_file', file_obj)
#            kdh01.save()
#
#            kdh02 = PackageUnit(name = 'KDH-02',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'back left dining area',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '1807G20349',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh02.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh02.buildings.add(East)
#            #--connect to spaces
#            kdh02.spaces.add(kitchen_space)
#            kdh02.spaces.add(dining_space)
#            #--connect to meters
#            kdh02.meters.add(east_main)    #electric
#            kdh02.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-02-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh02.__setattr__('image_file', file_obj)
#            kdh02.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-02-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh02.__setattr__('nameplate_file', file_obj)
#            kdh02.save()
#
#            kdh03 = PackageUnit(name = 'KDH-03',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'left dining area',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '1807G10244',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh03.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh03.buildings.add(East)
#            #--connect to spaces
#            kdh03.spaces.add(kitchen_space)
#            kdh03.spaces.add(dining_space)
#            #--connect to meters
#            kdh03.meters.add(east_main)    #electric
#            kdh03.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-03-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh03.__setattr__('image_file', file_obj)
#            kdh03.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-03-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh03.__setattr__('nameplate_file', file_obj)
#            kdh03.save()
#
#            kdh04 = PackageUnit(name = 'KDH-04',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'kitchen',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '2507G20353',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh04.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh04.buildings.add(East)
#            #--connect to spaces
#            kdh04.spaces.add(kitchen_space)
#            kdh04.spaces.add(dining_space)
#            #--connect to meters
#            kdh04.meters.add(east_main)    #electric
#            kdh04.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-04-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh04.__setattr__('image_file', file_obj)
#            kdh04.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-04-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh04.__setattr__('nameplate_file', file_obj)
#            kdh04.save()
#
#            kdh05 = PackageUnit(name = 'KDH-05',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'kitchen office/storage',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '1807G10242',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh05.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh05.buildings.add(East)
#            #--connect to spaces
#            kdh05.spaces.add(kitchen_space)
#            kdh05.spaces.add(dining_space)
#            #--connect to meters
#            kdh05.meters.add(east_main)    #electric
#            kdh05.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-05-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh05.__setattr__('image_file', file_obj)
#            kdh05.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-05-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh05.__setattr__('nameplate_file', file_obj)
#            kdh05.save()
#
#            kdh06 = PackageUnit(name = 'KDH-06',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'central dining area',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '1707G40214',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh06.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh06.buildings.add(East)
#            #--connect to spaces
#            kdh06.spaces.add(kitchen_space)
#            kdh06.spaces.add(dining_space)
#            #--connect to meters
#            kdh06.meters.add(east_main)    #electric
#            kdh06.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-06-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh06.__setattr__('image_file', file_obj)
#            kdh06.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-06-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh06.__setattr__('nameplate_file', file_obj)
#            kdh06.save()
#
#            kdh07 = PackageUnit(name = 'KDH-07',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'left front dining area',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '2207G20239',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh07.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh07.buildings.add(East)
#            #--connect to spaces
#            kdh07.spaces.add(kitchen_space)
#            kdh07.spaces.add(dining_space)
#            #--connect to meters
#            kdh07.meters.add(east_main)    #electric
#            kdh07.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-07-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh07.__setattr__('image_file', file_obj)
#            kdh07.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-07-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh07.__setattr__('nameplate_file', file_obj)
#            kdh07.save()
#
#            kdh08 = PackageUnit(name = 'KDH-08',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'bathrooms',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '2404G40183',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh08.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh08.buildings.add(East)
#            #--connect to spaces
#            kdh08.spaces.add(kitchen_space)
#            kdh08.spaces.add(dining_space)
#            #--connect to meters
#            kdh08.meters.add(east_main)    #electric
#            kdh08.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-08-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh08.__setattr__('image_file', file_obj)
#            kdh08.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-08-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh08.__setattr__('nameplate_file', file_obj)
#            kdh08.save()
#
#            kdh09 = PackageUnit(name = 'KDH-09',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'right central dining area',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '3403G20210',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh09.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh09.buildings.add(East)
#            #--connect to spaces
#            kdh09.spaces.add(kitchen_space)
#            kdh09.spaces.add(dining_space)
#            #--connect to meters
#            kdh09.meters.add(east_main)    #electric
#            kdh09.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-09-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh09.__setattr__('image_file', file_obj)
#            kdh09.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-09-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh09.__setattr__('nameplate_file', file_obj)
#            kdh09.save()
#
#            kdh10 = PackageUnit(name = 'KDH-10',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'right front dining area',
#                                age = None,
#                                make = 'Carrier',
#                                model = '48TFD006-A-511',
#                                serial_number = '2404G40181',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 74.0,
#                                nameplate_MBH_out = 59.2,
#                                nameplate_ng_eta = 0.80,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 3,
#                                nameplate_e1_FLA = 5.2,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh10.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh10.buildings.add(East)
#            #--connect to spaces
#            kdh10.spaces.add(kitchen_space)
#            kdh10.spaces.add(dining_space)
#            #--connect to meters
#            kdh10.meters.add(east_main)    #electric
#            kdh10.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-10-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh10.__setattr__('image_file', file_obj)
#            kdh10.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-10-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh10.__setattr__('nameplate_file', file_obj)
#            kdh10.save()
#
#            kdh11 = PackageUnit(name = 'KDH-11',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'most likely walk-in freezer condensing unit',
#                                age = None,
#                                make = 'Heatcraft',
#                                model = 'MOZ055L63CF',
#                                serial_number = 'T06F 04439',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 17.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 3.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh11.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh11.buildings.add(East)
#            #--connect to spaces
#            kdh11.spaces.add(kitchen_space)
#            kdh11.spaces.add(dining_space)
#            #--connect to meters
#            kdh11.meters.add(east_main)    #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-11-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh11.__setattr__('image_file', file_obj)
#            kdh11.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-11-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh11.__setattr__('nameplate_file', file_obj)
#            kdh11.save()
#
#            kdh12 = PackageUnit(name = 'KDH-12',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'most likely walk-in cooler condensing unit',
#                                age = None,
#                                make = 'Heatcraft',
#                                model = 'MOH029M23C',
#                                serial_number = 'T07M 00203',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 2,
#                                nameplate_c1_RLA = 9.9,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 0.5,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh12.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh12.buildings.add(East)
#            #--connect to spaces
#            kdh12.spaces.add(kitchen_space)
#            kdh12.spaces.add(dining_space)
#            #--connect to meters
#            kdh12.meters.add(east_main)    #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-12-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh12.__setattr__('image_file', file_obj)
#            kdh12.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-12-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh12.__setattr__('nameplate_file', file_obj)
#            kdh12.save()
#
#            kdh13 = PackageUnit(name = 'KDH-13',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'most likely vent hood or other kitchen exhaust',
#                                age = None,
#                                make = 'Cook',
#                                model = '150KSP-B',
#                                serial_number = '050S930748-0070005901',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = None,
#                                nameplate_c1_RLA = None,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 3,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh13.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh13.buildings.add(East)
#            #--connect to spaces
#            kdh13.spaces.add(kitchen_space)
#            kdh13.spaces.add(dining_space)
#            #--connect to meters
#            kdh13.meters.add(east_main)    #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-13-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh13.__setattr__('image_file', file_obj)
#            kdh13.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-13-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh13.__setattr__('nameplate_file', file_obj)
#            kdh13.save()
#
#            kdh14 = PackageUnit(name = 'KDH-14',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'most likely vent hood or other kitchen exhaust',
#                                age = None,
#                                make = 'Cook',
#                                model = '225V9B',
#                                serial_number = '050S930748-00/0003601',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = None,
#                                nameplate_c1_RLA = None,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 3,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh14.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh14.buildings.add(East)
#            #--connect to spaces
#            kdh14.spaces.add(kitchen_space)
#            kdh14.spaces.add(dining_space)
#            #--connect to meters
#            kdh14.meters.add(east_main)    #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-14-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh14.__setattr__('image_file', file_obj)
#            kdh14.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-14-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh14.__setattr__('nameplate_file', file_obj)
#            kdh14.save()
#
#            kdh15 = PackageUnit(name = 'KDH-15',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'most likely vent hood or other kitchen exhaust',
#                                age = None,
#                                make = 'Cook',
#                                model = '100C15DH',
#                                serial_number = '050S930748-00/0004801',
#                                nameplate_tons = None,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = None,
#                                nameplate_c1_RLA = None,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = None,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            kdh15.save()
#            #post-creation actions:
#            #--connect to buildings
#            kdh15.buildings.add(East)
#            #--connect to spaces
#            kdh15.spaces.add(kitchen_space)
#            kdh15.spaces.add(dining_space)
#            #--connect to meters
#            kdh15.meters.add(east_main)    #electric
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-15-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh15.__setattr__('image_file', file_obj)
#            kdh15.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-15-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            kdh15.__setattr__('nameplate_file', file_obj)
#            kdh15.save()
#
#            gyc01 = PackageUnit(name = 'GYC-01',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'weight room/Art Room',
#                                age = None,
#                                make = 'Goodman',
#                                model = 'CPG0601403DXXXBA',
#                                serial_number = '0903666056',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 138.0,
#                                nameplate_MBH_out = 110.0,
#                                nameplate_ng_eta = 0.797,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 7.6,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            gyc01.save()
#            #post-creation actions:
#            #--connect to buildings
#            gyc01.buildings.add(East)
#            #--connect to spaces
#            gyc01.spaces.add(gym_space)
#            gyc01.spaces.add(school_space)
#            #--connect to meters
#            gyc01.meters.add(east_main)    #electric
#            gyc01.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-01-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gyc01.__setattr__('image_file', file_obj)
#            gyc01.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-01-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gyc01.__setattr__('nameplate_file', file_obj)
#            gyc01.save()
#
#            gyc02 = PackageUnit(name = 'GYC-02',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'gym/CORE',
#                                age = None,
#                                make = 'Goodman',
#                                model = 'CPG0601403DXXXBA',
#                                serial_number = '0903666057',
#                                nameplate_tons = 5.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = 138.0,
#                                nameplate_MBH_out = 110.0,
#                                nameplate_ng_eta = 0.797,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 16.0,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = 1,
#                                nameplate_e1_PH = 1,
#                                nameplate_e1_FLA = 7.6,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            gyc02.save()
#            #post-creation actions:
#            #--connect to buildings
#            gyc02.buildings.add(East)
#            #--connect to spaces
#            gyc02.spaces.add(gym_space)
#            gyc02.spaces.add(school_space)
#            #--connect to meters
#            gyc02.meters.add(east_main)    #electric
#            gyc02.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-02-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gyc02.__setattr__('image_file', file_obj)
#            gyc02.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-02-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gyc02.__setattr__('nameplate_file', file_obj)
#            gyc02.save()
#
#            gyc03 = PackageUnit(name = 'GYC-03',
#                                equipment_type = 'Package Unit',
#                                location = 'East Bldg rooftop',
#                                description = '',
#                                serves = 'classrooms',
#                                age = None,
#                                make = 'Carrier',
#                                model = '25HBC348A500',
#                                serial_number = '3610E05804',
#                                nameplate_tons = 4.0,
#                                nameplate_EER = None,
#                                nameplate_MBH_in = None,
#                                nameplate_MBH_out = None,
#                                nameplate_ng_eta = None,
#                                nameplate_V = 230.0,
#                                nameplate_phase = 3,
#                                nameplate_pf = None,
#                                nameplate_RFC = None,
#                                nameplate_c1_QTY = 1,
#                                nameplate_c1_RLA = 13.7,
#                                nameplate_c1_PH = None,
#                                nameplate_c2_QTY = None,
#                                nameplate_c2_RLA = None,
#                                nameplate_c2_PH = None,
#                                nameplate_c3_QTY = None,
#                                nameplate_c3_RLA = None,
#                                nameplate_c3_PH = None,
#                                nameplate_e1_QTY = None,
#                                nameplate_e1_PH = None,
#                                nameplate_e1_FLA = None,
#                                nameplate_e2_QTY = None,
#                                nameplate_e2_PH = None,
#                                nameplate_e2_FLA = None,
#                                nameplate_f1_QTY = 1,
#                                nameplate_f1_PH = 1,
#                                nameplate_f1_FLA = 1.4,
#                                nameplate_f2_QTY = None,
#                                nameplate_f2_PH = None,
#                                nameplate_f2_FLA = None,
#                                dP_fan_max = None,
#                                dP_fan_min = None,
#                                SAF_max = None,
#                                SAF_min = None,
#                                speed_min = None,
#                                T_max = None,
#                                T_min = None,
#                                d = None,
#                                m = None,
#                                f = None,
#                                e = None,
#                                SCOC = None,
#                                SCUN = None,
#                                SHOC = None,
#                                SHUN = None,
#                                SRFC = None,
#                                )
#            gyc03.save()
#            #post-creation actions:
#            #--connect to buildings
#            gyc03.buildings.add(East)
#            #--connect to spaces
#            gyc03.spaces.add(school_space)
#            #--connect to meters
#            gyc03.meters.add(east_main)    #electric            
#            gyc03.meters.add(gas1290)       #gas
#            #--load image files
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-03-photo.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gyc03.__setattr__('image_file', file_obj)
#            gyc03.save()
#            file_url = STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-03-nameplate.jpg'
#            result = urllib.urlretrieve(file_url)
#            file_obj = File(open(result[0]))
#            gyc03.__setattr__('nameplate_file', file_obj)
#            gyc03.save()
#
#        except:
#            print 'Failed to create new Equipment.'


    ###---Measures
        acct1 = Account.objects.get(name='Town of Refuge, Inc. - ATL')
        ws = WeatherStation.objects.all()[0]
        e2 = Meter.objects.filter(account=acct1).get(name='Eden II (electric)')
        east_main = Meter.objects.filter(account=acct1).get(name='East Bldg (electric)')
        ev201 = Equipment.objects.filter(Q(buildings__account=acct1) | Q(meters__account=acct1)).distinct().get(name='EV2-01')
        ev202 = Equipment.objects.filter(Q(buildings__account=acct1) | Q(meters__account=acct1)).distinct().get(name='EV2-02')
        ev203 = Equipment.objects.filter(Q(buildings__account=acct1) | Q(meters__account=acct1)).distinct().get(name='EV2-03')
        ev204 = Equipment.objects.filter(Q(buildings__account=acct1) | Q(meters__account=acct1)).distinct().get(name='EV2-04')
        ev205 = Equipment.objects.filter(Q(buildings__account=acct1) | Q(meters__account=acct1)).distinct().get(name='EV2-05')

        try:
            em1_elec = EfficiencyMeasure(name = 'Controls on 23 RTUs (electric)',
                                            when = datetime(2014,3,1,tzinfo=UTC),
                                            utility_type = 'electricity',
                                            units = 'kW,kWh',
                                            annual_consumption_savings = 58000.0,
                                            peak_demand_savings = 0.0,
                                            annual_cost_savings = 7500.0,
                                            percent_uncertainty = 0.05,
                                            percent_cool = 0.47,
                                            percent_heat = 0.53,
                                            percent_flat = 0.0,
                                            percent_fixed = 0.0,
                                            
                                            weather_station = ws,
                                            )
            em1_elec.save()
            #post-creation actions:
            #--apportion annual savings numbers to individual months
            em1_elec.apportion_savings()
            #--create intermediate models to assign to Meters
            emma1 = EMMeterApportionment(efficiency_measure = em1_elec,
                                         meter = e2,
                                         assigned_fraction = 0.58)
            emma1.save()
            emma2 = EMMeterApportionment(efficiency_measure = em1_elec,
                                         meter = east_main,
                                         assigned_fraction = 0.42)
            emma2.save()
            #--create intermediate models to assign to Equipment
            for equip in [ev201,ev202,ev203,ev204,ev205]:
                emeaX = EMEquipmentApportionment(efficiency_measure = em1_elec,
                                             equipment = equip,
                                             assigned_fraction = 0.116)
                emeaX.save()
            
#            for equip in [vgd01,vgd02,vgd03,vgd04,kdh01,kdh02,kdh03,kdh04,kdh05,kdh06,
#                          kdh07,kdh08,kdh09,kdh10,gyc01,gyc02,gyc03]:
#                emeaX = EMEquipmentApportionment(efficiency_measure = em1_elec,
#                                             equipment = equip,
#                                             assigned_fraction = 0.0247)
#                emeaX.save()

            
#            em1_gas = EfficiencyMeasure(name = 'Controls on 23 RTUs (gas)',
#                                        when = datetime(2014,3,1,tzinfo=UTC),
#                                        utility_type = 'natural gas',
#                                        units = 'therms/h,therms',
#                                        annual_consumption_savings = 1500.0,
#                                        peak_demand_savings = 0.0,
#                                        annual_cost_savings = 1100.0,
#                                        percent_uncertainty = 0.05,
#                                        percent_cool = 0.0,
#                                        percent_heat = 1.0,
#                                        percent_flat = 0.0,
#                                        percent_fixed = 0.0,
#                                        
#                                        weather_station = ws,
#                                        )
#            em1_gas.save()
#            #post-creation actions:
#            #--apportion annual savings numbers to individual months
#            em1_gas.apportion_savings()
#            #--create intermediate models to assign to Meters
#            emma1 = EMMeterApportionment(efficiency_measure = em1_gas,
#                                         meter = gas1290,
#                                         assigned_fraction = 1.0)
#            emma1.save()
#            #--create intermediate models to assign to Equipment
#            for equip in [vgd01,vgd02,vgd03,vgd04,kdh01,kdh02,kdh03,kdh04,kdh05,kdh06,
#                          kdh07,kdh08,kdh09,kdh10,gyc01,gyc02,gyc03]:
#                emeaX = EMEquipmentApportionment(efficiency_measure = em1_elec,
#                                             equipment = equip,
#                                             assigned_fraction = 0.0588)
                emeaX.save()
            
        except:
            print 'Failed to create new Measures.'
