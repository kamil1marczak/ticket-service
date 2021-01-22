from django.core.management.base import BaseCommand
from ticket_platform.models import Event


class Command(BaseCommand):
    help = 'Add predefined ticket types'

    def handle(self, *args, **kwargs):
        Event.objects.bulk_create([
            Event(event_date_time='2021-01-29 01:00:00+01' ,name='A$AP concert', description='A$AP concert longer description', price_regular=10, price_premium=20, price_vip=100, regular_tickets_number=1000, premium_tickets_number=500, vip_tickets_number=100),
            Event(event_date_time='2021-01-28 01:00:00+01' ,name='MC Mialan - FC Barcelona', description='Football match', price_regular=20, price_premium=50, price_vip=200, regular_tickets_number=1000, premium_tickets_number=500, vip_tickets_number=100),
            Event(event_date_time='2021-01-27 01:00:00+01' ,name='Street performance', description='independent artist treet performance', price_regular=10, regular_tickets_number=1000),
            Event(event_date_time='2021-01-27 01:00:00+01' ,name='Deadpool', description='Cinema premiere', price_regular=20, price_premium=30, regular_tickets_number=1000, premium_tickets_number=500),
            Event(event_date_time='2021-01-27 01:00:00+01' ,name='Arthemis Delta', description='Arthemis Delta concert longer description', price_regular=10, price_premium=20, price_vip=100, regular_tickets_number=1000, premium_tickets_number=500, vip_tickets_number=100),
        ])

        self.stdout.write("random events have been updated")
