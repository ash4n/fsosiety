from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👑 Оплатить VPN', callback_data='purchase')],
        [InlineKeyboardButton(text='🏆 Твоя конфигурация', callback_data='configuration')],
        [InlineKeyboardButton(text='📖 Инструкция', callback_data='instruction')],
        [InlineKeyboardButton(text='👥 Рефералы', callback_data='referrers')]
    ])