from django.core.management.base import BaseCommand
from ticket_platform.models import Account


class Command(BaseCommand):
    help = 'Add EUR account'

    def handle(self, *args, **kwargs):
        account = Account(currency='EUR')

        self.stdout.write("EUR account ha been created")
