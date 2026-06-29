"""Klaviaturalar (reply va inline)."""
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from locales import t


def lang_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇿 O'zbekcha", callback_data="setlang:uz")
    kb.button(text="🇷🇺 Русский", callback_data="setlang:ru")
    return kb.as_markup()


def admin_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=t("btn_new_task", lang)),
           KeyboardButton(text=t("btn_all_tasks", lang)))
    kb.row(KeyboardButton(text=t("btn_accept_tasks", lang)),
           KeyboardButton(text=t("btn_reports", lang)))
    kb.row(KeyboardButton(text=t("btn_new_issue", lang)),
           KeyboardButton(text=t("btn_open_issues", lang)))
    kb.row(KeyboardButton(text=t("btn_attendance", lang)),
           KeyboardButton(text=t("btn_employees", lang)))
    kb.row(KeyboardButton(text=t("btn_projects", lang)),
           KeyboardButton(text=t("btn_materials", lang)))
    kb.row(KeyboardButton(text=t("btn_broadcast", lang)),
           KeyboardButton(text=t("btn_lang", lang)))
    return kb.as_markup(resize_keyboard=True)


def employee_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=t("btn_my_tasks", lang)),
           KeyboardButton(text=t("btn_send_report", lang)))
    kb.row(KeyboardButton(text=t("btn_my_issues", lang)))
    kb.row(KeyboardButton(text=t("btn_checkin", lang)),
           KeyboardButton(text=t("btn_checkout", lang)))
    kb.row(KeyboardButton(text=t("btn_lang", lang)))
    return kb.as_markup(resize_keyboard=True)


def cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=t("cancel", lang)))
    return kb.as_markup(resize_keyboard=True)


def skip_cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=t("skip", lang)))
    kb.row(KeyboardButton(text=t("cancel", lang)))
    return kb.as_markup(resize_keyboard=True)


def employees_inline(employees, prefix: str, lang: str) -> InlineKeyboardMarkup:
    """Xodimlarni tanlash uchun inline ro'yxat. callback: {prefix}:{user_id}"""
    kb = InlineKeyboardBuilder()
    for e in employees:
        kb.button(text=f"👤 {e['full_name']}", callback_data=f"{prefix}:{e['user_id']}")
    kb.adjust(1)
    return kb.as_markup()


def severity_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("sev_low", lang), callback_data="sev:low")
    kb.button(text=t("sev_normal", lang), callback_data="sev:normal")
    kb.button(text=t("sev_high", lang), callback_data="sev:high")
    kb.adjust(3)
    return kb.as_markup()


def task_employee_kb(task_id: int, status: str, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if status in ("new", "rejected"):
        kb.button(text=t("btn_start_task", lang), callback_data=f"tstart:{task_id}")
        kb.button(text=t("btn_done_task", lang), callback_data=f"tdone:{task_id}")
    elif status == "in_progress":
        kb.button(text=t("btn_done_task", lang), callback_data=f"tdone:{task_id}")
    kb.adjust(2)
    return kb.as_markup()


def task_accept_kb(task_id: int, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("btn_accept", lang), callback_data=f"taccept:{task_id}")
    kb.button(text=t("btn_reject", lang), callback_data=f"treject:{task_id}")
    kb.adjust(2)
    return kb.as_markup()


def issue_fix_kb(issue_id: int, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("btn_fix_issue", lang), callback_data=f"ifix:{issue_id}")
    return kb.as_markup()


def user_manage_kb(u, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if u["role"] == "employee":
        kb.button(text=t("btn_make_admin", lang), callback_data=f"role:admin:{u['user_id']}")
    else:
        kb.button(text=t("btn_make_employee", lang), callback_data=f"role:employee:{u['user_id']}")
    if u["active"]:
        kb.button(text=t("btn_deactivate", lang), callback_data=f"act:0:{u['user_id']}")
    else:
        kb.button(text=t("btn_activate", lang), callback_data=f"act:1:{u['user_id']}")
    kb.adjust(1)
    return kb.as_markup()


def projects_inline(projects, prefix: str) -> InlineKeyboardMarkup:
    """Loyihani tanlash inline ro'yxati. callback: {prefix}:{project_id}"""
    kb = InlineKeyboardBuilder()
    for p in projects:
        kb.button(text=f"📁 {p['name']}", callback_data=f"{prefix}:{p['id']}")
    kb.adjust(2)
    return kb.as_markup()


def projects_with_skip(projects, prefix: str, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for p in projects:
        kb.button(text=f"📁 {p['name']}", callback_data=f"{prefix}:{p['id']}")
    kb.button(text=t("skip", lang), callback_data=f"{prefix}:0")
    kb.adjust(2)
    return kb.as_markup()


def projects_panel(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("btn_add_project", lang), callback_data="proj_add")
    return kb.as_markup()
