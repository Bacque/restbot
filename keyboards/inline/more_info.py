from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn_get_details = InlineKeyboardButton(
    'Send me details', callback_data='more_info'
)
btn_close_dialog = InlineKeyboardButton(
    'I don`t need it', callback_data='close_dialog'
)
markup_more_info = InlineKeyboardMarkup().add(
    btn_get_details, btn_close_dialog
)
