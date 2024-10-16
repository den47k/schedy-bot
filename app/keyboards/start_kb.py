from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Create schedule')]
], resize_keyboard=True, one_time_keyboard=True)

