import os
from PIL import Image, ImageDraw, ImageFont

def generate_compact_er_diagram_png(output_path='docs/er_diagram.png'):
    scale = 2
    # Much more compact: 1300 x 480 (instead of 1600 x 920)
    w, h = 1320 * scale, 480 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'
    font_path = 'C:/Windows/Fonts/arial.ttf'

    font_title = ImageFont.truetype(font_bold_path, 12 * scale)
    font_field_bold = ImageFont.truetype(font_bold_path, 10.5 * scale)
    font_field_reg = ImageFont.truetype(font_path, 10.5 * scale)
    font_rel = ImageFont.truetype(font_bold_path, 10 * scale)

    def S(val):
        return int(val * scale)

    # Helper: draw table card
    def draw_table(x, y, tw, title, fields, title_bg='#F1F5F9'):
        th = 30
        row_h = 22
        total_h = th + len(fields) * row_h + 6

        # Header background
        draw.rectangle([S(x), S(y), S(x + tw), S(y + th)], fill=title_bg, outline='#334155', width=S(1.2))
        draw.text((S(x + 10), S(y + 7)), title, font=font_title, fill='#0F172A')

        # Body background
        draw.rectangle([S(x), S(y + th), S(x + tw), S(y + total_h)], fill='#FFFFFF', outline='#334155', width=S(1.2))

        # Fields
        cur_y = y + th + 4
        for fld in fields:
            name, ftype, note = fld[0], fld[1], fld[2] if len(fld) > 2 else ""
            
            # Name & key
            draw.text((S(x + 10), S(cur_y)), name, font=font_field_bold, fill='#1E293B')
            
            # Type
            draw.text((S(x + 100), S(cur_y)), ftype, font=font_field_reg, fill='#475569')

            # Note / constraint
            if note:
                draw.text((S(x + 180), S(cur_y)), note, font=font_field_reg, fill='#64748B')

            cur_y += row_h

        return x, y, tw, total_h

    # ================= 1. USER =================
    user_fields = [
        ("id", "INTEGER", "PK"),
        ("username", "VARCHAR", "UNIQUE"),
        ("email", "VARCHAR", "UNIQUE"),
        ("password", "VARCHAR", "PBKDF2 Hash"),
        ("date_joined", "DATETIME", ""),
    ]
    u_x, u_y, u_w, u_h = draw_table(30, 30, 260, "USER (auth_user)", user_fields, '#E2E8F0')

    # ================= 2. USER_PROFILE =================
    profile_fields = [
        ("id", "INTEGER", "PK"),
        ("user_id", "INTEGER", "FK -> user (1:1)"),
        ("is_email_verified", "BOOLEAN", "default: False"),
        ("phone", "VARCHAR", ""),
    ]
    p_x, p_y, p_w, p_h = draw_table(30, 220, 260, "USER_PROFILE", profile_fields, '#E0F2FE')

    # ================= 3. EMAIL_VERIFICATION_CODE =================
    code_fields = [
        ("id", "INTEGER", "PK"),
        ("user_id", "INTEGER", "FK -> user (1:N)"),
        ("code", "VARCHAR(6)", "6-значный код"),
        ("purpose", "VARCHAR", "verify / reset"),
        ("is_used", "BOOLEAN", "default: False"),
        ("created_at", "DATETIME", "TTL 15 мин"),
    ]
    c_x, c_y, c_w, c_h = draw_table(340, 30, 280, "EMAIL_VERIFICATION_CODE", code_fields, '#FEF3C7')

    # ================= 4. AIRPORT =================
    airport_fields = [
        ("id", "INTEGER", "PK"),
        ("code", "VARCHAR(10)", "UK (IATA)"),
        ("name", "VARCHAR", "Название хаба"),
        ("city", "VARCHAR", "Город"),
        ("country", "VARCHAR", "Страна"),
    ]
    a_x, a_y, a_w, a_h = draw_table(670, 120, 260, "AIRPORT (flights_airport)", airport_fields, '#E2E8F0')

    # ================= 5. FLIGHT =================
    flight_fields = [
        ("id", "INTEGER", "PK"),
        ("flight_number", "VARCHAR", "Номер (SU 1702)"),
        ("airline", "VARCHAR", "Авиакомпания"),
        ("from_code", "VARCHAR", "FK -> airport (1:N)"),
        ("to_code", "VARCHAR", "FK -> airport (1:N)"),
        ("departure_time", "VARCHAR", "ЧЧ:ММ"),
        ("arrival_time", "VARCHAR", "ЧЧ:ММ"),
        ("status", "VARCHAR", "scheduled / landed"),
        ("price", "INTEGER", "Цена (руб)"),
    ]
    f_x, f_y, f_w, f_h = draw_table(990, 80, 290, "FLIGHT (flights_flight)", flight_fields, '#DCFCE7')

    # ================= RELATIONSHIP ARROWS =================
    c_line = '#1E3A8A'

    # 1. USER -> USER_PROFILE (1 : 1, vertical)
    draw.line([S(u_x + 80), S(u_y + u_h), S(u_x + 80), S(p_y)], fill=c_line, width=S(1.8))
    # 1:1 cross marks
    draw.line([S(u_x + 72), S(u_y + u_h + 8), S(u_x + 88), S(u_y + u_h + 8)], fill=c_line, width=S(1.8))
    draw.line([S(u_x + 72), S(p_y - 8), S(u_x + 88), S(p_y - 8)], fill=c_line, width=S(1.8))
    draw.text((S(u_x + 90), S(u_y + u_h + 10)), "1 : 1", font=font_rel, fill=c_line)

    # 2. USER -> EMAIL_VERIFICATION_CODE (1 : N, horizontal)
    y_uc = u_y + 60
    draw.line([S(u_x + u_w), S(y_uc), S(c_x), S(y_uc)], fill=c_line, width=S(1.8))
    draw.line([S(u_x + u_w + 8), S(y_uc - 8), S(u_x + u_w + 8), S(y_uc + 8)], fill=c_line, width=S(1.8))
    # Crow foot
    draw.line([S(c_x - 12), S(y_uc - 8), S(c_x), S(y_uc)], fill=c_line, width=S(1.8))
    draw.line([S(c_x - 12), S(y_uc + 8), S(c_x), S(y_uc)], fill=c_line, width=S(1.8))
    draw.text((S(u_x + u_w + 12), S(y_uc - 18)), "1 : N", font=font_rel, fill=c_line)

    # 3. AIRPORT -> FLIGHT (1 : N, from_code and to_code)
    y_af_1 = 160
    draw.line([S(a_x + a_w), S(y_af_1), S(f_x), S(y_af_1)], fill=c_line, width=S(1.8))
    draw.line([S(a_x + a_w + 8), S(y_af_1 - 8), S(a_x + a_w + 8), S(y_af_1 + 8)], fill=c_line, width=S(1.8))
    # Crow foot
    draw.line([S(f_x - 12), S(y_af_1 - 8), S(f_x), S(y_af_1)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 12), S(y_af_1 + 8), S(f_x), S(y_af_1)], fill=c_line, width=S(1.8))
    draw.text((S(a_x + a_w + 10), S(y_af_1 - 18)), "1 : N (from)", font=font_rel, fill=c_line)

    y_af_2 = 210
    draw.line([S(a_x + a_w), S(y_af_2), S(f_x), S(y_af_2)], fill=c_line, width=S(1.8))
    draw.line([S(a_x + a_w + 8), S(y_af_2 - 8), S(a_x + a_w + 8), S(y_af_2 + 8)], fill=c_line, width=S(1.8))
    # Crow foot
    draw.line([S(f_x - 12), S(y_af_2 - 8), S(f_x), S(y_af_2)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 12), S(y_af_2 + 8), S(f_x), S(y_af_2)], fill=c_line, width=S(1.8))
    draw.text((S(a_x + a_w + 10), S(y_af_2 - 18)), "1 : N (to)", font=font_rel, fill=c_line)

    # Legend at bottom right
    leg_x, leg_y = 340, 230
    draw.rectangle([S(leg_x), S(leg_y), S(leg_x + 280), S(leg_y + 115)], fill='#FAFBFD', outline='#94A3B8', width=S(1))
    draw.text((S(leg_x + 10), S(leg_y + 10)), "Обозначения связей (ГОСТ):", font=font_title, fill='#1E293B')
    draw.text((S(leg_x + 10), S(leg_y + 35)), "• PK — Первичный ключ | FK — Внешний ключ", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 10), S(leg_y + 60)), "• 1 : 1 — Отношение один-к-одному (Профиль)", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 10), S(leg_y + 85)), "• 1 : N — Отношение один-ко-многим (Коды, Рейсы)", font=font_field_reg, fill='#334155')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"Compact ER diagram PNG generated: {output_path}")

if __name__ == '__main__':
    generate_compact_er_diagram_png()
