"""Avtomatik eslatmalar: deadline va kunlik hisobot."""
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
import database as db
from locales import t
from handlers import notify, notify_admins


async def check_deadlines(bot):
    """Muddati 60 daqiqa ichida tugaydigan yoki o'tib ketgan vazifalar bo'yicha eslatma."""
    now = datetime.now()
    soon = now + timedelta(minutes=60)
    for tk in await db.due_tasks_to_remind():
        try:
            dl = datetime.strptime(tk["deadline"], "%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            continue
        if dl <= soon:
            emp = await db.get_user(tk["assignee_id"])
            elang = emp["lang"] if emp else "uz"
            await notify(bot, tk["assignee_id"],
                         t("reminder_deadline", elang, id=tk["id"],
                           title=tk["title"], deadline=tk["deadline"]))
            ename = emp["full_name"] if emp else "?"
            await notify_admins(bot, t("reminder_deadline_admin", "uz",
                                id=tk["id"], assignee=ename, title=tk["title"]))
            await db.mark_reminded(tk["id"])


async def daily_report_reminder(bot):
    """Bugun hisobot yubormagan faol xodimlarga eslatma."""
    reports = await db.reports_for_day()
    reported = {r["user_id"] for r in reports}
    for e in await db.list_employees():
        if e["user_id"] not in reported:
            elang = e["lang"] or "uz"
            await notify(bot, e["user_id"], t("reminder_report", elang))


def setup_scheduler(bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
    scheduler.add_job(check_deadlines, "interval", minutes=15, args=[bot],
                      id="deadlines", replace_existing=True)
    scheduler.add_job(daily_report_reminder, "cron",
                      hour=config.DAILY_REPORT_HOUR,
                      minute=config.DAILY_REPORT_MINUTE,
                      args=[bot], id="daily_report", replace_existing=True)
    return scheduler
