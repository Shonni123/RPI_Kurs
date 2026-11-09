from rest_framework import serializers
from .models import Flight, Airport

class FlightSerializer(serializers.ModelSerializer):
    # Map model fields to React TypeScript camelCase interface
    id = serializers.CharField(source='flight_id')
    flightNumber = serializers.CharField(source='flight_number')
    departureTime = serializers.CharField(source='departure_time')
    arrivalTime = serializers.CharField(source='arrival_time')
    departureDate = serializers.CharField(source='departure_date')
    statusText = serializers.CharField(source='status_text')
    isRealApi = serializers.BooleanField(source='is_real_api')

    from_location = serializers.SerializerMethodField(method_name='get_from')
    to_location = serializers.SerializerMethodField(method_name='get_to')

    class Meta:
        model = Flight
        fields = [
            'id',
            'flightNumber',
            'airline',
            'aircraft',
            'from_location',
            'to_location',
            'departureTime',
            'arrivalTime',
            'departureDate',
            'duration',
            'status',
            'statusText',
            'altitude',
            'speed',
            'price',
            'isRealApi',
        ]

    def get_from(self, obj):
        return {
            'code': obj.from_code,
            'name': obj.from_name,
            'city': obj.from_city,
            'terminal': obj.from_terminal,
            'gate': obj.from_gate,
        }

    def get_to(self, obj):
        return {
            'code': obj.to_code,
            'name': obj.to_name,
            'city': obj.to_city,
            'terminal': obj.to_terminal,
            'gate': obj.to_gate,
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Rename from_location and to_location to 'from' and 'to'
        representation['from'] = representation.pop('from_location')
        representation['to'] = representation.pop('to_location')
        return representation


class AirportSerializer(serializers.ModelSerializer):
    departuresCount = serializers.IntegerField(source='departures_count')
    arrivalsCount = serializers.IntegerField(source='arrivals_count')

    class Meta:
        model = Airport
        fields = [
            'code',
            'name',
            'city',
            'country',
            'departuresCount',
            'arrivalsCount',
            'timezone',
        ]
