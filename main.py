import asyncio
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random import random_router
from handlers.review_dialog import review_router



token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(myinfo_router)
dp.include_router(random_router)
dp.include_router(review_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
