import os
from PIL import Image, ImageDraw, ImageFont

def generate_request_flow_png(output_path='docs/request_flow_diagram.png'):
    scale = 2
    # Wider canvas to comfortably accommodate Nginx and Django ORM: 1920 x 420
    w, h = 1920 * scale, 420 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'
    font_path = 'C:/Windows/Fonts/arial.ttf'

    font_group = ImageFont.truetype(font_bold_path, 12.5 * scale)
    font_box_title = ImageFont.truetype(font_bold_path, 11.5 * scale)
    font_box_sub = ImageFont.truetype(font_path, 10 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 9.5 * scale)
    font_fallback = ImageFont.truetype(font_path, 9.5 * scale)

    # Colors
    c_white = '#FFFFFF'
    c_border_outer = '#333333'
    c_border_inner = '#4A5568'
    c_text_dark = '#0F172A'
    c_text_sub = '#475569'
    c_arrow = '#1E3A8A'
    c_fallback_border = '#D97706'
    c_fallback_bg = '#FFFBEB'

    def S(val):
        return int(val * scale)

    # Helper: draw box
    def draw_box(x, y, bw, bh, text_main, text_sub=None, fill=c_white, border=c_border_inner, dashed=False):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill=fill, outline=border, width=S(1.2))
        if text_sub:
            tb1 = font_box_title.getbbox(text_main)
            tw1, th1 = tb1[2] - tb1[0], tb1[3] - tb1[1]
            draw.text((S(x + bw/2) - tw1/2, S(y + bh/2 - 9) - th1/2), text_main, font=font_box_title, fill=c_text_dark)
            
            tb2 = font_box_sub.getbbox(text_sub)
            tw2, th2 = tb2[2] - tb2[0], tb2[3] - tb2[1]
            draw.text((S(x + bw/2) - tw2/2, S(y + bh/2 + 10) - th2/2), text_sub, font=font_box_sub, fill=c_text_sub)
        else:
            tb = font_box_title.getbbox(text_main)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]
            draw.text((S(x + bw/2) - tw/2, S(y + bh/2) - th/2), text_main, font=font_box_title, fill=c_text_dark)

    # ================= 1. БАЗА ДАННЫХ (DATABASE) =================
    draw.rectangle([S(20), S(75), S(200), S(335)], fill=c_white, outline=c_border_outer, width=S(1.2))
    draw.text((S(30), S(88)), "База данных (Database)", font=font_group, fill=c_text_dark)

    # Цилиндр СУБД SQLite 3
    cx, cy, cw, ch = 35, 170, 150, 80
    draw.ellipse([S(cx), S(cy + 45), S(cx + cw), S(cy + ch)], fill='#E5E7EB', outline=c_border_inner, width=S(1.2))
    draw.rectangle([S(cx), S(cy + 15), S(cx + cw), S(cy + 60)], fill='#F3F4F6', outline=None)
    draw.line([S(cx), S(cy + 15), S(cx), S(cy + 60)], fill=c_border_inner, width=S(1.2))
    draw.line([S(cx + cw), S(cy + 15), S(cx + cw), S(cy + 60)], fill=c_border_inner, width=S(1.2))
    draw.ellipse([S(cx), S(cy), S(cx + cw), S(cy + 30)], fill='#E5E7EB', outline=c_border_inner, width=S(1.2))
    tb = font_box_title.getbbox("СУБД SQLite 3")
    draw.text((S(cx + cw/2) - (tb[2]-tb[0])/2, S(cy + 42)), "СУБД SQLite 3", font=font_box_title, fill=c_text_dark)

    # ================= 2. СЕРВЕРНАЯ ЧАСТЬ (BACKEND) =================
    draw.rectangle([S(235), S(75), S(1035), S(335)], fill=c_white, outline=c_border_outer, width=S(1.2))
    draw.text((S(250), S(88)), "Серверная часть (Backend & Web Server)", font=font_group, fill=c_text_dark)

    # Блок 1: Django ORM (ПУНКТ 1!)
    draw_box(250, 180, 160, 65, "Django ORM", "(Слой моделей)")

    # Блок 2: Контроллеры
    draw_box(445, 180, 195, 65, "Контроллеры", "(Flights, Airports, Auth)")

    # Блок 3: URL-маршрутизатор Django/DRF (ПУНКТ 5!)
    draw_box(675, 180, 185, 65, "URL-маршрутизатор", "Django / DRF")

    # Блок 4: Веб-сервер Nginx (ПУНКТ 2!)
    draw_box(895, 180, 125, 65, "Nginx", "(Reverse Proxy)", fill='#F8FAFC')

    # ================= 3. КЛИЕНТСКАЯ ЧАСТЬ (FRONTEND) =================
    draw.rectangle([S(1070), S(75), S(1895), S(335)], fill=c_white, outline=c_border_outer, width=S(1.2))
    draw.text((S(1085), S(88)), "Клиентская часть (Frontend)", font=font_group, fill=c_text_dark)

    # Блок 5: Службы данных (Services)
    draw_box(1090, 180, 150, 65, "Службы данных", "(Services / api.ts)")

    # Блок 6: Локальный кэш (Fallback)
    draw_box(1300, 180, 140, 65, "Локальный кэш", "(Fallback / Mocks)", fill=c_fallback_bg, border=c_fallback_border, dashed=True)

    # Блок 7: Интерфейс React SPA
    draw_box(1500, 180, 155, 65, "Интерфейс", "React SPA")

    # Блок 8: Пользователь
    draw_box(1720, 180, 155, 65, "Пользователь", None, fill='#F3F4F6')

    # Helper: draw curved arrow
    def draw_curve_arrow(p0, p1, p2, text=None, text_y_offset=0):
        steps = 40
        points = []
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
            points.append((S(x), S(y)))
        draw.line(points, fill=c_arrow, width=S(1.5))
        
        # Arrowhead
        dx = points[-1][0] - points[-3][0]
        dy = points[-1][1] - points[-3][1]
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            ux, uy = dx/length, dy/length
            nx, ny = -uy, ux
            tip = points[-1]
            asize = S(5.5)
            p_left = (tip[0] - asize*ux + asize*0.5*nx, tip[1] - asize*uy + asize*0.5*ny)
            p_right = (tip[0] - asize*ux - asize*0.5*nx, tip[1] - asize*uy - asize*0.5*ny)
            draw.polygon([tip, p_left, p_right], fill=c_arrow)

        # Label
        if text:
            tb = font_arrow.getbbox(text)
            tw = tb[2] - tb[0]
            tx = S(p1[0]) - tw/2
            ty = S(p1[1] + text_y_offset)
            draw.text((tx, ty), text, font=font_arrow, fill=c_arrow)

    # ================= НИЖНИЙ КОНТУР (ПРЯМОЙ ХОД ЗАПРОСА) =================

    # 1. Действие в интерфейсе (Пользователь -> Интерфейс)
    draw_curve_arrow((1720, 225), (1688, 265), (1655, 230), "1. Действие в интерфейсе", 10)

    # 2. Вызов метода (Интерфейс -> Службы данных)
    draw_curve_arrow((1500, 230), (1370, 310), (1240, 230), "2. Вызов метода", 10)

    # 3. HTTP Запрос (Службы данных -> Nginx)
    draw_curve_arrow((1090, 230), (1055, 275), (1020, 230), "3. HTTP-запрос", 10)

    # 4. Проксирование (Nginx -> URL-маршрутизатор)
    draw_curve_arrow((895, 225), (878, 250), (860, 225), "4. Проксирование", 10)

    # 5. Вызов контроллера (URL-маршрутизатор -> Контроллеры)
    draw_curve_arrow((675, 225), (658, 250), (640, 225), "5. Вызов контроллера", 10)

    # 6. ORM-запрос (Контроллеры -> Django ORM)
    draw_curve_arrow((445, 225), (428, 250), (410, 225), "6. ORM-запрос", 10)

    # 7. SQL Запрос (Django ORM -> SQLite)
    draw_curve_arrow((250, 230), (220, 275), (185, 230), "7. SQL-запрос", 10)

    # ================= ВЕРХНИЙ КОНТУР (ОБРАТНЫЙ ХОД ОТВЕТА) =================

    # 8. Результат SQL-запроса (SQLite -> Django ORM) [ПУНКТ 4!]
    draw_curve_arrow((185, 195), (220, 145), (248, 195), "8. Результат SQL-запроса", -22)

    # 9. Данные моделей (Django ORM -> Контроллеры)
    draw_curve_arrow((410, 200), (428, 175), (443, 200), "9. Данные моделей", -18)

    # 10. JSON Ответ (Контроллеры -> URL-маршрутизатор)
    draw_curve_arrow((640, 200), (658, 175), (673, 200), "10. JSON-ответ", -18)

    # 11. Передача ответа (URL-маршрутизатор -> Nginx)
    draw_curve_arrow((860, 200), (878, 175), (893, 200), "11. Ответ", -18)

    # 12. HTTP-ответ (JSON) (Nginx -> Службы данных) [ПУНКТ 3!]
    draw_curve_arrow((1020, 195), (1055, 145), (1088, 195), "12. HTTP-ответ (JSON)", -22)

    # 13. Обновление состояния (Службы данных -> Интерфейс)
    draw_curve_arrow((1240, 195), (1370, 115), (1498, 195), "13. Обновление состояния", -22)

    # 14. Рендеринг (Интерфейс -> Пользователь)
    draw_curve_arrow((1655, 195), (1688, 155), (1718, 195), "14. Рендеринг", -20)

    # ================= АВТОНОМНЫЙ ПУНКТИРНЫЙ КОНТУР (FALLBACK) =================
    # Службы -> Кэш
    draw.line([S(1240), S(212), S(1298), S(212)], fill=c_fallback_border, width=S(1.3))
    draw.polygon([(S(1298), S(212)), (S(1291), S(208)), (S(1291), S(216))], fill=c_fallback_border)
    tb1 = font_fallback.getbbox("Сбой сети / >2c")
    draw.text((S(1270) - (tb1[2]-tb1[0])/2, S(196)), "Сбой сети / >2c", font=font_fallback, fill=c_fallback_border)

    # Кэш -> Интерфейс
    draw.line([S(1440), S(212), S(1498), S(212)], fill=c_fallback_border, width=S(1.3))
    draw.polygon([(S(1498), S(212)), (S(1491), S(208)), (S(1491), S(216))], fill=c_fallback_border)
    tb2 = font_fallback.getbbox("Автономные данные")
    draw.text((S(1470) - (tb2[2]-tb2[0])/2, S(196)), "Автономные данные", font=font_fallback, fill=c_fallback_border)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"Updated Request Flow PNG generated: {output_path}")

if __name__ == '__main__':
    generate_request_flow_png()

