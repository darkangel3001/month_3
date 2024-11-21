from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot_config import review_answer

review_router = Router()


class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


rating_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=str(i)) for i in range(1, 6)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

date_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=str(i)) for i in range(1, 6)],
        [KeyboardButton(text=str(i)) for i in range(6, 11)],
        [KeyboardButton(text=str(i)) for i in range(11, 16)],
        [KeyboardButton(text=str(i)) for i in range(16, 21)],
        [KeyboardButton(text=str(i)) for i in range(21, 26)],
        [KeyboardButton(text=str(i)) for i in range(26, 32)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@review_router.message(F.text.in_(["стоп", "stop"]))
async def stop_review(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Отзыв был остановлен")

@review_router.callback_query(F.data == 'review')
async def start_review(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(RestaurantReview.name)
    await call.message.answer("Как вас зовут?")


@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_number)
    await message.answer("Введите ваш номер телефона или Instagram:")


@review_router.message(RestaurantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer("Введите дату вашего посещения:", reply_markup=date_keyboard)


@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    visit_date = message.text
    if not visit_date.isdigit():
        await message.answer("Вводите только цифры!")
        return
    visit_date = int(visit_date)
    if visit_date < 1 or visit_date > 31:
        await message.answer("Вводите дату от 1 до 31!")
        return

    await state.update_data(visit_date=message.text)
    await state.set_state(RestaurantReview.food_rating)
    await message.answer("Как вы оцениваете качество еды? (1-5)", reply_markup=rating_keyboard)


@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    food_rating = message.text
    if not food_rating.isdigit():
        await message.answer("Вводите только цифры!")
        return
    food_rating = int(food_rating)
    if food_rating < 1 or food_rating > 5:
        await message.answer("Вводите оценку от 1 до 5!")
        return

    await state.update_data(food_rating=message.text)
    await state.set_state(RestaurantReview.cleanliness_rating)
    await message.answer("Как вы оцениваете чистоту заведения? (1-5)", reply_markup=rating_keyboard)


@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    cleanliness_rating = message.text
    if not cleanliness_rating.isdigit():
        await message.answer("Вводите только цифры!")
        return
    cleanliness_rating = int(cleanliness_rating)
    if cleanliness_rating < 1 or cleanliness_rating > 5:
        await message.answer("Вводите чистоту заведения от 1 до 5!")
        return

    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(RestaurantReview.extra_comments)
    await message.answer("Дополнительные комментарии или жалобы (или пропустите, введя 'нет'):",
                         reply_markup=types.ReplyKeyboardRemove())


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await message.answer("Спасибо за отзыв!")
    data = await state.get_data()
    print(data)

    review_answer.execute(
        query="""
           INSERT INTO review (name, phone_number, visit_date, food_rating, 
           cleanliness_rating, extra_comments)
           VALUES (?, ?, ?, ?, ?, ?)
           """,
        params=(data["name"], data["phone_number"], data["visit_date"], data["food_rating"],
                data["cleanliness_rating"], data["extra_comments"])
    )

    await state.clear()