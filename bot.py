import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.token import validate_token
from dotenv import load_dotenv

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
    await message.answer("Привет! Я бот для выбора фильма 🎬")

# Основная функция запуска
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
