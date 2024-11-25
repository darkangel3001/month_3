from aiogram import Router, F, types, Dispatcher
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
    categories = State()

class Categories(StatesGroup):
    name = State()

@admin_rest_router.message(Command("new_categories"))
async def new_categories(message: types.Message, state: FSMContext):
    await state.set_state(Categories.name)
    await message.answer("Задайте новую категорию:")

@admin_rest_router.message(Categories.name)
async def process_cat(message: types.Message, state: FSMContext):
    category = message.text
    review_answer.execute(
        query="""
            INSERT INTO dish_categories (name)
            VALUES (?)
            """,
        params=(category, )
                     )
    await message.answer("Категория добавлена в БД")
    await state.clear()

@admin_rest_router.message(F.text.in_(["стоп", "stop"]))
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Добавление остановлено!")

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
    all_category = review_answer.fetch("SELECT * FROM dish_categories")
    if not all_category:
        await message.answer("Нет ни одной категории")
        await state.clear()
        return
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=dishes["name"]) for dishes  in all_category]
        ]
    )
    await state.set_state(Dishes.categories)
    await message.answer("Задайте категории блюда: ", reply_markup=kb)

@admin_rest_router.message(Dishes.categories)
async def process_categories(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    print(message.text)
    category_name = review_answer.fetch(
        query="SELECT name FROM dish_categories WHERE name = ?",
        params=(message.text,)
    )
    if not category_name:
        await message.answer("Вы напечатали не существующую категорию в БД")
        return
    await state.update_data(categories=category_name[0]["name"])
    data = await state.get_data()
    print(data)
    await state.clear()
    await message.answer("Блюдо добавлено", reply_markup=kb)
    review_answer.execute(
        query="""
        INSERT INTO dishes (name, price, cooking_time, categories)
        VALUES(?, ?, ?, ?)
        """,
        params=(data["name"], data["price"], data["cooking_time"], data["categories"]),
    )