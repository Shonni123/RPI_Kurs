from django.urls import path
from .views import (
    FlightListAPIView,
    FlightDetailAPIView,
    AirportListAPIView,
    SyncAviationstackAPIView,
    ApiStatusAPIView,
)

urlpatterns = [
    path('flights/', FlightListAPIView.as_view(), name='flight-list'),
    path('flights/<str:flight_id>/', FlightDetailAPIView.as_view(), name='flight-detail'),
    path('airports/', AirportListAPIView.as_view(), name='airport-list'),
    path('sync-aviationstack/', SyncAviationstackAPIView.as_view(), name='sync-aviationstack'),
    path('status/', ApiStatusAPIView.as_view(), name='api-status'),
]
