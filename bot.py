"""Menejer bot — ishga tushirish nuqtasi."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
import database as db
from handlers import router
from scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("menejer_bot")


async def main():
    await db.init_db()
    await db.seed_projects(config.DEFAULT_PROJECTS)
    logger.info("Ma'lumotlar bazasi tayyor.")

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.info("Eslatma rejasi ishga tushdi.")

    me = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s", me.username)

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
