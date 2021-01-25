from django.contrib.auth.models import User, Group
from .models import Event, Ticket, Account
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'



class TicketSerializer(serializers.ModelSerializer):
    # event = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Ticket
        # fields = ['ticket_type', 'sold_reserved', 'event']
        fields = '__all__'

    def charge(self, amount, currency='EUR'):
        account = Account.objects.get(currency=currency)
        account.balance += amount
        account.save()

    def create(self, validated_data):

        ticket_type = int(self.validated_data['ticket_type'])
        sold_reserved = int(self.validated_data['sold_reserved'])
        event = self.validated_data['event']

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

        # return Ticket.objects.create(**validated_data)
            return ticket
        else:
            return None

    def update(self, instance, validated_data):
        if instance.sold_reserved == 1:
            instance.sold_reserved = 0
            ticket_price = 0
            if instance.ticket_type == 0:
                ticket_price = instance.event.price_regular
            elif instance.ticket_type == 1:
                ticket_price = instance.event.price_premium
            elif instance.ticket_type == 2:
                ticket_price = instance.event.price_vip

            self.charge(amount=ticket_price, currency='EUR')

            instance.save()
            return instance
        else:
            return None

