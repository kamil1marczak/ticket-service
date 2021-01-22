from django.contrib import admin

# Register your models here.
from .models import Ticket, Account, Event

admin.site.register(Ticket)
admin.site.register(Account)
admin.site.register(Event)