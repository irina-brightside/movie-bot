import asyncio
import ssl
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
import certifi  # ✅ вот он

BOT_TOKEN = "8226924566:AAHOlJt5fL4NSgUQjDevhhZdwbsJAdrVylQ"

async def main():
    # 📌 Указываем явно путь к сертификатам от certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    connector = aiohttp.TCPConnector(ssl=ssl_context)
    client_session = aiohttp.ClientSession(connector=connector)
    session = AiohttpSession(client_session=client_session)

    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    @dp.message(F.text)
    async def echo_handler(message: Message):
        await message.answer(f"Ты написала: {message.text}")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await client_session.close()

if __name__ == "__main__":
    asyncio.run(main())