from django.core.management.base import BaseCommand

from BuildingSpeakApp.models import Account
from BuildingSpeak.settings import STATIC_URL
from django.core.files import File
account = Account.objects.get(id=1)

class Command(BaseCommand):

    def handle(self, *args, **options):
        file_url = STATIC_URL + 'site/temporary_files/Account_Image_City_of_Refuge.jpg'
        file_obj = File(open(file_url))
        account.__setattr__('image_file', file_obj)
        account.save()