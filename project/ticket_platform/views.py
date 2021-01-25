from django.db.models import F
from django.shortcuts import render, redirect
from .models import Event, Ticket, Account
from django.views import View
from django.views.generic import ListView
from .forms import AddEventForm, BuyTicketsForm, SignUpForm, BuyReservedForm
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SuperuserRequiredMixin
from django.contrib.auth.models import User
import uuid


from datetime import datetime

# Create your views here.

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('listing')

class UserLogoutView(LogoutView):
    template_name = 'user/logout.html'
    success_url = reverse_lazy('listing')

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'user/sign_up.html'
    success_url = reverse_lazy('listing')


class EventListingView(ListView):
    paginate_by = 20
    model = Event
    template_name = 'event_list.html'


class AddEventView(SuperuserRequiredMixin, CreateView):
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

class EventUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Event
    template_name = 'event_form.html'
    success_url = reverse_lazy('listing')
    form_class = AddEventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_function'] = 'Update Event'
        return context

class EventDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('listing')

class BuyTicketView(FormView):
    model = Ticket

    form_class = BuyTicketsForm

    def get(self, request, event_pk, ticket_type, sold_reserved):
        message = 'buy'
        if sold_reserved == 1:
            message = 'reserve'
        return render(request, 'buy_ticket_form.html', {'message': message})



    def charge(self, amount, currency='EUR'):
        account = Account.objects.get(currency=currency)
        account.balance += amount
        account.save()

    def form_valid(self, form, *args, **kwargs):
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

        new_ticket_id = None
        new_ticket_action = None
        no_ticket_message = None

        if ticket_left > 0:
            if sold_reserved == 0:
                self.charge(amount=ticket_price, currency='EUR')

            ticket = Ticket(event=event, sold_reserved=sold_reserved, ticket_type=ticket_type)
            ticket.save()
            new_ticket_id = ticket.id
            new_ticket_action = 'purchased' if sold_reserved == 1 else 'reserved'
        else:
            no_ticket_message = 'There is no more ticket available for this event'

        # return super(BuyTicketView, self).form_valid(form)
        return render(self.request, template_name='purchase_confirmation.html', context={"new_ticket_id": new_ticket_id, "new_ticket_action": new_ticket_action, "no_ticket_message": no_ticket_message})

class BuyReservedView(FormView):
    # model = Ticket
    template_name = 'buy_reserved.html'
    success_url = reverse_lazy('listing')
    form_class = BuyReservedForm

    def form_valid(self, form, *args, **kwargs):
        id = None
        new_ticket_action = None
        no_ticket_message = None

        try:
            id = form.cleaned_data.get('id')
            ticket = Ticket.objects.get(id=id)
            ticket.sold_reserved = 0
            ticket.save()
            new_ticket_action = 'purchased'
        except:
            no_ticket_message = 'No such reservation'
        return render(self.request, template_name='purchase_confirmation.html',
                      context={"new_ticket_id": id, "new_ticket_action": new_ticket_action,
                               "no_ticket_message": no_ticket_message})

