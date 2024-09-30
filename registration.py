from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3

from create import bot


class RegistrationFSM(StatesGroup):
    join_name = State()


async def registration(cb: types.CallbackQuery):
    await cb.answer()
    await RegistrationFSM.join_name.set()
    await cb.message.edit_text('Привет! Я твой культурный помощник, давай начнем?')
    await bot.send_message(cb.from_user.id, 'Как тебя зовут?')


async def name(msg: types.Message, state: FSMContext):
    await state.finish()
    text = msg.text
    try:
        with sqlite3.connect('database.db') as con:
            cursor = con.cursor()
            cursor.execute(f'UPDATE users SET name = "{text}" WHERE user_id = "{msg.from_user.id}";')
        buttons = [[types.InlineKeyboardButton('Отлично!', callback_data='sentiment great')],
                   [types.InlineKeyboardButton('Хорошо', callback_data='sentiment good')],
                   [types.InlineKeyboardButton('Так себе', callback_data='sentiment so-so')]]
        markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await bot.send_message(msg.from_user.id, f'Как твое настроение сегодня, {text}?', reply_markup=markup)
    except sqlite3.Error as e:
        print(e)


async def sentiment(cb: types.CallbackQuery):
    await cb.answer()
    sent = cb.data.split()[1]
    if sent == 'great':
        text = """
Замечательно! Тогда самое время заняться чем-нибудь интересным!
        """
    elif sent == 'good':
        text = """
Хорошо - не плохо! Самое время заняться чем-нибудь интересным!
        """
    else:
        text = """
Тогда самое время поднять настроение и заняться чем-нибудь интересным!
        """
    await cb.message.edit_text(text)
    text2 = """
Перед тобой ряд основных категорий мест, которые ты можешь посетить.
Выбери желаемую и продолжай искать что-нибудь по душе!
    """
    buttons = [[types.InlineKeyboardButton('Культура', callback_data='filter cultural')],
               [types.InlineKeyboardButton('Гастрономия', callback_data='filter gastronomy')],
               [types.InlineKeyboardButton('Общественные пространства', callback_data='filter public_spaces')],
               [types.InlineKeyboardButton('Развлечения', callback_data='filter entertainments')]]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(cb.from_user.id, text2, reply_markup=markup)


def reg_registration(dp: Dispatcher):
    dp.register_callback_query_handler(registration, text='start')
    dp.register_message_handler(name, state=RegistrationFSM.join_name)
    dp.register_callback_query_handler(sentiment, Text(startswith='sentiment'))
