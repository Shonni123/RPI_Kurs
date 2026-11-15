import os
from PIL import Image, ImageDraw, ImageFont

def generate_request_flow_png(output_path='docs/request_flow_diagram.png'):
    # Dimensions (2x scale for crisp 300 DPI print quality in Word)
    scale = 2
    w, h = 1600 * scale, 380 * scale
    
    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    font_path = 'C:/Windows/Fonts/arial.ttf'
    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'

    font_title = ImageFont.truetype(font_bold_path, 13 * scale)
    font_box_title = ImageFont.truetype(font_bold_path, 13 * scale)
    font_box_sub = ImageFont.truetype(font_path, 11 * scale)
    font_arrow = ImageFont.truetype(font_bold_path, 11 * scale)
    font_fallback = ImageFont.truetype(font_path, 10 * scale)

    # Colors (Academic clean style: pure white, light gray, thin dark borders, dark text)
    c_white = '#FFFFFF'
    c_bg_sub = '#F8F9FA'
    c_border_outer = '#333333'
    c_border_inner = '#4A5568'
    c_text_dark = '#111827'
    c_text_sub = '#4B5563'
    c_arrow = '#1E3A8A'
    c_fallback_border = '#D97706'
    c_fallback_bg = '#FFFBEB'

    def S(val):
        return int(val * scale)

    # Helper: Draw box
    def draw_box(x, y, bw, bh, text_main, text_sub=None, fill=c_white, border=c_border_inner, dashed=False):
        draw.rectangle([S(x), S(y), S(x + bw), S(y + bh)], fill=fill, outline=border, width=S(1.2))
        if text_sub:
            # Two lines of text
            tb1 = font_box_title.getbbox(text_main)
            tw1, th1 = tb1[2] - tb1[0], tb1[3] - tb1[1]
            draw.text((S(x + bw/2) - tw1/2, S(y + bh/2 - 10) - th1/2), text_main, font=font_box_title, fill=c_text_dark)
            
            tb2 = font_box_sub.getbbox(text_sub)
            tw2, th2 = tb2[2] - tb2[0], tb2[3] - tb2[1]
            draw.text((S(x + bw/2) - tw2/2, S(y + bh/2 + 10) - th2/2), text_sub, font=font_box_sub, fill=c_text_sub)
        else:
            # Single line
            tb = font_box_title.getbbox(text_main)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]
            draw.text((S(x + bw/2) - tw/2, S(y + bh/2) - th/2), text_main, font=font_box_title, fill=c_text_dark)

    # ================= 1. БАЗА ДАННЫХ (DATABASE) =================
    draw.rectangle([S(20), S(70), S(200), S(310)], fill=c_white, outline=c_border_outer, width=S(1.2))
    draw.text((S(30), S(82)), "База данных (Database)", font=font_title, fill=c_text_dark)

    # Цилиндр SQLite
    cx, cy, cw, ch = 35, 155, 150, 75
    # Нижняя дуга цилиндра
    draw.ellipse([S(cx), S(cy + 40), S(cx + cw), S(cy + ch)], fill='#E5E7EB', outline=c_border_inner, width=S(1.2))
    draw.rectangle([S(cx), S(cy + 15), S(cx + cw), S(cy + 55)], fill='#F3F4F6', outline=None)
    draw.line([S(cx), S(cy + 15), S(cx), S(cy + 55)], fill=c_border_inner, width=S(1.2))
    draw.line([S(cx + cw), S(cy + 15), S(cx + cw), S(cy + 55)], fill=c_border_inner, width=S(1.2))
    # Верхний эллипс
    draw.ellipse([S(cx), S(cy), S(cx + cw), S(cy + 30)], fill='#E5E7EB', outline=c_border_inner, width=S(1.2))
    tb = font_box_title.getbbox("СУБД SQLite 3")
    draw.text((S(cx + cw/2) - (tb[2]-tb[0])/2, S(cy + 38)), "СУБД SQLite 3", font=font_box_title, fill=c_text_dark)

    # ================= 2. СЕРВЕРНАЯ ЧАСТЬ (BACKEND) =================
    draw.rectangle([S(240), S(70), S(705), S(310)], fill=c_white, outline=c_border_outer, width=S(1.2))
    draw.text((S(255), S(82)), "Серверная часть (Backend)", font=font_title, fill=c_text_dark)

    draw_box(260, 160, 215, 65, "Контроллеры", "(Flights, Airports, Auth)")
    draw_box(515, 160, 170, 65, "REST API", "Маршрутизатор")

    # ================= 3. КЛИЕНТСКАЯ ЧАСТЬ (FRONTEND) =================
    draw.rectangle([S(745), S(70), S(1580), S(310)], fill=c_white, outline=c_border_outer, width=S(1.2))
    draw.text((S(760), S(82)), "Клиентская часть (Frontend)", font=font_title, fill=c_text_dark)

    draw_box(770, 160, 155, 65, "Службы данных", "(Services / api.ts)")
    draw_box(985, 160, 145, 65, "Локальный кэш", "(Fallback / Mocks)", fill=c_fallback_bg, border=c_fallback_border, dashed=True)
    draw_box(1190, 160, 160, 65, "Интерфейс", "React SPA")
    draw_box(1420, 160, 140, 65, "Пользователь", None, fill='#F9FAFB')

    # Helper: draw curved arrow using bezier
    def draw_curve_arrow(p0, p1, p2, text=None, text_y_offset=0, is_top=True):
        steps = 40
        points = []
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
            points.append((S(x), S(y)))
        draw.line(points, fill=c_arrow, width=S(1.6))
        
        # Arrowhead at p2
        # direction vector
        dx = points[-1][0] - points[-3][0]
        dy = points[-1][1] - points[-3][1]
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            ux, uy = dx/length, dy/length
            # normal
            nx, ny = -uy, ux
            tip = points[-1]
            asize = S(6)
            p_left = (tip[0] - asize*ux + asize*0.5*nx, tip[1] - asize*uy + asize*0.5*ny)
            p_right = (tip[0] - asize*ux - asize*0.5*nx, tip[1] - asize*uy - asize*0.5*ny)
            draw.polygon([tip, p_left, p_right], fill=c_arrow)

        # Label text
        if text:
            tb = font_arrow.getbbox(text)
            tw = tb[2] - tb[0]
            tx = S(p1[0]) - tw/2
            ty = S(p1[1] + text_y_offset)
            draw.text((tx, ty), text, font=font_arrow, fill=c_arrow)

    # 1. Действие в интерфейсе (Пользователь -> Интерфейс) [Нижняя дуга]
    draw_curve_arrow((1420, 205), (1390, 245), (1352, 210), "1. Действие в интерфейсе", 12)

    # 2. Вызов метода (Интерфейс -> Службы данных) [Нижняя дуга]
    draw_curve_arrow((1190, 210), (1055, 290), (928, 210), "2. Вызов метода", 12)

    # 3. HTTP Запрос (Службы данных -> REST API) [Нижняя дуга]
    draw_curve_arrow((770, 210), (728, 255), (688, 210), "3. HTTP Запрос", 12)

    # 4. Вызов контроллера (REST API -> Контроллеры) [Нижняя дуга]
    draw_curve_arrow((515, 205), (496, 230), (478, 205), "4. Вызов контроллера", 10)

    # 5. SQL Запрос (Контроллеры -> SQLite) [Нижняя дуга]
    draw_curve_arrow((260, 210), (225, 260), (188, 215), "5. SQL Запрос", 12)

    # 6. Строки данных (SQLite -> Контроллеры) [Верхняя дуга]
    draw_curve_arrow((188, 175), (225, 125), (258, 175), "6. Строки данных", -24)

    # 7. JSON Ответ (Контроллеры -> REST API) [Верхняя дуга]
    draw_curve_arrow((478, 175), (496, 150), (513, 175), "7. JSON Ответ", -20)

    # 8. HTTP 200/201 (REST API -> Службы данных) [Верхняя дуга]
    draw_curve_arrow((688, 175), (728, 125), (768, 175), "8. HTTP 200/201", -24)

    # 9. Обновление состояния (Службы данных -> Интерфейс) [Верхняя дуга]
    draw_curve_arrow((928, 175), (1055, 95), (1188, 175), "9. Обновление состояния", -24)

    # 10. Рендеринг (Интерфейс -> Пользователь) [Верхняя дуга]
    draw_curve_arrow((1352, 175), (1388, 135), (1418, 175), "10. Рендеринг", -22)

    # Fallback стрелки (прямые пунктирные)
    # Службы -> Кэш
    draw.line([S(925), S(192), S(983), S(192)], fill=c_fallback_border, width=S(1.4))
    # Стрелочка
    draw.polygon([(S(983), S(192)), (S(976), S(188)), (S(976), S(196))], fill=c_fallback_border)
    tb = font_fallback.getbbox("Сбой сети / >2c")
    draw.text((S(955) - (tb[2]-tb[0])/2, S(176)), "Сбой сети / >2c", font=font_fallback, fill=c_fallback_border)

    # Кэш -> Интерфейс
    draw.line([S(1130), S(192), S(1188), S(192)], fill=c_fallback_border, width=S(1.4))
    draw.polygon([(S(1188), S(192)), (S(1181), S(188)), (S(1181), S(196))], fill=c_fallback_border)
    tb = font_fallback.getbbox("Автономные данные")
    draw.text((S(1160) - (tb[2]-tb[0])/2, S(176)), "Автономные данные", font=font_fallback, fill=c_fallback_border)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"High-res white PNG generated: {output_path}")

if __name__ == '__main__':
    generate_request_flow_png()
