# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Monthling.kBtu_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'kBtu_consumption')

        # Deleting field 'Monthling.billing_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'billing_demand')

        # Deleting field 'Monthling.cost'
        db.delete_column('BuildingSpeakApp_monthling', 'cost')

        # Deleting field 'Monthling.peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'peak_demand')

        # Deleting field 'Monthling.kBtuh_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'kBtuh_peak_demand')

        # Deleting field 'Monthling.consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'consumption')

        # Adding field 'Monthling.base_billing_demand'
        db.add_column('BuildingSpeakApp_monthling', 'base_billing_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.base_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'base_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.base_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'base_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.base_kBtuh_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'base_kBtuh_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.base_kBtu_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'base_kBtu_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.base_cost'
        db.add_column('BuildingSpeakApp_monthling', 'base_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.exp_billing_demand'
        db.add_column('BuildingSpeakApp_monthling', 'exp_billing_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.exp_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'exp_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.exp_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'exp_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.exp_kBtuh_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'exp_kBtuh_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.exp_kBtu_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'exp_kBtu_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.exp_cost'
        db.add_column('BuildingSpeakApp_monthling', 'exp_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.act_billing_demand'
        db.add_column('BuildingSpeakApp_monthling', 'act_billing_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.act_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'act_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.act_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'act_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.act_kBtuh_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'act_kBtuh_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.act_kBtu_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'act_kBtu_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.act_cost'
        db.add_column('BuildingSpeakApp_monthling', 'act_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.esave_billing_demand'
        db.add_column('BuildingSpeakApp_monthling', 'esave_billing_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.esave_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'esave_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.esave_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'esave_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.esave_kBtuh_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'esave_kBtuh_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.esave_kBtu_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'esave_kBtu_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.esave_cost'
        db.add_column('BuildingSpeakApp_monthling', 'esave_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.asave_billing_demand'
        db.add_column('BuildingSpeakApp_monthling', 'asave_billing_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.asave_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'asave_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.asave_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'asave_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.asave_kBtuh_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'asave_kBtuh_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.asave_kBtu_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'asave_kBtu_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.asave_cost'
        db.add_column('BuildingSpeakApp_monthling', 'asave_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Monthling.kBtu_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'kBtu_consumption',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=3),
                      keep_default=False)

        # Adding field 'Monthling.billing_demand'
        db.add_column('BuildingSpeakApp_monthling', 'billing_demand',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=3),
                      keep_default=False)

        # Adding field 'Monthling.cost'
        db.add_column('BuildingSpeakApp_monthling', 'cost',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=3),
                      keep_default=False)

        # Adding field 'Monthling.peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=3),
                      keep_default=False)

        # Adding field 'Monthling.kBtuh_peak_demand'
        db.add_column('BuildingSpeakApp_monthling', 'kBtuh_peak_demand',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=3),
                      keep_default=False)

        # Adding field 'Monthling.consumption'
        db.add_column('BuildingSpeakApp_monthling', 'consumption',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=3),
                      keep_default=False)

        # Deleting field 'Monthling.base_billing_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'base_billing_demand')

        # Deleting field 'Monthling.base_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'base_peak_demand')

        # Deleting field 'Monthling.base_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'base_consumption')

        # Deleting field 'Monthling.base_kBtuh_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'base_kBtuh_peak_demand')

        # Deleting field 'Monthling.base_kBtu_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'base_kBtu_consumption')

        # Deleting field 'Monthling.base_cost'
        db.delete_column('BuildingSpeakApp_monthling', 'base_cost')

        # Deleting field 'Monthling.exp_billing_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'exp_billing_demand')

        # Deleting field 'Monthling.exp_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'exp_peak_demand')

        # Deleting field 'Monthling.exp_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'exp_consumption')

        # Deleting field 'Monthling.exp_kBtuh_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'exp_kBtuh_peak_demand')

        # Deleting field 'Monthling.exp_kBtu_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'exp_kBtu_consumption')

        # Deleting field 'Monthling.exp_cost'
        db.delete_column('BuildingSpeakApp_monthling', 'exp_cost')

        # Deleting field 'Monthling.act_billing_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'act_billing_demand')

        # Deleting field 'Monthling.act_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'act_peak_demand')

        # Deleting field 'Monthling.act_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'act_consumption')

        # Deleting field 'Monthling.act_kBtuh_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'act_kBtuh_peak_demand')

        # Deleting field 'Monthling.act_kBtu_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'act_kBtu_consumption')

        # Deleting field 'Monthling.act_cost'
        db.delete_column('BuildingSpeakApp_monthling', 'act_cost')

        # Deleting field 'Monthling.esave_billing_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'esave_billing_demand')

        # Deleting field 'Monthling.esave_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'esave_peak_demand')

        # Deleting field 'Monthling.esave_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'esave_consumption')

        # Deleting field 'Monthling.esave_kBtuh_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'esave_kBtuh_peak_demand')

        # Deleting field 'Monthling.esave_kBtu_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'esave_kBtu_consumption')

        # Deleting field 'Monthling.esave_cost'
        db.delete_column('BuildingSpeakApp_monthling', 'esave_cost')

        # Deleting field 'Monthling.asave_billing_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'asave_billing_demand')

        # Deleting field 'Monthling.asave_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'asave_peak_demand')

        # Deleting field 'Monthling.asave_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'asave_consumption')

        # Deleting field 'Monthling.asave_kBtuh_peak_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'asave_kBtuh_peak_demand')

        # Deleting field 'Monthling.asave_kBtu_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'asave_kBtu_consumption')

        # Deleting field 'Monthling.asave_cost'
        db.delete_column('BuildingSpeakApp_monthling', 'asave_cost')


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
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.OperatingSchedule']"}),
            'spaces': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Space']", 'symmetrical': 'False'})
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
            'serves': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'base_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'base_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'cdd': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_billing_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'esave_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Event']", 'symmetrical': 'False'}),
            'exp_billing_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_kBtu_consumption': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_kBtuh_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'exp_peak_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'hdd': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monther': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Monther']"}),
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
        'BuildingSpeakApp.space': {
            'EIA_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ESPM_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'Space'},
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