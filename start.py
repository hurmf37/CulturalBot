from aiogram import types, Dispatcher
import sqlite3

from create import bot


async def start(msg: types.Message):
    await msg.bot.set_my_commands([
        types.BotCommand('start', 'Начать сначала')])
    try:
        with sqlite3.connect('database.db') as con:
            cursor = con.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS users('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, user_name TEXT, name TEXT);')
        with sqlite3.connect('database.db') as con:
            cursor = con.cursor()
            cursor.execute('SELECT * FROM users;')
            results = cursor.fetchall()
        data = []
        for line in results:
            data.append(line)
            if str(msg.from_user.id) in line:
                text = f"""
Привет, {line[3]}! Перед тобой ряд основных мест, которые ты можешь посетить.
Выбери желаемую категорию и продолжай искать что-нибудь по душе!
                """
                buttons = [[types.InlineKeyboardButton('Культура', callback_data='filter cultural')],
                           [types.InlineKeyboardButton('Гастрономия', callback_data='filter gastronomy')],
                           [types.InlineKeyboardButton('Общественные пространства', callback_data='filter public_spaces')],
                           [types.InlineKeyboardButton('Развлечения', callback_data='filter entertainments')]]
                markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                await bot.send_message(msg.from_user.id, text, reply_markup=markup)
                break
        else:
            with sqlite3.connect('database.db') as con:
                cursor = con.cursor()
                cursor.execute(f'INSERT INTO users VALUES('
                               f'NULL, "{msg.from_user.id}", "@{msg.from_user.username}", NULL);')
                buttons = [[types.InlineKeyboardButton('Давай!', callback_data='start')]]
                markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            await bot.send_message(msg.from_user.id, 'Привет! Я твой культурный помощник, давай начнем?',
                                   reply_markup=markup)
    except sqlite3.Error as e:
        print(e)


def reg_start(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
