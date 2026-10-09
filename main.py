from aiogram import Bot, Dispatcher
import logging
import asyncio
from handlers import dates
from dotenv import load_dotenv
import os

load_dotenv()
token=os.environ["TELEGRAM_BOT_TOKEN"]

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(dates.router)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())

