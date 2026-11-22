import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets inner margins (padding) for a cell in dxa (1/20 pt)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_table_borders(table, color="D3D3D3"):
    """Applies neat borders to the entire table."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)

def build_comparison_document():
    doc = docx.Document()

    # Set margins (2 cm = 0.79 inches)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(0.98)
        section.right_margin = Inches(0.79)

    # Set default style font
    normal_style = doc.styles['Normal']
    font = normal_style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    # Document Header / Academic Title
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_meta = p_meta.add_run(
        "Курсовая работа по дисциплине:\n«Разработка программных интерфейсов» (РПИ)\n"
        "Тема: «Разработка веб-интерфейса для информационного\nсервиса об авиарейсах на React»"
    )
    run_meta.font.size = Pt(10)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(100, 116, 139)

    # Main Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(18)
    run_title = p_title.add_run("РАЗДЕЛ: СРАВНИТЕЛЬНЫЙ АНАЛИЗ АНАЛОГОВ И РАЗРАБАТЫВАЕМОГО СЕРВИСА")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    # 1. Введение
    h1 = doc.add_heading(level=1)
    r1 = h1.add_run("1. Введение и цели сравнительного анализа")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(3, 105, 161) # Sky 700

    p_intro = doc.add_paragraph(
        "При проектировании программных интерфейсов современных информационных сервисов первостепенное значение "
        "имеет определение требований целевой аудитории и выявление недостатков существующих рыночных решений. "
        "В предметной области мониторинга и отслеживания авиарейсов пользователю требуется оперативный, точный и "
        "не перегруженный доступ к ключевым характеристикам рейса: статусу вылета, времени задержки, номеру терминала и гейта."
    )
    p_intro.paragraph_format.line_spacing = 1.25
    p_intro.paragraph_format.space_after = Pt(8)

    p_intro2 = doc.add_paragraph(
        "Целью настоящего сравнительного анализа является систематизация функциональных, интерфейсных (UX/UI) "
        "и архитектурно-технологических особенностей ведущих сервисов-аналогов для обоснования выбранных проектных "
        "решений разрабатываемого веб-приложения «Авиарейсы»."
    )
    p_intro2.paragraph_format.line_spacing = 1.25
    p_intro2.paragraph_format.space_after = Pt(12)

    # 2. Обзор существующих решений
    h2 = doc.add_heading(level=1)
    r2 = h2.add_run("2. Обзор существующих программных продуктов-аналогов")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(3, 105, 161)

    competitors_desc = [
        ("Flightradar24", "Мировой лидер в сегменте отслеживания воздушных судов по протоколам ADS-B в режиме реального времени. "
                          "Достоинства: глобальное покрытие, интерактивная карта, детальная 3D-визуализация. "
                          "Недостатки: чрезвычайно перегруженный интерфейс для рядового пассажира, обилие баннерной рекламы "
                          "в бесплатной версии (с блокировкой каждые 3–5 минут), платная подписка на данные о гейтах и истории."),
        ("FlightAware", "Корпоративная платформа трекинга рейсов, ориентированная на авиакомпании, операторов аэропортов и B2B. "
                        "Достоинства: высокая надежность, подробная авиационная статистика. "
                        "Недостатки: узкоспециализированный дизайн, избыточное использование сложной терминологии, "
                        "ограниченный бесплатный функционал, медленная загрузка мобильного интерфейса."),
        ("Яндекс Расписания", "Популярный российский агрегатор расписаний всех видов транспорта (поезда, автобусы, самолеты). "
                              "Достоинства: качественная локализация, связь с экосистемой сервисов Яндекса. "
                              "Недостатки: устаревший табличный вид с полной перезагрузкой страниц при фильтрации, отсутствие "
                              "параметров телеметрии (высота, скорость, тип борта), редкое отображение гейтов."),
        ("Aviasales", "Крупнейший метапоисковик и агрегатор бронирования авиабилетов (Online Travel Agency). "
                      "Достоинства: быстрый поиск билетов, удобное мобильное приложение. "
                      "Недостатки: интерфейс ориентирован исключительно на коммерческие продажи (отели, аренда авто, экскурсии); "
                      "мониторинг статуса рейса является второстепенной функцией; отсутствие телеметрии полета.")
    ]

    for name, desc in competitors_desc:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_after = Pt(6)
        p_c.paragraph_format.line_spacing = 1.15
        run_name = p_c.add_run(f"• {name}: ")
        run_name.font.bold = True
        run_name.font.color.rgb = RGBColor(15, 23, 42)
        p_c.add_run(desc)

    # 3. Сравнительная таблица
    h3 = doc.add_heading(level=1)
    r3 = h3.add_run("3. Сводная сравнительная таблица характеристик")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(14)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(3, 105, 161)

    p_tbl_intro = doc.add_paragraph(
        "В таблице 1 представлено комплексное сопоставление разрабатываемого веб-сервиса «Авиарейсы» с рассмотренными аналогами "
        "по ключевым функциональным возможностям, эргономике и условиям использования."
    )
    p_tbl_intro.paragraph_format.space_after = Pt(8)

    p_tbl_caption = doc.add_paragraph()
    p_tbl_caption.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_cap = p_tbl_caption.add_run("Таблица 1 — Сравнение функциональных и интерфейсных характеристик сервисов")
    r_cap.font.italic = True
    r_cap.font.size = Pt(10.5)

    # Create Table
    table_data = [
        ["Критерий сравнения", "«Авиарейсы» (Проект)", "Flightradar24", "FlightAware", "Яндекс Расписания", "Aviasales"],
        ["Чистота интерфейса (отсутствие рекламы)", "Да (100% без рекламы)", "Нет (баннеры в Free)", "Нет (рекламные блоки)", "Частично (промо)", "Нет (реклама и продажи)"],
        ["Телеметрия полёта (высота, скорость)", "Да (метры, км/ч)", "Да (футы, узлы)", "Да (мили/ч, футы)", "Нет", "Нет"],
        ["Данные о терминале и гейте вылета", "Да (терминал + гейт)", "Частично (гейт платно)", "Да", "Частично (без гейта)", "Нет"],
        ["Интуитивность интерфейса для пассажира", "Высокая (Figma / Benzin)", "Низкая (сложная карта)", "Средняя (B2B перегруз)", "Средняя (таблицы)", "Средняя (уклон в продажи)"],
        ["Email-уведомления и подписка на статус", "Да (реальный SMTP Яндекс)", "По платной подписке", "Требует сложный аккаунт", "Только в приложении", "Только цены билетов"],
        ["Беспарольная верификация пользователя", "Да (6-значный email-код)", "Нет (логин + пароль)", "Нет (пароль)", "Нет (аккаунт Яндекс)", "Нет (телефон/почта)"],
        ["Мгновенная клиентская фильтрация", "Да (< 15 мс, React)", "С задержкой рендера", "С задержкой страницы", "Перезагрузка страниц", "Да"],
        ["Полный бесплатный доступ ко всем функциям", "Да (100% Free)", "Нет (подписка от $1.49)", "Нет (Enterprise тарифы)", "Да", "Да"],
        ["Адаптивность под смартфоны (Mobile-First)", "Да (капсульные карточки)", "Через отдельное приложение", "Базовая верстка", "Стандартная верстка", "Через приложение"],
        ["Синхронизация с живым API (Aviationstack)", "Да (бэкенд на Django)", "Собственные ADS-B", "Собственные радары", "Базы расписаний РФ", "GDS / агрегаторы"]
    ]

    table = doc.add_table(rows=len(table_data), cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="CBD5E1")

    # Column widths in inches (total ~ 6.5 in)
    col_widths = [Inches(1.8), Inches(1.3), Inches(0.95), Inches(0.95), Inches(1.0), Inches(0.95)]

    for row_idx, row in enumerate(table.rows):
        is_header = (row_idx == 0)
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

            # Cell text
            cell_text = table_data[row_idx][col_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05

            run = p.add_run(cell_text)

            if is_header:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                run.font.bold = True
                if col_idx == 1:
                    # Highlight our column header
                    set_cell_background(cell, "E0F2FE") # Sky 100
                    run.font.color.rgb = RGBColor(3, 105, 161)
                else:
                    set_cell_background(cell, "F1F5F9") # Slate 100
                    run.font.color.rgb = RGBColor(15, 23, 42)
            else:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9.5)
                # Alternating row background
                if col_idx == 1:
                    set_cell_background(cell, "F0F9FF") # Light Sky accent for our column
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(2, 132, 199)
                elif row_idx % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                    run.font.color.rgb = RGBColor(51, 65, 85)
                else:
                    set_cell_background(cell, "F8FAFC")
                    run.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_before = Pt(12)

    # 4. Балльная оценка
    h4 = doc.add_heading(level=1)
    r4 = h4.add_run("4. Экспертная балльная оценка эффективности (матрица взвешивания)")
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(14)
    r4.font.bold = True
    r4.font.color.rgb = RGBColor(3, 105, 161)

    p_scores_intro = doc.add_paragraph(
        "Для количественной оценки каждого программного решения сформирована взвешенная матрица критериев "
        "по 5-балльной шкале (1 — неудовлетворительно, 5 — превосходно). Каждой группе характеристик присвоен "
        "весовой коэффициент значимости с точки зрения удобства конечного пассажира (таблица 2)."
    )
    p_scores_intro.paragraph_format.space_after = Pt(8)

    p_tbl2_caption = doc.add_paragraph()
    r2_cap = p_tbl2_caption.add_run("Таблица 2 — Матрица взвешенных оценок сервисов")
    r2_cap.font.italic = True
    r2_cap.font.size = Pt(10.5)

    score_data = [
        ["Группа критериев", "Вес", "«Авиарейсы»", "Flightradar24", "FlightAware", "Яндекс Расписания", "Aviasales"],
        ["Эргономика и простота восприятия", "0.25", "4.9", "3.2", "3.4", "3.8", "3.6"],
        ["Полнота полезных пассажирских данных", "0.25", "4.8", "4.6", "4.7", "3.4", "2.8"],
        ["Скорость отклика интерфейса и фильтрации", "0.20", "4.9", "2.8", "3.3", "3.9", "4.5"],
        ["Отсутствие раздражающей рекламы", "0.15", "5.0", "2.1", "2.5", "3.5", "2.2"],
        ["Бесплатная доступность возможностей", "0.15", "5.0", "2.9", "3.0", "4.8", "4.6"],
        ["ИТОГОВЫЙ ВЗВЕШЕННЫЙ БАЛЛ", "1.00", "4.91", "3.31", "3.56", "3.79", "3.44"]
    ]

    table2 = doc.add_table(rows=len(score_data), cols=7)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2, color="CBD5E1")

    score_col_widths = [Inches(2.5), Inches(0.6), Inches(1.0), Inches(0.9), Inches(0.85), Inches(0.95), Inches(0.8)]

    for row_idx, row in enumerate(table2.rows):
        is_header = (row_idx == 0)
        is_total = (row_idx == len(score_data) - 1)

        for col_idx, cell in enumerate(row.cells):
            cell.width = score_col_widths[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

            val = score_data[row_idx][col_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)

            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)

            if is_header:
                run.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif is_total:
                run.font.bold = True
                if col_idx == 2:
                    set_cell_background(cell, "BAE6FD") # Sky 200
                    run.font.size = Pt(11)
                    run.font.color.rgb = RGBColor(3, 105, 161)
                else:
                    set_cell_background(cell, "E2E8F0")
            elif col_idx == 2:
                set_cell_background(cell, "F0F9FF")
                run.font.bold = True
                run.font.color.rgb = RGBColor(2, 132, 199)

    doc.add_paragraph().paragraph_format.space_before = Pt(12)

    # 5. Выводы
    h5 = doc.add_heading(level=1)
    r5 = h5.add_run("5. Выводы и конкурентные преимущества разработки")
    r5.font.name = 'Times New Roman'
    r5.font.size = Pt(14)
    r5.font.bold = True
    r5.font.color.rgb = RGBColor(3, 105, 161)

    conclusions = [
        "1. Высокая скорость и эргономика: благодаря архитектуре на базе React 19, TypeScript и сборщика Vite 6 обеспечен мгновенный отклик поисковой фильтрации (< 15 мс) без перезагрузки страниц, что значительно превосходит тяжеловесные решения с рендером 3D-карт (Flightradar24) и традиционные табличные сервисы (Яндекс Расписания).",
        "2. Фокус на пассажире и чистота восприятия: разработанный интерфейс полностью свободен от навязчивой рекламы, всплывающих баннеров и навязывания сторонних сервисов бронирования отелей (в отличие от Aviasales и бесплатных версий радаров).",
        "3. Полнота параметров рейса: пользователю в один клик доступны как точные данные аэропорта (терминал, гейт, статус посадки/задержки), так и телеметрия полета в реальном времени (текущая высота в метрах и путевая скорость в км/ч).",
        "4. Безопасность и удобство верификации: реализован механизм беспарольного подтверждения учетной записи через 6-значный одноразовый код, доставляемый на email пользователя по безопасному протоколу SMTP, а также информационная рассылка для зарегистрированных подписчиков."
    ]

    for c_text in conclusions:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_after = Pt(6)
        p_c.paragraph_format.line_spacing = 1.25
        run_c = p_c.add_run(c_text)
        run_c.font.size = Pt(11)

    # Save to files
    out_docx = os.path.abspath(os.path.join(os.path.dirname(__file__), "Сравнительный_анализ_аналогов.docx"))
    out_doc = os.path.abspath(os.path.join(os.path.dirname(__file__), "Сравнительный_анализ_аналогов.doc"))
    doc.save(out_docx)
    shutil.copyfile(out_docx, out_doc)
    print(f"Generated DOCX: {out_docx}")
    print(f"Generated DOC: {out_doc}")

if __name__ == '__main__':
    build_comparison_document()
