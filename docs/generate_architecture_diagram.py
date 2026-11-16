import os
from PIL import Image, ImageDraw, ImageFont

def generate_architecture_diagram_png(output_path='docs/project_architecture.png'):
    scale = 2
    w, h = 1650 * scale, 1020 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    font_path = 'C:/Windows/Fonts/arial.ttf'
    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'

    font_tier_title = ImageFont.truetype(font_bold_path, 13 * scale)
    font_box_title = ImageFont.truetype(font_bold_path, 11 * scale)
    font_box_text = ImageFont.truetype(font_path, 9.5 * scale)
    font_sub = ImageFont.truetype(font_path, 9 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 9.5 * scale)

    def S(val):
        return int(val * scale)

    # Helper: draw tier card
    def draw_tier(x, y, tw, th, title, bg='#FAFBFD', border='#94A3B8'):
        draw.rectangle([S(x), S(y), S(x + tw), S(y + th)], fill=bg, outline=border, width=S(1.4))
        # Title bar
        draw.rectangle([S(x), S(y), S(x + tw), S(y + 36)], fill='#FFFFFF', outline=border, width=S(1.4))
        draw.text((S(x + 18), S(y + 9)), title, font=font_tier_title, fill='#0F172A')

    # Helper: draw component box
    def draw_box(x, y, bw, bh, title, items=[], bg='#FFFFFF', border='#334155'):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill=bg, outline=border, width=S(1.2))
        draw.rectangle([S(x), S(y), S(x + bw), S(y + 26)], fill='#F1F5F9', outline=border, width=S(1.2))
        draw.text((S(x + 10), S(y + 5)), title, font=font_box_title, fill='#0F172A')
        cur_y = y + 33
        for item in items:
            draw.text((S(x + 10), S(cur_y)), item, font=font_box_text, fill='#334155')
            cur_y += 18

    # Helper: draw connecting vertical arrow
    def draw_vert_arrow(x, y1, y2, label=None, label_side='right', color='#1E3A8A'):
        draw.line([S(x), S(y1), S(x), S(y2)], fill=color, width=S(1.6))
        # Arrowhead at end
        asize = S(6)
        if y2 > y1:
            draw.polygon([(S(x), S(y2)), (S(x - 4), S(y2 - asize)), (S(x + 4), S(y2 - asize))], fill=color)
        else:
            draw.polygon([(S(x), S(y2)), (S(x - 4), S(y2 + asize)), (S(x + 4), S(y2 + asize))], fill=color)
        
        # Dual arrow head at start if bidirectional
        draw.polygon([(S(x), S(y1)), (S(x - 4), S(y1 + asize if y2 > y1 else y1 - asize)), (S(x + 4), S(y1 + asize if y2 > y1 else y1 - asize))], fill=color)

        if label:
            tb = font_arrow.getbbox(label)
            tw = tb[2] - tb[0]
            mid_y = (y1 + y2) / 2 - 8
            if label_side == 'right':
                draw.text((S(x + 12), S(mid_y)), label, font=font_arrow, fill=color)
            else:
                draw.text((S(x - 12 - tw/scale), S(mid_y)), label, font=font_arrow, fill=color)

    # ================= 1. КЛИЕНТСКИЙ УРОВЕНЬ (FRONTEND SPA) =================
    draw_tier(40, 30, 1570, 210, "1. Клиентский уровень (Frontend — React 19 Single Page Application)", '#F8FAFC', '#64748B')

    draw_box(65, 80, 340, 140, "Интерфейс и страницы (Pages)", [
        "• Landing (Hero, Features, Stats, FAQ)",
        "• Flights (Табло рейсов, живой поиск)",
        "• FlightDetail (/flights/:id, телеметрия)",
        "• Airports (Каталог хабов), Favorites",
        "• NotFound (404 авиационный экран)",
    ], '#FFFFFF', '#475569')

    draw_box(435, 80, 340, 140, "Компонентный уровень (UI Layer)", [
        "• FlightCard (Карточка рейса, бейджи)",
        "• Filters (Капсулы статусов, авиакомпании)",
        "• SearchBar (Быстрый поиск, автоочистка)",
        "• LoadingSkeleton (Мерцающий скелетон)",
        "• Drawer (Боковая навигация), Modal",
    ], '#FFFFFF', '#475569')

    draw_box(805, 80, 340, 140, "Управление состоянием и роутинг", [
        "• React Router v7 (SPA маршрутизация)",
        "• AuthContext (Сессия, статус верификации)",
        "• FavoritesContext (Список избранного)",
        "• LocalStorage API (Офлайн-сохранение)",
        "• useMemo / useCallback (Оптимизация 60 FPS)",
    ], '#FFFFFF', '#475569')

    draw_box(1175, 80, 410, 140, "Сервисный слой данных (Services)", [
        "• src/services/api.ts (Клиент API)",
        "• Axios / Fetch (Асинхронные HTTP запросы)",
        "• Interceptors (Обработка ошибок, CORS)",
        "• Mock Data Cache (Автономный fallback)",
        "• Преобразование camelCase <-> snake_case",
    ], '#EFF6FF', '#2563EB')

    # ================= 2. СЕТЕВОЙ УРОВЕНЬ И ПРОКСИ (GATEWAY) =================
    draw_tier(40, 280, 1570, 120, "2. Сетевой уровень и веб-сервер (Gateway & Web Server)", '#F0FDF4', '#16A34A')

    draw_box(65, 325, 460, 60, "Nginx (Static Web Server)", [
        "• Раздача сборки фронтенда (HTML, JS, CSS, шрифты)",
        "• Сжатие Gzip / Brotli, кэширование статики",
    ], '#FFFFFF', '#16A34A')

    draw_box(555, 325, 500, 60, "Nginx (Reverse Proxy & Security)", [
        "• Проксирование /api/* на бэкенд Gunicorn/Django",
        "• SSL/TLS Termination (HTTPS), CORS-политики",
    ], '#FFFFFF', '#16A34A')

    draw_box(1085, 325, 500, 60, "WSGI / Gunicorn (Application Server)", [
        "• WSGI-контейнер для запуска Python/Django",
        "• Пул рабочих процессов (Workers), обработка запросов",
    ], '#FFFFFF', '#16A34A')

    # Стрелки между Frontend и Nginx
    draw_vert_arrow(295, 240, 280, "HTTP 200 (Статика)", 'right', '#16A34A')
    draw_vert_arrow(1380, 240, 280, "REST API (JSON / HTTP)", 'right', '#1E3A8A')

    # ================= 3. СЕРВЕРНЫЙ УРОВЕНЬ (BACKEND — DJANGO 5 & DRF) =================
    draw_tier(40, 440, 1570, 260, "3. Серверный уровень (Backend — Django 5 & Django REST Framework)", '#FAF5FF', '#9333EA')

    draw_box(65, 490, 340, 190, "URL-маршрутизация и безопасность", [
        "• urls.py + DefaultRouter (DRF)",
        "• /api/flights/, /api/airports/",
        "• /api/auth/ (register, login, verify)",
        "• Security Middleware, CORS Headers",
        "• PBKDF2 Password Hashing (SHA256)",
        "• Token / Session Authentication",
    ], '#FFFFFF', '#7C3AED')

    draw_box(435, 490, 360, 190, "Контроллеры API (ViewSets)", [
        "• FlightViewSet (Выборка, фильтры, поиск)",
        "• AirportViewSet (Список узловых хабов)",
        "• AuthViewSet (Регистрация, 2FA вход)",
        "• Обработка параметров: search, airline,",
        "  status, ordering (цена / вылет)",
        "• Валидация входных данных (DTO)",
    ], '#FFFFFF', '#7C3AED')

    draw_box(825, 490, 350, 190, "Сериализаторы (DRF Serializers)", [
        "• FlightSerializer (Преобразование моделей)",
        "• AirportSerializer (IATA, города, страны)",
        "• UserProfileSerializer (Email, телефон)",
        "• EmailVerificationCodeSerializer",
        "• Форматирование реляционных связей",
        "• Преобразование типов и валидаторы",
    ], '#FFFFFF', '#7C3AED')

    draw_box(1205, 490, 380, 190, "Фоновые сервисы и бизнес-логика", [
        "• Flight Lifecycle Engine (Симуляция 24/7)",
        "• Актуализация статусов по часам:",
        "  scheduled -> boarding -> in_air -> landed",
        "• TTL Cleaner: удаление рейсов старше 14 дн.",
        "• EmailVerification: генерация 6-значных кодов",
        "• Cron / Background Tasks Демон",
    ], '#FFFDF0', '#D97706')

    # Стрелка между Nginx и Backend
    draw_vert_arrow(805, 400, 440, "WSGI Вызовы", 'right', '#7C3AED')

    # ================= 4. СЛОЙ ДАННЫХ И ИНТЕГРАЦИЙ =================
    draw_tier(40, 740, 1570, 250, "4. Слой доступа к данным, СУБД и внешние интеграции", '#FFFBEB', '#D97706')

    draw_box(65, 790, 380, 180, "Django ORM (Object-Relational Mapping)", [
        "• Абстракция базы данных и миграции",
        "• QuerySet API (ленивая загрузка, кэш)",
        "• Транзакции атомарности (atomic)",
        "• Реляционные связи: 1:1, 1:N",
        "• Автоматическая генерация SQL-запросов",
        "• Модели: Flight, Airport, User, Code",
    ], '#FFFFFF', '#B45309')

    draw_box(475, 790, 400, 180, "СУБД SQLite 3 (Реляционная база данных)", [
        "• flights_flight (Рейсы, терминалы, статус, цена)",
        "• flights_airport (Хабы, IATA коды, координаты)",
        "• auth_user (Учетные записи, хэши паролей)",
        "• accounts_userprofile (is_email_verified)",
        "• accounts_emailverificationcode (TTL 15м)",
        "• Индексы: IATA code, flight_number, status",
    ], '#F1F5F9', '#334155')

    draw_box(905, 790, 330, 180, "Яндекс SMTP (Почтовый шлюз)", [
        "• Сервер: smtp.yandex.ru",
        "• Защищенный протокол: SSL / TLS",
        "• Сетевой порт: 465 (SSL)",
        "• Отправка 6-значных кодов 2FA",
        "• Гарантированная доставка писем",
        "• Обработка ошибок SMTP соединений",
    ], '#FFFFFF', '#DC2626')

    draw_box(1265, 790, 320, 180, "Aviationstack API (Внешний шлюз)", [
        "• Внешний поставщик реальных авиаданных",
        "• REST API (JSON over HTTPS)",
        "• Расписания рейсов и фактические задержки",
        "• Первоначальное наполнение базы данных",
        "• Квотирование и защита от сбоев API",
        "• Фоновые sync-команды Django",
    ], '#FFFFFF', '#0284C7')

    # Стрелки между Backend и Data / External
    draw_vert_arrow(255, 700, 740, "QuerySet / ORM API", 'left', '#B45309')
    draw_vert_arrow(1070, 700, 740, "SMTP SSL (465)", 'left', '#DC2626')
    draw_vert_arrow(1425, 700, 740, "Aviationstack HTTPS", 'right', '#0284C7')

    # Горизонтальная стрелка между ORM и SQLite
    draw.line([S(445), S(880), S(475), S(880)], fill='#B45309', width=S(1.6))
    draw.polygon([(S(475), S(880)), (S(467), S(876)), (S(467), S(884))], fill='#B45309')
    draw.polygon([(S(445), S(880)), (S(453), S(876)), (S(453), S(884))], fill='#B45309')
    draw.text((S(446), S(860)), "SQL", font=font_arrow, fill='#B45309')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"Project Architecture diagram PNG generated: {output_path}")

if __name__ == '__main__':
    generate_architecture_diagram_png()
