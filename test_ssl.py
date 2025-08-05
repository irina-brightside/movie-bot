import ssl
import certifi
import aiohttp
import asyncio

async def test_ssl():
    url = "https://api.telegram.org"

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=ssl_context) as response:
                print("✅ Успешное подключение!")
                print(f"Статус: {response.status}")
                print(f"Ответ: {await response.text()[:100]}...")
    except Exception as e:
        print("❌ Ошибка подключения:")
        print(repr(e))

asyncio.run(test_ssl())