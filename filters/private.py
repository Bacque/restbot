from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return isinstance(message.chat.type, type(types.ChatType.PRIVATE))
