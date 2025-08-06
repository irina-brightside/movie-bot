from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import asyncio
import logging
import os
from datetime import datetime, timedelta
from aiogram import F
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.token import validate_token
from dotenv import load_dotenv


submitted_links = []

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка токена
validate_token(BOT_TOKEN)

# Логирование (для Railway обязательно, иначе не видно ошибок)
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Основная функция запуска
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    # Задачи по расписанию
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Moscow"))

# Каждую среду в 14:00 — напоминание о сборе фильмов
scheduler.add_job(
    send_reminder,
    CronTrigger(day_of_week="wed", hour=19, minute=27)
)

# Каждую следующую четверг в 19:00 — запуск голосования
scheduler.add_job(
    start_voting,
    CronTrigger(day_of_week="thu", hour=19, minute=0)
)

scheduler.start()

if __name__ == "__main__":
    asyncio.run(main())

# ID чата, куда бот будет писать (пока поставим временный заглушку)
GROUP_CHAT_ID = -4890829963

async def send_reminder():
    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="🎬 Пора выбирать фильм на киновечер! Пришлите ссылки на Кинопоиск до следующего четверга 19:00 🕖"
    )

async def start_voting():
    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="🗳 Время голосовать за фильм! Сейчас я запущу голосование..."
    )
    # Здесь потом подключим сбор фильмов и запуск голосовалки
