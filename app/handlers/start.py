from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.start_kb import start_kb
from app.keyboards.main_menu_kb import main_menu_kb
from app.utils import db
from app.utils.messages import START_TEXT, MAIN_MENU_TEXT


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    await message.delete()

    if db.check_group_name(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text=MAIN_MENU_TEXT.format(group_name=db.check_group_name(message.from_user.id)[0]),
                               reply_markup=main_menu_kb)
    else:
        await bot.send_message(message.from_user.id, text=START_TEXT, reply_markup=start_kb)
