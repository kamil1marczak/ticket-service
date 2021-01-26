from django.db import models
from django.db.models import Count, Q
from datetime import datetime, timedelta
import uuid
from django.utils.functional import cached_property


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_date_time = models.DateTimeField(db_index=True)
    name = models.CharField(db_index=True, max_length=200, null=False, unique=True)
    description = models.TextField(db_index=True, max_length=1024, null=True)
    price_regular = models.FloatField(db_index=True, null=True)
    price_premium = models.FloatField(db_index=True, null=True)
    price_vip = models.FloatField(db_index=True, null=True)
    regular_tickets_number = models.IntegerField(db_index=True, null=False, default=0)
    premium_tickets_number = models.IntegerField(db_index=True, null=False, default=0)
    vip_tickets_number = models.IntegerField(db_index=True, null=False, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # @property
    @cached_property
    def tickets_sold(self):
        tickets = self.ticket_set
        tickets.regular = tickets.filter(ticket_type=0).count()
        tickets.premium = tickets.filter(ticket_type=1).count()
        tickets.vip = tickets.filter(ticket_type=2).count()

        return tickets

    # @property
    @cached_property
    def tickets_left(self):
        tickets = self.ticket_set
        tickets.regular = self.regular_tickets_number - tickets.filter(ticket_type=0).count()
        tickets.premium = self.premium_tickets_number - tickets.filter(ticket_type=1).count()
        tickets.vip = self.vip_tickets_number - tickets.filter(ticket_type=2).count()

        return tickets

    def __str__(self):
        return self.name

class Ticket(models.Model):

    ticket_types_choices = (
        (0, 'Regular'),
        (1, 'Premium'),
        (2, 'VIP'),
    )

    sold_reserve_choices = (
        (0, 'sold'),
        (1, 'reserved'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_type = models.SmallIntegerField(db_index=True, choices=ticket_types_choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sold_reserved = models.SmallIntegerField(db_index=True, choices=sold_reserve_choices)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.event} - ticket_type: {self.ticket_type} - id: {self.id}"

class Account(models.Model):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    currencies = (
        ('EUR', 'Euro'),
        ('USD', 'US Dollar'),
        ('PLN', 'Polish Zloty'),
    )

    id = models.AutoField(primary_key=True,)
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier',)
    currency = models.CharField(db_index=True, choices=currencies, max_length=4)
    balance = models.PositiveIntegerField(verbose_name='Current balance', default=0)



    def __str__(self):
        return f"current balance {self.balance} {self.currency}"

