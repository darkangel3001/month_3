from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

review_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


@review_router.message(Command("review"))
async def start_review(message: types.Message, state: FSMContext):
    await state.set_state(RestaurantReview.name)
    await message.answer("Как вас зовут?")

@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_number)
    await message.answer("Введите ваш номер телефона или Instagram:")

@review_router.message(RestaurantReview.phone_number)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer("Введите дату вашего посещения:")

@review_router.message(RestaurantReview.visit_date)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(RestaurantReview.food_rating)
    await message.answer("Как вы оцениваете качество еды? (1-5)")

@review_router.message(RestaurantReview.food_rating)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await state.set_state(RestaurantReview.cleanliness_rating)
    await message.answer("Как вы оцениваете чистоту заведения? (1-5)")

@review_router.message(RestaurantReview.cleanliness_rating)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(RestaurantReview.extra_comments)
    await message.answer("Дополнительные комментарии или жалобы (или пропустите, введя 'нет'):")

@review_router.message(RestaurantReview.extra_comments)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await message.answer("Спасибо за отзыв!")
    data = await state.get_data()
    print(data)
    await state.clear()