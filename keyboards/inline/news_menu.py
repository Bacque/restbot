from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_previous = InlineKeyboardButton(
    'Previous ◀️', callback_data='previous'
)
btn_next = InlineKeyboardButton(
    'Next ▶️', callback_data='next'
)
btn_close = InlineKeyboardButton(
    'Close ❌', callback_data='close'
)
start = InlineKeyboardMarkup(row_width=1).add(
    btn_next, btn_close
)
end = InlineKeyboardMarkup(row_width=1).add(
    btn_previous, btn_close
)
middle = InlineKeyboardMarkup(row_width=2).add(
    btn_previous, btn_next, btn_close
)
