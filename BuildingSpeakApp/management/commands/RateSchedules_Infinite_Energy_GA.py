from django.core.management.base import BaseCommand

from decimal import Decimal
from BuildingSpeakApp.models import InfiniteEnergyGAGas, Utility

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        infe = Utility.objects.get(name='Infinite Energy')
        
        bizgas1 = InfiniteEnergyGAGas(
            name = 'Fixed Business Rate',
            utility = infe,
            basic_service_charge = Decimal(20),
            tax_percentage = Decimal(0.08),
            therm_rate = Decimal(0.66),
            )
        bizgas1.save()
        
