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

DEADLINE = datetime(2025, 8, 10, 21, 0)  # 10 августа 2025, 21:00 по МСК

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

# Хэндлер на команду /start
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("Привет! Я помогу вам выбрать фильм на киновечер! 🎬 Отправь мне сыылки на фильм с Кинопоиска."
                         f"Дедлайн: {DEADLINE.strftime('%d.%m.%Y %H:%M')} по МСК.")

@dp.message()
async def collect_links(message: Message):
    now = datetime.now()
    if now > DEADLINE:
        await message.answer("Прием ссылок завершён.")
        return

    if "kinopoisk.ru" in message.text:
        submitted_links.append((message.from_user.full_name, message.text))
        await message.answer("Ссылка принята ✅")
    else:
        await message.answer("Пожалуйста, отправь корректную ссылку на Кинопоиск.")

# Основная функция запуска
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



