import os
from PIL import Image, ImageDraw, ImageFont

def generate_sequence_diagram_png(output_path='docs/sequence_diagram.png'):
    scale = 2
    w, h = 1600 * scale, 1080 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    font_path = 'C:/Windows/Fonts/arial.ttf'
    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'

    font_part = ImageFont.truetype(font_bold_path, 11 * scale)
    font_scenario = ImageFont.truetype(font_bold_path, 12 * scale)
    font_msg = ImageFont.truetype(font_path, 10 * scale)
    font_msg_bold = ImageFont.truetype(font_bold_path, 10 * scale)

    def S(val):
        return int(val * scale)

    # Participants
    participants = [
        {"id": "user", "name": "Пользователь", "x": 90},
        {"id": "ui", "name": "React SPA (UI)", "x": 300},
        {"id": "api", "name": "Сервисы (api.ts)", "x": 510},
        {"id": "django", "name": "Django REST API", "x": 750},
        {"id": "engine", "name": "Движок сервисов", "x": 1010},
        {"id": "db", "name": "СУБД SQLite 3", "x": 1260},
        {"id": "smtp", "name": "Яндекс SMTP (SSL)", "x": 1500},
    ]

    p_map = {p["id"]: p["x"] for p in participants}

    # Draw participant boxes at top and bottom
    for p in participants:
        px = p["x"]
        pw = 140
        # Top box
        draw.rectangle([S(px - pw/2), S(30), S(px + pw/2), S(70)], fill='#F8FAFC', outline='#334155', width=S(1.2))
        tb = font_part.getbbox(p["name"])
        draw.text((S(px) - (tb[2]-tb[0])/2, S(50) - (tb[3]-tb[1])/2), p["name"], font=font_part, fill='#0F172A')

        # Bottom box
        draw.rectangle([S(px - pw/2), S(1020), S(px + pw/2), S(1060)], fill='#F8FAFC', outline='#334155', width=S(1.2))
        draw.text((S(px) - (tb[2]-tb[0])/2, S(1040) - (tb[3]-tb[1])/2), p["name"], font=font_part, fill='#0F172A')

        # Lifeline
        draw.line([S(px), S(70), S(px), S(1020)], fill='#CBD5E1', width=S(1))

    # Helper: draw arrow
    def draw_msg(src_id, dst_id, y, text, is_return=False, color='#1E3A8A'):
        x1 = p_map[src_id]
        x2 = p_map[dst_id]

        # Line
        if is_return:
            # dashed line
            step = 6
            cur_x = min(x1, x2)
            max_x = max(x1, x2)
            while cur_x < max_x:
                draw.line([S(cur_x), S(y), S(min(cur_x + step, max_x)), S(y)], fill=color, width=S(1.3))
                cur_x += step * 2
        else:
            draw.line([S(x1), S(y), S(x2), S(y)], fill=color, width=S(1.4))

        # Arrowhead
        arrow_size = S(6)
        if x2 > x1:
            draw.polygon([(S(x2), S(y)), (S(x2) - arrow_size, S(y) - arrow_size*0.6), (S(x2) - arrow_size, S(y) + arrow_size*0.6)], fill=color)
        else:
            draw.polygon([(S(x2), S(y)), (S(x2) + arrow_size, S(y) - arrow_size*0.6), (S(x2) + arrow_size, S(y) + arrow_size*0.6)], fill=color)

        # Text label above arrow
        mid_x = (x1 + x2) / 2
        tb = font_msg.getbbox(text)
        tw = tb[2] - tb[0]
        draw.text((S(mid_x) - tw/2, S(y - 15)), text, font=font_msg, fill=color)

    # ================= СЦЕНАРИЙ 1 =================
    s1_y = 95
    draw.rectangle([S(20), S(s1_y), S(1580), S(s1_y + 355)], fill='#F0F9FF', outline='#BAE6FD', width=S(1.2))
    draw.text((S(35), S(s1_y + 12)), "Сценарий 1: Получение табло рейсов, симуляция 24/7 и автоочистка TTL", font=font_scenario, fill='#0369A1')

    steps_s1 = [
        ("user", "ui", s1_y + 45, "1. Ввод фильтра \"Сочи\" на странице /flights", False),
        ("ui", "api", s1_y + 75, "2. fetchFlights({ search: \"Сочи\" })", False),
        ("api", "django", s1_y + 105, "3. GET /api/flights/?search=Сочи", False),
        ("django", "engine", s1_y + 135, "4. update_dynamic_flight_lifecycle()", False),
        ("engine", "db", s1_y + 165, "5. cleanup_archived_flights (DELETE старше 14 дней)", False),
        ("db", "engine", s1_y + 195, "6. 0 устаревших рейсов удалено", True),
        ("engine", "db", s1_y + 225, "7. UPDATE статусов по часам (scheduled -> in_air -> landed)", False),
        ("db", "engine", s1_y + 255, "8. Статусы рейсов актуализированы", True),
        ("django", "db", s1_y + 285, "9. SELECT * FROM flights WHERE search LIKE '%Сочи%'", False),
        ("db", "django", s1_y + 310, "10. Строки рейсов (ORM Queryset)", True),
        ("django", "api", s1_y + 330, "11. 200 OK [JSON: flights]", True),
        ("api", "ui", s1_y + 348, "12. Рендеринг карточек рейсов (useMemo, 60 FPS)", True),
    ]

    for src, dst, y, txt, is_ret in steps_s1:
        draw_msg(src, dst, y, txt, is_ret, '#0284C7' if is_ret else '#1E3A8A')

    # ================= СЦЕНАРИЙ 2 =================
    s2_y = 480
    draw.rectangle([S(20), S(s2_y), S(1580), S(s2_y + 515)], fill='#FFFDF0', outline='#FDE68A', width=S(1.2))
    draw.text((S(35), S(s2_y + 12)), "Сценарий 2: Регистрация и верификация через 6-значный код Яндекс SMTP (SSL)", font=font_scenario, fill='#92400E')

    steps_s2 = [
        ("user", "ui", s2_y + 45, "13. Ввод email и пароля в модальном окне регистрации", False),
        ("ui", "api", s2_y + 75, "14. register({ email, password })", False),
        ("api", "django", s2_y + 105, "15. POST /api/auth/register/", False),
        ("django", "db", s2_y + 135, "16. INSERT auth_user (хэш PBKDF2), userprofile (verified=False)", False),
        ("db", "django", s2_y + 165, "17. Пользователь создан", True),
        ("django", "engine", s2_y + 195, "18. EmailVerificationCode.generate_for_user()", False),
        ("engine", "db", s2_y + 225, "19. INSERT 6-значный код (TTL: 15 минут)", False),
        ("db", "engine", s2_y + 255, "20. Код верификации сохранен", True),
        ("django", "smtp", s2_y + 285, "21. send_mail(код, to=email, port=465 SSL smtp.yandex.ru)", False),
        ("smtp", "django", s2_y + 315, "22. 250 Message accepted for delivery", True),
        ("django", "api", s2_y + 340, "23. 201 Created { message: \"Код отправлен на почту\" }", True),
        ("api", "ui", s2_y + 365, "24. Открытие 6 ячеек ввода (автофокус)", True),
        ("user", "ui", s2_y + 395, "25. Ввод 6-значного кода из почтового ящика", False),
        ("ui", "api", s2_y + 420, "26. verifyEmail({ email, code })", False),
        ("api", "django", s2_y + 445, "27. POST /api/auth/verify-email/", False),
        ("django", "db", s2_y + 470, "28. SELECT код WHERE is_used=False AND expires > now()", False),
        ("db", "django", s2_y + 488, "29. UPDATE userprofile SET is_verified=True, is_used=True", True),
        ("django", "ui", s2_y + 504, "30. 200 OK { token, user: verified } -> Вход в профиль", True),
    ]

    for src, dst, y, txt, is_ret in steps_s2:
        draw_msg(src, dst, y, txt, is_ret, '#D97706' if is_ret else '#1E3A8A')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"Sequence diagram PNG generated: {output_path}")

if __name__ == '__main__':
    generate_sequence_diagram_png()
