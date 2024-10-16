from aiogram import Router, Bot, F
from aiogram.types import Message

from app.keyboards.time_delta_kb import time_delta_kb


router = Router()


@router.message(F.text == 'Get schedule')
async def get_schedule(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text='Choose your option', reply_markup=time_delta_kb)
    await message.delete()

