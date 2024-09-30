import os

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from config import syntax


async def sent_filters(cb: types.CallbackQuery):
    await cb.answer()
    data = cb.data.split()
    buttons, dr_name = [], []
    if len(data) == 2:
        for dr in os.listdir(f"cache/{data[1]}/"):
            dr_name.append(dr)
            buttons.append([types.InlineKeyboardButton(f"{syntax.get(data[1]).get(dr).get('name')}",
                                                       callback_data=f'filter {data[1]} {dr}')])
        buttons.append([types.InlineKeyboardButton('🔼 Меню', callback_data='menu')])
        markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await cb.message.edit_text(f"Раздел: {syntax.get(data[1]).get('name')}.", reply_markup=markup)
    elif len(data) == 3:
        for dr in os.listdir(f"cache/{data[1]}/{data[2]}"):
            dr_name.append(dr)
            buttons.append([types.InlineKeyboardButton(syntax.get(data[1]).get(data[2]).get(dr),
                                                       callback_data=f"{data[1]} {data[2]} {dr} send_photo")])
        buttons.append([types.InlineKeyboardButton('◀️ Назад', callback_data=f'back {data[1]}'),
                        types.InlineKeyboardButton('🔼 Меню', callback_data='menu')])
        markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await cb.message.edit_text(f"Раздел: {syntax.get(data[1]).get('name')}.\n"
                                   f"Категория: {syntax.get(data[1]).get(data[2]).get('name')}.",
                                   reply_markup=markup)


async def back(cb: types.CallbackQuery):
    await cb.answer()
    data = cb.data.split()
    buttons, dr_name = [], []
    for dr in os.listdir(f"cache/{data[1]}/"):
        dr_name.append(dr)
        buttons.append([types.InlineKeyboardButton(f"{syntax.get(data[1]).get(dr).get('name')}",
                                                   callback_data=f'filter {data[1]} {dr}')])
    buttons.append([types.InlineKeyboardButton('🔼 Меню', callback_data='menu')])
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.edit_text(f"Раздел: {syntax.get(data[1]).get('name')}.", reply_markup=markup)


async def back_location(cb: types.CallbackQuery):
    await cb.answer()
    data = cb.data.split()
    dr_name, buttons = [], []
    for dr in os.listdir(f"cache/{data[0]}/{data[1]}"):
        dr_name.append(dr)
        buttons.append([types.InlineKeyboardButton(syntax.get(data[0]).get(data[1]).get(dr),
                                                   callback_data=f"{data[0]} {data[1]} {dr} send_photo")])
    buttons.append([types.InlineKeyboardButton('◀️ Назад', callback_data=f'back {data[0]}'),
                    types.InlineKeyboardButton('🔼 Меню', callback_data='menu')])
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.edit_text(f"Раздел: {syntax.get(data[0]).get('name')}.\n"
                               f"Категория: {syntax.get(data[0]).get(data[1]).get('name')}.",
                               reply_markup=markup)


async def menu(cb: types.CallbackQuery):
    await cb.answer()
    text = """
Перед тобой ряд основных категорий мест, которые ты можешь посетить.
Выбери желаемую и продолжай искать что-нибудь по душе!
        """
    buttons = [[types.InlineKeyboardButton('Культура', callback_data='filter cultural')],
               [types.InlineKeyboardButton('Гастрономия', callback_data='filter gastronomy')],
               [types.InlineKeyboardButton('Общественные пространства', callback_data='filter public_spaces')],
               [types.InlineKeyboardButton('Развлечения', callback_data='filter entertainments')]]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.edit_text(text, reply_markup=markup)


def reg_filter_sent(dp: Dispatcher):
    dp.register_callback_query_handler(sent_filters, Text(startswith='filter'))
    dp.register_callback_query_handler(menu, text='menu')
    dp.register_callback_query_handler(back, Text(startswith='back'))
    dp.register_callback_query_handler(back_location, Text(endswith='back_location'))
