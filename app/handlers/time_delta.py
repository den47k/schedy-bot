from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.utils import db
from app.keyboards.time_delta_kb import time_delta_kb


router = Router()


@router.callback_query(F.data == 'next_class')
async def display_next_class_schedule(callback: CallbackQuery):
    user_group = db.check_group_name(callback.from_user.id)[0]
    data = db.get_next_class(user_group)
    if data != callback.message.text:
        await callback.message.edit_text(text=data, reply_markup=time_delta_kb)
    else:
        await callback.answer('Next class schedule')


@router.callback_query(F.data == 'today')
async def display_today_schedule(callback: CallbackQuery):
    user_group = db.check_group_name(callback.from_user.id)[0]
    data = db.get_today(user_group)
    await callback.message.edit_text(text=data, reply_markup=time_delta_kb)


@router.callback_query(F.data == 'tomorrow')
async def display_tomorrow_schedule(callback: CallbackQuery):
    user_group = db.check_group_name(callback.from_user.id)[0]
    data = db.get_tomorrow(user_group)
    await callback.message.edit_text(text=data, reply_markup=time_delta_kb)


@router.callback_query(F.data == 'next_week')
async def display_next_week_schedule(callback: CallbackQuery):
    user_group = db.check_group_name(callback.from_user.id)[0]
    data = db.get_next_week(user_group)
    await callback.message.edit_text(text=data, reply_markup=time_delta_kb)


@router.callback_query(F.data == 'close')
async def close_schedule(callback: CallbackQuery):
    await callback.message.delete()
