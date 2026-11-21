import requests
import datetime
from django.conf import settings
from .models import Flight, Airport

def fetch_and_sync_aviationstack_flights(limit=25):
    """
    Fetches real-time flight data from Aviationstack API and synchronizes into SQLite.
    Protects user's monthly rate limits by caching into local database.
    """
    api_key = settings.AVIATIONSTACK_API_KEY
    base_url = settings.AVIATIONSTACK_BASE_URL
    url = f"{base_url}/flights?access_key={api_key}&limit={limit}"

    try:
        response = requests.get(url, timeout=12)
        response.raise_for_status()
        json_data = response.json()
        raw_flights = json_data.get('data', [])

        saved_count = 0
        for item in raw_flights:
            flight_info = item.get('flight') or {}
            dep_info = item.get('departure') or {}
            arr_info = item.get('arrival') or {}
            airline_info = item.get('airline') or {}
            aircraft_info = item.get('aircraft') or {}
            live_info = item.get('live') or {}

            iata = flight_info.get('iata') or f"FL-{flight_info.get('number', '000')}"
            flight_number = flight_info.get('iata') or flight_info.get('number') or "Рейс"
            airline_name = airline_info.get('name') or "Международные авиалинии"

            # Parse times
            dep_sched = dep_info.get('scheduled')
            arr_sched = arr_info.get('scheduled')
            dep_time = "12:00"
            dep_date = datetime.date.today().isoformat()
            if dep_sched:
                try:
                    dt = datetime.datetime.fromisoformat(dep_sched.replace('Z', '+00:00'))
                    dep_time = dt.strftime('%H:%M')
                    dep_date = dt.strftime('%Y-%m-%d')
                except Exception:
                    pass

            arr_time = "15:30"
            if arr_sched:
                try:
                    dt = datetime.datetime.fromisoformat(arr_sched.replace('Z', '+00:00'))
                    arr_time = dt.strftime('%H:%M')
                except Exception:
                    pass

            # Map Aviationstack status to our system status
            raw_status = (item.get('flight_status') or 'scheduled').lower()
            if raw_status in ['active', 'in_air', 'en-route']:
                status = 'in_air'
                status_text = 'В полёте'
            elif raw_status in ['landed', 'arrived']:
                status = 'landed'
                status_text = f"Прибыл в {arr_time}"
            elif raw_status in ['incident', 'diverted', 'delayed']:
                status = 'delayed'
                status_text = f"Задержан"
            elif raw_status == 'cancelled':
                status = 'cancelled'
                status_text = 'Рейс отменён'
            else:
                status = 'scheduled'
                status_text = 'По расписанию'

            # Telemetry
            altitude = 10400 if status == 'in_air' else 0
            speed = 860 if status == 'in_air' else 0
            if live_info:
                if live_info.get('altitude'):
                    altitude = int(live_info.get('altitude'))
                if live_info.get('speed_horizontal'):
                    speed = int(live_info.get('speed_horizontal'))

            slug_id = (flight_number.lower().replace(' ', '-') + f"-{dep_info.get('iata', 'apt').lower()}").strip('-')

            # Skip invalid / empty flight records
            if not flight_number or flight_number.lower() in ['рейс', 'none', 'null', 'flight']:
                continue
            if not airline_name or airline_name.lower() in ['empty', 'none', 'null']:
                continue

            from_c = dep_info.get('iata') or 'SVO'
            to_c = arr_info.get('iata') or 'DXB'

            # Deduplicate codeshare flights (same route and same departure time)
            existing_dup = Flight.objects.filter(
                from_code=from_c,
                to_code=to_c,
                departure_time=dep_time,
                departure_date=dep_date
            ).exclude(flight_id=slug_id).first()
            if existing_dup:
                continue

            # Calculate dynamic duration
            diff_m = 160
            try:
                dh, dm = map(int, dep_time.split(':'))
                ah, am = map(int, arr_time.split(':'))
                diff_m = (ah * 60 + am) - (dh * 60 + dm)
                if diff_m < 0:
                    diff_m += 24 * 60
                dur_h = diff_m // 60
                dur_m = diff_m % 60
                duration = f"{dur_h} ч {dur_m:02d} мин" if dur_m else f"{dur_h} ч"
            except Exception:
                duration = "2 ч 40 мин"

            # Diverse aircraft model
            if aircraft_info and aircraft_info.get('iata'):
                aircraft = aircraft_info.get('iata')
            else:
                last_digit = int(flight_number[-1]) if flight_number[-1].isdigit() else 0
                if diff_m >= 360:
                    aircraft = 'Boeing 777-300ER' if last_digit % 2 == 0 else 'Airbus A350-900'
                elif diff_m >= 180:
                    aircraft = 'Airbus A321neo' if last_digit % 2 == 0 else 'Boeing 737-800'
                else:
                    aircraft = 'Airbus A320neo' if last_digit % 2 == 0 else 'Sukhoi Superjet 100'

            Flight.objects.update_or_create(
                flight_id=slug_id,
                defaults={
                    'flight_number': flight_number,
                    'airline': airline_name,
                    'aircraft': aircraft,
                    'from_code': from_c,
                    'from_name': dep_info.get('airport') or 'Аэропорт вылета',
                    'from_city': dep_info.get('airport', '').split(' ')[0] or 'Москва',
                    'from_terminal': dep_info.get('terminal'),
                    'from_gate': dep_info.get('gate'),
                    'to_code': to_c,
                    'to_name': arr_info.get('airport') or 'Аэропорт прилёта',
                    'to_city': arr_info.get('airport', '').split(' ')[0] or 'Дубай',
                    'to_terminal': arr_info.get('terminal'),
                    'to_gate': arr_info.get('gate'),
                    'departure_time': dep_time,
                    'arrival_time': arr_time,
                    'departure_date': dep_date,
                    'duration': duration,
                    'status': status,
                    'status_text': status_text,
                    'altitude': altitude,
                    'speed': speed,
                    'is_real_api': True,
                }
            )
            saved_count += 1

        return {
            'success': True,
            'message': f'Успешно синхронизировано {saved_count} реальных авиарейсов из Aviationstack API',
            'count': saved_count,
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
        }

def cleanup_archived_flights(days_retention=14):
    """
    Automatic Data Retention Policy (TTL cleanup):
    Deletes finished flights ('landed' or 'cancelled') that are older
    than `days_retention` days (default 14 days / 2 weeks).
    Protects database storage and keeps flight lists clean and relevant.
    """
    cutoff_date = datetime.date.today() - datetime.timedelta(days=days_retention)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')
    cutoff_datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_retention)

    # 1. Direct ORM delete for matching ISO departure dates
    deleted_count, _ = Flight.objects.filter(
        status__in=['landed', 'cancelled'],
        departure_date__lt=cutoff_str
    ).delete()

    # 2. Safety pass for any flights with non-standard date formats or updated_at
    remaining_finished = Flight.objects.filter(status__in=['landed', 'cancelled'])
    additional_deleted = 0
    for fl in remaining_finished:
        should_delete = False
        if fl.departure_date:
            try:
                fl_date = datetime.date.fromisoformat(fl.departure_date.strip()[:10])
                if fl_date < cutoff_date:
                    should_delete = True
            except Exception:
                pass
        if not should_delete and fl.updated_at:
            if fl.updated_at < cutoff_datetime:
                should_delete = True
        if should_delete:
            fl.delete()
            additional_deleted += 1

    return deleted_count + additional_deleted


def update_dynamic_flight_lifecycle():
    """
    Dynamically recalculates flight statuses and updates today's dates
    based on the current clock time so that the flight board always feels
    alive, active, and realistic 24/7.
    Also automatically runs cleanup for completed flights older than 14 days.
    """
    # 1. Automatic cleanup of finished flights older than 14 days (TTL)
    cleanup_archived_flights(days_retention=14)

    now = datetime.datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    current_minutes = now.hour * 60 + now.minute

    flights = Flight.objects.all()
    for flight in flights:
        changed = False

        # If flight is historical (departure_date < today) and finished (landed or cancelled),
        # keep it as a historical record until it expires via retention policy (14 days).
        if flight.departure_date and flight.departure_date < today_str and flight.status in ['landed', 'cancelled']:
            continue

        # Keep dates fresh to current date for today's active flights or flights missing date
        if not flight.departure_date or flight.departure_date == today_str:
            if flight.departure_date != today_str:
                flight.departure_date = today_str
                changed = True
        else:
            # If flight had an outdated non-completed status, update date to today to keep alive
            flight.departure_date = today_str
            changed = True

        # Parse departure and arrival time
        try:
            dep_h, dep_m = map(int, flight.departure_time.split(':'))
            arr_h, arr_m = map(int, flight.arrival_time.split(':'))
            dep_min = dep_h * 60 + dep_m
            arr_min = arr_h * 60 + arr_m

            # If arrival wraps past midnight (e.g. 23:30 to 02:15)
            if arr_min < dep_min:
                arr_min += 24 * 60

            # If flight is explicitly marked delayed
            if flight.status == 'delayed' or 'задержан' in flight.status_text.lower():
                flight.altitude = 0
                flight.speed = 0
                if changed:
                    flight.save()
                continue

            # Calculate dynamic status
            # 1) If current time < departure time
            if current_minutes < dep_min:
                diff_to_dep = dep_min - current_minutes
                if diff_to_dep <= 45:
                    flight.status = 'boarding'
                    flight.status_text = 'Посадка на борт'
                    flight.altitude = 0
                    flight.speed = 0
                else:
                    flight.status = 'scheduled'
                    flight.status_text = 'По расписанию'
                    flight.altitude = 0
                    flight.speed = 0
                changed = True
            # 2) If in the air (between departure and arrival)
            elif dep_min <= current_minutes < arr_min:
                flight.status = 'in_air'
                flight.status_text = 'В полёте'
                flight.altitude = 10400
                flight.speed = 870
                changed = True
            # 3) If landed
            else:
                flight.status = 'landed'
                flight.status_text = f'Прибыл в {flight.arrival_time}'
                flight.altitude = 0
                flight.speed = 0
                changed = True

        except Exception:
            pass

        if changed:
            flight.save()


def seed_initial_database():
    """
    Populates SQLite database with initial authentic flights and airports
    so the system is immediately fully operational.
    """
    today_str = datetime.date.today().isoformat()
    initial_airports = [
        {'code': 'SVO', 'name': 'Шереметьево имени А. С. Пушкина', 'city': 'Москва', 'country': 'Россия', 'departures_count': 142, 'arrivals_count': 138, 'timezone': 'UTC+3'},
        {'code': 'DME', 'name': 'Домодедово имени М. В. Ломоносова', 'city': 'Москва', 'country': 'Россия', 'departures_count': 98, 'arrivals_count': 95, 'timezone': 'UTC+3'},
        {'code': 'VKO', 'name': 'Внуково имени А. Н. Туполева', 'city': 'Москва', 'country': 'Россия', 'departures_count': 64, 'arrivals_count': 61, 'timezone': 'UTC+3'},
        {'code': 'LED', 'name': 'Пулково', 'city': 'Санкт-Петербург', 'country': 'Россия', 'departures_count': 88, 'arrivals_count': 84, 'timezone': 'UTC+3'},
        {'code': 'AER', 'name': 'Международный аэропорт Сочи', 'city': 'Сочи', 'country': 'Россия', 'departures_count': 76, 'arrivals_count': 72, 'timezone': 'UTC+3'},
        {'code': 'KZN', 'name': 'Международный аэропорт Казань', 'city': 'Казань', 'country': 'Россия', 'departures_count': 45, 'arrivals_count': 42, 'timezone': 'UTC+3'},
        {'code': 'DXB', 'name': 'Международный аэропорт Дубай', 'city': 'Дубай', 'country': 'ОАЭ', 'departures_count': 310, 'arrivals_count': 305, 'timezone': 'UTC+4'},
        {'code': 'IST', 'name': 'Новый аэропорт Стамбула', 'city': 'Стамбул', 'country': 'Турция', 'departures_count': 260, 'arrivals_count': 254, 'timezone': 'UTC+3'},
        {'code': 'DOH', 'name': 'Международный аэропорт Хамад', 'city': 'Доха', 'country': 'Катар', 'departures_count': 185, 'arrivals_count': 180, 'timezone': 'UTC+3'},
    ]
    for apt in initial_airports:
        Airport.objects.get_or_create(code=apt['code'], defaults=apt)

    from .seed_diverse_data import get_diverse_flights_data
    for fl in get_diverse_flights_data():
        Flight.objects.get_or_create(flight_id=fl['flight_id'], defaults=fl)

