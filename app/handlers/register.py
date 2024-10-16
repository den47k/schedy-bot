from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.utils import db
from app.keyboards.start_kb import start_kb
from app.keyboards.cancel_kb import cancel_kb
from app.keyboards.main_menu_kb import main_menu_kb
from app.utils.messages import MAIN_MENU_TEXT, ENTER_GROUP_TEXT


router = Router()


class RegisterState(StatesGroup):
    reg_group_name = State()


@router.message(F.text == 'Edit schedule')
@router.message(F.text == 'Create schedule')
async def start_register(message: Message, state: FSMContext, bot: Bot):
    await message.delete()

    db.create_user(message.from_user.id)
    await bot.send_message(message.from_user.id, ENTER_GROUP_TEXT, reply_markup=cancel_kb)
    await state.set_state(RegisterState.reg_group_name)


@router.message(F.text == 'Cancel')
async def cancel_registration(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    if db.check_group_name(message.from_user.id)[0]:
        await bot.send_message(message.from_user.id, text='Action cancelled', reply_markup=main_menu_kb)
    else:
        await bot.send_message(message.from_user.id, text='Action cancelled', reply_markup=start_kb)
    await state.clear()


@router.message(RegisterState.reg_group_name)
async def get_group_name(message: Message, state: FSMContext, bot: Bot):
    if message.text in db.get_groups_list():
        await state.update_data(group_name=message.text)
        data = await state.get_data()
        group_name = data.get('group_name')

        db.edit_created_user(message.from_user.id, group_name)
        await message.delete()
        await bot.send_message(message.from_user.id,
                               MAIN_MENU_TEXT.format(group_name=db.check_group_name(message.from_user.id)[0]),
                               reply_markup=main_menu_kb
                               )
        await state.clear()
    else:
        await message.delete()
        await bot.send_message(message.from_user.id, 'sikeeee, that`s the wrong number, try again')
