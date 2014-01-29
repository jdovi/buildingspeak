from django.core.management.base import BaseCommand

import urllib
from decimal import Decimal

from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import User

from BuildingSpeak.settings import STATIC_URL

from BuildingSpeakApp.models import UserProfile, Account, Building, Space, Meter, Equipment
from BuildingSpeakApp.models import RooftopUnit
from BuildingSpeakApp.models import MeterConsumptionModel, MeterPeakDemandModel
from BuildingSpeakApp.models import SpaceMeterApportionment, BuildingMeterApportionment
from BuildingSpeakApp.models import EfficiencyMeasure, EMMeterApportionment, EMEquipmentApportionment
from BuildingSpeakApp.models import WeatherStation, Utility
from BuildingSpeakApp.models import GAPowerPandL, InfiniteEnergyGAGas, CityOfATLWWW


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
                organization = 'City of Refuge, Inc. - ATL'
                )
            userprofile1.save()
            
            #post-creation actions
            #--load image file
            file_url = STATIC_URL + 'temporary_files/user1_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            userprofile1.__setattr__('image_file', file_obj)
            userprofile1.save()
        except:
            print 'Failed to create new UserProfiles.'
        
    ###---Account
        try:
            acct1 = Account(
            name = 'City of Refuge, Inc. - ATL',
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
            file_url = STATIC_URL + 'temporary_files/account1_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            acct1.__setattr__('image_file', file_obj)
            acct1.save()
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
                square_footage = 49800,
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
            file_url = STATIC_URL + 'temporary_files/east_bldg_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            East.__setattr__('image_file', file_obj)
            East.save()
            
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
                square_footage = 152000,
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
            file_url = STATIC_URL + 'temporary_files/west_bldg_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            West.__setattr__('image_file', file_obj)
            West.save()
        except:
            print 'Failed to create new Buildings.'
        
    ###---Spaces
        try:
            EdenI_space = Space(
                name = 'Eden I',
                building = West,
                square_footage = 36000,
                max_occupancy = None,
                space_type = 'Dormitory',
                EIA_type = 'Lodging',
                ESPM_type = 'Dormitory / Residence Hall',
                )
            EdenI_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/EdenI_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            EdenI_space.__setattr__('image_file', file_obj)
            EdenI_space.save()
            
            kitchen_space = Space(
                name = '180 Kitchen',
                building = East,
                square_footage = 4500,
                max_occupancy = None,
                space_type = 'Dining: Family',
                EIA_type = 'Food Service',
                ESPM_type = 'Other',
                )
            kitchen_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/kitchen_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            kitchen_space.__setattr__('image_file', file_obj)
            kitchen_space.save()
            
            dining_space = Space(
                name = 'Dining Area',
                building = East,
                square_footage = 11500,
                max_occupancy = None,
                space_type = 'Dining: Family',
                EIA_type = 'Food Service',
                ESPM_type = 'Other',
                )
            dining_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/dining_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            dining_space.__setattr__('image_file', file_obj)
            dining_space.save()
            
            compATL_space = Space(
                name = 'Compassion ATL',
                building = West,
                square_footage = 36000,
                max_occupancy = None,
                space_type = 'Warehouse',
                EIA_type = 'Warehouse and Storage',
                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
                )
            compATL_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/compATL_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            compATL_space.__setattr__('image_file', file_obj)
            compATL_space.save()
            
            EdenII_space = Space(
                name = 'Eden II',
                building = East,
                square_footage = 9700,
                max_occupancy = None,
                space_type = 'Dormitory',
                EIA_type = 'Lodging',
                ESPM_type = 'Dormitory / Residence Hall',
                )
            EdenII_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/EdenII_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            EdenII_space.__setattr__('image_file', file_obj)
            EdenII_space.save()
            
            dorms_space = Space(
                name = 'Dorms',
                building = East,
                square_footage = 11000,
                max_occupancy = None,
                space_type = 'Dormitory',
                EIA_type = 'Lodging',
                ESPM_type = 'Dormitory / Residence Hall',
                )
            dorms_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/dorms_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            dorms_space.__setattr__('image_file', file_obj)
            dorms_space.save()
            
            gym_space = Space(
                name = 'Gym',
                building = East,
                square_footage = 8700,
                max_occupancy = None,
                space_type = 'Gymnasium',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            gym_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/gym_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            gym_space.__setattr__('image_file', file_obj)
            gym_space.save()
            
            clinic_space = Space(
                name = 'Clinic',
                building = West,
                square_footage = 8700,
                max_occupancy = None,
                space_type = 'Health Care Clinic',
                EIA_type = 'Health Care - Outpatient',
                ESPM_type = 'Medical Office',
                )
            clinic_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/clinic_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            clinic_space.__setattr__('image_file', file_obj)
            clinic_space.save()
            
            offices_space = Space(
                name = 'Offices',
                building = West,
                square_footage = 10400,
                max_occupancy = None,
                space_type = 'Office',
                EIA_type = 'Office',
                ESPM_type = 'Office',
                )
            offices_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/offices_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            offices_space.__setattr__('image_file', file_obj)
            offices_space.save()
            
            playground_space = Space(
                name = 'Playground',
                building = West,
                square_footage = 4800,
                max_occupancy = None,
                space_type = 'Gymnasium',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            playground_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/playground_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            playground_space.__setattr__('image_file', file_obj)
            playground_space.save()
            
            school_space = Space(
                name = 'CORE',
                building = East,
                square_footage = 4400,
                max_occupancy = None,
                space_type = 'School/University',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            school_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/school_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            school_space.__setattr__('image_file', file_obj)
            school_space.save()
            
            unfinished_space = Space(
                name = 'Unfinished',
                building = West,
                square_footage = 44100,
                max_occupancy = None,
                space_type = 'Warehouse',
                EIA_type = 'Warehouse and Storage',
                ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
                )
            unfinished_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/unfinished_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            unfinished_space.__setattr__('image_file', file_obj)
            unfinished_space.save()
            
            newschool_space = Space(
                name = 'Bright Futures',
                building = West,
                square_footage = 7000,
                max_occupancy = None,
                space_type = 'School/University',
                EIA_type = 'Education',
                ESPM_type = 'K-12 School',
                )
            newschool_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/newschool_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            newschool_space.__setattr__('image_file', file_obj)
            newschool_space.save()
            
            newchurch_space = Space(
                name = 'Church',
                building = West,
                square_footage = 5000,
                max_occupancy = None,
                space_type = 'Religious Building',
                EIA_type = 'Religious Worship',
                ESPM_type = 'House of Worship',
                )
            newchurch_space.save()
            #post-creation actions:
            #--load image file
            file_url = STATIC_URL + 'temporary_files/newchurch_space_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            newchurch_space.__setattr__('image_file', file_obj)
            newchurch_space.save()
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
            
            #kitch = Meter(
            #    name = 'East Bldg',
            #    utility_type = 'electricity',
            #    location = 'loading dock area of bldg',
            #    serves = 'all of East Bldg except Eden II',
            #    units = 'kW,kWh',
            #    weather_station = ws,
            #    utility = gpc,
            #    rate_schedule = gpc_toueo7,
            #    account = acct1,
            #    make = 'unknown',
            #    model = 'unknown',
            #    serial_number = 'unknown',
            #    utility_account_number = '6126898026',
            #    utility_meter_number = '3081617',
            #    )
            #kitch.save()
            #post-creation actions:
            #--load image files
    #        file_url = STATIC_URL + 'temporary_files/kitch_image_file.jpg'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        kitch.__setattr__('image_file', file_obj)
    #        kitch.save()
    #        file_url = STATIC_URL + 'temporary_files/kitch_nameplate_file.jpg'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        kitch.__setattr__('nameplate_file', file_obj)
    #        kitch.save()
            #--load bill data file
    #        file_url = STATIC_URL + 'temporary_files/kitch_bill_data.csv'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        kitch.__setattr__('bill_data_file', file_obj)
    #        kitch.save()
    #        kitch.upload_bill_data(create_models_if_nonexistent=True)
    #        kitch.save()
    
            
            e1 = Meter(
                name = 'Eden I',
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
            file_url = STATIC_URL + 'temporary_files/e1_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            e1.__setattr__('image_file', file_obj)
            e1.save()
            file_url = STATIC_URL + 'temporary_files/e1_nameplate_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            e1.__setattr__('nameplate_file', file_obj)
            e1.save()
            #--load bill data file
            file_url = STATIC_URL + 'temporary_files/e1_bill_data.csv'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            e1.__setattr__('bill_data_file', file_obj)
            e1.save()
            e1.upload_bill_data(create_models_if_nonexistent = True)
            e1.save()
    
            e2 = Meter(
                name = 'Eden II',
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
            file_url = STATIC_URL + 'temporary_files/e2_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            e2.__setattr__('image_file', file_obj)
            e2.save()
            file_url = STATIC_URL + 'temporary_files/e2_nameplate_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            e2.__setattr__('nameplate_file', file_obj)
            e2.save()
            #--load bill data file
            file_url = STATIC_URL + 'temporary_files/e2_bill_data.csv'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            e2.__setattr__('bill_data_file', file_obj)
            e2.save()
            e2.upload_bill_data(create_models_if_nonexistent = True)
            e2.save()
            
            #wh = Meter(
            #    name = 'West Bldg south',
            #    utility_type = 'electricity',
            #    location = 'just south of Offices entrance on West Bldg',
            #    serves = 'Offices and Compassion ATL',
            #    units = 'kW,kWh',
            #    weather_station = ws,
            #    utility = gpc,
            #    rate_schedule = gpc_toueo7,
            #    account = acct1,
            #    make = 'unknown',
            #    model = 'unknown',
            #    serial_number = 'unknown',
            #    utility_account_number = '6168898017',
            #    utility_meter_number = '3081618',
            #    )
            #wh.save()
            #post-creation actions:
            #--load image files
    #        file_url = STATIC_URL + 'temporary_files/wh_image_file.jpg'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        wh.__setattr__('image_file', file_obj)
    #        wh.save()
    #        file_url = STATIC_URL + 'temporary_files/wh_nameplate_file.jpg'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        wh.__setattr__('nameplate_file', file_obj)
    #        wh.save()
            #--load bill data file
    #        file_url = STATIC_URL + 'temporary_files/wh_bill_data.csv'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        wh.__setattr__('bill_data_file', file_obj)
    #        wh.save()
    #        wh.upload_bill_data(create_models_if_nonexistent = True)
    #        wh.save()
            
            #playground = Meter(
            #    name = 'Playground',
            #    utility_type = 'electricity',
            #    location = 'south of Eden I entrance on West Bldg',
            #    serves = 'Playground and unfinished area between Eden I and Clinic',
            #    units = 'kW,kWh',
            #    weather_station = ws,
            #    utility = gpc,
            #    rate_schedule = gpc_gs7,
            #    account = acct1,
            #    make = 'unknown',
            #    model = 'unknown',
            #    serial_number = 'unknown',
            #    utility_account_number = '6147898017',
            #    utility_meter_number = '3081616',
            #    )
            #playground.save()
            #post-creation actions:
            #--load image files
    #        file_url = STATIC_URL + 'temporary_files/playground_image_file.jpg'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        playground.__setattr__('image_file', file_obj)
    #        playground.save()
    #        file_url = STATIC_URL + 'temporary_files/playground_nameplate_file.jpg'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        playground.__setattr__('nameplate_file', file_obj)
    #        playground.save()
            #--load bill data file
    #        file_url = STATIC_URL + 'temporary_files/playground_bill_data.csv'
    #        result = urllib.urlretrieve(file_url)
    #        file_obj = File(open(result[0]))
    #        playground.__setattr__('bill_data_file', file_obj)
    #        playground.save()
    #        playground.upload_bill_data(create_models_if_nonexistent = True)
    #        playground.save()
            
            clin = Meter(
                name = 'Clinic',
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
            clin.save()
            #post-creation actions:
            #--load image files
            file_url = STATIC_URL + 'temporary_files/clin_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            clin.__setattr__('image_file', file_obj)
            clin.save()
            file_url = STATIC_URL + 'temporary_files/clin_nameplate_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            clin.__setattr__('nameplate_file', file_obj)
            clin.save()
            #--load bill data file
            file_url = STATIC_URL + 'temporary_files/clin_bill_data.csv'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            clin.__setattr__('bill_data_file', file_obj)
            clin.save()
            clin.upload_bill_data(create_models_if_nonexistent = True)
            clin.save()
            
            gas1290 = Meter(
                name = 'East Bldg',
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
            file_url = STATIC_URL + 'temporary_files/gas1290_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            gas1290.__setattr__('image_file', file_obj)
            gas1290.save()
            file_url = STATIC_URL + 'temporary_files/gas1290_nameplate_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            gas1290.__setattr__('nameplate_file', file_obj)
            gas1290.save()
            #--load bill data file
            file_url = STATIC_URL + 'temporary_files/gas1290_bill_data.csv'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            gas1290.__setattr__('bill_data_file', file_obj)
            gas1290.save()
            gas1290.upload_bill_data(create_models_if_nonexistent = True)
            gas1290.save()
            
            gas1300 = Meter(
                name = 'West Bldg',
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
            file_url = STATIC_URL + 'temporary_files/gas1300_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            gas1300.__setattr__('image_file', file_obj)
            gas1300.save()
            file_url = STATIC_URL + 'temporary_files/gas1300_nameplate_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            gas1300.__setattr__('nameplate_file', file_obj)
            gas1300.save()
            #--load bill data file
            file_url = STATIC_URL + 'temporary_files/gas1300_bill_data.csv'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            gas1300.__setattr__('bill_data_file', file_obj)
            gas1300.save()
            gas1300.upload_bill_data(create_models_if_nonexistent = True)
            gas1300.save()
            
            simpson1290 = Meter(
                name = '1290 Simpson',
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
            file_url = STATIC_URL + 'temporary_files/simpson1290_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            simpson1290.__setattr__('image_file', file_obj)
            simpson1290.save()
            file_url = STATIC_URL + 'temporary_files/simpson1290_nameplate_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            simpson1290.__setattr__('nameplate_file', file_obj)
            simpson1290.save()
            #--load bill data file
            file_url = STATIC_URL + 'temporary_files/simpson1290_bill_data.csv'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            simpson1290.__setattr__('bill_data_file', file_obj)
            simpson1290.save()
            simpson1290.upload_bill_data(create_models_if_nonexistent = True)
            simpson1290.save()
            
            boone1300 = Meter(
                name = '1300 Boone',
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
            file_url = STATIC_URL + 'temporary_files/boone1300_image_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            boone1300.__setattr__('image_file', file_obj)
            boone1300.save()
            file_url = STATIC_URL + 'temporary_files/boone1300_nameplate_file.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            boone1300.__setattr__('nameplate_file', file_obj)
            boone1300.save()
            #--load bill data file
            file_url = STATIC_URL + 'temporary_files/boone1300_bill_data.csv'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0]))
            boone1300.__setattr__('bill_data_file', file_obj)
            boone1300.save()
            boone1300.upload_bill_data(create_models_if_nonexistent = True)
            boone1300.save()
        except:
            print 'Failed to create new Meters.'

