from django.db import models

class Flight(models.Model):
    STATUS_CHOICES = [
        ('in_air', 'В полёте'),
        ('scheduled', 'По расписанию / Ожидает взлёта'),
        ('delayed', 'Задержан'),
        ('landed', 'Прибыл'),
        ('boarding', 'Посадка'),
        ('cancelled', 'Отменён'),
    ]

    flight_id = models.CharField(max_length=50, unique=True, verbose_name="ID рейса (slug)")
    flight_number = models.CharField(max_length=30, verbose_name="Номер рейса")
    airline = models.CharField(max_length=100, verbose_name="Авиакомпания")
    aircraft = models.CharField(max_length=100, default="Airbus A320", verbose_name="Модель воздушного судна")

    # Вылет
    from_code = models.CharField(max_length=10, verbose_name="Код аэропорта вылета (IATA)")
    from_name = models.CharField(max_length=150, verbose_name="Название аэропорта вылета")
    from_city = models.CharField(max_length=100, verbose_name="Город вылета")
    from_terminal = models.CharField(max_length=20, blank=True, null=True, verbose_name="Терминал вылета")
    from_gate = models.CharField(max_length=20, blank=True, null=True, verbose_name="Гейт вылета")

    # Прилёт
    to_code = models.CharField(max_length=10, verbose_name="Код аэропорта прилёта (IATA)")
    to_name = models.CharField(max_length=150, verbose_name="Название аэропорта прилёта")
    to_city = models.CharField(max_length=100, verbose_name="Город прилёта")
    to_terminal = models.CharField(max_length=20, blank=True, null=True, verbose_name="Терминал прилёта")
    to_gate = models.CharField(max_length=20, blank=True, null=True, verbose_name="Гейт прилёта")

    # Время и статус
    departure_time = models.CharField(max_length=20, verbose_name="Время вылета (ЧЧ:ММ)")
    arrival_time = models.CharField(max_length=20, verbose_name="Время прилёта (ЧЧ:ММ)")
    departure_date = models.CharField(max_length=20, verbose_name="Дата вылета")
    duration = models.CharField(max_length=50, default="2 ч 30 мин", verbose_name="Время в пути")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='scheduled', verbose_name="Код статуса")
    status_text = models.CharField(max_length=100, default='По расписанию', verbose_name="Текст статуса")

    # Телеметрия и цена
    altitude = models.IntegerField(default=0, verbose_name="Высота (м)")
    speed = models.IntegerField(default=0, verbose_name="Скорость (км/ч)")
    price = models.IntegerField(default=0, verbose_name="Цена билета (руб)")

    is_real_api = models.BooleanField(default=False, verbose_name="Загружено из реального API Aviationstack")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Авиарейс"
        verbose_name_plural = "Авиарейсы"
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.flight_number} ({self.from_code} -> {self.to_code}) - {self.status_text}"


class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Код IATA")
    name = models.CharField(max_length=150, verbose_name="Название аэропорта")
    city = models.CharField(max_length=100, verbose_name="Город")
    country = models.CharField(max_length=100, verbose_name="Страна")
    departures_count = models.IntegerField(default=0, verbose_name="Число вылетов")
    arrivals_count = models.IntegerField(default=0, verbose_name="Число прилётов")
    timezone = models.CharField(max_length=50, default="UTC+3", verbose_name="Часовой пояс")

    class Meta:
        verbose_name = "Аэропорт"
        verbose_name_plural = "Аэропорты"
        ordering = ['city']

    def __str__(self):
        return f"{self.code} - {self.name} ({self.city})"
