from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), CommandStart())
async def command_start(message: types.Message):
    name = message.from_user.full_name
    link = 'https://t.me/ooo_my_defence_bot'
    await message.answer(
        f"Welcome, {name}!\n"
        f"Go to <a href='{link}'>private chat</a> with this bot in order to use main features!"
    )
