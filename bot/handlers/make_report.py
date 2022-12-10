from aiogram import Router, F

from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup,State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard
from utils.db import create_row

from standup.config import DEBUG

if DEBUG:
    import standup.debug_config as BotConfig
else:
    import standup.production_config as BotConfig
    
from standup.config_reader import *

config = debug_config if DEBUG else production_config


router = Router()

available_report_type = ["Заполнить стендап", "Пропускаю в этот раз"]
question = {'did':'Что вы делали с последнего стендапа?',
             'doing':'Что вы планируете делать следующие 2 дня?',
             'block':'Что блокирует ваш прогресс?'}


class OrderReport(StatesGroup):
    choose_submit_report = State()
    what_are_you_doing = State()
    what_do_you_wont_to_do = State()
    bloking_progress = State()
    
@router.message(Command(commands=["report"]))
async def cmd_report(message: Message, state: FSMContext):
    await message.answer(
        text="Надо что-то сделать",
        reply_markup=make_row_keyboard(available_report_type)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderReport.choose_submit_report)
    
@router.message(Text(text="Заполнить стендап"))
@router.message(Text(text="Пропускаю в этот раз"))
@router.message(OrderReport.choose_submit_report)
async def report_did(message: Message, state: FSMContext):
    if message.from_user.id in config.white_list or str(message.from_user.id) == config.admin_id.get_secret_value():
        if message.text == available_report_type[0]:
            await state.set_state(OrderReport.what_are_you_doing)
            await message.answer(
                text=question["did"],
                reply_markup=ReplyKeyboardRemove(),
            )
        elif message.text == available_report_type[1]:
            await message.answer(
                text="Очень жаль, что ты не заполнил стендап",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()
    
@router.message(OrderReport.what_are_you_doing)
async def report_doing(message: Message, state: FSMContext):
    await state.update_data(did=(message.text.lower(), "did"))
    await message.answer(
        text=question["doing"],
    )
    await state.set_state(OrderReport.what_do_you_wont_to_do)
    
@router.message(OrderReport.what_do_you_wont_to_do)
async def report_block(message: Message, state: FSMContext):
    await state.update_data(doing=(message.text.lower(), "doing"))
    await message.answer(
        text=question["block"],
    )
    await state.set_state(OrderReport.bloking_progress)
    
@router.message(OrderReport.bloking_progress)
async def report_chosen(message: Message, state: FSMContext):
    await state.update_data(block=(message.text.lower(), "block"))
    user_data = await state.get_data()
    user_ans = ''
    for item in user_data.values():
        user_ans += '<b>' + question[item[1]] + '</b>\n'
        user_ans += item[0] + '\n\n'
    await message.answer(
        text="Вот ваш стендап:\n\n" + user_ans,
        parse_mode="HTML"
    )
    await state.clear()
    create_row(table_name="standup", 
                   columns_name='(update_date, username, block, doing, did)',
                   row=(message.date, message.from_user.username, user_data['block'][0], user_data['doing'][0], user_data['did'][0])
                   )
