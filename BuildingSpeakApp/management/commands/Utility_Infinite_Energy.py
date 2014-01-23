from django.core.management.base import BaseCommand

from BuildingSpeakApp.models import Utility

class Command(BaseCommand):

    def handle(self, *args, **options):

        infe = Utility(
            name = 'Infinite Energy',
            )
        
        infe.save()
        
        #post-creation actions: upload utility logo to Utility.image_file