# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EnergyMeasure.percent_cool'
        db.add_column('BuildingSpeakApp_energymeasure', 'percent_cool',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.percent_heat'
        db.add_column('BuildingSpeakApp_energymeasure', 'percent_heat',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.percent_flat'
        db.add_column('BuildingSpeakApp_energymeasure', 'percent_flat',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jan_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'jan_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.feb_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'feb_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.mar_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'mar_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.apr_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'apr_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.may_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'may_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jun_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'jun_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jul_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'jul_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.aug_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'aug_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.sep_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'sep_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.oct_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'oct_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.nov_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'nov_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.dec_cons'
        db.add_column('BuildingSpeakApp_energymeasure', 'dec_cons',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jan_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'jan_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.feb_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'feb_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.mar_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'mar_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.apr_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'apr_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.may_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'may_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jun_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'jun_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jul_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'jul_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.aug_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'aug_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.sep_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'sep_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.oct_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'oct_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.nov_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'nov_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.dec_peak'
        db.add_column('BuildingSpeakApp_energymeasure', 'dec_peak',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jan_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'jan_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.feb_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'feb_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.mar_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'mar_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.apr_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'apr_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.may_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'may_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jun_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'jun_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.jul_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'jul_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.aug_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'aug_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.sep_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'sep_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.oct_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'oct_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.nov_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'nov_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.dec_cost'
        db.add_column('BuildingSpeakApp_energymeasure', 'dec_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'EnergyMeasure.weather_station'
        db.add_column('BuildingSpeakApp_energymeasure', 'weather_station',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['BuildingSpeakApp.WeatherStation']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EnergyMeasure.percent_cool'
        db.delete_column('BuildingSpeakApp_energymeasure', 'percent_cool')

        # Deleting field 'EnergyMeasure.percent_heat'
        db.delete_column('BuildingSpeakApp_energymeasure', 'percent_heat')

        # Deleting field 'EnergyMeasure.percent_flat'
        db.delete_column('BuildingSpeakApp_energymeasure', 'percent_flat')

        # Deleting field 'EnergyMeasure.jan_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jan_cons')

        # Deleting field 'EnergyMeasure.feb_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'feb_cons')

        # Deleting field 'EnergyMeasure.mar_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'mar_cons')

        # Deleting field 'EnergyMeasure.apr_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'apr_cons')

        # Deleting field 'EnergyMeasure.may_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'may_cons')

        # Deleting field 'EnergyMeasure.jun_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jun_cons')

        # Deleting field 'EnergyMeasure.jul_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jul_cons')

        # Deleting field 'EnergyMeasure.aug_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'aug_cons')

        # Deleting field 'EnergyMeasure.sep_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'sep_cons')

        # Deleting field 'EnergyMeasure.oct_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'oct_cons')

        # Deleting field 'EnergyMeasure.nov_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'nov_cons')

        # Deleting field 'EnergyMeasure.dec_cons'
        db.delete_column('BuildingSpeakApp_energymeasure', 'dec_cons')

        # Deleting field 'EnergyMeasure.jan_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jan_peak')

        # Deleting field 'EnergyMeasure.feb_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'feb_peak')

        # Deleting field 'EnergyMeasure.mar_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'mar_peak')

        # Deleting field 'EnergyMeasure.apr_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'apr_peak')

        # Deleting field 'EnergyMeasure.may_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'may_peak')

        # Deleting field 'EnergyMeasure.jun_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jun_peak')

        # Deleting field 'EnergyMeasure.jul_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jul_peak')

        # Deleting field 'EnergyMeasure.aug_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'aug_peak')

        # Deleting field 'EnergyMeasure.sep_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'sep_peak')

        # Deleting field 'EnergyMeasure.oct_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'oct_peak')

        # Deleting field 'EnergyMeasure.nov_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'nov_peak')

        # Deleting field 'EnergyMeasure.dec_peak'
        db.delete_column('BuildingSpeakApp_energymeasure', 'dec_peak')

        # Deleting field 'EnergyMeasure.jan_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jan_cost')

        # Deleting field 'EnergyMeasure.feb_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'feb_cost')

        # Deleting field 'EnergyMeasure.mar_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'mar_cost')

        # Deleting field 'EnergyMeasure.apr_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'apr_cost')

        # Deleting field 'EnergyMeasure.may_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'may_cost')

        # Deleting field 'EnergyMeasure.jun_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jun_cost')

        # Deleting field 'EnergyMeasure.jul_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'jul_cost')

        # Deleting field 'EnergyMeasure.aug_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'aug_cost')

        # Deleting field 'EnergyMeasure.sep_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'sep_cost')

        # Deleting field 'EnergyMeasure.oct_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'oct_cost')

        # Deleting field 'EnergyMeasure.nov_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'nov_cost')

        # Deleting field 'EnergyMeasure.dec_cost'
        db.delete_column('BuildingSpeakApp_energymeasure', 'dec_cost')

        # Deleting field 'EnergyMeasure.weather_station'
        db.delete_column('BuildingSpeakApp_energymeasure', 'weather_station_id')


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
        'BuildingSpeakApp.baselinemodel': {
            'F_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'F_stat_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'BaselineModel'},
            'SSQres': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Tccp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Thcp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Yavg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']", 'null': 'True'}),
            'model_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nbe': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'r_squared': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rmse': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
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
        'BuildingSpeakApp.ecmequipmentapportionment': {
            'Meta': {'object_name': 'ECMEquipmentApportionment'},
            'assigned_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'energymeasure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.EnergyMeasure']"}),
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Equipment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'BuildingSpeakApp.ecmmeterapportionment': {
            'Meta': {'object_name': 'ECMMeterApportionment'},
            'assigned_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '3', 'blank': 'True'}),
            'energymeasure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.EnergyMeasure']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.Meter']"})
        },
        'BuildingSpeakApp.energymeasure': {
            'Meta': {'object_name': 'EnergyMeasure'},
            'annual_consumption_savings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'annual_cost_savings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'apr_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'apr_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'apr_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'aug_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'aug_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'aug_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dec_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dec_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'dec_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'equipments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Equipment']", 'through': "orm['BuildingSpeakApp.ECMEquipmentApportionment']", 'symmetrical': 'False'}),
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
            'meters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['BuildingSpeakApp.Meter']", 'through': "orm['BuildingSpeakApp.ECMMeterApportionment']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nov_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nov_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'nov_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'oct_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'oct_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'oct_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'peak_demand_savings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_cool': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_flat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'percent_heat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'sep_cons': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'sep_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'sep_peak': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'utility_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weather_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.WeatherStation']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
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
            'current_baseline_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['BuildingSpeakApp.BaselineModel']", 'null': 'True'}),
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
            'cdd': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
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