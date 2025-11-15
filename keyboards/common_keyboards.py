from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏢 Настроить профиль НКО', callback_data='yes')],
        [InlineKeyboardButton(text='⏩ Пропустить → Главное меню', callback_data='main_menu')],
    ])

def get_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📝 Генерация текста', callback_data='text_generation')],
        [InlineKeyboardButton(text='🎨 Генерация картинки', callback_data='image_generation')],
        [InlineKeyboardButton(text='💾 Сохраненные посты', callback_data='saved_posts')],
        [InlineKeyboardButton(text='⚙️ Настройки НКО', callback_data='nko_settings')],
    ])

def get_text_generation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Свободная', callback_data='free')],
        [InlineKeyboardButton(text='Структурированная', callback_data='structured')],
    ])