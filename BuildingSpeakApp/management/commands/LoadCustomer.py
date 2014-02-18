from django.core.management.base import BaseCommand

from pytz import UTC
from decimal import Decimal
from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User

from BuildingSpeak.settings import STATIC_URL

from BuildingSpeakApp.models import UserProfile, Account, Building, Space, Meter
from BuildingSpeakApp.models import PackageUnit
from BuildingSpeakApp.models import SpaceMeterApportionment, BuildingMeterApportionment
from BuildingSpeakApp.models import EfficiencyMeasure, EMMeterApportionment, EMEquipmentApportionment
from BuildingSpeakApp.models import WeatherStation, Utility
from BuildingSpeakApp.models import GAPowerPandL, InfiniteEnergyGAGas, CityOfATLWWW
from BuildingSpeakApp.models import set_file_field



class Command(BaseCommand):

    def handle(self, *args, **options):

    ###---Users
        try:
            userJD = User.objects.get(username = 'jdovi')       #loaded to add to all new accounts
            userDA = User.objects.get(username = 'dashley')     #loaded to add to all new accounts
            
            user1 = User(
                username = 'smucker',
                password = 'lastlostleast',
                first_name = 'Steve',
                last_name = 'Smucker',
                email = 'smucker@cityofrefugeatl.org',
                is_active = True,
                is_staff = False,
                is_superuser = False,
                )
            user1.save()
        except:
            print 'Failed to create new Users.'
        
    ###---UserProfiles
        try:
            userprofile1 = UserProfile(
                user = user1,
                organization = 'Town of Refuge, Inc. - ATL'
                )
            userprofile1.save()
            #post-creation actions
            #--load image file
            set_file_field(userprofile1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/UserImages/default_user_image.png')
        except:
            print 'Failed to create new UserProfiles.'
        
    ###---Account
        try:
            acct1 = Account(
                name = 'Town of Refuge, Inc. - ATL',
                account_type = 'Commercial',
                street_address = '1300 Joseph Boone Blvd',
                city = 'Atlanta',
                state = 'GA',
                zip_code = '30314',
                launch_date = timezone.now(),
                first_name = 'Steve',
                last_name = 'Smucker',
                title = 'Director of Maintenance',
                email = 'smucker@cityofrefugeatl.org',
                phone = '404-713-6994',
                status = 'Active',
                monthly_payment = Decimal(0.0),
                )
            acct1.save()
            
            #post-creation actions
            #--attach users
            acct1.users.add(User.objects.get(username = 'smucker'))
            acct1.users.add(userJD)
            acct1.users.add(userDA)
            
            #--load image file
            set_file_field(acct1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/AccountImage_CityOfRefuge.gif')
        except:
            print 'Failed to create new Accounts.'
        
    ###---Buildings
        try:
            ws = WeatherStation.objects.get(name = 'ATL - downtown west')
            
            East = Building(
                name = 'East Bldg',
                building_type = 'Multi-Purpose',
                EIA_type = 'Other',
                ESPM_type = 'Other',
                account = acct1,
                weather_station = ws,
                street_address = '1300 Joseph Boone Blvd',
                city = 'Atlanta',
                state = 'GA',
                zip_code = '30314',
                age = 2004,
                square_footage = Decimal(49800),
                stories = 1,
                max_occupancy = None,
                first_name = 'Steve',
                last_name = 'Smucker',
                title = 'Director of Maintenance',
                email = 'smucker@cityofrefugeatl.org',
                phone = '404-713-6994',
                )
            East.save()
    
            #post-creation actions
            #--load image file
            set_file_field(East,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/BuildingImages/BuildingImage_EastBldg.JPG')
            
            West = Building(
                name = 'West Bldg',
                building_type = 'Multi-Purpose',
                EIA_type = 'Other',
                ESPM_type = 'Other',
                account = acct1,
                weather_station = ws,
                street_address = '1300 Joseph Boone Blvd',
                city = 'Atlanta',
                state = 'GA',
                zip_code = '30314',
                age = 2004,
                square_footage = Decimal(152000),
                stories = 1,
                max_occupancy = None,
                first_name = 'Steve',
                last_name = 'Smucker',
                title = 'Director of Maintenance',
                email = 'smucker@cityofrefugeatl.org',
                phone = '404-713-6994',
                )
            West.save()
            
            #post-creation actions:
            #--load image file
            set_file_field(West,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/BuildingImages/BuildingImage_WestBldg.JPG')
        except:
            print 'Failed to create new Buildings.'
        
    ###---Spaces
        try:
            EdenI_space = Space(
                name = 'Eden I',
                building = West,
                square_footage = Decimal(36000),
                max_occupancy = None,
                space_type = 'Dormitory',
                EIA_type = 'Lodging',
                ESPM_type = 'Dormitory / Residence Hall',
                )
            EdenI_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(EdenI_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            kitchen_space = Space(
                name = '180 Kitchen',
                building = East,
                square_footage = Decimal(4500),
                max_occupancy = None,
                space_type = 'Dining: Family',
                EIA_type = 'Food Service',
                ESPM_type = 'Other',
                )
            kitchen_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(kitchen_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            dining_space = Space(
                name = 'Dining Area',
                building = East,
                square_footage = Decimal(11500),
                max_occupancy = None,
                space_type = 'Dining: Family',
                EIA_type = 'Food Service',
                ESPM_type = 'Other',
                )
            dining_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(dining_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            compATL_space = Space(
                name = 'Compassion ATL',
                building = West,
                square_footage = Decimal(36000),
                max_occupancy = None,
                space_type = 'Warehouse',
                EIA_type = 'Warehouse and Storage',
                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
                )
            compATL_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(compATL_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/SpaceImage_compATL.JPG')
            
            EdenII_space = Space(
                name = 'Eden II',
                building = East,
                square_footage = Decimal(9700),
                max_occupancy = None,
                space_type = 'Dormitory',
                EIA_type = 'Lodging',
                ESPM_type = 'Dormitory / Residence Hall',
                )
            EdenII_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(EdenII_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            dorms_space = Space(
                name = 'Dorms',
                building = East,
                square_footage = Decimal(11000),
                max_occupancy = None,
                space_type = 'Dormitory',
                EIA_type = 'Lodging',
                ESPM_type = 'Dormitory / Residence Hall',
                )
            dorms_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(dorms_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            gym_space = Space(
                name = 'Gym',
                building = East,
                square_footage = Decimal(8700),
                max_occupancy = None,
                space_type = 'Gymnasium',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            gym_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(gym_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/SpaceImage_gym.JPG')
            
            clinic_space = Space(
                name = 'Clinic',
                building = West,
                square_footage = Decimal(8700),
                max_occupancy = None,
                space_type = 'Health Care Clinic',
                EIA_type = 'Health Care - Outpatient',
                ESPM_type = 'Medical Office',
                )
            clinic_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(clinic_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            offices_space = Space(
                name = 'Offices',
                building = West,
                square_footage = Decimal(10400),
                max_occupancy = None,
                space_type = 'Office',
                EIA_type = 'Office',
                ESPM_type = 'Office',
                )
            offices_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(offices_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            playground_space = Space(
                name = 'Playground',
                building = West,
                square_footage = Decimal(4800),
                max_occupancy = None,
                space_type = 'Gymnasium',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            playground_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(playground_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            school_space = Space(
                name = 'CORE',
                building = East,
                square_footage = Decimal(4400),
                max_occupancy = None,
                space_type = 'School/University',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            school_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(school_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/SpaceImage_school.JPG')
            
            unfinished_space = Space(
                name = 'Unfinished',
                building = West,
                square_footage = Decimal(44100),
                max_occupancy = None,
                space_type = 'Warehouse',
                EIA_type = 'Warehouse and Storage',
                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
                )
            unfinished_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(unfinished_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            newschool_space = Space(
                name = 'Bright Futures',
                building = West,
                square_footage = Decimal(7000),
                max_occupancy = None,
                space_type = 'School/University',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            newschool_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(newschool_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
            
            newchurch_space = Space(
                name = 'Church',
                building = West,
                square_footage = Decimal(5000),
                max_occupancy = None,
                space_type = 'Religious Building',
                EIA_type = 'Religious Worship',
                ESPM_type = 'House of Worship',
                )
            newchurch_space.save()
            #post-creation actions:
            #--load image file
            set_file_field(newchurch_space,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/SpaceImages/default_space_image.png')
        except:
            print 'Failed to create new Spaces.'        
        
    ###---Meters
        try:
            gpc = Utility.objects.get(name = 'Georgia Power Company')
            infe = Utility.objects.get(name = 'Infinite Energy')
            atlw = Utility.objects.get(name = 'City of Atlanta, Dept. of Watershed Mgmt.')
            
            atlwww = CityOfATLWWW.objects.get(name = 'Water and Wastewater 2012')
            infebizgas = InfiniteEnergyGAGas.objects.get(name = 'Fixed Business Rate')
            gpc_pls8_sec_in = GAPowerPandL.objects.get(name = 'GPC-PLS-8-secondary-inside')
            gpc_plm8_sec_in = GAPowerPandL.objects.get(name = 'GPC-PLM-8-secondary-inside')
            #gpc_gs7 = GAPowerGS.objects.get(name = 'GPC-GS-7') #####NEED TO MAKE
            #gpc_toueo7 = GAPowerTOU.objects.get(name = 'GPC-TOU-EO-7') #####NEED TO MAKE
            #gpc_tougsd7 = GAPowerTOU.objects.get(name = 'GPC-TOU-GSD-7') #####NEED TO MAKE
            
            east_main = Meter(
                name = 'East Bldg (electric)',
                utility_type = 'electricity',
                location = 'loading dock area of bldg',
                serves = 'all of East Bldg except Eden II',
                units = 'kW,kWh',
                weather_station = ws,
                utility = gpc,
#                rate_schedule = gpc_toueo7,
                rate_schedule = gpc_plm8_sec_in,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '6126898026',
                utility_meter_number = '3081617',
                )
            east_main.save()
            #post-creation actions:
            #--load image files
            set_file_field(east_main,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EastMain.JPG')
            set_file_field(east_main,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EastMain.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(east_main,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            east_main.upload_bill_data(create_models_if_nonexistent=True)
            east_main.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = east_main,
                                              building = East,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = east_main,
                                           space = kitchen_space,
                                           assigned_fraction = Decimal(0.3))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = east_main,
                                           space = dining_space,
                                           assigned_fraction = Decimal(0.2))
            sma2.save()
            sma3 = SpaceMeterApportionment(meter = east_main,
                                           space = dorms_space,
                                           assigned_fraction = Decimal(0.1))
            sma3.save()
            sma4 = SpaceMeterApportionment(meter = east_main,
                                           space = gym_space,
                                           assigned_fraction = Decimal(0.2))
            sma4.save()
            sma5 = SpaceMeterApportionment(meter = east_main,
                                           space = school_space,
                                           assigned_fraction = Decimal(0.2))
            sma5.save()
    
            
            e1 = Meter(
                name = 'Eden I (electric)',
                utility_type = 'electricity',
                location = 'northwest corner of West Bldg',
                serves = 'Eden I',
                units = 'kW,kWh',
                weather_station = ws,
                utility = gpc,
                rate_schedule = gpc_plm8_sec_in,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '0437031108',
                utility_meter_number = '3081619',
                )
            e1.save()
            #post-creation actions:
            #--load image files
            set_file_field(e1,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EdenI.JPG')
            set_file_field(e1,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EdenI.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(e1,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            e1.upload_bill_data(create_models_if_nonexistent = True)
            e1.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = e1,
                                              building = West,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = e1,
                                           space = EdenI_space,
                                           assigned_fraction = Decimal(1.0))
            sma1.save()
            
            
            e2 = Meter(
                name = 'Eden II (electric)',
                utility_type = 'electricity',
                location = 'northwest corner of East Bldg',
                serves = 'Eden II',
                units = 'kW,kWh',
                weather_station = ws,
                utility = gpc,
                rate_schedule = gpc_plm8_sec_in,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '3244865006',
                utility_meter_number = '3179180',
                )
            e2.save()
            #post-creation actions:
            #--load image files
            set_file_field(e2,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EdenII.JPG')
            set_file_field(e2,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EdenII.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(e2,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            e2.upload_bill_data(create_models_if_nonexistent = True)
            e2.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = e2,
                                              building = East,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = e2,
                                           space = EdenII_space,
                                           assigned_fraction = Decimal(1.0))
            sma1.save()
            
            wh = Meter(
                name = 'West Bldg south (electric)',
                utility_type = 'electricity',
                location = 'just south of Offices entrance on West Bldg',
                serves = 'Offices and Compassion ATL',
                units = 'kW,kWh',
                weather_station = ws,
                utility = gpc,
#                rate_schedule = gpc_toueo7,
                rate_schedule = gpc_plm8_sec_in,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '6168898017',
                utility_meter_number = '3081618',
                )
            wh.save()
            #post-creation actions:
            #--load image files
            set_file_field(wh,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Warehouse.JPG')
            set_file_field(wh,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Warehouse.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(wh,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            wh.upload_bill_data(create_models_if_nonexistent = True)
            wh.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = wh,
                                              building = West,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = wh,
                                           space = compATL_space,
                                           assigned_fraction = Decimal(0.3))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = wh,
                                           space = unfinished_space,
                                           assigned_fraction = Decimal(0.2))
            sma2.save()
            sma3 = SpaceMeterApportionment(meter = wh,
                                           space = offices_space,
                                           assigned_fraction = Decimal(0.5))
            sma3.save()
            
            newschool = Meter(
                name = 'New School (electric)',
                utility_type = 'electricity',
                location = 'south of Eden I entrance on West Bldg',
                serves = 'Playground and unfinished area between Eden I and Clinic',
                units = 'kW,kWh',
                weather_station = ws,
                utility = gpc,
#                rate_schedule = gpc_gs7,
                rate_schedule = gpc_plm8_sec_in,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '6147898017',
                utility_meter_number = '3081616',
                )
            newschool.save()
            #post-creation actions:
            #--load image files
            set_file_field(newschool,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_NewSchool.JPG')
            set_file_field(newschool,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_NewSchool.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(newschool,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            newschool.upload_bill_data(create_models_if_nonexistent = True)
            newschool.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = newschool,
                                              building = West,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = newschool,
                                           space = playground_space,
                                           assigned_fraction = Decimal(0.1))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = newschool,
                                           space = newschool_space,
                                           assigned_fraction = Decimal(0.7))
            sma2.save()
            sma3 = SpaceMeterApportionment(meter = newschool,
                                           space = newchurch_space,
                                           assigned_fraction = Decimal(0.2))
            sma3.save()
            
            clinic = Meter(
                name = 'Clinic (electric)',
                utility_type = 'electricity',
                location = 'north of covered Clinic entrance on West Bldg',
                serves = 'Clinic',
                units = 'kW,kWh',
                weather_station = ws,
                utility = gpc,
                rate_schedule = gpc_pls8_sec_in,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '1816415005',
                utility_meter_number = '3046324',
                )
            clinic.save()
            #post-creation actions:
            #--load image files
            set_file_field(clinic,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Clinic.JPG')
            set_file_field(clinic,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Clinic.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(clinic,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            clinic.upload_bill_data(create_models_if_nonexistent = True)
            clinic.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = clinic,
                                              building = West,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = clinic,
                                           space = clinic_space,
                                           assigned_fraction = Decimal(1.0))
            sma1.save()
            
            gas1290 = Meter(
                name = 'East Bldg (natural gas)',
                utility_type = 'natural gas',
                location = 'unknown',
                serves = 'East Bldg heating and domestic hot water',
                units = 'therms/h,therms',
                weather_station = ws,
                utility = infe,
                rate_schedule = infebizgas,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '9401260170',
                utility_meter_number = '000537796',
                )
            gas1290.save()
            #post-creation actions:
            #--load image files
            set_file_field(gas1290,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_EastGas.JPG')
            set_file_field(gas1290,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_EastGas.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(gas1290,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            gas1290.upload_bill_data(create_models_if_nonexistent = True)
            gas1290.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = gas1290,
                                              building = East,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = gas1290,
                                           space = dorms_space,
                                           assigned_fraction = Decimal(0.1))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = gas1290,
                                           space = kitchen_space,
                                           assigned_fraction = Decimal(0.4))
            sma2.save()
            sma3 = SpaceMeterApportionment(meter = gas1290,
                                           space = dining_space,
                                           assigned_fraction = Decimal(0.1))
            sma3.save()
            sma4 = SpaceMeterApportionment(meter = gas1290,
                                           space = gym_space,
                                           assigned_fraction = Decimal(0.2))
            sma4.save()
            sma5 = SpaceMeterApportionment(meter = gas1290,
                                           space = school_space,
                                           assigned_fraction = Decimal(0.1))
            sma5.save()
            sma6 = SpaceMeterApportionment(meter = gas1290,
                                           space = EdenII_space,
                                           assigned_fraction = Decimal(0.1))
            sma6.save()
            
            gas1300 = Meter(
                name = 'West Bldg (natural gas)',
                utility_type = 'natural gas',
                location = 'unknown',
                serves = 'West Bldg heating and domestic hot water',
                units = 'therms/h,therms',
                weather_station = ws,
                utility = infe,
                rate_schedule = infebizgas,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '8783526395',
                utility_meter_number = '003008386',
                )
            gas1300.save()
            #post-creation actions:
            #--load image files
            set_file_field(gas1300,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_WestGas.JPG')
            set_file_field(gas1300,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_WestGas.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(gas1300,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            gas1300.upload_bill_data(create_models_if_nonexistent = True)
            gas1300.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = gas1300,
                                              building = West,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = gas1300,
                                           space = playground_space,
                                           assigned_fraction = Decimal(0.1))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = gas1300,
                                           space = newschool_space,
                                           assigned_fraction = Decimal(0.2))
            sma2.save()
            sma3 = SpaceMeterApportionment(meter = gas1300,
                                           space = newchurch_space,
                                           assigned_fraction = Decimal(0.1))
            sma3.save()
            sma4 = SpaceMeterApportionment(meter = gas1300,
                                           space = EdenI_space,
                                           assigned_fraction = Decimal(0.3))
            sma4.save()
            sma5 = SpaceMeterApportionment(meter = gas1300,
                                           space = clinic_space,
                                           assigned_fraction = Decimal(0.15))
            sma5.save()
            sma6 = SpaceMeterApportionment(meter = gas1300,
                                           space = offices_space,
                                           assigned_fraction = Decimal(0.15))
            sma6.save()
            
            simpson1290 = Meter(
                name = '1290 Simpson (water)',
                utility_type = 'domestic water',
                location = 'unknown',
                serves = 'unknown',
                units = 'gpm,gal',
                weather_station = ws,
                utility = atlw,
                rate_schedule = atlwww,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '11-2487.301',
                utility_meter_number = 'NE51964675',
                )
            simpson1290.save()
            #post-creation actions:
            #--load image files
            set_file_field(simpson1290,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Simpson1290.JPG')
            set_file_field(simpson1290,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Simpson1290.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(simpson1290,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            simpson1290.upload_bill_data(create_models_if_nonexistent = True)
            simpson1290.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = simpson1290,
                                              building = East,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = simpson1290,
                                           space = kitchen_space,
                                           assigned_fraction = Decimal(0.7))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = simpson1290,
                                           space = EdenII_space,
                                           assigned_fraction = Decimal(0.3))
            sma2.save()
            
            boone1300 = Meter(
                name = '1300 Boone (water)',
                utility_type = 'domestic water',
                location = 'unknown',
                serves = 'unknown',
                units = 'gpm,gal',
                weather_station = ws,
                utility = atlw,
                rate_schedule = atlwww,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '12-9779.302',
                utility_meter_number = 'NE049764661',
                )
            boone1300.save()
            #post-creation actions:
            #--load image files
            set_file_field(boone1300,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Boone1300.JPG')
            set_file_field(boone1300,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Boone1300.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(boone1300,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            boone1300.upload_bill_data(create_models_if_nonexistent = True)
            boone1300.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = boone1300,
                                              building = West,
                                              assigned_fraction = Decimal(1.0))
            bma1.save()
            #--connect to spaces
            sma1 = SpaceMeterApportionment(meter = simpson1290,
                                           space = EdenI_space,
                                           assigned_fraction = Decimal(0.5))
            sma1.save()
            sma2 = SpaceMeterApportionment(meter = simpson1290,
                                           space = clinic_space,
                                           assigned_fraction = Decimal(0.1))
            sma2.save()
            sma3 = SpaceMeterApportionment(meter = simpson1290,
                                           space = newschool_space,
                                           assigned_fraction = Decimal(0.2))
            sma3.save()
            sma4 = SpaceMeterApportionment(meter = simpson1290,
                                           space = offices_space,
                                           assigned_fraction = Decimal(0.1))
            sma4.save()
            sma5 = SpaceMeterApportionment(meter = simpson1290,
                                           space = compATL_space,
                                           assigned_fraction = Decimal(0.1))
            sma5.save()

            simpson1300 = Meter(
                name = '1300 Simpson (water)',
                utility_type = 'domestic water',
                location = 'unknown',
                serves = 'fire service',
                units = 'gpm,gal',
                weather_station = ws,
                utility = atlw,
                rate_schedule = atlwww,
                account = acct1,
                make = 'unknown',
                model = 'unknown',
                serial_number = 'unknown',
                utility_account_number = '0155559301',
                utility_meter_number = 'unknown',
                )
            simpson1300.save()
            #post-creation actions:
            #--load image files
            set_file_field(simpson1300,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterLocation_Simpson1300.JPG')
            set_file_field(simpson1300,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterImages/MeterNameplate_Simpson1300.JPG')
            #--load bill data file, possibly create meter models
            set_file_field(simpson1300,
                            'bill_data_file',
                            STATIC_URL + 'upload_files/NewAccount/MeterBillData/Eden_I_Electric.csv')
            simpson1300.upload_bill_data(create_models_if_nonexistent = True)
            simpson1300.save()
            #--connect to buildings
            bma1 = BuildingMeterApportionment(meter = simpson1300,
                                              building = East,
                                              assigned_fraction = Decimal(0.5))
            bma1.save()
            bma2 = BuildingMeterApportionment(meter = simpson1300,
                                              building = West,
                                              assigned_fraction = Decimal(0.5))
            bma2.save()

        except:
            print 'Failed to create new Meters.'

    ###---Equipment
        try:
            off01 = PackageUnit(name = 'OFF-01',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'Bankhead',
                                age = None,
                                make = 'Trane',
                                model = 'YCD048C3L0BA',
                                serial_number = 'J161427170',
                                nameplate_tons = Decimal(4.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(90.0),
                                nameplate_MBH_out = Decimal(72.9),
                                nameplate_ng_eta = Decimal(0.81),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(14.8),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(4.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(2.1),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            off01.save()
            #post-creation actions:
            #--connect to buildings
            off01.buildings.add(West)
            #--connect to spaces
            off01.spaces.add(offices_space)
            #--connect to meters
            off01.meters.add(wh)        #electric
            off01.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(off01,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-01-photo.JPG')
            set_file_field(off01,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-01-nameplate.JPG')

            off02 = PackageUnit(name = 'OFF-02',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'Kim, foyer/hall/Simpson/bathrooms',
                                age = None,
                                make = 'Lennox',
                                model = 'GCS16-1353-270-7Y',
                                serial_number = '5692C00479',
                                nameplate_tons = Decimal(10.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(270.0),
                                nameplate_MBH_out = Decimal(216.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(17.3),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(10.6),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(2.1),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            off02.save()
            #post-creation actions:
            #--connect to buildings
            off02.buildings.add(West)
            #--connect to spaces
            off02.spaces.add(offices_space)
            #--connect to meters
            off02.meters.add(wh)        #electric
            off02.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(off02,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-02-photo.JPG')
            set_file_field(off02,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-02-nameplate.JPG')

            off03 = PackageUnit(name = 'OFF-03',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'Kids Cave',
                                age = None,
                                make = 'Payne',
                                model = '588ANW030080ACAD',
                                serial_number = '2196G10899',
                                nameplate_tons = Decimal(2.5),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(80.0),
                                nameplate_MBH_out = Decimal(64.8),
                                nameplate_ng_eta = Decimal(0.81),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(1),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(14.4),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(2.0),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            off03.save()
            #post-creation actions:
            #--connect to buildings
            off03.buildings.add(West)
            #--connect to spaces
            off03.spaces.add(offices_space)
            #--connect to meters
            off03.meters.add(wh)        #electric
            off03.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(off03,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-03-photo.JPG')
            set_file_field(off03,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-03-nameplate.JPG')

            off04 = PackageUnit(name = 'OFF-04',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'offices behind R.C./hall',
                                age = None,
                                make = 'Lennox',
                                model = 'HP29-036-1Y',
                                serial_number = '5899A 15307',
                                nameplate_tons = Decimal(3.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(11.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.1),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            off04.save()
            #post-creation actions:
            #--connect to buildings
            off04.buildings.add(West)
            #--connect to spaces
            off04.spaces.add(offices_space)
            #--connect to meters
            off04.meters.add(wh)       #electric
            off04.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(off04,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-04-photo.JPG')
            set_file_field(off04,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-04-nameplate.JPG')

            off05 = PackageUnit(name = 'OFF-05',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'Bruce/conference room/Seth/Resource Center',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511--',
                                serial_number = '1704G10322',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            off05.save()
            #post-creation actions:
            #--connect to buildings
            off05.buildings.add(West)
            #--connect to spaces
            off05.spaces.add(offices_space)
            #--connect to meters
            off05.meters.add(wh)       #electric
            off05.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(off05,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-05-photo.JPG')
            set_file_field(off05,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-05-nameplate.JPG')

            off06 = PackageUnit(name = 'OFF-06',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'Pharmacy',
                                age = None,
                                make = 'Lennox',
                                model = 'KGA048S4DH1G',
                                serial_number = '5610M05717',
                                nameplate_tons = Decimal(4.0),
                                nameplate_EER = Decimal(11.0),
                                nameplate_MBH_in = Decimal(150.0),
                                nameplate_MBH_out = Decimal(120.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(6.2),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(2.0),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.1),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            off06.save()
            #post-creation actions:
            #--connect to buildings
            off06.buildings.add(West)
            #--connect to spaces
            off06.spaces.add(offices_space)
            #--connect to meters
            off05.meters.add(wh)       #electric
            off06.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(off06,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-06-photo.JPG')
            set_file_field(off06,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/OFF-06-nameplate.JPG')

            cli01 = PackageUnit(name = 'CLI-01',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'back hall exam rooms',
                                age = None,
                                make = 'Lennox',
                                model = 'KGA036S4DM1G',
                                serial_number = '5610J08145',
                                nameplate_tons = Decimal(3.0),
                                nameplate_EER = Decimal(10.7),
                                nameplate_MBH_in = Decimal(105.0),
                                nameplate_MBH_out = Decimal(84.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(5.8),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(2.0),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.1),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            cli01.save()
            #post-creation actions:
            #--connect to buildings
            cli01.buildings.add(West)
            #--connect to spaces
            cli01.spaces.add(clinic_space)
            #--connect to meters
            cli01.meters.add(clinic)    #electric
            cli01.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(cli01,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-01-photo.JPG')
            set_file_field(cli01,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-01-nameplate.JPG')

            cli02 = PackageUnit(name = 'CLI-02',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'left hall/dental/reception',
                                age = None,
                                make = 'Lennox',
                                model = 'KGA048S4DH1G',
                                serial_number = '5610M05716',
                                nameplate_tons = Decimal(4.0),
                                nameplate_EER = Decimal(11.0),
                                nameplate_MBH_in = Decimal(150.0),
                                nameplate_MBH_out = Decimal(120.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(6.2),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(2.0),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.1),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            cli02.save()
            #post-creation actions:
            #--connect to buildings
            cli02.buildings.add(West)
            #--connect to spaces
            cli02.spaces.add(clinic_space)
            #--connect to meters
            cli02.meters.add(clinic)    #electric
            cli02.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(cli02,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-02-photo.JPG')
            set_file_field(cli02,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-02-nameplate.JPG')

            cli03 = PackageUnit(name = 'CLI-03',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'waiting area/front bathroom',
                                age = None,
                                make = 'Lennox',
                                model = 'KGA060S4DH2G',
                                serial_number = '5610G15564',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = Decimal(11.2),
                                nameplate_MBH_in = Decimal(150.0),
                                nameplate_MBH_out = Decimal(120.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(8.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(2.5),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.3),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            cli03.save()
            #post-creation actions:
            #--connect to buildings
            cli03.buildings.add(West)
            #--connect to spaces
            cli03.spaces.add(clinic_space)
            #--connect to meters
            cli03.meters.add(clinic)    #electric
            cli03.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(cli03,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-03-photo.JPG')
            set_file_field(cli03,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-03-nameplate.JPG')

            cli04 = PackageUnit(name = 'CLI-04',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'conference room/counseling room',
                                age = None,
                                make = 'Lennox',
                                model = 'KGA048S4DH1G',
                                serial_number = '5610F07737',
                                nameplate_tons = Decimal(4.0),
                                nameplate_EER = Decimal(11.0),
                                nameplate_MBH_in = Decimal(150.0),
                                nameplate_MBH_out = Decimal(120.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(6.2),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(2.0),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.1),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            cli04.save()
            #post-creation actions:
            #--connect to buildings
            cli04.buildings.add(West)
            #--connect to spaces
            cli04.spaces.add(clinic_space)
            #--connect to meters
            cli04.meters.add(clinic)    #electric
            cli04.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(cli04,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-04-photo.JPG')
            set_file_field(cli04,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-04-nameplate.JPG')

            cli05 = PackageUnit(name = 'CLI-05',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'offices/back bathrooms/break room',
                                age = None,
                                make = 'Lennox',
                                model = 'KGA060S4DH2G',
                                serial_number = '5610G05233',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = Decimal(11.2),
                                nameplate_MBH_in = Decimal(150.0),
                                nameplate_MBH_out = Decimal(120.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(8.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(2.5),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.3),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            cli05.save()
            #post-creation actions:
            #--connect to buildings
            cli05.buildings.add(West)
            #--connect to spaces
            cli05.spaces.add(clinic_space)
            #--connect to meters
            cli05.meters.add(clinic)    #electric
            cli05.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(cli05,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-05-photo.JPG')
            set_file_field(cli05,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/CLI-05-nameplate.JPG')

            ev101 = PackageUnit(name = 'EV1-01',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'left offices/hall',
                                age = None,
                                make = 'Lennox',
                                model = 'TGA150S2BM1G',
                                serial_number = '5608G15333',
                                nameplate_tons = Decimal(11.5),
                                nameplate_EER = Decimal(9.5),
                                nameplate_MBH_in = Decimal(180.0),
                                nameplate_MBH_out = Decimal(144.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(9.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(7.6),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev101.save()
            #post-creation actions:
            #--connect to buildings
            ev101.buildings.add(West)
            #--connect to spaces
            ev101.spaces.add(EdenI_space)
            #--connect to meters
            ev101.meters.add(e1)        #electric
            ev101.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(ev101,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-01-photo.JPG')
            set_file_field(ev101,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-01-nameplate.JPG')

            ev102 = PackageUnit(name = 'EV1-02',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'back left hall/dorms',
                                age = None,
                                make = 'Lennox',
                                model = 'TGA150S2BM1G',
                                serial_number = '5608G05219',
                                nameplate_tons = Decimal(11.5),
                                nameplate_EER = Decimal(9.5),
                                nameplate_MBH_in = Decimal(180.0),
                                nameplate_MBH_out = Decimal(144.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(9.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(7.6),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev102.save()
            #post-creation actions:
            #--connect to buildings
            ev102.buildings.add(West)
            #--connect to spaces
            ev102.spaces.add(EdenI_space)
            #--connect to meters
            ev102.meters.add(e1)        #electric
            ev102.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(ev102,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-02-photo.JPG')
            set_file_field(ev102,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-02-nameplate.jp')

            ev103 = PackageUnit(name = 'EV1-03',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'common area/FML',
                                age = None,
                                make = 'Lennox',
                                model = 'TGA090S2BM1G',
                                serial_number = '5608F06581',
                                nameplate_tons = Decimal(7.5),
                                nameplate_EER = Decimal(10.1),
                                nameplate_MBH_in = Decimal(180.0),
                                nameplate_MBH_out = Decimal(144.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(6.4),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(3.4),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.3),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev103.save()
            #post-creation actions:
            #--connect to buildings
            ev103.buildings.add(West)
            #--connect to spaces
            ev103.spaces.add(EdenI_space)
            #--connect to meters
            ev103.meters.add(e1)        #electric
            ev103.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(ev103,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-03-photo.JPG')
            set_file_field(ev103,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-03-nameplate.JPG')

            ev104 = PackageUnit(name = 'EV1-04',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'back right hall',
                                age = None,
                                make = 'Lennox',
                                model = 'TGA102S2BM1G',
                                serial_number = '5607M01370',
                                nameplate_tons = Decimal(8.3),
                                nameplate_EER = Decimal(10.1),
                                nameplate_MBH_in = Decimal(180.0),
                                nameplate_MBH_out = Decimal(144.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(7.1),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(3.4),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.3),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev104.save()
            #post-creation actions:
            #--connect to buildings
            ev104.buildings.add(West)
            #--connect to spaces
            ev104.spaces.add(EdenI_space)
            #--connect to meters
            ev104.meters.add(e1)        #electric
            ev104.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(ev104,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-04-photo.JPG')
            set_file_field(ev104,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-04-nameplate.JPG')

            ev105 = PackageUnit(name = 'EV1-05',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'right hall',
                                age = None,
                                make = 'Lennox',
                                model = 'TGA150S2BM1G',
                                serial_number = '5608H01253',
                                nameplate_tons = Decimal(11.5),
                                nameplate_EER = Decimal(9.5),
                                nameplate_MBH_in = Decimal(180.0),
                                nameplate_MBH_out = Decimal(144.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(9.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(7.6),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev105.save()
            #post-creation actions:
            #--connect to buildings
            ev105.buildings.add(West)
            #--connect to spaces
            ev105.spaces.add(EdenI_space)
            #--connect to meters
            ev105.meters.add(e1)        #electric
            ev105.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(ev105,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-05-photo.JPG')
            set_file_field(ev105,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-05-nameplate.JPG')

            ev106 = PackageUnit(name = 'EV1-06',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'common area',
                                age = None,
                                make = 'Lennox',
                                model = 'TGA090S2BM1G',
                                serial_number = '5608811495',
                                nameplate_tons = Decimal(7.5),
                                nameplate_EER = Decimal(10.1),
                                nameplate_MBH_in = Decimal(180.0),
                                nameplate_MBH_out = Decimal(144.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(6.4),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(3.4),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.3),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev106.save()
            #post-creation actions:
            #--connect to buildings
            ev106.buildings.add(West)
            #--connect to spaces
            ev106.spaces.add(EdenI_space)
            #--connect to meters
            ev106.meters.add(e1)        #electric
            ev106.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(ev106,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-06-photo.JPG')
            set_file_field(ev106,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-06-nameplate.JPG')

            ev107 = PackageUnit(name = 'EV1-07',
                                equipment_type = 'Package Unit',
                                location = 'West Bldg rooftop',
                                description = '',
                                serves = 'Fulton County offices',
                                age = None,
                                make = 'Carrier',
                                model = '48TMD008-A-501',
                                serial_number = '2004G20670',
                                nameplate_tons = Decimal(7.5),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(125.0),
                                nameplate_MBH_out = Decimal(100.0),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(14.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.8),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(2),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev107.save()
            #post-creation actions:
            #--connect to buildings
            ev107.buildings.add(West)
            #--connect to spaces
            ev107.spaces.add(EdenI_space)
            #--connect to meters
            ev107.meters.add(e1)        #electric
            ev107.meters.add(gas1300)   #gas
            #--load image files
            set_file_field(ev107,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-07-photo.JPG')
            set_file_field(ev107,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV1-07-nameplate.JPG')

            ev201 = PackageUnit(name = 'EV2-01',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'Room 3',
                                age = None,
                                make = 'Lennox',
                                model = 'THA048S2BN1G',
                                serial_number = '5609B01178',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = None,
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = None,
                                nameplate_f1_PH = None,
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev201.save()
            #post-creation actions:
            #--connect to buildings
            ev201.buildings.add(East)
            #--connect to spaces
            ev201.spaces.add(EdenII_space)
            #--connect to meters
            ev201.meters.add(e2)            #electric
            #--load image files
            set_file_field(ev201,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-01-photo.JPG')
            set_file_field(ev201,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-01-nameplate.JPG')

            ev202 = PackageUnit(name = 'EV2-02',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'Room 4',
                                age = None,
                                make = 'Lennox',
                                model = 'THA036S2BN1G',
                                serial_number = '5609B04467',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = None,
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = None,
                                nameplate_f1_PH = None,
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev202.save()
            #post-creation actions:
            #--connect to buildings
            ev202.buildings.add(East)
            #--connect to spaces
            ev202.spaces.add(EdenII_space)
            #--connect to meters
            ev202.meters.add(e2)            #electric
            #--load image files
            set_file_field(ev202,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-02-photo.JPG')
            set_file_field(ev202,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-02-nameplate.JPG')

            ev203 = PackageUnit(name = 'EV2-03',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'Common Area',
                                age = None,
                                make = 'Lennox',
                                model = 'THA036S2BN1G',
                                serial_number = '5609C09237',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(480.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(4.5),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = None,
                                nameplate_f1_PH = None,
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev203.save()
            #post-creation actions:
            #--connect to buildings
            ev203.buildings.add(East)
            #--connect to spaces
            ev203.spaces.add(EdenII_space)
            #--connect to meters
            ev203.meters.add(e2)            #electric
            #--load image files
            set_file_field(ev203,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-03-photo.JPG')
            set_file_field(ev203,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-03-nameplate.JPG')

            ev204 = PackageUnit(name = 'EV2-04',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'Room 2',
                                age = None,
                                make = 'Lennox',
                                model = 'THA060S2BN1G',
                                serial_number = '5609B04220',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = None,
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = None,
                                nameplate_f1_PH = None,
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev204.save()
            #post-creation actions:
            #--connect to buildings
            ev204.buildings.add(East)
            #--connect to spaces
            ev204.spaces.add(EdenII_space)
            #--connect to meters
            ev204.meters.add(e2)            #electric
            #--load image files
            set_file_field(ev204,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-04-photo.JPG')
            set_file_field(ev204,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-04-nameplate.JPG')

            ev205 = PackageUnit(name = 'EV2-05',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'Room 1/hall',
                                age = None,
                                make = 'Lennox',
                                model = 'THA048S2BN1G',
                                serial_number = '5609B01179',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = None,
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = None,
                                nameplate_f1_PH = None,
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            ev205.save()
            #post-creation actions:
            #--connect to buildings
            ev205.buildings.add(East)
            #--connect to spaces
            ev205.spaces.add(EdenII_space)
            #--connect to meters
            ev205.meters.add(e2)            #electric
            #--load image files
            set_file_field(ev205,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-05-photo.JPG')
            set_file_field(ev205,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/EV2-05-nameplate.JPG')

            vgd01 = PackageUnit(name = 'VGD-01',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'EV II overflow',
                                age = None,
                                make = 'Carrier',
                                model = '48TCDA07A2A5A0A0A0',
                                serial_number = '4510G10082',
                                nameplate_tons = Decimal(5.8),
                                nameplate_EER = Decimal(11.0),
                                nameplate_MBH_in = Decimal(72.0),
                                nameplate_MBH_out = Decimal(59.0),
                                nameplate_ng_eta = Decimal(0.82),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(19.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(7.5),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            vgd01.save()
            #post-creation actions:
            #--connect to buildings
            vgd01.buildings.add(East)
            #--connect to spaces
            vgd01.spaces.add(dorms_space)
            #--connect to meters
            vgd01.meters.add(east_main)    #electric
            vgd01.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(vgd01,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-01-photo.JPG')
            set_file_field(vgd01,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-01-nameplate.JPG')

            vgd02 = PackageUnit(name = 'VGD-02',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'left visiting group',
                                age = None,
                                make = 'Carrier',
                                model = '48TCDA07A2A5A0A0A0',
                                serial_number = '4510G10083',
                                nameplate_tons = Decimal(5.8),
                                nameplate_EER = Decimal(11.0),
                                nameplate_MBH_in = Decimal(72.0),
                                nameplate_MBH_out = Decimal(59.0),
                                nameplate_ng_eta = Decimal(0.82),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(19.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(7.5),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            vgd02.save()
            #post-creation actions:
            #--connect to buildings
            vgd02.buildings.add(East)
            #--connect to spaces
            vgd02.spaces.add(dorms_space)
            #--connect to meters
            vgd02.meters.add(east_main)    #electric
            vgd02.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(vgd02,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-02-photo.JPG')
            set_file_field(vgd02,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-02-nameplate.JPG')

            vgd03 = PackageUnit(name = 'VGD-03',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'right visiting group/sanctuary',
                                age = None,
                                make = 'Carrier',
                                model = '48TCDA07A2A5A0A0A0',
                                serial_number = '4510G10079',
                                nameplate_tons = Decimal(5.8),
                                nameplate_EER = Decimal(11.0),
                                nameplate_MBH_in = Decimal(72.0),
                                nameplate_MBH_out = Decimal(59.0),
                                nameplate_ng_eta = Decimal(0.82),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(19.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(7.5),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            vgd03.save()
            #post-creation actions:
            #--connect to buildings
            vgd03.buildings.add(East)
            #--connect to spaces
            vgd03.spaces.add(dorms_space)
            #--connect to meters
            vgd03.meters.add(east_main)    #electric
            vgd03.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(vgd03,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-03-photo.JPG')
            set_file_field(vgd03,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-03-nameplate.JPG')

            vgd04 = PackageUnit(name = 'VGD-04',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'lounge/sanctuary',
                                age = None,
                                make = 'Carrier',
                                model = '48TCDA07A2A5A0A0A0',
                                serial_number = '4510G10084',
                                nameplate_tons = Decimal(5.8),
                                nameplate_EER = Decimal(11.0),
                                nameplate_MBH_in = Decimal(72.0),
                                nameplate_MBH_out = Decimal(59.0),
                                nameplate_ng_eta = Decimal(0.82),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(19.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(7.5),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            vgd04.save()
            #post-creation actions:
            #--connect to buildings
            vgd04.buildings.add(East)
            #--connect to spaces
            vgd04.spaces.add(dorms_space)
            #--connect to meters
            vgd04.meters.add(east_main)    #electric
            vgd04.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(vgd04,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-04-photo.JPG')
            set_file_field(vgd04,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/VGD-04-nameplate.JPG')

            kdh01 = PackageUnit(name = 'KDH-01',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'dining behind bay',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '2207G50292',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh01.save()
            #post-creation actions:
            #--connect to buildings
            kdh01.buildings.add(East)
            #--connect to spaces
            kdh01.spaces.add(kitchen_space)
            kdh01.spaces.add(dining_space)
            #--connect to meters
            kdh01.meters.add(east_main)    #electric
            kdh01.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh01,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-01-photo.JPG')
            set_file_field(kdh01,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-01-nameplate.JPG')

            kdh02 = PackageUnit(name = 'KDH-02',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'back left dining area',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '1807G20349',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh02.save()
            #post-creation actions:
            #--connect to buildings
            kdh02.buildings.add(East)
            #--connect to spaces
            kdh02.spaces.add(kitchen_space)
            kdh02.spaces.add(dining_space)
            #--connect to meters
            kdh02.meters.add(east_main)    #electric
            kdh02.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh02,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-02-photo.JPG')
            set_file_field(kdh02,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-02-nameplate.JPG')

            kdh03 = PackageUnit(name = 'KDH-03',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'left dining area',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '1807G10244',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh03.save()
            #post-creation actions:
            #--connect to buildings
            kdh03.buildings.add(East)
            #--connect to spaces
            kdh03.spaces.add(kitchen_space)
            kdh03.spaces.add(dining_space)
            #--connect to meters
            kdh03.meters.add(east_main)    #electric
            kdh03.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh03,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-03-photo.JPG')
            set_file_field(kdh03,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-03-nameplate.jp')

            kdh04 = PackageUnit(name = 'KDH-04',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'kitchen',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '2507G20353',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh04.save()
            #post-creation actions:
            #--connect to buildings
            kdh04.buildings.add(East)
            #--connect to spaces
            kdh04.spaces.add(kitchen_space)
            kdh04.spaces.add(dining_space)
            #--connect to meters
            kdh04.meters.add(east_main)    #electric
            kdh04.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh04,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-04-photo.JPG')
            set_file_field(kdh04,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-04-nameplate.JPG')

            kdh05 = PackageUnit(name = 'KDH-05',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'kitchen office/storage',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '1807G10242',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh05.save()
            #post-creation actions:
            #--connect to buildings
            kdh05.buildings.add(East)
            #--connect to spaces
            kdh05.spaces.add(kitchen_space)
            kdh05.spaces.add(dining_space)
            #--connect to meters
            kdh05.meters.add(east_main)    #electric
            kdh05.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh05,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-05-photo.JPG')
            set_file_field(kdh05,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-05-nameplate.JPG')

            kdh06 = PackageUnit(name = 'KDH-06',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'central dining area',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '1707G40214',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh06.save()
            #post-creation actions:
            #--connect to buildings
            kdh06.buildings.add(East)
            #--connect to spaces
            kdh06.spaces.add(kitchen_space)
            kdh06.spaces.add(dining_space)
            #--connect to meters
            kdh06.meters.add(east_main)    #electric
            kdh06.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh06,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-06-photo.JPG')
            set_file_field(kdh06,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-06-nameplate.JPG')

            kdh07 = PackageUnit(name = 'KDH-07',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'left front dining area',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '2207G20239',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh07.save()
            #post-creation actions:
            #--connect to buildings
            kdh07.buildings.add(East)
            #--connect to spaces
            kdh07.spaces.add(kitchen_space)
            kdh07.spaces.add(dining_space)
            #--connect to meters
            kdh07.meters.add(east_main)    #electric
            kdh07.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh07,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-07-photo.JPG')
            set_file_field(kdh07,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-07-nameplate.JPG')

            kdh08 = PackageUnit(name = 'KDH-08',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'bathrooms',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '2404G40183',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh08.save()
            #post-creation actions:
            #--connect to buildings
            kdh08.buildings.add(East)
            #--connect to spaces
            kdh08.spaces.add(kitchen_space)
            kdh08.spaces.add(dining_space)
            #--connect to meters
            kdh08.meters.add(east_main)    #electric
            kdh08.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh08,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-08-photo.JPG')
            set_file_field(kdh08,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-08-nameplate.JPG')

            kdh09 = PackageUnit(name = 'KDH-09',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'right central dining area',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '3403G20210',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh09.save()
            #post-creation actions:
            #--connect to buildings
            kdh09.buildings.add(East)
            #--connect to spaces
            kdh09.spaces.add(kitchen_space)
            kdh09.spaces.add(dining_space)
            #--connect to meters
            kdh09.meters.add(east_main)    #electric
            kdh09.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh09,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-09-photo.JPG')
            set_file_field(kdh09,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-09-nameplate.JPG')

            kdh10 = PackageUnit(name = 'KDH-10',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'right front dining area',
                                age = None,
                                make = 'Carrier',
                                model = '48TFD006-A-511',
                                serial_number = '2404G40181',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(74.0),
                                nameplate_MBH_out = Decimal(59.2),
                                nameplate_ng_eta = Decimal(0.80),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(3),
                                nameplate_e1_FLA = Decimal(5.2),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh10.save()
            #post-creation actions:
            #--connect to buildings
            kdh10.buildings.add(East)
            #--connect to spaces
            kdh10.spaces.add(kitchen_space)
            kdh10.spaces.add(dining_space)
            #--connect to meters
            kdh10.meters.add(east_main)    #electric
            kdh10.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(kdh10,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-10-photo.JPG')
            set_file_field(kdh10,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-10-nameplate.JPG')

            kdh11 = PackageUnit(name = 'KDH-11',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'most likely walk-in freezer condensing unit',
                                age = None,
                                make = 'Heatcraft',
                                model = 'MOZ055L63CF',
                                serial_number = 'T06F 04439',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(17.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(3.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh11.save()
            #post-creation actions:
            #--connect to buildings
            kdh11.buildings.add(East)
            #--connect to spaces
            kdh11.spaces.add(kitchen_space)
            kdh11.spaces.add(dining_space)
            #--connect to meters
            kdh11.meters.add(east_main)    #electric
            #--load image files
            set_file_field(kdh11,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-11-photo.JPG')
            set_file_field(kdh11,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-11-nameplate.JPG')

            kdh12 = PackageUnit(name = 'KDH-12',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'most likely walk-in cooler condensing unit',
                                age = None,
                                make = 'Heatcraft',
                                model = 'MOH029M23C',
                                serial_number = 'T07M 00203',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(2),
                                nameplate_c1_RLA = Decimal(9.9),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(0.5),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh12.save()
            #post-creation actions:
            #--connect to buildings
            kdh12.buildings.add(East)
            #--connect to spaces
            kdh12.spaces.add(kitchen_space)
            kdh12.spaces.add(dining_space)
            #--connect to meters
            kdh12.meters.add(east_main)    #electric
            #--load image files
            set_file_field(kdh12,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-12-photo.JPG')
            set_file_field(kdh12,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-12-nameplate.JPG')

            kdh13 = PackageUnit(name = 'KDH-13',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'most likely vent hood or other kitchen exhaust',
                                age = None,
                                make = 'Cook',
                                model = '150KSP-B',
                                serial_number = '050S930748-0070005901',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = None,
                                nameplate_c1_RLA = None,
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(3),
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh13.save()
            #post-creation actions:
            #--connect to buildings
            kdh13.buildings.add(East)
            #--connect to spaces
            kdh13.spaces.add(kitchen_space)
            kdh13.spaces.add(dining_space)
            #--connect to meters
            kdh13.meters.add(east_main)    #electric
            #--load image files
            set_file_field(kdh13,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-13-photo.JPG')
            set_file_field(kdh13,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-13-nameplate.JPG')

            kdh14 = PackageUnit(name = 'KDH-14',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'most likely vent hood or other kitchen exhaust',
                                age = None,
                                make = 'Cook',
                                model = '225V9B',
                                serial_number = '050S930748-00/0003601',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = None,
                                nameplate_c1_RLA = None,
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(3),
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh14.save()
            #post-creation actions:
            #--connect to buildings
            kdh14.buildings.add(East)
            #--connect to spaces
            kdh14.spaces.add(kitchen_space)
            kdh14.spaces.add(dining_space)
            #--connect to meters
            kdh14.meters.add(east_main)    #electric
            #--load image files
            set_file_field(kdh14,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-14-photo.JPG')
            set_file_field(kdh14,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-14-nameplate.JPG')

            kdh15 = PackageUnit(name = 'KDH-15',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'most likely vent hood or other kitchen exhaust',
                                age = None,
                                make = 'Cook',
                                model = '100C15DH',
                                serial_number = '050S930748-00/0004801',
                                nameplate_tons = None,
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = None,
                                nameplate_c1_RLA = None,
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = None,
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            kdh15.save()
            #post-creation actions:
            #--connect to buildings
            kdh15.buildings.add(East)
            #--connect to spaces
            kdh15.spaces.add(kitchen_space)
            kdh15.spaces.add(dining_space)
            #--connect to meters
            kdh15.meters.add(east_main)    #electric
            #--load image files
            set_file_field(kdh15,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-15-photo.JPG')
            set_file_field(kdh15,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/KDH-15-nameplate.JPG')

            gyc01 = PackageUnit(name = 'GYC-01',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'weight room/Art Room',
                                age = None,
                                make = 'Goodman',
                                model = 'CPG0601403DXXXBA',
                                serial_number = '0903666056',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(138.0),
                                nameplate_MBH_out = Decimal(110.0),
                                nameplate_ng_eta = Decimal(0.797),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(7.6),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            gyc01.save()
            #post-creation actions:
            #--connect to buildings
            gyc01.buildings.add(East)
            #--connect to spaces
            gyc01.spaces.add(gym_space)
            gyc01.spaces.add(school_space)
            #--connect to meters
            gyc01.meters.add(east_main)    #electric
            gyc01.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(gyc01,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-01-photo.JPG')
            set_file_field(gyc01,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-01-nameplate.JPG')

            gyc02 = PackageUnit(name = 'GYC-02',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'gym/CORE',
                                age = None,
                                make = 'Goodman',
                                model = 'CPG0601403DXXXBA',
                                serial_number = '0903666057',
                                nameplate_tons = Decimal(5.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = Decimal(138.0),
                                nameplate_MBH_out = Decimal(110.0),
                                nameplate_ng_eta = Decimal(0.797),
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(16.0),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = Decimal(1),
                                nameplate_e1_PH = Decimal(1),
                                nameplate_e1_FLA = Decimal(7.6),
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            gyc02.save()
            #post-creation actions:
            #--connect to buildings
            gyc02.buildings.add(East)
            #--connect to spaces
            gyc02.spaces.add(gym_space)
            gyc02.spaces.add(school_space)
            #--connect to meters
            gyc02.meters.add(east_main)    #electric
            gyc02.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(gyc02,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-02-photo.JPG')
            set_file_field(gyc02,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-02-nameplate.JPG')

            gyc03 = PackageUnit(name = 'GYC-03',
                                equipment_type = 'Package Unit',
                                location = 'East Bldg rooftop',
                                description = '',
                                serves = 'classrooms',
                                age = None,
                                make = 'Carrier',
                                model = '25HBC348A500',
                                serial_number = '3610E05804',
                                nameplate_tons = Decimal(4.0),
                                nameplate_EER = None,
                                nameplate_MBH_in = None,
                                nameplate_MBH_out = None,
                                nameplate_ng_eta = None,
                                nameplate_V = Decimal(230.0),
                                nameplate_phase = Decimal(3),
                                nameplate_pf = None,
                                nameplate_RFC = None,
                                nameplate_c1_QTY = Decimal(1),
                                nameplate_c1_RLA = Decimal(13.7),
                                nameplate_c1_PH = None,
                                nameplate_c2_QTY = None,
                                nameplate_c2_RLA = None,
                                nameplate_c2_PH = None,
                                nameplate_c3_QTY = None,
                                nameplate_c3_RLA = None,
                                nameplate_c3_PH = None,
                                nameplate_e1_QTY = None,
                                nameplate_e1_PH = None,
                                nameplate_e1_FLA = None,
                                nameplate_e2_QTY = None,
                                nameplate_e2_PH = None,
                                nameplate_e2_FLA = None,
                                nameplate_f1_QTY = Decimal(1),
                                nameplate_f1_PH = Decimal(1),
                                nameplate_f1_FLA = Decimal(1.4),
                                nameplate_f2_QTY = None,
                                nameplate_f2_PH = None,
                                nameplate_f2_FLA = None,
                                dP_fan_max = None,
                                dP_fan_min = None,
                                SAF_max = None,
                                SAF_min = None,
                                speed_min = None,
                                T_max = None,
                                T_min = None,
                                d0 = None,
                                d1 = None,
                                d2 = None,
                                m0 = None,
                                m1 = None,
                                m2 = None,
                                m3 = None,
                                f0 = None,
                                f1 = None,
                                f2 = None,
                                e0 = None,
                                e1 = None,
                                e2 = None,
                                SCOC = None,
                                SCUN = None,
                                SHOC = None,
                                SHUN = None,
                                SRFC = None,
                                )
            gyc03.save()
            #post-creation actions:
            #--connect to buildings
            gyc03.buildings.add(East)
            #--connect to spaces
            gyc03.spaces.add(school_space)
            #--connect to meters
            gyc03.meters.add(east_main)    #electric            
            gyc03.meters.add(gas1290)       #gas
            #--load image files
            set_file_field(gyc03,
                            'image_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-03-photo.JPG')
            set_file_field(gyc03,
                            'nameplate_file',
                            STATIC_URL + 'upload_files/NewAccount/EquipmentImages/GYC-03-nameplate.JPG')

        except:
            print 'Failed to create new Equipment.'


    ###---Measures
        try:
            em1_elec = EfficiencyMeasure(name = 'Controls on 23 RTUs (electric)',
                                            when = datetime(2014,3,1,tzinfo=UTC),
                                            utility_type = 'electricity',
                                            units = 'kW,kWh',
                                            annual_consumption_savings = Decimal(58000.0),
                                            peak_demand_savings = Decimal(0.0),
                                            annual_cost_savings = Decimal(7500.0),
                                            percent_uncertainty = Decimal(0.05),
                                            percent_cool = Decimal(0.47),
                                            percent_heat = Decimal(0.53),
                                            percent_flat = Decimal(0.0),
                                            percent_fixed = Decimal(0.0),
                                            
                                            weather_station = ws,
                                            )
            em1_elec.save()
            #post-creation actions:
            #--apportion annual savings numbers to individual months
            em1_elec.apportion_savings()
            #--create intermediate models to assign to Meters
            emma1 = EMMeterApportionment(efficiency_measure = em1_elec,
                                         meter = e2,
                                         assigned_fraction = Decimal(0.58))
            emma1.save()
            emma2 = EMMeterApportionment(efficiency_measure = em1_elec,
                                         meter = east_main,
                                         assigned_fraction = Decimal(0.42))
            emma2.save()
            #--create intermediate models to assign to Equipment
            for equip in [ev201,ev202,ev203,ev204,ev205]:
                emeaX = EMEquipmentApportionment(efficiency_measure = em1_elec,
                                             equipment = equip,
                                             assigned_fraction = Decimal(0.116))
                emeaX.save()
                
                for equip in [vgd01,vgd02,vgd03,vgd04,kdh01,kdh02,kdh03,kdh04,kdh05,kdh06,
                              kdh07,kdh08,kdh09,kdh10,gyc01,gyc02,gyc03]:
                    emeaX = EMEquipmentApportionment(efficiency_measure = em1_elec,
                                                 equipment = equip,
                                                 assigned_fraction = Decimal(0.0247))
                    emeaX.save()
    
                
            em1_gas = EfficiencyMeasure(name = 'Controls on 23 RTUs (gas)',
                                        when = datetime(2014,3,1,tzinfo=UTC),
                                        utility_type = 'natural gas',
                                        units = 'therms/h,therms',
                                        annual_consumption_savings = Decimal(1500.0),
                                        peak_demand_savings = Decimal(0.0),
                                        annual_cost_savings = Decimal(1100.0),
                                        percent_uncertainty = Decimal(0.05),
                                        percent_cool = Decimal(0.0),
                                        percent_heat = Decimal(1.0),
                                        percent_flat = Decimal(0.0),
                                        percent_fixed = Decimal(0.0),
                                        
                                        weather_station = ws,
                                        )
            em1_gas.save()
            #post-creation actions:
            #--apportion annual savings numbers to individual months
            em1_gas.apportion_savings()
            #--create intermediate models to assign to Meters
            emma1 = EMMeterApportionment(efficiency_measure = em1_gas,
                                         meter = gas1290,
                                         assigned_fraction = Decimal(1.0))
            emma1.save()
            #--create intermediate models to assign to Equipment
            for equip in [vgd01,vgd02,vgd03,vgd04,kdh01,kdh02,kdh03,kdh04,kdh05,kdh06,
                          kdh07,kdh08,kdh09,kdh10,gyc01,gyc02,gyc03]:
                emeaX = EMEquipmentApportionment(efficiency_measure = em1_elec,
                                             equipment = equip,
                                             assigned_fraction = Decimal(0.0588))
                emeaX.save()
            
        except:
            print 'Failed to create new Measures.'
