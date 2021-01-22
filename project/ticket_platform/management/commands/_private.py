
from ticket_platform.models import Event, TicketType, Ticket
from django.contrib.auth.models import User

def add_ticket_types():
    TicketType.objects.bulk_create([
        TicketType(id=1, name='regular'),
        TicketType(id=2, name='premium'),
        TicketType(id=3, name='VIP'),
        ])

