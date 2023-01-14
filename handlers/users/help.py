from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from filters import IsPrivate


@dp.message_handler(IsPrivate(), CommandHelp(), state='*')
async def bot_help(message: types.Message):
    text = ("Commands: ",
            "/start - Adds you into DB",
            "/help - Simple help command",
            "/get_info - Gives info about COVID-19 for last 6 month",
            "/news - Gives you news about virus")

    await message.answer("\n".join(text))
