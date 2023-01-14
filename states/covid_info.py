from aiogram.dispatcher.filters.state import StatesGroup, State


class GetInfo(StatesGroup):
    choose_country = State()
    more_info = State()
