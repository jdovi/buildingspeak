from django.core.management.base import BaseCommand

from BuildingSpeakApp.models import Utility

class Command(BaseCommand):

    def handle(self, *args, **options):

        atlw = Utility(
            name = 'City of Atlanta, Dept. of Watershed Mgmt.',
            )
        
        atlw.save()
        
        #post-creation actions: upload utility logo to Utility.image_file