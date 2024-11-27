from aiogram import Router, F, types
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    msg = f"Привет, {name}"
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://www.instagram.com/faiza_cafe?igsh=MTE5NXcxbHdqdXYyaA=="
                ),
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://faiza.kg/"
                ),
                types.InlineKeyboardButton(
                    text="Оставить отзыв",
                    callback_data="review"
                )
            ]
        ]
    )
    await message.answer(msg, reply_markup=kb)
