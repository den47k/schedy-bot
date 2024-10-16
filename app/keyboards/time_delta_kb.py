from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


buttons = [
    [
        InlineKeyboardButton(text='Next class', callback_data='next_class'),
        InlineKeyboardButton(text='Today', callback_data='today')
    ],
    [
        InlineKeyboardButton(text='Tomorrow', callback_data='tomorrow'),
        InlineKeyboardButton(text='Next week', callback_data='next_week')
    ],
    [
        InlineKeyboardButton(text='Close', callback_data='close')
    ]
]

time_delta_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
