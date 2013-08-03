import csv, pytz, os, inspect, itertools, requests
from BuildingSpeakApp.models import Equipment, Message
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from decimal import Decimal

rtu_tracking_array_names = [
'time_stamps',
'A',
'V',
'ph',
'pf',
'kW',
'ng_btuh_in',
'ng_btuh_del',
'ng_eta',
'ng_cfm',
'ng_HV',
'st_h_in',
'st_h_out',
'st_btuh_del',
'st_flow',
'cw_flow',
'cw_temp_in',
'cw_temp_out',
'cw_tons_del',
'hw_flow',
'hw_temp_in',
'hw_temp_out',
'hw_btuh_del',
'fo_btuh_in',
'fo_btuh_del',
'fo_eta',
'fo_gpm',
'fo_HV',
'rtu_SAT',
'rtu_SAH',
'rtu_SAF',
'rtu_SAP',
'rtu_RAT',
'rtu_RAH',
'rtu_RAF',
'rtu_RAP',
'rtu_OAT',
'rtu_OAH',
'rtu_OAF',
'rtu_OAP',
'rtu_MAT',
'rtu_MAH',
'rtu_MAF',
'rtu_MAP',
'rtu_SPT',
'rtu_SPH',
'rtu_SPP',
'rtu_dP_filter',
'rtu_dP_cooling_coil',
'rtu_dP_supply_fan',
'rtu_eta_fan',
'rtu_eta_motor',
'rtu_eta_drive',
'rtu_RFC',
'rtu_tons_del',
'rtu_btuh_del',
'rtu_eta_cool',
'rtu_eta_heat',
'rtu_speed',
'rtu_setpoints_cool_occ',
'rtu_setpoints_cool_uno',
'rtu_setpoints_heat_occ',
'rtu_setpoints_heat_uno',
'rtu_setpoints_RFC',
'rtu_status_unit',
'rtu_status_cool',
'rtu_status_heat',
'rtu_status_econ',
'rtu_status_supply_fan',
'rtu_status_return_fan',
'rtu_status_condenser_fan']

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        for equip in Equipment.objects.all():
            
            if (    not(equip.data_file_ignore) and
                    (equip.data_file_channel_names is not None) and
                    (len(equip.data_file_channel_names)!=0)             ):
                r = requests.get(equip.data_file.url)
                if r.status_code == 404: #not found error code
                    m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
                                message_type='error',
                                subject='reading data file',
                                comment=''.join(['Data file missing for equipment ' + equip.name,
                                                 ' serving building(s) ',
                                                 ','.join([x.name for x in equip.building_set.all()]),
                                                 ' via meter(s) ',
                                                 ','.join([x.name for x in equip.meter_set.all()]),
                                                 ' under account ', equip.parent_account_name(),
                                                 ' (Equipment pk = ',
                                                 '%06d)' % equip.pk]),
                                notes='Running ' + __file__ + ' in ' + 
                                    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                                )
                    m.save()
                    equip.messages.add(m)
                    equip.save()
                elif r.status_code == 200: #all-is-well code
                    csvfilereader = csv.reader(equip.data_file, delimiter=',', quotechar='|')
                    some_data_read_in = False #flag set if/when data actually read into Equipment
                    ti = equip.data_file_channel_indices[equip.data_file_channel_names.index('time_stamps')]
                    for row in csvfilereader:
                        try:
                            t_raw = datetime.strptime(row[ti], equip.data_file_time_format) #tz naive
                            t_shifted = t_raw - timedelta(hours=float(equip.data_file_GMT_offset)) #shift to utc
                            t_utc = t_shifted.replace(tzinfo=pytz.utc) #then make tz aware and store in utc
                            if ( (equip.time_stamps is not None) and 
                                 (len(equip.time_stamps)!=0) and
                                 (t_utc <= equip.time_stamps[-1]) ):  #if data on row is old, ignore it
                                pass
                            else:
                                for i,chan in itertools.izip(equip.data_file_channel_indices,
                                                             equip.data_file_channel_names):
                                    if chan == 'time_stamps':
                                        x = equip.__getattribute__(chan)
                                        if x is None: x = []
                                        x.extend([t_utc])
                                        equip.__setattr__(chan,x)
                                    else:
                                        x = equip.__getattribute__(chan)
                                        if x is None: x = []
                                        x.extend([Decimal(row[i])])
                                        equip.__setattr__(chan,x)
                                    some_data_read_in = True
                                for unchan in rtu_tracking_array_names:
                                    if unchan in equip.data_file_channel_names:
                                        pass #skip if it's a tracked field
                                    else:
                                        x = equip.__getattribute__(unchan)
                                        if x is None: x = []
                                        x.extend([Decimal('nan')])
                                        equip.__setattr__(unchan,x)
                        except ValueError:
                            pass #ignore the error due to non-data row and keeping reading data file
                        except IndexError:
                            pass #ignore the error, keep reading data file to get to data rows
                    if some_data_read_in:
                        m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
                                    message_type='task completed',
                                    subject='reading data file',
                                    comment=''.join(['Successfully read data file for equipment ' + equip.name,
                                                     ' serving building(s) ',
                                                     ','.join([x.name for x in equip.building_set.all()]),
                                                     ' via meter(s) ',
                                                     ','.join([x.name for x in equip.meter_set.all()]),
                                                     ' under account ', equip.parent_account_name(),
                                                     ' (Equipment pk = ',
                                                     '%06d)' % equip.pk]),
                                    notes='Running ' + __file__ + ' in ' + 
                                        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                                    )
                        m.save()
                        equip.messages.add(m)
                        equip.save()
                    else:
                        m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
                                    message_type='warning',
                                    subject='reading data file',
                                    comment=''.join(['Successfully read data file but no data found for equipment ' + equip.name,
                                                     ' serving building(s) ',
                                                     ','.join([x.name for x in equip.building_set.all()]),
                                                     ' via meter(s) ',
                                                     ','.join([x.name for x in equip.meter_set.all()]),
                                                     ' under account ', equip.parent_account_name(),
                                                     ' (Equipment pk = ',
                                                     '%06d)' % equip.pk]),
                                    notes='Running ' + __file__ + ' in ' + 
                                        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) +
                                        '. Possible problems: mismatch between Equipment''s data file ' +
                                        'time format and actual data file''s time format; all data in file ' +
                                        'older than most recent data already stored in Equipment.'
                                    )
                        m.save()
                        equip.messages.add(m)
                        equip.save()
                else: #something went wrong but we don't know what
                    m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
                                message_type='error',
                                subject='reading data file',
                                comment=''.join(['Unknown error loading data file for equipment ' + equip.name,
                                                 ' serving building(s) ',
                                                 ','.join([x.name for x in equip.building_set.all()]),
                                                 ' via meter(s) ',
                                                 ','.join([x.name for x in equip.meter_set.all()]),
                                                 ' under account ', equip.parent_account_name(),
                                                 ' (Equipment pk = ',
                                                 '%06d)' % equip.pk]),
                                notes='Running ' + __file__ + ' in ' + 
                                    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                                )
                    m.save()
                    equip.messages.add(m)
                    equip.save()

