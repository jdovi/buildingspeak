from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        from django.contrib.auth.models import User
        from BuildingSpeakApp.models import UserProfile
        
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
        
        userprofile1 = UserProfile(
            user = user1,
            organization = 'City of Refuge, Inc. - ATL'
            )
        userprofile1.save()
        
        #post-creation actions: upload image to UserProfile.image_file
        
        from decimal import Decimal
        from django.utils import timezone
        from django.contrib.auth.models import User
        from BuildingSpeakApp.models import Account
        
        CoRATL = Account(
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
        CoRATL.save()
        
        CoRATL.users.add(User.objects.get(username = 'smucker'))
        CoRATL.users.add(User.objects.get(username = 'dashley'))
        
        #post-creation actions:
        #   1) if tracking, upload observed_file and/or provided_file and set tracking parameters in admin
        #   2) upload photo to Account.image_file
        
        from BuildingSpeakApp.models import Account, WeatherStation, Building
        
        acct = Account.objects.get(name = 'City of Refuge, Inc. - ATL')
        ws = WeatherStation.objects.get(name = 'ATL - downtown west')
        
        East = Building(
            name = 'East Bldg',
            building_type = 'Multi-Purpose',
            EIA_type = 'Other',
            ESPM_type = 'Other',
            account = acct,
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
        
        West = Building(
            name = 'West Bldg',
            building_type = 'Multi-Purpose',
            EIA_type = 'Other',
            ESPM_type = 'Other',
            account = acct,
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
        #   1) if tracking, upload observed_file and/or provided_file and set tracking parameters in admin
        #   2) upload photo to Building.image_file
        
        from BuildingSpeakApp.models import Space, Building, Account
        
        acct = Account.objects.get(name = 'City of Refuge, Inc. - ATL')
        east = Building.objects.filter(account = acct).get(name = 'East Bldg')
        west = Building.objects.filter(account = acct).get(name = 'West Bldg')
        
        EdenI = Space(
            name = 'Eden I',
            building = west,
            square_footage = 36000,
            max_occupancy = None,
            space_type = 'Dormitory',
            EIA_type = 'Lodging',
            ESPM_type = 'Dormitory / Residence Hall',
            )
        EdenI.save()
        
        kitchen = Space(
            name = '180 Kitchen',
            building = east,
            square_footage = 4500,
            max_occupancy = None,
            space_type = 'Dining: Family',
            EIA_type = 'Food Service',
            ESPM_type = 'Other',
            )
        kitchen.save()
        
        dining = Space(
            name = 'Dining Area',
            building = east,
            square_footage = 11500,
            max_occupancy = None,
            space_type = 'Dining: Family',
            EIA_type = 'Food Service',
            ESPM_type = 'Other',
            )
        dining.save()
        
        compATL = Space(
            name = 'Compassion ATL',
            building = west,
            square_footage = 36000,
            max_occupancy = None,
            space_type = 'Warehouse',
            EIA_type = 'Warehouse and Storage',
            ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
            )
        compATL.save()
        
        EdenII = Space(
            name = 'Eden II',
            building = east,
            square_footage = 9700,
            max_occupancy = None,
            space_type = 'Dormitory',
            EIA_type = 'Lodging',
            ESPM_type = 'Dormitory / Residence Hall',
            )
        EdenII.save()
        
        dorms = Space(
            name = 'Dorms',
            building = east,
            square_footage = 11000,
            max_occupancy = None,
            space_type = 'Dormitory',
            EIA_type = 'Lodging',
            ESPM_type = 'Dormitory / Residence Hall',
            )
        dorms.save()
        
        gym = Space(
            name = 'Gym',
            building = east,
            square_footage = 8700,
            max_occupancy = None,
            space_type = 'Gymnasium',
            EIA_type = 'Education',
            ESPM_type = 'K-12 School',
            )
        gym.save()
        
        clinic = Space(
            name = 'Clinic',
            building = west,
            square_footage = 8700,
            max_occupancy = None,
            space_type = 'Health Care Clinic',
            EIA_type = 'Health Care - Outpatient',
            ESPM_type = 'Medical Office',
            )
        clinic.save()
        
        offices = Space(
            name = 'Offices',
            building = west,
            square_footage = 10400,
            max_occupancy = None,
            space_type = 'Office',
            EIA_type = 'Office',
            ESPM_type = 'Office',
            )
        offices.save()
        
        playground = Space(
            name = 'Playground',
            building = west,
            square_footage = 4800,
            max_occupancy = None,
            space_type = 'Gymnasium',
            EIA_type = 'Education',
            ESPM_type = 'K-12 School',
            )
        playground.save()
        
        school = Space(
            name = 'CORE',
            building = east,
            square_footage = 4400,
            max_occupancy = None,
            space_type = 'School/University',
            EIA_type = 'Education',
            ESPM_type = 'K-12 School',
            )
        school.save()
        
        unfinished = Space(
            name = 'Unfinished',
            building = west,
            square_footage = 44100,
            max_occupancy = None,
            space_type = 'Warehouse',
            EIA_type = 'Warehouse and Storage',
            ESPM_type = 'Warehouse (Refrigerated or Unrefrigerated)',
            )
        unfinished.save()
        
        newschool = Space(
            name = 'Bright Futures',
            building = west,
            square_footage = 7000,
            max_occupancy = None,
            space_type = 'School/University',
            EIA_type = 'Education',
            ESPM_type = 'K-12 School',
            )
        newschool.save()
        
        newchurch = Space(
            name = 'Church',
            building = west,
            square_footage = 5000,
            max_occupancy = None,
            space_type = 'Religious Building',
            EIA_type = 'Religious Worship',
            ESPM_type = 'House of Worship',
            )
        newchurch.save()
        
        #post-creation actions:
        #   1) if tracking, upload observed_file and/or provided_file and set tracking parameters in admin
        #   2) upload photo to Space.image_file
        
        from BuildingSpeakApp.models import Meter, SpaceMeterApportionment,BuildingMeterApportionment
        from BuildingSpeakApp.models import Space, Building, Account, WeatherStation, Utility
        from BuildingSpeakApp.models import GAPowerPandL, GAPowerRider, InfiniteEnergyGAGas, CityOfATLWWW
        
        acct = Account.objects.get(name = 'City of Refuge, Inc. - ATL')
        ws = WeatherStation.objects.get(name = 'ATL - downtown west')
        
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
        
        east = Building.objects.filter(account = acct).get(name = 'East Bldg')
        west = Building.objects.filter(account = acct).get(name = 'West Bldg')
        
        edenII = Space.objects.filter(building__account = acct).filter(building = east).get(name = 'Eden II')
        dining = Space.objects.filter(building__account = acct).filter(building = east).get(name = 'Dining Area')
        dorms = Space.objects.filter(building__account = acct).filter(building = east).get(name = 'Dorms')
        gym = Space.objects.filter(building__account = acct).filter(building = east).get(name = 'Gym')
        school = Space.objects.filter(building__account = acct).filter(building = east).get(name = 'CORE')
        kitchen = Space.objects.filter(building__account = acct).filter(building = east).get(name = '180 Kitchen')
        unfinished = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Unfinished')
        newschool = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Bright Futures')
        newchurch = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Church')
        edenI = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Eden I')
        compATL = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Compassion ATL')
        clinic = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Clinic')
        offices = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Offices')
        playground = Space.objects.filter(building__account = acct).filter(building = west).get(name = 'Playground')
        
        #kitch = Meter(
        #    name = 'East Bldg',
        #    utility_type = 'electricity',
        #    location = 'loading dock area of bldg',
        #    serves = 'all of East Bldg except Eden II',
        #    units = 'kW,kWh',
        #    weather_station = ws,
        #    utility = gpc,
        #    rate_schedule = gpc_toueo7,
        #    account = acct,
        #    make = 'unknown',
        #    model = 'unknown',
        #    serial_number = 'unknown',
        #    utility_account_number = '6126898026',
        #    utility_meter_number = '3081617',
        #    )
        #kitch.save()
        
        e1 = Meter(
            name = 'Eden I',
            utility_type = 'electricity',
            location = 'northwest corner of West Bldg',
            serves = 'Eden I',
            units = 'kW,kWh',
            weather_station = ws,
            utility = gpc,
            rate_schedule = gpc_plm8_sec_in,
            account = acct,
            make = 'unknown',
            model = 'unknown',
            serial_number = 'unknown',
            utility_account_number = '0437031108',
            utility_meter_number = '3081619',
            )
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
            account = acct,
            make = 'unknown',
            model = 'unknown',
            serial_number = 'unknown',
            utility_account_number = '3244865006',
            utility_meter_number = '3179180',
            )
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
        #    account = acct,
        #    make = 'unknown',
        #    model = 'unknown',
        #    serial_number = 'unknown',
        #    utility_account_number = '6168898017',
        #    utility_meter_number = '3081618',
        #    )
        #wh.save()
        
        #playground = Meter(
        #    name = 'Playground',
        #    utility_type = 'electricity',
        #    location = 'south of Eden I entrance on West Bldg',
        #    serves = 'Playground and unfinished area between Eden I and Clinic',
        #    units = 'kW,kWh',
        #    weather_station = ws,
        #    utility = gpc,
        #    rate_schedule = gpc_gs7,
        #    account = acct,
        #    make = 'unknown',
        #    model = 'unknown',
        #    serial_number = 'unknown',
        #    utility_account_number = '6147898017',
        #    utility_meter_number = '3081616',
        #    )
        #playground.save()
        
        clin = Meter(
            name = 'Clinic',
            utility_type = 'electricity',
            location = 'north of covered Clinic entrance on West Bldg',
            serves = 'Clinic',
            units = 'kW,kWh',
            weather_station = ws,
            utility = gpc,
            rate_schedule = gpc_pls8_sec_in,
            account = acct,
            make = 'unknown',
            model = 'unknown',
            serial_number = 'unknown',
            utility_account_number = '1816415005',
            utility_meter_number = '3046324',
            )
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
            account = acct,
            make = 'unknown',
            model = 'unknown',
            serial_number = 'unknown',
            utility_account_number = '9401260170',
            utility_meter_number = '000537796',
            )
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
            account = acct,
            make = 'unknown',
            model = 'unknown',
            serial_number = 'unknown',
            utility_account_number = '8783526395',
            utility_meter_number = '003008386',
            )
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
            account = acct,
            make = 'unknown',
            model = 'unknown',
            serial_number = 'unknown',
            utility_account_number = '11-2487.301',
            utility_meter_number = 'NE51964675',
            )
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
            account = acct,
            make = 'unknown',
            model = 'unknown',
            serial_number = 'unknown',
            utility_account_number = '12-9779.302',
            utility_meter_number = 'NE049764661',
            )
        boone1300.save()
        
        
        
        #post-creation actions:
        #   1) if tracking, upload observed_file and/or provided_file and set tracking parameters in admin
        #   2) upload photos to Meter.image_file and Meter.nameplate_file
