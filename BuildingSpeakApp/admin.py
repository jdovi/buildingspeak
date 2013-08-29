from BuildingSpeakApp.models import Account, Building, Meter, Equipment, Space
from BuildingSpeakApp.models import RooftopUnit, Reader, Reading, Message
from BuildingSpeakApp.models import UnitSchedule, OperatingSchedule, Utility
from BuildingSpeakApp.models import RateSchedule, RateScheduleRider
from BuildingSpeakApp.models import BillingCycler, BillingCycle, Monther, Monthling
from BuildingSpeakApp.models import WeatherStation, WeatherDataPoint, ManagementAction
from BuildingSpeakApp.models import UserProfile
from BuildingSpeakApp.models import GAPowerRider, GAPowerPandL
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account Information', {'fields': ['name',
                                            'account_type',
                                            'street_address',
                                            'city',
                                            'state',
                                            'zip_code',
                                            'launch_date']}),
        ('Contact Details',     {'fields': ['first_name',
                                            'last_name',
                                            'title',
                                            'email',
                                            'phone'],
                                'classes': ['collapse']}),
        ('Billing Information', {'fields': ['status',
                                            'monthly_payment',
                                            'last_invoice_date',
                                            'last_paid_date',
                                            'next_invoice_date',
                                            'bill_addressee',
                                            'bill_email_address',
                                            'bill_street_address',
                                            'bill_city',
                                            'bill_state',
                                            'bill_zip_code',
                                            'bill_to_email',
                                            'bill_to_location'],
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
    list_filter = ['status', 'launch_date', 'last_invoice_date', 'last_paid_date',
                   'next_invoice_date', 'zip_code']
    #date_heirarchy = 'launch_date'
    
class BuildingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Building Information',   {'fields': ['account',
                                               'name',
                                               'street_address',
                                               'city',
                                               'state',
                                               'zip_code',
                                               'weather_station']}),
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

class MeterAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Meter Information',   {'fields': ['account',
                                            'name',
                                            'utility_type',
                                            'utility_account_number',
                                            'utility_meter_number',
                                            'location',
                                            'serves']}),
        ('Nameplate',      {'fields': ['make',
                                       'model',
                                       'serial_number',
                                       'nameplate_file'],
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
        ('Bill Data File', {'fields': ['bill_data_import',
                                       'bill_data_file'],
                        'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'account_name_for_admin', 'utility_account_number',
                    'utility_type', 'units', 'utility_name_for_admin', 'rate_schedule_name_for_admin',
                    'weather_station_name_for_admin', 'connected_building_names_for_admin',
                    'connected_equipment_names_for_admin')
    search_fields = ['name', 'id', 'utility_account_number', 'utility_type', 'units']
    list_filter = ['utility_type', 'units']

class EquipmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Equipment Information', {'fields': ['name',
                                              'equipment_type']}),
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
        ('Nameplate File', {'fields': ['nameplate_file'],
                            'classes': ['collapse']}),
    ]
    list_display = ('name', 'id', 'account_name_for_admin', 'equipment_type',
                    'connected_meters_for_admin', 'connected_buildings_for_admin',
                    'connected_spaces_for_admin')
    search_fields = ['name', 'id', 'equipment_type']
    list_filter = ['equipment_type']

class SpaceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Space Information',   {'fields': ['building',
                                            'name',
                                            'square_footage',
                                            'max_occupancy']}),
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
    
class RooftopUnitAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Nameplate',   {'fields': ['name',
                                    'age',
                                    'make',
                                    'model',
                                    'serial_number',
                                    'nameplate_tons',
                                    'nameplate_EER']}),
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
        ('Nameplate File', {'fields': ['nameplate_file'],
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
        ('Information', {'fields': ['name']}),
    ]
    list_display = ('name', 'id', 'unit_schedules_for_admin', 'connected_models_for_admin')
    search_fields = ['name', 'id']
    
class ReadingAdmin(admin.ModelAdmin): 
    fieldsets = [
        ('Information', {'fields': ['when',
                                    'value']}),
    ]
    list_display = ('id', 'reader', 'when', 'value')
    
#class EventAdmin(admin.ModelAdmin):
#    fieldsets = [
#        ('Information', {'fields': ['name',
#                                    'description',
#                                    'when']}),
#    ]
#    list_display = ('name', 'id', 'description', 'when')
#    search_fields = ['name', 'id', 'description', 'when']
#    list_filter = ['when']
    
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
                                    'rate_file']}),
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

class BillingCyclerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['meter']}),
    ]
    list_display = ('id', 'meter_for_admin', 'billing_cycles_for_admin')
    
class BillingCycleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['period_date',
                                    'start_date',
                                    'end_date']}),
    ]
    list_display = ('id', 'billing_cycler_for_admin', 'period_date', 'start_date', 'end_date')
    search_fields = ['id', 'period_date', 'start_date', 'end_date']
    list_filter = ['period_date', 'start_date', 'end_date']
    
class MontherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['meter',
                                    'name',
                                    'help_text']}),
    ]
    list_display = ('name', 'id', 'help_text', 'meter_for_admin', 'monthlings_for_admin')
    search_fields = ['name', 'id', 'help_text']
    list_filter = ['name', 'help_text']
    
class MonthlingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information', {'fields': ['when',
                                    'base_billing_demand',
                                    'base_peak_demand',
                                    'base_consumption',
                                    'base_kBtuh_peak_demand',
                                    'base_kBtu_consumption',
                                    'base_cost',
                                    'exp_billing_demand',
                                    'exp_peak_demand',
                                    'exp_consumption',
                                    'exp_kBtuh_peak_demand',
                                    'exp_kBtu_consumption',
                                    'exp_cost',
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
                    'oldest_data_point_for_admin', 'connected_buildings_for_admin',
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

class ManagementActionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Upload New Model Info', {'fields': ['load_model_data',
                                              'model_data_file_for_upload']}),
        ('Create Import Template', {'fields': ['create_a_new_import_file']}),
    ]
    list_display = ('name', 'latest_messages_for_admin')

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Profile Information', {'fields': ['user',
                                                 'organization',
                                                 'image_file']}),
    ]
    list_display = ('user_for_admin', 'user_id_for_admin', 'organization')
    
class GAPowerRiderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rider Information', {'fields': ['name',
                                          'percent_of_base_revenue',
                                          'percent_of_total_revenue',
                                          'summer_cost_per_kWh',
                                          'winter_cost_per_kWh',
                                          'apply_to_base_revenue',
                                          'apply_to_total_revenue',
                                          'apply_to_consumption']}),
    ]
    list_display = ('name',)

class GAPowerPandLAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rider Information', {'fields': ['name',
                                          'basic_service_charge',
                                          'tax_percentage']}),
    ]
    list_display = ('name',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Meter, MeterAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Space, SpaceAdmin)
admin.site.register(RooftopUnit, RooftopUnitAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UnitSchedule, UnitScheduleAdmin)
admin.site.register(OperatingSchedule, OperatingScheduleAdmin)
admin.site.register(Utility, UtilityAdmin)
admin.site.register(RateSchedule, RateScheduleAdmin)
admin.site.register(RateScheduleRider, RateScheduleRiderAdmin)
admin.site.register(BillingCycler, BillingCyclerAdmin)
admin.site.register(BillingCycle, BillingCycleAdmin)
admin.site.register(Monther, MontherAdmin)
admin.site.register(Monthling, MonthlingAdmin)
admin.site.register(WeatherStation, WeatherStationAdmin)
admin.site.register(WeatherDataPoint, WeatherDataPointAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GAPowerPandL, GAPowerPandLAdmin)
admin.site.register(GAPowerRider, GAPowerRiderAdmin)
