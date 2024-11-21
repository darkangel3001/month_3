from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot_config import review_answer

admin_rest_router = Router()

admin_rest_router.message.filter(
    F.from_user.id == 1629085599
)

class Dishes(StatesGroup):
    name = State()
    price = State()
    cooking_time = State()

# @admin_rest_router.message(F.text.in_(["стоп", "stop"]))
# async def stop(message: types.Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Добавление прервано")

@admin_rest_router.message(Command("dishes"), default_state)
async def dishes_start(message: types.Message, state: FSMContext):
    await state.set_state(Dishes.name)
    await message.answer("Введите название блюда")

@admin_rest_router.message(Dishes.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dishes.price)
    await message.answer("Задайте цену")

@admin_rest_router.message(Dishes.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Dishes.cooking_time)
    await message.answer("Задайте время готовки")

@admin_rest_router.message(Dishes.cooking_time)
async def process_cooking_time(message: types.Message, state: FSMContext):
    await state.update_data(cooking_time=message.text)
    await message.answer("Блюдо добавлено")
    data = await state.get_data()
    print(data)
    await state.clear()

    review_answer.execute(
        query="""
        INSERT INTO dishes (name, price, cooking_time)
        VALUES(?, ?, ?)
        """,
        params=(data["name"], data["price"], data["cooking_time"]),
    )