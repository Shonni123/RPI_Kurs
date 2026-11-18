import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

def generate_drawio_xml(output_path="docs/project_architecture.drawio"):
    xml_content = """<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="24.7.17">
  <diagram id="project-architecture" name="Архитектура проекта">
    <mxGraphModel dx="1422" dy="880" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="950" background="#FFFFFF" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ================= 1. КЛИЕНТСКИЙ УРОВЕНЬ ================= -->
        <mxCell id="tier1_group" value="1. Клиентский уровень (Client Tier)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="40" width="760" height="110" as="geometry" />
        </mxCell>
        <mxCell id="box_browser" value="&lt;b&gt;Браузер пользователя&lt;/b&gt;&lt;br&gt;Desktop / Mobile (Chrome, Safari, Firefox)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#334155;fontSize=11;fontColor=#0F172A;arcSize=6;" vertex="1" parent="tier1_group">
          <mxGeometry x="30" y="42" width="310" height="52" as="geometry" />
        </mxCell>
        <mxCell id="box_spa" value="&lt;b&gt;React 19 SPA&lt;/b&gt;&lt;br&gt;Vite 8.2, React Router v7, Tailwind CSS, Lucide Icons" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2563EB;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier1_group">
          <mxGeometry x="410" y="42" width="320" height="52" as="geometry" />
        </mxCell>
        <mxCell id="edge_browser_spa" value="Взаимодействие с UI" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;fontColor=#475569;fontSize=10;fontStyle=1;" edge="1" parent="tier1_group" source="box_browser" target="box_spa">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ================= 2. ВЕБ-СЕРВЕР И ШЛЮЗ ================= -->
        <mxCell id="tier2_group" value="2. Веб-сервер и шлюз (Gateway Tier)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="190" width="760" height="95" as="geometry" />
        </mxCell>
        <mxCell id="box_nginx" value="&lt;b&gt;Nginx 1.25 Alpine&lt;/b&gt;&lt;br&gt;Reverse Proxy / Раздача статики (Gzip, кэширование, SPA try_files, прокси /api/)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#059669;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier2_group">
          <mxGeometry x="80" y="38" width="600" height="46" as="geometry" />
        </mxCell>

        <!-- ================= 3. УРОВЕНЬ ПРИЛОЖЕНИЙ ================= -->
        <mxCell id="tier3_group" value="3. Уровень приложений (Application Tier)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="325" width="760" height="135" as="geometry" />
        </mxCell>
        <mxCell id="box_django" value="&lt;b&gt;Python 3.12 + Django 5 &amp; DRF REST API (Port 8000)&lt;/b&gt;&lt;br&gt;URL-роутер, FlightViewSet, AirportViewSet, AuthViewSet (PBKDF2-SHA256, 2FA)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier3_group">
          <mxGeometry x="30" y="42" width="410" height="75" as="geometry" />
        </mxCell>
        <mxCell id="box_engine" value="&lt;b&gt;Фоновые сервисы движка&lt;/b&gt;&lt;br&gt;• Flight Lifecycle Engine 24/7&lt;br&gt;• Очистка архива (cleanup_archived)&lt;br&gt;• Генератор 6-значных 2FA кодов" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#D97706;fontSize=10.5;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier3_group">
          <mxGeometry x="470" y="42" width="260" height="75" as="geometry" />
        </mxCell>
        <mxCell id="edge_django_engine" value="Асинхр. запуск" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#64748B;strokeWidth=1.2;fontColor=#64748B;fontSize=10;dashed=1;" edge="1" parent="tier3_group" source="box_django" target="box_engine">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ================= 4. УРОВЕНЬ ХРАНЕНИЯ ДАННЫХ ================= -->
        <mxCell id="tier4_group" value="4. Уровень хранения данных (Data Storage Tier)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="500" width="760" height="120" as="geometry" />
        </mxCell>
        <mxCell id="box_orm" value="&lt;b&gt;Django ORM&lt;/b&gt;&lt;br&gt;Слой моделей, QuerySet API, миграции, транзакционная целостность" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7C3AED;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier4_group">
          <mxGeometry x="60" y="45" width="280" height="55" as="geometry" />
        </mxCell>
        <mxCell id="box_sqlite" value="&lt;b&gt;Встроенная СУБД SQLite 3&lt;/b&gt;&lt;br&gt;Реляционная БД (db.sqlite3 / DatabaseSync)&lt;br&gt;&lt;i&gt;flights, airports, user_profile, verification_codes&lt;/i&gt;" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#FFFFFF;strokeColor=#DC2626;fontSize=10.5;fontColor=#0F172A;strokeWidth=1.5;" vertex="1" parent="tier4_group">
          <mxGeometry x="410" y="38" width="310" height="70" as="geometry" />
        </mxCell>
        <mxCell id="edge_orm_sqlite" value="SQL-запросы (CRUD)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.5;fontColor=#7C3AED;fontSize=10;fontStyle=1;" edge="1" parent="tier4_group" source="box_orm" target="box_sqlite">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ================= 5. ВНЕШНИЕ СЕРВИСЫ ================= -->
        <mxCell id="tier5_group" value="5. Внешние сервисы (External Services)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="870" y="270" width="420" height="200" as="geometry" />
        </mxCell>
        <mxCell id="box_yandex" value="&lt;b&gt;Яндекс Почта (Yandex SMTP)&lt;/b&gt;&lt;br&gt;SSL порт 465 / TLS порт 587&lt;br&gt;Отправка 6-значных кодов подтверждения email" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#EA580C;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier5_group">
          <mxGeometry x="30" y="45" width="360" height="58" as="geometry" />
        </mxCell>
        <mxCell id="box_aviation" value="&lt;b&gt;Aviationstack API&lt;/b&gt;&lt;br&gt;Внешний REST API провайдер реальных данных авиации&lt;br&gt;Первичная инициализация и синхронизация расписаний" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0891B2;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier5_group">
          <mxGeometry x="30" y="122" width="360" height="58" as="geometry" />
        </mxCell>

        <!-- ================= 6. КОНТЕЙНЕРИЗАЦИЯ ================= -->
        <mxCell id="tier6_group" value="6. Контейнеризация и инфраструктура (Infrastructure)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="870" y="40" width="420" height="195" as="geometry" />
        </mxCell>
        <mxCell id="box_docker" value="&lt;b&gt;Docker Compose Orchestration&lt;/b&gt;&lt;br&gt;• flight_tracker_frontend (Nginx Alpine + SPA dist, порт 3000:80)&lt;br&gt;• flight_tracker_backend (Python 3.12, Gunicorn/DRF, порт 8000:8000)&lt;br&gt;• Том хранения данных: backend_data:/app/data (SQLite 3 persistence)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontSize=10.5;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="tier6_group">
          <mxGeometry x="25" y="45" width="370" height="125" as="geometry" />
        </mxCell>

        <!-- ================= МЕЖУРОВНЕВЫЕ СВЯЗИ ================= -->
        <!-- SPA -> Nginx -->
        <mxCell id="edge_spa_nginx" value="HTTPS / Раздача статики и API-запросы" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=2;fontColor=#1E3A8A;fontSize=10.5;fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.65;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_spa" target="box_nginx">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Nginx -> Django -->
        <mxCell id="edge_nginx_django" value="Проксирование /api/ на внутренний порт 8000" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2;fontColor=#065F46;fontSize=10.5;fontStyle=1;exitX=0.35;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_nginx" target="box_django">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Django -> ORM -->
        <mxCell id="edge_django_orm" value="ORM-запросы (QuerySet API)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=2;fontColor=#5B21B6;fontSize=10.5;fontStyle=1;exitX=0.4;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_django" target="box_orm">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Django / Фоновые сервисы -> Внешние сервисы -->
        <mxCell id="edge_django_yandex" value="SMTP / TLS (Порт 465) Отправка писем" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#EA580C;strokeWidth=1.5;fontColor=#C2410C;fontSize=10;fontStyle=1;exitX=1;exitY=0.3;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_django" target="box_yandex">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="edge_engine_aviation" value="REST API / HTTPS Синхронизация" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0891B2;strokeWidth=1.5;fontColor=#0E7490;fontSize=10;fontStyle=1;exitX=1;exitY=0.7;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_engine" target="box_aviation">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Docker Compose Infrastructure связи -->
        <mxCell id="edge_docker_nginx" value="Управление контейнером" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284C7;strokeWidth=1.3;dashed=1;fontColor=#0369A1;fontSize=9.5;exitX=0;exitY=0.6;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_docker" target="box_nginx">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="edge_docker_django" value="Управление контейнером" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284C7;strokeWidth=1.3;dashed=1;fontColor=#0369A1;fontSize=9.5;exitX=0.2;exitY=1;exitDx=0;exitDy=0;entryX=0.85;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_docker" target="box_django">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="edge_docker_volume" value="Монтирование тома данных backend_data" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284C7;strokeWidth=1.3;dashed=1;fontColor=#0369A1;fontSize=9.5;exitX=0.7;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_docker" target="box_sqlite">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1164" y="240" />
              <mxPoint x="1310" y="240" />
              <mxPoint x="1310" y="573" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content.strip())
    print(f"Generated draw.io XML: {output_path}")

def generate_architecture_png(output_path="docs/project_architecture.png"):
    scale = 2
    w, h = 1350 * scale, 680 * scale

    # Pure white canvas
    img = Image.new("RGB", (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_path = "C:/Windows/Fonts/arial.ttf"
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"

    font_tier_title = ImageFont.truetype(font_bold_path, 12 * scale)
    font_box_title = ImageFont.truetype(font_bold_path, 10.5 * scale)
    font_box_text = ImageFont.truetype(font_path, 9 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 8.5 * scale)
    font_arrow_small = ImageFont.truetype(font_path, 8 * scale)

    def S(v):
        return int(v * scale)

    def draw_tier(x, y, tw, th, title, bg="#F8FAFC", border="#64748B"):
        draw.rectangle([S(x), S(y), S(x + tw), S(y + th)], fill=bg, outline=border, width=S(1.4))
        draw.rectangle([S(x), S(y), S(x + tw), S(y + 28)], fill="#FFFFFF", outline=border, width=S(1.4))
        draw.text((S(x + 14), S(y + 6)), title, font=font_tier_title, fill="#0F172A")

    def draw_box(x, y, bw, bh, title, lines=[], bg="#FFFFFF", border="#334155", bwidth=1.2):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill=bg, outline=border, width=S(bwidth))
        draw.text((S(x + 10), S(y + 8)), title, font=font_box_title, fill="#0F172A")
        cur_y = y + 26
        for line in lines:
            draw.text((S(x + 10), S(cur_y)), line, font=font_box_text, fill="#334155")
            cur_y += 15

    def draw_cylinder(x, y, bw, bh, title, lines=[], bg="#FFFFFF", border="#DC2626", bwidth=1.5):
        # Draw cylinder base and top ellipse
        draw.rectangle([S(x), S(y + 8), S(x + bw), S(y + bh)], fill=bg, outline=border, width=S(bwidth))
        draw.ellipse([S(x), S(y), S(x + bw), S(y + 16)], fill="#FEE2E2", outline=border, width=S(bwidth))
        draw.text((S(x + 12), S(y + 18)), title, font=font_box_title, fill="#991B1B")
        cur_y = y + 36
        for line in lines:
            draw.text((S(x + 12), S(cur_y)), line, font=font_box_text, fill="#334155")
            cur_y += 15

    def draw_arrow(p1, p2, label=None, label_pos=None, color="#2563EB", width=1.6, dashed=False):
        # p1 and p2 are (x, y)
        x1, y1 = p1
        x2, y2 = p2
        if dashed:
            # simple dashed line
            dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            d_segs = max(1, int(dist / 8))
            for i in range(d_segs):
                if i % 2 == 0:
                    t_a = i / d_segs
                    t_b = min(1.0, (i + 0.7) / d_segs)
                    draw.line([S(x1 + (x2 - x1)*t_a), S(y1 + (y2 - y1)*t_a),
                               S(x1 + (x2 - x1)*t_b), S(y1 + (y2 - y1)*t_b)], fill=color, width=S(width))
        else:
            draw.line([S(x1), S(y1), S(x2), S(y2)], fill=color, width=S(width))
        
        # Arrowhead at p2
        asize = S(5)
        # determine orientation
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            ux = dx / length
            uy = dy / length
            vx = -uy
            vy = ux
            tip = (S(x2), S(y2))
            left = (S(x2 - ux * 8 + vx * 4), S(y2 - uy * 8 + vy * 4))
            right = (S(x2 - ux * 8 - vx * 4), S(y2 - uy * 8 - vy * 4))
            draw.polygon([tip, left, right], fill=color)

        if label:
            lx, ly = label_pos if label_pos else ((x1 + x2)/2, (y1 + y2)/2 - 10)
            draw.text((S(lx), S(ly)), label, font=font_arrow, fill=color)

    # 1. CLIENT TIER
    draw_tier(40, 30, 780, 100, "1. Клиентский уровень (Client Tier)", "#F8FAFC", "#475569")
    draw_box(60, 65, 310, 52, "Браузер пользователя (Desktop / Mobile)", [
        "Chrome, Safari, Firefox, Edge, Мобильные браузеры"
    ], "#FFFFFF", "#334155")
    draw_box(460, 65, 340, 52, "React 19 SPA (Vite 8.2, React Router v7)", [
        "Tailwind CSS, Lucide Icons, AuthContext, LocalStorage"
    ], "#FFFFFF", "#2563EB", 1.5)
    draw_arrow((370, 91), (460, 91), "Взаимодействие", (375, 76), "#475569")

    # 2. GATEWAY TIER
    draw_tier(40, 160, 780, 90, "2. Веб-сервер и шлюз (Gateway Tier)", "#F8FAFC", "#475569")
    draw_box(120, 195, 620, 44, "Nginx 1.25 Alpine (Reverse Proxy / Раздача статики)", [
        "Раздача бандла SPA (/), Gzip-сжатие, кэширование, проксирование /api/ на :8000"
    ], "#FFFFFF", "#059669", 1.5)

    # 3. APPLICATION TIER
    draw_tier(40, 280, 780, 130, "3. Уровень приложений (Application Tier)", "#F8FAFC", "#475569")
    draw_box(60, 315, 410, 80, "Python 3.12 + Django 5 & DRF (Port 8000)", [
        "• URL-маршрутизатор (urls.py, DefaultRouter)",
        "• Контроллеры API: FlightViewSet, AirportViewSet, AuthViewSet",
        "• Аутентификация: PBKDF2-SHA256, сессии, валидация 2FA",
    ], "#FFFFFF", "#0284C7", 1.5)

    draw_box(500, 315, 300, 80, "Фоновые сервисы (Background Engine)", [
        "• Flight Lifecycle Engine 24/7 (симуляция)",
        "• Очистка архива: cleanup_archived_flights",
        "• Генерация и проверка 6-значных 2FA кодов",
    ], "#FFFFFF", "#D97706", 1.5)

    draw_arrow((470, 355), (500, 355), "Асинхр.", (465, 340), "#64748B", dashed=True)

    # 4. DATA STORAGE TIER
    draw_tier(40, 440, 780, 120, "4. Уровень хранения данных (Data Storage Tier)", "#F8FAFC", "#475569")
    draw_box(60, 475, 310, 68, "Django ORM", [
        "• Слой реляционных моделей и QuerySet API",
        "• Исключение SQL-инъекций, транзакции",
        "• Миграции схем данных (0001_initial)",
    ], "#FFFFFF", "#7C3AED", 1.5)

    draw_cylinder(440, 465, 360, 80, "Встроенная СУБД SQLite 3", [
        "• Реляционная БД db.sqlite3 (DatabaseSync)",
        "• Таблицы: flights, airports, user_profile, verification_codes",
    ], "#FFFFFF", "#DC2626", 1.5)

    draw_arrow((370, 509), (440, 509), "SQL-запросы (CRUD)", (372, 492), "#7C3AED")

    # 5. EXTERNAL SERVICES
    draw_tier(860, 240, 450, 200, "5. Внешние сервисы (External Services)", "#F8FAFC", "#475569")
    draw_box(880, 275, 410, 65, "Яндекс Почта (Yandex SMTP)", [
        "• Протокол: SMTP через защищённый SSL порт 465 / TLS :587",
        "• Отправка 6-значных кодов подтверждения email",
    ], "#FFFFFF", "#EA580C", 1.5)

    draw_box(880, 355, 410, 68, "Aviationstack API (Внешний REST API)", [
        "• Глобальный поставщик реальных данных авиации",
        "• Первичная инициализация расписаний и синхронизация",
    ], "#FFFFFF", "#0891B2", 1.5)

    # 6. INFRASTRUCTURE TIER
    draw_tier(860, 30, 450, 180, "6. Контейнеризация и инфраструктура (Infrastructure)", "#F8FAFC", "#475569")
    draw_box(880, 65, 410, 128, "Docker Compose Orchestration", [
        "• flight_tracker_frontend (Nginx Alpine + SPA dist, порт 3000:80)",
        "• flight_tracker_backend (Python 3.12, Django/DRF, порт 8000:8000)",
        "• Изолированная сеть bridge (внутреннее проксирование)",
        "• Постоянный том данных: backend_data:/app/data (SQLite 3 persistence)",
    ], "#FFFFFF", "#0284C7", 1.5)

    # CONNECTING INTER-TIER ARROWS
    # SPA -> Nginx
    draw.line([S(630), S(117), S(630), S(195)], fill="#2563EB", width=S(1.8))
    draw_arrow((630, 185), (630, 195), "HTTPS / Статика и REST API", (638, 145), "#2563EB")

    # Nginx -> Django
    draw.line([S(265), S(239), S(265), S(315)], fill="#059669", width=S(1.8))
    draw_arrow((265, 305), (265, 315), "Проксирование /api/ на порт 8000", (273, 268), "#059669")

    # Django -> ORM
    draw.line([S(215), S(395), S(215), S(475)], fill="#7C3AED", width=S(1.8))
    draw_arrow((215, 465), (215, 475), "QuerySet API", (223, 428), "#7C3AED")

    # Django -> Yandex SMTP
    draw_arrow((470, 335), (880, 305), "SMTP SSL :465 (Отправка кодов)", (560, 295), "#EA580C")

    # Engine -> Aviationstack
    draw_arrow((800, 375), (880, 385), "REST API / HTTPS", (805, 360), "#0891B2")

    # Docker -> Nginx
    draw_arrow((880, 120), (740, 205), "Управление контейнером", (760, 150), "#0284C7", dashed=True)

    # Docker -> Django
    draw_arrow((880, 155), (470, 325), "Управление контейнером", (560, 225), "#0284C7", dashed=True)

    # Docker -> Volume -> SQLite
    draw_arrow((1085, 193), (800, 505), "Монтирование тома данных backend_data", (880, 480), "#0284C7", dashed=True)

    # Footer note
    draw.text((S(40), S(630)), "Многоуровневая архитектура веб-сервиса Flight Tracker (РПИ). Чистая модульная архитектура, 6 уровней (Tiers), C4 Container Model.", font=font_arrow_small, fill="#64748B")

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Generated 300 DPI PNG: {output_path}")

def generate_architecture_svg(output_path="docs/project_architecture.svg"):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1350 670" width="100%" height="100%" style="background:#FFFFFF; font-family: Arial, sans-serif;">
  <defs>
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
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#EA580C" />
    </marker>
    <marker id="arrow-cyan" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0891B2" />
    </marker>
    <marker id="arrow-docker" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7" />
    </marker>
    <marker id="arrow-gray" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569" />
    </marker>
  </defs>

  <!-- 1. КЛИЕНТСКИЙ УРОВЕНЬ -->
  <rect x="40" y="30" width="780" height="100" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="40" y="30" width="780" height="28" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="54" y="49" font-size="13" font-weight="bold" fill="#0F172A">1. Клиентский уровень (Client Tier)</text>

  <rect x="60" y="66" width="310" height="52" rx="4" fill="#FFFFFF" stroke="#334155" stroke-width="1.2" />
  <text x="72" y="86" font-size="11.5" font-weight="bold" fill="#0F172A">Браузер пользователя (Desktop / Mobile)</text>
  <text x="72" y="103" font-size="10" fill="#475569">Chrome, Safari, Firefox, Edge, Мобильные клиенты</text>

  <rect x="460" y="66" width="340" height="52" rx="4" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.5" />
  <text x="472" y="86" font-size="11.5" font-weight="bold" fill="#0F172A">React 19 SPA (Vite 8.2, React Router v7)</text>
  <text x="472" y="103" font-size="10" fill="#475569">Tailwind CSS, Lucide Icons, AuthContext, LocalStorage</text>

  <line x1="370" y1="92" x2="452" y2="92" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-gray)" />
  <text x="382" y="84" font-size="9" font-weight="bold" fill="#475569">Взаимодействие</text>

  <!-- 2. ВЕБ-СЕРВЕР И ШЛЮЗ -->
  <rect x="40" y="160" width="780" height="90" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="40" y="160" width="780" height="28" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="54" y="179" font-size="13" font-weight="bold" fill="#0F172A">2. Веб-сервер и шлюз (Gateway Tier)</text>

  <rect x="120" y="196" width="620" height="44" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="1.5" />
  <text x="135" y="214" font-size="11.5" font-weight="bold" fill="#0F172A">Nginx 1.25 Alpine (Reverse Proxy / Раздача статики)</text>
  <text x="135" y="230" font-size="10" fill="#475569">Раздача бандла SPA (/), Gzip-сжатие, кэширование, проксирование /api/ на :8000</text>

  <!-- 3. УРОВЕНЬ ПРИЛОЖЕНИЙ -->
  <rect x="40" y="280" width="780" height="130" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="40" y="280" width="780" height="28" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="54" y="299" font-size="13" font-weight="bold" fill="#0F172A">3. Уровень приложений (Application Tier)</text>

  <rect x="60" y="318" width="410" height="80" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5" />
  <text x="72" y="337" font-size="11.5" font-weight="bold" fill="#0F172A">Python 3.12 + Django 5 &amp; DRF (Port 8000)</text>
  <text x="72" y="354" font-size="10" fill="#475569">• URL-маршрутизатор (urls.py, DefaultRouter)</text>
  <text x="72" y="370" font-size="10" fill="#475569">• Контроллеры API: FlightViewSet, AirportViewSet, AuthViewSet</text>
  <text x="72" y="386" font-size="10" fill="#475569">• Аутентификация: PBKDF2-SHA256, сессии, валидация 2FA</text>

  <rect x="500" y="318" width="300" height="80" rx="4" fill="#FFFFFF" stroke="#D97706" stroke-width="1.5" />
  <text x="512" y="337" font-size="11.5" font-weight="bold" fill="#0F172A">Фоновые сервисы (Background Engine)</text>
  <text x="512" y="354" font-size="10" fill="#475569">• Flight Lifecycle Engine 24/7 (симуляция полетов)</text>
  <text x="512" y="370" font-size="10" fill="#475569">• Очистка архива: cleanup_archived_flights</text>
  <text x="512" y="386" font-size="10" fill="#475569">• Генерация и проверка 6-значных 2FA кодов</text>

  <line x1="470" y1="358" x2="492" y2="358" stroke="#64748B" stroke-width="1.3" stroke-dasharray="3,3" marker-end="url(#arrow-gray)" />

  <!-- 4. УРОВЕНЬ ХРАНЕНИЯ ДАННЫХ -->
  <rect x="40" y="440" width="780" height="120" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="40" y="440" width="780" height="28" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="54" y="459" font-size="13" font-weight="bold" fill="#0F172A">4. Уровень хранения данных (Data Storage Tier)</text>

  <rect x="60" y="478" width="310" height="68" rx="4" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.5" />
  <text x="72" y="497" font-size="11.5" font-weight="bold" fill="#0F172A">Django ORM</text>
  <text x="72" y="514" font-size="10" fill="#475569">• Слой реляционных моделей и QuerySet API</text>
  <text x="72" y="530" font-size="10" fill="#475569">• Исключение прямых SQL-инъекций, транзакции</text>

  <path d="M 440 488 C 440 478, 800 478, 800 488 L 800 538 C 800 548, 440 548, 440 538 Z" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.5" />
  <path d="M 440 488 C 440 498, 800 498, 800 488" fill="none" stroke="#DC2626" stroke-width="1.5" />
  <text x="460" y="508" font-size="11.5" font-weight="bold" fill="#991B1B">Встроенная СУБД SQLite 3 (DatabaseSync)</text>
  <text x="460" y="525" font-size="10" fill="#475569">• Реляционная база данных db.sqlite3 (persistent volume)</text>
  <text x="460" y="540" font-size="9.5" fill="#64748B">flights, airports, user_profile, email_verification_code</text>

  <line x1="370" y1="512" x2="432" y2="512" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arrow-purple)" />
  <text x="375" y="504" font-size="9" font-weight="bold" fill="#7C3AED">SQL-запросы</text>

  <!-- 5. ВНЕШНИЕ СЕРВИСЫ -->
  <rect x="860" y="240" width="450" height="200" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="860" y="240" width="450" height="28" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="874" y="259" font-size="13" font-weight="bold" fill="#0F172A">5. Внешние сервисы (External Services)</text>

  <rect x="880" y="278" width="410" height="65" rx="4" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.5" />
  <text x="895" y="298" font-size="11.5" font-weight="bold" fill="#0F172A">Яндекс Почта (Yandex SMTP)</text>
  <text x="895" y="315" font-size="10" fill="#475569">• Протокол: SMTP через защищённый SSL порт 465 / TLS :587</text>
  <text x="895" y="331" font-size="10" fill="#475569">• Отправка 6-значных кодов подтверждения email</text>

  <rect x="880" y="358" width="410" height="68" rx="4" fill="#FFFFFF" stroke="#0891B2" stroke-width="1.5" />
  <text x="895" y="378" font-size="11.5" font-weight="bold" fill="#0F172A">Aviationstack API (Внешний REST API)</text>
  <text x="895" y="395" font-size="10" fill="#475569">• Глобальный поставщик реальных данных авиации</text>
  <text x="895" y="411" font-size="10" fill="#475569">• Первичная инициализация расписаний и синхронизация</text>

  <!-- 6. КОНТЕЙНЕРИЗАЦИЯ -->
  <rect x="860" y="30" width="450" height="180" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="860" y="30" width="450" height="28" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="874" y="49" font-size="13" font-weight="bold" fill="#0F172A">6. Контейнеризация и инфраструктура (Infrastructure)</text>

  <rect x="880" y="66" width="410" height="128" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5" />
  <text x="895" y="86" font-size="11.5" font-weight="bold" fill="#0F172A">Docker Compose Orchestration</text>
  <text x="895" y="105" font-size="10" fill="#475569">• flight_tracker_frontend (Nginx Alpine + SPA dist, порт 3000:80)</text>
  <text x="895" y="123" font-size="10" fill="#475569">• flight_tracker_backend (Python 3.12, Django/DRF, порт 8000:8000)</text>
  <text x="895" y="141" font-size="10" fill="#475569">• Изолированная сеть bridge (внутреннее проксирование)</text>
  <text x="895" y="159" font-size="10" fill="#475569">• Постоянный том данных: backend_data:/app/data (SQLite 3)</text>

  <!-- МЕЖУРОВНЕВЫЕ СВЯЗИ -->
  <!-- SPA -> Nginx -->
  <line x1="630" y1="118" x2="630" y2="188" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-blue)" />
  <text x="638" y="150" font-size="10" font-weight="bold" fill="#2563EB">HTTPS / Статика и REST API</text>

  <!-- Nginx -> Django -->
  <line x1="265" y1="240" x2="265" y2="310" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)" />
  <text x="275" y="275" font-size="10" font-weight="bold" fill="#059669">Проксирование /api/ на :8000</text>

  <!-- Django -> ORM -->
  <line x1="215" y1="398" x2="215" y2="470" stroke="#7C3AED" stroke-width="2" marker-end="url(#arrow-purple)" />
  <text x="225" y="435" font-size="10" font-weight="bold" fill="#7C3AED">QuerySet API</text>

  <!-- Django -> Yandex -->
  <path d="M 470 338 L 872 305" fill="none" stroke="#EA580C" stroke-width="1.6" marker-end="url(#arrow-orange)" />
  <text x="560" y="315" font-size="9.5" font-weight="bold" fill="#EA580C">SMTP SSL :465 (Коды 2FA)</text>

  <!-- Engine -> Aviationstack -->
  <path d="M 800 375 L 872 385" fill="none" stroke="#0891B2" stroke-width="1.6" marker-end="url(#arrow-cyan)" />
  <text x="805" y="368" font-size="9.5" font-weight="bold" fill="#0891B2">REST API / HTTPS</text>

  <!-- Docker Compose connections -->
  <path d="M 880 120 L 748 202" fill="none" stroke="#0284C7" stroke-width="1.4" stroke-dasharray="4,4" marker-end="url(#arrow-docker)" />
  <text x="765" y="155" font-size="9" fill="#0284C7">Управление контейнером</text>

  <path d="M 880 155 L 478 325" fill="none" stroke="#0284C7" stroke-width="1.4" stroke-dasharray="4,4" marker-end="url(#arrow-docker)" />
  <text x="580" y="225" font-size="9" fill="#0284C7">Управление контейнером</text>

  <path d="M 1085 194 L 808 505" fill="none" stroke="#0284C7" stroke-width="1.4" stroke-dasharray="4,4" marker-end="url(#arrow-docker)" />
  <text x="885" y="485" font-size="9" fill="#0284C7">Монтирование тома данных backend_data</text>

  <text x="40" y="630" font-size="10" fill="#64748B">Архитектура проекта Flight Tracker. 6 уровней (Tiers) по стандартам РПИ: Клиентский, Шлюз Nginx, Приложения Django, Хранение данных SQLite/ORM, Внешние сервисы, Контейнеризация Docker.</text>
</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Generated SVG: {output_path}")

if __name__ == "__main__":
    generate_drawio_xml()
    generate_architecture_png()
    generate_architecture_svg()
