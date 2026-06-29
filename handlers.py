"""Barcha handlerlar: vazifa, hisobot, kamchilik, davomat, xodimlar."""
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

import config
import database as db
import keyboards as kb
from locales import t, status_label, sev_label

router = Router()


# ===== FSM holatlari =====
class TaskFSM(StatesGroup):
    project = State()
    assignee = State()
    title = State()
    desc = State()
    deadline = State()


class IssueFSM(StatesGroup):
    project = State()
    target = State()
    text = State()
    severity = State()


class ReportFSM(StatesGroup):
    text = State()


class BroadcastFSM(StatesGroup):
    text = State()


class ProjectFSM(StatesGroup):
    name = State()


# ===== Yordamchilar =====
async def is_admin(user_id) -> bool:
    if user_id in config.OWNER_IDS:
        return True
    u = await db.get_user(user_id)
    return bool(u and u["role"] == "admin")


async def get_lang(user_id) -> str:
    u = await db.get_user(user_id)
    return u["lang"] if u else "uz"


async def send_menu(message: Message, user_id: int):
    lang = await get_lang(user_id)
    if await is_admin(user_id):
        await message.answer(t("menu", lang), reply_markup=kb.admin_menu(lang))
    else:
        await message.answer(t("menu", lang), reply_markup=kb.employee_menu(lang))


def fmt_deadline(dl, lang):
    return dl if dl else t("none", lang)


async def notify(bot, user_id, text, reply_markup=None):
    try:
        await bot.send_message(user_id, text, reply_markup=reply_markup)
    except Exception:
        pass  # foydalanuvchi botni bloklagan bo'lishi mumkin


async def notify_admins(bot, text, exclude=None, reply_markup=None):
    sent = set()
    for oid in config.OWNER_IDS:
        if oid != exclude:
            await notify(bot, oid, text, reply_markup)
            sent.add(oid)
    for u in await db.list_all_users():
        if u["role"] == "admin" and u["user_id"] not in sent and u["user_id"] != exclude:
            await notify(bot, u["user_id"], text, reply_markup)
    if config.WORK_GROUP_ID:
        await notify(bot, config.WORK_GROUP_ID, text)


async def post_to_project(bot, project_id, kind, text) -> bool:
    """Loyihaning bog'langan guruhidagi kerakli mavzuga (topic) yozadi."""
    if not project_id:
        return False
    proj = await db.get_project(project_id)
    if not proj or not proj["chat_id"]:
        return False
    topic = await db.get_topic(project_id, kind)
    thread_id = topic["thread_id"] if topic else None
    try:
        await bot.send_message(proj["chat_id"], text, message_thread_id=thread_id)
        return True
    except Exception:
        return False


# ===== /start va til =====
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return
    await state.clear()
    u = await db.get_user(message.from_user.id)
    role = "admin" if message.from_user.id in config.OWNER_IDS else "employee"
    if u and u["role"] == "admin":
        role = "admin"
    await db.add_user(
        message.from_user.id,
        message.from_user.full_name,
        message.from_user.username,
        role,
    )
    if message.from_user.id in config.OWNER_IDS:
        await db.set_role(message.from_user.id, "admin")
    u = await db.get_user(message.from_user.id)
    if not u or not u["lang"]:
        await message.answer(t("choose_lang", "uz"), reply_markup=kb.lang_kb())
        return
    await _greet(message, u)


async def _greet(message: Message, u):
    lang = u["lang"]
    name = u["full_name"]
    if await is_admin(u["user_id"]):
        await message.answer(t("welcome_admin", lang, name=name), reply_markup=kb.admin_menu(lang))
    else:
        await message.answer(t("welcome_employee", lang, name=name), reply_markup=kb.employee_menu(lang))


@router.callback_query(F.data.startswith("setlang:"))
async def cb_setlang(call: CallbackQuery):
    lang = call.data.split(":")[1]
    await db.set_lang(call.from_user.id, lang)
    await call.message.edit_text(t("lang_set", lang))
    u = await db.get_user(call.from_user.id)
    await _greet(call.message, u)
    await call.answer()


@router.message(Command("id"))
async def cmd_id(message: Message):
    await message.answer(
        f"🆔 Sizning ID: <code>{message.from_user.id}</code>\n"
        f"💬 Chat ID: <code>{message.chat.id}</code>"
    )


# ===== Bekor qilish (har qanday tilda) =====
@router.message(F.text.in_({"❌ Bekor qilish", "❌ Отмена"}))
async def cancel_any(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.clear()
    await message.answer(t("cancelled", lang))
    await send_menu(message, message.from_user.id)


# ===== Til o'zgartirish tugmasi =====
@router.message(F.text.in_({"🌐 Til", "🌐 Язык"}))
async def change_lang(message: Message):
    await message.answer(t("choose_lang", "uz"), reply_markup=kb.lang_kb())


# ========================================================
#                  VAZIFA BERISH (admin)
# ========================================================
@router.message(F.text.in_({"➕ Vazifa berish", "➕ Поставить задачу"}))
async def task_new_start(message: Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    employees = await db.list_employees()
    if not employees:
        await message.answer(t("no_employees", lang))
        return
    projects = await db.list_projects()
    await state.set_state(TaskFSM.project)
    await message.answer(t("ask_task_project", lang),
                         reply_markup=kb.projects_with_skip(projects, "tproj", lang))


@router.callback_query(TaskFSM.project, F.data.startswith("tproj:"))
async def task_pick_project(call: CallbackQuery, state: FSMContext):
    pid = int(call.data.split(":")[1]) or None
    await state.update_data(project=pid)
    lang = await get_lang(call.from_user.id)
    employees = await db.list_employees()
    await state.set_state(TaskFSM.assignee)
    await call.message.edit_text(t("ask_task_assignee", lang),
                                 reply_markup=kb.employees_inline(employees, "tassignee", lang))
    await call.answer()


@router.callback_query(TaskFSM.assignee, F.data.startswith("tassignee:"))
async def task_pick_assignee(call: CallbackQuery, state: FSMContext):
    assignee_id = int(call.data.split(":")[1])
    await state.update_data(assignee=assignee_id)
    lang = await get_lang(call.from_user.id)
    await state.set_state(TaskFSM.title)
    await call.message.edit_text(t("ask_task_title", lang))
    await call.answer()


@router.message(TaskFSM.title)
async def task_title(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.update_data(title=message.text.strip())
    await state.set_state(TaskFSM.desc)
    await message.answer(t("ask_task_desc", lang), reply_markup=kb.skip_cancel_kb(lang))


@router.message(TaskFSM.desc)
async def task_desc(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    text = message.text.strip()
    if text in (t("skip", "uz"), t("skip", "ru")):
        text = ""
    await state.update_data(desc=text)
    await state.set_state(TaskFSM.deadline)
    await message.answer(t("ask_task_deadline", lang), reply_markup=kb.skip_cancel_kb(lang))


@router.message(TaskFSM.deadline)
async def task_deadline(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    raw = message.text.strip()
    deadline = None
    if raw not in (t("skip", "uz"), t("skip", "ru")):
        try:
            dt = datetime.strptime(raw, "%Y-%m-%d %H:%M")
            deadline = dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            await message.answer(t("bad_deadline", lang))
            return
    data = await state.get_data()
    task_id = await db.create_task(
        data["title"], data["desc"], data["assignee"], message.from_user.id, deadline,
        data.get("project")
    )
    await state.clear()
    await message.answer(t("task_created_admin", lang, id=task_id))
    await send_menu(message, message.from_user.id)

    # Xodimga yuborish
    emp = await db.get_user(data["assignee"])
    emp_lang = emp["lang"] if emp else "uz"
    desc_line = f"📝 {data['desc']}\n" if data["desc"] else ""
    txt = t("task_new_for_employee", emp_lang, id=task_id, title=data["title"],
            desc=desc_line, deadline=fmt_deadline(deadline, emp_lang),
            creator=message.from_user.full_name)
    await notify(message.bot, data["assignee"], txt,
                 reply_markup=kb.task_employee_kb(task_id, "new", emp_lang))
    # Loyiha guruhidagi "tasks" mavzusiga post
    g_desc = f"📝 {data['desc']}\n" if data["desc"] else ""
    await post_to_project(message.bot, data.get("project"), "tasks",
        t("post_task", "uz", id=task_id, title=data["title"], desc=g_desc,
          assignee=(emp["full_name"] if emp else "?"),
          deadline=fmt_deadline(deadline, "uz")))


# ===== Xodim vazifa holatini o'zgartirishi =====
@router.callback_query(F.data.startswith("tstart:"))
async def task_start(call: CallbackQuery):
    task_id = int(call.data.split(":")[1])
    task = await db.get_task(task_id)
    lang = await get_lang(call.from_user.id)
    if not task or task["assignee_id"] != call.from_user.id:
        await call.answer(t("not_allowed", lang), show_alert=True)
        return
    await db.update_task_status(task_id, "in_progress")
    await call.message.edit_reply_markup(reply_markup=kb.task_employee_kb(task_id, "in_progress", lang))
    await call.answer(t("task_started", lang, id=task_id))


@router.callback_query(F.data.startswith("tdone:"))
async def task_done(call: CallbackQuery):
    task_id = int(call.data.split(":")[1])
    task = await db.get_task(task_id)
    lang = await get_lang(call.from_user.id)
    if not task or task["assignee_id"] != call.from_user.id:
        await call.answer(t("not_allowed", lang), show_alert=True)
        return
    await db.update_task_status(task_id, "done")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(t("task_done_employee", lang, id=task_id))
    # Adminni xabardor qilish + qabul tugmalari
    admin_txt = t("task_done_notify_admin", "uz", name=call.from_user.full_name,
                  id=task_id, title=task["title"])
    await notify_admins(call.bot, admin_txt, reply_markup=kb.task_accept_kb(task_id, "uz"))
    await post_to_project(call.bot, task["project_id"], "tasks",
        t("post_task_done", "uz", id=task_id, title=task["title"],
          assignee=call.from_user.full_name))
    await call.answer()


@router.callback_query(F.data.startswith("taccept:"))
async def task_accept(call: CallbackQuery):
    task_id = int(call.data.split(":")[1])
    if not await is_admin(call.from_user.id):
        return
    task = await db.get_task(task_id)
    await db.update_task_status(task_id, "accepted")
    lang = await get_lang(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(t("task_accepted_admin", lang, id=task_id))
    emp = await db.get_user(task["assignee_id"])
    emp_lang = emp["lang"] if emp else "uz"
    await notify(call.bot, task["assignee_id"], t("task_accepted", emp_lang, id=task_id))


@router.callback_query(F.data.startswith("treject:"))
async def task_reject(call: CallbackQuery):
    task_id = int(call.data.split(":")[1])
    if not await is_admin(call.from_user.id):
        return
    task = await db.get_task(task_id)
    await db.update_task_status(task_id, "rejected")
    lang = await get_lang(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(t("task_rejected_admin", lang, id=task_id))
    emp = await db.get_user(task["assignee_id"])
    emp_lang = emp["lang"] if emp else "uz"
    await notify(call.bot, task["assignee_id"], t("task_rejected", emp_lang, id=task_id),
                 reply_markup=kb.task_employee_kb(task_id, "rejected", emp_lang))


# ===== Mening vazifalarim (xodim) =====
@router.message(F.text.in_({"📋 Mening vazifalarim", "📋 Мои задачи"}))
async def my_tasks(message: Message):
    lang = await get_lang(message.from_user.id)
    tasks = await db.tasks_for_user(message.from_user.id)
    if not tasks:
        await message.answer(t("no_tasks", lang))
        return
    for tk in tasks:
        desc_line = f"📝 {tk['description']}\n" if tk["description"] else ""
        txt = (f"#{tk['id']} — <b>{tk['title']}</b>\n{desc_line}"
               f"⏰ {fmt_deadline(tk['deadline'], lang)}\n"
               f"📊 {status_label(tk['status'], lang)}")
        await message.answer(txt, reply_markup=kb.task_employee_kb(tk["id"], tk["status"], lang))


# ===== Barcha vazifalar (admin) =====
@router.message(F.text.in_({"📋 Barcha vazifalar", "📋 Все задачи"}))
async def all_tasks(message: Message):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    tasks = await db.all_open_tasks()
    if not tasks:
        await message.answer(t("no_tasks_admin", lang))
        return
    lines = []
    for tk in tasks:
        emp = await db.get_user(tk["assignee_id"])
        ename = emp["full_name"] if emp else "?"
        lines.append(f"#{tk['id']} {status_label(tk['status'], lang)}\n"
                     f"📌 {tk['title']} — 👤 {ename}\n"
                     f"⏰ {fmt_deadline(tk['deadline'], lang)}")
    await message.answer("\n\n".join(lines))


# ===== Qabul qilish ro'yxati (admin) =====
@router.message(F.text.in_({"✅ Qabul qilish (bajarilgan)", "✅ Приёмка (выполненные)"}))
async def accept_list(message: Message):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    tasks = await db.tasks_pending_acceptance()
    if not tasks:
        await message.answer(t("no_pending", lang))
        return
    for tk in tasks:
        emp = await db.get_user(tk["assignee_id"])
        ename = emp["full_name"] if emp else "?"
        txt = (f"#{tk['id']} — <b>{tk['title']}</b>\n👤 {ename}\n"
               f"📊 {status_label(tk['status'], lang)}")
        await message.answer(txt, reply_markup=kb.task_accept_kb(tk["id"], lang))


# ========================================================
#                  HISOBOT (xodim)
# ========================================================
@router.message(F.text.in_({"🗒 Hisobot yuborish", "🗒 Отправить отчёт"}))
async def report_start(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(ReportFSM.text)
    await message.answer(t("ask_report", lang), reply_markup=kb.cancel_kb(lang))


@router.message(ReportFSM.text)
async def report_save(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await db.add_report(message.from_user.id, message.text.strip())
    await state.clear()
    await message.answer(t("report_saved", lang))
    await send_menu(message, message.from_user.id)
    admin_txt = t("report_notify_admin", "uz", name=message.from_user.full_name,
                  text=message.text.strip())
    await notify_admins(message.bot, admin_txt, exclude=message.from_user.id)


# ===== Bugungi hisobotlar (admin) =====
@router.message(F.text.in_({"🗒 Bugungi hisobotlar", "🗒 Отчёты за сегодня"}))
async def reports_today(message: Message):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    reports = await db.reports_for_day()
    if not reports:
        await message.answer(t("no_reports", lang))
        return
    header = t("reports_header", lang, day=db.today())
    lines = [header, ""]
    for r in reports:
        tm = r["created_at"][11:16]
        lines.append(f"👤 <b>{r['full_name']}</b> ({tm})\n{r['text']}\n")
    await message.answer("\n".join(lines))


# ========================================================
#                  XATO / KAMCHILIK (admin)
# ========================================================
@router.message(F.text.in_({"⚠️ Xato/kamchilik", "⚠️ Ошибка/замечание"}))
async def issue_start(message: Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    employees = await db.list_employees()
    if not employees:
        await message.answer(t("no_employees", lang))
        return
    projects = await db.list_projects()
    await state.set_state(IssueFSM.project)
    await message.answer(t("ask_issue_project", lang),
                         reply_markup=kb.projects_with_skip(projects, "iproj", lang))


@router.callback_query(IssueFSM.project, F.data.startswith("iproj:"))
async def issue_pick_project(call: CallbackQuery, state: FSMContext):
    pid = int(call.data.split(":")[1]) or None
    await state.update_data(project=pid)
    lang = await get_lang(call.from_user.id)
    employees = await db.list_employees()
    await state.set_state(IssueFSM.target)
    await call.message.edit_text(t("ask_issue_target", lang),
                                 reply_markup=kb.employees_inline(employees, "itarget", lang))
    await call.answer()


@router.callback_query(IssueFSM.target, F.data.startswith("itarget:"))
async def issue_pick(call: CallbackQuery, state: FSMContext):
    target_id = int(call.data.split(":")[1])
    await state.update_data(target=target_id)
    lang = await get_lang(call.from_user.id)
    await state.set_state(IssueFSM.text)
    await call.message.edit_text(t("ask_issue_text", lang))
    await call.answer()


@router.message(IssueFSM.text)
async def issue_text(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.update_data(text=message.text.strip())
    await state.set_state(IssueFSM.severity)
    await message.answer(t("ask_issue_severity", lang), reply_markup=kb.severity_kb(lang))


@router.callback_query(IssueFSM.severity, F.data.startswith("sev:"))
async def issue_sev(call: CallbackQuery, state: FSMContext):
    sev = call.data.split(":")[1]
    data = await state.get_data()
    lang = await get_lang(call.from_user.id)
    issue_id = await db.add_issue(data["target"], call.from_user.id, data["text"], sev,
                                 data.get("project"))
    await state.clear()
    await call.message.edit_text(t("issue_created_admin", lang, id=issue_id))
    await call.answer()
    await send_menu(call.message, call.from_user.id)
    emp = await db.get_user(data["target"])
    emp_lang = emp["lang"] if emp else "uz"
    txt = t("issue_for_employee", emp_lang, id=issue_id, sev=sev_label(sev, emp_lang),
            text=data["text"], creator=call.from_user.full_name)
    await notify(call.bot, data["target"], txt, reply_markup=kb.issue_fix_kb(issue_id, emp_lang))
    await post_to_project(call.bot, data.get("project"), "issues",
        t("post_issue", "uz", id=issue_id, sev=sev_label(sev, "uz"),
          target=(emp["full_name"] if emp else "?"), text=data["text"]))


@router.callback_query(F.data.startswith("ifix:"))
async def issue_fix(call: CallbackQuery):
    issue_id = int(call.data.split(":")[1])
    issue = await db.get_issue(issue_id)
    lang = await get_lang(call.from_user.id)
    if not issue or issue["target_id"] != call.from_user.id:
        await call.answer(t("not_allowed", lang), show_alert=True)
        return
    await db.fix_issue(issue_id)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(t("issue_fixed_employee", lang, id=issue_id))
    await notify_admins(call.bot, t("issue_fixed_admin", "uz",
                        name=call.from_user.full_name, id=issue_id))
    await post_to_project(call.bot, issue["project_id"], "issues",
        t("post_issue_fixed", "uz", id=issue_id, target=call.from_user.full_name))


# ===== Ochiq kamchiliklar (admin) =====
@router.message(F.text.in_({"🔧 Ochiq kamchiliklar", "🔧 Открытые замечания"}))
async def open_issues(message: Message):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    issues = await db.all_open_issues()
    if not issues:
        await message.answer(t("no_issues", lang))
        return
    lines = [t("issues_header", lang), ""]
    for i in issues:
        lines.append(f"#{i['id']} {sev_label(i['severity'], lang)} — 👤 {i['full_name']}\n{i['text']}\n")
    await message.answer("\n".join(lines))


# ===== Mening kamchiliklarim (xodim) =====
@router.message(F.text.in_({"⚠️ Mening kamchiliklarim", "⚠️ Мои замечания"}))
async def my_issues(message: Message):
    lang = await get_lang(message.from_user.id)
    issues = await db.open_issues_for_user(message.from_user.id)
    if not issues:
        await message.answer(t("no_issues", lang))
        return
    await message.answer(t("my_issues_header", lang))
    for i in issues:
        txt = f"#{i['id']} {sev_label(i['severity'], lang)}\n{i['text']}"
        await message.answer(txt, reply_markup=kb.issue_fix_kb(i["id"], lang))


# ========================================================
#                  DAVOMAT (xodim)
# ========================================================
@router.message(F.text.in_({"🟢 Ishga keldim", "🟢 Пришёл на работу"}))
async def do_checkin(message: Message):
    lang = await get_lang(message.from_user.id)
    tm, ok = await db.check_in(message.from_user.id)
    tm_s = tm[11:16] if tm else "?"
    if ok:
        await message.answer(t("checkin_ok", lang, time=tm_s))
        await notify_admins(message.bot,
            f"🟢 {message.from_user.full_name} ishga keldi: {tm_s}",
            exclude=message.from_user.id)
    else:
        await message.answer(t("checkin_already", lang, time=tm_s))


@router.message(F.text.in_({"🔴 Ishdan ketdim", "🔴 Ушёл с работы"}))
async def do_checkout(message: Message):
    lang = await get_lang(message.from_user.id)
    tm, ok = await db.check_out(message.from_user.id)
    if ok:
        tm_s = tm[11:16]
        await message.answer(t("checkout_ok", lang, time=tm_s))
        await notify_admins(message.bot,
            f"🔴 {message.from_user.full_name} ishdan ketdi: {tm_s}",
            exclude=message.from_user.id)
    else:
        await message.answer(t("checkout_no_in", lang))


# ===== Davomat ko'rish (admin) =====
@router.message(F.text.in_({"🕒 Davomat", "🕒 Посещаемость"}))
async def view_attendance(message: Message):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    rows = await db.attendance_for_day()
    if not rows:
        await message.answer(t("no_attendance", lang))
        return
    lines = [t("attendance_header", lang, day=db.today()), ""]
    for r in rows:
        ci = r["check_in"][11:16] if r["check_in"] else "—"
        co = r["check_out"][11:16] if r["check_out"] else "—"
        lines.append(f"👤 {r['full_name']}: 🟢 {ci}  →  🔴 {co}")
    await message.answer("\n".join(lines))


# ========================================================
#                  XODIMLAR (admin)
# ========================================================
@router.message(F.text.in_({"👥 Xodimlar", "👥 Сотрудники"}))
async def employees_list(message: Message):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    users = await db.list_all_users()
    users = [u for u in users if u["user_id"] not in config.OWNER_IDS or u["role"] != "admin"] or users
    if not users:
        await message.answer(t("no_employees", lang))
        return
    await message.answer(t("employees_header", lang))
    for u in users:
        await _send_user_card(message, u, lang)


async def _send_user_card(message_or_call, u, lang):
    status = ("✅" if u["active"] else "🚫")
    txt = t("user_card", lang, name=u["full_name"], id=u["user_id"],
            username=("@" + u["username"]) if u["username"] else "—",
            role=u["role"], status=status)
    target = message_or_call if isinstance(message_or_call, Message) else message_or_call.message
    await target.answer(txt, reply_markup=kb.user_manage_kb(u, lang))


@router.callback_query(F.data.startswith("role:"))
async def cb_role(call: CallbackQuery):
    if not await is_admin(call.from_user.id):
        return
    _, role, uid = call.data.split(":")
    await db.set_role(int(uid), role)
    lang = await get_lang(call.from_user.id)
    await call.answer(t("role_changed", lang))
    u = await db.get_user(int(uid))
    try:
        await call.message.edit_reply_markup(reply_markup=kb.user_manage_kb(u, lang))
    except Exception:
        pass


@router.callback_query(F.data.startswith("act:"))
async def cb_act(call: CallbackQuery):
    if not await is_admin(call.from_user.id):
        return
    _, active, uid = call.data.split(":")
    await db.set_active(int(uid), int(active))
    lang = await get_lang(call.from_user.id)
    await call.answer(t("status_changed", lang))
    u = await db.get_user(int(uid))
    try:
        await call.message.edit_reply_markup(reply_markup=kb.user_manage_kb(u, lang))
    except Exception:
        pass


# ========================================================
#                  E'LON (admin)
# ========================================================
@router.message(F.text.in_({"📢 E'lon yuborish", "📢 Рассылка"}))
async def broadcast_start(message: Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        return
    lang = await get_lang(message.from_user.id)
    await state.set_state(BroadcastFSM.text)
    await message.answer(t("ask_broadcast", lang), reply_markup=kb.cancel_kb(lang))


@router.message(BroadcastFSM.text)
async def broadcast_send(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.clear()
    employees = await db.list_employees()
    n = 0
    for e in employees:
        elang = e["lang"] or "uz"
        await notify(message.bot, e["user_id"],
                     t("broadcast_msg", elang, text=message.text.strip()))
        n += 1
    await message.answer(t("broadcast_sent", lang, n=n))
    await send_menu(message, message.from_user.id)


# ========================================================
#                  LOYIHALAR (admin, shaxsiy chat)
# ========================================================
VALID_KINDS = {"tasks", "issues", "reports", "general"}


@router.message(F.text.in_({"📁 Loyihalar", "📁 Проекты"}))
async def projects_menu(message: Message):
    if not await is_admin(message.from_user.id) or message.chat.type != "private":
        return
    lang = await get_lang(message.from_user.id)
    projects = await db.list_projects(active_only=False)
    if not projects:
        await message.answer(t("no_projects", lang), reply_markup=kb.projects_panel(lang))
        return
    lines = [t("projects_header", lang), ""]
    for p in projects:
        if p["chat_id"]:
            tps = await db.topics_for_project(p["id"])
            tlist = ", ".join(sorted(x["kind"] for x in tps)) or "—"
            lines.append(t("proj_line_linked", lang, name=p["name"], chat=p["chat_id"], topics=tlist))
        else:
            lines.append(t("proj_line_unlinked", lang, name=p["name"]))
    await message.answer("\n".join(lines), reply_markup=kb.projects_panel(lang))


@router.callback_query(F.data == "proj_add")
async def project_add_start(call: CallbackQuery, state: FSMContext):
    if not await is_admin(call.from_user.id):
        return
    lang = await get_lang(call.from_user.id)
    await state.set_state(ProjectFSM.name)
    await call.message.answer(t("ask_project_name", lang), reply_markup=kb.cancel_kb(lang))
    await call.answer()


@router.message(ProjectFSM.name)
async def project_add_save(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    name = message.text.strip()
    await db.add_project(name)
    await state.clear()
    await message.answer(t("project_added", lang, name=name))
    await send_menu(message, message.from_user.id)


# ========================================================
#       GURUH KOMANDALARI: /bogla, /mavzu, /holat
# ========================================================
@router.message(Command("bogla"))
async def cmd_link(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.answer(t("link_not_group", "uz"))
        return
    if not await is_admin(message.from_user.id):
        return
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(t("link_usage", "uz"))
        return
    name = parts[1].strip()
    proj = await db.get_project_by_name(name)
    if not proj:
        proj_id = await db.add_project(name)   # bo'lmasa yangi loyiha sifatida ochib bog'laymiz
    else:
        proj_id = proj["id"]
    await db.link_project_chat(proj_id, message.chat.id)
    await message.answer(t("link_ok", "uz", name=name))


@router.message(Command("mavzu"))
async def cmd_topic(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.answer(t("link_not_group", "uz"))
        return
    if not await is_admin(message.from_user.id):
        return
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(t("topic_usage", "uz"))
        return
    kind = parts[1].strip().lower()
    if kind not in VALID_KINDS:
        await message.answer(t("topic_bad_kind", "uz"))
        return
    proj = await db.get_project_by_chat(message.chat.id)
    if not proj:
        await message.answer(t("topic_not_linked", "uz"))
        return
    thread_id = message.message_thread_id
    if not thread_id:
        await message.answer(t("topic_no_thread", "uz"))
        return
    await db.set_topic(proj["id"], kind, thread_id, kind)
    await message.answer(t("topic_ok", "uz", title=kind, kind=kind, name=proj["name"]))


@router.message(Command("holat"))
async def cmd_status(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        return
    proj = await db.get_project_by_chat(message.chat.id)
    if not proj:
        await message.answer(t("status_no_link", "uz"))
        return
    tps = await db.topics_for_project(proj["id"])
    tlist = ", ".join(f"{x['kind']}#{x['thread_id']}" for x in tps) or "—"
    await message.answer(t("status_group", "uz", name=proj["name"],
                           chat=message.chat.id, topics=tlist))


# ========================================================
#   DESIGN GURUHI: MAVZU = LOYIHA + TAYYOR MATERIALLAR
# ========================================================
@router.message(Command("biriktir"))
async def cmd_bind_topic(message: Message):
    """Design-guruhda mavzuni loyihaga biriktirish (mavzu ichida yuboriladi)."""
    if message.chat.type not in ("group", "supergroup"):
        await message.answer(t("link_not_group", "uz"))
        return
    if not await is_admin(message.from_user.id):
        return
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(t("bind_usage", "uz"))
        return
    if not message.message_thread_id:
        await message.answer(t("topic_no_thread", "uz"))
        return
    name = parts[1].strip()
    proj = await db.get_project_by_name(name)
    proj_id = proj["id"] if proj else await db.add_project(name)
    await db.bind_topic_project(message.chat.id, message.message_thread_id, proj_id, name)
    await message.answer(t("bind_ok", "uz", name=name))


def _media_kind(message: Message):
    """Xabardagi media turini aniqlaydi: 'visual', 'video' yoki None."""
    if message.photo:
        return "visual"
    if message.video or message.animation:
        return "video"
    if message.document:
        mime = (message.document.mime_type or "").lower()
        if mime.startswith("image/"):
            return "visual"
        if mime.startswith("video/"):
            return "video"
    return None


@router.message(
    (F.chat.type.in_({"group", "supergroup"}))
    & (F.photo | F.video | F.document | F.animation)
)
async def capture_deliverable(message: Message):
    """Loyiha mavzusiga tashlangan tayyor vizual/videoni avtomatik qayd etadi."""
    kind = _media_kind(message)
    if not kind:
        return
    # Loyihani aniqlash: avval mavzu=loyiha, keyin guruh=loyiha
    project_id = None
    if message.message_thread_id:
        tp = await db.get_topic_project(message.chat.id, message.message_thread_id)
        if tp:
            project_id = tp["project_id"]
    if not project_id:
        proj = await db.get_project_by_chat(message.chat.id)
        if proj:
            project_id = proj["id"]
    if not project_id:
        return  # bu guruh/mavzu hech qaysi loyihaga biriktirilmagan
    name = message.from_user.full_name if message.from_user else "?"
    uid = message.from_user.id if message.from_user else 0
    await db.add_deliverable(project_id, uid, name, kind)


@router.message(F.text.in_({"🎨 Tayyor materiallar", "🎨 Готовые материалы"}))
async def materials_summary(message: Message):
    if not await is_admin(message.from_user.id) or message.chat.type != "private":
        return
    lang = await get_lang(message.from_user.id)
    rows = await db.deliverables_summary()
    if not rows:
        await message.answer(t("no_materials", lang))
        return
    agg = {}
    for r in rows:
        pname = r["project"] or "—"
        agg.setdefault(pname, {"visual": 0, "video": 0})
        agg[pname][r["kind"]] = r["cnt"]
    lines = [t("materials_header", lang, day=db.today()), ""]
    tv = tvid = 0
    for pname, c in agg.items():
        lines.append(t("mat_line", lang, project=pname, visual=c["visual"], video=c["video"]))
        tv += c["visual"]; tvid += c["video"]
    lines.append(t("mat_total", lang, visual=tv, video=tvid))
    await message.answer("\n".join(lines))
