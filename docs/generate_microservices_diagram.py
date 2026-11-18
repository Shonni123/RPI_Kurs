import os
import zlib, base64, urllib.parse
from PIL import Image, ImageDraw, ImageFont

def make_drawio_file(graph_model_xml, diagram_id="microservices-architecture", diagram_name="Микросервисная архитектура"):
    url_encoded = urllib.parse.quote(graph_model_xml.strip(), safe='~()*!\'')
    compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
    compressed = compressor.compress(url_encoded.encode('utf-8')) + compressor.flush()
    b64_payload = base64.b64encode(compressed).decode('utf-8')
    
    file_content = f'''<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="24.7.17">
  <diagram id="{diagram_id}" name="{diagram_name}">{b64_payload}</diagram>
</mxfile>'''
    return file_content

def generate_drawio_xml(output_path="docs/microservices_architecture.drawio"):
    graph_model = """<mxGraphModel dx="1422" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="950" background="#FFFFFF" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- ================= ФАКТИЧЕСКАЯ АРХИТЕКТУРА (МОНОЛИТ) ================= -->
    <mxCell id="PANEL_MONOLITH" value="ФАКТИЧЕСКАЯ АРХИТЕКТУРА: 3-Звенный Клиент-Серверный Монолит" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=12.5;fontColor=#0F172A;startSize=30;rounded=1;arcSize=4;" vertex="1" parent="1">
      <mxGeometry x="50" y="40" width="560" height="740" as="geometry" />
    </mxCell>

    <mxCell id="M_CLIENT" value="&lt;b&gt;Frontend Клиент (React 19 SPA)&lt;/b&gt;&lt;br&gt;Vite 8.2, React Router v7, Tailwind CSS, LocalStorage" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2563EB;fontSize=11;fontColor=#0F172A;strokeWidth=1.5;arcSize=6;" vertex="1" parent="PANEL_MONOLITH">
      <mxGeometry x="40" y="55" width="480" height="55" as="geometry" />
    </mxCell>

    <mxCell id="M_SERVER" value="&lt;b&gt;Монолитный Backend (Python 3.12 + Django 5 &amp; DRF)&lt;/b&gt;&lt;br&gt;DefaultRouter, FlightViewSet, AirportViewSet, AuthViewSet (2FA)&lt;br&gt;&lt;i&gt;Встроенный фоновый движок симуляции полетов (24/7 Engine)&lt;/i&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontSize=11;fontColor=#0F172A;strokeWidth=1.5;arcSize=6;" vertex="1" parent="PANEL_MONOLITH">
      <mxGeometry x="40" y="165" width="480" height="75" as="geometry" />
    </mxCell>

    <mxCell id="M_DB" value="&lt;b&gt;Встроенная база данных (SQLite 3 db.sqlite3)&lt;/b&gt;&lt;br&gt;Таблицы: flights, airports, user_profile, email_verification_code" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#FFFFFF;strokeColor=#DC2626;fontSize=11;fontColor=#0F172A;strokeWidth=1.5;" vertex="1" parent="PANEL_MONOLITH">
      <mxGeometry x="40" y="295" width="480" height="70" as="geometry" />
    </mxCell>

    <mxCell id="edge_m1" value="HTTP REST на единый сервер" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=1.8;fontColor=#1D4ED8;fontSize=10;fontStyle=1;" edge="1" parent="PANEL_MONOLITH" source="M_CLIENT" target="M_SERVER">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <mxCell id="edge_m2" value="Прямой in-process доступ через Django ORM" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.8;fontColor=#6D28D9;fontSize=10;fontStyle=1;" edge="1" parent="PANEL_MONOLITH" source="M_SERVER" target="M_DB">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <!-- Преимущества монолита -->
    <mxCell id="M_BENEFITS" value="Преимущества монолита для курсового проекта" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#059669;fontStyle=1;fontSize=11.5;fontColor=#047857;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="PANEL_MONOLITH">
      <mxGeometry x="40" y="420" width="480" height="275" as="geometry" />
    </mxCell>
    <mxCell id="B1" value="&lt;b&gt;Быстрый запуск одной командой&lt;/b&gt;&lt;br&gt;Оркестрация через docker-compose up, единый образ приложения, отсутствие распределённых зависимостей" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="M_BENEFITS">
      <mxGeometry x="20" y="38" width="440" height="65" as="geometry" />
    </mxCell>
    <mxCell id="B2" value="&lt;b&gt;Нулевые сетевые задержки вызовов&lt;/b&gt;&lt;br&gt;Бизнес-логика, контроллеры и база данных общаются внутри одного процесса без overhead сериализации gRPC/HTTP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="M_BENEFITS">
      <mxGeometry x="20" y="115" width="440" height="65" as="geometry" />
    </mxCell>
    <mxCell id="B3" value="&lt;b&gt;ACID-транзакции без распределенности&lt;/b&gt;&lt;br&gt;Строгая согласованность данных (Consistency) без необходимости реализации 2PC-транзакций и паттерна Saga" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="M_BENEFITS">
      <mxGeometry x="20" y="192" width="440" height="65" as="geometry" />
    </mxCell>


    <!-- ================= ЦЕЛЕВАЯ МИКРОСЕРВИСНАЯ СХЕМА ================= -->
    <mxCell id="PANEL_MICRO" value="ЦЕЛЕВАЯ ПРОЕКТНАЯ СХЕМА: Декомпозиция при масштабировании (&gt;100k MAU)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=12.5;fontColor=#0F172A;startSize=30;rounded=1;arcSize=4;" vertex="1" parent="1">
      <mxGeometry x="680" y="40" width="620" height="740" as="geometry" />
    </mxCell>

    <mxCell id="GW" value="&lt;b&gt;API Gateway (Nginx / Kong / Traefik)&lt;/b&gt;&lt;br&gt;Единая точка входа, SSL-терминация, балансировка, Rate Limiting, JWT-проверка" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#059669;fontSize=11;fontColor=#0F172A;strokeWidth=1.5;arcSize=6;" vertex="1" parent="PANEL_MICRO">
      <mxGeometry x="35" y="48" width="550" height="50" as="geometry" />
    </mxCell>

    <!-- Пул автономных микросервисов -->
    <mxCell id="MS_SERVICES" value="Пул автономных микросервисов со своими БД (Database-per-Service)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontStyle=1;fontSize=11.5;fontColor=#0369A1;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="PANEL_MICRO">
      <mxGeometry x="35" y="130" width="550" height="340" as="geometry" />
    </mxCell>

    <mxCell id="MS_FLIGHTS" value="&lt;b&gt;Flight Catalog Service&lt;/b&gt;&lt;br&gt;Поиск, расписание, фильтрация&lt;br&gt;&lt;font color=&quot;#2563EB&quot;&gt;&lt;b&gt;+ PostgreSQL (Master-Replica) / Redis Cache&lt;/b&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F9FF;strokeColor=#BAE6FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MS_SERVICES">
      <mxGeometry x="20" y="38" width="510" height="58" as="geometry" />
    </mxCell>

    <mxCell id="MS_AUTH" value="&lt;b&gt;Auth &amp; User Service&lt;/b&gt;&lt;br&gt;Управление аккаунтами, сессии, токены, профили&lt;br&gt;&lt;font color=&quot;#7C3AED&quot;&gt;&lt;b&gt;+ PostgreSQL&lt;/b&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F9FF;strokeColor=#BAE6FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MS_SERVICES">
      <mxGeometry x="20" y="110" width="510" height="58" as="geometry" />
    </mxCell>

    <mxCell id="MS_TRACK" value="&lt;b&gt;Flight Telemetry &amp; Lifecycle Service&lt;/b&gt;&lt;br&gt;Координаты, высота, скорость, изменение статусов в реальном времени&lt;br&gt;&lt;font color=&quot;#D97706&quot;&gt;&lt;b&gt;+ TimescaleDB (Time-series СУБД)&lt;/b&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F9FF;strokeColor=#BAE6FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MS_SERVICES">
      <mxGeometry x="20" y="182" width="510" height="58" as="geometry" />
    </mxCell>

    <mxCell id="MS_NOTIF" value="&lt;b&gt;Notification Service&lt;/b&gt;&lt;br&gt;Рассылка 6-значных 2FA кодов, уведомления об изменении статусов рейсов&lt;br&gt;&lt;font color=&quot;#EA580C&quot;&gt;&lt;b&gt;+ Yandex SMTP / Webhook / Push Gateway&lt;/b&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F9FF;strokeColor=#BAE6FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MS_SERVICES">
      <mxGeometry x="20" y="254" width="510" height="58" as="geometry" />
    </mxCell>

    <!-- Шина событий -->
    <mxCell id="BUS" value="&lt;b&gt;Шина событий (Apache Kafka / RabbitMQ Event Broker)&lt;/b&gt;&lt;br&gt;Асинхронная доставка сообщений, буферизация нагрузки, pub/sub топики" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontSize=11;fontColor=#78350F;strokeWidth=1.5;arcSize=6;" vertex="1" parent="PANEL_MICRO">
      <mxGeometry x="35" y="505" width="550" height="55" as="geometry" />
    </mxCell>

    <!-- Связи Gateway -> Services -->
    <mxCell id="edge_gw_flights" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=1.5;exitX=0.2;exitY=1;exitDx=0;exitDy=0;entryX=0.2;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="PANEL_MICRO" source="GW" target="MS_FLIGHTS">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <mxCell id="edge_gw_auth" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="PANEL_MICRO" source="GW" target="MS_AUTH">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <mxCell id="edge_gw_track" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=1.5;exitX=0.8;exitY=1;exitDx=0;exitDy=0;entryX=0.8;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="PANEL_MICRO" source="GW" target="MS_TRACK">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <!-- Связи с шиной событий -->
    <mxCell id="edge_auth_bus" value="Событие UserRegistered (2FA)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D97706;strokeWidth=1.3;dashed=1;fontColor=#B45309;fontSize=9.5;exitX=0.15;exitY=1;exitDx=0;exitDy=0;entryX=0.15;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="PANEL_MICRO" source="MS_AUTH" target="BUS">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="110" y="320" />
          <mxPoint x="110" y="505" />
        </Array>
      </mxGeometry>
    </mxCell>

    <mxCell id="edge_track_bus" value="Событие FlightStatusChanged" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D97706;strokeWidth=1.3;dashed=1;fontColor=#B45309;fontSize=9.5;exitX=0.85;exitY=1;exitDx=0;exitDy=0;entryX=0.85;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="PANEL_MICRO" source="MS_TRACK" target="BUS">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="490" y="390" />
          <mxPoint x="490" y="505" />
        </Array>
      </mxGeometry>
    </mxCell>

    <mxCell id="edge_bus_notif" value="Отправка email с кодом 2FA" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#EA580C;strokeWidth=1.3;dashed=1;fontColor=#C2410C;fontSize=9.5;exitX=0.45;exitY=0;exitDx=0;exitDy=0;entryX=0.45;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="PANEL_MICRO" source="BUS" target="MS_NOTIF">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

    <mxCell id="edge_bus_flights" value="Инвалидация кэша расписаний" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=1.3;dashed=1;fontColor=#1D4ED8;fontSize=9.5;exitX=0.05;exitY=0;exitDx=0;exitDy=0;entryX=0.05;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="PANEL_MICRO" source="BUS" target="MS_FLIGHTS">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="60" y="490" />
          <mxPoint x="60" y="240" />
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- ================= СВЯЗЬ МЕЖДУ МОНОЛИТОМ И МИКРОСЕРВИСАМИ ================= -->
    <mxCell id="edge_evolution" value="Эволюционный переход при росте нагрузки (&gt;100k MAU)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=2;dashed=1;fontColor=#334155;fontSize=11;fontStyle=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="PANEL_MONOLITH" target="PANEL_MICRO">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>

  </root>
</mxGraphModel>"""
    file_content = make_drawio_file(graph_model, "microservices-architecture", "Микросервисная архитектура")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"Generated draw.io (compressed base64): {output_path}")

def generate_microservices_png(output_path="docs/microservices_architecture.png"):
    scale = 2
    w, h = 1350 * scale, 820 * scale

    img = Image.new("RGB", (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_path = "C:/Windows/Fonts/arial.ttf"
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"

    font_panel_title = ImageFont.truetype(font_bold_path, 11.5 * scale)
    font_sub_title = ImageFont.truetype(font_bold_path, 10.5 * scale)
    font_box_title = ImageFont.truetype(font_bold_path, 10 * scale)
    font_box_text = ImageFont.truetype(font_path, 9 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 8.5 * scale)

    def S(v):
        return int(v * scale)

    def draw_panel(x, y, pw, ph, title):
        draw.rectangle([S(x), S(y), S(x + pw), S(y + ph)], fill="#F8FAFC", outline="#475569", width=S(1.4))
        draw.rectangle([S(x), S(y), S(x + pw), S(y + 26)], fill="#FFFFFF", outline="#475569", width=S(1.4))
        draw.text((S(x + 12), S(y + 5)), title, font=font_panel_title, fill="#0F172A")

    def draw_subgraph(x, y, sw, sh, title, border="#0284C7"):
        draw.rectangle([S(x), S(y), S(x + sw), S(y + sh)], fill="#FFFFFF", outline=border, width=S(1.2))
        draw.rectangle([S(x), S(y), S(x + sw), S(y + 22)], fill="#F8FAFC", outline=border, width=S(1.2))
        draw.text((S(x + 10), S(y + 4)), title, font=font_sub_title, fill="#0369A1")

    def draw_box(x, y, bw, bh, title, lines=[], bg="#FFFFFF", border="#334155", bwidth=1.2):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill=bg, outline=border, width=S(bwidth))
        draw.text((S(x + 10), S(y + 8)), title, font=font_box_title, fill="#0F172A")
        cur_y = y + 24
        for line in lines:
            draw.text((S(x + 10), S(cur_y)), line, font=font_box_text, fill="#334155")
            cur_y += 14

    def draw_cylinder(x, y, bw, bh, title, lines=[]):
        draw.rectangle([S(x), S(y + 8), S(x + bw), S(y + bh)], fill="#FFFFFF", outline="#DC2626", width=S(1.4))
        draw.ellipse([S(x), S(y), S(x + bw), S(y + 16)], fill="#FEE2E2", outline="#DC2626", width=S(1.4))
        draw.text((S(x + 12), S(y + 18)), title, font=font_box_title, fill="#991B1B")
        cur_y = y + 36
        for line in lines:
            draw.text((S(x + 12), S(cur_y)), line, font=font_box_text, fill="#334155")
            cur_y += 14

    def draw_arrow(p1, p2, label=None, color="#475569", width=1.5, dashed=False):
        x1, y1 = p1
        x2, y2 = p2
        if dashed:
            dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            segs = max(1, int(dist / 8))
            for i in range(segs):
                if i % 2 == 0:
                    ta = i / segs
                    tb = min(1.0, (i + 0.6) / segs)
                    draw.line([S(x1 + (x2 - x1)*ta), S(y1 + (y2 - y1)*ta),
                               S(x1 + (x2 - x1)*tb), S(y1 + (y2 - y1)*tb)], fill=color, width=S(width))
        else:
            draw.line([S(x1), S(y1), S(x2), S(y2)], fill=color, width=S(width))

        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            ux = dx / length
            uy = dy / length
            vx = -uy
            vy = ux
            tip = (S(x2), S(y2))
            left = (S(x2 - ux * 6 + vx * 3), S(y2 - uy * 6 + vy * 3))
            right = (S(x2 - ux * 6 - vx * 3), S(y2 - uy * 6 - vy * 3))
            draw.polygon([tip, left, right], fill=color)

        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2 - 9
            draw.text((S(mx + 8), S(my)), label, font=font_arrow, fill=color)

    # 1. МОНОЛИТ
    draw_panel(40, 30, 560, 740, "ФАКТИЧЕСКАЯ АРХИТЕКТУРА: 3-Звенный Клиент-Серверный Монолит")
    draw_box(70, 75, 500, 50, "Frontend Клиент (React 19 SPA)", [
        "Vite 8.2, React Router v7, Tailwind CSS, LocalStorage кэш"
    ], "#FFFFFF", "#2563EB", 1.5)

    draw_box(70, 165, 500, 68, "Монолитный Backend (Python 3.12 + Django 5 & DRF)", [
        "DefaultRouter, FlightViewSet, AirportViewSet, AuthViewSet (2FA)",
        "Встроенный фоновый движок симуляции полетов (24/7 Engine)"
    ], "#FFFFFF", "#0284C7", 1.5)

    draw_cylinder(70, 275, 500, 65, "Встроенная база данных (SQLite 3 db.sqlite3)", [
        "Таблицы: flights, airports, user_profile, email_verification_code"
    ])

    draw_arrow((320, 125), (320, 165), label="HTTP REST", color="#2563EB", width=1.8)
    draw_arrow((320, 233), (320, 275), label="Django ORM", color="#7C3AED", width=1.8)

    # Преимущества монолита
    draw_subgraph(70, 380, 500, 360, "Преимущества монолита для курсового проекта", "#059669")
    draw_box(90, 420, 460, 85, "Быстрый запуск одной командой", [
        "• Оркестрация через docker-compose up за 30 секунд",
        "• Единый монолитный репозиторий без рассинхронизации версий",
        "• Отсутствие необходимости в Service Discovery и Consul"
    ], "#ECFDF5", "#A7F3D0")

    draw_box(90, 525, 460, 85, "Нулевые сетевые задержки вызовов", [
        "• Прямой in-process вызов контроллеров и моделей без задержек",
        "• Нет накладных расходов на сетевую сериализацию gRPC/HTTP",
        "• Удобная отладка и логирование в едином потоке"
    ], "#ECFDF5", "#A7F3D0")

    draw_box(90, 630, 460, 85, "ACID-транзакции без распределенности", [
        "• Строгая согласованность данных (Consistency) из коробки",
        "• Нет риска частичных отказов и сложных откатов (Saga pattern)",
        "• Локальный транзакционный журнал SQLite 3 (WAL mode)"
    ], "#ECFDF5", "#A7F3D0")

    # 2. МИКРОСЕРВИСЫ
    draw_panel(670, 30, 640, 740, "ЦЕЛЕВАЯ ПРОЕКТНАЯ СХЕМА: Декомпозиция при масштабировании (>100k MAU)")
    draw_box(700, 75, 580, 50, "API Gateway (Nginx / Kong / Traefik)", [
        "Единый шлюз, SSL-терминация, балансировка нагрузки, Rate Limiting, JWT-аудит"
    ], "#FFFFFF", "#059669", 1.5)

    draw_subgraph(700, 150, 580, 370, "Пул автономных микросервисов со своими БД (Database-per-Service)", "#0284C7")
    draw_box(720, 185, 540, 68, "Flight Catalog Service + PostgreSQL / Redis Cache", [
        "Поиск, расписание, фильтрация по статусам, IATA аэропорты",
        "Кэширование часто запрашиваемых данных в Redis (TTL 60s)"
    ], "#F0F9FF", "#BAE6FD")

    draw_box(720, 265, 540, 68, "Auth & User Service + PostgreSQL", [
        "Регистрация, хэширование паролей, профили пользователей",
        "Управление сессиями и выдача JWT access/refresh токенов"
    ], "#F0F9FF", "#BAE6FD")

    draw_box(720, 345, 540, 68, "Flight Telemetry & Lifecycle Service + TimescaleDB", [
        "Фоновый движок симуляции полетов, расчет высоты, скорости и координат",
        "Оптимизированная Time-series база данных для временных рядов"
    ], "#F0F9FF", "#BAE6FD")

    draw_box(720, 425, 540, 68, "Notification Service (Email 2FA / Webhook / Push)", [
        "Асинхронная отправка 6-значных кодов подтверждения через Yandex SMTP",
        "Push-уведомления пассажиров о задержке и посадке рейсов"
    ], "#F0F9FF", "#BAE6FD")

    # Шина событий
    draw_box(700, 545, 580, 55, "Шина событий (Apache Kafka / RabbitMQ Event Broker)", [
        "Асинхронный брокер событий, pub/sub топики: user-events, flight-status-events"
    ], "#FEF3C7", "#D97706", 1.5)

    # Связи Gateway -> Микросервисы
    draw_arrow((780, 125), (780, 185), color="#059669")
    draw_arrow((990, 125), (990, 265), color="#059669")
    draw_arrow((1200, 125), (1200, 345), color="#059669")

    # Связи с шиной событий
    draw_arrow((750, 333), (750, 545), label="UserRegistered", color="#D97706", dashed=True)
    draw_arrow((1180, 413), (1180, 545), label="FlightStatusChanged", color="#D97706", dashed=True)
    draw_arrow((990, 545), (990, 493), label="Отправка 2FA", color="#EA580C", dashed=True)
    draw_arrow((715, 545), (715, 253), label="Инвалидация кэша", color="#2563EB", dashed=True)

    # Эволюционный переход
    draw_arrow((600, 400), (670, 400), label="Эволюция (>100k MAU)", color="#475569", width=2, dashed=True)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Generated 300 DPI PNG: {output_path}")

def generate_microservices_svg(output_path="docs/microservices_architecture.svg"):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1350 820" width="100%" height="100%" style="background:#FFFFFF; font-family: Arial, sans-serif;">
  <defs>
    <marker id="arrow-gray" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563EB" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#7C3AED" />
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#D97706" />
    </marker>
  </defs>

  <!-- МОНОЛИТ -->
  <rect x="40" y="30" width="560" height="740" rx="6" fill="#F8FAFC" stroke="#475569" stroke-width="1.4" />
  <rect x="40" y="30" width="560" height="26" rx="6" fill="#FFFFFF" stroke="#475569" stroke-width="1.4" />
  <text x="52" y="48" font-size="12" font-weight="bold" fill="#0F172A">ФАКТИЧЕСКАЯ АРХИТЕКТУРА: 3-Звенный Клиент-Серверный Монолит</text>

  <rect x="70" y="75" width="500" height="50" rx="4" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.5" />
  <text x="85" y="96" font-size="11" font-weight="bold" fill="#0F172A">Frontend Клиент (React 19 SPA)</text>
  <text x="85" y="112" font-size="9.5" fill="#475569">Vite 8.2, React Router v7, Tailwind CSS, LocalStorage кэш</text>

  <rect x="70" y="165" width="500" height="68" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5" />
  <text x="85" y="185" font-size="11" font-weight="bold" fill="#0F172A">Монолитный Backend (Python 3.12 + Django 5 &amp; DRF)</text>
  <text x="85" y="202" font-size="9.5" fill="#475569">DefaultRouter, FlightViewSet, AirportViewSet, AuthViewSet (2FA)</text>
  <text x="85" y="218" font-size="9.5" fill="#0369A1">Встроенный фоновый движок симуляции полетов (24/7 Engine)</text>

  <path d="M 70 283 C 70 273, 570 273, 570 283 L 570 330 C 570 340, 70 340, 70 330 Z" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.4" />
  <path d="M 70 283 C 70 293, 570 293, 570 283" fill="none" stroke="#DC2626" stroke-width="1.4" />
  <text x="90" y="305" font-size="11" font-weight="bold" fill="#991B1B">Встроенная база данных (SQLite 3 db.sqlite3)</text>
  <text x="90" y="322" font-size="9.5" fill="#475569">Таблицы: flights, airports, user_profile, email_verification_code</text>

  <line x1="320" y1="125" x2="320" y2="157" stroke="#2563EB" stroke-width="1.8" marker-end="url(#arrow-blue)" />
  <text x="328" y="145" font-size="9.5" font-weight="bold" fill="#2563EB">HTTP REST</text>

  <line x1="320" y1="233" x2="320" y2="267" stroke="#7C3AED" stroke-width="1.8" marker-end="url(#arrow-purple)" />
  <text x="328" y="255" font-size="9.5" font-weight="bold" fill="#7C3AED">Django ORM</text>

  <!-- Преимущества монолита -->
  <rect x="70" y="380" width="500" height="360" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="1.2" />
  <rect x="70" y="380" width="500" height="22" rx="4" fill="#F8FAFC" stroke="#059669" stroke-width="1.2" />
  <text x="80" y="396" font-size="11" font-weight="bold" fill="#047857">Преимущества монолита для курсового проекта</text>

  <rect x="90" y="420" width="460" height="85" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="105" y="442" font-size="10.5" font-weight="bold" fill="#0F172A">Быстрый запуск одной командой</text>
  <text x="105" y="460" font-size="9" fill="#334155">• Оркестрация через docker-compose up за 30 секунд</text>
  <text x="105" y="475" font-size="9" fill="#334155">• Единый репозиторий без рассинхронизации версий контрактов</text>
  <text x="105" y="490" font-size="9" fill="#334155">• Отсутствие необходимости в Service Discovery и Consul</text>

  <rect x="90" y="525" width="460" height="85" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="105" y="547" font-size="10.5" font-weight="bold" fill="#0F172A">Нулевые сетевые задержки вызовов</text>
  <text x="105" y="565" font-size="9" fill="#334155">• Прямой in-process вызов контроллеров и моделей без сети</text>
  <text x="105" y="580" font-size="9" fill="#334155">• Нет накладных расходов на сетевую сериализацию gRPC/HTTP</text>
  <text x="105" y="595" font-size="9" fill="#334155">• Удобная отладка и логирование в едином потоке сервера</text>

  <rect x="90" y="630" width="460" height="85" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="105" y="652" font-size="10.5" font-weight="bold" fill="#0F172A">ACID-транзакции без распределенности</text>
  <text x="105" y="670" font-size="9" fill="#334155">• Строгая согласованность данных (Consistency) из коробки</text>
  <text x="105" y="685" font-size="9" fill="#334155">• Нет риска частичных отказов и сложных откатов (Saga pattern)</text>
  <text x="105" y="700" font-size="9" fill="#334155">• Локальный транзакционный журнал SQLite 3 (WAL mode)</text>

  <!-- МИКРОСЕРВИСЫ -->
  <rect x="670" y="30" width="640" height="740" rx="6" fill="#F8FAFC" stroke="#475569" stroke-width="1.4" />
  <rect x="670" y="30" width="640" height="26" rx="6" fill="#FFFFFF" stroke="#475569" stroke-width="1.4" />
  <text x="682" y="48" font-size="12" font-weight="bold" fill="#0F172A">ЦЕЛЕВАЯ ПРОЕКТНАЯ СХЕМА: Декомпозиция при масштабировании (&gt;100k MAU)</text>

  <rect x="700" y="75" width="580" height="50" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="1.5" />
  <text x="715" y="96" font-size="11" font-weight="bold" fill="#0F172A">API Gateway (Nginx / Kong / Traefik)</text>
  <text x="715" y="112" font-size="9.5" fill="#475569">Единый шлюз, SSL-терминация, балансировка нагрузки, Rate Limiting, JWT-аудит</text>

  <rect x="700" y="150" width="580" height="370" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" />
  <rect x="700" y="150" width="580" height="22" rx="4" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.2" />
  <text x="710" y="166" font-size="11" font-weight="bold" fill="#0369A1">Пул автономных микросервисов со своими БД (Database-per-Service)</text>

  <rect x="720" y="185" width="540" height="68" rx="3" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1" />
  <text x="735" y="206" font-size="10.5" font-weight="bold" fill="#0F172A">Flight Catalog Service + PostgreSQL / Redis Cache</text>
  <text x="735" y="223" font-size="9" fill="#475569">Поиск, расписание, фильтрация по статусам, IATA аэропорты</text>
  <text x="735" y="238" font-size="9" fill="#0284C7">Кэширование горячих поисковых запросов в Redis (TTL 60s)</text>

  <rect x="720" y="265" width="540" height="68" rx="3" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1" />
  <text x="735" y="286" font-size="10.5" font-weight="bold" fill="#0F172A">Auth &amp; User Service + PostgreSQL</text>
  <text x="735" y="303" font-size="9" fill="#475569">Регистрация, хэширование паролей, профили пользователей</text>
  <text x="735" y="318" font-size="9" fill="#7C3AED">Управление сессиями и выдача JWT access/refresh токенов</text>

  <rect x="720" y="345" width="540" height="68" rx="3" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1" />
  <text x="735" y="366" font-size="10.5" font-weight="bold" fill="#0F172A">Flight Telemetry &amp; Lifecycle Service + TimescaleDB</text>
  <text x="735" y="383" font-size="9" fill="#475569">Фоновый движок симуляции полетов, расчет высоты, скорости и координат</text>
  <text x="735" y="398" font-size="9" fill="#D97706">Оптимизированная Time-series база данных для временных рядов</text>

  <rect x="720" y="425" width="540" height="68" rx="3" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1" />
  <text x="735" y="446" font-size="10.5" font-weight="bold" fill="#0F172A">Notification Service (Email 2FA / Webhook / Push)</text>
  <text x="735" y="463" font-size="9" fill="#475569">Асинхронная отправка 6-значных кодов подтверждения через Yandex SMTP</text>
  <text x="735" y="478" font-size="9" fill="#EA580C">Push-уведомления пассажиров о задержке и посадке рейсов</text>

  <rect x="700" y="545" width="580" height="55" rx="4" fill="#FEF3C7" stroke="#D97706" stroke-width="1.5" />
  <text x="715" y="567" font-size="11" font-weight="bold" fill="#78350F">Шина событий (Apache Kafka / RabbitMQ Event Broker)</text>
  <text x="715" y="585" font-size="9.5" fill="#92400E">Асинхронный брокер событий, pub/sub топики: user-events, flight-status-events</text>

  <!-- СВЯЗИ В МИКРОСЕРВИСАХ -->
  <line x1="780" y1="125" x2="780" y2="177" stroke="#059669" stroke-width="1.5" marker-end="url(#arrow-green)" />
  <path d="M 990 125 L 990 257" fill="none" stroke="#059669" stroke-width="1.5" marker-end="url(#arrow-green)" />
  <path d="M 1200 125 L 1200 337" fill="none" stroke="#059669" stroke-width="1.5" marker-end="url(#arrow-green)" />

  <path d="M 750 333 L 750 537" fill="none" stroke="#D97706" stroke-width="1.3" stroke-dasharray="3,3" marker-end="url(#arrow-orange)" />
  <text x="758" y="520" font-size="8.5" font-weight="bold" fill="#D97706">UserRegistered</text>

  <path d="M 1180 413 L 1180 537" fill="none" stroke="#D97706" stroke-width="1.3" stroke-dasharray="3,3" marker-end="url(#arrow-orange)" />
  <text x="1070" y="525" font-size="8.5" font-weight="bold" fill="#D97706">FlightStatusChanged</text>

  <path d="M 990 545 L 990 501" fill="none" stroke="#EA580C" stroke-width="1.3" stroke-dasharray="3,3" marker-end="url(#arrow-orange)" />
  <text x="998" y="525" font-size="8.5" font-weight="bold" fill="#EA580C">Отправка 2FA</text>

  <path d="M 715 545 L 715 261" fill="none" stroke="#2563EB" stroke-width="1.3" stroke-dasharray="3,3" marker-end="url(#arrow-blue)" />
  <text x="635" y="300" font-size="8" font-weight="bold" fill="#2563EB">Инвалидация кэша</text>

  <!-- ЭВОЛЮЦИОННЫЙ ПЕРЕХОД -->
  <line x1="600" y1="400" x2="662" y2="400" stroke="#475569" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-gray)" />
  <text x="590" y="390" font-size="9.5" font-weight="bold" fill="#334155">Эволюция (&gt;100k MAU)</text>
</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Generated SVG: {output_path}")

if __name__ == "__main__":
    generate_drawio_xml()
    generate_microservices_png()
    generate_microservices_svg()
