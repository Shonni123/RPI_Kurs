# ER-диаграмма базы данных (Entity-Relationship Diagram)

В данном документе представлена актуальная **ER-диаграмма реляционной базы данных** веб-сервиса **Flight Tracker** (СУБД SQLite 3 / Django ORM).

Схема оптимизирована по ГОСТу: в сущность **FLIGHT** включены все необходимые атрибуты телеметрии и актуализации данных (`departure_date`, `altitude`, `speed`, `updated_at`, `price`).

---

## 1. Готовое изображение ER-диаграммы (для вставки в отчёт Word)

![Актуальная ER-диаграмма базы данных](./er_diagram.png)

*Файлы диаграммы высокой четкости (300 DPI) для пояснительной записки:*
* **Редактируемый проект Draw.io:** [`docs/er_diagram.drawio`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/er_diagram.drawio)
* **PNG формат:** [`docs/er_diagram.png`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/er_diagram.png)
* **Векторный SVG формат:** [`docs/er_diagram.svg`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/er_diagram.svg)

---

## 2. Актуальная ER-диаграмма в нотации Mermaid

```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': {'darkMode': false, 'background': '#FFFFFF', 'mainBkg': '#FFFFFF', 'nodeBorder': '#333333', 'textColor': '#000000', 'lineColor': '#1E3A8A'}}}%%
erDiagram
    USER ||--|| USER_PROFILE : "1:1 имеет профиль"
    USER ||--o{ EMAIL_VERIFICATION_CODE : "1:N генерирует коды"
    AIRPORT ||--o{ FLIGHT : "1:N вылет (from)"
    AIRPORT ||--o{ FLIGHT : "1:N прилет (to)"

    USER {
        int id PK
        varchar username UK
        varchar email UK
        varchar password "PBKDF2 Hash"
        datetime date_joined
    }

    USER_PROFILE {
        int id PK
        int user_id FK "1:1 к auth_user"
        boolean is_email_verified "Подтверждение почты"
        varchar phone "Номер телефона"
    }

    EMAIL_VERIFICATION_CODE {
        int id PK
        int user_id FK "1:N к auth_user"
        varchar code "6-значный код"
        varchar purpose "verify / reset"
        boolean is_used "Использован"
        datetime created_at "TTL 15 мин"
    }

    AIRPORT {
        int id PK
        varchar code UK "IATA (SVO, DXB)"
        varchar name "Название хаба"
        varchar city "Город"
        varchar country "Страна"
    }

    FLIGHT {
        int id PK
        varchar flight_number "Номер (SU 1702)"
        varchar airline "Авиакомпания"
        varchar from_code FK "Код вылета"
        varchar to_code FK "Код прилета"
        varchar departure_date "Дата вылета"
        varchar departure_time "Время вылета"
        varchar arrival_time "Время прилета"
        varchar status "scheduled / in_air"
        int altitude "Высота полета (м)"
        int speed "Скорость (км/ч)"
        int price "Стоимость (руб.)"
        datetime updated_at "Время обновления"
    }
```

---

## 3. Сводная таблица сущности FLIGHT

| Поле | Тип данных | Назначение |
| :--- | :--- | :--- |
| `id` | `INTEGER` (PK) | Уникальный идентификатор рейса |
| `flight_number` | `VARCHAR(30)` | Номер рейса (например, SU 1702) |
| `airline` | `VARCHAR(100)` | Название авиакомпании |
| `from_code` | `VARCHAR(10)` (FK) | Код аэропорта вылета (связь 1:N с Airport) |
| `to_code` | `VARCHAR(10)` (FK) | Код аэропорта прилёта (связь 1:N с Airport) |
| `departure_date` | `VARCHAR(20)` | **Дата вылета (ГГГГ-ММ-ДД)** |
| `departure_time` | `VARCHAR(20)` | Время вылета (ЧЧ:ММ) |
| `arrival_time` | `VARCHAR(20)` | Время прилёта (ЧЧ:ММ) |
| `status` | `VARCHAR(30)` | Статус рейса (`scheduled`, `in_air`, `landed`) |
| `altitude` | `INTEGER` | **Телеметрия: текущая высота (м)** |
| `speed` | `INTEGER` | **Телеметрия: текущая скорость (км/ч)** |
| `price` | `INTEGER` | **Стоимость билета в рублях** |
| `updated_at` | `DATETIME` | **Временная метка последнего обновления** |
