import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from standup.config import DEBUG

if DEBUG:
    import standup.debug_config as BotConfig
else:
    import standup.production_config as BotConfig
    
from standup.config_reader import *
from handlers import common, make_report
import datetime
from keyboards.simple_row import make_row_keyboard


config = debug_config if DEBUG else production_config



last_time_full = (datetime.datetime.today() + datetime.timedelta(hours=2)).strftime('%H:%M') #поправка на Нидерлады
time = last_time_full[:2] + last_time_full[3:]
print(time)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        filename=BotConfig.OUT_FILE_DIR
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())

    dp.include_router(common.router)
    dp.include_router(make_report.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
async def remind(t):
    bot = Bot(config.bot_token.get_secret_value())
    last_time = t
    while True:
        await asyncio.sleep(30)
        time_now_full = (datetime.datetime.today() + datetime.timedelta(hours=2)).strftime('%H:%M') #поправка на Нидерлады
        week_day = datetime.datetime.today().weekday()
        time_now = time_now_full[:2] + time_now_full[3:]
        if last_time != time_now:
            last_time = time_now
            text = f"Время заполнять стендап"
            if time_now == BotConfig.STANDUP_TIME and week_day in BotConfig.STANDUP_DAYS:
                for i in config.white_list:
                    try:
                        await bot.send_message(chat_id = i, text = text, reply_markup=make_row_keyboard(["Заполнить стендап", "Пропускаю в этот раз"]))
                    except BaseException:
                        print(f"Какая-то ошибка!!!")
                else:
                    try:
                        await bot.send_message(chat_id = config.admin_id.get_secret_value(), text = text, reply_markup=make_row_keyboard(["Заполнить стендап", "Пропускаю в этот раз"]))
                    except BaseException:
                        print(f"Какая-то ошибка!!!")
    
    
    

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete((asyncio.gather(remind(time), main())))

