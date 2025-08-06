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

@router.message(F.text)
async def handle_movie_links(message: Message):
    if datetime.now() > DEADLINE:
        await message.answer("⛔ Прием фильмов завершен.")
        return

    urls = re.findall(r'https?://\S+', message.text)

    valid_urls = []
    invalid_urls = []

    for url in urls:
        if re.match(KINOPOISK_URL_PATTERN, url):
            valid_urls.append(url)
        else:
            invalid_urls.append(url)

    # Сохраняем валидные ссылки
    for url in valid_urls:
        user_movie_suggestions.setdefault(message.from_user.id, []).append(url)

    if invalid_urls:
        await message.answer("⚠️ Некоторые ссылки недопустимы. Принимаются только ссылки на Кинопоиск.")
    elif valid_urls:
        await message.answer("✅ Фильм(ы) приняты!")

# Основная функция запуска
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
