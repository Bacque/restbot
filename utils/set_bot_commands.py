from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Adds user into DB"),
            types.BotCommand("news", "Gives new info about virus"),
            types.BotCommand("help", "Simple help command")
        ]
    )
