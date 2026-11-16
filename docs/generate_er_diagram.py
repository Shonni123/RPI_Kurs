import os
from PIL import Image, ImageDraw, ImageFont

def generate_compact_er_diagram_png(output_path='docs/er_diagram.png'):
    scale = 2
    # Width and height to comfortably house the updated FLIGHT table
    w, h = 1380 * scale, 480 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'
    font_path = 'C:/Windows/Fonts/arial.ttf'

    font_title = ImageFont.truetype(font_bold_path, 11.5 * scale)
    font_field_bold = ImageFont.truetype(font_bold_path, 10 * scale)
    font_field_reg = ImageFont.truetype(font_path, 10 * scale)
    font_rel = ImageFont.truetype(font_bold_path, 9.5 * scale)

    def S(val):
        return int(val * scale)

    # Helper: draw table card
    def draw_table(x, y, tw, title, fields, title_bg='#F1F5F9', border_color='#334155'):
        th = 28
        row_h = 24
        total_h = th + len(fields) * row_h + 4

        # Header background
        draw.rectangle([S(x), S(y), S(x + tw), S(y + th)], fill=title_bg, outline=border_color, width=S(1.2))
        draw.text((S(x + 10), S(y + 6)), title, font=font_title, fill='#0F172A')

        # Body background
        draw.rectangle([S(x), S(y + th), S(x + tw), S(y + total_h)], fill='#FFFFFF', outline=border_color, width=S(1.2))

        # Fields
        cur_y = y + th + 4
        for fld in fields:
            name, ftype, note = fld[0], fld[1], fld[2] if len(fld) > 2 else ""
            
            # Key / Name
            draw.text((S(x + 10), S(cur_y)), name, font=font_field_bold, fill='#1E293B')
            
            # Type
            draw.text((S(x + 115), S(cur_y)), ftype, font=font_field_reg, fill='#475569')

            # Note / constraint
            if note:
                draw.text((S(x + 205), S(cur_y)), note, font=font_field_reg, fill='#64748B')

            cur_y += row_h

        return x, y, tw, total_h

    # ================= 1. USER =================
    user_fields = [
        ("PK | id", "INTEGER", ""),
        ("UK | username", "VARCHAR(150)", ""),
        ("UK | email", "VARCHAR(254)", ""),
        ("     | password", "VARCHAR(128)", "PBKDF2"),
        ("     | date_joined", "DATETIME", ""),
    ]
    u_x, u_y, u_w, u_h = draw_table(40, 40, 280, "USER (auth_user)", user_fields, '#E2E8F0')

    # ================= 2. USER_PROFILE =================
    profile_fields = [
        ("PK | id", "INTEGER", ""),
        ("FK | user_id", "INTEGER", "1:1 к user"),
        ("     | is_verified", "BOOLEAN", "Email"),
        ("     | phone", "VARCHAR(30)", ""),
    ]
    p_x, p_y, p_w, p_h = draw_table(40, 260, 280, "USER_PROFILE (accounts_userprofile)", profile_fields, '#E0F2FE', '#0284C7')

    # ================= 3. EMAIL_VERIFICATION_CODE =================
    code_fields = [
        ("PK | id", "INTEGER", ""),
        ("FK | user_id", "INTEGER", "1:N к user"),
        ("     | code", "VARCHAR(6)", "6 цифр"),
        ("     | purpose", "VARCHAR(20)", "verify / reset"),
        ("     | is_used", "BOOLEAN", "default: False"),
        ("     | created_at", "DATETIME", "TTL 15 мин"),
    ]
    c_x, c_y, c_w, c_h = draw_table(360, 40, 290, "EMAIL_VERIFICATION_CODE", code_fields, '#FEF3C7', '#D97706')

    # ================= 4. AIRPORT =================
    airport_fields = [
        ("PK | id", "INTEGER", ""),
        ("UK | code", "VARCHAR(10)", "IATA (SVO, DXB)"),
        ("     | name", "VARCHAR(150)", "Название хаба"),
        ("     | city", "VARCHAR(100)", "Город"),
        ("     | country", "VARCHAR(100)", "Страна"),
    ]
    a_x, a_y, a_w, a_h = draw_table(690, 40, 280, "AIRPORT (flights_airport)", airport_fields, '#E2E8F0')

    # ================= 5. FLIGHT (ДОПОЛНЕННАЯ) =================
    flight_fields = [
        ("PK | id", "INTEGER", ""),
        ("     | flight_number", "VARCHAR(30)", "SU 1702"),
        ("     | airline", "VARCHAR(100)", "Авиакомпания"),
        ("FK | from_code", "VARCHAR(10)", "1:N вылет"),
        ("FK | to_code", "VARCHAR(10)", "1:N прилет"),
        ("     | dep_date", "VARCHAR(20)", "Дата вылета"),
        ("     | dep_time", "VARCHAR(20)", "ЧЧ:ММ"),
        ("     | arr_time", "VARCHAR(20)", "ЧЧ:ММ"),
        ("     | status", "VARCHAR(30)", "scheduled..."),
        ("     | altitude", "INTEGER", "Высота (м)"),
        ("     | speed", "INTEGER", "Скорость (км/ч)"),
        ("     | price", "INTEGER", "Цена (руб.)"),
        ("     | updated_at", "DATETIME", "Обновление"),
    ]
    f_x, f_y, f_w, f_h = draw_table(1010, 40, 320, "FLIGHT (flights_flight)", flight_fields, '#DCFCE7', '#16A34A')

    # ================= СВЯЗИ (RELATIONSHIPS) =================
    c_line = '#1E3A8A'

    # 1. USER -> USER_PROFILE (1 : 1, vertical)
    draw.line([S(u_x + 140), S(u_y + u_h), S(u_x + 140), S(p_y)], fill=c_line, width=S(1.8))
    draw.line([S(u_x + 132), S(u_y + u_h + 10), S(u_x + 148), S(u_y + u_h + 10)], fill=c_line, width=S(1.8))
    draw.line([S(u_x + 132), S(p_y - 10), S(u_x + 148), S(p_y - 10)], fill=c_line, width=S(1.8))
    draw.text((S(u_x + 155), S(u_y + u_h + 16)), "1 : 1", font=font_rel, fill=c_line)

    # 2. USER -> EMAIL_VERIFICATION_CODE (1 : N, horizontal)
    y_uc = u_y + 60
    draw.line([S(u_x + u_w), S(y_uc), S(c_x), S(y_uc)], fill=c_line, width=S(1.8))
    draw.line([S(u_x + u_w + 8), S(y_uc - 8), S(u_x + u_w + 8), S(y_uc + 8)], fill=c_line, width=S(1.8))
    # Crow foot
    draw.line([S(c_x - 12), S(y_uc - 8), S(c_x), S(y_uc)], fill=c_line, width=S(1.8))
    draw.line([S(c_x - 12), S(y_uc + 8), S(c_x), S(y_uc)], fill=c_line, width=S(1.8))
    draw.text((S(u_x + u_w + 10), S(y_uc - 18)), "1 : N", font=font_rel, fill=c_line)

    # 3. AIRPORT -> FLIGHT (from_code, 1:N)
    y_af_from = 115
    draw.line([S(a_x + a_w), S(y_af_from), S(f_x), S(y_af_from)], fill=c_line, width=S(1.8))
    draw.line([S(a_x + a_w + 8), S(y_af_from - 8), S(a_x + a_w + 8), S(y_af_from + 8)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 12), S(y_af_from - 8), S(f_x), S(y_af_from)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 12), S(y_af_from + 8), S(f_x), S(y_af_from)], fill=c_line, width=S(1.8))
    draw.text((S(a_x + a_w + 8), S(y_af_from - 18)), "1 : N (from)", font=font_rel, fill=c_line)

    # 4. AIRPORT -> FLIGHT (to_code, 1:N)
    y_af_to = 145
    draw.line([S(a_x + a_w), S(y_af_to), S(f_x), S(y_af_to)], fill=c_line, width=S(1.8))
    draw.line([S(a_x + a_w + 8), S(y_af_to - 8), S(a_x + a_w + 8), S(y_af_to + 8)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 12), S(y_af_to - 8), S(f_x), S(y_af_to)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 12), S(y_af_to + 8), S(f_x), S(y_af_to)], fill=c_line, width=S(1.8))
    draw.text((S(a_x + a_w + 8), S(y_af_to - 18)), "1 : N (to)", font=font_rel, fill=c_line)

    # ================= ЛЕГЕНДА =================
    leg_x, leg_y = 360, 260
    draw.rectangle([S(leg_x), S(leg_y), S(leg_x + 610), S(leg_y + 130)], fill='#FAFBFD', outline='#94A3B8', width=S(1))
    draw.text((S(leg_x + 12), S(leg_y + 10)), "Обозначения реляционных связей (ГОСТ):", font=font_title, fill='#1E293B')
    draw.text((S(leg_x + 12), S(leg_y + 36)), "• PK — Первичный ключ (Primary Key) | FK — Внешний ключ (Foreign Key)", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 12), S(leg_y + 60)), "• UK — Ограничение уникальности (Unique Constraint)", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 12), S(leg_y + 84)), "• 1 : 1 — Отношение один-к-одному (Пользователь -> Профиль)", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 12), S(leg_y + 108)), "• 1 : N — Отношение один-ко-многим (Коды подтверждения, Маршруты рейсов)", font=font_field_reg, fill='#334155')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"Updated Compact ER diagram PNG generated: {output_path}")

if __name__ == '__main__':
    generate_compact_er_diagram_png()
