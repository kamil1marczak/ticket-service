from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Event, Ticket, Account


class EventTests(APITestCase):
    data = {
               "event_date_time": "2021-01-29T00:00:00Z",
               "name": "test event name",
               "description": "test event description",
               "price_regular": 10.0,
               "price_premium": 20.0,
               "price_vip": 100.0,
               "regular_tickets_number": 1000,
               "premium_tickets_number": 500,
               "vip_tickets_number": 100,
           }
    url = reverse('event-list')


    def test_create_event_without_token(self):

        response_data = {
            "detail": "Authentication credentials were not provided."
        }

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, response_data)

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.event_fixture = Event.objects.create(event_date_time='2021-01-29 01:00:00+01', name='A$AP concert',
                             description='A$AP concert longer description', price_regular=10, price_premium=20,
                             price_vip=100, regular_tickets_number=1000, premium_tickets_number=500,
                             vip_tickets_number=100)

        self.url_detail = reverse('event-detail', kwargs={'pk': self.event_fixture.pk})

    def test_create_event_with_token(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, self.data, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(self.data, response.data)

    def test_event_list(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        # self.assertDictContainsSubset(self.data, response.data)

    def test_event_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url_detail, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        expected_response_part = {"description": "A$AP concert longer description"}
        self.assertDictContainsSubset(expected_response_part, response.data)

    def test_event_put(self):
        self.client.force_login(user=self.user)
        response = self.client.put(self.url_detail, self.data, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(self.data, response.data)

    def test_event_patch(self):
        self.client.force_login(user=self.user)
        partial_data = {"description": "patch description"}
        response = self.client.patch(self.url_detail, partial_data, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(partial_data, response.data)


