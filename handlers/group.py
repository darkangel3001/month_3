from aiogram import Router, F, types
from aiogram.filters import Command
from datetime import timedelta

group_router = Router()

@group_router.message(Command("ban", prefix=":"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("сделайте реплай на пользователя чтобы активировать команду бан!")
    else:
        id = message.reply_to_message.from_user.id
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            until_date=timedelta(days=1)
        )


bad_words = ['дурак','тупой','дебил','пидарас','козел','идиот']

@group_router.message(F.text)
async def ms_group(message: types.Message):
    for word in bad_words:
        if word in message.text.lower():
            await message.answer("Данное слово запрещено")
            await message.delete()
            await message.bot.ban_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id
            )
            break

#фото по приколу добавил если что
@group_router.message(F.photo)
async def delete_images(message: types.Message):
    await message.delete()
    await message.answer("Нельзя картинки и гифки")