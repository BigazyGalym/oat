from django.core.management.base import BaseCommand
from orders.models import ServiceType

class Command(BaseCommand):
       help = 'Seeds the database with initial ServiceType data'

       def handle(self, *args, **options):
           service_types = [
               {'name': 'Tractor', 'description': 'Тракторные услуги'},
               {'name': 'Kamaz', 'description': 'Услуги КамАЗ'},
           ]
           for st in service_types:
               ServiceType.objects.get_or_create(name=st['name'], defaults=st)
           self.stdout.write(self.style.SUCCESS('Successfully seeded ServiceType data'))