import os
from PIL import Image, ImageDraw, ImageFont

def generate_er_diagram_png(output_path='docs/er_diagram.png'):
    scale = 2
    w, h = 1600 * scale, 920 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'
    font_path = 'C:/Windows/Fonts/arial.ttf'

    font_title = ImageFont.truetype(font_bold_path, 13 * scale)
    font_field_bold = ImageFont.truetype(font_bold_path, 10.5 * scale)
    font_field_reg = ImageFont.truetype(font_path, 10.5 * scale)
    font_rel = ImageFont.truetype(font_bold_path, 10 * scale)

    def S(val):
        return int(val * scale)

    # Helper: draw table card
    def draw_table(x, y, tw, title, fields, title_bg='#F1F5F9'):
        th = 32
        row_h = 24
        total_h = th + len(fields) * row_h + 8

        # Header background
        draw.rectangle([S(x), S(y), S(x + tw), S(y + th)], fill=title_bg, outline='#334155', width=S(1.2))
        draw.text((S(x + 12), S(y + 8)), title, font=font_title, fill='#0F172A')

        # Body background
        draw.rectangle([S(x), S(y + th), S(x + tw), S(y + total_h)], fill='#FFFFFF', outline='#334155', width=S(1.2))

        # Fields
        cur_y = y + th + 6
        for fld in fields:
            name, ftype, note = fld[0], fld[1], fld[2] if len(fld) > 2 else ""
            
            # Name & key
            draw.text((S(x + 12), S(cur_y)), name, font=font_field_bold, fill='#1E293B')
            
            # Type
            draw.text((S(x + 140), S(cur_y)), ftype, font=font_field_reg, fill='#475569')

            # Note / constraint
            if note:
                draw.text((S(x + 230), S(cur_y)), note, font=font_field_reg, fill='#64748B')

            cur_y += row_h

        return x, y, tw, total_h

    # ================= DRAW TABLES =================

    # 1. USER
    user_fields = [
        ("id", "INTEGER", "PK, autoincrement"),
        ("username", "VARCHAR(150)", "UNIQUE"),
        ("email", "VARCHAR(254)", "UNIQUE"),
        ("password", "VARCHAR(128)", "PBKDF2-SHA256 hash"),
        ("first_name", "VARCHAR(150)", ""),
        ("last_name", "VARCHAR(150)", ""),
        ("is_active", "BOOLEAN", "default: True"),
        ("date_joined", "DATETIME", ""),
    ]
    u_x, u_y, u_w, u_h = draw_table(40, 40, 360, "USER (auth_user)", user_fields, '#E2E8F0')

    # 2. USER_PROFILE
    profile_fields = [
        ("id", "INTEGER", "PK, autoincrement"),
        ("user_id", "INTEGER", "FK -> auth_user.id (UNIQUE)"),
        ("is_email_verified", "BOOLEAN", "default: False"),
        ("phone", "VARCHAR(30)", ""),
        ("created_at", "DATETIME", ""),
    ]
    p_x, p_y, p_w, p_h = draw_table(460, 40, 370, "USER_PROFILE (accounts_userprofile)", profile_fields, '#E0F2FE')

    # 3. EMAIL_VERIFICATION_CODE
    code_fields = [
        ("id", "INTEGER", "PK, autoincrement"),
        ("user_id", "INTEGER", "FK -> auth_user.id"),
        ("code", "VARCHAR(6)", "6-значный цифровой код"),
        ("purpose", "VARCHAR(20)", "verify_email / reset_pass"),
        ("is_used", "BOOLEAN", "default: False"),
        ("created_at", "DATETIME", "TTL: 15 минут"),
    ]
    c_x, c_y, c_w, c_h = draw_table(890, 40, 370, "EMAIL_VERIFICATION_CODE", code_fields, '#FEF3C7')

    # 4. AIRPORT
    airport_fields = [
        ("id", "INTEGER", "PK, autoincrement"),
        ("code", "VARCHAR(10)", "UK (IATA: SVO, DME, DXB)"),
        ("name", "VARCHAR(150)", "Название аэропорта"),
        ("city", "VARCHAR(100)", "Город"),
        ("country", "VARCHAR(100)", "Страна"),
        ("departures_count", "INTEGER", "Статистика вылетов"),
        ("arrivals_count", "INTEGER", "Статистика прилетов"),
        ("timezone", "VARCHAR(20)", "UTC+3, UTC+4 и др."),
    ]
    a_x, a_y, a_w, a_h = draw_table(40, 350, 360, "AIRPORT (flights_airport)", airport_fields, '#E2E8F0')

    # 5. FLIGHT
    flight_fields = [
        ("id", "INTEGER", "PK, autoincrement"),
        ("flight_id", "VARCHAR(50)", "UK slug (su-1702, s7-2041)"),
        ("flight_number", "VARCHAR(30)", "Номер рейса (SU 1702)"),
        ("airline", "VARCHAR(100)", "Авиакомпания"),
        ("aircraft", "VARCHAR(100)", "Модель борта (Airbus A350)"),
        ("from_code", "VARCHAR(10)", "FK -> flights_airport.code"),
        ("from_name", "VARCHAR(150)", "Аэропорт вылета"),
        ("from_city", "VARCHAR(100)", "Город вылета"),
        ("from_terminal", "VARCHAR(20)", "Терминал вылета"),
        ("from_gate", "VARCHAR(20)", "Гейт вылета"),
        ("to_code", "VARCHAR(10)", "FK -> flights_airport.code"),
        ("to_name", "VARCHAR(150)", "Аэропорт прилета"),
        ("to_city", "VARCHAR(100)", "Город прилета"),
        ("to_terminal", "VARCHAR(20)", "Терминал прилета"),
        ("to_gate", "VARCHAR(20)", "Гейт прилета"),
        ("departure_time", "VARCHAR(20)", "ЧЧ:ММ вылета"),
        ("arrival_time", "VARCHAR(20)", "ЧЧ:ММ прилета"),
        ("departure_date", "VARCHAR(20)", "ГГГГ-ММ-ДД"),
        ("duration", "VARCHAR(50)", "Время в пути"),
        ("status", "VARCHAR(30)", "scheduled, in_air, landed, etc."),
        ("status_text", "VARCHAR(100)", "По расписанию, В полёте..."),
        ("altitude", "INTEGER", "Высота (м)"),
        ("speed", "INTEGER", "Скорость (км/ч)"),
        ("price", "INTEGER", "Стоимость (руб)"),
        ("is_real_api", "BOOLEAN", "Синхронизировано из API"),
        ("created_at", "DATETIME", ""),
        ("updated_at", "DATETIME", "TTL удаление через 14 дней"),
    ]
    f_x, f_y, f_w, f_h = draw_table(460, 260, 480, "FLIGHT (flights_flight)", flight_fields, '#DCFCE7')

    # ================= RELATIONSHIP ARROWS =================
    c_line = '#1E3A8A'

    # 1. USER -> USER_PROFILE (1 : 1)
    # Line between u_x + u_w and p_x
    y_mid_up = 90
    draw.line([S(u_x + u_w), S(y_mid_up), S(p_x), S(y_mid_up)], fill=c_line, width=S(1.8))
    # 1:1 cross marks
    draw.line([S(u_x + u_w + 10), S(y_mid_up - 8), S(u_x + u_w + 10), S(y_mid_up + 8)], fill=c_line, width=S(1.8))
    draw.line([S(u_x + u_w + 16), S(y_mid_up - 8), S(u_x + u_w + 16), S(y_mid_up + 8)], fill=c_line, width=S(1.8))
    draw.line([S(p_x - 10), S(y_mid_up - 8), S(p_x - 10), S(y_mid_up + 8)], fill=c_line, width=S(1.8))
    draw.line([S(p_x - 16), S(y_mid_up - 8), S(p_x - 16), S(y_mid_up + 8)], fill=c_line, width=S(1.8))
    draw.text((S(u_x + u_w + 22), S(y_mid_up - 20)), "1 : 1 (Профиль)", font=font_rel, fill=c_line)

    # 2. USER -> EMAIL_VERIFICATION_CODE (1 : N)
    # Line from USER top/middle over or direct from USER_PROFILE to CODE
    draw.line([S(p_x + p_w), S(y_mid_up), S(c_x), S(y_mid_up)], fill=c_line, width=S(1.8))
    draw.line([S(p_x + p_w + 10), S(y_mid_up - 8), S(p_x + p_w + 10), S(y_mid_up + 8)], fill=c_line, width=S(1.8))
    # Crow foot at c_x
    draw.line([S(c_x - 14), S(y_mid_up - 8), S(c_x), S(y_mid_up)], fill=c_line, width=S(1.8))
    draw.line([S(c_x - 14), S(y_mid_up + 8), S(c_x), S(y_mid_up)], fill=c_line, width=S(1.8))
    draw.text((S(p_x + p_w + 15), S(y_mid_up - 20)), "1 : N (Коды подтверждения)", font=font_rel, fill=c_line)

    # 3. AIRPORT -> FLIGHT (1 : N for departures from_code)
    y_air_dep = 480
    draw.line([S(a_x + a_w), S(y_air_dep), S(f_x), S(y_air_dep)], fill=c_line, width=S(1.8))
    # 1 side
    draw.line([S(a_x + a_w + 10), S(y_air_dep - 8), S(a_x + a_w + 10), S(y_air_dep + 8)], fill=c_line, width=S(1.8))
    # N side (Crow foot)
    draw.line([S(f_x - 14), S(y_air_dep - 8), S(f_x), S(y_air_dep)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 14), S(y_air_dep + 8), S(f_x), S(y_air_dep)], fill=c_line, width=S(1.8))
    draw.text((S(a_x + a_w + 12), S(y_air_dep - 20)), "1 : N (from_code)", font=font_rel, fill=c_line)

    # 4. AIRPORT -> FLIGHT (1 : N for arrivals to_code)
    y_air_arr = 560
    draw.line([S(a_x + a_w), S(y_air_arr), S(f_x), S(y_air_arr)], fill=c_line, width=S(1.8))
    # 1 side
    draw.line([S(a_x + a_w + 10), S(y_air_arr - 8), S(a_x + a_w + 10), S(y_air_arr + 8)], fill=c_line, width=S(1.8))
    # N side (Crow foot)
    draw.line([S(f_x - 14), S(y_air_arr - 8), S(f_x), S(y_air_arr)], fill=c_line, width=S(1.8))
    draw.line([S(f_x - 14), S(y_air_arr + 8), S(f_x), S(y_air_arr)], fill=c_line, width=S(1.8))
    draw.text((S(a_x + a_w + 12), S(y_air_arr - 20)), "1 : N (to_code)", font=font_rel, fill=c_line)

    # Legend / Info box
    leg_x, leg_y, leg_w, leg_h = 980, 260, 280, 160
    draw.rectangle([S(leg_x), S(leg_y), S(leg_x + leg_w), S(leg_y + leg_h)], fill='#FAFBFD', outline='#94A3B8', width=S(1.2))
    draw.text((S(leg_x + 12), S(leg_y + 12)), "Условные обозначения:", font=font_title, fill='#1E293B')
    draw.text((S(leg_x + 12), S(leg_y + 40)), "• PK — Первичный ключ (Primary Key)", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 12), S(leg_y + 65)), "• FK — Внешний ключ (Foreign Key)", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 12), S(leg_y + 90)), "• UK — Ограничение уникальности", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 12), S(leg_y + 115)), "• 1 : 1 — Связь один к одному", font=font_field_reg, fill='#334155')
    draw.text((S(leg_x + 12), S(leg_y + 135)), "• 1 : N — Связь один ко многим", font=font_field_reg, fill='#334155')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"ER diagram PNG generated: {output_path}")

if __name__ == '__main__':
    generate_er_diagram_png()
