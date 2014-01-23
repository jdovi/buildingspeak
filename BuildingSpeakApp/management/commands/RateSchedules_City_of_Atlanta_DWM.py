from django.core.management.base import BaseCommand

from decimal import Decimal
from BuildingSpeakApp.models import CityOfATLWWW, Utility

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        atlw = Utility.objects.get(name='City of Atlanta, Dept. of Watershed Mgmt.')
        
        w_ww = CityOfATLWWW(
            name = 'Water and Wastewater 2012',
            utility = atlw,
            base_charge = Decimal(13.12),
            tax_percentage = Decimal(0.08),
            tier1 = Decimal(4.0),
            tier2 = Decimal(7.0),
            tier3 = Decimal(999999999),
            rate1 = Decimal(12.32),
            rate2 = Decimal(18.98),
            rate3 = Decimal(21.85),
            security_surcharge = Decimal(0.15),
            )
        w_ww.save()
        
