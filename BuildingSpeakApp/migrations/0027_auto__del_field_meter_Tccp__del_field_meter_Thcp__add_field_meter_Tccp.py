# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Meter.Tccp'
        db.delete_column('BuildingSpeakApp_meter', 'Tccp')

        # Deleting field 'Meter.Thcp'
        db.delete_column('BuildingSpeakApp_meter', 'Thcp')

        # Adding field 'Meter.Tccp_demand'
        db.add_column('BuildingSpeakApp_meter', 'Tccp_demand',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Meter.Thcp_demand'
        db.add_column('BuildingSpeakApp_meter', 'Thcp_demand',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Meter.Tccp_consumption'
        db.add_column('BuildingSpeakApp_meter', 'Tccp_consumption',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Meter.Thcp_consumption'
        db.add_column('BuildingSpeakApp_meter', 'Thcp_consumption',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'MeterPeakDemandModel.beta00_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.meter'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'meter_id')

        # Deleting field 'MeterPeakDemandModel.beta06v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06v')

        # Deleting field 'MeterPeakDemandModel.beta06p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06p')

        # Deleting field 'MeterPeakDemandModel.beta09_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_p_value')

        # Deleting field 'MeterPeakDemandModel.beta04_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_se')

        # Deleting field 'MeterPeakDemandModel.beta07_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_se')

        # Deleting field 'MeterPeakDemandModel.beta09p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09p')

        # Deleting field 'MeterPeakDemandModel.beta00_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_p_value')

        # Deleting field 'MeterPeakDemandModel.beta09v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09v')

        # Deleting field 'MeterPeakDemandModel.beta01p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01p')

        # Deleting field 'MeterPeakDemandModel.beta01v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01v')

        # Deleting field 'MeterPeakDemandModel.df'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'df')

        # Deleting field 'MeterPeakDemandModel.beta10_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta01_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_p_value')

        # Deleting field 'MeterPeakDemandModel.beta01_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_t_stat')

        # Deleting field 'MeterPeakDemandModel.rmse'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'rmse')

        # Deleting field 'MeterPeakDemandModel.beta04_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_p_value')

        # Deleting field 'MeterPeakDemandModel.p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'p')

        # Deleting field 'MeterPeakDemandModel.beta08v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08v')

        # Deleting field 'MeterPeakDemandModel.beta08p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08p')

        # Deleting field 'MeterPeakDemandModel.beta05_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta04p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04p')

        # Deleting field 'MeterPeakDemandModel.beta02_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_se')

        # Deleting field 'MeterPeakDemandModel.beta04v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04v')

        # Deleting field 'MeterPeakDemandModel.nbe'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'nbe')

        # Deleting field 'MeterPeakDemandModel.beta05_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_se')

        # Deleting field 'MeterPeakDemandModel.beta10_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_se')

        # Deleting field 'MeterPeakDemandModel.beta10_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_p_value')

        # Deleting field 'MeterPeakDemandModel.beta01_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_se')

        # Deleting field 'MeterPeakDemandModel.beta05_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta07v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07v')

        # Deleting field 'MeterPeakDemandModel.beta07p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07p')

        # Deleting field 'MeterPeakDemandModel.beta00_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_t_stat')

        # Deleting field 'MeterPeakDemandModel.cvrmse'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'cvrmse')

        # Deleting field 'MeterPeakDemandModel.last_month'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'last_month')

        # Deleting field 'MeterPeakDemandModel.beta07_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta04_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta08_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta10v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10v')

        # Deleting field 'MeterPeakDemandModel.beta10p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10p')

        # Deleting field 'MeterPeakDemandModel.F_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'F_stat')

        # Deleting field 'MeterPeakDemandModel.beta02p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02p')

        # Deleting field 'MeterPeakDemandModel.beta02v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02v')

        # Deleting field 'MeterPeakDemandModel.autocorr_coeff'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'autocorr_coeff')

        # Deleting field 'MeterPeakDemandModel.F_stat_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'F_stat_p_value')

        # Deleting field 'MeterPeakDemandModel.acceptance_score'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'acceptance_score')

        # Deleting field 'MeterPeakDemandModel.beta02_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta07_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta05v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05v')

        # Deleting field 'MeterPeakDemandModel.beta01_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta05p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05p')

        # Deleting field 'MeterPeakDemandModel.beta06_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.adj_r_squared'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'adj_r_squared')

        # Deleting field 'MeterPeakDemandModel.first_month'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'first_month')

        # Deleting field 'MeterPeakDemandModel.model_type'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'model_type')

        # Deleting field 'MeterPeakDemandModel.Yavg'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'Yavg')

        # Deleting field 'MeterPeakDemandModel.beta00v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00v')

        # Deleting field 'MeterPeakDemandModel.beta00p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00p')

        # Deleting field 'MeterPeakDemandModel.beta05_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_p_value')

        # Deleting field 'MeterPeakDemandModel.beta08_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_se')

        # Deleting field 'MeterPeakDemandModel.beta06_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta08_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta06_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_p_value')

        # Deleting field 'MeterPeakDemandModel.r_squared'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'r_squared')

        # Deleting field 'MeterPeakDemandModel.beta04_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta09_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta09_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta02_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_p_value')

        # Deleting field 'MeterPeakDemandModel.beta03_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_p_value')

        # Deleting field 'MeterPeakDemandModel.beta08_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_p_value')

        # Deleting field 'MeterPeakDemandModel.beta03_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta03_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_se')

        # Deleting field 'MeterPeakDemandModel.beta06_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_se')

        # Deleting field 'MeterPeakDemandModel.beta03_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_95_conf_int')

        # Deleting field 'MeterPeakDemandModel.beta03p'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03p')

        # Deleting field 'MeterPeakDemandModel.beta03v'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03v')

        # Deleting field 'MeterPeakDemandModel.beta09_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_se')

        # Deleting field 'MeterPeakDemandModel.beta07_p_value'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_p_value')

        # Deleting field 'MeterPeakDemandModel.SSQres'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'SSQres')

        # Deleting field 'MeterPeakDemandModel.beta00_se'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_se')

        # Deleting field 'MeterPeakDemandModel.beta02_t_stat'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_t_stat')

        # Deleting field 'MeterPeakDemandModel.beta10_95_conf_int'
        db.delete_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_95_conf_int')

        # Removing M2M table for field messages on 'MeterPeakDemandModel'
        db.delete_table('BuildingSpeakApp_meterpeakdemandmodel_messages')

        # Deleting field 'Monthling.cdd'
        db.delete_column('BuildingSpeakApp_monthling', 'cdd')

        # Deleting field 'Monthling.hdd'
        db.delete_column('BuildingSpeakApp_monthling', 'hdd')

        # Adding field 'Monthling.hdd_demand'
        db.add_column('BuildingSpeakApp_monthling', 'hdd_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.cdd_demand'
        db.add_column('BuildingSpeakApp_monthling', 'cdd_demand',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.hdd_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'hdd_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.cdd_consumption'
        db.add_column('BuildingSpeakApp_monthling', 'cdd_consumption',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'MeterConsumptionModel.predict_alpha'
        db.add_column('BuildingSpeakApp_meterconsumptionmodel', 'predict_alpha',
                      self.gf('django.db.models.fields.FloatField')(default=0.05, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Meter.Tccp'
        db.add_column('BuildingSpeakApp_meter', 'Tccp',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Meter.Thcp'
        db.add_column('BuildingSpeakApp_meter', 'Thcp',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Meter.Tccp_demand'
        db.delete_column('BuildingSpeakApp_meter', 'Tccp_demand')

        # Deleting field 'Meter.Thcp_demand'
        db.delete_column('BuildingSpeakApp_meter', 'Thcp_demand')

        # Deleting field 'Meter.Tccp_consumption'
        db.delete_column('BuildingSpeakApp_meter', 'Tccp_consumption')

        # Deleting field 'Meter.Thcp_consumption'
        db.delete_column('BuildingSpeakApp_meter', 'Thcp_consumption')

        # Adding field 'MeterPeakDemandModel.beta00_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.meter'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'meter',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BuildingSpeakApp.Meter'], null=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta06v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta06p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta09_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta04_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta07_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta09p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta00_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta09v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta01p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta01v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.df'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'df',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta10_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta01_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta01_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.rmse'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'rmse',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta04_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta08v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta08p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta05_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta04p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta02_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta04v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.nbe'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'nbe',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta05_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta10_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta10_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta01_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta05_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta07v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta07p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta00_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.cvrmse'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'cvrmse',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.last_month'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'last_month',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta07_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta04_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta08_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta10v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta10p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.F_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'F_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta02p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta02v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.autocorr_coeff'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'autocorr_coeff',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.F_stat_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'F_stat_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.acceptance_score'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'acceptance_score',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta02_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta07_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta05v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta01_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta01_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta05p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta06_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.adj_r_squared'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'adj_r_squared',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.first_month'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'first_month',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.model_type'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'model_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.Yavg'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'Yavg',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta00v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta00p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta05_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta05_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta08_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta06_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta08_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta06_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.r_squared'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'r_squared',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta04_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta04_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta09_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta09_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta02_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta03_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta08_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta08_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta03_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta03_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta06_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta06_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta03_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta03p'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03p',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta03v'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta03v',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta09_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta09_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta07_p_value'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta07_p_value',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.SSQres'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'SSQres',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta00_se'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta00_se',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta02_t_stat'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta02_t_stat',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MeterPeakDemandModel.beta10_95_conf_int'
        db.add_column('BuildingSpeakApp_meterpeakdemandmodel', 'beta10_95_conf_int',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field messages on 'MeterPeakDemandModel'
        db.create_table('BuildingSpeakApp_meterpeakdemandmodel_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meterpeakdemandmodel', models.ForeignKey(orm['BuildingSpeakApp.meterpeakdemandmodel'], null=False)),
            ('message', models.ForeignKey(orm['BuildingSpeakApp.message'], null=False))
        ))
        db.create_unique('BuildingSpeakApp_meterpeakdemandmodel_messages', ['meterpeakdemandmodel_id', 'message_id'])

        # Adding field 'Monthling.cdd'
        db.add_column('BuildingSpeakApp_monthling', 'cdd',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Monthling.hdd'
        db.add_column('BuildingSpeakApp_monthling', 'hdd',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True),
                      keep_default=False)

        # Deleting field 'Monthling.hdd_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'hdd_demand')

        # Deleting field 'Monthling.cdd_demand'
        db.delete_column('BuildingSpeakApp_monthling', 'cdd_demand')

        # Deleting field 'Monthling.hdd_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'hdd_consumption')

        # Deleting field 'Monthling.cdd_consumption'
        db.delete_column('BuildingSpeakApp_monthling', 'cdd_consumption')

        # Deleting field 'MeterConsumptionModel.predict_alpha'
        db.delete_column('BuildingSpeakApp_meterconsumptionmodel', 'predict_alpha')


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
            'percent_fixed': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
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
            'Tccp_consumption': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Tccp_demand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Thcp_consumption': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Thcp_demand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
        'BuildingSpeakApp.meterconsumptionmodel': {
            'F_stat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'F_stat_p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'MeterConsumptionModel'},
            'SSQres': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
            'predict_alpha': ('django.db.models.fields.FloatField', [], {'default': '0.05', 'null': 'True', 'blank': 'True'}),
            'r_squared': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rmse': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'BuildingSpeakApp.meterpeakdemandmodel': {
            'Meta': {'object_name': 'MeterPeakDemandModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'cdd_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
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
            'hdd_demand': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
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