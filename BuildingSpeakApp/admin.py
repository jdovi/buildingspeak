from BuildingSpeakApp.models import Account, Building, Meter, Equipment, Space, EfficiencyMeasure
from BuildingSpeakApp.models import BuildingMeterApportionment, SpaceMeterApportionment
from BuildingSpeakApp.models import EMMeterApportionment, EMEquipmentApportionment
from BuildingSpeakApp.models import MeterConsumptionModel, MeterPeakDemandModel
from BuildingSpeakApp.models import PackageUnit, Reader, Reading, Message
from BuildingSpeakApp.models import UnitSchedule, OperatingSchedule, Utility
from BuildingSpeakApp.models import RateSchedule, RateScheduleRider
from BuildingSpeakApp.models import Monther, Monthling
from BuildingSpeakApp.models import WeatherStation, WeatherDataPoint
from BuildingSpeakApp.models import UserProfile
from BuildingSpeakApp.models import GAPowerRider, GAPowerPandL, InfiniteEnergyGAGas, CityOfATLWWW
from django.contrib import admin

class SpaceMeterApportionmentInline(admin.TabularInline):
    model = SpaceMeterApportionment
    extra = 1

class BuildingMeterApportionmentInline(admin.TabularInline):
    model = BuildingMeterApportionment
    extra = 1

class EMMeterApportionmentInline(admin.TabularInline):
    model = EMMeterApportionment
    extra = 1

class EMEquipmentApportionmentInline(admin.TabularInline):
    model = EMEquipmentApportionment
    extra = 1

class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account Information', {'fields': ['name',
                                            'account_type',
                                            'street_address',
                                            'city',
                                            'state',
                                            'zip_code',
                                            'launch_date']}),
        ('Relationships', {'fields': 	   ['messages',
                                            'users',
                                            'readers',
                                            'schedules']}),
        ('Contact Details',     {'fields': ['first_name',
                                            'last_name',
                                            'title',
                                            'email',
                                            'phone'],
                                'classes': ['collapse']}),
        ('Billing Information', {'fields': ['status',
                                            'monthly_payment'],
                                'classes': ['collapse']}),
        ('Data Files', {'fields': ['observed_file',
                                  'observed_file_track',
                                  'observed_file_skiprows',
                                  'observed_file_column_for_indexing',
                                  'observed_file_time_zone',
                                  'observed_file_GMT_offset',
                                  'observed_file_adjusts_for_DST',
                                  'provided_file',
                                  'provided_file_track',
                                  'provided_file_skiprows',
                                  'provided_file_column_for_indexing',
                                  'provided_file_time_zone',
                                  'provided_file_GMT_offset',
                                  'provided_file_adjusts_for_DST'],
                        'classes': ['collapse']}),
        ('Image File', {'fields': ['image_file'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'zip_code', 'account_type', 'status', 'monthly_payment',
                    'connected_meters_for_admin', 'connected_buildings_for_admin',
                    'connected_equipments_for_admin')
    search_fields = ['name', 'id', 'zip_code', 'account_type', 'status', 'monthly_payment']
    list_filter = ['status', 'launch_date', 'zip_code']
    
class BuildingAdmin(admin.ModelAdmin):
    inlines = (BuildingMeterApportionmentInline,)
    fieldsets = [
        ('Building Information',   {'fields': ['account',
                                               'name',
                                               'street_address',
                                               'city',
                                               'state',
                                               'zip_code']}),
        ('Relationships',   {'fields':  ['weather_station',
                                         'messages',
                                         'readers',
                                         'schedules']}),
        ('Point of Contact', {'fields': ['first_name',
                                         'last_name',
                                         'title',
                                         'email',
                                         'phone'],
                             'classes': ['collapse']}),
        ('Characteristics',  {'fields': ['age',
                                         'square_footage',
                                         'stories',
                                         'building_type',
                                         'EIA_type',
                                         'ESPM_type',
                                         'max_occupancy'],
                             'classes': ['collapse']}),
        ('Data Files', {'fields': ['observed_file',
                                  'observed_file_track',
                                  'observed_file_skiprows',
                                  'observed_file_column_for_indexing',
                                  'observed_file_time_zone',
                                  'observed_file_GMT_offset',
                                  'observed_file_adjusts_for_DST',
                                  'provided_file',
                                  'provided_file_track',
                                  'provided_file_skiprows',
                                  'provided_file_column_for_indexing',
                                  'provided_file_time_zone',
                                  'provided_file_GMT_offset',
                                  'provided_file_adjusts_for_DST'],
                        'classes': ['collapse']}),
        ('Image File', {'fields': ['image_file'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'account_for_admin', 'square_footage', 'building_type',
                    'connected_spaces_for_admin', 'weather_station_for_admin',
                    'connected_meters_for_admin', 'connected_equipments_for_admin')
    search_fields = ['name', 'id', 'square_footage', 'building_type']
    list_filter = ['account', 'building_type']

class EfficiencyMeasureAdmin(admin.ModelAdmin):
    inlines = (EMMeterApportionmentInline, )
    inlines = (EMEquipmentApportionmentInline, )
    fieldsets = [
        ('Measure Information', {'fields': ['name',
                                            'when',
                                            'utility_type',
                                            'units',
                                            'weather_station']}),
        ('Annual Fields',   {'fields':  ['annual_consumption_savings',
                                         'peak_demand_savings',
                                         'annual_cost_savings',
                                         'percent_uncertainty',
                                         'percent_cool',
                                         'percent_heat',
                                         'percent_flat',
                                         'percent_fixed'],
                             'classes': ['collapse']}),
        ('Consumption',   {'fields':    ['jan_cons',
                                         'feb_cons',
                                         'mar_cons',
                                         'apr_cons',
                                         'may_cons',
                                         'jun_cons',
                                         'jul_cons',
                                         'aug_cons',
                                         'sep_cons',
                                         'oct_cons',
                                         'nov_cons',
                                         'dec_cons'],
                             'classes': ['collapse']}),
        ('Peak Demand',   {'fields':    ['jan_peak',
                                         'feb_peak',
                                         'mar_peak',
                                         'apr_peak',
                                         'may_peak',
                                         'jun_peak',
                                         'jul_peak',
                                         'aug_peak',
                                         'sep_peak',
                                         'oct_peak',
                                         'nov_peak',
                                         'dec_peak'],
                             'classes': ['collapse']}),
        ('Cost',   {'fields':           ['jan_cost',
                                         'feb_cost',
                                         'mar_cost',
                                         'apr_cost',
                                         'may_cost',
                                         'jun_cost',
                                         'jul_cost',
                                         'aug_cost',
                                         'sep_cost',
                                         'oct_cost',
                                         'nov_cost',
                                         'dec_cost'],
                             'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'when', 'utility_type', 'units', 'weather_station')
    search_fields = ['name', 'id', 'utility_type', 'units', 'weather_station']
    list_filter = ['name', 'utility_type', 'units', 'weather_station']

class MeterAdmin(admin.ModelAdmin):
    inlines = (BuildingMeterApportionmentInline, )
    inlines = (EMMeterApportionmentInline, )
    fieldsets = [
        ('Meter Information',   {'fields': ['account',
                                            'name',
                                            'utility_type',
                                            'units',
                                            'utility_account_number',
                                            'utility_meter_number',
                                            'location',
                                            'serves']}),
        ('Relationships',   {'fields':  ['weather_station',
                                         'utility',
                                         'rate_schedule',
                                         'readers',
                                         'schedules',
                                         'messages']}),
        ('Nameplate',      {'fields': ['make',
                                       'model',
                                       'serial_number'],
                            'classes': ['collapse']}),
        ('Data Files', {'fields': ['bill_data_file',
                                   'observed_file',
                                  'observed_file_track',
                                  'observed_file_skiprows',
                                  'observed_file_column_for_indexing',
                                  'observed_file_time_zone',
                                  'observed_file_GMT_offset',
                                  'observed_file_adjusts_for_DST',
                                  'provided_file',
                                  'provided_file_track',
                                  'provided_file_skiprows',
                                  'provided_file_column_for_indexing',
                                  'provided_file_time_zone',
                                  'provided_file_GMT_offset',
                                  'provided_file_adjusts_for_DST'],
                        'classes': ['collapse']}),
        ('Image Files', {'fields': ['image_file',
                                    'nameplate_file'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'account_name_for_admin', 'utility_account_number',
                    'utility_type', 'units', 'utility_name_for_admin', 'rate_schedule_name_for_admin',
                    'weather_station_name_for_admin', 'connected_building_names_for_admin',
                    'connected_equipment_names_for_admin')
    search_fields = ['name', 'id', 'utility_account_number', 'utility_type', 'units']
    list_filter = ['utility_type', 'units']

class MeterConsumptionModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['meter',
                                    'model_type',
                                    'first_month',
                                    'last_month']}),
        ('Model Parameters', {'fields': ['Tccp',
                                        'Thcp',
                                        'prediction_alpha',
                                        'beta00p', 'beta00v',
                                        'beta01p', 'beta01v',
                                        'beta02p', 'beta02v',
                                        'beta03p', 'beta03v',
                                        'beta04p', 'beta04v',
                                        'beta05p', 'beta05v',
                                        'beta06p', 'beta06v',
                                        'beta07p', 'beta07v',
                                        'beta08p', 'beta08v',
                                        'beta09p', 'beta09v',
                                        'beta10p', 'beta10v',
                                        ],
                         'classes': ['collapse']}),
        ('Parameter Stats', {'fields': ['beta00_se', 'beta00_t_stat', 'beta00_p_value', 'beta00_95_conf_int',
                                        'beta01_se', 'beta01_t_stat', 'beta01_p_value', 'beta01_95_conf_int',
                                        'beta02_se', 'beta02_t_stat', 'beta02_p_value', 'beta02_95_conf_int',
                                        'beta03_se', 'beta03_t_stat', 'beta03_p_value', 'beta03_95_conf_int',
                                        'beta04_se', 'beta04_t_stat', 'beta04_p_value', 'beta04_95_conf_int',
                                        'beta05_se', 'beta05_t_stat', 'beta05_p_value', 'beta05_95_conf_int',
                                        'beta06_se', 'beta06_t_stat', 'beta06_p_value', 'beta06_95_conf_int',
                                        'beta07_se', 'beta07_t_stat', 'beta07_p_value', 'beta07_95_conf_int',
                                        'beta08_se', 'beta08_t_stat', 'beta08_p_value', 'beta08_95_conf_int',
                                        'beta09_se', 'beta09_t_stat', 'beta09_p_value', 'beta09_95_conf_int',
                                        'beta10_se', 'beta10_t_stat', 'beta10_p_value', 'beta10_95_conf_int',
                                        ],
                         'classes': ['collapse']}),
        ('Model Stats', {'fields': ['r_squared',
                                    'adj_r_squared',
                                    'p',
                                    'df',
                                    'Yavg',
                                    'SSQres',
                                    'rmse',
                                    'cvrmse',
                                    'nbe',
                                    'F_stat',
                                    'F_stat_p_value',
                                    'autocorr_coeff',
                                    'acceptance_score'],
                         'classes': ['collapse']}),
        ('Relationships',   {'fields':  ['messages'],
                            'classes': ['collapse']}),
    ]
    list_display = ('id', 'meter', 'model_type')
    search_fields = ['id', 'meter', 'model_type']
    list_filter = ['meter', 'model_type']

class MeterPeakDemandModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['meter',
                                    'model_type',
                                    'first_month',
                                    'last_month']}),
        ('Model Parameters', {'fields': ['Tccp',
                                        'Thcp',
                                        'prediction_alpha',
                                        'beta00p', 'beta00v',
                                        'beta01p', 'beta01v',
                                        'beta02p', 'beta02v',
                                        'beta03p', 'beta03v',
                                        'beta04p', 'beta04v',
                                        'beta05p', 'beta05v',
                                        'beta06p', 'beta06v',
                                        'beta07p', 'beta07v',
                                        'beta08p', 'beta08v',
                                        'beta09p', 'beta09v',
                                        'beta10p', 'beta10v',
                                        ],
                         'classes': ['collapse']}),
        ('Parameter Stats', {'fields': ['beta00_se', 'beta00_t_stat', 'beta00_p_value', 'beta00_95_conf_int',
                                        'beta01_se', 'beta01_t_stat', 'beta01_p_value', 'beta01_95_conf_int',
                                        'beta02_se', 'beta02_t_stat', 'beta02_p_value', 'beta02_95_conf_int',
                                        'beta03_se', 'beta03_t_stat', 'beta03_p_value', 'beta03_95_conf_int',
                                        'beta04_se', 'beta04_t_stat', 'beta04_p_value', 'beta04_95_conf_int',
                                        'beta05_se', 'beta05_t_stat', 'beta05_p_value', 'beta05_95_conf_int',
                                        'beta06_se', 'beta06_t_stat', 'beta06_p_value', 'beta06_95_conf_int',
                                        'beta07_se', 'beta07_t_stat', 'beta07_p_value', 'beta07_95_conf_int',
                                        'beta08_se', 'beta08_t_stat', 'beta08_p_value', 'beta08_95_conf_int',
                                        'beta09_se', 'beta09_t_stat', 'beta09_p_value', 'beta09_95_conf_int',
                                        'beta10_se', 'beta10_t_stat', 'beta10_p_value', 'beta10_95_conf_int',
                                        ],
                         'classes': ['collapse']}),
        ('Model Stats', {'fields': ['r_squared',
                                    'adj_r_squared',
                                    'p',
                                    'df',
                                    'Yavg',
                                    'SSQres',
                                    'rmse',
                                    'cvrmse',
                                    'nbe',
                                    'F_stat',
                                    'F_stat_p_value',
                                    'autocorr_coeff',
                                    'acceptance_score'],
                         'classes': ['collapse']}),
        ('Relationships',   {'fields':  ['messages'],
                            'classes': ['collapse']}),
    ]
    list_display = ('id', 'meter', 'model_type')
    search_fields = ['id', 'meter', 'model_type']
    list_filter = ['meter', 'model_type']

class EquipmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Equipment Information', {'fields': ['name',
                                              'equipment_type',
                                              'location',
                                              'description']}),
        ('Relationships',   {'fields':  ['meters',
                                         'buildings',
                                         'spaces',
                                         'readers',
                                         'schedule',
                                         'messages']}),
        ('Data Files', {'fields': ['observed_file',
                                  'observed_file_track',
                                  'observed_file_skiprows',
                                  'observed_file_column_for_indexing',
                                  'observed_file_time_zone',
                                  'observed_file_GMT_offset',
                                  'observed_file_adjusts_for_DST',
                                  'provided_file',
                                  'provided_file_track',
                                  'provided_file_skiprows',
                                  'provided_file_column_for_indexing',
                                  'provided_file_time_zone',
                                  'provided_file_GMT_offset',
                                  'provided_file_adjusts_for_DST'],
                        'classes': ['collapse']}),
        ('Image Files', {'fields': ['image_file',
                                    'nameplate_file'],
                         'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'account_name_for_admin', 'equipment_type',
                    'connected_meters_for_admin', 'connected_buildings_for_admin',
                    'connected_spaces_for_admin')
    search_fields = ['name', 'id', 'equipment_type']
    list_filter = ['equipment_type']

class SpaceAdmin(admin.ModelAdmin):
    inlines = (SpaceMeterApportionmentInline,)
    fieldsets = [
        ('Space Information',   {'fields': ['building',
                                            'name',
                                            'space_type',
                                            'EIA_type',
                                            'ESPM_type',
                                            'square_footage',
                                            'max_occupancy']}),
        ('Relationships',   {'fields':  ['readers',
                                         'schedules',
                                         'messages'],
                             'classes': ['collapse']}),
        ('Data Files', {'fields': ['observed_file',
                                  'observed_file_track',
                                  'observed_file_skiprows',
                                  'observed_file_column_for_indexing',
                                  'observed_file_time_zone',
                                  'observed_file_GMT_offset',
                                  'observed_file_adjusts_for_DST',
                                  'provided_file',
                                  'provided_file_track',
                                  'provided_file_skiprows',
                                  'provided_file_column_for_indexing',
                                  'provided_file_time_zone',
                                  'provided_file_GMT_offset',
                                  'provided_file_adjusts_for_DST'],
                        'classes': ['collapse']}),
        ('Image File', {'fields': ['image_file'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'building_name_for_admin', 'account_name_for_admin', 'space_type',
                    'square_footage', 'max_occupancy', 'connected_equipments_for_admin')
    search_fields = ['name', 'id', 'space_type', 'square_footage', 'max_occupancy']
    list_filter = ['space_type']
    
class PackageUnitAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Nameplate',   {'fields': ['name',
                                    'age',
                                    'make',
                                    'model',
                                    'serial_number',
                                    'nameplate_tons',
                                    'nameplate_EER',
                                    'nameplate_MBH_in',
                                    'nameplate_MBH_out',
                                    'nameplate_ng_eta']}),
        ('Details',   {'fields': ['nameplate_V',
                                  'nameplate_phase',
                                  'nameplate_pf',
                                  'nameplate_RFC',
                                  'nameplate_c1_QTY',
                                  'nameplate_c1_RLA',
                                  'nameplate_c1_PH',
                                  'nameplate_c2_QTY',
                                  'nameplate_c2_RLA',
                                  'nameplate_c2_PH',
                                  'nameplate_c3_QTY',
                                  'nameplate_c3_RLA',
                                  'nameplate_c3_PH',
                                  'nameplate_e1_QTY',
                                  'nameplate_e1_PH',
                                  'nameplate_e1_FLA',
                                  'nameplate_e2_QTY',
                                  'nameplate_e2_PH',
                                  'nameplate_e2_FLA',
                                  'nameplate_f1_QTY',
                                  'nameplate_f1_PH',
                                  'nameplate_f1_FLA',
                                  'nameplate_f2_QTY',
                                  'nameplate_f2_PH',
                                  'nameplate_f2_FLA',
                                  ],
                        'classes': ['collapse']}),
        ('Constants', {'fields': ['dP_fan_max',
                                  'dP_fan_min',
                                  'SAF_max',
                                  'SAF_min',
                                  'speed_min',
                                  'T_max',
                                  'T_min',
                                  ],
                        'classes': ['collapse']}),
        ('Parameters', {'fields': ['d', 'm', 'f', 'e'],
                        'classes': ['collapse']}),
        ('Setpoints', {'fields': ['SCOC', 'SCUN', 'SHOC', 'SHUN', 'SRFC'],
                        'classes': ['collapse']}),
        ('Data Files', {'fields': ['observed_file',
                                  'observed_file_track',
                                  'observed_file_skiprows',
                                  'observed_file_column_for_indexing',
                                  'observed_file_time_zone',
                                  'observed_file_GMT_offset',
                                  'observed_file_adjusts_for_DST',
                                  'provided_file',
                                  'provided_file_track',
                                  'provided_file_skiprows',
                                  'provided_file_column_for_indexing',
                                  'provided_file_time_zone',
                                  'provided_file_GMT_offset',
                                  'provided_file_adjusts_for_DST'],
                        'classes': ['collapse']}),
        ('Image Files', {'fields': ['image_file',
                                    'nameplate_file'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'make', 'model', 'age', 'connected_meters_for_admin',
                    'connected_buildings_for_admin', 'connected_spaces_for_admin')
    search_fields = ['name', 'id', 'make', 'model', 'age']
    list_filter = ['make', 'model', 'age']
    
class ReaderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                    'help_text',
                                    'active',
                                    'source',
                                    'column_index',
                                    'column_header',
                                    'expected_min',
                                    'expected_max']}),
    ]
    list_display = ('name', 'id', 'active', 'source', 'column_index', 'column_header',
                    'connected_models_for_admin')
    search_fields = ['name', 'id', 'active', 'source', 'column_index', 'column_header']
    list_filter = ['name', 'active', 'source']
    
class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['when',
                                    'dismissed',
                                    'message_type',
                                    'subject',
                                    'comment',
                                    'notes']}),
    ]
    list_display = ('id', 'when', 'dismissed', 'message_type', 'subject', 'comment',
                    'connected_models_for_admin')
    search_fields = ['id', 'when', 'dismissed', 'message_type', 'subject', 'comment']
    list_filter = ['when', 'dismissed', 'message_type', 'subject']
    
class UnitScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                    'day_of_week_list',
                                    'month_list',
                                    'day_of_month_list',
                                    'hour_list',
                                    'minute_list',
                                    'cron_string']}),
    ]
    list_display = ('name', 'id', 'cron_string', 'connected_operating_schedules_for_admin')
    search_fields = ['name', 'id', 'cron_string']
    list_filter = ['cron_string']
    
class OperatingScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                    'units']}),
    ]
    list_display = ('name', 'id', 'unit_schedules_for_admin', 'connected_models_for_admin')
    search_fields = ['name', 'id']
    
class ReadingAdmin(admin.ModelAdmin): 
    fieldsets = [
        ('Information', {'fields': ['when',
                                    'value']}),
    ]
    list_display = ('id', 'reader', 'when', 'value')
    
class UtilityAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                    'image_file']}),
    ]
    list_display = ('name','id', 'rate_schedules_for_admin')
    search_fields = ['name', 'id']
    
class RateScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['utility',
                                    'name',
                                    'rate_file',
                                    'riders']}),
    ]
    list_display = ('name', 'id', 'utility_name_for_admin', 'connected_meter_names_for_admin',
                    'connected_rider_names_for_admin')
    search_fields = ['name', 'id']
    list_filter = ['utility']
    
class RateScheduleRiderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['utility',
                                    'name',
                                    'rider_file']}),
    ]
    list_display = ('name', 'id', 'utility_name_for_admin', 'connected_rate_names_for_admin')
    search_fields = ['name', 'id']
    list_filter = ['utility']
    
class MontherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['meter',
                                    'name',
                                    'help_text',
                                    'consumption_model',
                                    'peak_demand_model']}),
    ]
    list_display = ('name', 'id', 'help_text', 'meter_for_admin', 'monthlings_for_admin')
    search_fields = ['name', 'id', 'help_text']
    list_filter = ['name', 'help_text']
    
class MonthlingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['monther',
                                    
                                    'when',
                                    'start_date',
                                    'end_date',
                                    
                                    'hdd_peak_demand',
                                    'cdd_peak_demand',
                                    'hdd_consumption',
                                    'cdd_consumption',

                                    'base_billing_demand',
                                    'base_peak_demand',
                                    'base_consumption',
                                    'base_kBtuh_peak_demand',
                                    'base_kBtu_consumption',
                                    'base_cost',

                                    'base_billing_demand_delta',
                                    'base_peak_demand_delta',
                                    'base_consumption_delta',
                                    'base_kBtuh_peak_demand_delta',
                                    'base_kBtu_consumption_delta',
                                    'base_cost_delta',

                                    'exp_billing_demand',
                                    'exp_peak_demand',
                                    'exp_consumption',
                                    'exp_kBtuh_peak_demand',
                                    'exp_kBtu_consumption',
                                    'exp_cost',

                                    'exp_billing_demand_delta',
                                    'exp_peak_demand_delta',
                                    'exp_consumption_delta',
                                    'exp_kBtuh_peak_demand_delta',
                                    'exp_kBtu_consumption_delta',
                                    'exp_cost_delta',

                                    'act_billing_demand',
                                    'act_peak_demand',
                                    'act_consumption',
                                    'act_kBtuh_peak_demand',
                                    'act_kBtu_consumption',
                                    'act_cost',

                                    'esave_billing_demand',
                                    'esave_peak_demand',
                                    'esave_consumption',
                                    'esave_kBtuh_peak_demand',
                                    'esave_kBtu_consumption',
                                    'esave_cost',

                                    'esave_billing_demand_delta',
                                    'esave_peak_demand_delta',
                                    'esave_consumption_delta',
                                    'esave_kBtuh_peak_demand_delta',
                                    'esave_kBtu_consumption_delta',
                                    'esave_cost_delta',

                                    'asave_billing_demand',
                                    'asave_peak_demand',
                                    'asave_consumption',
                                    'asave_kBtuh_peak_demand',
                                    'asave_kBtu_consumption',
                                    'asave_cost',
                                    ]}),
    ]
    list_display = ('id', 'monther_id_for_admin', 'monther_for_admin', 'when', 'base_billing_demand',
                    'base_peak_demand', 'base_consumption', 'base_cost')
    search_fields = ['id', 'when']
    list_filter = ['when']
    
class WeatherStationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                    'description',
                                    'latitude',
                                    'longitude',
                                    'tz_name']}),
        ('Weather Data Date File', {'fields': ['weather_data_import',
                                               'weather_data_upload_file'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'description', 'latitude', 'longitude',
                    'oldest_data_point_for_admin', 'get_duplicates_for_admin',
                    'missing_hours_for_admin', 'connected_buildings_for_admin',
                    'connected_meters_for_admin')
    search_fields = ['name', 'id', 'description', 'latitude', 'longitude']
    list_filter = ['name', 'tz_name']
    
class WeatherDataPointAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['weather_station','time','summary','icon','sunriseTime','sunsetTime',
                                   'precipIntensity','precipIntensityMax',
                                   'precipIntensityMaxTime','precipProbability',
                                   'precipType','precipAccumulation','temperature',
                                   'temperatureMin','temperatureMinTime',
                                   'temperatureMax','temperatureMaxTime','dewPoint',
                                   'windSpeed','windBearing','cloudCover','humidity',
                                   'pressure','visibility','ozone']}),
    ]
    list_display = ('id', 'weather_station_for_admin', 'time',
                    'temperature', 'humidity')
    search_fields = ['id', 'time']
    list_filter = ['weather_station', 'time']

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Profile Information', {'fields': ['user',
                                                 'organization',
                                                 'mobile_phone',
                                                 'desk_phone',
                                                 'image_file']}),
    ]
    list_display = ('user_for_admin', 'user_id_for_admin', 'organization')
    
class GAPowerRiderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                          'percent_of_base_revenue',
                                          'percent_of_total_revenue',
                                          'summer_cost_per_kWh',
                                          'winter_cost_per_kWh',
                                          'apply_to_base_revenue',
                                          'apply_to_total_revenue',
                                          'apply_to_consumption']}),
    ]
    list_display = ('name','percent_of_base_revenue', 'percent_of_total_revenue', 
                    'summer_cost_per_kWh', 'winter_cost_per_kWh', 'apply_to_base_revenue',
                    'apply_to_total_revenue', 'apply_to_consumption')

class GAPowerPandLAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name']}),
        ('General', {'fields': ['use_input_billing_demand',
                                'basic_service_charge',
                                'tax_percentage'],
                     'classes': ['collapse']}),
        ('Tier 1', {'fields': ['tier1', 'tier1a', 'tier1b', 'tier1c', 'tier1d',
                               'rate1a', 'rate1b', 'rate1c', 'rate1d'],
                     'classes': ['collapse']}),
        ('Tier 2', {'fields': ['tier2', 'tier2a', 'tier2b', 'tier2c', 'tier2d',
                               'rate2a', 'rate2b', 'rate2c', 'rate2d'],
                     'classes': ['collapse']}),
        ('Tier 3', {'fields': ['tier3', 'tier3a', 'tier3b', 'tier3c', 'tier3d',
                               'rate3a', 'rate3b', 'rate3c', 'rate3d'],
                     'classes': ['collapse']}),
        ('Tier 4', {'fields': ['tier4', 'tier4a', 'tier4b', 'tier4c', 'tier4d',
                               'rate4a', 'rate4b', 'rate4c', 'rate4d'],
                     'classes': ['collapse']}),
        ('Other', {'fields':   ['excess_kW_threshold',
                                'excess_kW_rate',
                                'window_minutes',
                                'summer_start_month',
                                'summer_end_month',
                                'winter_start_month',
                                'winter_end_month',
                                'billing_demand_sliding_month_window',
                                'summer_summer_threshold',
                                'summer_winter_threshold',
                                'winter_summer_threshold',
                                'winter_winter_threshold',
                                'contract_minimum_demand',
                                'minimum_fraction_contract_capacity',
                                'absolute_minimum_demand',
                                'lim_service_sliding_month_window',
                                'limitation_of_service_max_kW',
                                'limitation_of_service_min_kW',
                                'limitation_of_service_winter_percent',
                                'limitation_of_service_summer_percent'],
                     'classes': ['collapse']}),
    ]
    list_display = ('name',)

class CityOfATLWWWAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                          'tax_percentage',
                                          'tier1',
                                          'tier2',
                                          'tier3',
                                          'rate1',
                                          'rate2',
                                          'rate3',
                                          'security_surcharge']}),
    ]
    list_display = ('name',)

class InfiniteEnergyGAGasAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['name',
                                          'basic_service_charge',
                                          'tax_percentage',
                                          'therm_rate']}),
    ]
    list_display = ('name',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Meter, MeterAdmin)
admin.site.register(MeterConsumptionModel, MeterConsumptionModelAdmin)
admin.site.register(MeterPeakDemandModel, MeterPeakDemandModelAdmin)
admin.site.register(EfficiencyMeasure, EfficiencyMeasureAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Space, SpaceAdmin)
admin.site.register(PackageUnit, PackageUnitAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UnitSchedule, UnitScheduleAdmin)
admin.site.register(OperatingSchedule, OperatingScheduleAdmin)
admin.site.register(Utility, UtilityAdmin)
admin.site.register(RateSchedule, RateScheduleAdmin)
admin.site.register(RateScheduleRider, RateScheduleRiderAdmin)
admin.site.register(Monther, MontherAdmin)
admin.site.register(Monthling, MonthlingAdmin)
admin.site.register(WeatherStation, WeatherStationAdmin)
admin.site.register(WeatherDataPoint, WeatherDataPointAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GAPowerPandL, GAPowerPandLAdmin)
admin.site.register(GAPowerRider, GAPowerRiderAdmin)
admin.site.register(CityOfATLWWW, CityOfATLWWWAdmin)
admin.site.register(InfiniteEnergyGAGas, InfiniteEnergyGAGasAdmin)
