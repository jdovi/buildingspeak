#import dbarray
import pandas as pd
from pytz import UTC
from numpy import NaN
from django.db import models
from croniter import croniter
from django.utils import timezone
from django.core import urlresolvers
from decimal import getcontext, Decimal
from datetime import datetime, timedelta
from djorm_pgarray.fields import ArrayField
from model_utils.managers import InheritanceManager
from storages.backends.s3boto import S3BotoStorage
from django.contrib.auth.models import User

from models_functions import *


class KnowsChild(models.Model):
    """This class makes it
    possible to call the
    base class but run
    subclass functions on
    the base class instances
    accessible by calling
    the base class.
    
    Example: 
        Animal has speak()=Generic
        Dog has speak()=Woof
        Cat has speak()=Meow
        
        KnowsChild enables the
        following to produce
        the desired Woof/Woof/
        Meow instead of Generic/
        Generic/Generic.
        
        Dog.objects.create()
        Dog.objects.create()
        Cat.objects.create()
        for animal in Animal.objects.all():
            animal.as_child().speak()
    
    Given RateSchedule and
    RateScheduleSubclass
    both with what_am_i()
    functions with simple
    print statements, we get:
        >>>RateSchedule.objects.filter(_my_subclass='rateschedulesubclass')[0].what_am_i()
        i am a RateSchedule

        >>>RateSchedule.objects.filter(_my_subclass='rateschedulesubclass')[0].as_child().what_am_i()
        i am a SUB
    """
    # Make a place to store the class name of the child
    _my_subclass = models.CharField(max_length=200) 
 
    class Meta:
        abstract = True
        app_label = 'BuildingSpeakApp'
 
    def as_child(self):
        return getattr(self, self._my_subclass)
 
    def save(self, *args, **kwargs):
        # save what kind we are.
        self._my_subclass = self.__class__.__name__.lower() 
        super(KnowsChild, self).save(*args, **kwargs)
    
class RateSchedule(KnowsChild):
    """Superclass for Utility
    RateSchedules. Parents
    Meters.  Uses KnowsChild
    abstract class to enable
    access to subclass instance
    functions from superclass
    instances (Django default
    is to return the superclass
    instance, which requires
    knowledge of the subclass
    names in order to access
    the subclass instances
    themselves)."""
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    utility = models.ForeignKey('Utility')
    riders = models.ManyToManyField('RateScheduleRider')
    messages = models.ManyToManyField('Message')
    
    #file-related attributes
    rate_file = models.FileField(null=True, blank=True, upload_to=rate_file_path_rate_schedule, 
                    storage=S3BotoStorage(location='utility_files'),
                    help_text='link to rate schedule file')
    
    #functions
    def utility_name_for_admin(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_utility_change',args=(self.utility.id,)), self.utility.name)
    utility_name_for_admin.allow_tags = True
    utility_name_for_admin.short_description = 'Provider'
    def connected_meter_names_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_meter_change',args=(meter.id,)), meter.name) for meter in self.meter_set.all()])
    connected_meter_names_for_admin.allow_tags = True
    connected_meter_names_for_admin.short_description = 'Connected Meters'
    
    #functions expected to be defined on all subclasses to enable universal
    #calling across all RateSchedules, regardless of subclass type
    def __unicode__(self):
        print 'Warning: should be using subclass instance of actual rate schedule, not the parent superclass RateSchedule.'
        return self.name
    def get_cost_df(self, df):
        """Empty function on superclass
        RateSchedule; should be coded
        in subclasses and called from
        there using as_child() function
        as necessary on RateSchedule
        querysets.
        
        Return df with Cost column or
        original df if unable to 
        complete calculation."""
        print 'Warning: should be using subclass instance of actual rate schedule, not the parent superclass RateSchedule.'
    def is_eligible_df(self, df):
        """Empty function on superclass
        RateSchedule; should be coded
        in subclasses and called from
        there using as_child() function
        as necessary on RateSchedule
        querysets.
        
        Return True, False, or None
        if not enough information
        or data points."""
        print 'Warning: should be using subclass instance of actual rate schedule, not the parent superclass RateSchedule.'
    def get_billing_demand_df(self, df):
        """Empty function on superclass
        RateSchedule; should be coded
        in subclasses and called from
        there using as_child() function
        as necessary on RateSchedule
        querysets.
        
        Return df with Billing Demand
        column or original df if
        unable to calculated Billing
        Demand."""
        print 'Warning: should be using subclass instance of actual rate schedule, not the parent superclass RateSchedule.'
    class Meta:
        app_label = 'BuildingSpeakApp'

class RateScheduleRider(KnowsChild):
    """Superclass for Utility
    RateSchedule Riders. Uses
    KnowsChild abstract class
    to enable access to
    subclass instance functions
    from superclass instances
    (Django default is to
    return the superclass
    instance, which requires
    knowledge of the subclass
    names in order to access
    the subclass instances
    themselves)."""
    name = models.CharField(blank=True, max_length=200)

    #relationships
    utility = models.ForeignKey('Utility')
    messages = models.ManyToManyField('Message')
    
    #file-related attributes
    rider_file = models.FileField(null=True, blank=True, upload_to=rate_file_path_rate_schedule, 
                    storage=S3BotoStorage(location='utility_files'),
                    help_text='link to rate schedule rider file')

    #functions expected to be defined on all subclasses to enable universal
    #calling across all RateScheduleRiders, regardless of subclass type
    def __unicode__(self):
        print 'Warning: should be using subclass instance of actual rider, not the parent superclass RateScheduleRider.'
        return self.name
    def get_cost_df(self, df):
        """Empty function on superclass
        RateScheduleRider; should be coded
        in subclasses and called from
        there using as_child() function
        as necessary on RateScheduleRider
        querysets.
        
        Return df with Cost column or
        original df if unable to 
        complete calculation."""
        print 'Warning: should be using subclass instance of actual rider, not the parent superclass RateScheduleRider.'
        
    class Meta:
        app_label = 'BuildingSpeakApp'

