"""Bot sozlamalari (.env fayldan o'qiladi)."""
import os
from dotenv import load_dotenv

load_dotenv()


def _parse_ids(raw: str) -> list[int]:
    ids = []
    for part in (raw or "").replace(" ", "").split(","):
        if part:
            try:
                ids.append(int(part))
            except ValueError:
                pass
    return ids


BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OWNER_IDS = _parse_ids(os.getenv("OWNER_IDS", ""))

_work_group = os.getenv("WORK_GROUP_ID", "").strip()
WORK_GROUP_ID = int(_work_group) if _work_group else None

TIMEZONE = os.getenv("TIMEZONE", "Asia/Tashkent").strip()
DAILY_REPORT_HOUR = int(os.getenv("DAILY_REPORT_HOUR", "18"))
DAILY_REPORT_MINUTE = int(os.getenv("DAILY_REPORT_MINUTE", "0"))

DB_PATH = os.getenv("DB_PATH", "manager_bot.db").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi. .env faylga BotFather tokenini yozing "
        "(.env.example dan nusxa oling)."
    )
if not OWNER_IDS:
    raise RuntimeError(
        "OWNER_IDS topilmadi. .env faylga o'z Telegram ID raqamingizni yozing."
    )


# Boshlang'ich loyihalar ro'yxati (birinchi ishga tushishda bazaga yoziladi).
# Keyinchalik botning "📁 Loyihalar" menyusidan qo'shish/o'zgartirish mumkin.
DEFAULT_PROJECTS = [
    "Hofmann uz",
    "Hofmann AIR",
    "SMEG",
    "Joseph Joseph",
    "Hofmann Next",
    "Hofmann Parkentskiy",
    "Hofmann Jomiy",
    "Hofmann Jomiy Outlet",
    "Hofmann Qoyliq",
    "Hofmann Qoyliq Outlet",
    "Great Generation",
    "Chico",
]
