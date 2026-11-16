# Диаграмма последовательности (Sequence Diagram)

В данном документе представлена актуальная **UML-диаграмма последовательности (Sequence Diagram)**, полностью переработанная в строгом соответствии с архитектурой проекта и замечаниями.

---

## 1. Сводка исправлений

| № | Было (замечание) | Стало (исправлено) | Архитектурное обоснование |
|---|---|---|---|
| **1** | Фоновая обработка рейсов была привязана к пользовательскому GET-запросу | **Выделен независимый процесс `loop`** | Демон жизненного цикла рейсов (пересчет статусов `scheduled -> in_air -> landed` и автоочистка TTL старше 14 дней) выполняется автономно, а GET-запрос пользователя выполняет только чтение с фильтрацией. |
| **2** | В шаге 29 было `UPDATE userprofile SET is_verified=True, is_used=True` | **Разделено на два независимых UPDATE через Django ORM** | `is_email_verified` принадлежит модели `USER_PROFILE`, а флаг `is_used` — модели `EMAIL_VERIFICATION_CODE`. |
| **3** | В условии проверки кода было `expires > now()` | **Заменено на проверку времени создания `(now() - created_at) <= 15 минут`** | В структуре базы данных нет отдельного поля `expires`, срок жизни 15 минут вычисляется от временной метки `created_at` и TTL. |
| **4** | В ответе шага 30 было `200 OK { token, user: verified }` | **Заменено на `200 OK — Электронная почта подтверждена`** | Не приписывает проекту лишнюю функциональность токенов, которая не была зафиксирована в спецификации. |
| **5** | Отсутствовал участник `Django ORM` | **Добавлена отдельная линия жизни `Django ORM`** | Полное соответствие первой диаграмме запросов: доступ к СУБД SQLite 3 из контроллеров и движка сервисов осуществляется исключительно через слой моделей Django ORM. |

---

## 2. Актуальная диаграмма последовательности (Mermaid)

```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': {'darkMode': false, 'background': '#FFFFFF', 'mainBkg': '#FFFFFF', 'nodeBorder': '#333333', 'textColor': '#000000', 'lineColor': '#1E3A8A'}}}%%
sequenceDiagram
    autonumber
    actor User as Пользователь
    participant UI as React SPA (UI)
    participant Api as Сервисы (api.ts)
    participant Django as Django REST API
    participant Engine as Движок сервисов
    participant ORM as Django ORM
    participant DB as СУБД SQLite 3
    participant SMTP as Яндекс SMTP (SSL)

    %% Блок 1: Фоновый процесс 24/7
    rect rgb(248, 250, 252)
    Note over Engine, DB: loop [Фоновый процесс: Демон жизненного цикла 24/7 и автоочистка TTL]
    Engine->>ORM: cleanup_archived_flights()
    ORM->>DB: DELETE FROM flights WHERE status IN ('landed','cancelled') AND updated_at < now() - 14 дн
    DB-->>ORM: Результат SQL (0 записей удалено)
    ORM-->>Engine: Подтверждение очистки TTL
    Engine->>ORM: update_dynamic_flight_lifecycle() (пересчет по времени)
    ORM->>DB: UPDATE flights SET status = 'in_air' / 'landed' WHERE ...
    DB-->>ORM: Статусы актуализированы
    ORM-->>Engine: Итерация цикла завершена
    end

    %% Блок 2: Получение табло рейсов пользователем
    rect rgb(240, 249, 255)
    Note over User, DB: Сценарий 1: Получение табло рейсов и фильтрация (Основной пользовательский процесс)
    User->>UI: Ввод фильтра "Сочи" на странице /flights
    UI->>Api: fetchFlights({ search: "Сочи" })
    Api->>Django: GET /api/flights/?search=Сочи
    Django->>ORM: Flight.objects.filter(Q(from_city__icontains=...) | Q(to_city__icontains=...))
    ORM->>DB: SELECT * FROM flights_flight WHERE search LIKE '%Сочи%'
    DB-->>ORM: Результат SQL-запроса (строки данных)
    ORM-->>Django: QuerySet объектов моделей Flight
    Django-->>Api: 200 OK [JSON: flights (camelCase)]
    Api-->>UI: Обновление состояния (стейта useMemo)
    UI-->>User: Отрисовка карточек рейсов (60 FPS)
    end

    %% Блок 3: Регистрация и подтверждение email
    rect rgb(254, 252, 232)
    Note over User, SMTP: Сценарий 2: Регистрация и подтверждение email через Яндекс SMTP (SSL)
    User->>UI: Ввод email и пароля в форме регистрации
    UI->>Api: register({ email, password })
    Api->>Django: POST /api/auth/register/
    Django->>ORM: User.objects.create_user(), UserProfile.objects.create()
    ORM->>DB: INSERT INTO auth_user (хэш PBKDF2), accounts_userprofile
    DB-->>ORM: Записи созданы
    ORM-->>Django: Пользователь сохранен
    Django->>ORM: EmailVerificationCode.generate_for_user()
    ORM->>DB: INSERT INTO accounts_emailverificationcode (код, created_at)
    DB-->>ORM: Код верификации сохранен
    ORM-->>Django: Код готов к отправке
    Django->>SMTP: send_mail(код, to=email, port=465 SSL smtp.yandex.ru)
    SMTP-->>Django: 250 Message accepted for delivery
    Django-->>Api: 201 Created { message: "Код отправлен на почту" }
    Api-->>UI: Открытие формы ввода 6-значного кода
    User->>UI: Ввод 6-значного кода из почты
    UI->>Api: verifyEmail({ email, code })
    Api->>Django: POST /api/auth/verify-email/
    Django->>ORM: EmailVerificationCode.objects.filter(code=..., is_used=False)
    ORM->>DB: SELECT * WHERE code = '...' AND is_used = FALSE AND (now() - created_at) <= 15 мин
    DB-->>ORM: Код найден и валиден
    ORM-->>Django: Подтверждение валидности кода
    Django->>ORM: Раздельное обновление: profile.is_email_verified = True, code.is_used = True
    ORM->>DB: UPDATE accounts_userprofile SET is_email_verified = TRUE; UPDATE accounts_emailverificationcode SET is_used = TRUE
    DB-->>ORM: Данные обновлены в SQLite
    ORM-->>Django: Транзакция успешно зафиксирована
    Django-->>Api: 200 OK — Электронная почта подтверждена
    Api-->>UI: Обновление статуса в интерфейсе
    UI-->>User: Уведомление об успешном подтверждении почты
    end
```

---

## 3. Ссылки на файлы диаграммы

* **Редактируемый проект Draw.io:** [`docs/sequence_diagram.drawio`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/sequence_diagram.drawio)
* **Растровое изображение для Word (300 DPI, белый фон):** [`docs/sequence_diagram.png`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/sequence_diagram.png)
* **Векторный формат:** [`docs/sequence_diagram.svg`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/sequence_diagram.svg)
