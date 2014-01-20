from django.db import models
from django.core import urlresolvers

from models_functions import *

class Message(models.Model):
    #Message class used to store all BuildingSpeak messages
    #use "object.messages.all()" to retrieve entire message log for a given object
    #use "object.messages.filter(field1 = value1)" to retrieve a subset of object's message log
    #use "object.messages.add(newmessage)" to add a Message to an object,
    #       where newmessage = Message(...set attributes here...)
    #message_type options: Code Warning, Code Error, User
    """Inputs:
        when = datetime
        message_type = string
        subject = string
        comment = text
        notes = text (staff notes entered via admin)
        
    Message may be attached to any BuildingSpeak
    model.  Used for capturing errors and 
    warnings during code execution as well as
    notifications to users."""
    
    when = models.DateTimeField(null=True, blank=True)
    dismissed = models.DateTimeField(null=True, blank=True)
    message_type = models.CharField(max_length=200,
                                    choices=[('Code Error', 'Code Error'),
                                             ('Code Warning', 'Code Warning'),
                                             ('Code Success', 'Code Success'),
                                             ('Model Info', 'Model Info'),
                                             ('Event', 'Event'),
                                             ('User Info', 'User Info'),
                                             ('Alert', 'Alert')])
    subject = models.CharField(max_length=200)
        #subjects should be short and sweet and generic; the comment holds specific details
        #common subjects:
            #Model created.
            #Open model data file failed.
            #Parse uploaded file to dataframe failed.
            #Retrieve class failed.
            #Retrieve model failed.
            #Swap model for string PK failed.
            #Swap model for string name failed.
            #Swap models for string PKs failed.
            #Model update failed.
            #Loaded and/or updated model.
            #Model load failed.
            #Model save failed.
            #Swap string PKs for models failed.
            #Created upload template.
            #Created processed file.
            #Write processed file failed.
            #No provided file being tracked.
            #Updated readers.
            #Update readers failed.
            #Adjust dataframe index failed.
            #File not found.
            #No observed_file being tracked.
            #Function received bad arguments.
            #Calculation failed.
            
    comment = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    def connected_models_for_admin(self):
        equiplist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_equipment_change',args=(equip.id,)), equip.name) for equip in self.equipment_set.all()])
        acctlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_account_change',args=(acct.id,)), acct.name) for acct in self.account_set.all()])
        bldglist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_building_change',args=(bldg.id,)), bldg.name) for bldg in self.building_set.all()])
        meterlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
        spacelist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_space_change',args=(space.id,)), space.name) for space in self.space_set.all()])
        rateschedulelist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_rateschedule_change',args=(rateschedule.id,)), rateschedule.name) for rateschedule in self.rateschedule_set.all()])
        utilitylist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_utility_change',args=(utility.id,)), utility.name) for utility in self.utility_set.all()])
        weatherstationlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_weatherstation_change',args=(weatherstation.id,)), weatherstation.name) for weatherstation in self.weatherstation_set.all()])
        managementactionlist = '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_managementaction_change',args=(managementaction.id,)), managementaction.name) for managementaction in self.managementaction_set.all()])
        return ''.join([equiplist,acctlist,bldglist,meterlist,spacelist,rateschedulelist,utilitylist,weatherstationlist,managementactionlist])
    connected_models_for_admin.allow_tags = True
    connected_models_for_admin.short_description = 'Connected Models'
    def __unicode__(self):
        return ': '.join([str(self.when),self.message_type,self.subject,self.comment])
    class Meta:
        app_label = 'BuildingSpeakApp'
