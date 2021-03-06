from django.core.management.base import BaseCommand

import urllib
from decimal import Decimal

from django.core.files import File

from BuildingSpeak.settings import STATIC_URL

from BuildingSpeakApp.models import WeatherStation, Utility
from BuildingSpeakApp.models import InfiniteEnergyGAGas, CityOfATLWWW, GAPowerPandL, GAPowerRider


class Command(BaseCommand):

    def handle(self, *args, **options):
    ###---WeatherStations
        try:
            ATLdw = WeatherStation(
                name = 'ATL - downtown west',
                description = '1300 Joseph Boone Blvd, Atlanta, GA 30314',
                latitude = Decimal(33.7637360),
                longitude = Decimal(-84.4301300),
                tz_name = 'US/Eastern',
                )
            ATLdw.save()
        except:
            print 'Failed to create new WeatherStations.'
        else:
            print 'Created new WeatherStations.'
        
    ###---Utilitys
        try:
            atlw = Utility(
                name = 'City of Atlanta, Dept. of Watershed Mgmt.',
                )
            atlw.save()
            #post-creation actions
            #--load image file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/UtilityImage_ATL_Water.png'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            atlw.__setattr__('image_file', file_obj)
            atlw.save()
            
            infe = Utility(
                name = 'Infinite Energy',
                )
            infe.save()
            #post-creation actions
            #--load image file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/UtilityImage_Infinite_Energy.jpg'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            infe.__setattr__('image_file', file_obj)
            infe.save()
            
            GPC = Utility(
                name = 'Georgia Power Company',
                )
            GPC.save()
            #post-creation actions
            #--load image file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/UtilityImage_Georgia_Power.png'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPC.__setattr__('image_file', file_obj)
            GPC.save()
        except:
            print 'Failed to create new Utilities.'
        else:
            print 'Created new Utilities.'

    ###---Riders
        try:
            GPCECCR2 = GAPowerRider(
                name = 'GPC-ECCR-2',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.100131),
                percent_of_total_revenue = Decimal(0.0),
                summer_cost_per_kWh = Decimal(0.0),
                winter_cost_per_kWh = Decimal(0.0),
                apply_to_base_revenue = True,
                apply_to_total_revenue = False,
                apply_to_consumption = False,
                )
            GPCECCR2.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_ECCR-2.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCECCR2.__setattr__('rider_file', file_obj)
            GPCECCR2.save()
            
            GPCNCCR3 = GAPowerRider(
                name = 'GPC-NCCR-3',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.075821),
                percent_of_total_revenue = Decimal(0.0),
                summer_cost_per_kWh = Decimal(0.0),
                winter_cost_per_kWh = Decimal(0.0),
                apply_to_base_revenue = True,
                apply_to_total_revenue = False,
                apply_to_consumption = False,
                )
            GPCNCCR3.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_NCCR-3.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCNCCR3.__setattr__('rider_file', file_obj)
            GPCNCCR3.save()
            
            GPCDSMC3 = GAPowerRider(
                name = 'GPC-DSM-C-3',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.014484),
                percent_of_total_revenue = Decimal(0.0),
                summer_cost_per_kWh = Decimal(0.0),
                winter_cost_per_kWh = Decimal(0.0),
                apply_to_base_revenue = True,
                apply_to_total_revenue = False,
                apply_to_consumption = False,
                )
            GPCDSMC3.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_DSM-C-3.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCDSMC3.__setattr__('rider_file', file_obj)
            GPCDSMC3.save()
            
            GPCFCR23sec = GAPowerRider(
                name = 'GPC-FCR-23-secondary',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.0),
                percent_of_total_revenue = Decimal(0.0),
                summer_cost_per_kWh = Decimal(0.039323),
                winter_cost_per_kWh = Decimal(0.032584),
                apply_to_base_revenue = False,
                apply_to_total_revenue = False,
                apply_to_consumption = True,
                )
            GPCFCR23sec.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_FCR-23.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCFCR23sec.__setattr__('rider_file', file_obj)
            GPCFCR23sec.save()
            
            GPCFCR23prim = GAPowerRider(
                name = 'GPC-FCR-23-primary',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.0),
                percent_of_total_revenue = Decimal(0.0),
                summer_cost_per_kWh = Decimal(0.038912),
                winter_cost_per_kWh = Decimal(0.032244),
                apply_to_base_revenue = False,
                apply_to_total_revenue = False,
                apply_to_consumption = True,
                )
            GPCFCR23prim.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_FCR-23.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCFCR23prim.__setattr__('rider_file', file_obj)
            GPCFCR23prim.save()
            
            GPCFCR23tran = GAPowerRider(
                name = 'GPC-FCR-23-transmission',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.0),
                percent_of_total_revenue = Decimal(0.0),
                summer_cost_per_kWh = Decimal(0.038349),
                winter_cost_per_kWh = Decimal(0.031778),
                apply_to_base_revenue = False,
                apply_to_total_revenue = False,
                apply_to_consumption = True,
                )
            GPCFCR23tran.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_FCR-23.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCFCR23tran.__setattr__('rider_file', file_obj)
            GPCFCR23tran.save()
            
            GPCMFF2in = GAPowerRider(
                name = 'GPC-MFF-2-inside',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.0),
                percent_of_total_revenue = Decimal(0.029109),
                summer_cost_per_kWh = Decimal(0.0),
                winter_cost_per_kWh = Decimal(0.0),
                apply_to_base_revenue = False,
                apply_to_total_revenue = True,
                apply_to_consumption = False,
                )
            GPCMFF2in.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_MFF-2.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCMFF2in.__setattr__('rider_file', file_obj)
            GPCMFF2in.save()
            
            GPCMFF2out = GAPowerRider(
                name = 'GPC-MFF-2-outside',
                utility = GPC,
                percent_of_base_revenue = Decimal(0.0),
                percent_of_total_revenue = Decimal(0.010801),
                summer_cost_per_kWh = Decimal(0.0),
                winter_cost_per_kWh = Decimal(0.0),
                apply_to_base_revenue = False,
                apply_to_total_revenue = True,
                apply_to_consumption = False,
                )
            GPCMFF2out.save()
            #post-creation actions
            #--load rider file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RiderFile_Georgia_Power_MFF-2.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCMFF2out.__setattr__('rider_file', file_obj)
            GPCMFF2out.save()
        except:
            print 'Failed to create new RateScheduleRiders.'
        else:
            print 'Created new RateScheduleRiders.'
        
    ###---RateSchedules
        try:
            bizgas1 = InfiniteEnergyGAGas(
                name = 'Fixed Business Rate',
                utility = infe,
                basic_service_charge = Decimal(20),
                tax_percentage = Decimal(0.08),
                therm_rate = Decimal(0.66),
                )
            bizgas1.save()
            
            w_ww = CityOfATLWWW(
                name = 'Water and Wastewater 2012',
                utility = atlw,
                base_charge = Decimal(13.12),
                tax_percentage = Decimal(0.08),
                tier1 = Decimal(4.0),
                tier2 = Decimal(7.0),
                tier3 = Decimal(999999999),
                rate1 = Decimal(12.32),
                rate2 = Decimal(18.98),
                rate3 = Decimal(21.85),
                security_surcharge = Decimal(0.15),
                )
            w_ww.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_City_of_Atlanta_water.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            w_ww.__setattr__('rate_file', file_obj)
            w_ww.save()
            
            #-----secondary-inside
            GPCPLS8_sec_in = GAPowerPandL(
                name = 'GPC-PLS-8-secondary-inside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 25,
                tier1b = 3000,
                tier1c = 10000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0,
                rate1b = 0.105403,
                rate1c = 0.099215,
                rate1d = 0.086343,
                rate2a = 0.010644,
                rate2b = 0.010644,
                rate2c = 0.010644,
                rate2d = 0.010644,
                rate3a = 0.008068,
                rate3b = 0.008068,
                rate3c = 0.008068,
                rate3d = 0.008068,
                rate4a = 0.007028,
                rate4b = 0.007028,
                rate4c = 0.007028,
                rate4d = 0.007028,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.72,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 5,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 30,
                limitation_of_service_min_kW = 0,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLS8_sec_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_Georgia_Power_PLS-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLS8_sec_in.__setattr__('rate_file', file_obj)
            GPCPLS8_sec_in.save()
            #--add riders
            GPCPLS8_sec_in.riders.add(GPCECCR2)
            GPCPLS8_sec_in.riders.add(GPCNCCR3)
            GPCPLS8_sec_in.riders.add(GPCDSMC3)
            GPCPLS8_sec_in.riders.add(GPCFCR23sec)
            GPCPLS8_sec_in.riders.add(GPCMFF2in)
            
            GPCPLM8_sec_in = GAPowerPandL(
                name = 'GPC-PLM-8-secondary-inside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.106704,
                rate1b = 0.097727,
                rate1c = 0.084260,
                rate1d = 0.065330,
                rate2a = 0.010855,
                rate2b = 0.010855,
                rate2c = 0.010855,
                rate2d = 0.010855,
                rate3a = 0.008166,
                rate3b = 0.008166,
                rate3c = 0.008166,
                rate3d = 0.008166,
                rate4a = 0.007106,
                rate4b = 0.007106,
                rate4c = 0.007106,
                rate4d = 0.007106,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.81,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 30,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 500,
                limitation_of_service_min_kW = 30,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLM8_sec_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLM-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLM8_sec_in.__setattr__('rate_file', file_obj)
            GPCPLM8_sec_in.save()
            #--add riders
            GPCPLM8_sec_in.riders.add(GPCECCR2)
            GPCPLM8_sec_in.riders.add(GPCNCCR3)
            GPCPLM8_sec_in.riders.add(GPCDSMC3)
            GPCPLM8_sec_in.riders.add(GPCFCR23sec)
            GPCPLM8_sec_in.riders.add(GPCMFF2in)
            
            GPCPLL8_sec_in = GAPowerPandL(
                name = 'GPC-PLL-8-secondary-inside',
                utility = GPC,
                basic_service_charge = 20,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.125319,
                rate1b = 0.113642,
                rate1c = 0.096926,
                rate1d = 0.074732,
                rate2a = 0.012880,
                rate2b = 0.012880,
                rate2c = 0.012880,
                rate2d = 0.012880,
                rate3a = 0.009713,
                rate3b = 0.009713,
                rate3c = 0.009713,
                rate3d = 0.009713,
                rate4a = 0.007290,
                rate4b = 0.007290,
                rate4c = 0.007290,
                rate4d = 0.007290,
                excess_kW_threshold = 0.0,
                excess_kW_rate = 9.01,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 500,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 999999,
                limitation_of_service_min_kW = 500,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLL8_sec_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLL-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLL8_sec_in.__setattr__('rate_file', file_obj)
            GPCPLL8_sec_in.save()
            #--add riders
            GPCPLL8_sec_in.riders.add(GPCECCR2)
            GPCPLL8_sec_in.riders.add(GPCNCCR3)
            GPCPLL8_sec_in.riders.add(GPCDSMC3)
            GPCPLL8_sec_in.riders.add(GPCFCR23sec)
            GPCPLL8_sec_in.riders.add(GPCMFF2in)
            
            #----secondary-outside
            GPCPLS8_sec_out = GAPowerPandL(
                name = 'GPC-PLS-8-secondary-outside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 25,
                tier1b = 3000,
                tier1c = 10000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0,
                rate1b = 0.105403,
                rate1c = 0.099215,
                rate1d = 0.086343,
                rate2a = 0.010644,
                rate2b = 0.010644,
                rate2c = 0.010644,
                rate2d = 0.010644,
                rate3a = 0.008068,
                rate3b = 0.008068,
                rate3c = 0.008068,
                rate3d = 0.008068,
                rate4a = 0.007028,
                rate4b = 0.007028,
                rate4c = 0.007028,
                rate4d = 0.007028,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.72,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 5,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 30,
                limitation_of_service_min_kW = 0,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLS8_sec_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLS-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLS8_sec_out.__setattr__('rate_file', file_obj)
            GPCPLS8_sec_out.save()
            #--add riders
            GPCPLS8_sec_out.riders.add(GPCECCR2)
            GPCPLS8_sec_out.riders.add(GPCNCCR3)
            GPCPLS8_sec_out.riders.add(GPCDSMC3)
            GPCPLS8_sec_out.riders.add(GPCFCR23sec)
            GPCPLS8_sec_out.riders.add(GPCMFF2out)
            
            GPCPLM8_sec_out = GAPowerPandL(
                name = 'GPC-PLM-8-secondary-outside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.106704,
                rate1b = 0.097727,
                rate1c = 0.084260,
                rate1d = 0.065330,
                rate2a = 0.010855,
                rate2b = 0.010855,
                rate2c = 0.010855,
                rate2d = 0.010855,
                rate3a = 0.008166,
                rate3b = 0.008166,
                rate3c = 0.008166,
                rate3d = 0.008166,
                rate4a = 0.007106,
                rate4b = 0.007106,
                rate4c = 0.007106,
                rate4d = 0.007106,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.81,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 30,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 500,
                limitation_of_service_min_kW = 30,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLM8_sec_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLM-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLM8_sec_out.__setattr__('rate_file', file_obj)
            GPCPLM8_sec_out.save()
            #--add riders
            GPCPLM8_sec_out.riders.add(GPCECCR2)
            GPCPLM8_sec_out.riders.add(GPCNCCR3)
            GPCPLM8_sec_out.riders.add(GPCDSMC3)
            GPCPLM8_sec_out.riders.add(GPCFCR23sec)
            GPCPLM8_sec_out.riders.add(GPCMFF2out)
            
            GPCPLL8_sec_out = GAPowerPandL(
                name = 'GPC-PLL-8-secondary-outside',
                utility = GPC,
                basic_service_charge = 20,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.125319,
                rate1b = 0.113642,
                rate1c = 0.096926,
                rate1d = 0.074732,
                rate2a = 0.012880,
                rate2b = 0.012880,
                rate2c = 0.012880,
                rate2d = 0.012880,
                rate3a = 0.009713,
                rate3b = 0.009713,
                rate3c = 0.009713,
                rate3d = 0.009713,
                rate4a = 0.007290,
                rate4b = 0.007290,
                rate4c = 0.007290,
                rate4d = 0.007290,
                excess_kW_threshold = 0.0,
                excess_kW_rate = 9.01,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 500,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 999999,
                limitation_of_service_min_kW = 500,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLL8_sec_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLL-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLL8_sec_out.__setattr__('rate_file', file_obj)
            GPCPLL8_sec_out.save()
            #--add riders
            GPCPLL8_sec_out.riders.add(GPCECCR2)
            GPCPLL8_sec_out.riders.add(GPCNCCR3)
            GPCPLL8_sec_out.riders.add(GPCDSMC3)
            GPCPLL8_sec_out.riders.add(GPCFCR23sec)
            GPCPLL8_sec_out.riders.add(GPCMFF2out)
            
            #----primary-inside
            GPCPLS8_prim_in = GAPowerPandL(
                name = 'GPC-PLS-8-primary-inside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 25,
                tier1b = 3000,
                tier1c = 10000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0,
                rate1b = 0.105403,
                rate1c = 0.099215,
                rate1d = 0.086343,
                rate2a = 0.010644,
                rate2b = 0.010644,
                rate2c = 0.010644,
                rate2d = 0.010644,
                rate3a = 0.008068,
                rate3b = 0.008068,
                rate3c = 0.008068,
                rate3d = 0.008068,
                rate4a = 0.007028,
                rate4b = 0.007028,
                rate4c = 0.007028,
                rate4d = 0.007028,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.72,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 5,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 30,
                limitation_of_service_min_kW = 0,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLS8_prim_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLS-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLS8_prim_in.__setattr__('rate_file', file_obj)
            GPCPLS8_prim_in.save()
            #--add riders
            GPCPLS8_prim_in.riders.add(GPCECCR2)
            GPCPLS8_prim_in.riders.add(GPCNCCR3)
            GPCPLS8_prim_in.riders.add(GPCDSMC3)
            GPCPLS8_prim_in.riders.add(GPCFCR23prim)
            GPCPLS8_prim_in.riders.add(GPCMFF2in)
            
            GPCPLM8_prim_in = GAPowerPandL(
                name = 'GPC-PLM-8-primary-inside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.106704,
                rate1b = 0.097727,
                rate1c = 0.084260,
                rate1d = 0.065330,
                rate2a = 0.010855,
                rate2b = 0.010855,
                rate2c = 0.010855,
                rate2d = 0.010855,
                rate3a = 0.008166,
                rate3b = 0.008166,
                rate3c = 0.008166,
                rate3d = 0.008166,
                rate4a = 0.007106,
                rate4b = 0.007106,
                rate4c = 0.007106,
                rate4d = 0.007106,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.81,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 30,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 500,
                limitation_of_service_min_kW = 30,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLM8_prim_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLM-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLM8_prim_in.__setattr__('rate_file', file_obj)
            GPCPLM8_prim_in.save()
            #--add riders
            GPCPLM8_prim_in.riders.add(GPCECCR2)
            GPCPLM8_prim_in.riders.add(GPCNCCR3)
            GPCPLM8_prim_in.riders.add(GPCDSMC3)
            GPCPLM8_prim_in.riders.add(GPCFCR23prim)
            GPCPLM8_prim_in.riders.add(GPCMFF2in)
            
            GPCPLL8_prim_in = GAPowerPandL(
                name = 'GPC-PLL-8-primary-inside',
                utility = GPC,
                basic_service_charge = 20,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.125319,
                rate1b = 0.113642,
                rate1c = 0.096926,
                rate1d = 0.074732,
                rate2a = 0.012880,
                rate2b = 0.012880,
                rate2c = 0.012880,
                rate2d = 0.012880,
                rate3a = 0.009713,
                rate3b = 0.009713,
                rate3c = 0.009713,
                rate3d = 0.009713,
                rate4a = 0.007290,
                rate4b = 0.007290,
                rate4c = 0.007290,
                rate4d = 0.007290,
                excess_kW_threshold = 0.0,
                excess_kW_rate = 9.01,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 500,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 999999,
                limitation_of_service_min_kW = 500,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLL8_prim_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLL-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLL8_prim_in.__setattr__('rate_file', file_obj)
            GPCPLL8_prim_in.save()
            #--add riders
            GPCPLL8_prim_in.riders.add(GPCECCR2)
            GPCPLL8_prim_in.riders.add(GPCNCCR3)
            GPCPLL8_prim_in.riders.add(GPCDSMC3)
            GPCPLL8_prim_in.riders.add(GPCFCR23prim)
            GPCPLL8_prim_in.riders.add(GPCMFF2in)
            
            #-----primary-outside
            GPCPLS8_prim_out = GAPowerPandL(
                name = 'GPC-PLS-8-primary-outside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 25,
                tier1b = 3000,
                tier1c = 10000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0,
                rate1b = 0.105403,
                rate1c = 0.099215,
                rate1d = 0.086343,
                rate2a = 0.010644,
                rate2b = 0.010644,
                rate2c = 0.010644,
                rate2d = 0.010644,
                rate3a = 0.008068,
                rate3b = 0.008068,
                rate3c = 0.008068,
                rate3d = 0.008068,
                rate4a = 0.007028,
                rate4b = 0.007028,
                rate4c = 0.007028,
                rate4d = 0.007028,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.72,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 5,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 30,
                limitation_of_service_min_kW = 0,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLS8_prim_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLS-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLS8_prim_out.__setattr__('rate_file', file_obj)
            GPCPLS8_prim_out.save()
            #--add riders
            GPCPLS8_prim_out.riders.add(GPCECCR2)
            GPCPLS8_prim_out.riders.add(GPCNCCR3)
            GPCPLS8_prim_out.riders.add(GPCDSMC3)
            GPCPLS8_prim_out.riders.add(GPCFCR23prim)
            GPCPLS8_prim_out.riders.add(GPCMFF2out)
            
            GPCPLM8_prim_out = GAPowerPandL(
                name = 'GPC-PLM-8-primary-outside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.106704,
                rate1b = 0.097727,
                rate1c = 0.084260,
                rate1d = 0.065330,
                rate2a = 0.010855,
                rate2b = 0.010855,
                rate2c = 0.010855,
                rate2d = 0.010855,
                rate3a = 0.008166,
                rate3b = 0.008166,
                rate3c = 0.008166,
                rate3d = 0.008166,
                rate4a = 0.007106,
                rate4b = 0.007106,
                rate4c = 0.007106,
                rate4d = 0.007106,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.81,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 30,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 500,
                limitation_of_service_min_kW = 30,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLM8_prim_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLM-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLM8_prim_out.__setattr__('rate_file', file_obj)
            GPCPLM8_prim_out.save()
            #--add riders
            GPCPLM8_prim_out.riders.add(GPCECCR2)
            GPCPLM8_prim_out.riders.add(GPCNCCR3)
            GPCPLM8_prim_out.riders.add(GPCDSMC3)
            GPCPLM8_prim_out.riders.add(GPCFCR23prim)
            GPCPLM8_prim_out.riders.add(GPCMFF2out)
            
            GPCPLL8_prim_out = GAPowerPandL(
                name = 'GPC-PLL-8-primary-outside',
                utility = GPC,
                basic_service_charge = 20,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.125319,
                rate1b = 0.113642,
                rate1c = 0.096926,
                rate1d = 0.074732,
                rate2a = 0.012880,
                rate2b = 0.012880,
                rate2c = 0.012880,
                rate2d = 0.012880,
                rate3a = 0.009713,
                rate3b = 0.009713,
                rate3c = 0.009713,
                rate3d = 0.009713,
                rate4a = 0.007290,
                rate4b = 0.007290,
                rate4c = 0.007290,
                rate4d = 0.007290,
                excess_kW_threshold = 0.0,
                excess_kW_rate = 9.01,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 500,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 999999,
                limitation_of_service_min_kW = 500,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLL8_prim_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLL-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLL8_prim_out.__setattr__('rate_file', file_obj)
            GPCPLL8_prim_out.save()
            #--add riders
            GPCPLL8_prim_out.riders.add(GPCECCR2)
            GPCPLL8_prim_out.riders.add(GPCNCCR3)
            GPCPLL8_prim_out.riders.add(GPCDSMC3)
            GPCPLL8_prim_out.riders.add(GPCFCR23prim)
            GPCPLL8_prim_out.riders.add(GPCMFF2out)
            
            #----transmission-inside
            GPCPLS8_tran_in = GAPowerPandL(
                name = 'GPC-PLS-8-transmission-inside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 25,
                tier1b = 3000,
                tier1c = 10000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0,
                rate1b = 0.105403,
                rate1c = 0.099215,
                rate1d = 0.086343,
                rate2a = 0.010644,
                rate2b = 0.010644,
                rate2c = 0.010644,
                rate2d = 0.010644,
                rate3a = 0.008068,
                rate3b = 0.008068,
                rate3c = 0.008068,
                rate3d = 0.008068,
                rate4a = 0.007028,
                rate4b = 0.007028,
                rate4c = 0.007028,
                rate4d = 0.007028,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.72,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 5,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 30,
                limitation_of_service_min_kW = 0,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLS8_tran_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLS-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLS8_tran_in.__setattr__('rate_file', file_obj)
            GPCPLS8_tran_in.save()
            #--add riders
            GPCPLS8_tran_in.riders.add(GPCECCR2)
            GPCPLS8_tran_in.riders.add(GPCNCCR3)
            GPCPLS8_tran_in.riders.add(GPCDSMC3)
            GPCPLS8_tran_in.riders.add(GPCFCR23tran)
            GPCPLS8_tran_in.riders.add(GPCMFF2in)
            
            GPCPLM8_tran_in = GAPowerPandL(
                name = 'GPC-PLM-8-transmission-inside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.106704,
                rate1b = 0.097727,
                rate1c = 0.084260,
                rate1d = 0.065330,
                rate2a = 0.010855,
                rate2b = 0.010855,
                rate2c = 0.010855,
                rate2d = 0.010855,
                rate3a = 0.008166,
                rate3b = 0.008166,
                rate3c = 0.008166,
                rate3d = 0.008166,
                rate4a = 0.007106,
                rate4b = 0.007106,
                rate4c = 0.007106,
                rate4d = 0.007106,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.81,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 30,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 500,
                limitation_of_service_min_kW = 30,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLM8_tran_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLM-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLM8_tran_in.__setattr__('rate_file', file_obj)
            GPCPLM8_tran_in.save()
            #--add riders
            GPCPLM8_tran_in.riders.add(GPCECCR2)
            GPCPLM8_tran_in.riders.add(GPCNCCR3)
            GPCPLM8_tran_in.riders.add(GPCDSMC3)
            GPCPLM8_tran_in.riders.add(GPCFCR23tran)
            GPCPLM8_tran_in.riders.add(GPCMFF2in)
            
            GPCPLL8_tran_in = GAPowerPandL(
                name = 'GPC-PLL-8-transmission-inside',
                utility = GPC,
                basic_service_charge = 20,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.125319,
                rate1b = 0.113642,
                rate1c = 0.096926,
                rate1d = 0.074732,
                rate2a = 0.012880,
                rate2b = 0.012880,
                rate2c = 0.012880,
                rate2d = 0.012880,
                rate3a = 0.009713,
                rate3b = 0.009713,
                rate3c = 0.009713,
                rate3d = 0.009713,
                rate4a = 0.007290,
                rate4b = 0.007290,
                rate4c = 0.007290,
                rate4d = 0.007290,
                excess_kW_threshold = 0.0,
                excess_kW_rate = 9.01,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 500,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 999999,
                limitation_of_service_min_kW = 500,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLL8_tran_in.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLL-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLL8_tran_in.__setattr__('rate_file', file_obj)
            GPCPLL8_tran_in.save()
            #--add riders
            GPCPLL8_tran_in.riders.add(GPCECCR2)
            GPCPLL8_tran_in.riders.add(GPCNCCR3)
            GPCPLL8_tran_in.riders.add(GPCDSMC3)
            GPCPLL8_tran_in.riders.add(GPCFCR23tran)
            GPCPLL8_tran_in.riders.add(GPCMFF2in)
            
            #-----transmission-outside
            GPCPLS8_tran_out = GAPowerPandL(
                name = 'GPC-PLS-8-transmission-outside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 25,
                tier1b = 3000,
                tier1c = 10000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0,
                rate1b = 0.105403,
                rate1c = 0.099215,
                rate1d = 0.086343,
                rate2a = 0.010644,
                rate2b = 0.010644,
                rate2c = 0.010644,
                rate2d = 0.010644,
                rate3a = 0.008068,
                rate3b = 0.008068,
                rate3c = 0.008068,
                rate3d = 0.008068,
                rate4a = 0.007028,
                rate4b = 0.007028,
                rate4c = 0.007028,
                rate4d = 0.007028,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.72,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 5,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 30,
                limitation_of_service_min_kW = 0,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLS8_tran_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLS-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLS8_tran_out.__setattr__('rate_file', file_obj)
            GPCPLS8_tran_out.save()
            #--add riders
            GPCPLS8_tran_out.riders.add(GPCECCR2)
            GPCPLS8_tran_out.riders.add(GPCNCCR3)
            GPCPLS8_tran_out.riders.add(GPCDSMC3)
            GPCPLS8_tran_out.riders.add(GPCFCR23tran)
            GPCPLS8_tran_out.riders.add(GPCMFF2out)
            
            GPCPLM8_tran_out = GAPowerPandL(
                name = 'GPC-PLM-8-transmission-outside',
                utility = GPC,
                basic_service_charge = 18,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.106704,
                rate1b = 0.097727,
                rate1c = 0.084260,
                rate1d = 0.065330,
                rate2a = 0.010855,
                rate2b = 0.010855,
                rate2c = 0.010855,
                rate2d = 0.010855,
                rate3a = 0.008166,
                rate3b = 0.008166,
                rate3c = 0.008166,
                rate3d = 0.008166,
                rate4a = 0.007106,
                rate4b = 0.007106,
                rate4c = 0.007106,
                rate4d = 0.007106,
                excess_kW_threshold = 30,
                excess_kW_rate = 7.81,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 30,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 500,
                limitation_of_service_min_kW = 30,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLM8_tran_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLM-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLM8_tran_out.__setattr__('rate_file', file_obj)
            GPCPLM8_tran_out.save()
            #--add riders
            GPCPLM8_tran_out.riders.add(GPCECCR2)
            GPCPLM8_tran_out.riders.add(GPCNCCR3)
            GPCPLM8_tran_out.riders.add(GPCDSMC3)
            GPCPLM8_tran_out.riders.add(GPCFCR23tran)
            GPCPLM8_tran_out.riders.add(GPCMFF2out)
            
            GPCPLL8_tran_out = GAPowerPandL(
                name = 'GPC-PLL-8-transmission-outside',
                utility = GPC,
                basic_service_charge = 20,
                tax_percentage = 0.08,
                use_input_billing_demand = True,
                tier1 = 200,
                tier1a = 3000,
                tier1b = 10000,
                tier1c = 200000,
                tier1d = 999999999,
                tier2 = 400,
                tier2a = 999999996,
                tier2b = 999999997,
                tier2c = 999999998,
                tier2d = 999999999,
                tier3 = 600,
                tier3a = 999999996,
                tier3b = 999999997,
                tier3c = 999999998,
                tier3d = 999999999,
                tier4 = 999999999,
                tier4a = 999999996,
                tier4b = 999999997,
                tier4c = 999999998,
                tier4d = 999999999,
                rate1a = 0.125319,
                rate1b = 0.113642,
                rate1c = 0.096926,
                rate1d = 0.074732,
                rate2a = 0.012880,
                rate2b = 0.012880,
                rate2c = 0.012880,
                rate2d = 0.012880,
                rate3a = 0.009713,
                rate3b = 0.009713,
                rate3c = 0.009713,
                rate3d = 0.009713,
                rate4a = 0.007290,
                rate4b = 0.007290,
                rate4c = 0.007290,
                rate4d = 0.007290,
                excess_kW_threshold = 0.0,
                excess_kW_rate = 9.01,
                window_minutes = 30,
                summer_start_month = 6,
                summer_end_month = 9,
                winter_start_month = 10,
                winter_end_month = 5,
                billing_demand_sliding_month_window = 11,
                summer_summer_threshold = 0.95,
                summer_winter_threshold = 0.60,
                winter_summer_threshold = 0.95,
                winter_winter_threshold = 0.60,
                contract_minimum_demand = 0,
                minimum_fraction_contract_capacity = 0.50,
                absolute_minimum_demand = 500,
                lim_service_sliding_month_window = 11,
                limitation_of_service_max_kW = 999999,
                limitation_of_service_min_kW = 500,
                limitation_of_service_winter_percent = 0.6,
                limitation_of_service_summer_percent = 0.95,
                )
            GPCPLL8_tran_out.save()
            #post-creation actions
            #--load rate file
            file_url = STATIC_URL + 'upload_files/BuildingSpeakBuiltins_001/RateFile_GeorgiaPower_PLL-8.pdf'
            result = urllib.urlretrieve(file_url)
            file_obj = File(open(result[0],'rb'))
            GPCPLL8_tran_out.__setattr__('rate_file', file_obj)
            GPCPLL8_tran_out.save()
            #--add riders
            GPCPLL8_tran_out.riders.add(GPCECCR2)
            GPCPLL8_tran_out.riders.add(GPCNCCR3)
            GPCPLL8_tran_out.riders.add(GPCDSMC3)
            GPCPLL8_tran_out.riders.add(GPCFCR23tran)
            GPCPLL8_tran_out.riders.add(GPCMFF2out)
        except:
            print 'Failed to create new RateSchedules.'
        else:
            print 'Created new RateSchedules.'
