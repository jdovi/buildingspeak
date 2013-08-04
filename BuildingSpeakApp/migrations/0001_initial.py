# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'BuildingSpeakApp_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dismissed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('message_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Message'])

        # Adding model 'Reader'
        db.create_table(u'BuildingSpeakApp_reader', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_reader_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reader_id', 'event_id'])

        # Adding M2M table for field messages on 'Reader'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_reader_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reader_id', 'message_id'])

        # Adding model 'Reading'
        db.create_table(u'BuildingSpeakApp_reading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=3)),
            ('reader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Reader'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Reading'])

        # Adding M2M table for field events on 'Reading'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_reading_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reading', models.ForeignKey(orm['BuildingSpeakApp.reading'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reading_id', 'event_id'])

        # Adding model 'Account'
        db.create_table(u'BuildingSpeakApp_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_account_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'message_id'])

        # Adding M2M table for field users on 'Account'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_account_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'user_id'])

        # Adding M2M table for field readers on 'Account'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_account_readers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'reader_id'])

        # Adding M2M table for field events on 'Account'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_account_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'event_id'])

        # Adding M2M table for field schedules on 'Account'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_account_schedules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['BuildingSpeakApp.account'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'operatingschedule_id'])

        # Adding model 'BuildingMeterApportionment'
        db.create_table(u'BuildingSpeakApp_buildingmeterapportionment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Building'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['BuildingMeterApportionment'])

        # Adding model 'Building'
        db.create_table(u'BuildingSpeakApp_building', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_building_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['building_id', 'message_id'])

        # Adding M2M table for field readers on 'Building'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_building_readers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique(m2m_table_name, ['building_id', 'reader_id'])

        # Adding M2M table for field events on 'Building'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_building_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['building_id', 'event_id'])

        # Adding M2M table for field schedules on 'Building'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_building_schedules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['building_id', 'operatingschedule_id'])

        # Adding model 'BillingCycler'
        db.create_table(u'BuildingSpeakApp_billingcycler', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['BillingCycler'])

        # Adding M2M table for field messages on 'BillingCycler'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_billingcycler_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('billingcycler', models.ForeignKey(orm['BuildingSpeakApp.billingcycler'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['billingcycler_id', 'message_id'])

        # Adding model 'BillingCycle'
        db.create_table(u'BuildingSpeakApp_billingcycle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('period_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('billingcycler', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.BillingCycler'])),
        ))
        db.send_create_signal('BuildingSpeakApp', ['BillingCycle'])

        # Adding M2M table for field messages on 'BillingCycle'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_billingcycle_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('billingcycle', models.ForeignKey(orm['BuildingSpeakApp.billingcycle'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['billingcycle_id', 'message_id'])

        # Adding model 'Monther'
        db.create_table(u'BuildingSpeakApp_monther', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('consumption_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.MeterConsumptionModel'], null=True)),
            ('peak_demand_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.MeterPeakDemandModel'], null=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Monther'])

        # Adding M2M table for field events on 'Monther'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_monther_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monther', models.ForeignKey(orm['BuildingSpeakApp.monther'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['monther_id', 'event_id'])

        # Adding M2M table for field messages on 'Monther'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_monther_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monther', models.ForeignKey(orm['BuildingSpeakApp.monther'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['monther_id', 'message_id'])

        # Adding model 'Monthling'
        db.create_table(u'BuildingSpeakApp_monthling', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
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

        # Adding M2M table for field events on 'Monthling'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_monthling_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monthling', models.ForeignKey(orm['BuildingSpeakApp.monthling'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['monthling_id', 'event_id'])

        # Adding model 'Meter'
        db.create_table(u'BuildingSpeakApp_meter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_meter_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meter_id', 'message_id'])

        # Adding M2M table for field readers on 'Meter'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_meter_readers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meter_id', 'reader_id'])

        # Adding M2M table for field events on 'Meter'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_meter_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meter_id', 'event_id'])

        # Adding M2M table for field schedules on 'Meter'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_meter_schedules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meter_id', 'operatingschedule_id'])

        # Adding model 'Equipment'
        db.create_table(u'BuildingSpeakApp_equipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_equipment_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['equipment_id', 'message_id'])

        # Adding M2M table for field meters on 'Equipment'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_equipment_meters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False))
        ))
        db.create_unique(m2m_table_name, ['equipment_id', 'meter_id'])

        # Adding M2M table for field buildings on 'Equipment'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_equipment_buildings')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('building', models.ForeignKey(orm['BuildingSpeakApp.building'], null=False))
        ))
        db.create_unique(m2m_table_name, ['equipment_id', 'building_id'])

        # Adding M2M table for field spaces on 'Equipment'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_equipment_spaces')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False))
        ))
        db.create_unique(m2m_table_name, ['equipment_id', 'space_id'])

        # Adding M2M table for field readers on 'Equipment'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_equipment_readers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique(m2m_table_name, ['equipment_id', 'reader_id'])

        # Adding M2M table for field events on 'Equipment'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_equipment_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['BuildingSpeakApp.equipment'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['equipment_id', 'event_id'])

        # Adding model 'WeatherStation'
        db.create_table(u'BuildingSpeakApp_weatherstation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_weatherstation_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('weatherstation', models.ForeignKey(orm['BuildingSpeakApp.weatherstation'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['weatherstation_id', 'message_id'])

        # Adding model 'WeatherDataPoint'
        db.create_table(u'BuildingSpeakApp_weatherdatapoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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

        # Adding model 'EMMeterApportionment'
        db.create_table(u'BuildingSpeakApp_emmeterapportionment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('efficiency_measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.EfficiencyMeasure'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['EMMeterApportionment'])

        # Adding model 'EMEquipmentApportionment'
        db.create_table(u'BuildingSpeakApp_emequipmentapportionment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('equipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Equipment'])),
            ('efficiency_measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.EfficiencyMeasure'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['EMEquipmentApportionment'])

        # Adding model 'EfficiencyMeasure'
        db.create_table(u'BuildingSpeakApp_efficiencymeasure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('annual_consumption_savings', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('peak_demand_savings', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('annual_cost_savings', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_efficiencymeasure_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('efficiencymeasure', models.ForeignKey(orm['BuildingSpeakApp.efficiencymeasure'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['efficiencymeasure_id', 'message_id'])

        # Adding model 'Floor'
        db.create_table(u'BuildingSpeakApp_floor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_floor_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['floor_id', 'message_id'])

        # Adding M2M table for field readers on 'Floor'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_floor_readers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique(m2m_table_name, ['floor_id', 'reader_id'])

        # Adding M2M table for field events on 'Floor'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_floor_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['floor_id', 'event_id'])

        # Adding M2M table for field schedules on 'Floor'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_floor_schedules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['floor_id', 'operatingschedule_id'])

        # Adding M2M table for field meters on 'Floor'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_floor_meters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('floor', models.ForeignKey(orm['BuildingSpeakApp.floor'], null=False)),
            ('meter', models.ForeignKey(orm['BuildingSpeakApp.meter'], null=False))
        ))
        db.create_unique(m2m_table_name, ['floor_id', 'meter_id'])

        # Adding model 'SpaceMeterApportionment'
        db.create_table(u'BuildingSpeakApp_spacemeterapportionment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'])),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Space'])),
            ('assigned_fraction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['SpaceMeterApportionment'])

        # Adding model 'Space'
        db.create_table(u'BuildingSpeakApp_space', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_space_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['space_id', 'message_id'])

        # Adding M2M table for field readers on 'Space'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_space_readers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False)),
            ('reader', models.ForeignKey(orm['BuildingSpeakApp.reader'], null=False))
        ))
        db.create_unique(m2m_table_name, ['space_id', 'reader_id'])

        # Adding M2M table for field events on 'Space'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_space_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['space_id', 'event_id'])

        # Adding M2M table for field schedules on 'Space'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_space_schedules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('space', models.ForeignKey(orm['BuildingSpeakApp.space'], null=False)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['space_id', 'operatingschedule_id'])

        # Adding model 'MeterConsumptionModel'
        db.create_table(u'BuildingSpeakApp_meterconsumptionmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_meterconsumptionmodel_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meterconsumptionmodel', models.ForeignKey(orm['BuildingSpeakApp.meterconsumptionmodel'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meterconsumptionmodel_id', 'message_id'])

        # Adding model 'MeterPeakDemandModel'
        db.create_table(u'BuildingSpeakApp_meterpeakdemandmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['MeterPeakDemandModel'])

        # Adding model 'RateSchedule'
        db.create_table(u'BuildingSpeakApp_rateschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_my_subclass', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('utility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Utility'])),
            ('rate_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['RateSchedule'])

        # Adding M2M table for field messages on 'RateSchedule'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_rateschedule_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rateschedule', models.ForeignKey(orm['BuildingSpeakApp.rateschedule'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['rateschedule_id', 'message_id'])

        # Adding model 'RateScheduleRider'
        db.create_table(u'BuildingSpeakApp_rateschedulerider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_my_subclass', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('rate_schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.RateSchedule'])),
            ('rider_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['RateScheduleRider'])

        # Adding M2M table for field messages on 'RateScheduleRider'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_rateschedulerider_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rateschedulerider', models.ForeignKey(orm['BuildingSpeakApp.rateschedulerider'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['rateschedulerider_id', 'message_id'])

        # Adding model 'GAPowerPLS'
        db.create_table(u'BuildingSpeakApp_gapowerpls', (
            (u'rateschedule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['BuildingSpeakApp.RateSchedule'], unique=True, primary_key=True)),
            ('basic_service_charge', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
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
            ('limitation_of_service_kW', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('limitation_of_service_winter_percent', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
            ('limitation_of_service_summer_percent', self.gf('django.db.models.fields.DecimalField')(default='0', null=True, max_digits=20, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['GAPowerPLS'])

        # Adding model 'RooftopUnit'
        db.create_table(u'BuildingSpeakApp_rooftopunit', (
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['BuildingSpeakApp.Equipment'], unique=True, primary_key=True)),
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
        db.create_table(u'BuildingSpeakApp_unitschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_unitschedule_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unitschedule', models.ForeignKey(orm['BuildingSpeakApp.unitschedule'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['unitschedule_id', 'message_id'])

        # Adding model 'OperatingSchedule'
        db.create_table(u'BuildingSpeakApp_operatingschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['OperatingSchedule'])

        # Adding M2M table for field messages on 'OperatingSchedule'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_operatingschedule_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['operatingschedule_id', 'message_id'])

        # Adding M2M table for field units on 'OperatingSchedule'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_operatingschedule_units')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('operatingschedule', models.ForeignKey(orm['BuildingSpeakApp.operatingschedule'], null=False)),
            ('unitschedule', models.ForeignKey(orm['BuildingSpeakApp.unitschedule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['operatingschedule_id', 'unitschedule_id'])

        # Adding model 'Utility'
        db.create_table(u'BuildingSpeakApp_utility', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Utility'])

        # Adding M2M table for field messages on 'Utility'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_utility_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('utility', models.ForeignKey(orm['BuildingSpeakApp.utility'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['utility_id', 'message_id'])

        # Adding M2M table for field events on 'Utility'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_utility_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('utility', models.ForeignKey(orm['BuildingSpeakApp.utility'], null=False)),
            ('event', models.ForeignKey(orm['BuildingSpeakApp.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['utility_id', 'event_id'])

        # Adding model 'Event'
        db.create_table(u'BuildingSpeakApp_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['Event'])

        # Adding model 'ManagementAction'
        db.create_table(u'BuildingSpeakApp_managementaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Click this link to perform management actions', max_length=200)),
            ('create_a_new_import_file', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('import_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('load_model_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('model_data_file_for_upload', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('processed_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('BuildingSpeakApp', ['ManagementAction'])

        # Adding M2M table for field messages on 'ManagementAction'
        m2m_table_name = db.shorten_name(u'BuildingSpeakApp_managementaction_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('managementaction', models.ForeignKey(orm['BuildingSpeakApp.managementaction'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['managementaction_id', 'message_id'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'BuildingSpeakApp_message')

        # Deleting model 'Reader'
        db.delete_table(u'BuildingSpeakApp_reader')

        # Removing M2M table for field events on 'Reader'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_reader_events'))

        # Removing M2M table for field messages on 'Reader'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_reader_messages'))

        # Deleting model 'Reading'
        db.delete_table(u'BuildingSpeakApp_reading')

        # Removing M2M table for field events on 'Reading'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_reading_events'))

        # Deleting model 'Account'
        db.delete_table(u'BuildingSpeakApp_account')

        # Removing M2M table for field messages on 'Account'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_account_messages'))

        # Removing M2M table for field users on 'Account'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_account_users'))

        # Removing M2M table for field readers on 'Account'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_account_readers'))

        # Removing M2M table for field events on 'Account'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_account_events'))

        # Removing M2M table for field schedules on 'Account'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_account_schedules'))

        # Deleting model 'BuildingMeterApportionment'
        db.delete_table(u'BuildingSpeakApp_buildingmeterapportionment')

        # Deleting model 'Building'
        db.delete_table(u'BuildingSpeakApp_building')

        # Removing M2M table for field messages on 'Building'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_building_messages'))

        # Removing M2M table for field readers on 'Building'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_building_readers'))

        # Removing M2M table for field events on 'Building'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_building_events'))

        # Removing M2M table for field schedules on 'Building'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_building_schedules'))

        # Deleting model 'BillingCycler'
        db.delete_table(u'BuildingSpeakApp_billingcycler')

        # Removing M2M table for field messages on 'BillingCycler'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_billingcycler_messages'))

        # Deleting model 'BillingCycle'
        db.delete_table(u'BuildingSpeakApp_billingcycle')

        # Removing M2M table for field messages on 'BillingCycle'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_billingcycle_messages'))

        # Deleting model 'Monther'
        db.delete_table(u'BuildingSpeakApp_monther')

        # Removing M2M table for field events on 'Monther'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_monther_events'))

        # Removing M2M table for field messages on 'Monther'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_monther_messages'))

        # Deleting model 'Monthling'
        db.delete_table(u'BuildingSpeakApp_monthling')

        # Removing M2M table for field events on 'Monthling'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_monthling_events'))

        # Deleting model 'Meter'
        db.delete_table(u'BuildingSpeakApp_meter')

        # Removing M2M table for field messages on 'Meter'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_meter_messages'))

        # Removing M2M table for field readers on 'Meter'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_meter_readers'))

        # Removing M2M table for field events on 'Meter'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_meter_events'))

        # Removing M2M table for field schedules on 'Meter'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_meter_schedules'))

        # Deleting model 'Equipment'
        db.delete_table(u'BuildingSpeakApp_equipment')

        # Removing M2M table for field messages on 'Equipment'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_equipment_messages'))

        # Removing M2M table for field meters on 'Equipment'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_equipment_meters'))

        # Removing M2M table for field buildings on 'Equipment'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_equipment_buildings'))

        # Removing M2M table for field spaces on 'Equipment'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_equipment_spaces'))

        # Removing M2M table for field readers on 'Equipment'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_equipment_readers'))

        # Removing M2M table for field events on 'Equipment'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_equipment_events'))

        # Deleting model 'WeatherStation'
        db.delete_table(u'BuildingSpeakApp_weatherstation')

        # Removing M2M table for field messages on 'WeatherStation'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_weatherstation_messages'))

        # Deleting model 'WeatherDataPoint'
        db.delete_table(u'BuildingSpeakApp_weatherdatapoint')

        # Deleting model 'EMMeterApportionment'
        db.delete_table(u'BuildingSpeakApp_emmeterapportionment')

        # Deleting model 'EMEquipmentApportionment'
        db.delete_table(u'BuildingSpeakApp_emequipmentapportionment')

        # Deleting model 'EfficiencyMeasure'
        db.delete_table(u'BuildingSpeakApp_efficiencymeasure')

        # Removing M2M table for field messages on 'EfficiencyMeasure'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_efficiencymeasure_messages'))

        # Deleting model 'Floor'
        db.delete_table(u'BuildingSpeakApp_floor')

        # Removing M2M table for field messages on 'Floor'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_floor_messages'))

        # Removing M2M table for field readers on 'Floor'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_floor_readers'))

        # Removing M2M table for field events on 'Floor'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_floor_events'))

        # Removing M2M table for field schedules on 'Floor'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_floor_schedules'))

        # Removing M2M table for field meters on 'Floor'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_floor_meters'))

        # Deleting model 'SpaceMeterApportionment'
        db.delete_table(u'BuildingSpeakApp_spacemeterapportionment')

        # Deleting model 'Space'
        db.delete_table(u'BuildingSpeakApp_space')

        # Removing M2M table for field messages on 'Space'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_space_messages'))

        # Removing M2M table for field readers on 'Space'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_space_readers'))

        # Removing M2M table for field events on 'Space'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_space_events'))

        # Removing M2M table for field schedules on 'Space'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_space_schedules'))

        # Deleting model 'MeterConsumptionModel'
        db.delete_table(u'BuildingSpeakApp_meterconsumptionmodel')

        # Removing M2M table for field messages on 'MeterConsumptionModel'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_meterconsumptionmodel_messages'))

        # Deleting model 'MeterPeakDemandModel'
        db.delete_table(u'BuildingSpeakApp_meterpeakdemandmodel')

        # Deleting model 'RateSchedule'
        db.delete_table(u'BuildingSpeakApp_rateschedule')

        # Removing M2M table for field messages on 'RateSchedule'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_rateschedule_messages'))

        # Deleting model 'RateScheduleRider'
        db.delete_table(u'BuildingSpeakApp_rateschedulerider')

        # Removing M2M table for field messages on 'RateScheduleRider'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_rateschedulerider_messages'))

        # Deleting model 'GAPowerPLS'
        db.delete_table(u'BuildingSpeakApp_gapowerpls')

        # Deleting model 'RooftopUnit'
        db.delete_table(u'BuildingSpeakApp_rooftopunit')

        # Deleting model 'UnitSchedule'
        db.delete_table(u'BuildingSpeakApp_unitschedule')

        # Removing M2M table for field messages on 'UnitSchedule'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_unitschedule_messages'))

        # Deleting model 'OperatingSchedule'
        db.delete_table(u'BuildingSpeakApp_operatingschedule')

        # Removing M2M table for field messages on 'OperatingSchedule'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_operatingschedule_messages'))

        # Removing M2M table for field units on 'OperatingSchedule'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_operatingschedule_units'))

        # Deleting model 'Utility'
        db.delete_table(u'BuildingSpeakApp_utility')

        # Removing M2M table for field messages on 'Utility'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_utility_messages'))

        # Removing M2M table for field events on 'Utility'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_utility_events'))

        # Deleting model 'Event'
        db.delete_table(u'BuildingSpeakApp_event')

        # Deleting model 'ManagementAction'
        db.delete_table(u'BuildingSpeakApp_managementaction')

        # Removing M2M table for field messages on 'ManagementAction'
        db.delete_table(db.shorten_name(u'BuildingSpeakApp_managementaction_messages'))


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'BuildingSpeakApp.billingcycle': {
            'Meta': {'object_name': 'BillingCycle'},
            'billingcycler': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.BillingCycler']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'period_date': ('django.db.models.fields.DateTimeField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'BuildingSpeakApp.billingcycler': {
            'Meta': {'object_name': 'BillingCycler'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'BuildingSpeakApp.emmeterapportionment': {
            'Meta': {'object_name': 'EMMeterApportionment'},
            'assigned_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'efficiency_measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.EfficiencyMeasure']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"})
        },
        'BuildingSpeakApp.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'buildings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Building']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'equipment_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']"}),
            'spaces': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Space']", 'symmetrical': 'False'})
        },
        'BuildingSpeakApp.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.floor': {
            'EIA_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ESPM_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'Floor'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Building']"}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'BuildingSpeakApp.gapowerpls': {
            'Meta': {'object_name': 'GAPowerPLS', '_ormbases': ['BuildingSpeakApp.RateSchedule']},
            'absolute_minimum_demand': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'basic_service_charge': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'billing_demand_sliding_month_window': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'contract_minimum_demand': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'excess_kW_rate': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'excess_kW_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'lim_service_sliding_month_window': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'limitation_of_service_kW': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
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
            u'rateschedule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['BuildingSpeakApp.RateSchedule']", 'unique': 'True', 'primary_key': 'True'}),
            'summer_end_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'summer_start_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'summer_summer_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'summer_winter_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
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
            'window_minutes': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_end_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_start_month': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_summer_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'winter_winter_threshold': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'})
        },
        'BuildingSpeakApp.managementaction': {
            'Meta': {'object_name': 'ManagementAction'},
            'create_a_new_import_file': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'Meta': {'object_name': 'MeterPeakDemandModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'BuildingSpeakApp.monther': {
            'Meta': {'object_name': 'Monther'},
            'consumption_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.MeterConsumptionModel']", 'null': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monther': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Monther']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        'BuildingSpeakApp.operatingschedule': {
            'Meta': {'object_name': 'OperatingSchedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.UnitSchedule']", 'symmetrical': 'False'})
        },
        'BuildingSpeakApp.rateschedule': {
            'Meta': {'object_name': 'RateSchedule'},
            '_my_subclass': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rate_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Utility']"})
        },
        'BuildingSpeakApp.rateschedulerider': {
            'Meta': {'object_name': 'RateScheduleRider'},
            '_my_subclass': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rate_schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.RateSchedule']"}),
            'rider_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.reading': {
            'Meta': {'object_name': 'Reading'},
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['BuildingSpeakApp.Equipment']", 'unique': 'True', 'primary_key': 'True'}),
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
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Space']"})
        },
        'BuildingSpeakApp.unitschedule': {
            'Meta': {'object_name': 'UnitSchedule'},
            'cron_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'day_of_month_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'day_of_week_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'hour_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'minute_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'month_list': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'BuildingSpeakApp.utility': {
            'Meta': {'object_name': 'Utility'},
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Message']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tz_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weather_data_import': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weather_data_upload_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['BuildingSpeakApp']