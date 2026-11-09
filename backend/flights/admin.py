from django.contrib import admin
from .models import Flight, Airport

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'from_code', 'to_code', 'departure_time', 'arrival_time', 'status', 'is_real_api')
    list_filter = ('status', 'airline', 'is_real_api', 'from_code', 'to_code')
    search_fields = ('flight_number', 'airline', 'from_city', 'to_city', 'from_code', 'to_code')

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country', 'departures_count', 'arrivals_count', 'timezone')
    search_fields = ('code', 'name', 'city', 'country')
