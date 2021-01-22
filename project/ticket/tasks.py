from celery import shared_task
from django.core.management import call_command


@shared_task
def delete_overdue_reservations():
    call_command("delayed_reservations", )