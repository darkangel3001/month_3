from aiogram import Router, types
from aiogram.filters import Command

myinfo_router = Router()

@myinfo_router.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    user = message.from_user
    username = user.username if user.username else 'Не указан'
    msg = f"id: {user.id}\nusername: {username}\nfirst_name: {user.first_name}"
    await message.answer(msg)
