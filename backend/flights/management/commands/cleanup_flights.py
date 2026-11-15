from django.core.management.base import BaseCommand
from flights.services import cleanup_archived_flights

class Command(BaseCommand):
    help = 'Cleans up completed (landed/cancelled) flights older than the specified retention days (default: 14 days)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=14,
            help='Retention period in days (default: 14)',
        )

    def handle(self, *args, **options):
        days = options['days']
        count = cleanup_archived_flights(days_retention=days)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} completed flight(s) older than {days} days.')
        )
