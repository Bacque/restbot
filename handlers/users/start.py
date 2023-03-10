import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.covid_info import GetInfo

from filters import IsPrivate
from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    username = message.from_user.username
    # Adding user into DB
    try:
        db.add_user(id=message.from_user.id,
                    username=username,
                    name=name)
        await message.answer(f"Welcome, {name}!")
        # Informing admins
        count = db.count_users()[0]
        msg = f"{message.from_user.full_name} joined to DB.\nThere are {count} users in DB."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} is already in DB")
        await message.answer(f"Welcome, {name}!")

    await GetInfo.choose_country.set()
    await message.answer('Send me name of the country')
