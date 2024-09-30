import os

from aiogram import types, Dispatcher
from aiogram.types import InputFile
from aiogram.dispatcher.filters import Text

from create import bot
from config import extensions


async def send_location(cb: types.CallbackQuery):
    await cb.answer()
    await cb.message.edit_text('Жди, материал загружается...')
    data = cb.data.split()
    dir_name = []
    buttons = [[types.InlineKeyboardButton('◀️ Назад', callback_data=f'{data[0]} {data[1]} {data[2]} back_location'),
                types.InlineKeyboardButton('🔼 Меню', callback_data='menu')]]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    with open(os.path.join('cache', data[0], data[1], data[2], f'{data[2]}.txt'), 'r', encoding='utf-8') as f:
        text = f.read()
    for e in extensions:
        for file in os.listdir(f"cache/{data[0]}/{data[1]}/{data[2]}"):
            dir_name.append(file)
        if f'{data[2]}.{e}' in dir_name:
            await bot.send_photo(cb.from_user.id, caption=text, photo=InputFile(os.path.join('cache', data[0], data[1], data[2], f'{data[2]}.{e}')))
            await cb.message.delete()
    await bot.send_message(cb.from_user.id, 'Хочешь посмотреть что-то еще?', reply_markup=markup)


def reg_send_location(dp: Dispatcher):
    dp.register_callback_query_handler(send_location, Text(endswith='send_photo'))
