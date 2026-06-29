"""Ikki tilli matnlar: UZ / RU."""

TEXTS = {
    # ===== Umumiy =====
    "choose_lang": {
        "uz": "Tilni tanlang / Выберите язык:",
        "ru": "Tilni tanlang / Выберите язык:",
    },
    "lang_set": {"uz": "✅ Til o'rnatildi: O'zbekcha", "ru": "✅ Язык установлен: Русский"},
    "welcome_admin": {
        "uz": "👨‍💼 Salom, {name}!\nSiz <b>menejer (admin)</b> sifatida kirdingiz.\nQuyidagi menyudan foydalaning:",
        "ru": "👨‍💼 Здравствуйте, {name}!\nВы вошли как <b>менеджер (админ)</b>.\nИспользуйте меню ниже:",
    },
    "welcome_employee": {
        "uz": "👋 Salom, {name}!\nSiz <b>xodim</b> sifatida ro'yxatdan o'tdingiz.\nQuyidagi menyudan foydalaning:",
        "ru": "👋 Здравствуйте, {name}!\nВы зарегистрированы как <b>сотрудник</b>.\nИспользуйте меню ниже:",
    },
    "menu": {"uz": "🏠 Asosiy menyu", "ru": "🏠 Главное меню"},
    "back": {"uz": "⬅️ Orqaga", "ru": "⬅️ Назад"},
    "cancel": {"uz": "❌ Bekor qilish", "ru": "❌ Отмена"},
    "cancelled": {"uz": "Bekor qilindi.", "ru": "Отменено."},
    "not_allowed": {"uz": "⛔ Bu amal uchun ruxsat yo'q.", "ru": "⛔ Нет доступа к этому действию."},
    "none": {"uz": "— bo'sh —", "ru": "— пусто —"},
    "skip": {"uz": "⏭ O'tkazib yuborish", "ru": "⏭ Пропустить"},

    # ===== Admin menyu tugmalari =====
    "btn_new_task": {"uz": "➕ Vazifa berish", "ru": "➕ Поставить задачу"},
    "btn_all_tasks": {"uz": "📋 Barcha vazifalar", "ru": "📋 Все задачи"},
    "btn_accept_tasks": {"uz": "✅ Qabul qilish (bajarilgan)", "ru": "✅ Приёмка (выполненные)"},
    "btn_new_issue": {"uz": "⚠️ Xato/kamchilik", "ru": "⚠️ Ошибка/замечание"},
    "btn_open_issues": {"uz": "🔧 Ochiq kamchiliklar", "ru": "🔧 Открытые замечания"},
    "btn_reports": {"uz": "🗒 Bugungi hisobotlar", "ru": "🗒 Отчёты за сегодня"},
    "btn_attendance": {"uz": "🕒 Davomat", "ru": "🕒 Посещаемость"},
    "btn_employees": {"uz": "👥 Xodimlar", "ru": "👥 Сотрудники"},
    "btn_broadcast": {"uz": "📢 E'lon yuborish", "ru": "📢 Рассылка"},

    # ===== Xodim menyu tugmalari =====
    "btn_my_tasks": {"uz": "📋 Mening vazifalarim", "ru": "📋 Мои задачи"},
    "btn_send_report": {"uz": "🗒 Hisobot yuborish", "ru": "🗒 Отправить отчёт"},
    "btn_my_issues": {"uz": "⚠️ Mening kamchiliklarim", "ru": "⚠️ Мои замечания"},
    "btn_checkin": {"uz": "🟢 Ishga keldim", "ru": "🟢 Пришёл на работу"},
    "btn_checkout": {"uz": "🔴 Ishdan ketdim", "ru": "🔴 Ушёл с работы"},
    "btn_lang": {"uz": "🌐 Til", "ru": "🌐 Язык"},

    # ===== Vazifa yaratish =====
    "ask_task_assignee": {"uz": "Vazifa kimga beriladi? Xodimni tanlang:", "ru": "Кому поставить задачу? Выберите сотрудника:"},
    "ask_task_title": {"uz": "✍️ Vazifa sarlavhasini yozing:", "ru": "✍️ Введите заголовок задачи:"},
    "ask_task_desc": {"uz": "📝 Vazifa tafsilotini yozing (yoki o'tkazib yuboring):", "ru": "📝 Введите описание задачи (или пропустите):"},
    "ask_task_deadline": {
        "uz": "⏰ Muddatni kiriting: <code>YYYY-MM-DD SOAT:DAQIQA</code>\nMisol: <code>2026-07-05 18:00</code>\nYoki muddatsiz uchun o'tkazib yuboring.",
        "ru": "⏰ Введите срок: <code>ГГГГ-ММ-ДД ЧАС:МИН</code>\nПример: <code>2026-07-05 18:00</code>\nИли пропустите, если без срока.",
    },
    "bad_deadline": {"uz": "❌ Sana formati noto'g'ri. Misol: 2026-07-05 18:00", "ru": "❌ Неверный формат даты. Пример: 2026-07-05 18:00"},
    "task_created_admin": {"uz": "✅ Vazifa #{id} yaratildi va xodimga yuborildi.", "ru": "✅ Задача #{id} создана и отправлена сотруднику."},
    "task_new_for_employee": {
        "uz": "🆕 <b>Yangi vazifa #{id}</b>\n\n📌 {title}\n{desc}⏰ Muddat: {deadline}\n👤 Bergan: {creator}",
        "ru": "🆕 <b>Новая задача #{id}</b>\n\n📌 {title}\n{desc}⏰ Срок: {deadline}\n👤 Поставил: {creator}",
    },

    # ===== Vazifa holatlari =====
    "btn_start_task": {"uz": "▶️ Boshladim", "ru": "▶️ Начал"},
    "btn_done_task": {"uz": "✅ Bajardim", "ru": "✅ Выполнил"},
    "task_started": {"uz": "▶️ Vazifa #{id} ishga olindi.", "ru": "▶️ Задача #{id} взята в работу."},
    "task_done_employee": {"uz": "✅ Vazifa #{id} bajarildi deb belgilandi. Menejer tasdiqlaydi.", "ru": "✅ Задача #{id} отмечена выполненной. Менеджер подтвердит."},
    "task_done_notify_admin": {
        "uz": "✅ <b>{name}</b> vazifani bajardi:\n#{id} — {title}\n\nQabul qilasizmi?",
        "ru": "✅ <b>{name}</b> выполнил задачу:\n#{id} — {title}\n\nПринять?",
    },
    "btn_accept": {"uz": "👍 Qabul qilaman", "ru": "👍 Принять"},
    "btn_reject": {"uz": "👎 Qaytaraman", "ru": "👎 Вернуть"},
    "task_accepted": {"uz": "👍 Vazifa #{id} qabul qilindi. Rahmat!", "ru": "👍 Задача #{id} принята. Спасибо!"},
    "task_accepted_admin": {"uz": "👍 Vazifa #{id} qabul qilindi.", "ru": "👍 Задача #{id} принята."},
    "task_rejected": {"uz": "👎 Vazifa #{id} qaytarildi. Iltimos, qayta ko'rib chiqing.", "ru": "👎 Задача #{id} возвращена. Пожалуйста, доработайте."},
    "task_rejected_admin": {"uz": "👎 Vazifa #{id} xodimga qaytarildi.", "ru": "👎 Задача #{id} возвращена сотруднику."},
    "no_tasks": {"uz": "📭 Ochiq vazifalaringiz yo'q.", "ru": "📭 У вас нет открытых задач."},
    "no_tasks_admin": {"uz": "📭 Hozircha vazifalar yo'q.", "ru": "📭 Пока нет задач."},
    "no_pending": {"uz": "📭 Qabul qilishni kutayotgan vazifa yo'q.", "ru": "📭 Нет задач, ожидающих приёмки."},

    # ===== Hisobot =====
    "ask_report": {"uz": "🗒 Bugun nima ish qildingiz? Hisobotni yozing:", "ru": "🗒 Что вы сделали сегодня? Напишите отчёт:"},
    "report_saved": {"uz": "✅ Hisobotingiz saqlandi va menejerga yuborildi. Rahmat!", "ru": "✅ Ваш отчёт сохранён и отправлен менеджеру. Спасибо!"},
    "report_notify_admin": {"uz": "🗒 <b>{name}</b> hisobot yubordi:\n\n{text}", "ru": "🗒 <b>{name}</b> прислал отчёт:\n\n{text}"},
    "reports_header": {"uz": "🗒 <b>Bugungi hisobotlar ({day})</b>", "ru": "🗒 <b>Отчёты за сегодня ({day})</b>"},
    "no_reports": {"uz": "📭 Bugun hali hisobot yo'q.", "ru": "📭 Сегодня отчётов пока нет."},

    # ===== Xato / kamchilik =====
    "ask_issue_target": {"uz": "Kamchilik kimga tegishli? Xodimni tanlang:", "ru": "Кому адресовано замечание? Выберите сотрудника:"},
    "ask_issue_text": {"uz": "⚠️ Xato/kamchilikni yozing:", "ru": "⚠️ Опишите ошибку/замечание:"},
    "ask_issue_severity": {"uz": "Muhimlik darajasini tanlang:", "ru": "Выберите уровень важности:"},
    "sev_low": {"uz": "🟢 Past", "ru": "🟢 Низкий"},
    "sev_normal": {"uz": "🟡 O'rta", "ru": "🟡 Средний"},
    "sev_high": {"uz": "🔴 Yuqori", "ru": "🔴 Высокий"},
    "issue_created_admin": {"uz": "✅ Kamchilik #{id} xodimga yetkazildi.", "ru": "✅ Замечание #{id} отправлено сотруднику."},
    "issue_for_employee": {
        "uz": "⚠️ <b>Kamchilik #{id}</b> ({sev})\n\n{text}\n\n👤 Bildirgan: {creator}\nTuzatgach «✅ Tuzatdim» tugmasini bosing.",
        "ru": "⚠️ <b>Замечание #{id}</b> ({sev})\n\n{text}\n\n👤 Указал: {creator}\nПосле исправления нажмите «✅ Исправил».",
    },
    "btn_fix_issue": {"uz": "✅ Tuzatdim", "ru": "✅ Исправил"},
    "issue_fixed_employee": {"uz": "✅ Kamchilik #{id} tuzatildi deb belgilandi.", "ru": "✅ Замечание #{id} отмечено как исправленное."},
    "issue_fixed_admin": {"uz": "✅ <b>{name}</b> kamchilik #{id} ni tuzatdi.", "ru": "✅ <b>{name}</b> исправил замечание #{id}."},
    "issues_header": {"uz": "🔧 <b>Ochiq kamchiliklar</b>", "ru": "🔧 <b>Открытые замечания</b>"},
    "my_issues_header": {"uz": "⚠️ <b>Sizdagi ochiq kamchiliklar</b>", "ru": "⚠️ <b>Ваши открытые замечания</b>"},
    "no_issues": {"uz": "👍 Ochiq kamchilik yo'q.", "ru": "👍 Открытых замечаний нет."},

    # ===== Davomat =====
    "checkin_ok": {"uz": "🟢 Ishga kelganingiz qayd etildi: {time}", "ru": "🟢 Приход зафиксирован: {time}"},
    "checkin_already": {"uz": "ℹ️ Siz bugun allaqachon kelgansiz: {time}", "ru": "ℹ️ Вы уже отмечались сегодня: {time}"},
    "checkout_ok": {"uz": "🔴 Ishdan ketganingiz qayd etildi: {time}", "ru": "🔴 Уход зафиксирован: {time}"},
    "checkout_no_in": {"uz": "❗ Avval «🟢 Ishga keldim» tugmasini bosing.", "ru": "❗ Сначала нажмите «🟢 Пришёл на работу»."},
    "attendance_header": {"uz": "🕒 <b>Davomat ({day})</b>", "ru": "🕒 <b>Посещаемость ({day})</b>"},
    "no_attendance": {"uz": "📭 Bugun davomat belgilanmagan.", "ru": "📭 Сегодня посещаемость не отмечена."},

    # ===== Xodimlar boshqaruvi =====
    "employees_header": {"uz": "👥 <b>Xodimlar ro'yxati</b>\n(Boshqarish uchun ustiga bosing)", "ru": "👥 <b>Список сотрудников</b>\n(Нажмите для управления)"},
    "no_employees": {"uz": "📭 Hali xodimlar yo'q. Ular /start bossin.", "ru": "📭 Сотрудников пока нет. Пусть нажмут /start."},
    "user_card": {
        "uz": "👤 <b>{name}</b>\nID: <code>{id}</code>\nUsername: {username}\nRol: {role}\nHolat: {status}",
        "ru": "👤 <b>{name}</b>\nID: <code>{id}</code>\nUsername: {username}\nРоль: {role}\nСтатус: {status}",
    },
    "btn_make_admin": {"uz": "⬆️ Adminga aylantirish", "ru": "⬆️ Сделать админом"},
    "btn_make_employee": {"uz": "⬇️ Xodimga aylantirish", "ru": "⬇️ Сделать сотрудником"},
    "btn_deactivate": {"uz": "🚫 Faolsizlantirish", "ru": "🚫 Деактивировать"},
    "btn_activate": {"uz": "✅ Faollashtirish", "ru": "✅ Активировать"},
    "role_changed": {"uz": "✅ Rol o'zgartirildi.", "ru": "✅ Роль изменена."},
    "status_changed": {"uz": "✅ Holat o'zgartirildi.", "ru": "✅ Статус изменён."},

    # ===== E'lon =====
    "ask_broadcast": {"uz": "📢 Barcha xodimlarga yuboriladigan e'lonni yozing:", "ru": "📢 Введите объявление для всех сотрудников:"},
    "broadcast_sent": {"uz": "✅ E'lon {n} xodimga yuborildi.", "ru": "✅ Объявление отправлено {n} сотрудникам."},
    "broadcast_msg": {"uz": "📢 <b>E'lon</b>\n\n{text}", "ru": "📢 <b>Объявление</b>\n\n{text}"},

    # ===== Eslatmalar =====
    "reminder_deadline": {
        "uz": "⏰ <b>Eslatma!</b> Vazifa #{id} muddati yaqinlashdi/o'tdi:\n📌 {title}\n⏰ {deadline}",
        "ru": "⏰ <b>Напоминание!</b> Срок задачи #{id} подходит/истёк:\n📌 {title}\n⏰ {deadline}",
    },
    "reminder_report": {
        "uz": "🗒 <b>Eslatma:</b> bugungi hisobotingizni yuborishni unutmang!\n«🗒 Hisobot yuborish» tugmasini bosing.",
        "ru": "🗒 <b>Напоминание:</b> не забудьте отправить отчёт за сегодня!\nНажмите «🗒 Отправить отчёт».",
    },
    "reminder_deadline_admin": {
        "uz": "⏰ Vazifa #{id} ({assignee}) muddati o'tmoqda: {title}",
        "ru": "⏰ У задачи #{id} ({assignee}) истекает срок: {title}",
    },
}

STATUS_LABEL = {
    "new": {"uz": "🆕 Yangi", "ru": "🆕 Новая"},
    "in_progress": {"uz": "▶️ Jarayonda", "ru": "▶️ В работе"},
    "done": {"uz": "✅ Bajarilgan (tasdiq kutilmoqda)", "ru": "✅ Выполнена (ждёт приёмки)"},
    "accepted": {"uz": "👍 Qabul qilingan", "ru": "👍 Принята"},
    "rejected": {"uz": "👎 Qaytarilgan", "ru": "👎 Возвращена"},
}

SEV_LABEL = {
    "low": {"uz": "🟢 Past", "ru": "🟢 Низкий"},
    "normal": {"uz": "🟡 O'rta", "ru": "🟡 Средний"},
    "high": {"uz": "🔴 Yuqori", "ru": "🔴 Высокий"},
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    entry = TEXTS.get(key, {})
    text = entry.get(lang) or entry.get("uz") or key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def status_label(status: str, lang: str = "uz") -> str:
    return STATUS_LABEL.get(status, {}).get(lang, status)


def sev_label(sev: str, lang: str = "uz") -> str:
    return SEV_LABEL.get(sev, {}).get(lang, sev)


# ===== Loyiha va guruh/topic matnlari (qo'shimcha) =====
TEXTS.update({
    "btn_projects": {"uz": "📁 Loyihalar", "ru": "📁 Проекты"},
    "ask_task_project": {"uz": "📁 Vazifa qaysi loyihaga tegishli?", "ru": "📁 К какому проекту относится задача?"},
    "ask_issue_project": {"uz": "📁 Kamchilik qaysi loyihaga tegishli?", "ru": "📁 К какому проекту относится замечание?"},
    "projects_header": {"uz": "📁 <b>Loyihalar</b>\n(✅ = guruhga bog'langan)", "ru": "📁 <b>Проекты</b>\n(✅ = привязан к группе)"},
    "btn_add_project": {"uz": "➕ Loyiha qo'shish", "ru": "➕ Добавить проект"},
    "ask_project_name": {"uz": "✍️ Yangi loyiha nomini yozing:", "ru": "✍️ Введите название нового проекта:"},
    "project_added": {"uz": "✅ Loyiha qo'shildi: {name}", "ru": "✅ Проект добавлен: {name}"},
    "no_projects": {"uz": "📭 Loyihalar yo'q.", "ru": "📭 Проектов нет."},
    "proj_line_linked": {"uz": "✅ {name} — guruh: <code>{chat}</code> | mavzular: {topics}", "ru": "✅ {name} — группа: <code>{chat}</code> | темы: {topics}"},
    "proj_line_unlinked": {"uz": "⬜ {name} — bog'lanmagan", "ru": "⬜ {name} — не привязан"},

    # Guruh komandalar
    "link_usage": {
        "uz": "ℹ️ Bu komanda guruh ichida ishlaydi.\nGuruhni loyihaga bog'lash:\n<code>/bogla Loyiha nomi</code>",
        "ru": "ℹ️ Команда работает внутри группы.\nПривязать группу к проекту:\n<code>/bogla Название проекта</code>",
    },
    "link_not_group": {"uz": "❗ Bu komanda faqat guruhda ishlaydi.", "ru": "❗ Команда работает только в группе."},
    "link_no_project": {"uz": "❌ Bunday loyiha topilmadi: {name}", "ru": "❌ Проект не найден: {name}"},
    "link_ok": {"uz": "✅ Ushbu guruh «{name}» loyihasiga bog'landi.\nEndi har bir mavzu ichida <code>/mavzu turi</code> yuboring.\nTurlar: tasks, issues, reports, general", "ru": "✅ Группа привязана к проекту «{name}».\nТеперь внутри каждой темы отправьте <code>/mavzu тип</code>.\nТипы: tasks, issues, reports, general"},
    "topic_usage": {
        "uz": "ℹ️ Mavzu ichida yuboring:\n<code>/mavzu issues</code>\nTurlar: tasks (vazifalar), issues (kamchiliklar), reports (hisobotlar), general (umumiy)",
        "ru": "ℹ️ Отправьте внутри темы:\n<code>/mavzu issues</code>\nТипы: tasks, issues, reports, general",
    },
    "topic_not_linked": {"uz": "❗ Avval guruhni loyihaga bog'lang: /bogla", "ru": "❗ Сначала привяжите группу: /bogla"},
    "topic_no_thread": {"uz": "❗ Bu komandani forum MAVZUSI (topic) ichida yuboring.", "ru": "❗ Отправьте эту команду внутри ТЕМЫ (topic) форума."},
    "topic_bad_kind": {"uz": "❌ Noto'g'ri tur. Mavjud: tasks, issues, reports, general", "ru": "❌ Неверный тип. Доступно: tasks, issues, reports, general"},
    "topic_ok": {"uz": "✅ «{title}» mavzusi → <b>{kind}</b> sifatida saqlandi ({name}).", "ru": "✅ Тема «{title}» → сохранена как <b>{kind}</b> ({name})."},
    "status_group": {
        "uz": "📁 Loyiha: <b>{name}</b>\n💬 Chat: <code>{chat}</code>\n🧵 Mavzular: {topics}",
        "ru": "📁 Проект: <b>{name}</b>\n💬 Чат: <code>{chat}</code>\n🧵 Темы: {topics}",
    },
    "status_no_link": {"uz": "⬜ Bu guruh hech qaysi loyihaga bog'lanmagan.", "ru": "⬜ Группа не привязана ни к одному проекту."},

    # Guruhga yuboriladigan postlar
    "post_task": {
        "uz": "🆕 <b>Vazifa #{id}</b>\n📌 {title}\n{desc}👤 Mas'ul: {assignee}\n⏰ Muddat: {deadline}",
        "ru": "🆕 <b>Задача #{id}</b>\n📌 {title}\n{desc}👤 Ответственный: {assignee}\n⏰ Срок: {deadline}",
    },
    "post_issue": {
        "uz": "⚠️ <b>Kamchilik #{id}</b> ({sev})\n👤 {target}\n{text}",
        "ru": "⚠️ <b>Замечание #{id}</b> ({sev})\n👤 {target}\n{text}",
    },
    "post_task_done": {"uz": "✅ Vazifa #{id} bajarildi: {title} ({assignee})", "ru": "✅ Задача #{id} выполнена: {title} ({assignee})"},
    "post_issue_fixed": {"uz": "✅ Kamchilik #{id} tuzatildi ({target})", "ru": "✅ Замечание #{id} исправлено ({target})"},
})


# ===== Tayyor materiallar trekeri (qo'shimcha) =====
TEXTS.update({
    "btn_materials": {"uz": "🎨 Tayyor materiallar", "ru": "🎨 Готовые материалы"},
    "materials_header": {"uz": "🎨 <b>Bugungi tayyor materiallar ({day})</b>", "ru": "🎨 <b>Готовые материалы за сегодня ({day})</b>"},
    "no_materials": {"uz": "📭 Bugun hali material tashlanmagan.", "ru": "📭 Сегодня материалов пока нет."},
    "mat_line": {"uz": "📁 <b>{project}</b>: 🖼 {visual} vizual | 🎬 {video} video", "ru": "📁 <b>{project}</b>: 🖼 {visual} визуал | 🎬 {video} видео"},
    "mat_total": {"uz": "\n<b>Jami:</b> 🖼 {visual} vizual | 🎬 {video} video", "ru": "\n<b>Итого:</b> 🖼 {visual} визуал | 🎬 {video} видео"},

    # /biriktir
    "bind_usage": {
        "uz": "ℹ️ Bu mavzuni loyihaga biriktirish (mavzu ICHIDA yuboring):\n<code>/biriktir Loyiha nomi</code>",
        "ru": "ℹ️ Привязать тему к проекту (отправьте ВНУТРИ темы):\n<code>/biriktir Название проекта</code>",
    },
    "bind_ok": {"uz": "✅ Ushbu mavzu «{name}» loyihasiga biriktirildi.\nEndi shu yerga tashlangan rasm/videolar avtomatik hisoblanadi.", "ru": "✅ Тема привязана к проекту «{name}».\nТеперь фото/видео здесь будут учитываться автоматически."},
    "delivery_logged": {"uz": "✅ {kind} qayd etildi → {project}", "ru": "✅ {kind} учтён → {project}"},
})
