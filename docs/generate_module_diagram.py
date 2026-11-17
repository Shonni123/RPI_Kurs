import os
from PIL import Image, ImageDraw, ImageFont

def generate_module_diagram_png(output_path='docs/module_diagram.png'):
    scale = 2
    w, h = 1800 * scale, 1140 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    font_path = 'C:/Windows/Fonts/arial.ttf'
    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'

    font_subsystem = ImageFont.truetype(font_bold_path, 13 * scale)
    font_pkg_title = ImageFont.truetype(font_bold_path, 11 * scale)
    font_text_bold = ImageFont.truetype(font_bold_path, 9.5 * scale)
    font_text = ImageFont.truetype(font_path, 9.5 * scale)
    font_tag = ImageFont.truetype(font_bold_path, 8.5 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 9 * scale)

    def S(val):
        return int(val * scale)

    # Helper: Draw Subsystem container
    def draw_subsystem(x, y, sw, sh, title, bg='#FAFBFD', border='#64748B'):
        draw.rectangle([S(x), S(y), S(x + sw), S(y + sh)], fill=bg, outline=border, width=S(1.5))
        draw.rectangle([S(x), S(y), S(x + sw), S(y + 36)], fill='#FFFFFF', outline=border, width=S(1.5))
        draw.text((S(x + 18), S(y + 9)), title, font=font_subsystem, fill='#0F172A')

    # Helper: Draw UML Component card
    def draw_component(x, y, cw, ch, title, stereotype="«component»", items=[], bg='#FFFFFF', border='#334155'):
        # Body
        draw.rectangle([S(x), S(y), S(x + cw), S(y + ch)], fill=bg, outline=border, width=S(1.2))
        
        # Header
        draw.rectangle([S(x), S(y), S(x + cw), S(y + 38)], fill='#F1F5F9', outline=border, width=S(1.2))
        
        # UML Component icon on right of header
        ix = x + cw - 24
        iy = y + 8
        draw.rectangle([S(ix), S(iy), S(ix + 16), S(iy + 20)], fill='#FFFFFF', outline='#475569', width=S(1))
        draw.rectangle([S(ix - 4), S(iy + 3), S(ix + 4), S(iy + 8)], fill='#FFFFFF', outline='#475569', width=S(1))
        draw.rectangle([S(ix - 4), S(iy + 11), S(ix + 4), S(iy + 16)], fill='#FFFFFF', outline='#475569', width=S(1))

        # Title & Stereotype
        draw.text((S(x + 10), S(y + 4)), stereotype, font=font_tag, fill='#64748B')
        draw.text((S(x + 10), S(y + 18)), title, font=font_pkg_title, fill='#0F172A')

        # Items
        cur_y = y + 46
        for item in items:
            if item.startswith("• "):
                draw.text((S(x + 10), S(cur_y)), item, font=font_text, fill='#334155')
            elif item.startswith("  - "):
                draw.text((S(x + 20), S(cur_y)), item, font=font_text, fill='#475569')
            elif item.startswith(" [") or item.startswith("API:"):
                draw.text((S(x + 10), S(cur_y)), item, font=font_text_bold, fill='#1E3A8A')
            else:
                draw.text((S(x + 10), S(cur_y)), item, font=font_text, fill='#334155')
            cur_y += 18

    # Helper: draw connecting line with label
    def draw_connector(p1, p2, label=None, label_pos=None, is_dashed=False, color='#1E3A8A'):
        if is_dashed:
            # dashed line
            step = 6
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                steps = int(dist / step)
                for i in range(0, steps, 2):
                    t1 = i / steps
                    t2 = min((i + 1) / steps, 1.0)
                    draw.line([S(p1[0] + dx*t1), S(p1[1] + dy*t1), S(p1[0] + dx*t2), S(p1[1] + dy*t2)], fill=color, width=S(1.3))
        else:
            draw.line([S(p1[0]), S(p1[1]), S(p2[0]), S(p2[1])], fill=color, width=S(1.5))

        # Arrowhead at p2
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            ux, uy = dx/dist, dy/dist
            nx, ny = -uy, ux
            tip = (S(p2[0]), S(p2[1]))
            asize = S(5.5)
            p_left = (tip[0] - asize*ux + asize*0.5*nx, tip[1] - asize*uy + asize*0.5*ny)
            p_right = (tip[0] - asize*ux - asize*0.5*nx, tip[1] - asize*uy - asize*0.5*ny)
            draw.polygon([tip, p_left, p_right], fill=color)

        if label:
            lx, ly = label_pos if label_pos else ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2 - 12)
            draw.text((S(lx), S(ly)), label, font=font_arrow, fill=color)

    # ================= 1. ПОДСИСТЕМА FRONTEND (REACT 19 SPA) =================
    draw_subsystem(30, 30, 750, 1070, "Подсистема клиентской части (Frontend Subsystem — React 19)", '#F8FAFC', '#2563EB')

    # Компонент 1.1: Pages Module
    draw_component(50, 80, 340, 440, "Модуль страниц (Pages)", "«module: pages»", [
        "Интерфейсы пользовательских экранов:",
        "• HomePage.tsx (Лендинг, Hero, FAQ)",
        "• FlightsPage.tsx (Табло рейсов)",
        "• FlightDetailPage.tsx (/flights/:id)",
        "• AirportsPage.tsx (Каталог хабов)",
        "• FavoritesPage.tsx (Избранные рейсы)",
        "• UserProfilePage.tsx (Личный кабинет)",
        "• AboutPage.tsx (О сервисе и стек)",
        "• NotFoundPage.tsx (404 Not Found)",
        "",
        "Взаимодействие:",
        "  - Запрашивает компоненты UI",
        "  - Подписывается на Auth/Favorites",
        "  - Инициирует запросы к сервисам",
    ], '#FFFFFF', '#3B82F6')

    # Компонент 1.2: UI Components Module
    draw_component(410, 80, 350, 440, "Модуль компонентов (UI)", "«module: components»", [
        "Атомарные блоки пользовательского интерфейса:",
        "• auth/ (AuthModal, EmailVerifyForm,",
        "  RegisterForm, LoginForm)",
        "• flights/ (FlightCard, StatusBadge,",
        "  Filters, SearchBar, SortDropdown)",
        "• home/ (HeroSection, FeaturesSection,",
        "  StatsSection, FAQSection, Newsletter)",
        "• layout/ (Header, Footer, DrawerMenu)",
        "• common/ (LoadingSkeleton, EmptyState,",
        "  Button, Badge, Modal)",
        "",
        "Особенности:",
        "  - Чистые функции (React.FC)",
        "  - Tailwind CSS стилизация",
        "  - Доступность по WCAG 2.1",
    ], '#FFFFFF', '#3B82F6')

    # Компонент 1.3: State & Context Module
    draw_component(50, 545, 340, 530, "Модуль состояния (State)", "«module: context & hooks»", [
        "Реактивное управление данными:",
        "• AuthContext.tsx",
        "  - session token, user profile",
        "  - login(), logout(), verify()",
        "  - статус is_email_verified",
        "• FavoritesContext.tsx",
        "  - toggleFavorite(), isFavorite()",
        "  - синхронизация со счётчиком",
        "",
        "Кастомные хуки (hooks/):",
        "• useFlights.ts (кэширование, стейт)",
        "• useDebounce.ts (оптимизация ввода)",
        "• useLocalStorage.ts (персистентность)",
        "",
        "Маршрутизация (React Router v7):",
        "• App.tsx (Дерево маршрутов SPA)",
        "• Динамические роуты /flights/:id",
    ], '#FFFFFF', '#3B82F6')

    # Компонент 1.4: Client Services Module
    draw_component(410, 545, 350, 530, "Модуль сервисов (Services)", "«module: api services»", [
        "Клиент доступа к данным и сети:",
        "• api.ts (REST-клиент рейсов)",
        "  - fetchFlights(params)",
        "  - fetchFlightById(id)",
        "  - fetchAirports()",
        "• authApi.ts (Клиент авторизации)",
        "  - login(email, password)",
        "  - register(email, password)",
        "  - verifyEmail(email, code)",
        "• mockFlights.ts (Offline Fallback)",
        "  - Резервный кэш рейсов при сбое",
        "",
        "Сетевая конфигурация:",
        "  - Axios instance c базовым URL",
        "  - Трансформация snake <-> camel",
        "  - Обработка ошибок тайм-аута (2с)",
    ], '#EFF6FF', '#1D4ED8')

    # Внутри-фронтенд стрелки
    draw_connector((220, 520), (220, 545), "useContext", (225, 528), False, '#2563EB')
    draw_connector((390, 300), (410, 300), "Render", (392, 285), False, '#2563EB')
    draw_connector((410, 780), (390, 780), "State update", (330, 765), True, '#2563EB')
    draw_connector((220, 520), (410, 680), "api calls", (310, 600), False, '#2563EB')

    # ================= 2. СЕТЕВОЙ ШЛЮЗ (NGINX GATEWAY) =================
    draw_subsystem(805, 30, 205, 1070, "Сетевой шлюз (Nginx)", '#F0FDF4', '#16A34A')

    draw_component(820, 160, 175, 330, "Nginx Static Server", "«web-server»", [
        "Раздача статики:",
        "• index.html",
        "• assets/*.js (Бандл)",
        "• assets/*.css",
        "• fonts/ (Benzin, TT)",
        "",
        "Оптимизации:",
        "• Gzip / Brotli",
        "• Кэширование ассетов",
        "• Fallback на index.html",
        "  для SPA-маршрутов",
    ], '#FFFFFF', '#16A34A')

    draw_component(820, 570, 175, 390, "Nginx Reverse Proxy", "«reverse-proxy»", [
        "Маршрутизация вызовов:",
        "• Проксирование /api/*",
        "  на 127.0.0.1:8000",
        "• SSL/TLS Termination",
        "  (Порт 443 / HTTPS)",
        "• Заголовки CORS:",
        "  Allow-Origin",
        "  Allow-Methods",
        "  Allow-Headers",
        "• Rate-limiting защита",
        "• Буферизация ответов",
    ], '#FFFFFF', '#16A34A')

    # Связи Фронтенд <-> Nginx
    draw_connector((760, 260), (820, 260), "HTTP GET", (765, 245), False, '#16A34A')
    draw_connector((760, 720), (820, 720), "/api/* JSON", (762, 705), False, '#1E3A8A')

    # ================= 3. ПОДСИСТЕМА BACKEND (DJANGO 5 & DRF) =================
    draw_subsystem(1035, 30, 735, 1070, "Подсистема серверной части (Backend Subsystem — Django 5 & DRF)", '#FAF5FF', '#7C3AED')

    # Компонент 3.1: Корневой модуль маршрутизации
    draw_component(1055, 80, 330, 245, "URL Router & Security", "«core: urls.py»", [
        "Диспетчеризация входящих запросов:",
        "• backend/urls.py (Корневой роутер)",
        "• DefaultRouter DRF (/api/flights/)",
        "• URL-паттерны /api/auth/*",
        "• SecurityMiddleware, CorsMiddleware",
        "• PBKDF2 Password Hashing (SHA256)",
        "• Сессионная и токен-аутентификация",
    ], '#FFFFFF', '#7C3AED')

    # Компонент 3.2: Приложение Accounts
    draw_component(1415, 80, 335, 245, "Модуль Accounts", "«app: accounts»", [
        "Управление пользователями и 2FA:",
        "• views.py (Register, VerifyEmail, Login)",
        "• serializers.py (User, Profile, Code)",
        "• models.py (UserProfile, Code)",
        "• services.py (EmailService, Генерация кода)",
        "• 6-значные коды с TTL 15 минут",
        "• Связь 1:1 к Django auth_user",
    ], '#FFFFFF', '#7C3AED')

    # Компонент 3.3: Приложение Flights
    draw_component(1055, 355, 330, 290, "Модуль Flights", "«app: flights»", [
        "Управление рейсами и аэропортами:",
        "• views.py (FlightViewSet, AirportViewSet)",
        "• serializers.py (Flight, Airport DTO)",
        "• models.py (Flight, Airport таблицы)",
        "• Параметры поиска и фильтрации:",
        "  - search, airline, status",
        "  - ordering: price, departure_time",
        "• Валидация входных данных QuerySet",
    ], '#FFFFFF', '#7C3AED')

    # Компонент 3.4: Фоновые сервисы и движок 24/7
    draw_component(1415, 355, 335, 290, "Модуль Services (24/7 Engine)", "«services: lifecycle»", [
        "Фоновая бизнес-логика и симуляция:",
        "• services.py (FlightLifecycleEngine)",
        "• Актуализация статусов по часам:",
        "  scheduled -> boarding -> in_air -> landed",
        "• commands/cleanup_flights.py:",
        "  - автоочистка рейсов старше 14 дней",
        "• services.py (AviationstackSyncClient):",
        "  - загрузка реальных рейсов из API",
    ], '#FFFDF0', '#D97706')

    # Компонент 3.5: Django ORM (Слой абстракции данных)
    draw_component(1055, 675, 695, 120, "Слой моделей и абстракции данных (Django ORM)", "«data access layer»", [
        "• QuerySet API (ленивая загрузка, транзакции atomic, валидация связей 1:1 и 1:N)",
        "• Модели сущностей: Flight, Airport, UserProfile, EmailVerificationCode, auth_user",
        "• Генерация высокопроизводительных SQL-запросов (SELECT, INSERT, UPDATE, DELETE)",
    ], '#FFFFFF', '#B45309')

    # Компонент 3.6: База данных SQLite 3
    draw_component(1055, 825, 330, 250, "База данных SQLite 3", "«database: sqlite3»", [
        "Файл реляционной базы (db.sqlite3):",
        "• flights_flight (Рейсы, статус, цена)",
        "• flights_airport (Хабы, IATA, город)",
        "• auth_user (Хэши паролей PBKDF2)",
        "• accounts_userprofile (is_email_verified)",
        "• accounts_emailverificationcode (TTL 15м)",
        "• Индексы: IATA code, flight_number",
    ], '#F1F5F9', '#334155')

    # Компонент 3.7: Внешние интерфейсы (Интеграции)
    draw_component(1415, 825, 335, 250, "Внешние сервисы (Integrations)", "«external interfaces»", [
        "Внешние сетевые шлюзы:",
        "• Яндекс SMTP (smtp.yandex.ru)",
        "  - Защищенный протокол SSL (порт 465)",
        "  - Отправка 6-значных кодов 2FA",
        "• Aviationstack REST API",
        "  - Загрузка расписаний рейсов мира",
        "  - Источник реальных авиаданных",
    ], '#FFFFFF', '#DC2626')

    # Связи Nginx -> Backend
    draw_connector((995, 680), (1055, 210), "WSGI /api/*", (985, 420), False, '#7C3AED')

    # Внутри бэкенда связи
    draw_connector((1385, 170), (1415, 170), "auth calls", (1380, 155), False, '#7C3AED')
    draw_connector((1220, 325), (1220, 355), "dispatch", (1225, 335), False, '#7C3AED')
    draw_connector((1385, 470), (1415, 470), "run lifecycle", (1380, 455), False, '#D97706')

    # Backend -> ORM
    draw_connector((1220, 645), (1220, 675), "QuerySet API", (1225, 655), False, '#B45309')
    draw_connector((1580, 645), (1580, 675), "ORM Queries", (1585, 655), False, '#B45309')

    # ORM -> SQLite & External
    draw_connector((1220, 795), (1220, 825), "SQL CRUD", (1225, 805), False, '#334155')
    draw_connector((1580, 795), (1580, 825), "SMTP / HTTPS", (1585, 805), False, '#DC2626')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"Module diagram PNG generated: {output_path}")

if __name__ == '__main__':
    generate_module_diagram_png()
