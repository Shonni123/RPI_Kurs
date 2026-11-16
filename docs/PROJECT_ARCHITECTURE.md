# Архитектура проекта (Project Architecture)

В данном документе представлена многоуровневая архитектура программного комплекса веб-сервиса **Flight Tracker** («Разработка веб-интерфейса для информационного сервиса об авиарейсах на React»), спроектированная в строгом соответствии с принципами чистой архитектуры, разделения ответственности (SoC) и требованиями дисциплины «Разработка программных интерфейсов» (РПИ).

---

## 1. Готовое изображение архитектуры проекта (для отчёта Word/PDF)

![Архитектура проекта](./project_architecture.png)

*Файлы архитектурной диаграммы высокой чёткости (300 DPI) на чистом белом фоне:*
* **Редактируемый проект Draw.io:** [`docs/project_architecture.drawio`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/project_architecture.drawio)
* **PNG формат:** [`docs/project_architecture.png`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/project_architecture.png)
* **Векторный SVG формат:** [`docs/project_architecture.svg`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/project_architecture.svg)

---

## 2. Диаграмма архитектуры проекта в нотации Mermaid

```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': {'darkMode': false, 'background': '#FFFFFF', 'mainBkg': '#FFFFFF', 'nodeBorder': '#333333', 'textColor': '#000000', 'lineColor': '#1E3A8A'}}}%%
graph TD
    subgraph Tier1["1. Клиентский уровень (Frontend — React 19 SPA)"]
        UI_Pages["Страницы и экраны (Landing, Flights, Detail, Airports)"]
        UI_Components["UI-компоненты (FlightCard, Filters, SearchBar, Skeleton)"]
        UI_State["Управление состоянием и роутинг (React Router v7, AuthContext, LocalStorage)"]
        UI_Services["Сервисный слой данных (api.ts, Axios, Offline Cache)"]
        UI_Pages --> UI_Components
        UI_Components --> UI_State
        UI_State --> UI_Services
    end

    subgraph Tier2["2. Сетевой уровень и веб-сервер (Gateway & Web Server)"]
        Nginx_Static["Nginx Static Web Server (HTML, JS, CSS, Gzip)"]
        Nginx_Proxy["Nginx Reverse Proxy (SSL Termination, CORS, /api/*)"]
        Gunicorn_WSGI["WSGI / Gunicorn (Python Application Server)"]
        Nginx_Proxy --> Gunicorn_WSGI
    end

    subgraph Tier3["3. Серверный уровень (Backend — Django 5 & DRF)"]
        DRF_Router["URL-маршрутизация и безопасность (urls.py, DefaultRouter, PBKDF2)"]
        DRF_ViewSets["Контроллеры API (FlightViewSet, AirportViewSet, AuthViewSet)"]
        DRF_Serializers["Сериализаторы моделей (DRF ModelSerializers)"]
        Engine_Background["Фоновые сервисы и бизнес-логика (Flight Lifecycle Engine 24/7, TTL Cleaner)"]
        DRF_Router --> DRF_ViewSets
        DRF_ViewSets --> DRF_Serializers
        DRF_ViewSets --> Engine_Background
    end

    subgraph Tier4["4. Слой данных, СУБД и внешние интеграции"]
        Django_ORM["Django ORM (Слой моделей, QuerySet API, миграции)"]
        SQLite_DB[("СУБД SQLite 3 (flights, airports, auth, codes)")]
        Yandex_SMTP["Яндекс SMTP (SSL порт 465, 2FA коды)"]
        Aviationstack_API["Aviationstack API (Внешний REST шлюз)"]
        Django_ORM <--> SQLite_DB
    end

    %% Межуровневые связи
    UI_Pages <-->|"HTTP (Статика)"| Nginx_Static
    UI_Services <-->|"REST API (JSON over HTTPS)"| Nginx_Proxy
    Gunicorn_WSGI <-->|"WSGI Вызовы"| DRF_Router
    DRF_ViewSets <-->|"QuerySet API"| Django_ORM
    Engine_Background <-->|"Отправка 2FA"| Yandex_SMTP
    Engine_Background <-->|"Синхронизация рейсов"| Aviationstack_API
```

---

## 3. Детальное описание архитектурных уровней

### Уровень 1: Клиентский уровень (Frontend — React 19 SPA)
* **Страницы (Pages):** Полноценное одностраничное приложение (`Landing`, `Flights`, `FlightDetail`, `Airports`, `Favorites`, `About`, `NotFound`).
* **Компоненты (UI Layer):** Атомарные переиспользуемые элементы интерфейса: карточки рейсов с индикацией статуса, плашки авиакомпаний, живой поиск с debounce, мерцающие скелетоны загрузки, модальные окна и боковая шторка навигации.
* **Стейт и маршрутизация:** Маршрутизация на базе `react-router-dom v7`. Контексты `AuthContext` (авторизация, статус верификации почты) и `FavoritesContext` с локальным хранением в `localStorage`.
* **Сервисный слой данных (`src/services/api.ts`):** Инкапсулирует вызовы к REST API через Axios/Fetch, производит сериализацию/десериализацию форматов (snake_case $\leftrightarrow$ camelCase) и предоставляет fallback-кэш на случай сбоя сети.

### Уровень 2: Сетевой уровень и обратный прокси-сервер (Nginx & Gunicorn)
* **Раздача статики:** Nginx отдаёт скомпилированный бандл фронтенда с поддержкой кэширования и сжатия Gzip / Brotli.
* **Обратный прокси:** Все клиентские вызовы по маске `/api/*` прозрачно проксируются на внутренний бэкенд-сервер. Nginx обеспечивает изоляцию внутренней сети, SSL-терминацию и настройку CORS-заголовков.
* **WSGI-сервер (Gunicorn):** Обеспечивает запуск многопоточного пула воркеров для обработки Python/Django-запросов.

### Уровень 3: Серверный уровень (Backend — Django 5 & DRF)
* **URL-диспетчер и безопасность:** `urls.py` и `DefaultRouter` сопоставляют URI с контроллерами. Слой middleware осуществляет валидацию токенов и хэширование паролей по стандарту **PBKDF2-SHA256**.
* **Контроллеры (ViewSets):** `FlightViewSet` (поиск по городам/аэропортам, фильтрация по статусу и авиакомпаниям, сортировка), `AirportViewSet` (каталог узловых аэропортов), `AuthViewSet` (регистрация и двухфакторное подтверждение почты).
* **Сериализаторы (DRF Serializers):** Преобразуют реляционные объекты в структурированный JSON с валидацией полей.
* **Фоновые сервисы:** Движок симуляции полетов 24/7 (`update_dynamic_flight_lifecycle`), планировщик очистки архивных рейсов старше 14 дней (`cleanup_archived_flights`) и генератор 6-значных кодов подтверждения.

### Уровень 4: Слой доступа к данным и внешние интеграции
* **Django ORM:** Объектно-реляционное отображение (ORM), исключающее прямые небезопасные SQL-инъекции и обеспечивающее транзакционную целостность данных.
* **СУБД SQLite 3:** Локальная высокопроизводительная реляционная база данных с индексацией по ключевым полям (`IATA code`, `flight_number`, `status`).
* **Яндекс SMTP:** Интеграция с официальным почтовым шлюзом Яндекса через шифрованный канал SSL (порт 465) для отправки 6-значных кодов подтверждения регистрации.
* **Aviationstack API:** Внешний провайдер реальных данных гражданской авиации для начальной загрузки и синхронизации актуальных расписаний.
