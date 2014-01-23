from django.core.management.base import BaseCommand

from BuildingSpeakApp.models import Utility

class Command(BaseCommand):

    def handle(self, *args, **options):

        GPC = Utility(
            name = 'Georgia Power Company',
            )
        
        GPC.save()
        
        #post-creation actions: upload utility logo to Utility.image_file