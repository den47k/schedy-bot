from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Cancel')]
], resize_keyboard=True, one_time_keyboard=True)
