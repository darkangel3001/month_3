from aiogram import F, Router, types
from aiogram.filters import Command

from bot_config import review_answer

dish_router = Router()

@dish_router.message(Command("menu"))
async def menu(message: types.Message):
    all_dishes = review_answer.fetch(
        "SELECT * FROM dishes ORDER BY price DESC"
    )
    print(all_dishes)
    await message.answer("Блюда нашего меню")
    for dish in all_dishes:
        await message.answer(F"-----{dish['name']}-----\n"
                             F"Цена: {dish['price']}сом\n"
                             F"Время готовки: {dish['cooking_time']}минут")