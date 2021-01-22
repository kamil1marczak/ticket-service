from django.db.models import F
from django.shortcuts import render, redirect
from .models import Event, Ticket, Account
from django.views import View
from django.views.generic import ListView
from .forms import AddEventForm, BuyTicketsForm
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime

# Create your views here.


class EventListingView(ListView):
    paginate_by = 20
    model = Event
    template_name = 'event_list.html'


class AddEventView(CreateView):
    model = Event
    # fields = ['event_date_time', 'name', 'description']
    # fields = '__all__'

    form_class = AddEventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('listing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_function'] = 'Add Event'
        return context

class EventUpdateView(UpdateView):
    model = Event
    template_name = 'event_form.html'
    success_url = reverse_lazy('listing')
    form_class = AddEventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_function'] = 'Update Event'
        return context

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('listing')

class BuyTicketView(FormView):
    model = Ticket
    success_url = reverse_lazy('listing')
    template_name = 'buy_ticket_form.html'
    form_class = BuyTicketsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sold_reserved = kwargs.get('sold_reserved')
        message = 'buy'
        if sold_reserved == 1:
            message = 'reserve'
        context['message'] = message
        return context

    def charge(self, amount, currency='EUR'):
        account = Account.objects.get(currency=currency)
        account.balance += amount
        account.save()

    def form_valid(self, form):
        event_pk = self.kwargs.get('event_pk')
        sold_reserved = self.kwargs.get('sold_reserved')
        event = Event.objects.get(pk=event_pk)

        ticket_type = self.kwargs.get('ticket_type')

        ticket_left = 0
        ticket_price = 0
        if ticket_type == 0:
            ticket_left = event.tickets_left.regular
            ticket_price = event.price_regular
        elif ticket_type == 1:
            ticket_left = event.tickets_left.premium
            ticket_price = event.price_premium
        elif ticket_type == 2:
            ticket_left = event.tickets_left.vip
            ticket_price = event.price_vip

        if ticket_left > 0:
            if sold_reserved == 0:
                self.charge(amount=ticket_price, currency='EUR')

            ticket = Ticket(event=event, sold_reserved=sold_reserved, ticket_type=ticket_type)
            ticket.save()
        else:
            pass

        return super(BuyTicketView, self).form_valid(form)
