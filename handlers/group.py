from aiogram import Router, F, types
from aiogram.filters import Command
from datetime import datetime, timedelta

group_router = Router()


@group_router.message(Command("ban", prefix="!"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Сделайте реплай на сообщение пользователя, чтобы активировать команду бан!")
        return

    id = message.reply_to_message.from_user.id
    until_date = datetime.now() + timedelta(days=1)
    try:
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            until_date=until_date
        )
        await message.answer(f"Пользователь {id} заблокирован на 1 день.")
    except Exception as e:
        await message.answer(f"Ошибка при блокировке: {e}")

bad_words = ['дурак', 'тупой', 'дебил', 'пидарас', 'козел', 'идиот']


@group_router.message(F.text)
async def ms_group(message: types.Message):
    for word in bad_words:
        if word in message.text.lower():
            await message.answer("Данное слово запрещено")
            await message.delete()
            try:
                await message.bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id
                )
                await message.answer(
                    f"Пользователь {message.from_user.id} заблокирован за использование запрещенных слов.")
            except Exception as e:
                await message.answer(f"Ошибка при блокировке: {e}")
            break

@group_router.message(F.photo)
async def delete_images(message: types.Message):
    try:
        await message.delete()
        await message.answer("Отправка картинок запрещена!")
    except Exception as e:
        await message.answer(f"Ошибка при удалении: {e}")