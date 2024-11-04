import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client import bot
from aiogram.filters import Command
from dotenv import dotenv_values
from random import choice


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    msg = f"Привет, {name}!"
    await message.answer(msg)

@dp.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    id = message.from_user.id
    name = message.from_user.username
    if message.from_user.username is None:
        name = 'Не указан'
    first_name = message.from_user.first_name
    msg = f'id: {id}\nname: {name}\nfirst_name: {first_name}'
    await message.answer(msg)

@dp.message(Command("random"))
async def random_handler(message: types.Message):
    name_list = ('Эржан', 'Игорь', 'Азирет', 'Алихан')
    random_name = choice(name_list)
    msg = random_name
    await message.answer(msg)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())