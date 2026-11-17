# Модульная диаграмма программного комплекса (UML Component / Module Diagram)

В данном документе представлена **Модульная диаграмма** веб-сервиса **Flight Tracker** («Разработка веб-интерфейса для информационного сервиса об авиарейсах на React»), спроектированная в строгом соответствии со стандартами UML и принципами модульной декомпозиции программной инженерии по дисциплине «Разработка программных интерфейсов» (РПИ).

---

## 1. Готовое изображение модульной диаграммы (для отчёта Word/PDF)

![Модульная диаграмма программного комплекса](./module_diagram.png)

*Файлы модульной диаграммы высокой чёткости (300 DPI) на чистом белом фоне:*
* **Редактируемый проект Draw.io:** [`docs/module_diagram.drawio`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/module_diagram.drawio)
* **PNG формат:** [`docs/module_diagram.png`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/module_diagram.png)
* **Векторный SVG формат:** [`docs/module_diagram.svg`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/module_diagram.svg)

---

## 2. Модульная диаграмма в нотации Mermaid

```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': {'darkMode': false, 'background': '#FFFFFF', 'mainBkg': '#FFFFFF', 'nodeBorder': '#333333', 'textColor': '#000000', 'lineColor': '#1E3A8A'}}}%%
graph TD
    subgraph Frontend["Подсистема клиентской части (React 19 SPA)"]
        Pages["Модуль страниц (Pages)<br/>• HomePage, FlightsPage, FlightDetailPage<br/>• AirportsPage, FavoritesPage, UserProfile"]
        UI_Components["Модуль UI-компонентов<br/>• auth/ (AuthModal, 6-code Verify)<br/>• flights/ (FlightCard, Filters, Search)<br/>• layout/ (Header, Footer, Drawer)"]
        State_Module["Модуль состояния (State & Context)<br/>• AuthContext, FavoritesContext<br/>• useFlights, useDebounce, Router v7"]
        Services_Module["Модуль API-сервисов (Services)<br/>• api.ts (REST-клиент рейсов)<br/>• authApi.ts (Регистрация, 2FA)<br/>• mockFlights.ts (Offline Fallback)"]
        
        Pages -->|"«use»"| UI_Components
        Pages -->|"«subscribe»"| State_Module
        State_Module -->|"«call»"| Services_Module
    end

    subgraph Gateway["Сетевой шлюз (Nginx)"]
        Nginx_Static["Nginx Static Server<br/>(Раздача HTML5, JS-бандла, CSS, Gzip)"]
        Nginx_Proxy["Nginx Reverse Proxy<br/>(SSL 443, CORS, проксирование /api/*)"]
    end

    subgraph Backend["Подсистема серверной части (Django 5 & DRF)"]
        Router_Module["Ядро и маршрутизация (urls.py)<br/>• DefaultRouter, CORS, PBKDF2"]
        Accounts_App["Модуль Accounts<br/>• views.py, serializers.py, models.py<br/>• EmailService, генерация 6-значных кодов"]
        Flights_App["Модуль Flights<br/>• FlightViewSet, AirportViewSet<br/>• Фильтры, поиск, сортировка"]
        Lifecycle_Engine["Модуль Services (24/7 Engine)<br/>• FlightLifecycleEngine (статусы)<br/>• cleanup_flights (TTL очистка 14 дней)<br/>• AviationstackSyncClient"]
        Django_ORM["Слой моделей (Django ORM)<br/>• QuerySet API, транзакции atomic, миграции"]
        SQLite_DB[("СУБД SQLite 3<br/>• flights, airports, auth_user, codes")]
        External_Services["Внешние интерфейсы<br/>• Яндекс SMTP (порт 465 SSL)<br/>• Aviationstack REST API"]

        Router_Module -->|"«dispatch»"| Accounts_App
        Router_Module -->|"«dispatch»"| Flights_App
        Flights_App -->|"«invoke»"| Lifecycle_Engine
        Flights_App -->|"QuerySet"| Django_ORM
        Accounts_App -->|"QuerySet"| Django_ORM
        Lifecycle_Engine -->|"QuerySet"| Django_ORM
        Django_ORM -->|"SQL CRUD"| SQLite_DB
        Accounts_App -->|"SMTP SSL"| External_Services
        Lifecycle_Engine -->|"HTTPS Sync"| External_Services
    end

    %% Межсистемные связи
    UI_Components -->|"HTTP GET"| Nginx_Static
    Services_Module -->|"/api/* JSON"| Nginx_Proxy
    Nginx_Proxy -->|"WSGI Вызовы"| Router_Module
```

---

## 3. Описание модульной декомпозиции программного комплекса

### 3.1 Подсистема клиентской части (Frontend — React 19)
* **Модуль страниц (`src/pages/`):** Высокоуровневые экранные формы (`HomePage`, `FlightsPage`, `FlightDetailPage`, `AirportsPage`, `FavoritesPage`, `UserProfilePage`, `AboutPage`, `NotFoundPage`). Модуль отвечает за композицию интерфейса, обработку параметров маршрута (`useParams`) и передачу данных в UI-компоненты.
* **Модуль компонентов (`src/components/`):** Иерархия переиспользуемых визуальных блоков:
  * `auth/` — диалоговые формы входа, регистрации и 6-ячеечного ввода кода подтверждения;
  * `flights/` — интерактивные карточки рейсов, переключатели статусов («В полёте», «Ожидает взлёта», «Прибыл»), селектор авиакомпаний;
  * `layout/` — шапка со счётчиком избранного, подвал и плавная боковая шторка (Drawer);
  * `common/` — скелетоны ожидания (`LoadingSkeleton`) и заглушки отсутствия данных (`EmptyState`).
* **Модуль состояния и хуков (`src/context/`, `src/hooks/`):** Обеспечивает единый источник правды (Single Source of Truth). `AuthContext` сохраняет токен и профиль пользователя; `FavoritesContext` синхронизирует закладки с `localStorage`; хуки `useDebounce` снижают нагрузку на сервер при поиске рейсов.
* **Модуль API-сервисов (`src/services/`):** Сетевой модуль (`api.ts`, `authApi.ts`) инкапсулирует вызовы HTTP, преобразует snake_case сервера в camelCase интерфейса и активирует `mockFlights.ts` при задержке ответа свыше 2 секунд.

### 3.2 Сетевой шлюз (Gateway — Nginx)
* **Nginx Static Server:** Обеспечивает высокоскоростную отдачу скомпилированных ассетов (HTML, JavaScript, CSS, шрифты Benzin и TT Travels) со сжатием Gzip/Brotli и клиентским кэшированием.
* **Nginx Reverse Proxy:** Выступает единой точкой входа (`Single Point of Entry`), экранирует внутренний контур Django, терминарует SSL/TLS и настраивает заголовки CORS.

### 3.3 Подсистема серверной части (Backend — Django 5 & DRF)
* **Модуль ядра и диспетчеризации (`backend/`):** Конфигурация параметров безопасности (`settings.py`), корневой URL-диспетчер (`urls.py`) и генерация схемы эндпоинтов на базе DRF `DefaultRouter`.
* **Модуль `flights` (`backend/flights/`):** Реализует REST API управления авиарейсами: выборка с многокритериальной фильтрацией (город, аэропорт, статус, перевозчик), динамическая сортировка по стоимости и времени вылета.
* **Модуль `accounts` (`backend/accounts/`):** Отвечает за аутентификацию и безопасность: регистрация новых пользователей, хэширование паролей по стандарту PBKDF2-SHA256, генерация криптостойких 6-значных кодов с TTL 15 минут.
* **Модуль фоновых служб (`Lifecycle Engine & Services`):** Независимый демон 24/7 (`update_dynamic_flight_lifecycle`), который автоматически рассчитывает текущее положение и статус борта по системному времени, и фоновая команда `cleanup_flights`, удаляющая рейсы старше 14 дней.
* **Слой моделей (`Django ORM`):** Гарантирует типобезопасный доступ к реляционным таблицам без прямых сырых SQL-вызовов, обеспечивая ACID-транзакции.
* **СУБД SQLite 3:** Локальное дисковое реляционное хранилище со структурированными индексами.
* **Внешние интерфейсы:** Почтовый шлюз Яндекс SMTP (порт 465 SSL) для отправки кодов 2FA и клиент Aviationstack API для периодической синхронизации глобального расписания.
