from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import logging
from django.conf import settings
from django.core.mail import send_mail
from .models import Flight, Airport, NewsletterSubscriber

logger = logging.getLogger(__name__)
from .serializers import FlightSerializer, AirportSerializer
from .services import (
    fetch_and_sync_aviationstack_flights,
    seed_initial_database,
    update_dynamic_flight_lifecycle,
    cleanup_archived_flights,
)

class FlightListAPIView(APIView):
    """
    Returns filtered and searched list of flights.
    """
    def get(self, request):
        # Auto-seed if database is empty
        if not Flight.objects.exists():
            seed_initial_database()

        # Update dynamic statuses according to current time
        update_dynamic_flight_lifecycle()

        queryset = Flight.objects.all()

        # Filter by status
        status_param = request.query_params.get('status')
        if status_param and status_param != 'all':
            queryset = queryset.filter(status=status_param)

        # Filter by airline
        airline_param = request.query_params.get('airline')
        if airline_param and airline_param != 'all':
            queryset = queryset.filter(airline__iexact=airline_param)

        # Search query
        search_param = request.query_params.get('search')
        if search_param:
            q = search_param.strip()
            queryset = queryset.filter(
                Q(flight_number__icontains=q) |
                Q(from_city__icontains=q) |
                Q(from_code__icontains=q) |
                Q(to_city__icontains=q) |
                Q(to_code__icontains=q) |
                Q(airline__icontains=q) |
                Q(aircraft__icontains=q)
            )

        # Ordering
        ordering = request.query_params.get('ordering', 'time')
        if ordering == 'airline':
            queryset = queryset.order_by('airline')
        else:
            queryset = queryset.order_by('departure_time')

        serializer = FlightSerializer(queryset, many=True)
        return Response(serializer.data)


class FlightDetailAPIView(APIView):
    """
    Returns single flight by slug ID.
    """
    def get(self, request, flight_id):
        update_dynamic_flight_lifecycle()
        try:
            flight = Flight.objects.get(flight_id=flight_id)
            serializer = FlightSerializer(flight)
            return Response(serializer.data)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)


class AirportListAPIView(APIView):
    """
    Returns list of hubs and airports with live calculated departures and arrivals.
    """
    def get(self, request):
        if not Airport.objects.exists():
            seed_initial_database()

        airports = Airport.objects.all()
        # Always ensure departure and arrival counts strictly match actual flights in DB
        for apt in airports:
            dep_count = Flight.objects.filter(from_code=apt.code).count()
            arr_count = Flight.objects.filter(to_code=apt.code).count()
            if apt.departures_count != dep_count or apt.arrivals_count != arr_count:
                apt.departures_count = dep_count
                apt.arrivals_count = arr_count
                apt.save(update_fields=['departures_count', 'arrivals_count'])

        serializer = AirportSerializer(airports, many=True)
        return Response(serializer.data)


class SyncAviationstackAPIView(APIView):
    """
    Fetches real-time flight data from Aviationstack API and updates SQLite database.
    """
    def post(self, request):
        limit = int(request.data.get('limit', 20))
        result = fetch_and_sync_aviationstack_flights(limit=limit)
        return Response(result)

    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        result = fetch_and_sync_aviationstack_flights(limit=limit)
        return Response(result)


class ApiStatusAPIView(APIView):
    """
    System status and statistics.
    """
    def get(self, request):
        return Response({
            'status': 'online',
            'service': 'Flight Information Service REST API',
            'version': '1.0.0',
            'flights_in_db': Flight.objects.count(),
            'airports_in_db': Airport.objects.count(),
            'aviationstack_integration': 'enabled',
        })


class CleanupArchivedFlightsAPIView(APIView):
    """
    Data retention & TTL maintenance:
    Deletes completed (landed or cancelled) flights older than the given days (default 14 days / 2 weeks).
    """
    def post(self, request):
        days = int(request.data.get('days', 14))
        deleted_count = cleanup_archived_flights(days_retention=days)
        return Response({
            'success': True,
            'message': f'Успешно очищено {deleted_count} завершённых рейсов старше {days} дней',
            'deleted_count': deleted_count,
            'remaining_flights': Flight.objects.count(),
        })

    def get(self, request):
        days = int(request.query_params.get('days', 14))
        deleted_count = cleanup_archived_flights(days_retention=days)
        return Response({
            'success': True,
            'message': f'Успешно очищено {deleted_count} завершённых рейсов старше {days} дней',
            'deleted_count': deleted_count,
            'remaining_flights': Flight.objects.count(),
        })


class NewsletterSubscribeAPIView(APIView):
    """
    Subscribes user to newsletter and sends authentic welcome confirmation email.
    """
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        if not email or '@' not in email or '.' not in email:
            return Response(
                {'success': False, 'error': 'Пожалуйста, укажите корректный адрес электронной почты.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()

        # Send welcome email via Yandex SMTP
        subject = 'Добро пожаловать в рассылку сервиса «Авиарейсы» ✈️'
        message = (
            f'Здравствуйте!\n\n'
            f'Благодарим вас за подписку на информационный сервис «Авиарейсы».\n\n'
            f'Теперь вы будете первыми узнавать:\n'
            f' • об оперативных изменениях в расписании и статусах рейсов;\n'
            f' • о задержках и метеоусловиях в ключевых аэропортах;\n'
            f' • о полезных советах и рекомендациях для комфортных перелётов.\n\n'
            f'Вы можете в любой момент изменить параметры уведомлений в личном кабинете на сайте.\n\n'
            f'---\n'
            f'С уважением,\n'
            f'Команда информационного сервиса «Авиарейсы»'
        )

        email_sent = False
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'Авиарейсы <noreply@aviaraces.ru>'),
                recipient_list=[email],
                fail_silently=False,
            )
            email_sent = True
            logger.info(f'Newsletter confirmation email sent to {email}')
        except Exception as e:
            logger.error(f'Failed to send newsletter email to {email}: {e}')

        return Response({
            'success': True,
            'message': 'Вы успешно подписались на рассылку! Проверьте вашу почту.',
            'email': email,
            'email_sent': email_sent,
            'is_new': created,
        }, status=status.HTTP_200_OK)
