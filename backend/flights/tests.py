from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from flights.models import Flight, Airport
from flights.services import cleanup_archived_flights
import datetime

class FlightApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.airport = Airport.objects.create(
            code='SVO',
            name='Шереметьево',
            city='Москва',
            country='Россия',
            departures_count=100,
            arrivals_count=90,
            timezone='UTC+3'
        )
        self.flight = Flight.objects.create(
            flight_id='su-100',
            flight_number='SU 100',
            airline='Аэрофлот',
            aircraft='Airbus A320',
            from_code='SVO',
            from_name='Шереметьево',
            from_city='Москва',
            to_code='LED',
            to_name='Пулково',
            to_city='Санкт-Петербург',
            departure_time='10:00',
            arrival_time='11:30',
            departure_date=datetime.date.today().isoformat(),
            status='scheduled',
            status_text='По расписанию',
            price=4500
        )

    def test_flight_list_api(self):
        response = self.client.get(reverse('flight-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_flight_detail_api(self):
        response = self.client.get(reverse('flight-detail', kwargs={'flight_id': 'su-100'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['flightNumber'], 'SU 100')

    def test_airport_list_api(self):
        response = self.client.get(reverse('airport-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_cleanup_archived_flights(self):
        old_date = (datetime.date.today() - datetime.timedelta(days=20)).isoformat()
        Flight.objects.create(
            flight_id='old-flight-99',
            flight_number='OLD 99',
            airline='Old Air',
            from_code='SVO',
            from_name='SVO',
            from_city='Moscow',
            to_code='LED',
            to_name='LED',
            to_city='SPB',
            departure_time='09:00',
            arrival_time='10:30',
            departure_date=old_date,
            status='landed',
            status_text='Прибыл'
        )
        deleted = cleanup_archived_flights(days_retention=14)
        self.assertEqual(deleted, 1)
        self.assertFalse(Flight.objects.filter(flight_id='old-flight-99').exists())
