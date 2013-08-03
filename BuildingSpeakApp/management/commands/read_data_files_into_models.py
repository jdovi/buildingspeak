#import csv, pytz, os, inspect, itertools, requests
from BuildingSpeakApp.models import Account, Building, Floor, Meter, Equipment
#from BuildingSpeakApp.models import Message
from django.core.management.base import BaseCommand
#from datetime import datetime, timedelta
#from decimal import Decimal

class Command(BaseCommand):

    def handle(self, *args, **options):

        [x.update_readers() for x in Account.objects.all()]
        [x.update_readers() for x in Building.objects.all()]
        [x.update_readers() for x in Floor.objects.all()]
        [x.update_readers() for x in Meter.objects.all()]
        [x.update_readers() for x in Equipment.objects.all()]
        
#        for equip in Equipment.objects.all():
#            
#                r = requests.get(equip.data_file.url)
#                if r.status_code == 404: #not found error code
#                    m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
#                                message_type='error',
#                                subject='reading data file',
#                                comment=''.join(['Data file missing for equipment ' + equip.name,
#                                                 ' serving building(s) ',
#                                                 ','.join([x.name for x in equip.building_set.all()]),
#                                                 ' via meter(s) ',
#                                                 ','.join([x.name for x in equip.meter_set.all()]),
#                                                 ' under account ', equip.parent_account_name(),
#                                                 ' (Equipment pk = ',
#                                                 '%06d)' % equip.pk]),
#                                notes='Running ' + __file__ + ' in ' + 
#                                    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#                                )
#                    m.save()
#                    equip.messages.add(m)
#                    equip.save()
#                elif r.status_code == 200: #all-is-well code
#                    csvfilereader = csv.reader(equip.data_file, delimiter=',', quotechar='|')
#                    some_data_read_in = False #flag set if/when data actually read into Equipment
#                    ti = equip.data_file_channel_indices[equip.data_file_channel_names.index('time_stamps')]
#                    for row in csvfilereader:
#                        try:
#                            t_raw = datetime.strptime(row[ti], equip.data_file_time_format) #tz naive
#                            t_shifted = t_raw - timedelta(hours=float(equip.data_file_GMT_offset)) #shift to utc
#                            t_utc = t_shifted.replace(tzinfo=pytz.utc) #then make tz aware and store in utc
#                            if ( (equip.time_stamps is not None) and 
#                                 (len(equip.time_stamps)!=0) and
#                                 (t_utc <= equip.time_stamps[-1]) ):  #if data on row is old, ignore it
#                                pass
#                            else:
#                                for i,chan in itertools.izip(equip.data_file_channel_indices,
#                                                             equip.data_file_channel_names):
#                                    if chan == 'time_stamps':
#                                        x = equip.__getattribute__(chan)
#                                        if x is None: x = []
#                                        x.extend([t_utc])
#                                        equip.__setattr__(chan,x)
#                                    else:
#                                        x = equip.__getattribute__(chan)
#                                        if x is None: x = []
#                                        x.extend([Decimal(row[i])])
#                                        equip.__setattr__(chan,x)
#                                    some_data_read_in = True
#                                for unchan in rtu_tracking_array_names:
#                                    if unchan in equip.data_file_channel_names:
#                                        pass #skip if it's a tracked field
#                                    else:
#                                        x = equip.__getattribute__(unchan)
#                                        if x is None: x = []
#                                        x.extend([Decimal('nan')])
#                                        equip.__setattr__(unchan,x)
#                        except ValueError:
#                            pass #ignore the error due to non-data row and keeping reading data file
#                        except IndexError:
#                            pass #ignore the error, keep reading data file to get to data rows
#                    if some_data_read_in:
#                        m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
#                                    message_type='task completed',
#                                    subject='reading data file',
#                                    comment=''.join(['Successfully read data file for equipment ' + equip.name,
#                                                     ' serving building(s) ',
#                                                     ','.join([x.name for x in equip.building_set.all()]),
#                                                     ' via meter(s) ',
#                                                     ','.join([x.name for x in equip.meter_set.all()]),
#                                                     ' under account ', equip.parent_account_name(),
#                                                     ' (Equipment pk = ',
#                                                     '%06d)' % equip.pk]),
#                                    notes='Running ' + __file__ + ' in ' + 
#                                        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#                                    )
#                        m.save()
#                        equip.messages.add(m)
#                        equip.save()
#                    else:
#                        m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
#                                    message_type='warning',
#                                    subject='reading data file',
#                                    comment=''.join(['Successfully read data file but no data found for equipment ' + equip.name,
#                                                     ' serving building(s) ',
#                                                     ','.join([x.name for x in equip.building_set.all()]),
#                                                     ' via meter(s) ',
#                                                     ','.join([x.name for x in equip.meter_set.all()]),
#                                                     ' under account ', equip.parent_account_name(),
#                                                     ' (Equipment pk = ',
#                                                     '%06d)' % equip.pk]),
#                                    notes='Running ' + __file__ + ' in ' + 
#                                        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) +
#                                        '. Possible problems: mismatch between Equipment''s data file ' +
#                                        'time format and actual data file''s time format; all data in file ' +
#                                        'older than most recent data already stored in Equipment.'
#                                    )
#                        m.save()
#                        equip.messages.add(m)
#                        equip.save()
#                else: #something went wrong but we don't know what
#                    m = Message(time_stamp=datetime.utcnow().replace(tzinfo=pytz.utc),
#                                message_type='error',
#                                subject='reading data file',
#                                comment=''.join(['Unknown error loading data file for equipment ' + equip.name,
#                                                 ' serving building(s) ',
#                                                 ','.join([x.name for x in equip.building_set.all()]),
#                                                 ' via meter(s) ',
#                                                 ','.join([x.name for x in equip.meter_set.all()]),
#                                                 ' under account ', equip.parent_account_name(),
#                                                 ' (Equipment pk = ',
#                                                 '%06d)' % equip.pk]),
#                                notes='Running ' + __file__ + ' in ' + 
#                                    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#                                )
#                    m.save()
#                    equip.messages.add(m)
#                    equip.save()

