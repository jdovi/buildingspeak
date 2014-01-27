from django.db import models
from django.core import urlresolvers
from storages.backends.s3boto import S3BotoStorage

from models_functions import *


class Utility(models.Model):
    """Model for utility providers.  Accepts
    logo image file.  Parents Rate Schedules."""
    name = models.CharField(blank=True, max_length=200)
    
    #relationships
    messages = models.ManyToManyField('Message', blank=True)
    
    #file-related attributes
    image_file = models.FileField(null=True, blank=True, upload_to=image_file_path_utility, 
                    storage=S3BotoStorage(location='utility_files'),
                    help_text='link to utility logo file')

    #functions
    def rate_schedules_for_admin(self):
        return '<br>'.join(['<a href="%s">%s</a>' % (urlresolvers.reverse('admin:BuildingSpeakApp_rateschedule_change',args=(rs.id,)), rs.name) for rs in self.rateschedule_set.all()])
    rate_schedules_for_admin.allow_tags = True
    rate_schedules_for_admin.short_description = 'Rates'
    def __unicode__(self):
        return self.name
    class Meta:
        app_label = 'BuildingSpeakApp'
