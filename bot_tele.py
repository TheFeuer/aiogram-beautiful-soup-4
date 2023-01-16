import asyncio
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from main import check_new_apart

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
user_id = os.getenv("ID")

bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    start_button = ["Все объявления", "Последние 6", "Свежие объявления"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer("Этот бот будет присылать актуальные объявления "
                         "на сайте |Крыша| по заданному фильтру "
                         "до 180000т и в выделенной области", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все объявления"))
async def new_all_promo(message: types.Message):
    with open("new_apart.json") as file:
        new_apart = json.load(file)

    for a, b in sorted(new_apart.items()):
        apart = f'{hbold(b["card_date"])}\n' \
                f'Цена: {hcode(b["card_price"])}\n' \
                f'{hlink(b["card_title"], b["card_url"])}'

        await message.answer(apart)


@dp.message_handler(Text(equals="Последние 6"))
async def get_last_six(message: types.Message):
    with open("new_apart.json") as file:
        new_apart = json.load(file)

    for a, b in sorted(new_apart.items())[-6:]:
        apart = f'{hbold(b["card_date"])}\n' \
                f'Цена: {hcode(b["card_price"])}\n' \
                f'{hlink(b["card_title"], b["card_url"])}'

        await message.answer(apart)


@dp.message_handler(Text(equals="Свежие объявления"))
async def get_fresh_promo(message: types.Message):
    fresh_apart = check_new_apart()

    if len(fresh_apart) >= 1:
        for a, b in sorted(fresh_apart.items()):
            apart = f'{hbold(b["card_date"])}\n' \
                    f'Цена: {hcode(b["card_price"])}\n' \
                    f'{hlink(b["card_title"], b["card_url"])}'

            await message.answer(apart)
    else:
        await message.answer("На данный момент нет новых объявлений")


async def new_apart_every_hour():
    while True:
        fresh_apart = check_new_apart()

        if len(fresh_apart) >= 1:
            for a, b in sorted(fresh_apart.items()):
                apart = f'{hbold(b["card_date"])}\n' \
                        f'Цена: {hcode(b["card_price"])}\n' \
                        f'{hlink(b["card_title"], b["card_url"])}'

                await bot.send_message(user_id, apart, disable_notification=True)
        else:
            await bot.send_message(user_id, "На данный момент нет новых объявлений", disable_notification=True)

        await asyncio.sleep(7200)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(new_apart_every_hour())
    executor.start_polling(dp, skip_updates=True)
