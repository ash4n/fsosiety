from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='ща', callback_data='yes')],
        [InlineKeyboardButton(text='не', callback_data='main_menu')],
    ])

def get_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='кнопка 1', callback_data='1')],
        [InlineKeyboardButton(text='кнопка 2', callback_data='2')],
        [InlineKeyboardButton(text='кнопка 3', callback_data='3')],
        [InlineKeyboardButton(text='кнопка 4', callback_data='4')],
    ])