from django.core.management.base import BaseCommand

from BuildingSpeakApp.models import Account
from BuildingSpeak.settings import STATIC_URL
from django.core.files import File
import urllib

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        file_url = STATIC_URL + 'temporary_files/Account_Image_City_of_Refuge.jpg'
        result = urllib.urlretrieve(file_url)
        file_obj = File(open(result[0]))
        
        account = Account.objects.get(id=1)
        account.__setattr__('image_file', file_obj)
        account.save()