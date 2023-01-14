from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), CommandHelp())
async def help_command(message: types.Message):
    msg = f"This bot doesn't work in groups or channels\n" \
          f"Please, follow the link below to use the bot!\n" \
          f"@ooo_my_defence_bot"
    await message.answer(msg)
