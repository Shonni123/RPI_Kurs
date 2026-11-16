# Диаграмма последовательности (Sequence Diagram)

В данном документе представлена **UML-диаграмма последовательности (Sequence Diagram)**, иллюстрирующая сквозной жизненный цикл взаимодействий между пользователем, клиентским приложением React 19, бэкендом Django REST Framework, базой данных SQLite 3 и внешним почтовым шлюзом Яндекс SMTP.

Диаграмма охватывает два главных пользовательских сценария:
1. **Сценарий А:** Запрос табло рейсов с фильтрацией, динамическим пересчетом жизненного цикла 24/7 и автоочисткой TTL.
2. **Сценарий Б:** Регистрация пользователя с генерацией 6-значного кода и отправкой через Яндекс SMTP по защищенному протоколу SSL (порт 465).

---

## 1. Готовое изображение диаграммы (для вставки в отчёт Word)

![Диаграмма последовательности](./sequence_diagram.png)

*Файлы диаграммы высокой четкости (300 DPI) для пояснительной записки:*
* **PNG формат:** [`docs/sequence_diagram.png`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/sequence_diagram.png)
* **Векторный SVG формат:** [`docs/sequence_diagram.svg`](file:///c:/Users/faizr/PycharmProjects/KursovayaRPI/docs/sequence_diagram.svg)

---

## 2. Диаграмма последовательности (Mermaid-код)

```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': {'darkMode': false, 'background': '#FFFFFF', 'mainBkg': '#FFFFFF', 'nodeBorder': '#333333', 'textColor': '#000000', 'lineColor': '#1E3A8A'}}}%%
sequenceDiagram
    autonumber
    actor User as Пользователь
    participant UI as React SPA (UI)
    participant Api as Сервисы (api.ts)
    participant Django as Django REST API
    participant Engine as Движок сервисов
    participant DB as СУБД SQLite 3
    participant SMTP as Яндекс SMTP (SSL 465)

    %% Сценарий 1: Просмотр и фильтрация табло рейсов
    rect rgb(240, 249, 255)
    Note over User, DB: Сценарий 1: Получение табло рейсов и симуляция статусов 24/7
    User->>UI: Ввод фильтра "Сочи" на странице /flights
    UI->>Api: fetchFlights({ search: "Сочи" })
    Api->>Django: GET /api/flights/?search=Сочи
    Django->>Engine: update_dynamic_flight_lifecycle()
    Engine->>DB: cleanup_archived_flights (DELETE старше 14 дней)
    DB-->>Engine: 0 записей удалено
    Engine->>DB: Обновление статусов по часам (scheduled -> in_air -> landed)
    DB-->>Engine: Статусы актуализированы
    Django->>DB: SELECT * FROM flights_flight WHERE search LIKE '%Сочи%'
    DB-->>Django: Строки рейсов
    Django-->>Api: 200 OK [JSON: flights (camelCase)]
    Api-->>UI: Обновление стейта (useMemo)
    UI-->>User: Отрисовка карточек рейсов (60 FPS)
    end

    %% Сценарий 2: Регистрация и подтверждение email кодом
    rect rgb(254, 252, 232)
    Note over User, SMTP: Сценарий 2: Регистрация и подтверждение email 6-значным кодом
    User->>UI: Ввод email и пароля в модалке регистрации
    UI->>Api: register({ email, password })
    Api->>Django: POST /api/auth/register/
    Django->>DB: INSERT auth_user (хэш PBKDF2), userprofile (verified=False)
    DB-->>Django: User создан
    Django->>Engine: EmailVerificationCode.generate_for_user()
    Engine->>DB: INSERT 6-значный код (TTL 15 мин)
    DB-->>Engine: Код сохранен
    Django->>SMTP: send_mail(код, to=email, port=465 SSL)
    SMTP-->>Django: 250 Message accepted for delivery
    Django-->>Api: 201 Created { message: "Код отправлен на почту" }
    Api-->>UI: Переключение на таб ввода кода
    UI-->>User: Отображение 6 ячеек ввода (автофокус)

    User->>UI: Ввод 6-значного кода из письма
    UI->>Api: verifyEmail({ email, code })
    Api->>Django: POST /api/auth/verify-email/
    Django->>DB: SELECT код WHERE is_used=False AND expires > now()
    DB-->>Django: Код валиден
    Django->>DB: UPDATE userprofile SET is_email_verified=True, code.is_used=True
    DB-->>Django: Профиль подтвержден
    Django-->>Api: 200 OK { token, user: { is_verified: true } }
    Api-->>UI: Сохранение сессии в AuthContext
    UI-->>User: Успешный вход, статус "Подтвержден", переход в профиль
    end
```

---

## 3. Подробное описание взаимодействий

### Сценарий 1: Онлайн-мониторинг рейсов и симуляция 24/7
1. **Шаги 1–3:** Пользователь задает критерии поиска на странице `/flights`. React передает вызов в модуль `api.ts`, формирующий GET-запрос к API.
2. **Шаги 4–8:** Перед выдачей рейсов контроллер запускает фоновый движок `update_dynamic_flight_lifecycle()`:
   * Проводится проверка TTL: завершенные рейсы (`landed`/`cancelled`) старше 14 дней удаляются из базы.
   * Актуализируются статусы бортов по текущему системному времени (за 45 мин до вылета — `boarding`, во время полета — `in_air`, по прибытии — `landed`).
3. **Шаги 9–12:** Сериализатор форматирует строки из базы SQLite в JSON со свойствами в camelCase, React обновляет стейт и отрисовывает карточки со скоростью 60 FPS.

### Сценарий 2: Регистрация и 2FA подтверждение почты
1. **Шаги 13–16:** Пользователь отправляет регистрационную форму. Django хэширует пароль по стандарту **PBKDF2-SHA256** и создает записи в таблицах `auth_user` и `accounts_userprofile`.
2. **Шаги 17–22:** Генерируется случайный криптостойкий 6-значный код со сроком действия 15 минут. Инициируется SMTP-сессия с почтовым сервером Яндекса через SSL-порт 465. Пользователю отдается форма с 6 ячейками ввода.
3. **Шаги 23–29:** При вводе кода отправляется запрос верификации. Сервер проверяет актуальность кода в базе, помечает его использованным (`is_used = True`), обновляет статус профиля `is_email_verified = True` и авторизует пользователя.

