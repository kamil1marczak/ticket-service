from django import forms
from .models import Event, Ticket, Account
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class DateInput(forms.DateInput):
    input_type = 'date'

class AddEventForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)
        self.fields['price_regular'].required = False
        self.fields['regular_tickets_number'].required = False
        self.fields['price_premium'].required = False
        self.fields['price_vip'].required = False
        self.fields['vip_tickets_number'].required = False

    class Meta:
        model = Event

        fields = ['event_date_time', 'name', 'description', 'price_regular', 'regular_tickets_number', 'price_premium', 'premium_tickets_number', 'price_vip', 'vip_tickets_number']

        widgets = {
            'event_date_time': DateInput(),
        }

        labels = {
            'name': _('Title of the event'),
            'description': _('Description of the event'),
            'price_regular': _('Price for regular type tickets'),
            'regular_tickets_number': _('Number of regular type tickets'),
            'price_premium': _('Price for premium type tickets'),
            'premium_tickets_number': _('Number of premium type tickets'),
            'price_vip': _('Price for VIP type tickets'),
            'vip_tickets_number': _('Number of VIP type tickets'),

        }
        help_texts = {
            'name': _('title have to be 200 characters or shorter'),
            'description': _('title have to be 1024 characters (10pt page) or shorter'),
        }
        error_messages = {
            'name': {
                'max_length': _("This event's title is too long."),
            },
            'description': {
                'max_length': _("This event's description is too long."),
            },
        }

class BuyTicketsForm(ModelForm):


    class Meta:
        model = Ticket
        fields = []
        # fields = ['event', 'ticket_type', 'sold_reserved']

