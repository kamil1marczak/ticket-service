from datetime import timedelta, time, datetime

from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import make_aware

from ticket_platform.models import Ticket


now = timezone.now()
time_limit = now - timedelta(minutes=15)


class Command(BaseCommand):
    help = "Detect and delete all outdated reservations (older than 15 minute)"

    def handle(self, *args, **options):
        # orders = Order.objects.filter(confirmed_date__range=(today_start, today_end))
        overdue_reservations = Ticket.objects.filter(Q(sold_reserved=1) & Q(created__lte=time_limit))

        if overdue_reservations is not None:
            overdue_count = overdue_reservations.count()
            overdue_reservations.delete()

            self.stdout.write(f"{overdue_count} overdue reservations have been deleted")
        else:
            self.stdout.write("No overdue reservation")
