import os
from PIL import Image, ImageDraw, ImageFont

def generate_drawio_xml(output_path="docs/module_diagram.drawio"):
    xml_content = """<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="24.7.17">
  <diagram id="module-diagram" name="Модульная диаграмма">
    <mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="950" pageHeight="1100" background="#FFFFFF" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ================= 1. СЛОЙ ПРЕДСТАВЛЕНИЯ ================= -->
        <mxCell id="LAYER_PRES" value="1. Слой представления (Presentation Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="30" width="820" height="150" as="geometry" />
        </mxCell>

        <!-- Модуль страниц (Pages) -->
        <mxCell id="MOD_PAGES" value="Модуль страниц (Pages)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#3B82F6;fontStyle=1;fontSize=11.5;fontColor=#1D4ED8;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="LAYER_PRES">
          <mxGeometry x="25" y="38" width="350" height="98" as="geometry" />
        </mxCell>
        <mxCell id="P_HOME" value="HomePage / LandingPage" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_PAGES">
          <mxGeometry x="15" y="30" width="320" height="20" as="geometry" />
        </mxCell>
        <mxCell id="P_FLIGHTS" value="FlightsPage / FlightDetailPage" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_PAGES">
          <mxGeometry x="15" y="52" width="320" height="20" as="geometry" />
        </mxCell>
        <mxCell id="P_EXTRA" value="AirportsPage / FavoritesPage / ProfilePage" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_PAGES">
          <mxGeometry x="15" y="74" width="320" height="20" as="geometry" />
        </mxCell>

        <!-- Модуль UI-компонентов (Components) -->
        <mxCell id="MOD_UI" value="Модуль UI-компонентов (Components)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#3B82F6;fontStyle=1;fontSize=11.5;fontColor=#1D4ED8;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="LAYER_PRES">
          <mxGeometry x="440" y="38" width="355" height="98" as="geometry" />
        </mxCell>
        <mxCell id="UI_NAV" value="Navbar / Footer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_UI">
          <mxGeometry x="15" y="30" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="UI_CARD" value="FlightCard / Filters / SearchBar" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_UI">
          <mxGeometry x="15" y="52" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="UI_MODAL" value="AuthModal / VerifyCodeModal" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_UI">
          <mxGeometry x="15" y="74" width="325" height="20" as="geometry" />
        </mxCell>

        <!-- MOD_PAGES -> MOD_UI -->
        <mxCell id="edge_pages_ui" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=1.5;" edge="1" parent="LAYER_PRES" source="MOD_PAGES" target="MOD_UI">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ================= 2. СЛОЙ СОСТОЯНИЯ И ХУКОВ ================= -->
        <mxCell id="LAYER_STATE" value="2. Слой состояния и хуков (State &amp; Logic Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="215" width="820" height="150" as="geometry" />
        </mxCell>

        <mxCell id="CTX" value="Глобальное состояние (AuthContext / Favorites)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7C3AED;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="LAYER_STATE">
          <mxGeometry x="25" y="58" width="350" height="55" as="geometry" />
        </mxCell>

        <!-- Хуки предметной логики -->
        <mxCell id="MOD_HOOKS" value="Хуки предметной логики" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7C3AED;fontStyle=1;fontSize=11.5;fontColor=#6D28D9;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="LAYER_STATE">
          <mxGeometry x="440" y="38" width="355" height="98" as="geometry" />
        </mxCell>
        <mxCell id="H_FLIGHTS" value="useFlights (Каталог и фильтрация)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#C4B5FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_HOOKS">
          <mxGeometry x="15" y="30" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="H_FLIGHT" value="useFlight (Детальная информация)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#C4B5FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_HOOKS">
          <mxGeometry x="15" y="52" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="H_AUTH" value="useAuth (Авторизация и 2FA)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#C4B5FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_HOOKS">
          <mxGeometry x="15" y="74" width="325" height="20" as="geometry" />
        </mxCell>

        <!-- ================= 3. СЛОЙ СЕТЕВЫХ СЛУЖБ ================= -->
        <mxCell id="LAYER_SVC" value="3. Слой сетевых служб (Data Services Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="400" width="820" height="150" as="geometry" />
        </mxCell>

        <mxCell id="API_CLIENT" value="Универсальный сетевой клиент (api.ts)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#059669;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="LAYER_SVC">
          <mxGeometry x="25" y="58" width="350" height="55" as="geometry" />
        </mxCell>

        <!-- Службы предметных данных -->
        <mxCell id="MOD_SVC" value="Службы предметных данных" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#059669;fontStyle=1;fontSize=11.5;fontColor=#047857;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="LAYER_SVC">
          <mxGeometry x="440" y="38" width="355" height="98" as="geometry" />
        </mxCell>
        <mxCell id="S_FLIGHT" value="flightService" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10.5;fontColor=#0F172A;fontStyle=1;" vertex="1" parent="MOD_SVC">
          <mxGeometry x="15" y="30" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="S_AUTH" value="authService" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10.5;fontColor=#0F172A;fontStyle=1;" vertex="1" parent="MOD_SVC">
          <mxGeometry x="15" y="52" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="S_AIRPORT" value="airportService" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#A7F3D0;fontSize=10.5;fontColor=#0F172A;fontStyle=1;" vertex="1" parent="MOD_SVC">
          <mxGeometry x="15" y="74" width="325" height="20" as="geometry" />
        </mxCell>

        <!-- ================= 4. СЛОЙ СЕРВЕРНОЙ ЛОГИКИ ================= -->
        <mxCell id="LAYER_BE" value="4. Слой серверной логики (Backend Application Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="585" width="820" height="150" as="geometry" />
        </mxCell>

        <mxCell id="MID" value="Middleware (CORS, Django JSON Parser)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="LAYER_BE">
          <mxGeometry x="25" y="58" width="350" height="55" as="geometry" />
        </mxCell>

        <!-- Контроллеры REST API -->
        <mxCell id="MOD_ROUTERS" value="Контроллеры REST API (backend/urls.py)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#0284C7;fontStyle=1;fontSize=11.5;fontColor=#0369A1;startSize=26;rounded=1;arcSize=6;" vertex="1" parent="LAYER_BE">
          <mxGeometry x="440" y="38" width="355" height="98" as="geometry" />
        </mxCell>
        <mxCell id="R_FLIGHTS" value="/api/flights Контроллер" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F2FE;strokeColor=#BAE6FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_ROUTERS">
          <mxGeometry x="15" y="30" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="R_AIRPORTS" value="/api/airports Контроллер" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F2FE;strokeColor=#BAE6FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_ROUTERS">
          <mxGeometry x="15" y="52" width="325" height="20" as="geometry" />
        </mxCell>
        <mxCell id="R_AUTH" value="/api/auth Контроллер" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F2FE;strokeColor=#BAE6FD;fontSize=10.5;fontColor=#0F172A;" vertex="1" parent="MOD_ROUTERS">
          <mxGeometry x="15" y="74" width="325" height="20" as="geometry" />
        </mxCell>

        <!-- ================= 5. СЛОЙ ДОСТУПА К ДАННЫМ ================= -->
        <mxCell id="LAYER_DATA" value="5. Слой доступа к базе данных (Database Access Layer)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;fontSize=13;fontColor=#0F172A;startSize=28;rounded=1;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="60" y="770" width="820" height="130" as="geometry" />
        </mxCell>

        <mxCell id="DB_MOD" value="Модуль базы данных (Django ORM / models.py)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7C3AED;fontSize=11;fontColor=#0F172A;arcSize=6;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="LAYER_DATA">
          <mxGeometry x="25" y="48" width="350" height="55" as="geometry" />
        </mxCell>

        <mxCell id="DB_STORE" value="SQLite 3 СУБД (flights.db)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#FFFFFF;strokeColor=#DC2626;fontSize=11;fontColor=#0F172A;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="LAYER_DATA">
          <mxGeometry x="440" y="42" width="355" height="66" as="geometry" />
        </mxCell>

        <!-- ================= МЕЖСЛОЙНЫЕ СВЯЗИ СВЕРХУ ВНИЗ ================= -->
        <!-- MOD_PAGES --> CTX -->
        <mxCell id="edge_pages_ctx" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;exitX=0.25;exitY=1;exitDx=0;exitDy=0;entryX=0.25;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="MOD_PAGES" target="CTX">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- MOD_PAGES --> MOD_HOOKS -->
        <mxCell id="edge_pages_hooks" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;exitX=0.75;exitY=1;exitDx=0;exitDy=0;entryX=0.25;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="MOD_PAGES" target="MOD_HOOKS">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- MOD_HOOKS --> MOD_SVC -->
        <mxCell id="edge_hooks_svc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="MOD_HOOKS" target="MOD_SVC">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- MOD_SVC --> API_CLIENT -->
        <mxCell id="edge_svc_client" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;exitX=0.2;exitY=1;exitDx=0;exitDy=0;entryX=0.8;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="1" source="MOD_SVC" target="API_CLIENT">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="571" y="538" />
              <mxPoint x="365" y="538" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- API_CLIENT -->|HTTP REST JSON| MID -->
        <mxCell id="edge_client_mid" value="HTTP REST JSON" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=1.8;fontColor=#065F46;fontSize=10;fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="API_CLIENT" target="MID">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- MID --> MOD_ROUTERS -->
        <mxCell id="edge_mid_routers" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="MID" target="MOD_ROUTERS">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- MOD_ROUTERS --> DB_MOD -->
        <mxCell id="edge_routers_dbmod" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;exitX=0.3;exitY=1;exitDx=0;exitDy=0;entryX=0.7;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="MOD_ROUTERS" target="DB_MOD">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- DB_MOD --> DB_STORE -->
        <mxCell id="edge_dbmod_store" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="DB_MOD" target="DB_STORE">
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
    w, h = 950 * scale, 950 * scale

    img = Image.new("RGB", (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_path = "C:/Windows/Fonts/arial.ttf"
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"

    font_layer_title = ImageFont.truetype(font_bold_path, 11.5 * scale)
    font_sub_title = ImageFont.truetype(font_bold_path, 10.5 * scale)
    font_item = ImageFont.truetype(font_path, 9.5 * scale)
    font_item_bold = ImageFont.truetype(font_bold_path, 10 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 8.5 * scale)

    def S(v):
        return int(v * scale)

    def draw_layer(x, y, lw, lh, title):
        draw.rectangle([S(x), S(y), S(x + lw), S(y + lh)], fill="#F8FAFC", outline="#64748B", width=S(1.4))
        draw.rectangle([S(x), S(y), S(x + lw), S(y + 24)], fill="#FFFFFF", outline="#64748B", width=S(1.4))
        draw.text((S(x + 12), S(y + 4)), title, font=font_layer_title, fill="#0F172A")

    def draw_subgraph(x, y, sw, sh, title, border="#3B82F6"):
        draw.rectangle([S(x), S(y), S(x + sw), S(y + sh)], fill="#FFFFFF", outline=border, width=S(1.2))
        draw.rectangle([S(x), S(y), S(x + sw), S(y + 20)], fill="#F8FAFC", outline=border, width=S(1.2))
        draw.text((S(x + 10), S(y + 3)), title, font=font_sub_title, fill="#1D4ED8")

    def draw_item_box(x, y, bw, bh, text, bold=False, bg="#F1F5F9", border="#94A3B8"):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill=bg, outline=border, width=S(1))
        f = font_item_bold if bold else font_item
        tb = f.getbbox(text)
        tw = tb[2] - tb[0]
        tx = x + (bw - tw / scale) / 2
        ty = y + (bh - 12) / 2
        draw.text((S(tx), S(ty)), text, font=f, fill="#0F172A")

    def draw_main_box(x, y, bw, bh, text, border="#7C3AED"):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill="#FFFFFF", outline=border, width=S(1.4))
        tb = font_item_bold.getbbox(text)
        tw = tb[2] - tb[0]
        tx = x + (bw - tw / scale) / 2
        ty = y + (bh - 12) / 2
        draw.text((S(tx), S(ty)), text, font=font_item_bold, fill="#0F172A")

    def draw_cylinder(x, y, bw, bh, text):
        draw.rectangle([S(x), S(y + 6), S(x + bw), S(y + bh)], fill="#FFFFFF", outline="#DC2626", width=S(1.4))
        draw.ellipse([S(x), S(y), S(x + bw), S(y + 12)], fill="#FEE2E2", outline="#DC2626", width=S(1.4))
        tb = font_item_bold.getbbox(text)
        tw = tb[2] - tb[0]
        tx = x + (bw - tw / scale) / 2
        ty = y + 16 + (bh - 28) / 2
        draw.text((S(tx), S(ty)), text, font=font_item_bold, fill="#991B1B")

    def draw_arrow(p1, p2, label=None, color="#475569", width=1.5):
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
            left = (S(x2 - ux * 6 + vx * 3), S(y2 - uy * 6 + vy * 3))
            right = (S(x2 - ux * 6 - vx * 3), S(y2 - uy * 6 - vy * 3))
            draw.polygon([tip, left, right], fill=color)

        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2 - 8
            draw.text((S(mx + 6), S(my)), label, font=font_arrow, fill=color)

    # 1. LAYER_PRES
    draw_layer(50, 25, 850, 140, "1. Слой представления (Presentation Layer)")
    # MOD_PAGES
    draw_subgraph(75, 58, 360, 95, "Модуль страниц (Pages)", "#3B82F6")
    draw_item_box(90, 85, 330, 18, "HomePage / LandingPage")
    draw_item_box(90, 107, 330, 18, "FlightsPage / FlightDetailPage")
    draw_item_box(90, 129, 330, 18, "AirportsPage / FavoritesPage / ProfilePage")
    # MOD_UI
    draw_subgraph(515, 58, 360, 95, "Модуль UI-компонентов (Components)", "#3B82F6")
    draw_item_box(530, 85, 330, 18, "Navbar / Footer")
    draw_item_box(530, 107, 330, 18, "FlightCard / Filters / SearchBar")
    draw_item_box(530, 129, 330, 18, "AuthModal / VerifyCodeModal")
    # MOD_PAGES --> MOD_UI
    draw_arrow((435, 105), (515, 105), color="#2563EB")

    # 2. LAYER_STATE
    draw_layer(50, 195, 850, 135, "2. Слой состояния и хуков (State & Logic Layer)")
    draw_main_box(75, 235, 360, 75, "Глобальное состояние (AuthContext / Favorites)", "#7C3AED")
    # MOD_HOOKS
    draw_subgraph(515, 225, 360, 95, "Хуки предметной логики", "#7C3AED")
    draw_item_box(530, 252, 330, 18, "useFlights (Каталог и фильтрация)", bg="#F5F3FF", border="#C4B5FD")
    draw_item_box(530, 274, 330, 18, "useFlight (Детальная информация)", bg="#F5F3FF", border="#C4B5FD")
    draw_item_box(530, 296, 330, 18, "useAuth (Авторизация и 2FA)", bg="#F5F3FF", border="#C4B5FD")

    # 3. LAYER_SVC
    draw_layer(50, 360, 850, 135, "3. Слой сетевых служб (Data Services Layer)")
    draw_main_box(75, 400, 360, 75, "Универсальный сетевой клиент (api.ts)", "#059669")
    # MOD_SVC
    draw_subgraph(515, 390, 360, 95, "Службы предметных данных", "#059669")
    draw_item_box(530, 417, 330, 18, "flightService", bold=True, bg="#ECFDF5", border="#A7F3D0")
    draw_item_box(530, 439, 330, 18, "authService", bold=True, bg="#ECFDF5", border="#A7F3D0")
    draw_item_box(530, 461, 330, 18, "airportService", bold=True, bg="#ECFDF5", border="#A7F3D0")

    # 4. LAYER_BE
    draw_layer(50, 525, 850, 135, "4. Слой серверной логики (Backend Application Layer)")
    draw_main_box(75, 565, 360, 75, "Middleware (CORS, Django JSON Parser)", "#0284C7")
    # MOD_ROUTERS
    draw_subgraph(515, 555, 360, 95, "Контроллеры REST API (backend/urls.py)", "#0284C7")
    draw_item_box(530, 582, 330, 18, "/api/flights Контроллер", bg="#E0F2FE", border="#BAE6FD")
    draw_item_box(530, 604, 330, 18, "/api/airports Контроллер", bg="#E0F2FE", border="#BAE6FD")
    draw_item_box(530, 626, 330, 18, "/api/auth Контроллер", bg="#E0F2FE", border="#BAE6FD")

    # 5. LAYER_DATA
    draw_layer(50, 690, 850, 125, "5. Слой доступа к базе данных (Database Access Layer)")
    draw_main_box(75, 730, 360, 65, "Модуль базы данных (Django ORM / models.py)", "#7C3AED")
    draw_cylinder(515, 725, 360, 70, "SQLite 3 СУБД (flights.db)")

    # СВЯЗИ
    # MOD_PAGES --> CTX
    draw_arrow((170, 153), (170, 235))
    # MOD_PAGES --> MOD_HOOKS
    draw_arrow((360, 153), (590, 225))
    # MOD_HOOKS --> MOD_SVC
    draw_arrow((695, 320), (695, 390))
    # MOD_SVC --> API_CLIENT
    draw.line([S(580), S(485), S(580), S(505), S(380), S(505), S(380), S(475)], fill="#475569", width=S(1.5))
    draw_arrow((380, 485), (380, 475), color="#475569")
    # API_CLIENT -->|HTTP REST JSON| MID
    draw_arrow((255, 475), (255, 565), label="HTTP REST JSON", color="#059669", width=1.8)
    # MID --> MOD_ROUTERS
    draw_arrow((435, 602), (515, 602))
    # MOD_ROUTERS --> DB_MOD
    draw_arrow((600, 650), (350, 730))
    # DB_MOD --> DB_STORE
    draw_arrow((435, 762), (515, 762), color="#7C3AED", width=1.8)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Generated 300 DPI PNG: {output_path}")

def generate_module_svg(output_path="docs/module_diagram.svg"):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 850" width="100%" height="100%" style="background:#FFFFFF; font-family: Arial, sans-serif;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
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
  </defs>

  <!-- 1. LAYER_PRES -->
  <rect x="50" y="25" width="850" height="140" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="25" width="850" height="24" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="62" y="42" font-size="12" font-weight="bold" fill="#0F172A">1. Слой представления (Presentation Layer)</text>

  <rect x="75" y="58" width="360" height="95" rx="4" fill="#FFFFFF" stroke="#3B82F6" stroke-width="1.2" />
  <rect x="75" y="58" width="360" height="20" rx="4" fill="#F8FAFC" stroke="#3B82F6" stroke-width="1.2" />
  <text x="85" y="73" font-size="11" font-weight="bold" fill="#1D4ED8">Модуль страниц (Pages)</text>
  <rect x="90" y="85" width="330" height="18" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="180" y="98" font-size="10" fill="#0F172A">HomePage / LandingPage</text>
  <rect x="90" y="107" width="330" height="18" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="170" y="120" font-size="10" fill="#0F172A">FlightsPage / FlightDetailPage</text>
  <rect x="90" y="129" width="330" height="18" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="140" y="142" font-size="10" fill="#0F172A">AirportsPage / FavoritesPage / ProfilePage</text>

  <rect x="515" y="58" width="360" height="95" rx="4" fill="#FFFFFF" stroke="#3B82F6" stroke-width="1.2" />
  <rect x="515" y="58" width="360" height="20" rx="4" fill="#F8FAFC" stroke="#3B82F6" stroke-width="1.2" />
  <text x="525" y="73" font-size="11" font-weight="bold" fill="#1D4ED8">Модуль UI-компонентов (Components)</text>
  <rect x="530" y="85" width="330" height="18" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="645" y="98" font-size="10" fill="#0F172A">Navbar / Footer</text>
  <rect x="530" y="107" width="330" height="18" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="610" y="120" font-size="10" fill="#0F172A">FlightCard / Filters / SearchBar</text>
  <rect x="530" y="129" width="330" height="18" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1" />
  <text x="615" y="142" font-size="10" fill="#0F172A">AuthModal / VerifyCodeModal</text>

  <line x1="435" y1="105" x2="507" y2="105" stroke="#2563EB" stroke-width="1.5" marker-end="url(#arrow-blue)" />

  <!-- 2. LAYER_STATE -->
  <rect x="50" y="195" width="850" height="135" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="195" width="850" height="24" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="62" y="212" font-size="12" font-weight="bold" fill="#0F172A">2. Слой состояния и хуков (State &amp; Logic Layer)</text>

  <rect x="75" y="235" width="360" height="75" rx="4" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.4" />
  <text x="100" y="278" font-size="11" font-weight="bold" fill="#0F172A">Глобальное состояние (AuthContext / Favorites)</text>

  <rect x="515" y="225" width="360" height="95" rx="4" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.2" />
  <rect x="515" y="225" width="360" height="20" rx="4" fill="#F8FAFC" stroke="#7C3AED" stroke-width="1.2" />
  <text x="525" y="240" font-size="11" font-weight="bold" fill="#6D28D9">Хуки предметной логики</text>
  <rect x="530" y="252" width="330" height="18" rx="3" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1" />
  <text x="605" y="265" font-size="10" fill="#0F172A">useFlights (Каталог и фильтрация)</text>
  <rect x="530" y="274" width="330" height="18" rx="3" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1" />
  <text x="615" y="287" font-size="10" fill="#0F172A">useFlight (Детальная информация)</text>
  <rect x="530" y="296" width="330" height="18" rx="3" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1" />
  <text x="625" y="309" font-size="10" fill="#0F172A">useAuth (Авторизация и 2FA)</text>

  <!-- 3. LAYER_SVC -->
  <rect x="50" y="360" width="850" height="135" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="360" width="850" height="24" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="62" y="377" font-size="12" font-weight="bold" fill="#0F172A">3. Слой сетевых служб (Data Services Layer)</text>

  <rect x="75" y="400" width="360" height="75" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="1.4" />
  <text x="125" y="443" font-size="11" font-weight="bold" fill="#0F172A">Универсальный сетевой клиент (api.ts)</text>

  <rect x="515" y="390" width="360" height="95" rx="4" fill="#FFFFFF" stroke="#059669" stroke-width="1.2" />
  <rect x="515" y="390" width="360" height="20" rx="4" fill="#F8FAFC" stroke="#059669" stroke-width="1.2" />
  <text x="525" y="405" font-size="11" font-weight="bold" fill="#047857">Службы предметных данных</text>
  <rect x="530" y="417" width="330" height="18" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="655" y="430" font-size="10" font-weight="bold" fill="#0F172A">flightService</text>
  <rect x="530" y="439" width="330" height="18" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="658" y="452" font-size="10" font-weight="bold" fill="#0F172A">authService</text>
  <rect x="530" y="461" width="330" height="18" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
  <text x="650" y="474" font-size="10" font-weight="bold" fill="#0F172A">airportService</text>

  <!-- 4. LAYER_BE -->
  <rect x="50" y="525" width="850" height="135" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="525" width="850" height="24" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="62" y="542" font-size="12" font-weight="bold" fill="#0F172A">4. Слой серверной логики (Backend Application Layer)</text>

  <rect x="75" y="565" width="360" height="75" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.4" />
  <text x="120" y="608" font-size="11" font-weight="bold" fill="#0F172A">Middleware (CORS, Django JSON Parser)</text>

  <rect x="515" y="555" width="360" height="95" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" />
  <rect x="515" y="555" width="360" height="20" rx="4" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.2" />
  <text x="525" y="570" font-size="11" font-weight="bold" fill="#0369A1">Контроллеры REST API (backend/urls.py)</text>
  <rect x="530" y="582" width="330" height="18" rx="3" fill="#E0F2FE" stroke="#BAE6FD" stroke-width="1" />
  <text x="630" y="595" font-size="10" fill="#0F172A">/api/flights Контроллер</text>
  <rect x="530" y="604" width="330" height="18" rx="3" fill="#E0F2FE" stroke="#BAE6FD" stroke-width="1" />
  <text x="625" y="617" font-size="10" fill="#0F172A">/api/airports Контроллер</text>
  <rect x="530" y="626" width="330" height="18" rx="3" fill="#E0F2FE" stroke="#BAE6FD" stroke-width="1" />
  <text x="635" y="639" font-size="10" fill="#0F172A">/api/auth Контроллер</text>

  <!-- 5. LAYER_DATA -->
  <rect x="50" y="690" width="850" height="125" rx="6" fill="#F8FAFC" stroke="#64748B" stroke-width="1.4" />
  <rect x="50" y="690" width="850" height="24" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.4" />
  <text x="62" y="707" font-size="12" font-weight="bold" fill="#0F172A">5. Слой доступа к базе данных (Database Access Layer)</text>

  <rect x="75" y="730" width="360" height="65" rx="4" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.4" />
  <text x="95" y="768" font-size="11" font-weight="bold" fill="#0F172A">Модуль базы данных (Django ORM / models.py)</text>

  <path d="M 515 735 C 515 725, 875 725, 875 735 L 875 785 C 875 795, 515 795, 515 785 Z" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.4" />
  <path d="M 515 735 C 515 745, 875 745, 875 735" fill="none" stroke="#DC2626" stroke-width="1.4" />
  <text x="620" y="766" font-size="11" font-weight="bold" fill="#991B1B">SQLite 3 СУБД (flights.db)</text>

  <!-- СВЯЗИ -->
  <!-- MOD_PAGES --> CTX -->
  <line x1="170" y1="153" x2="170" y2="227" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- MOD_PAGES --> MOD_HOOKS -->
  <path d="M 360 153 L 360 185 L 590 185 L 590 217" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- MOD_HOOKS --> MOD_SVC -->
  <line x1="695" y1="320" x2="695" y2="382" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- MOD_SVC --> API_CLIENT -->
  <path d="M 580 485 L 580 505 L 380 505 L 380 483" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- API_CLIENT -->|HTTP REST JSON| MID -->
  <line x1="255" y1="475" x2="255" y2="557" stroke="#059669" stroke-width="1.8" marker-end="url(#arrow-green)" />
  <text x="262" y="520" font-size="9" font-weight="bold" fill="#059669">HTTP REST JSON</text>

  <!-- MID --> MOD_ROUTERS -->
  <line x1="435" y1="602" x2="507" y2="602" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- MOD_ROUTERS --> DB_MOD -->
  <path d="M 600 650 L 600 680 L 350 680 L 350 722" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)" />

  <!-- DB_MOD --> DB_STORE -->
  <line x1="435" y1="762" x2="507" y2="762" stroke="#7C3AED" stroke-width="1.8" marker-end="url(#arrow-purple)" />
</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Generated SVG: {output_path}")

if __name__ == "__main__":
    generate_drawio_xml()
    generate_module_png()
    generate_module_svg()
