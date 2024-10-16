from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Get schedule')],
    [KeyboardButton(text='Edit schedule')]
], resize_keyboard=True)
