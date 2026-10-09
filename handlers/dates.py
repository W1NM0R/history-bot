from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

import aiosqlite
from random import shuffle

router = Router()

@router.message(Command("start"))
async def start(msg: types.Message):

    inline = InlineKeyboardBuilder()

    inline.add(types.InlineKeyboardButton(text="Получить список дат", callback_data="get-list"))
    inline.add(types.InlineKeyboardButton(text="Начать изучение дат", callback_data="learn-dates"))
    inline.adjust(1)

    await msg.reply("Бот для изучения дат. Выберите действие:", reply_markup=inline.as_markup())

@router.callback_query(F.data == "get-list")
async def get_list(cb: types.CallbackQuery):
    response=""

    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute("SELECT * FROM dates")
        rows = await cursor.fetchall()
        for date, event in rows:
            response += f"{date} - {event}\n"

    inline = InlineKeyboardBuilder()

    inline.add(types.InlineKeyboardButton(text="Начать изучение дат", callback_data="learn-dates"))

    await cb.message.answer(response, reply_markup=inline.as_markup())

@router.callback_query(F.data == "learn-dates")
async def learn_dates(cb: types.CallbackQuery):
    dates = list()

    inline = InlineKeyboardBuilder()

    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute("SELECT date, event FROM dates ORDER BY RANDOM() LIMIT 1")
        date_true, event = await cursor.fetchone()

        cursor = await db.execute("SELECT date FROM dates WHERE date != ? ORDER BY RANDOM() LIMIT 3", (date_true,))
        dates_fake_raw = await cursor.fetchall()

        for i in dates_fake_raw:
            for x in i: dates.append(x)

        dates.append(date_true)
        shuffle(dates)
    for i in dates:
        inline.add(types.InlineKeyboardButton(text=i, callback_data="true-date" if i == date_true else f"false:{date_true}"))

    inline.adjust(1)

    await cb.message.answer(f"Событие: {event}", reply_markup=inline.as_markup())

@router.callback_query(F.data == "true-date")
async def true_date(cb: types.CallbackQuery):
    inline = InlineKeyboardBuilder()
    inline.add(types.InlineKeyboardButton(text="Далее", callback_data="learn-dates"))

    await cb.message.answer("✅ Верно", reply_markup=inline.as_markup())

@router.callback_query(F.data.startswith("false:"))
async def false_date(cb: types.CallbackQuery):
    inline = InlineKeyboardBuilder()
    inline.add(types.InlineKeyboardButton(text="Далее", callback_data="learn-dates"))    

    await cb.message.answer(f"❌ Неверно\nПравильный ответ: {cb.data[:6]}", reply_markup=inline.as_markup())