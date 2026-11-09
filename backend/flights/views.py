from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Flight, Airport
from .serializers import FlightSerializer, AirportSerializer
from .services import fetch_and_sync_aviationstack_flights, seed_initial_database

class FlightListAPIView(APIView):
    """
    Returns filtered and searched list of flights.
    """
    def get(self, request):
        # Auto-seed if database is empty
        if not Flight.objects.exists():
            seed_initial_database()

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
        if ordering == 'price':
            queryset = queryset.order_by('price')
        else:
            queryset = queryset.order_by('departure_time')

        serializer = FlightSerializer(queryset, many=True)
        return Response(serializer.data)


class FlightDetailAPIView(APIView):
    """
    Returns single flight by slug ID.
    """
    def get(self, request, flight_id):
        try:
            flight = Flight.objects.get(flight_id=flight_id)
            serializer = FlightSerializer(flight)
            return Response(serializer.data)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)


class AirportListAPIView(APIView):
    """
    Returns list of hubs and airports.
    """
    def get(self, request):
        if not Airport.objects.exists():
            seed_initial_database()

        airports = Airport.objects.all()
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
