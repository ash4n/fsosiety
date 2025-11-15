from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏢 Настроить профиль НКО', callback_data='input_nko_info')],
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
        [InlineKeyboardButton(text='Свободная', callback_data='text_gen_input')],
        [InlineKeyboardButton(text='Структурированная', callback_data='text_gen_input')],
    ])

def get_text_styles():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Информационный / Образовательный', callback_data='informational')],
        [InlineKeyboardButton(text='Развлекательный / Юмористический', callback_data='humorous')],
        [InlineKeyboardButton(text='Вовлекающий (для вовлечения аудитории)', callback_data='engaging')],
        [InlineKeyboardButton(text='Вдохновляющий / Мотивирующий', callback_data='inspiring')],
        [InlineKeyboardButton(text='Личный / История', callback_data='personal')],
        [InlineKeyboardButton(text='Новостной / Анонсирующий', callback_data='news')]     
    ])