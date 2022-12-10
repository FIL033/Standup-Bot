from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from utils.db import find_row, create_row

from standup.config import DEBUG

if DEBUG:
    import standup.debug_config as BotConfig
else:
    import standup.production_config as BotConfig

from standup.config_reader import *

config = debug_config if DEBUG else production_config

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Тут можно будет писать свои стендапы\n" 
             "Для отмены во время заполнения напишите (/cancel)",
        reply_markup=ReplyKeyboardRemove()
    )
    
    if not find_row(table_name="users", value=message.from_user.id, column_name="user_id") and message.from_user.id in config.white_list or str(message.from_user.id) == config.admin_id.get_secret_value():
        create_row(table_name="users", 
                   columns_name='(user_id, chat_id, username)',
                   row=(message.from_user.id, message.chat.id, message.from_user.username)
                   )
        


@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
