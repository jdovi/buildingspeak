# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('BuildingSpeakApp_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dismissed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('message_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Message'])

        # Adding model 'Monther'
        db.create_table('BuildingSpeakApp_monther', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('consumption_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.MeterConsumptionModel'], null=True)),
            ('peak_demand_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.MeterPeakDemandModel'], null=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Monther'])

        # Adding M2M table for field messages on 'Monther'
        db.create_table('BuildingSpeakApp_monther_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monther', models.ForeignKey(orm['BuildingSpeakApp.monther'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_monther_messages', ['monther_id', 'message_id'])

        # Adding model 'Monthling'
        db.create_table('BuildingSpeakApp_monthling', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('hdd_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('cdd_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('hdd_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('cdd_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_billing_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_kBtuh_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_kBtu_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_billing_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_peak_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_consumption_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_kBtuh_peak_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_kBtu_consumption_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('base_cost_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_billing_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_kBtuh_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_kBtu_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_billing_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_peak_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_consumption_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_kBtuh_peak_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_kBtu_consumption_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('exp_cost_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('act_billing_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('act_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('act_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('act_kBtuh_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('act_kBtu_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('act_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_billing_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_kBtuh_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_kBtu_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_billing_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_peak_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_consumption_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_kBtuh_peak_demand_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_kBtu_consumption_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('esave_cost_delta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('asave_billing_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('asave_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('asave_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('asave_kBtuh_peak_demand', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('asave_kBtu_consumption', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('asave_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('monther', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Monther'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Monthling'])

        # Adding model 'Reader'
        db.create_table('BuildingSpeakApp_reader', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('column_index', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('column_header', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('expected_min', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('expected_max', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Reader'])

        # Adding M2M table for field messages on 'Reader'
        db.create_table('BuildingSpeakApp_reader_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_reader_messages', ['reader_id', 'message_id'])

        # Adding model 'Reading'
        db.create_table('BuildingSpeakApp_reading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('reader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Reader'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Reading'])

        # Adding model 'SpaceMeterApportionment'
        db.create_table('BuildingSpeakApp_spacemeterapportionment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Space'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['SpaceMeterApportionment'])

        # Adding model 'Space'
        db.create_table('BuildingSpeakApp_space', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Building'])),
            ('observed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('observed_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('observed_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('observed_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('observed_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('provided_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('provided_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('provided_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('square_footage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_occupancy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('space_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('EIA_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('ESPM_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Space'])

        # Adding M2M table for field messages on 'Space'
        db.create_table('BuildingSpeakApp_space_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_space_messages', ['space_id', 'message_id'])

        # Adding M2M table for field readers on 'Space'
        db.create_table('BuildingSpeakApp_space_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_space_readers', ['space_id', 'reader_id'])

        # Adding M2M table for field schedules on 'Space'
        db.create_table('BuildingSpeakApp_space_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_space_schedules', ['space_id', 'operatingschedule_id'])

        # Adding model 'Account'
        db.create_table('BuildingSpeakApp_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('observed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('observed_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('observed_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('observed_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('observed_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('provided_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('provided_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('provided_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('launch_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('monthly_payment', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('stripe_customer_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Account'])

        # Adding M2M table for field messages on 'Account'
        db.create_table('BuildingSpeakApp_account_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_account_messages', ['account_id', 'message_id'])

        # Adding M2M table for field users on 'Account'
        db.create_table('BuildingSpeakApp_account_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_account_users', ['account_id', 'user_id'])

        # Adding M2M table for field readers on 'Account'
        db.create_table('BuildingSpeakApp_account_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_account_readers', ['account_id', 'reader_id'])

        # Adding M2M table for field schedules on 'Account'
        db.create_table('BuildingSpeakApp_account_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_account_schedules', ['account_id', 'operatingschedule_id'])

        # Adding model 'BuildingMeterApportionment'
        db.create_table('BuildingSpeakApp_buildingmeterapportionment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Building'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['BuildingMeterApportionment'])

        # Adding model 'Building'
        db.create_table('BuildingSpeakApp_building', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('building_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('EIA_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('ESPM_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Account'])),
            ('weather_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.WeatherStation'])),
            ('observed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('observed_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('observed_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('observed_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('observed_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('provided_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('provided_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('provided_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('square_footage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stories', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_occupancy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Building'])

        # Adding M2M table for field messages on 'Building'
        db.create_table('BuildingSpeakApp_building_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_building_messages', ['building_id', 'message_id'])

        # Adding M2M table for field readers on 'Building'
        db.create_table('BuildingSpeakApp_building_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_building_readers', ['building_id', 'reader_id'])

        # Adding M2M table for field schedules on 'Building'
        db.create_table('BuildingSpeakApp_building_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_building_schedules', ['building_id', 'operatingschedule_id'])

        # Adding model 'EMMeterApportionment'
        db.create_table('BuildingSpeakApp_emmeterapportionment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('efficiency_measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.EfficiencyMeasure'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['EMMeterApportionment'])

        # Adding model 'EMEquipmentApportionment'
        db.create_table('BuildingSpeakApp_emequipmentapportionment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('equipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Equipment'])),
            ('efficiency_measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.EfficiencyMeasure'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['EMEquipmentApportionment'])

        # Adding model 'EfficiencyMeasure'
        db.create_table('BuildingSpeakApp_efficiencymeasure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('annual_consumption_savings', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('peak_demand_savings', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('annual_cost_savings', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('percent_uncertainty', self.gf('django.db.models.fields.DecimalField')(default='0.01000000000000000020816681711721685132943093776702880859375', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('percent_cool', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('percent_heat', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('percent_flat', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('percent_fixed', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('utility_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('jan_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('feb_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('mar_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('apr_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('may_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jun_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jul_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('aug_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('sep_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('oct_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nov_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('dec_cons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jan_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('feb_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('mar_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('apr_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('may_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jun_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jul_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('aug_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('sep_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('oct_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nov_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('dec_peak', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jan_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('feb_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('mar_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('apr_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('may_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jun_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('jul_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('aug_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('sep_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('oct_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nov_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('dec_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('weather_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.WeatherStation'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['EfficiencyMeasure'])

        # Adding M2M table for field messages on 'EfficiencyMeasure'
        db.create_table('BuildingSpeakApp_efficiencymeasure_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('efficiencymeasure', models.ForeignKey(orm['BuildingSpeakApp.efficiencymeasure'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_efficiencymeasure_messages', ['efficiencymeasure_id', 'message_id'])

        # Adding model 'Equipment'
        db.create_table('BuildingSpeakApp_equipment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.OperatingSchedule'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('equipment_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('observed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('observed_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('observed_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('observed_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('observed_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('provided_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('provided_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('provided_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('nameplate_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Equipment'])

        # Adding M2M table for field messages on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_messages', ['equipment_id', 'message_id'])

        # Adding M2M table for field meters on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_meters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_meters', ['equipment_id', 'meter_id'])

        # Adding M2M table for field buildings on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_buildings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_buildings', ['equipment_id', 'building_id'])

        # Adding M2M table for field spaces on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_spaces', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_spaces', ['equipment_id', 'space_id'])

        # Adding M2M table for field readers on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_readers', ['equipment_id', 'reader_id'])

        # Adding model 'Meter'
        db.create_table('BuildingSpeakApp_meter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('utility_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('serves', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('weather_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.WeatherStation'])),
            ('utility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Utility'])),
            ('rate_schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.RateSchedule'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Account'])),
            ('observed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('observed_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('observed_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observed_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('observed_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('observed_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('provided_file_track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provided_file_skiprows', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_column_for_indexing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('provided_file_time_zone', self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=200, blank=True)),
            ('provided_file_GMT_offset', self.gf('django.db.models.fields.DecimalField')(default='-5', null=True, max_digits=4, decimal_places=2, blank=True)),
            ('provided_file_adjusts_for_DST', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('nameplate_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('bill_data_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('bill_data_import', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('utility_account_number', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('utility_meter_number', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Meter'])

        # Adding M2M table for field messages on 'Meter'
        db.create_table('BuildingSpeakApp_meter_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meter_messages', ['meter_id', 'message_id'])

        # Adding M2M table for field readers on 'Meter'
        db.create_table('BuildingSpeakApp_meter_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meter_readers', ['meter_id', 'reader_id'])

        # Adding M2M table for field schedules on 'Meter'
        db.create_table('BuildingSpeakApp_meter_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meter_schedules', ['meter_id', 'operatingschedule_id'])

        # Adding model 'MeterConsumptionModel'
        db.create_table('BuildingSpeakApp_meterconsumptionmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('first_month', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('last_month', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('Tccp', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('Thcp', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prediction_alpha', self.gf('django.db.models.fields.FloatField')(default=0.1, null=True, blank=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'], null=True)),
            ('beta00p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta01v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta02v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta03v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta04v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta05v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta06v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta07v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta08v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta09v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta10v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('r_squared', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('adj_r_squared', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('df', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('Yavg', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('SSQres', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rmse', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cvrmse', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('nbe', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('F_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('F_stat_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('autocorr_coeff', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('acceptance_score', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['MeterConsumptionModel'])

        # Adding M2M table for field messages on 'MeterConsumptionModel'
        db.create_table('BuildingSpeakApp_meterconsumptionmodel_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meterconsumptionmodel', models.ForeignKey(orm['BuildingSpeakApp.meterconsumptionmodel'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meterconsumptionmodel_messages', ['meterconsumptionmodel_id', 'message_id'])

        # Adding model 'MeterPeakDemandModel'
        db.create_table('BuildingSpeakApp_meterpeakdemandmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('first_month', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('last_month', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('Tccp', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('Thcp', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prediction_alpha', self.gf('django.db.models.fields.FloatField')(default=0.1, null=True, blank=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'], null=True)),
            ('beta00p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta01v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta02v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta03v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta04v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta05v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta06v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta07v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta08v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta09v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('beta10v', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('r_squared', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('adj_r_squared', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('df', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('Yavg', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('SSQres', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rmse', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cvrmse', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('nbe', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('F_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('F_stat_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('autocorr_coeff', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('acceptance_score', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta00_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta01_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta02_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta03_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta04_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta05_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta06_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta07_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta08_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta09_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_se', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_t_stat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_p_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('beta10_95_conf_int', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['MeterPeakDemandModel'])

        # Adding M2M table for field messages on 'MeterPeakDemandModel'
        db.create_table('BuildingSpeakApp_meterpeakdemandmodel_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meterpeakdemandmodel', models.ForeignKey(orm['BuildingSpeakApp.meterpeakdemandmodel'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meterpeakdemandmodel_messages', ['meterpeakdemandmodel_id', 'message_id'])

        # Adding model 'RateSchedule'
        db.create_table('BuildingSpeakApp_rateschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_my_subclass', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('utility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Utility'])),
            ('rate_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['RateSchedule'])

        # Adding M2M table for field riders on 'RateSchedule'
        db.create_table('BuildingSpeakApp_rateschedule_riders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rateschedule', models.ForeignKey(orm['BuildingSpeakApp.rateschedule'], null=False)),
            ('rateschedulerider', models.ForeignKey(orm['BuildingSpeakApp.rateschedulerider'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_rateschedule_riders', ['rateschedule_id', 'rateschedulerider_id'])

        # Adding M2M table for field messages on 'RateSchedule'
        db.create_table('BuildingSpeakApp_rateschedule_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rateschedule', models.ForeignKey(orm['BuildingSpeakApp.rateschedule'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_rateschedule_messages', ['rateschedule_id', 'message_id'])

        # Adding model 'RateScheduleRider'
        db.create_table('BuildingSpeakApp_rateschedulerider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_my_subclass', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('utility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Utility'])),
            ('rider_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['RateScheduleRider'])

        # Adding M2M table for field messages on 'RateScheduleRider'
        db.create_table('BuildingSpeakApp_rateschedulerider_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rateschedulerider', models.ForeignKey(orm['BuildingSpeakApp.rateschedulerider'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_rateschedulerider_messages', ['rateschedulerider_id', 'message_id'])

        # Adding model 'GAPowerPandL'
        db.create_table('BuildingSpeakApp_gapowerpandl', (
            ('rateschedule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['BuildingSpeakApp.RateSchedule'], unique=True, primary_key=True)),
            ('use_input_billing_demand', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('basic_service_charge', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tax_percentage', self.gf('django.db.models.fields.DecimalField')(default='0.08000000000000000166533453693773481063544750213623046875', null=True, max_digits=10, decimal_places=7, blank=True)),
            ('tier1', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier1a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier1b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier1c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier1d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier2', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier2a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier2b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier2c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier2d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier3', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier3a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier3b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier3c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier3d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier4', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier4a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier4b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier4c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier4d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate1a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate1b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate1c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate1d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate2a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate2b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate2c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate2d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate3a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate3b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate3c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate3d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate4a', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate4b', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate4c', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate4d', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('excess_kW_threshold', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('excess_kW_rate', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('window_minutes', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('summer_start_month', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('summer_end_month', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('winter_start_month', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('winter_end_month', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('billing_demand_sliding_month_window', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('summer_summer_threshold', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('summer_winter_threshold', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('winter_summer_threshold', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('winter_winter_threshold', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('contract_minimum_demand', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('minimum_fraction_contract_capacity', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('absolute_minimum_demand', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('lim_service_sliding_month_window', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('limitation_of_service_max_kW', self.gf('django.db.models.fields.DecimalField')(default='999999', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('limitation_of_service_min_kW', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('limitation_of_service_winter_percent', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('limitation_of_service_summer_percent', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['GAPowerPandL'])

        # Adding model 'GAPowerRider'
        db.create_table('BuildingSpeakApp_gapowerrider', (
            ('rateschedulerider_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['BuildingSpeakApp.RateScheduleRider'], unique=True, primary_key=True)),
            ('percent_of_base_revenue', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=10, decimal_places=9, blank=True)),
            ('percent_of_total_revenue', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=10, decimal_places=9, blank=True)),
            ('summer_cost_per_kWh', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=7, blank=True)),
            ('winter_cost_per_kWh', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=7, blank=True)),
            ('apply_to_base_revenue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('apply_to_total_revenue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('apply_to_consumption', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['GAPowerRider'])

        # Adding model 'InfiniteEnergyGAGas'
        db.create_table('BuildingSpeakApp_infiniteenergygagas', (
            ('rateschedule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['BuildingSpeakApp.RateSchedule'], unique=True, primary_key=True)),
            ('basic_service_charge', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tax_percentage', self.gf('django.db.models.fields.DecimalField')(default='0.08000000000000000166533453693773481063544750213623046875', null=True, max_digits=10, decimal_places=7, blank=True)),
            ('therm_rate', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['InfiniteEnergyGAGas'])

        # Adding model 'CityOfATLWWW'
        db.create_table('BuildingSpeakApp_cityofatlwww', (
            ('rateschedule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['BuildingSpeakApp.RateSchedule'], unique=True, primary_key=True)),
            ('base_charge', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tax_percentage', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=10, decimal_places=7, blank=True)),
            ('tier1', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier2', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('tier3', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate1', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate2', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('rate3', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('security_surcharge', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['CityOfATLWWW'])

        # Adding model 'RooftopUnit'
        db.create_table('BuildingSpeakApp_rooftopunit', (
            ('equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['BuildingSpeakApp.Equipment'], unique=True, primary_key=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('nameplate_tons', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_EER', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('nameplate_MBH_in', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_MBH_out', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_ng_eta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
            ('nameplate_V', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_phase', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_pf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_RFC', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c1_QTY', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c1_RLA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c1_PH', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c2_QTY', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c2_RLA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c2_PH', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c3_QTY', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c3_RLA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_c3_PH', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_e1_QTY', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_e1_PH', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_e1_FLA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_e2_QTY', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_e2_PH', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_e2_FLA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_f1_QTY', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_f1_PH', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_f1_FLA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_f2_QTY', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_f2_PH', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('nameplate_f2_FLA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('dP_fan_max', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('dP_fan_min', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('SAF_max', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('SAF_min', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('speed_min', self.gf('django.db.models.fields.DecimalField')(default='0.200000000000000011102230246251565404236316680908203125', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('T_max', self.gf('django.db.models.fields.DecimalField')(default='150', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('T_min', self.gf('django.db.models.fields.DecimalField')(default='-50', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('d', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='decimal', null=True, blank=True)),
            ('m', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='decimal', null=True, blank=True)),
            ('f', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='decimal', null=True, blank=True)),
            ('e', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='decimal', null=True, blank=True)),
            ('SCOC', self.gf('django.db.models.fields.DecimalField')(default='72', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('SCUN', self.gf('django.db.models.fields.DecimalField')(default='80', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('SHOC', self.gf('django.db.models.fields.DecimalField')(default='68', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('SHUN', self.gf('django.db.models.fields.DecimalField')(default='60', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('SRFC', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['RooftopUnit'])

        # Adding model 'UnitSchedule'
        db.create_table('BuildingSpeakApp_unitschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cron_string', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('day_of_week_list', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='text', null=True, blank=True)),
            ('month_list', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='text', null=True, blank=True)),
            ('day_of_month_list', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='text', null=True, blank=True)),
            ('hour_list', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='text', null=True, blank=True)),
            ('minute_list', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='text', null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['UnitSchedule'])

        # Adding M2M table for field messages on 'UnitSchedule'
        db.create_table('BuildingSpeakApp_unitschedule_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unitschedule', models.ForeignKey(orm['BuildingSpeakApp.unitschedule'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_unitschedule_messages', ['unitschedule_id', 'message_id'])

        # Adding model 'OperatingSchedule'
        db.create_table('BuildingSpeakApp_operatingschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['OperatingSchedule'])

        # Adding M2M table for field messages on 'OperatingSchedule'
        db.create_table('BuildingSpeakApp_operatingschedule_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_operatingschedule_messages', ['operatingschedule_id', 'message_id'])

        # Adding M2M table for field units on 'OperatingSchedule'
        db.create_table('BuildingSpeakApp_operatingschedule_units', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False)),
            ('unitschedule', models.ForeignKey(orm['BuildingSpeakApp.unitschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_operatingschedule_units', ['operatingschedule_id', 'unitschedule_id'])

        # Adding model 'Utility'
        db.create_table('BuildingSpeakApp_utility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Utility'])

        # Adding M2M table for field messages on 'Utility'
        db.create_table('BuildingSpeakApp_utility_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('utility', models.ForeignKey(orm['BuildingSpeakApp.utility'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_utility_messages', ['utility_id', 'message_id'])

        # Adding model 'UserProfile'
        db.create_table('BuildingSpeakApp_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('mobile_phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('desk_phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['UserProfile'])

        # Adding M2M table for field messages on 'UserProfile'
        db.create_table('BuildingSpeakApp_userprofile_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['BuildingSpeakApp.userprofile'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_userprofile_messages', ['userprofile_id', 'message_id'])

        # Adding model 'WeatherStation'
        db.create_table('BuildingSpeakApp_weatherstation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=7)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=7)),
            ('tz_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('weather_data_import', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('weather_data_upload_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['WeatherStation'])

        # Adding M2M table for field messages on 'WeatherStation'
        db.create_table('BuildingSpeakApp_weatherstation_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('weatherstation', models.ForeignKey(orm['BuildingSpeakApp.weatherstation'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_weatherstation_messages', ['weatherstation_id', 'message_id'])

        # Adding model 'WeatherDataPoint'
        db.create_table('BuildingSpeakApp_weatherdatapoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('sunriseTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sunsetTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('precipIntensity', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('precipIntensityMax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('precipIntensityMaxTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('precipProbability', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('precipType', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('precipAccumulation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('temperature', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('temperatureMin', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('temperatureMinTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('temperatureMax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('temperatureMaxTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dewPoint', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('windSpeed', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('windBearing', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('cloudCover', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('humidity', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('pressure', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('visibility', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('ozone', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('weather_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.WeatherStation'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['WeatherDataPoint'])

        # Adding model 'ManagementAction'
        db.create_table('BuildingSpeakApp_managementaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Click this link to perform management actions', max_length=200)),
            ('create_a_new_import_file', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('import_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('load_model_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('model_data_file_for_upload', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('processed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['ManagementAction'])

        # Adding M2M table for field messages on 'ManagementAction'
        db.create_table('BuildingSpeakApp_managementaction_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('managementaction', models.ForeignKey(orm['BuildingSpeakApp.managementaction'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_managementaction_messages', ['managementaction_id', 'message_id'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('BuildingSpeakApp_message')

        # Deleting model 'Monther'
        db.delete_table('BuildingSpeakApp_monther')

        # Removing M2M table for field messages on 'Monther'
        db.delete_table('BuildingSpeakApp_monther_messages')

        # Deleting model 'Monthling'
        db.delete_table('BuildingSpeakApp_monthling')

        # Deleting model 'Reader'
        db.delete_table('BuildingSpeakApp_reader')

        # Removing M2M table for field messages on 'Reader'
        db.delete_table('BuildingSpeakApp_reader_messages')

        # Deleting model 'Reading'
        db.delete_table('BuildingSpeakApp_reading')

        # Deleting model 'SpaceMeterApportionment'
        db.delete_table('BuildingSpeakApp_spacemeterapportionment')

        # Deleting model 'Space'
        db.delete_table('BuildingSpeakApp_space')

        # Removing M2M table for field messages on 'Space'
        db.delete_table('BuildingSpeakApp_space_messages')

        # Removing M2M table for field readers on 'Space'
        db.delete_table('BuildingSpeakApp_space_readers')

        # Removing M2M table for field schedules on 'Space'
        db.delete_table('BuildingSpeakApp_space_schedules')

        # Deleting model 'Account'
        db.delete_table('BuildingSpeakApp_account')

        # Removing M2M table for field messages on 'Account'
        db.delete_table('BuildingSpeakApp_account_messages')

        # Removing M2M table for field users on 'Account'
        db.delete_table('BuildingSpeakApp_account_users')

        # Removing M2M table for field readers on 'Account'
        db.delete_table('BuildingSpeakApp_account_readers')

        # Removing M2M table for field schedules on 'Account'
        db.delete_table('BuildingSpeakApp_account_schedules')

        # Deleting model 'BuildingMeterApportionment'
        db.delete_table('BuildingSpeakApp_buildingmeterapportionment')

        # Deleting model 'Building'
        db.delete_table('BuildingSpeakApp_building')

        # Removing M2M table for field messages on 'Building'
        db.delete_table('BuildingSpeakApp_building_messages')

        # Removing M2M table for field readers on 'Building'
        db.delete_table('BuildingSpeakApp_building_readers')

        # Removing M2M table for field schedules on 'Building'
        db.delete_table('BuildingSpeakApp_building_schedules')

        # Deleting model 'EMMeterApportionment'
        db.delete_table('BuildingSpeakApp_emmeterapportionment')

        # Deleting model 'EMEquipmentApportionment'
        db.delete_table('BuildingSpeakApp_emequipmentapportionment')

        # Deleting model 'EfficiencyMeasure'
        db.delete_table('BuildingSpeakApp_efficiencymeasure')

        # Removing M2M table for field messages on 'EfficiencyMeasure'
        db.delete_table('BuildingSpeakApp_efficiencymeasure_messages')

        # Deleting model 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment')

        # Removing M2M table for field messages on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_messages')

        # Removing M2M table for field meters on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_meters')

        # Removing M2M table for field buildings on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_buildings')

        # Removing M2M table for field spaces on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_spaces')

        # Removing M2M table for field readers on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_readers')

        # Deleting model 'Meter'
        db.delete_table('BuildingSpeakApp_meter')

        # Removing M2M table for field messages on 'Meter'
        db.delete_table('BuildingSpeakApp_meter_messages')

        # Removing M2M table for field readers on 'Meter'
        db.delete_table('BuildingSpeakApp_meter_readers')

        # Removing M2M table for field schedules on 'Meter'
        db.delete_table('BuildingSpeakApp_meter_schedules')

        # Deleting model 'MeterConsumptionModel'
        db.delete_table('BuildingSpeakApp_meterconsumptionmodel')

        # Removing M2M table for field messages on 'MeterConsumptionModel'
        db.delete_table('BuildingSpeakApp_meterconsumptionmodel_messages')

        # Deleting model 'MeterPeakDemandModel'
        db.delete_table('BuildingSpeakApp_meterpeakdemandmodel')

        # Removing M2M table for field messages on 'MeterPeakDemandModel'
        db.delete_table('BuildingSpeakApp_meterpeakdemandmodel_messages')

        # Deleting model 'RateSchedule'
        db.delete_table('BuildingSpeakApp_rateschedule')

        # Removing M2M table for field riders on 'RateSchedule'
        db.delete_table('BuildingSpeakApp_rateschedule_riders')

        # Removing M2M table for field messages on 'RateSchedule'
        db.delete_table('BuildingSpeakApp_rateschedule_messages')

        # Deleting model 'RateScheduleRider'
        db.delete_table('BuildingSpeakApp_rateschedulerider')

        # Removing M2M table for field messages on 'RateScheduleRider'
        db.delete_table('BuildingSpeakApp_rateschedulerider_messages')

        # Deleting model 'GAPowerPandL'
        db.delete_table('BuildingSpeakApp_gapowerpandl')

        # Deleting model 'GAPowerRider'
        db.delete_table('BuildingSpeakApp_gapowerrider')

        # Deleting model 'InfiniteEnergyGAGas'
        db.delete_table('BuildingSpeakApp_infiniteenergygagas')

        # Deleting model 'CityOfATLWWW'
        db.delete_table('BuildingSpeakApp_cityofatlwww')

        # Deleting model 'RooftopUnit'
        db.delete_table('BuildingSpeakApp_rooftopunit')

        # Deleting model 'UnitSchedule'
        db.delete_table('BuildingSpeakApp_unitschedule')

        # Removing M2M table for field messages on 'UnitSchedule'
        db.delete_table('BuildingSpeakApp_unitschedule_messages')

        # Deleting model 'OperatingSchedule'
        db.delete_table('BuildingSpeakApp_operatingschedule')

        # Removing M2M table for field messages on 'OperatingSchedule'
        db.delete_table('BuildingSpeakApp_operatingschedule_messages')

        # Removing M2M table for field units on 'OperatingSchedule'
        db.delete_table('BuildingSpeakApp_operatingschedule_units')

        # Deleting model 'Utility'
        db.delete_table('BuildingSpeakApp_utility')

        # Removing M2M table for field messages on 'Utility'
        db.delete_table('BuildingSpeakApp_utility_messages')

        # Deleting model 'UserProfile'
        db.delete_table('BuildingSpeakApp_userprofile')

        # Removing M2M table for field messages on 'UserProfile'
        db.delete_table('BuildingSpeakApp_userprofile_messages')

        # Deleting model 'WeatherStation'
        db.delete_table('BuildingSpeakApp_weatherstation')

        # Removing M2M table for field messages on 'WeatherStation'
        db.delete_table('BuildingSpeakApp_weatherstation_messages')

        # Deleting model 'WeatherDataPoint'
        db.delete_table('BuildingSpeakApp_weatherdatapoint')

        # Deleting model 'ManagementAction'
        db.delete_table('BuildingSpeakApp_managementaction')

        # Removing M2M table for field messages on 'ManagementAction'
        db.delete_table('BuildingSpeakApp_managementaction_messages')


    models = {
        'BuildingSpeakApp.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'launch_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'monthly_payment': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'observed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'observed_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'observed_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'observed_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'observed_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'provided_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provided_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'provided_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'provided_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Reader']", 'symmetrical': 'False'}),
            'schedules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'BuildingSpeakApp.building': {
            'EIA_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ESPM_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'Building'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Account']"}),
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'building_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'max_occupancy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Meter']", 'through': "orm['BuildingSpeakApp.BuildingMeterApportionment']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'observed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'observed_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'observed_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'observed_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'observed_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'provided_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provided_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'provided_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'provided_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Reader']", 'symmetrical': 'False'}),
            'schedules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']", 'symmetrical': 'False'}),
            'square_footage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'stories': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weather_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.WeatherStation']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'BuildingSpeakApp.buildingmeterapportionment': {
            'Meta': {'object_name': 'BuildingMeterApportionment'},
            'assigned_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"})
        },
        'BuildingSpeakApp.cityofatlwww': {
            'Meta': {'object_name': 'CityOfATLWWW', '_ormbases': ['BuildingSpeakApp.RateSchedule']},
            'base_charge': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate1': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate2': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate3': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rateschedule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['BuildingSpeakApp.RateSchedule']", 'unique': 'True', 'primary_key': 'True'}),
            'security_surcharge': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tax_percentage': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'tier1': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier2': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier3': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'})
        },
        'BuildingSpeakApp.efficiencymeasure': {
            'Meta': {'object_name': 'EfficiencyMeasure'},
            'annual_consumption_savings': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'annual_cost_savings': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'apr_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'apr_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'apr_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'aug_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'aug_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'aug_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dec_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dec_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dec_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'equipments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Equipment']", 'through': "orm['BuildingSpeakApp.EMEquipmentApportionment']", 'symmetrical': 'False'}),
            'feb_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'feb_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'feb_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jan_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jan_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jan_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jul_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jul_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jul_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jun_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jun_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'jun_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'mar_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'mar_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'mar_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'may_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'may_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'may_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Meter']", 'through': "orm['BuildingSpeakApp.EMMeterApportionment']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nov_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nov_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nov_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'oct_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'oct_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'oct_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'peak_demand_savings': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_cool': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_fixed': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_flat': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_heat': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_uncertainty': ('django.db.models.fields.DecimalField', [], {'default': "'0.01000000000000000020816681711721685132943093776702880859375'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'sep_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'sep_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'sep_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weather_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.WeatherStation']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.emequipmentapportionment': {
            'Meta': {'object_name': 'EMEquipmentApportionment'},
            'assigned_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'efficiency_measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.EfficiencyMeasure']"}),
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Equipment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'BuildingSpeakApp.emmeterapportionment': {
            'Meta': {'object_name': 'EMMeterApportionment'},
            'assigned_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'efficiency_measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.EfficiencyMeasure']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"})
        },
        'BuildingSpeakApp.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'buildings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Building']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'equipment_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Meter']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nameplate_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'observed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'observed_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'observed_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'observed_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'observed_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provided_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'provided_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'provided_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Reader']", 'symmetrical': 'False'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']", 'null': 'True', 'blank': 'True'}),
            'spaces': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Space']", 'symmetrical': 'False'})
        },
        'BuildingSpeakApp.gapowerpandl': {
            'Meta': {'object_name': 'GAPowerPandL', '_ormbases': ['BuildingSpeakApp.RateSchedule']},
            'absolute_minimum_demand': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'basic_service_charge': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'billing_demand_sliding_month_window': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'contract_minimum_demand': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'excess_kW_rate': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'excess_kW_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'lim_service_sliding_month_window': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'limitation_of_service_max_kW': ('django.db.models.fields.DecimalField', [], {'default': "'999999'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'limitation_of_service_min_kW': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'limitation_of_service_summer_percent': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'limitation_of_service_winter_percent': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'minimum_fraction_contract_capacity': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate1a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate1b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate1c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate1d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate2a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate2b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate2c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate2d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate3a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate3b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate3c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate3d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate4a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate4b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate4c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rate4d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rateschedule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['BuildingSpeakApp.RateSchedule']", 'unique': 'True', 'primary_key': 'True'}),
            'summer_end_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'summer_start_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'summer_summer_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'summer_winter_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tax_percentage': ('django.db.models.fields.DecimalField', [], {'default': "'0.08000000000000000166533453693773481063544750213623046875'", 'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'tier1': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier1a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier1b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier1c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier1d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier2': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier2a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier2b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier2c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier2d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier3': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier3a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier3b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier3c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier3d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier4': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier4a': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier4b': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier4c': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'tier4d': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'use_input_billing_demand': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'window_minutes': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_end_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_start_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_summer_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_winter_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'})
        },
        'BuildingSpeakApp.gapowerrider': {
            'Meta': {'object_name': 'GAPowerRider', '_ormbases': ['BuildingSpeakApp.RateScheduleRider']},
            'apply_to_base_revenue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'apply_to_consumption': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'apply_to_total_revenue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'percent_of_base_revenue': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'percent_of_total_revenue': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'rateschedulerider_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['BuildingSpeakApp.RateScheduleRider']", 'unique': 'True', 'primary_key': 'True'}),
            'summer_cost_per_kWh': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '7', 'blank': 'True'}),
            'winter_cost_per_kWh': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '7', 'blank': 'True'})
        },
        'BuildingSpeakApp.infiniteenergygagas': {
            'Meta': {'object_name': 'InfiniteEnergyGAGas', '_ormbases': ['BuildingSpeakApp.RateSchedule']},
            'basic_service_charge': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'rateschedule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['BuildingSpeakApp.RateSchedule']", 'unique': 'True', 'primary_key': 'True'}),
            'tax_percentage': ('django.db.models.fields.DecimalField', [], {'default': "'0.08000000000000000166533453693773481063544750213623046875'", 'null': 'True', 'max_digits': '10', 'decimal_places': '7', 'blank': 'True'}),
            'therm_rate': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'})
        },
        'BuildingSpeakApp.managementaction': {
            'Meta': {'object_name': 'ManagementAction'},
            'create_a_new_import_file': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'load_model_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'model_data_file_for_upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Click this link to perform management actions'", 'max_length': '200'}),
            'processed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.message': {
            'Meta': {'object_name': 'Message'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dismissed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.meter': {
            'Meta': {'object_name': 'Meter'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Account']"}),
            'bill_data_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bill_data_import': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nameplate_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'observed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'observed_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'observed_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'observed_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'observed_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provided_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'provided_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'provided_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rate_schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.RateSchedule']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Reader']", 'symmetrical': 'False'}),
            'schedules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']", 'symmetrical': 'False'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'serves': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Utility']"}),
            'utility_account_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility_meter_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weather_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.WeatherStation']"})
        },
        'BuildingSpeakApp.meterconsumptionmodel': {
            'F_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'F_stat_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'MeterConsumptionModel'},
            'SSQres': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Tccp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Thcp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Yavg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'acceptance_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'adj_r_squared': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'autocorr_coeff': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta01_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta02_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta03_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta04_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta05_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta06_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta07_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta08_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta09_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta10_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cvrmse': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'df': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'first_month': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_month': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']", 'null': 'True'}),
            'model_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nbe': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prediction_alpha': ('django.db.models.fields.FloatField', [], {'default': '0.1', 'null': 'True', 'blank': 'True'}),
            'r_squared': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rmse': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.meterpeakdemandmodel': {
            'F_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'F_stat_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'MeterPeakDemandModel'},
            'SSQres': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Tccp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Thcp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Yavg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'acceptance_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'adj_r_squared': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'autocorr_coeff': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta00v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta01_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta01v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta02_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta02v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta03_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta03v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta04_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta04v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta05_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta05v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta06_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta06v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta07_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta07v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta08_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta08v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta09_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta09v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'beta10_95_conf_int': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10_se': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10_t_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beta10v': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cvrmse': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'df': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'first_month': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_month': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']", 'null': 'True'}),
            'model_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nbe': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prediction_alpha': ('django.db.models.fields.FloatField', [], {'default': '0.1', 'null': 'True', 'blank': 'True'}),
            'r_squared': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rmse': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.monther': {
            'Meta': {'object_name': 'Monther'},
            'consumption_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.MeterConsumptionModel']", 'null': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'peak_demand_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.MeterPeakDemandModel']", 'null': 'True'})
        },
        'BuildingSpeakApp.monthling': {
            'Meta': {'object_name': 'Monthling'},
            'act_billing_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'act_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'act_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'act_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'act_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'act_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'asave_billing_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'asave_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'asave_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'asave_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'asave_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'asave_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_billing_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_billing_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_consumption_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_cost_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_kBtu_consumption_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_kBtuh_peak_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_peak_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'cdd_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'cdd_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'esave_billing_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_billing_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_consumption_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_cost_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_kBtu_consumption_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_kBtuh_peak_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_peak_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_billing_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_billing_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_consumption_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_cost_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_kBtu_consumption_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_kBtuh_peak_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_peak_demand_delta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'hdd_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'hdd_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monther': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Monther']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        'BuildingSpeakApp.operatingschedule': {
            'Meta': {'object_name': 'OperatingSchedule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.UnitSchedule']", 'symmetrical': 'False'})
        },
        'BuildingSpeakApp.rateschedule': {
            'Meta': {'object_name': 'RateSchedule'},
            '_my_subclass': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rate_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'riders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.RateScheduleRider']", 'symmetrical': 'False'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Utility']"})
        },
        'BuildingSpeakApp.rateschedulerider': {
            'Meta': {'object_name': 'RateScheduleRider'},
            '_my_subclass': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rider_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Utility']"})
        },
        'BuildingSpeakApp.reader': {
            'Meta': {'object_name': 'Reader'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'column_header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'column_index': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expected_max': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'expected_min': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.reading': {
            'Meta': {'object_name': 'Reading'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Reader']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        'BuildingSpeakApp.rooftopunit': {
            'Meta': {'object_name': 'RooftopUnit', '_ormbases': ['BuildingSpeakApp.Equipment']},
            'SAF_max': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'SAF_min': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'SCOC': ('django.db.models.fields.DecimalField', [], {'default': "'72'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'SCUN': ('django.db.models.fields.DecimalField', [], {'default': "'80'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'SHOC': ('django.db.models.fields.DecimalField', [], {'default': "'68'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'SHUN': ('django.db.models.fields.DecimalField', [], {'default': "'60'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'SRFC': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'T_max': ('django.db.models.fields.DecimalField', [], {'default': "'150'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'T_min': ('django.db.models.fields.DecimalField', [], {'default': "'-50'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'd': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'decimal'", 'null': 'True', 'blank': 'True'}),
            'dP_fan_max': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dP_fan_min': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'e': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'decimal'", 'null': 'True', 'blank': 'True'}),
            'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['BuildingSpeakApp.Equipment']", 'unique': 'True', 'primary_key': 'True'}),
            'f': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'decimal'", 'null': 'True', 'blank': 'True'}),
            'm': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'decimal'", 'null': 'True', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nameplate_EER': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_MBH_in': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_MBH_out': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_RFC': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_V': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c1_PH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c1_QTY': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c1_RLA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c2_PH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c2_QTY': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c2_RLA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c3_PH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c3_QTY': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_c3_RLA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_e1_FLA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_e1_PH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_e1_QTY': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_e2_FLA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_e2_PH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_e2_QTY': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_f1_FLA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_f1_PH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_f1_QTY': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_f2_FLA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_f2_PH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_f2_QTY': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_ng_eta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_pf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_phase': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nameplate_tons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'speed_min': ('django.db.models.fields.DecimalField', [], {'default': "'0.200000000000000011102230246251565404236316680908203125'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'})
        },
        'BuildingSpeakApp.space': {
            'EIA_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ESPM_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'Space'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_occupancy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Meter']", 'through': "orm['BuildingSpeakApp.SpaceMeterApportionment']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'observed_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'observed_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'observed_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'observed_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observed_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'observed_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provided_file_GMT_offset': ('django.db.models.fields.DecimalField', [], {'default': "'-5'", 'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'provided_file_adjusts_for_DST': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provided_file_column_for_indexing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_skiprows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'provided_file_time_zone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '200', 'blank': 'True'}),
            'provided_file_track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Reader']", 'symmetrical': 'False'}),
            'schedules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']", 'symmetrical': 'False'}),
            'space_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'square_footage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.spacemeterapportionment': {
            'Meta': {'object_name': 'SpaceMeterApportionment'},
            'assigned_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Space']"})
        },
        'BuildingSpeakApp.unitschedule': {
            'Meta': {'object_name': 'UnitSchedule'},
            'cron_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'day_of_month_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'day_of_week_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'hour_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'minute_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'month_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'BuildingSpeakApp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'desk_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'BuildingSpeakApp.utility': {
            'Meta': {'object_name': 'Utility'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'BuildingSpeakApp.weatherdatapoint': {
            'Meta': {'object_name': 'WeatherDataPoint'},
            'cloudCover': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dewPoint': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'humidity': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ozone': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'precipAccumulation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'precipIntensity': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'precipIntensityMax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'precipIntensityMaxTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'precipProbability': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'precipType': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'pressure': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sunriseTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sunsetTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'temperatureMax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'temperatureMaxTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'temperatureMin': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'temperatureMinTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'visibility': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'weather_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.WeatherStation']"}),
            'windBearing': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'windSpeed': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'})
        },
        'BuildingSpeakApp.weatherstation': {
            'Meta': {'object_name': 'WeatherStation'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tz_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weather_data_import': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weather_data_upload_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['BuildingSpeakApp']