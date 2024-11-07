from random import choice
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

random_router = Router()

# Список рецептов
recipes = [
    {"name": "Оливье", "image": "image/olivier.jpeg", "caption": "Рецепт: для Оливье нужно: картошку, горох, яйца, огурцы,колбасу или мясо ."},
    {"name": "Лагман", "image": "image/lagman.jpeg", "caption": "Рецепт: для Лагмана нужно: лапшу, мясо, зеленый и красные перцы, лук, и некоторые овощи по вкусу."},
    {"name": "Плов", "image": "image/plov.jpeg", "caption": "Рецепт: для плова нужно: рис, мясо, морковка ."},
]

@random_router.message(Command("random"))
async def random_handler(message: types.Message):
    recipe =choice(recipes)
    photo= FSInputFile(recipe['image'])
    await message.answer_photo(photo, caption=recipe["caption"])

