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
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('dismissed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('message_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Message'])

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

        # Adding M2M table for field events on 'Reader'
        db.create_table('BuildingSpeakApp_reader_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_reader_events', ['reader_id', 'event_id'])

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

        # Adding M2M table for field events on 'Reading'
        db.create_table('BuildingSpeakApp_reading_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reading', models.ForeignKey(orm['BuildingSpeakApp.reading'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_reading_events', ['reading_id', 'event_id'])

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
            ('last_invoice_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_paid_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('next_invoice_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('bill_addressee', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('bill_email_address', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('bill_street_address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('bill_city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('bill_state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('bill_zip_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('bill_to_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('bill_to_location', self.gf('django.db.models.fields.BooleanField')(default=True)),
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

        # Adding M2M table for field events on 'Account'
        db.create_table('BuildingSpeakApp_account_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_account_events', ['account_id', 'event_id'])

        # Adding M2M table for field schedules on 'Account'
        db.create_table('BuildingSpeakApp_account_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_account_schedules', ['account_id', 'operatingschedule_id'])

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

        # Adding M2M table for field meters on 'Building'
        db.create_table('BuildingSpeakApp_building_meters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_building_meters', ['building_id', 'meter_id'])

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

        # Adding M2M table for field events on 'Building'
        db.create_table('BuildingSpeakApp_building_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_building_events', ['building_id', 'event_id'])

        # Adding M2M table for field schedules on 'Building'
        db.create_table('BuildingSpeakApp_building_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_building_schedules', ['building_id', 'operatingschedule_id'])

        # Adding model 'Equipment'
        db.create_table('BuildingSpeakApp_equipment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.OperatingSchedule'])),
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

        # Adding M2M table for field floors on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_floors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_floors', ['equipment_id', 'floor_id'])

        # Adding M2M table for field readers on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_readers', ['equipment_id', 'reader_id'])

        # Adding M2M table for field events on 'Equipment'
        db.create_table('BuildingSpeakApp_equipment_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_equipment_events', ['equipment_id', 'event_id'])

        # Adding model 'Floor'
        db.create_table('BuildingSpeakApp_floor', (
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
        db.send_create_signal('BuildingSpeakApp', ['Floor'])

        # Adding M2M table for field messages on 'Floor'
        db.create_table('BuildingSpeakApp_floor_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_floor_messages', ['floor_id', 'message_id'])

        # Adding M2M table for field readers on 'Floor'
        db.create_table('BuildingSpeakApp_floor_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_floor_readers', ['floor_id', 'reader_id'])

        # Adding M2M table for field events on 'Floor'
        db.create_table('BuildingSpeakApp_floor_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_floor_events', ['floor_id', 'event_id'])

        # Adding M2M table for field schedules on 'Floor'
        db.create_table('BuildingSpeakApp_floor_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_floor_schedules', ['floor_id', 'operatingschedule_id'])

        # Adding M2M table for field meters on 'Floor'
        db.create_table('BuildingSpeakApp_floor_meters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_floor_meters', ['floor_id', 'meter_id'])

        # Adding model 'BillingCycler'
        db.create_table('BuildingSpeakApp_billingcycler', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['BillingCycler'])

        # Adding M2M table for field messages on 'BillingCycler'
        db.create_table('BuildingSpeakApp_billingcycler_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('billingcycler', models.ForeignKey(orm['BuildingSpeakApp.billingcycler'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_billingcycler_messages', ['billingcycler_id', 'message_id'])

        # Adding model 'BillingCycle'
        db.create_table('BuildingSpeakApp_billingcycle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('period_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('billingcycler', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.BillingCycler'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['BillingCycle'])

        # Adding M2M table for field messages on 'BillingCycle'
        db.create_table('BuildingSpeakApp_billingcycle_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('billingcycle', models.ForeignKey(orm['BuildingSpeakApp.billingcycle'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_billingcycle_messages', ['billingcycle_id', 'message_id'])

        # Adding model 'Monther'
        db.create_table('BuildingSpeakApp_monther', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Monther'])

        # Adding M2M table for field events on 'Monther'
        db.create_table('BuildingSpeakApp_monther_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monther', models.ForeignKey(orm['BuildingSpeakApp.monther'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_monther_events', ['monther_id', 'event_id'])

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
            ('billing_demand', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('peak_demand', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('consumption', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('kBtuh_peak_demand', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('kBtu_consumption', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('monther', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Monther'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Monthling'])

        # Adding M2M table for field events on 'Monthling'
        db.create_table('BuildingSpeakApp_monthling_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monthling', models.ForeignKey(orm['BuildingSpeakApp.monthling'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_monthling_events', ['monthling_id', 'event_id'])

        # Adding model 'Meter'
        db.create_table('BuildingSpeakApp_meter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('utility_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
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

        # Adding M2M table for field events on 'Meter'
        db.create_table('BuildingSpeakApp_meter_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meter_events', ['meter_id', 'event_id'])

        # Adding M2M table for field schedules on 'Meter'
        db.create_table('BuildingSpeakApp_meter_schedules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meter_schedules', ['meter_id', 'operatingschedule_id'])

        # Adding model 'RateSchedule'
        db.create_table('BuildingSpeakApp_rateschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('utility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Utility'])),
            ('rate_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['RateSchedule'])

        # Adding M2M table for field messages on 'RateSchedule'
        db.create_table('BuildingSpeakApp_rateschedule_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rateschedule', models.ForeignKey(orm['BuildingSpeakApp.rateschedule'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_rateschedule_messages', ['rateschedule_id', 'message_id'])

        # Adding M2M table for field events on 'RateSchedule'
        db.create_table('BuildingSpeakApp_rateschedule_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rateschedule', models.ForeignKey(orm['BuildingSpeakApp.rateschedule'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_rateschedule_events', ['rateschedule_id', 'event_id'])

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

        # Adding M2M table for field events on 'Utility'
        db.create_table('BuildingSpeakApp_utility_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('utility', models.ForeignKey(orm['BuildingSpeakApp.utility'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_utility_events', ['utility_id', 'event_id'])

        # Adding model 'WeatherStation'
        db.create_table('BuildingSpeakApp_weatherstation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=7)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=7)),
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
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('sunriseTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('sunsetTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('precipIntensity', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('precipIntensityMax', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('precipIntensityMaxTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('precipProbability', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('precipType', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('precipAccumulation', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('temperature', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('temperatureMin', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('temperatureMinTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('temperatureMax', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('temperatureMaxTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('dewPoint', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('windSpeed', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('windBearing', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('cloudCover', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('humidity', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('pressure', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('visibility', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('ozone', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('weather_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.WeatherStation'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['WeatherDataPoint'])

        # Adding model 'Event'
        db.create_table('BuildingSpeakApp_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Event'])

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

        # Deleting model 'Reader'
        db.delete_table('BuildingSpeakApp_reader')

        # Removing M2M table for field events on 'Reader'
        db.delete_table('BuildingSpeakApp_reader_events')

        # Removing M2M table for field messages on 'Reader'
        db.delete_table('BuildingSpeakApp_reader_messages')

        # Deleting model 'Reading'
        db.delete_table('BuildingSpeakApp_reading')

        # Removing M2M table for field events on 'Reading'
        db.delete_table('BuildingSpeakApp_reading_events')

        # Deleting model 'Account'
        db.delete_table('BuildingSpeakApp_account')

        # Removing M2M table for field messages on 'Account'
        db.delete_table('BuildingSpeakApp_account_messages')

        # Removing M2M table for field users on 'Account'
        db.delete_table('BuildingSpeakApp_account_users')

        # Removing M2M table for field readers on 'Account'
        db.delete_table('BuildingSpeakApp_account_readers')

        # Removing M2M table for field events on 'Account'
        db.delete_table('BuildingSpeakApp_account_events')

        # Removing M2M table for field schedules on 'Account'
        db.delete_table('BuildingSpeakApp_account_schedules')

        # Deleting model 'Building'
        db.delete_table('BuildingSpeakApp_building')

        # Removing M2M table for field meters on 'Building'
        db.delete_table('BuildingSpeakApp_building_meters')

        # Removing M2M table for field messages on 'Building'
        db.delete_table('BuildingSpeakApp_building_messages')

        # Removing M2M table for field readers on 'Building'
        db.delete_table('BuildingSpeakApp_building_readers')

        # Removing M2M table for field events on 'Building'
        db.delete_table('BuildingSpeakApp_building_events')

        # Removing M2M table for field schedules on 'Building'
        db.delete_table('BuildingSpeakApp_building_schedules')

        # Deleting model 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment')

        # Removing M2M table for field messages on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_messages')

        # Removing M2M table for field meters on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_meters')

        # Removing M2M table for field buildings on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_buildings')

        # Removing M2M table for field floors on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_floors')

        # Removing M2M table for field readers on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_readers')

        # Removing M2M table for field events on 'Equipment'
        db.delete_table('BuildingSpeakApp_equipment_events')

        # Deleting model 'Floor'
        db.delete_table('BuildingSpeakApp_floor')

        # Removing M2M table for field messages on 'Floor'
        db.delete_table('BuildingSpeakApp_floor_messages')

        # Removing M2M table for field readers on 'Floor'
        db.delete_table('BuildingSpeakApp_floor_readers')

        # Removing M2M table for field events on 'Floor'
        db.delete_table('BuildingSpeakApp_floor_events')

        # Removing M2M table for field schedules on 'Floor'
        db.delete_table('BuildingSpeakApp_floor_schedules')

        # Removing M2M table for field meters on 'Floor'
        db.delete_table('BuildingSpeakApp_floor_meters')

        # Deleting model 'BillingCycler'
        db.delete_table('BuildingSpeakApp_billingcycler')

        # Removing M2M table for field messages on 'BillingCycler'
        db.delete_table('BuildingSpeakApp_billingcycler_messages')

        # Deleting model 'BillingCycle'
        db.delete_table('BuildingSpeakApp_billingcycle')

        # Removing M2M table for field messages on 'BillingCycle'
        db.delete_table('BuildingSpeakApp_billingcycle_messages')

        # Deleting model 'Monther'
        db.delete_table('BuildingSpeakApp_monther')

        # Removing M2M table for field events on 'Monther'
        db.delete_table('BuildingSpeakApp_monther_events')

        # Removing M2M table for field messages on 'Monther'
        db.delete_table('BuildingSpeakApp_monther_messages')

        # Deleting model 'Monthling'
        db.delete_table('BuildingSpeakApp_monthling')

        # Removing M2M table for field events on 'Monthling'
        db.delete_table('BuildingSpeakApp_monthling_events')

        # Deleting model 'Meter'
        db.delete_table('BuildingSpeakApp_meter')

        # Removing M2M table for field messages on 'Meter'
        db.delete_table('BuildingSpeakApp_meter_messages')

        # Removing M2M table for field readers on 'Meter'
        db.delete_table('BuildingSpeakApp_meter_readers')

        # Removing M2M table for field events on 'Meter'
        db.delete_table('BuildingSpeakApp_meter_events')

        # Removing M2M table for field schedules on 'Meter'
        db.delete_table('BuildingSpeakApp_meter_schedules')

        # Deleting model 'RateSchedule'
        db.delete_table('BuildingSpeakApp_rateschedule')

        # Removing M2M table for field messages on 'RateSchedule'
        db.delete_table('BuildingSpeakApp_rateschedule_messages')

        # Removing M2M table for field events on 'RateSchedule'
        db.delete_table('BuildingSpeakApp_rateschedule_events')

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

        # Removing M2M table for field events on 'Utility'
        db.delete_table('BuildingSpeakApp_utility_events')

        # Deleting model 'WeatherStation'
        db.delete_table('BuildingSpeakApp_weatherstation')

        # Removing M2M table for field messages on 'WeatherStation'
        db.delete_table('BuildingSpeakApp_weatherstation_messages')

        # Deleting model 'WeatherDataPoint'
        db.delete_table('BuildingSpeakApp_weatherdatapoint')

        # Deleting model 'Event'
        db.delete_table('BuildingSpeakApp_event')

        # Deleting model 'ManagementAction'
        db.delete_table('BuildingSpeakApp_managementaction')

        # Removing M2M table for field messages on 'ManagementAction'
        db.delete_table('BuildingSpeakApp_managementaction_messages')


    models = {
        'BuildingSpeakApp.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bill_addressee': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bill_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bill_email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'bill_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'bill_street_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bill_to_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bill_to_location': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bill_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_invoice_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'last_paid_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'launch_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'monthly_payment': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'next_invoice_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'BuildingSpeakApp.billingcycle': {
            'Meta': {'object_name': 'BillingCycle'},
            'billingcycler': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.BillingCycler']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'period_date': ('django.db.models.fields.DateTimeField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'BuildingSpeakApp.billingcycler': {
            'Meta': {'object_name': 'BillingCycler'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"})
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
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'max_occupancy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Meter']", 'symmetrical': 'False'}),
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
        'BuildingSpeakApp.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'buildings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Building']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'equipment_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'floors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Floor']", 'symmetrical': 'False'}),
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
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']"})
        },
        'BuildingSpeakApp.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.floor': {
            'EIA_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ESPM_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'Floor'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Building']"}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_occupancy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Meter']", 'symmetrical': 'False'}),
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
            'comment': ('django.db.models.fields.TextField', [], {}),
            'dismissed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'BuildingSpeakApp.meter': {
            'Meta': {'object_name': 'Meter'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Account']"}),
            'bill_data_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
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
            'units': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Utility']"}),
            'utility_account_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility_meter_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weather_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.WeatherStation']"})
        },
        'BuildingSpeakApp.monther': {
            'Meta': {'object_name': 'Monther'},
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'BuildingSpeakApp.monthling': {
            'Meta': {'object_name': 'Monthling'},
            'billing_demand': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'consumption': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'monther': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Monther']"}),
            'peak_demand': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
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
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rate_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Utility']"})
        },
        'BuildingSpeakApp.reader': {
            'Meta': {'object_name': 'Reader'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'column_header': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'column_index': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
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
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
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
        'BuildingSpeakApp.utility': {
            'Meta': {'object_name': 'Utility'},
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'BuildingSpeakApp.weatherdatapoint': {
            'Meta': {'object_name': 'WeatherDataPoint'},
            'cloudCover': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'dewPoint': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'humidity': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ozone': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'precipAccumulation': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'precipIntensity': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'precipIntensityMax': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'precipIntensityMaxTime': ('django.db.models.fields.DateTimeField', [], {}),
            'precipProbability': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'precipType': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pressure': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sunriseTime': ('django.db.models.fields.DateTimeField', [], {}),
            'sunsetTime': ('django.db.models.fields.DateTimeField', [], {}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'temperatureMax': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'temperatureMaxTime': ('django.db.models.fields.DateTimeField', [], {}),
            'temperatureMin': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'temperatureMinTime': ('django.db.models.fields.DateTimeField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'visibility': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'weather_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.WeatherStation']"}),
            'windBearing': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'}),
            'windSpeed': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '3'})
        },
        'BuildingSpeakApp.weatherstation': {
            'Meta': {'object_name': 'WeatherStation'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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