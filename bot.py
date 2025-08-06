import asyncio
import logging
import re
from aiogram.types import KeyboardButtonPollType
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Получение токена и ID чата из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Убедись, что это число

# Создание экземпляра бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Хранилище фильмов
movie_links = []

# Регулярка для ссылок на Кинопоиск
KINopoisk_PATTERN = re.compile(r"https?://(www\.)?kinopoisk\.ru/film/\S+")

@dp.message()
async def handle_movie_links(message: types.Message):
    if message.chat.id != CHAT_ID:
        return

    links = re.findall(r"https?://\S+", message.text)
    kino_links = [link for link in links if KINopoisk_PATTERN.match(link)]
    bad_links = [link for link in links if not KINopoisk_PATTERN.match(link)]

    response = ""

    if kino_links:
        suggested_movies.extend(kino_links)
        response += f"✅ Добавлены ссылки: {' | '.join(kino_links)}\n"

    if bad_links:
        response += f"⚠️ Не добавлены (некорректные): {' | '.join(bad_links)}"

    if response:
        await message.reply(response)

async def send_reminder():
    text = (
        "🎬 Пора выбирать фильм для киновечера!\n"
        "Отправьте ссылки на фильмы с Кинопоиска.\n"
        "📌 Дедлайн: до <b>четверга 19:00</b> по Москве."
    )
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder, CronTrigger(day_of_week='wed', hour=20, minute=00, timezone="Europe/Moscow"))

    
@dp.startup()
async def schedule_vote():
    scheduler.add_job(send_vote_poll, CronTrigger(day_of_week='wed', hour=20, minute=28, timezone="Europe/Moscow"))

scheduler.start()

async def send_vote_poll():
    if not movie_links:
        await bot.send_message(CHAT_ID, "Фильмы для голосования не были предложены.")
        return

    options = [f"🎬 {link}" for link in movie_links]
    await bot.send_poll(
        chat_id=CHAT_ID,
        question="Выбираем фильм для киновечера 🎥",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

    movie_links.clear()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
