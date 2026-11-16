import os
from PIL import Image, ImageDraw, ImageFont

def generate_updated_sequence_diagram_png(output_path='docs/sequence_diagram.png'):
    scale = 2
    w, h = 1750 * scale, 1420 * scale

    # Pure white background
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    font_path = 'C:/Windows/Fonts/arial.ttf'
    font_bold_path = 'C:/Windows/Fonts/arialbd.ttf'

    font_part = ImageFont.truetype(font_bold_path, 11 * scale)
    font_scenario = ImageFont.truetype(font_bold_path, 12 * scale)
    font_msg = ImageFont.truetype(font_path, 9.5 * scale)
    font_msg_bold = ImageFont.truetype(font_bold_path, 9.5 * scale)

    def S(val):
        return int(val * scale)

    # 8 Participants (Включая Django ORM как отдельную линию жизни!)
    participants = [
        {"id": "user", "name": "Пользователь", "x": 80},
        {"id": "ui", "name": "React SPA (UI)", "x": 280},
        {"id": "api", "name": "Сервисы (api.ts)", "x": 480},
        {"id": "django", "name": "Django REST API", "x": 700},
        {"id": "engine", "name": "Движок сервисов", "x": 920},
        {"id": "orm", "name": "Django ORM", "x": 1130},
        {"id": "db", "name": "СУБД SQLite 3", "x": 1350},
        {"id": "smtp", "name": "Яндекс SMTP (SSL)", "x": 1580},
    ]

    p_map = {p["id"]: p["x"] for p in participants}

    # Draw participant boxes at top and bottom
    for p in participants:
        px = p["x"]
        pw = 145
        # Top box
        draw.rectangle([S(px - pw/2), S(30), S(px + pw/2), S(70)], fill='#F8FAFC', outline='#334155', width=S(1.2))
        tb = font_part.getbbox(p["name"])
        draw.text((S(px) - (tb[2]-tb[0])/2, S(50) - (tb[3]-tb[1])/2), p["name"], font=font_part, fill='#0F172A')

        # Bottom box
        draw.rectangle([S(px - pw/2), S(1350), S(px + pw/2), S(1390)], fill='#F8FAFC', outline='#334155', width=S(1.2))
        draw.text((S(px) - (tb[2]-tb[0])/2, S(1370) - (tb[3]-tb[1])/2), p["name"], font=font_part, fill='#0F172A')

        # Lifeline
        draw.line([S(px), S(70), S(px), S(1350)], fill='#CBD5E1', width=S(1))

    # Helper: draw arrow
    def draw_msg(src_id, dst_id, y, text, is_return=False, color='#1E3A8A'):
        x1 = p_map[src_id]
        x2 = p_map[dst_id]

        # Line
        if is_return:
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
        draw.text((S(mid_x) - tw/2, S(y - 14)), text, font=font_msg, fill=color)

    # ================= 1. ФОНОВЫЙ ПРОЦЕСС (loop: независимый цикл 24/7) =================
    b1_y = 90
    draw.rectangle([S(20), S(b1_y), S(1710), S(b1_y + 245)], fill='#F8FAFC', outline='#94A3B8', width=S(1.2))
    draw.rectangle([S(20), S(b1_y), S(380), S(b1_y + 28)], fill='#E2E8F0', outline='#94A3B8', width=S(1.2))
    draw.text((S(28), S(b1_y + 7)), "loop [Фоновый процесс: Демон жизненного цикла 24/7]", font=font_msg_bold, fill='#0F172A')

    steps_bg = [
        ("engine", "orm", b1_y + 45, "1. cleanup_archived_flights()", False),
        ("orm", "db", b1_y + 70, "2. DELETE FROM flights WHERE status IN ('landed','cancelled') AND updated_at < now() - 14 дн", False),
        ("db", "orm", b1_y + 95, "3. Результат SQL (0 записей удалено)", True),
        ("orm", "engine", b1_y + 118, "4. Подтверждение очистки TTL", True),
        ("engine", "orm", b1_y + 142, "5. update_dynamic_flight_lifecycle() (пересчет по текущему времени)", False),
        ("orm", "db", b1_y + 167, "6. UPDATE flights SET status = 'in_air' / 'landed' WHERE ...", False),
        ("db", "orm", b1_y + 192, "7. Статусы рейсов актуализированы в базе", True),
        ("orm", "engine", b1_y + 215, "8. Итерация фонового цикла завершена", True),
    ]
    for src, dst, y, txt, is_ret in steps_bg:
        draw_msg(src, dst, y, txt, is_ret, '#475569' if is_ret else '#0F172A')

    # ================= 2. ОСНОВНОЙ ПРОЦЕСС: ПОЛУЧЕНИЕ СПИСКА РЕЙСОВ =================
    b2_y = 355
    draw.rectangle([S(20), S(b2_y), S(1710), S(b2_y + 295)], fill='#F0F9FF', outline='#BAE6FD', width=S(1.2))
    draw.text((S(35), S(b2_y + 12)), "Сценарий 1: Получение табло рейсов и фильтрация (Основной пользовательский процесс)", font=font_scenario, fill='#0369A1')

    steps_s1 = [
        ("user", "ui", b2_y + 45, "9. Ввод фильтра \"Сочи\" на странице /flights", False),
        ("ui", "api", b2_y + 75, "10. fetchFlights({ search: \"Сочи\" })", False),
        ("api", "django", b2_y + 105, "11. GET /api/flights/?search=Сочи", False),
        ("django", "orm", b2_y + 135, "12. Flight.objects.filter(Q(from_city__icontains=...) | Q(to_city__icontains=...))", False),
        ("orm", "db", b2_y + 165, "13. SELECT * FROM flights_flight WHERE search LIKE '%Сочи%'", False),
        ("db", "orm", b2_y + 195, "14. Результат SQL-запроса (строки данных)", True),
        ("orm", "django", b2_y + 220, "15. QuerySet объектов моделей Flight", True),
        ("django", "api", b2_y + 245, "16. 200 OK [JSON: flights (camelCase)]", True),
        ("api", "ui", b2_y + 268, "17. Обновление состояния (стейта useMemo)", True),
        ("ui", "user", b2_y + 288, "18. Отрисовка карточек рейсов (60 FPS)", True),
    ]
    for src, dst, y, txt, is_ret in steps_s1:
        draw_msg(src, dst, y, txt, is_ret, '#0284C7' if is_ret else '#1E3A8A')

    # ================= 3. РЕГИСТРАЦИЯ И ВЕРИФИКАЦИЯ EMAIL =================
    b3_y = 670
    draw.rectangle([S(20), S(b3_y), S(1710), S(b3_y + 660)], fill='#FFFDF0', outline='#FDE68A', width=S(1.2))
    draw.text((S(35), S(b3_y + 12)), "Сценарий 2: Регистрация и подтверждение email через Яндекс SMTP (SSL)", font=font_scenario, fill='#92400E')

    steps_s2 = [
        ("user", "ui", b3_y + 45, "19. Ввод email и пароля в форме регистрации", False),
        ("ui", "api", b3_y + 72, "20. register({ email, password })", False),
        ("api", "django", b3_y + 98, "21. POST /api/auth/register/", False),
        ("django", "orm", b3_y + 125, "22. User.objects.create_user(), UserProfile.objects.create()", False),
        ("orm", "db", b3_y + 152, "23. INSERT INTO auth_user (хэш PBKDF2), accounts_userprofile", False),
        ("db", "orm", b3_y + 178, "24. Записи созданы", True),
        ("orm", "django", b3_y + 202, "25. Пользователь сохранен", True),
        ("django", "orm", b3_y + 228, "26. EmailVerificationCode.generate_for_user()", False),
        ("orm", "db", b3_y + 254, "27. INSERT INTO accounts_emailverificationcode (код, created_at)", False),
        ("db", "orm", b3_y + 279, "28. Код верификации сохранен", True),
        ("orm", "django", b3_y + 303, "29. Код готов к отправке", True),
        ("django", "smtp", b3_y + 330, "30. send_mail(код, to=email, port=465 SSL smtp.yandex.ru)", False),
        ("smtp", "django", b3_y + 356, "31. 250 Message accepted for delivery", True),
        ("django", "api", b3_y + 382, "32. 201 Created { message: \"Код отправлен на почту\" }", True),
        ("api", "ui", b3_y + 406, "33. Открытие формы ввода 6-значного кода", True),
        ("user", "ui", b3_y + 434, "34. Ввод 6-значного кода из почты", False),
        ("ui", "api", b3_y + 460, "35. verifyEmail({ email, code })", False),
        ("api", "django", b3_y + 486, "36. POST /api/auth/verify-email/", False),
        ("django", "orm", b3_y + 512, "37. EmailVerificationCode.objects.filter(code=..., is_used=False)", False),
        ("orm", "db", b3_y + 538, "38. SELECT * WHERE code = '...' AND is_used = FALSE AND (now() - created_at) <= 15 мин", False),
        ("db", "orm", b3_y + 562, "39. Код найден и валиден", True),
        ("orm", "django", b3_y + 584, "40. Подтверждение валидности кода", True),
        ("django", "orm", b3_y + 608, "41. Раздельное обновление: profile.is_email_verified = True, code.is_used = True", False),
        ("orm", "db", b3_y + 630, "42. UPDATE accounts_userprofile SET is_email_verified = TRUE; UPDATE accounts_emailverificationcode SET is_used = TRUE", False),
        ("db", "orm", b3_y + 652, "43. Данные обновлены в SQLite", True),
        ("orm", "django", b3_y + 672, "44. Транзакция успешно зафиксирована", True),
        ("django", "api", b3_y + 692, "45. 200 OK — Электронная почта подтверждена", True),
        ("api", "ui", b3_y + 712, "46. Обновление статуса в интерфейсе", True),
        ("ui", "user", b3_y + 730, "47. Уведомление об успешном подтверждении почты", True),
    ]
    for src, dst, y, txt, is_ret in steps_s2:
        draw_msg(src, dst, y, txt, is_ret, '#D97706' if is_ret else '#1E3A8A')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"Updated Sequence diagram PNG generated: {output_path}")

if __name__ == '__main__':
    generate_updated_sequence_diagram_png()
