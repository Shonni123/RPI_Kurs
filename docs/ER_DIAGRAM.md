# ER-диаграмма базы данных (Entity-Relationship Diagram)

В данном документе представлена **ER-диаграмма реляционной базы данных** веб-сервиса **Flight Tracker**, спроектированной на базе СУБД SQLite 3 с использованием Django ORM.

Схема выполнена в строгом академическом стиле на **чистом белом фоне** для вставки в пояснительную записку к курсовой работе (ГОСТ).

---

## 1. Готовое изображение ER-диаграммы (для вставки в отчёт Word)

![ER-диаграмма базы данных](./er_diagram.png)

*Файлы диаграммы высокой четкости (300 DPI) для пояснительной записки:*
* **PNG формат:** [`docs/er_diagram.png`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/er_diagram.png)
* **Векторный SVG формат:** [`docs/er_diagram.svg`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/er_diagram.svg)

---

## 2. ER-диаграмма в нотации Mermaid

```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': {'darkMode': false, 'background': '#FFFFFF', 'mainBkg': '#FFFFFF', 'nodeBorder': '#333333', 'textColor': '#000000', 'lineColor': '#1E3A8A'}}}%%
erDiagram
    USER ||--|| USER_PROFILE : "1:1 имеет профиль"
    USER ||--o{ EMAIL_VERIFICATION_CODE : "1:N генерирует коды"
    AIRPORT ||--o{ FLIGHT : "1:N аэропорт вылета"
    AIRPORT ||--o{ FLIGHT : "1:N аэропорт прилета"

    USER {
        int id PK
        varchar username UK
        varchar email UK
        varchar password "Хэш PBKDF2-SHA256"
        varchar first_name
        varchar last_name
        boolean is_active
        datetime date_joined
    }

    USER_PROFILE {
        int id PK
        int user_id FK "1:1 к auth_user"
        boolean is_email_verified "Подтверждение почты"
        varchar phone "Номер телефона"
        datetime created_at
    }

    EMAIL_VERIFICATION_CODE {
        int id PK
        int user_id FK "1:N к auth_user"
        varchar code "6-значный код"
        varchar purpose "verify_email / reset_password"
        boolean is_used "Флаг использования"
        datetime created_at "Срок действия 15 мин"
    }

    AIRPORT {
        int id PK
        varchar code UK "IATA-код (SVO, DME, DXB)"
        varchar name "Название аэропорта"
        varchar city "Город"
        varchar country "Страна"
        int departures_count "Количество вылетов"
        int arrivals_count "Количество прилетов"
        varchar timezone "Часовой пояс"
    }

    FLIGHT {
        int id PK
        varchar flight_id UK "Уникальный slug (su-1702)"
        varchar flight_number "Номер рейса (SU 1702)"
        varchar airline "Авиакомпания"
        varchar aircraft "Модель борта (Airbus A350)"
        varchar from_code FK "Код аэропорта вылета"
        varchar from_name "Аэропорт вылета"
        varchar from_city "Город вылета"
        varchar from_terminal "Терминал"
        varchar from_gate "Гейт"
        varchar to_code FK "Код аэропорта прилета"
        varchar to_name "Аэропорт прилета"
        varchar to_city "Город прилета"
        varchar to_terminal "Терминал"
        varchar to_gate "Гейт"
        varchar departure_time "Время вылета (ЧЧ:ММ)"
        varchar arrival_time "Время прилета (ЧЧ:ММ)"
        varchar departure_date "Дата вылета (ГГГГ-ММ-ДД)"
        varchar duration "Время в пути"
        varchar status "scheduled / in_air / landed / etc."
        varchar status_text "Текст статуса"
        int altitude "Высота полета (м)"
        int speed "Скорость (км/ч)"
        int price "Стоимость билета (руб)"
        boolean is_real_api "Флаг Aviationstack API"
        datetime created_at
        datetime updated_at "TTL удаление через 14 дней"
    }
```

---

## 3. Описание сущностей и реляционных связей

### 1. `auth_user` (Пользователи системы)
Базовая таблица аутентификации Django. Хранит учетные данные: уникальные логин и email, а также хэш пароля (криптостойкий алгоритм **PBKDF2 с солью SHA-256**).

### 2. `accounts_userprofile` (Профиль пользователя)
* **Тип связи:** `One-to-One (1:1)` с таблицей `auth_user` (`user_id` с ограничением UNIQUE и каскадным удалением `ON DELETE CASCADE`).
* **Назначение:** Расширение данных пользователя. Хранит статус верификации email (`is_email_verified`), контактный телефон и дату регистрации.

### 3. `accounts_emailverificationcode` (Коды подтверждения)
* **Тип связи:** `Many-to-One (1:N)` с таблицей `auth_user` (`user_id` с внешним ключом `ON DELETE CASCADE`).
* **Назначение:** Хранит временные 6-значные коды для подтверждения регистрации и сброса забытого пароля. Предусматривает автоматическую инвалидацию ранее выданных кодов и срок жизни 15 минут.

### 4. `flights_airport` (Аэропорты и хабы)
Справочная таблица транспортных узлов. Уникальный ключ `code` (3-символьный IATA-код) используется для связывания с маршрутами рейсов.

### 5. `flights_flight` (Авиарейсы и телеметрия)
* **Тип связи:** Логическая связь `Many-to-One (1:N)` с таблицей `flights_airport` по кодам `from_code` и `to_code`.
* **Назначение:** Полная карточка рейса, включая маршрут, терминалы, гейты, расписание, динамический статус жизненного цикла (`scheduled` $\rightarrow$ `boarding` $\rightarrow$ `in_air` $\rightarrow$ `landed`), параметры высоты и скорости. Поле `updated_at` и `departure_date` используются сервисом автоочистки завершенных рейсов (TTL 14 дней).
