from aiogram.dispatcher.filters.state import StatesGroup, State


class GetNews(StatesGroup):
    news_menu = State()
