import os
from PIL import Image, ImageDraw, ImageFont

def generate_drawio_xml(output_path="docs/module_diagram.drawio"):
    xml_content = """<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="24.7.17">
  <diagram id="module-diagram" name="Модульная диаграмма">
    <mxGraphModel dx="1422" dy="880" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1300" pageHeight="1150" background="#FFFFFF" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ================= 1. СЛОЙ ПРЕДСТАВЛЕНИЯ ================= -->
        <mxCell id="layer1" value="1. Слой представления (Presentation Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="80" y="30" width="1140" height="155" as="geometry" />
        </mxCell>
        
        <!-- Модуль страниц -->
        <mxCell id="sub_pages" value="Модуль страниц (Pages)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#3B82F6;fontStyle=1;fontSize=11.5;fontColor=#1D4ED8;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="layer1">
          <mxGeometry x="30" y="38" width="510" height="102" as="geometry" />
        </mxCell>
        <mxCell id="p1" value="&lt;b&gt;HomePage&lt;/b&gt; (Лендинг, промо-блоки, FAQ, Stats)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_pages">
          <mxGeometry x="15" y="32" width="230" height="30" as="geometry" />
        </mxCell>
        <mxCell id="p2" value="&lt;b&gt;FlightsPage / FlightDetailPage&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_pages">
          <mxGeometry x="260" y="32" width="235" height="30" as="geometry" />
        </mxCell>
        <mxCell id="p3" value="&lt;b&gt;AirportsPage / FavoritesPage / UserProfilePage&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_pages">
          <mxGeometry x="15" y="66" width="480" height="28" as="geometry" />
        </mxCell>

        <!-- Модуль UI-компонентов -->
        <mxCell id="sub_ui" value="Модуль UI-компонентов (Components)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2563EB;fontStyle=1;fontSize=11.5;fontColor=#1D4ED8;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="layer1">
          <mxGeometry x="580" y="38" width="530" height="102" as="geometry" />
        </mxCell>
        <mxCell id="ui1" value="&lt;b&gt;Navbar / TopNav / Footer&lt;/b&gt; (Навигация, адаптив)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_ui">
          <mxGeometry x="15" y="32" width="240" height="30" as="geometry" />
        </mxCell>
        <mxCell id="ui2" value="&lt;b&gt;FlightCard / StatusBadge / SearchBar&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_ui">
          <mxGeometry x="270" y="32" width="245" height="30" as="geometry" />
        </mxCell>
        <mxCell id="ui3" value="&lt;b&gt;AuthModal&lt;/b&gt; (Регистрация, 2FA код) / &lt;b&gt;LoadingSkeleton, ErrorState&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_ui">
          <mxGeometry x="15" y="66" width="500" height="28" as="geometry" />
        </mxCell>

        <!-- Связь Pages -> UI -->
        <mxCell id="edge_pages_ui" value="Отображение" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=1.5;fontColor=#1D4ED8;fontSize=10;fontStyle=1;" edge="1" parent="layer1" source="sub_pages" target="sub_ui">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ================= 2. СЛОЙ СОСТОЯНИЯ И ХУКОВ ================= -->
        <mxCell id="layer2" value="2. Слой состояния и хуков (State &amp; Logic Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="80" y="215" width="1140" height="135" as="geometry" />
        </mxCell>
        <mxCell id="box_ctx" value="&lt;b&gt;Глобальное состояние&lt;/b&gt;&lt;br&gt;&lt;b&gt;AuthContext&lt;/b&gt; (Пользователь, JWT/сессия, 2FA статус)&lt;br&gt;&lt;b&gt;LocalStorage&lt;/b&gt; (Кэш авторизации, избранные рейсы)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7C3AED;fontSize=10.5;fontColor=#0F172A;arcSize=6;strokeWidth=1.3;" vertex="1" parent="layer2">
          <mxGeometry x="30" y="42" width="400" height="75" as="geometry" />
        </mxCell>

        <mxCell id="sub_hooks" value="Хуки предметной логики" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7C3AED;fontStyle=1;fontSize=11.5;fontColor=#6D28D9;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="layer2">
          <mxGeometry x="470" y="38" width="640" height="82" as="geometry" />
        </mxCell>
        <mxCell id="h1" value="&lt;b&gt;useFlights&lt;/b&gt; (Каталог, фильтрация, автообновление)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#C4B5FD;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_hooks">
          <mxGeometry x="15" y="34" width="280" height="34" as="geometry" />
        </mxCell>
        <mxCell id="h2" value="&lt;b&gt;useFavorites / useDebounce&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#C4B5FD;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_hooks">
          <mxGeometry x="310" y="34" width="170" height="34" as="geometry" />
        </mxCell>
        <mxCell id="h3" value="&lt;b&gt;useAuth&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#C4B5FD;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_hooks">
          <mxGeometry x="495" y="34" width="130" height="34" as="geometry" />
        </mxCell>

        <!-- ================= 3. СЛОЙ СЕТЕВЫХ СЛУЖБ ================= -->
        <mxCell id="layer3" value="3. Слой сетевых служб (Data Services Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="80" y="380" width="1140" height="135" as="geometry" />
        </mxCell>
        <mxCell id="box_api_client" value="&lt;b&gt;Универсальный сетевой клиент&lt;/b&gt;&lt;br&gt;&lt;b&gt;api.ts&lt;/b&gt; (Axios / Fetch)&lt;br&gt;Базовый URL, перехватчики заголовков, обработка ошибок 401/403/500, fallback-кэш" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#059669;fontSize=10.5;fontColor=#0F172A;arcSize=6;strokeWidth=1.3;" vertex="1" parent="layer3">
          <mxGeometry x="30" y="42" width="400" height="75" as="geometry" />
        </mxCell>

        <mxCell id="sub_services" value="Службы предметных данных" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#059669;fontStyle=1;fontSize=11.5;fontColor=#047857;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="layer3">
          <mxGeometry x="470" y="38" width="640" height="82" as="geometry" />
        </mxCell>
        <mxCell id="s1" value="&lt;b&gt;flightService&lt;/b&gt; (Рейсы, поиск, фильтры)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_services">
          <mxGeometry x="15" y="34" width="200" height="34" as="geometry" />
        </mxCell>
        <mxCell id="s2" value="&lt;b&gt;authApi&lt;/b&gt; (Регистрация, 2FA код, профиль)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_services">
          <mxGeometry x="225" y="34" width="220" height="34" as="geometry" />
        </mxCell>
        <mxCell id="s3" value="&lt;b&gt;airportService&lt;/b&gt; (Хабы, IATA справочник)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_services">
          <mxGeometry x="455" y="34" width="170" height="34" as="geometry" />
        </mxCell>

        <!-- ================= 4. СЛОЙ СЕРВЕРНОЙ ЛОГИКИ ================= -->
        <mxCell id="layer4" value="4. Слой серверной логики (Backend Application Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="80" y="550" width="1140" height="185" as="geometry" />
        </mxCell>
        <mxCell id="box_mid" value="&lt;b&gt;Middleware &amp; Маршрутизация&lt;/b&gt;&lt;br&gt;&lt;b&gt;backend/urls.py&lt;/b&gt; (DefaultRouter)&lt;br&gt;CORS Middleware, JSON Parser, PBKDF2 PasswordHasher" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontSize=10.5;fontColor=#0F172A;arcSize=6;strokeWidth=1.3;" vertex="1" parent="layer4">
          <mxGeometry x="30" y="42" width="400" height="60" as="geometry" />
        </mxCell>

        <mxCell id="sub_routers" value="Контроллеры REST API (ViewSets)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontStyle=1;fontSize=11.5;fontColor=#0369A1;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="layer4">
          <mxGeometry x="470" y="38" width="640" height="80" as="geometry" />
        </mxCell>
        <mxCell id="r1" value="&lt;b&gt;/api/flights&lt;/b&gt; Контроллер&lt;br&gt;(FlightViewSet, Serializers)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F2FE;strokeColor=#BAE6FD;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_routers">
          <mxGeometry x="15" y="32" width="190" height="36" as="geometry" />
        </mxCell>
        <mxCell id="r2" value="&lt;b&gt;/api/auth&lt;/b&gt; Контроллер&lt;br&gt;(AuthViewSet, 2FA Verify)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F2FE;strokeColor=#BAE6FD;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_routers">
          <mxGeometry x="220" y="32" width="200" height="36" as="geometry" />
        </mxCell>
        <mxCell id="r3" value="&lt;b&gt;/api/airports&lt;/b&gt; Контроллер&lt;br&gt;(AirportViewSet)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F2FE;strokeColor=#BAE6FD;fontSize=10;fontColor=#0F172A;" vertex="1" parent="sub_routers">
          <mxGeometry x="435" y="32" width="190" height="36" as="geometry" />
        </mxCell>

        <mxCell id="box_engine" value="&lt;b&gt;Фоновые сервисы движка (services/flight_lifecycle.py)&lt;/b&gt;&lt;br&gt;• Flight Lifecycle Engine 24/7 (симуляция этапов рейсов)&lt;br&gt;• cleanup_archived_flights (очистка архива старше 14 дней)&lt;br&gt;• Генерация и проверка 6-значных кодов подтверждения email" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#D97706;fontSize=10.5;fontColor=#0F172A;arcSize=6;strokeWidth=1.3;" vertex="1" parent="layer4">
          <mxGeometry x="30" y="115" width="1080" height="55" as="geometry" />
        </mxCell>

        <!-- ================= 5. СЛОЙ ДОСТУПА К ДАННЫМ ================= -->
        <mxCell id="layer5" value="5. Слой доступа к базе данных (Database Access Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="80" y="770" width="1140" height="120" as="geometry" />
        </mxCell>
        <mxCell id="box_db_mod" value="&lt;b&gt;Модуль Django ORM (models.py / QuerySet API)&lt;/b&gt;&lt;br&gt;Объектно-реляционное отображение, валидация полей, транзакции, миграции схем" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7C3AED;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;" vertex="1" parent="layer5">
          <mxGeometry x="40" y="45" width="480" height="55" as="geometry" />
        </mxCell>
        <mxCell id="box_db_store" value="&lt;b&gt;SQLite 3 СУБД (db.sqlite3)&lt;/b&gt;&lt;br&gt;Реляционная СУБД (flights, airports, user_profile, verification_codes)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#FFFFFF;strokeColor=#DC2626;fontSize=11;fontColor=#0F172A;strokeWidth=1.5;" vertex="1" parent="layer5">
          <mxGeometry x="610" y="38" width="490" height="68" as="geometry" />
        </mxCell>
        <mxCell id="edge_orm_store" value="Синхронный in-process SQL доступ (CRUD)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.8;fontColor=#6D28D9;fontSize=10.5;fontStyle=1;" edge="1" parent="layer5" source="box_db_mod" target="box_db_store">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ================= МЕЖСЛОЙНЫЕ СВЯЗИ СВЕРХУ ВНИЗ ================= -->
        <!-- Pages -> Context -->
        <mxCell id="edge_p_ctx" value="Подписка на состояние" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.5;fontColor=#6D28D9;fontSize=10;exitX=0.25;exitY=1;exitDx=0;exitDy=0;entryX=0.35;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="sub_pages" target="box_ctx">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Pages -> Hooks -->
        <mxCell id="edge_p_hooks" value="Вызов хуков" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3B82F6;strokeWidth=1.5;fontColor=#1D4ED8;fontSize=10;exitX=0.75;exitY=1;exitDx=0;exitDy=0;entryX=0.2;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="sub_pages" target="sub_hooks">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Hooks -> Services -->
        <mxCell id="edge_hooks_svc" value="Делегирование запросов" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.5;fontColor=#6D28D9;fontSize=10;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="sub_hooks" target="sub_services">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Services -> API Client -->
        <mxCell id="edge_svc_client" value="Вызов сетевого клиента" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=1.5;fontColor=#047857;fontSize=10;exitX=0.1;exitY=1;exitDx=0;exitDy=0;entryX=0.8;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="layer3" source="sub_services" target="box_api_client">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="534" y="125" />
              <mxPoint x="350" y="125" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- API Client -> Middleware (HTTP REST JSON) -->
        <mxCell id="edge_client_mid" value="HTTP REST JSON (/api/)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2;fontColor=#065F46;fontSize=11;fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_api_client" target="box_mid">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Middleware -> Routers -->
        <mxCell id="edge_mid_routers" value="Маршрутизация" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284C7;strokeWidth=1.5;fontColor=#0369A1;fontSize=10;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="layer4" source="box_mid" target="sub_routers">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Routers -> ORM -->
        <mxCell id="edge_routers_orm" value="QuerySet API вызовы" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.8;fontColor=#6D28D9;fontSize=10.5;fontStyle=1;exitX=0.3;exitY=1;exitDx=0;exitDy=0;entryX=0.65;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="sub_routers" target="box_db_mod">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Engine -> ORM -->
        <mxCell id="edge_engine_orm" value="Обновление статусов и очистка архива" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D97706;strokeWidth=1.5;fontColor=#B45309;fontSize=10;exitX=0.3;exitY=1;exitDx=0;exitDy=0;entryX=0.3;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="box_engine" target="box_db_mod">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content.strip())
    print(f"Generated draw.io XML: {output_path}")

def generate_module_png(output_path="docs/module_diagram.png"):
    scale = 2
    w, h = 1300 * scale, 1000 * scale

    img = Image.new("RGB", (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_path = "C:/Windows/Fonts/arial.ttf"
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"

    font_layer_title = ImageFont.truetype(font_bold_path, 12 * scale)
    font_sub_title = ImageFont.truetype(font_bold_path, 10.5 * scale)
    font_box_title = ImageFont.truetype(font_bold_path, 10 * scale)
    font_box_text = ImageFont.truetype(font_path, 9 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 8.5 * scale)
    font_note = ImageFont.truetype(font_path, 8 * scale)

    def S(v):
        return int(v * scale)

    def draw_layer(x, y, lw, lh, title, bg="#F8FAFC", border="#64748B"):
        draw.rectangle([S(x), S(y), S(x + lw), S(y + lh)], fill=bg, outline=border, width=S(1.4))
        draw.rectangle([S(x), S(y), S(x + lw), S(y + 26)], fill="#FFFFFF", outline=border, width=S(1.4))
        draw.text((S(x + 14), S(y + 5)), title, font=font_layer_title, fill="#0F172A")

    def draw_sub(x, y, sw, sh, title, bg="#FFFFFF", border="#2563EB"):
        draw.rectangle([S(x), S(y), S(x + sw), S(y + sh)], fill=bg, outline=border, width=S(1.2))
        draw.rectangle([S(x), S(y), S(x + sw), S(y + 22)], fill="#F8FAFC", outline=border, width=S(1.2))
        draw.text((S(x + 10), S(y + 4)), title, font=font_sub_title, fill="#1E3A8A")

    def draw_box(x, y, bw, bh, title, lines=[], bg="#FFFFFF", border="#334155", bwidth=1.2):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill=bg, outline=border, width=S(bwidth))
        draw.text((S(x + 8), S(y + 6)), title, font=font_box_title, fill="#0F172A")
        cur_y = y + 22
        for line in lines:
            draw.text((S(x + 8), S(cur_y)), line, font=font_box_text, fill="#334155")
            cur_y += 14

    def draw_cylinder(x, y, bw, bh, title, lines=[], bg="#FFFFFF", border="#DC2626"):
        draw.rectangle([S(x), S(y + 8), S(x + bw), S(y + bh)], fill=bg, outline=border, width=S(1.4))
        draw.ellipse([S(x), S(y), S(x + bw), S(y + 16)], fill="#FEE2E2", outline=border, width=S(1.4))
        draw.text((S(x + 12), S(y + 18)), title, font=font_box_title, fill="#991B1B")
        cur_y = y + 36
        for line in lines:
            draw.text((S(x + 12), S(cur_y)), line, font=font_box_text, fill="#334155")
            cur_y += 14

    def draw_arrow(p1, p2, label=None, label_pos=None, color="#2563EB", width=1.6):
        x1, y1 = p1
        x2, y2 = p2
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
            left = (S(x2 - ux * 7 + vx * 3.5), S(y2 - uy * 7 + vy * 3.5))
            right = (S(x2 - ux * 7 - vx * 3.5), S(y2 - uy * 7 - vy * 3.5))
            draw.polygon([tip, left, right], fill=color)

        if label:
            lx, ly = label_pos if label_pos else ((x1 + x2)/2, (y1 + y2)/2 - 10)
            draw.text((S(lx), S(ly)), label, font=font_arrow, fill=color)

    # 1. СЛОЙ ПРЕДСТАВЛЕНИЯ
    draw_layer(50, 30, 1200, 140, "1. Слой представления (Presentation Layer)")
    draw_sub(70, 65, 520, 95, "Модуль страниц (Pages)")
    draw_box(85, 93, 230, 26, "HomePage (Лендинг, промо, FAQ)", [], "#F1F5F9", "#94A3B8")
    draw_box(330, 93, 245, 26, "FlightsPage / FlightDetailPage", [], "#F1F5F9", "#94A3B8")
    draw_box(85, 125, 490, 26, "AirportsPage / FavoritesPage / UserProfilePage", [], "#F1F5F9", "#94A3B8")

    draw_sub(670, 65, 560, 95, "Модуль UI-компонентов (Components)")
    draw_box(685, 93, 250, 26, "Navbar / TopNav / Footer (Навигация)", [], "#F1F5F9", "#94A3B8")
    draw_box(950, 93, 265, 26, "FlightCard / StatusBadge / SearchBar", [], "#F1F5F9", "#94A3B8")
    draw_box(685, 125, 530, 26, "AuthModal (Регистрация, 2FA код) / LoadingSkeleton, ErrorState", [], "#F1F5F9", "#94A3B8")

    draw_arrow((590, 112), (670, 112), "Отображение", (598, 98), "#2563EB")

    # 2. СЛОЙ СОСТОЯНИЯ И ХУКОВ
    draw_layer(50, 200, 1200, 125, "2. Слой состояния и хуков (State & Logic Layer)")
    draw_box(70, 235, 420, 78, "Глобальное состояние (State)", [
        "• AuthContext (Пользователь, сессия, 2FA статус)",
        "• LocalStorage (Кэш авторизации, избранные рейсы)",
        "• React Router v7 (Диспетчеризация маршрутов)",
    ], "#FFFFFF", "#7C3AED", 1.4)

    draw_sub(530, 235, 700, 78, "Хуки предметной логики")
    draw_box(545, 265, 270, 38, "useFlights", ["Каталог, фильтры, автообновление"], "#F5F3FF", "#C4B5FD")
    draw_box(830, 265, 220, 38, "useFavorites / useDebounce", ["Избранное, отложенный ввод"], "#F5F3FF", "#C4B5FD")
    draw_box(1065, 265, 150, 38, "useAuth", ["Сессия, токен, 2FA"], "#F5F3FF", "#C4B5FD")

    # 3. СЛОЙ СЕТЕВЫХ СЛУЖБ
    draw_layer(50, 355, 1200, 125, "3. Слой сетевых служб (Data Services Layer)")
    draw_box(70, 390, 420, 78, "Универсальный сетевой клиент", [
        "• api.ts (Axios / Fetch экземпляр)",
        "• Базовый URL, перехватчики заголовков (headers)",
        "• Обработка ошибок 401/403/500, fallback-кэш",
    ], "#FFFFFF", "#059669", 1.4)

    draw_sub(530, 390, 700, 78, "Службы предметных данных")
    draw_box(545, 420, 210, 38, "flightService", ["Поиск, фильтры, детали рейса"], "#ECFDF5", "#A7F3D0")
    draw_box(770, 420, 230, 38, "authApi", ["Регистрация, 2FA код, вход"], "#ECFDF5", "#A7F3D0")
    draw_box(1015, 420, 200, 38, "airportService", ["Хабы, IATA справочник"], "#ECFDF5", "#A7F3D0")

    # 4. СЛОЙ СЕРВЕРНОЙ ЛОГИКИ
    draw_layer(50, 510, 1200, 185, "4. Слой серверной логики (Backend Application Layer)")
    draw_box(70, 545, 420, 65, "Middleware & Маршрутизация", [
        "• backend/urls.py (DefaultRouter)",
        "• CORS Middleware, Django JSON Parser",
        "• Безопасность: PBKDF2-SHA256, сессии",
    ], "#FFFFFF", "#0284C7", 1.4)

    draw_sub(530, 545, 700, 65, "Контроллеры REST API (ViewSets)")
    draw_box(545, 572, 210, 32, "/api/flights Контроллер", ["(FlightViewSet, Serializers)"], "#E0F2FE", "#BAE6FD")
    draw_box(770, 572, 230, 32, "/api/auth Контроллер", ["(AuthViewSet, 2FA Verify)"], "#E0F2FE", "#BAE6FD")
    draw_box(1015, 572, 200, 32, "/api/airports Контроллер", ["(AirportViewSet)"], "#E0F2FE", "#BAE6FD")

    draw_box(70, 622, 1160, 60, "Фоновые сервисы движка (services/flight_lifecycle.py)", [
        "• Flight Lifecycle Engine 24/7 (динамическая симуляция этапов рейсов: Scheduled -> Boarding -> Departed -> En Route -> Landed -> Arrived)",
        "• cleanup_archived_flights (очистка архивных рейсов старше 14 дней), генератор и валидатор 6-значных 2FA кодов",
    ], "#FFFFFF", "#D97706", 1.4)

    # 5. СЛОЙ ДОСТУПА К ДАННЫМ
    draw_layer(50, 725, 1200, 120, "5. Слой доступа к базе данных (Database Access Layer)")
    draw_box(70, 760, 480, 70, "Модуль Django ORM (models.py / QuerySet API)", [
        "• Объектно-реляционное отображение (ORM)",
        "• Защита от прямых SQL-инъекций, транзакции atomic",
        "• Управление схемами и миграциями данных",
    ], "#FFFFFF", "#7C3AED", 1.5)

    draw_cylinder(630, 750, 600, 80, "SQLite 3 СУБД (db.sqlite3)", [
        "• Встроенная реляционная база данных (DatabaseSync)",
        "• Таблицы: flights, airports, user_profile, email_verification_code",
    ], "#FFFFFF", "#DC2626")

    draw_arrow((550, 795), (630, 795), "Синхронный in-process SQL доступ", (540, 780), "#7C3AED")

    # ВЕРТИКАЛЬНЫЕ СВЯЗИ
    # Pages -> Context
    draw_arrow((200, 160), (200, 235), "Подписка на состояние", (208, 185), "#7C3AED")
    # Pages -> Hooks
    draw_arrow((450, 160), (600, 235), "Вызов хуков", (510, 185), "#3B82F6")
    # Hooks -> Services
    draw_arrow((880, 313), (880, 390), "Делегирование запросов", (888, 345), "#7C3AED")
    # Services -> API Client
    draw_arrow((530, 435), (490, 435), "Вызов клиента", (475, 418), "#059669")
    # API Client -> Middleware (HTTP REST JSON)
    draw_arrow((280, 468), (280, 545), "HTTP REST JSON (/api/)", (288, 500), "#059669")
    # Middleware -> Routers
    draw_arrow((490, 577), (530, 577), "Роутинг", (485, 562), "#0284C7")
    # Routers -> ORM
    draw_arrow((700, 610), (350, 760), "QuerySet API вызовы", (530, 705), "#7C3AED")
    # Engine -> ORM
    draw_arrow((300, 682), (300, 760), "ORM CRUD", (308, 715), "#D97706")

    draw.text((S(50), S(875)), "Модульная диаграмма программного комплекса Flight Tracker (РПИ). 5-слойная модульная архитектура: Представление -> Состояние/Хуки -> Сетевые службы -> Серверная логика -> База данных.", font=font_note, fill="#64748B")

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Generated 300 DPI PNG: {output_path}")

def generate_module_svg(output_path="docs/module_diagram.svg"):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 920" width="100%" height="100%" style="background:#FFFFFF; font-family: Arial, sans-serif;">
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563EB" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#7C3AED" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arrow-sky" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7" />
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#D97706" />
    </marker>
  </defs>

  <!-- 1. СЛОЙ ПРЕДСТАВЛЕНИЯ -->
  <rect x="50" y="30" width="1200" height="140" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="30" width="1200" height="26" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="64" y="48" font-size="12" font-weight="bold" fill="#0F172A">1. Слой представления (Presentation Layer)</text>

  <rect x="70" y="65" width="520" height="95" rx="4" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.2" />
  <rect x="70" y="65" width="520" height="22" rx="4" fill="#F8FAFC" stroke="#2563EB" stroke-width="1.2" />
  <text x="80" y="80" font-size="11" font-weight="bold" fill="#1D4ED8">Модуль страниц (Pages)</text>
  <rect x="85" y="93" width="230" height="26" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="95" y="110" font-size="10" font-weight="bold" fill="#0F172A">HomePage (Лендинг, промо, FAQ)</text>
  <rect x="330" y="93" width="245" height="26" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="340" y="110" font-size="10" font-weight="bold" fill="#0F172A">FlightsPage / FlightDetailPage</text>
  <rect x="85" y="125" width="490" height="26" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="95" y="142" font-size="10" font-weight="bold" fill="#0F172A">AirportsPage / FavoritesPage / UserProfilePage</text>

  <rect x="670" y="65" width="560" height="95" rx="4" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.2" />
  <rect x="670" y="65" width="560" height="22" rx="4" fill="#F8FAFC" stroke="#2563EB" stroke-width="1.2" />
  <text x="680" y="80" font-size="11" font-weight="bold" fill="#1D4ED8">Модуль UI-компонентов (Components)</text>
  <rect x="685" y="93" width="250" height="26" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="695" y="110" font-size="10" font-weight="bold" fill="#0F172A">Navbar / TopNav / Footer (Навигация)</text>
  <rect x="950" y="93" width="265" height="26" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="960" y="110" font-size="10" font-weight="bold" fill="#0F172A">FlightCard / StatusBadge / SearchBar</text>
  <rect x="685" y="125" width="530" height="26" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="695" y="142" font-size="10" font-weight="bold" fill="#0F172A">AuthModal (Регистрация, 2FA код) / LoadingSkeleton, ErrorState</text>

  <line x1="590" y1="112" x2="662" y2="112" stroke="#2563EB" stroke-width="1.5" marker-end="url(#arrow-blue)" />
  <text x="598" y="105" font-size="9.5" font-weight="bold" fill="#2563EB">Отображение</text>

  <!-- 2. СЛОЙ СОСТОЯНИЯ И ХУКОВ -->
  <rect x="50" y="200" width="1200" height="125" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="200" width="1200" height="26" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="64" y="218" font-size="12" font-weight="bold" fill="#0F172A">2. Слой состояния и хуков (State &amp; Logic Layer)</text>

  <rect x="70" y="235" width="420" height="78" rx="4" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.4" />
  <text x="82" y="254" font-size="11" font-weight="bold" fill="#0F172A">Глобальное состояние (State)</text>
  <text x="82" y="271" font-size="9.5" fill="#334155">• AuthContext (Пользователь, JWT/сессия, 2FA статус)</text>
  <text x="82" y="287" font-size="9.5" fill="#334155">• LocalStorage (Кэш авторизации, избранные рейсы)</text>
  <text x="82" y="303" font-size="9.5" fill="#334155">• React Router v7 (Диспетчеризация маршрутов)</text>

  <rect x="530" y="235" width="700" height="78" rx="4" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.2" />
  <rect x="530" y="235" width="700" height="22" rx="4" fill="#F8FAFC" stroke="#7C3AED" stroke-width="1.2" />
  <text x="540" y="250" font-size="11" font-weight="bold" fill="#6D28D9">Хуки предметной логики</text>
  <rect x="545" y="265" width="270" height="38" rx="3" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1" />
  <text x="555" y="281" font-size="10" font-weight="bold" fill="#0F172A">useFlights</text>
  <text x="555" y="295" font-size="9" fill="#475569">Каталог, фильтры, автообновление</text>

  <rect x="830" y="265" width="220" height="38" rx="3" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1" />
  <text x="840" y="281" font-size="10" font-weight="bold" fill="#0F172A">useFavorites / useDebounce</text>
  <text x="840" y="295" font-size="9" fill="#475569">Избранное, отложенный ввод</text>

  <rect x="1065" y="265" width="150" height="38" rx="3" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1" />
  <text x="1075" y="281" font-size="10" font-weight="bold" fill="#0F172A">useAuth</text>
  <text x="1075" y="295" font-size="9" fill="#475569">Сессия, токен, 2FA</text>

  <!-- 3. СЛОЙ СЕТЕВЫХ СЛУЖБ -->
  <rect x="50" y="355" width="1200" height="125" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="355" width="1200" height="26" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="64" y="373" font-size="12" font-weight="bold" fill="#0F172A">3. Слой сетевых служб (Data Services Layer)</text>

  <rect x="70" y="390" width="420" height="78" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="1.4" />
  <text x="82" y="409" font-size="11" font-weight="bold" fill="#0F172A">Универсальный сетевой клиент</text>
  <text x="82" y="426" font-size="9.5" fill="#334155">• api.ts (Axios / Fetch экземпляр)</text>
  <text x="82" y="442" font-size="9.5" fill="#334155">• Базовый URL, перехватчики заголовков (headers)</text>
  <text x="82" y="458" font-size="9.5" fill="#334155">• Обработка ошибок 401/403/500, fallback-кэш</text>

  <rect x="530" y="390" width="700" height="78" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="1.2" />
  <rect x="530" y="390" width="700" height="22" rx="4" fill="#F8FAFC" stroke="#059669" stroke-width="1.2" />
  <text x="540" y="405" font-size="11" font-weight="bold" fill="#047857">Службы предметных данных</text>

  <rect x="545" y="420" width="210" height="38" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="555" y="436" font-size="10" font-weight="bold" fill="#0F172A">flightService</text>
  <text x="555" y="450" font-size="9" fill="#475569">Поиск, фильтры, детали рейса</text>

  <rect x="770" y="420" width="230" height="38" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="780" y="436" font-size="10" font-weight="bold" fill="#0F172A">authApi</text>
  <text x="780" y="450" font-size="9" fill="#475569">Регистрация, 2FA код, вход</text>

  <rect x="1015" y="420" width="200" height="38" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="1025" y="436" font-size="10" font-weight="bold" fill="#0F172A">airportService</text>
  <text x="1025" y="450" font-size="9" fill="#475569">Хабы, IATA справочник</text>

  <!-- 4. СЛОЙ СЕРВЕРНОЙ ЛОГИКИ -->
  <rect x="50" y="510" width="1200" height="185" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="510" width="1200" height="26" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="64" y="528" font-size="12" font-weight="bold" fill="#0F172A">4. Слой серверной логики (Backend Application Layer)</text>

  <rect x="70" y="545" width="420" height="65" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.4" />
  <text x="82" y="564" font-size="11" font-weight="bold" fill="#0F172A">Middleware &amp; Маршрутизация</text>
  <text x="82" y="581" font-size="9.5" fill="#334155">• backend/urls.py (DefaultRouter)</text>
  <text x="82" y="597" font-size="9.5" fill="#334155">• CORS Middleware, Django JSON Parser, PBKDF2</text>

  <rect x="530" y="545" width="700" height="65" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" />
  <rect x="530" y="545" width="700" height="22" rx="4" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.2" />
  <text x="540" y="560" font-size="11" font-weight="bold" fill="#0369A1">Контроллеры REST API (ViewSets)</text>

  <rect x="545" y="572" width="210" height="32" rx="3" fill="#E0F2FE" stroke="#BAE6FD" stroke-width="1" />
  <text x="555" y="587" font-size="9.5" font-weight="bold" fill="#0F172A">/api/flights Контроллер</text>
  <text x="555" y="599" font-size="8.5" fill="#475569">(FlightViewSet, Serializers)</text>

  <rect x="770" y="572" width="230" height="32" rx="3" fill="#E0F2FE" stroke="#BAE6FD" stroke-width="1" />
  <text x="780" y="587" font-size="9.5" font-weight="bold" fill="#0F172A">/api/auth Контроллер</text>
  <text x="780" y="599" font-size="8.5" fill="#475569">(AuthViewSet, 2FA Verify)</text>

  <rect x="1015" y="572" width="200" height="32" rx="3" fill="#E0F2FE" stroke="#BAE6FD" stroke-width="1" />
  <text x="1025" y="587" font-size="9.5" font-weight="bold" fill="#0F172A">/api/airports Контроллер</text>
  <text x="1025" y="599" font-size="8.5" fill="#475569">(AirportViewSet)</text>

  <rect x="70" y="622" width="1160" height="60" rx="4" fill="#FFFFFF" stroke="#D97706" stroke-width="1.4" />
  <text x="82" y="641" font-size="11" font-weight="bold" fill="#92400E">Фоновые сервисы движка (services/flight_lifecycle.py)</text>
  <text x="82" y="658" font-size="9.5" fill="#334155">• Flight Lifecycle Engine 24/7 (симуляция этапов рейсов: Scheduled -> Boarding -> Departed -> En Route -> Landed -> Arrived)</text>
  <text x="82" y="673" font-size="9.5" fill="#334155">• cleanup_archived_flights (очистка архивных рейсов старше 14 дней), генератор и валидатор 6-значных 2FA кодов</text>

  <!-- 5. СЛОЙ ДОСТУПА К ДАННЫМ -->
  <rect x="50" y="725" width="1200" height="120" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="725" width="1200" height="26" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="64" y="743" font-size="12" font-weight="bold" fill="#0F172A">5. Слой доступа к базе данных (Database Access Layer)</text>

  <rect x="70" y="760" width="480" height="70" rx="4" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.5" />
  <text x="82" y="779" font-size="11" font-weight="bold" fill="#0F172A">Модуль Django ORM (models.py / QuerySet API)</text>
  <text x="82" y="796" font-size="9.5" fill="#334155">• Объектно-реляционное отображение (ORM)</text>
  <text x="82" y="812" font-size="9.5" fill="#334155">• Защита от прямых SQL-инъекций, транзакции atomic</text>
  <text x="82" y="826" font-size="9.5" fill="#334155">• Управление схемами и миграциями данных</text>

  <path d="M 630 765 C 630 755, 1230 755, 1230 765 L 1230 820 C 1230 830, 630 830, 630 820 Z" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.5" />
  <path d="M 630 765 C 630 775, 1230 775, 1230 765" fill="none" stroke="#DC2626" stroke-width="1.5" />
  <text x="650" y="785" font-size="11" font-weight="bold" fill="#991B1B">SQLite 3 СУБД (db.sqlite3)</text>
  <text x="650" y="802" font-size="9.5" fill="#334155">• Встроенная реляционная база данных (DatabaseSync)</text>
  <text x="650" y="818" font-size="9.5" fill="#475569">Таблицы: flights, airports, user_profile, email_verification_code</text>

  <line x1="550" y1="795" x2="622" y2="795" stroke="#7C3AED" stroke-width="1.6" marker-end="url(#arrow-purple)" />
  <text x="555" y="787" font-size="9" font-weight="bold" fill="#7C3AED">SQL доступ</text>

  <!-- МЕЖСЛОЙНЫЕ СВЯЗИ СВЕРХУ ВНИЗ -->
  <line x1="200" y1="160" x2="200" y2="228" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arrow-purple)" />
  <text x="208" y="195" font-size="9" font-weight="bold" fill="#7C3AED">Подписка на состояние</text>

  <line x1="450" y1="160" x2="595" y2="230" stroke="#2563EB" stroke-width="1.5" marker-end="url(#arrow-blue)" />
  <text x="510" y="195" font-size="9" font-weight="bold" fill="#2563EB">Вызов хуков</text>

  <line x1="880" y1="313" x2="880" y2="382" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arrow-purple)" />
  <text x="888" y="350" font-size="9" font-weight="bold" fill="#7C3AED">Делегирование запросов</text>

  <line x1="530" y1="435" x2="498" y2="435" stroke="#059669" stroke-width="1.5" marker-end="url(#arrow-green)" />
  <text x="500" y="425" font-size="8.5" font-weight="bold" fill="#059669">Вызов</text>

  <line x1="280" y1="468" x2="280" y2="538" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)" />
  <text x="288" y="505" font-size="10" font-weight="bold" fill="#059669">HTTP REST JSON (/api/)</text>

  <line x1="490" y1="577" x2="522" y2="577" stroke="#0284C7" stroke-width="1.5" marker-end="url(#arrow-sky)" />
  <text x="495" y="570" font-size="8.5" font-weight="bold" fill="#0284C7">Роутинг</text>

  <line x1="700" y1="610" x2="350" y2="752" stroke="#7C3AED" stroke-width="1.8" marker-end="url(#arrow-purple)" />
  <text x="530" y="705" font-size="9.5" font-weight="bold" fill="#7C3AED">QuerySet API вызовы</text>

  <line x1="300" y1="682" x2="300" y2="752" stroke="#D97706" stroke-width="1.5" marker-end="url(#arrow-orange)" />
  <text x="308" y="720" font-size="9" font-weight="bold" fill="#D97706">ORM CRUD</text>

  <text x="50" y="875" font-size="9.5" fill="#64748B">Модульная диаграмма веб-сервиса Flight Tracker. 5 слоев по стандартам РПИ: Представление -> Состояние/Хуки -> Сетевые службы -> Серверная логика -> База данных.</text>
</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Generated SVG: {output_path}")

if __name__ == "__main__":
    generate_drawio_xml()
    generate_module_png()
    generate_module_svg()

