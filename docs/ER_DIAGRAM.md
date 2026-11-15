# ER-диаграмма базы данных (Entity-Relationship Diagram)

В данном документе представлена компактная **ER-диаграмма реляционной базы данных** веб-сервиса **Flight Tracker** (СУБД SQLite 3 / Django ORM).

Схема оптимизирована по ГОСТу: оставлены только ключевые атрибуты (PK, FK, UK и главные бизнес-поля), что делает диаграмму компактной, легко читаемой и идеально подходящей для вставки в лист А4 отчёта.

---

## 1. Готовое изображение ER-диаграммы (для вставки в отчёт Word)

![Компактная ER-диаграмма базы данных](./er_diagram.png)

*Файлы диаграммы высокой четкости (300 DPI) для пояснительной записки:*
* **PNG формат:** [`docs/er_diagram.png`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/er_diagram.png)
* **Векторный SVG формат:** [`docs/er_diagram.svg`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/er_diagram.svg)

---

## 2. Компактная ER-диаграмма в нотации Mermaid

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
        varchar departure_time "Время вылета"
        varchar arrival_time "Время прилета"
        varchar status "scheduled / in_air"
        int price "Стоимость (руб)"
    }
```

---

## 3. Сводная таблица связей

| Отношение | Тип связи | Внешний ключ (FK) | Ограничения целостности | Назначение |
| :--- | :---: | :--- | :--- | :--- |
| **USER $\leftrightarrow$ USER_PROFILE** | **1 : 1** | `user_id` $\rightarrow$ `User.id` | `UNIQUE`, `ON DELETE CASCADE` | Личный профиль с флагом подтверждения email |
| **USER $\leftrightarrow$ EMAIL_VERIFICATION_CODE** | **1 : N** | `user_id` $\rightarrow$ `User.id` | `ON DELETE CASCADE` | Временные 6-значные коды (TTL 15 мин) |
| **AIRPORT $\leftrightarrow$ FLIGHT (вылет)** | **1 : N** | `from_code` $\rightarrow$ `Airport.code` | Логическая целостность | Привязка рейса к аэропорту отправления |
| **AIRPORT $\leftrightarrow$ FLIGHT (прилёт)** | **1 : N** | `to_code` $\rightarrow$ `Airport.code` | Логическая целостность | Привязка рейса к аэропорту назначения |
