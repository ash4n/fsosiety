from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏢 Настроить профиль НКО', callback_data='input_nko_info')],
        [InlineKeyboardButton(text='⏩ Пропустить → Главное меню', callback_data='main_menu')],
    ])

def get_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🤖 Генерация текста', callback_data='text_generation')],
        [InlineKeyboardButton(text='🎨 Генерация картинки', callback_data='image_generation')],
        [InlineKeyboardButton(text='📝 Редактор текста', callback_data='text_editor')],
        [InlineKeyboardButton(text='⏳ Создание контент-плана', callback_data='content_plan_creator')],
        [InlineKeyboardButton(text='💾 Сохраненные посты', callback_data='saved_posts')],
        [InlineKeyboardButton(text='⚙️ Настройки НКО', callback_data='input_nko_info')],
    ])

def get_text_generation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔓 Свободная', callback_data='text_gen_input')],
        [InlineKeyboardButton(text='🏗 Структурированная', callback_data='text_gen_input_structurized')],
        [InlineKeyboardButton(text='📄 Сгенерировать пост на основе другого', callback_data='text_gen_input_copy')],
        [InlineKeyboardButton(text='💡 Попросить идею чего-либо (визуал)', callback_data='text_gen_input_idea')],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')]
    ])

def get_text_styles_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📚 Информационный / Образовательный', callback_data='style0')],
        [InlineKeyboardButton(text='😄 Развлекательный / Юмористический', callback_data='style1')],
        [InlineKeyboardButton(text='👥 Вовлекающий (для вовлечения аудитории)', callback_data='style2')],
        [InlineKeyboardButton(text='✨ Вдохновляющий / Мотивирующий', callback_data='style3')],
        [InlineKeyboardButton(text='👤 Личный / История', callback_data='style4')],
        [InlineKeyboardButton(text='📰 Новостной / Анонсирующий', callback_data='style5')],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')]     
    ])
def back_to_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')]
    ])
def generate_another_one_image_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎨 Генерация картинки', callback_data='image_generation')],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')]
    ])
def generate_text_post_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔄 Сгенерировать заново', callback_data='text_generation')],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='💾 Сохранить', callback_data='save_text')],
        [InlineKeyboardButton(text='🎨 Добавить картинку', callback_data='image_generation_text')]
    ])

def generate_post_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='💾 Сохранить', callback_data='save_post')],
    ])

def generate_content_plan_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='💾 Сохранить', callback_data='save_text')],
        [InlineKeyboardButton(text='🎨 Генерация картинки', callback_data='image_generation')]
    ])

def get_saved_posts_keyboard(ids: list):
    keyboard = []
    count = 0
    for i in ids:
        count += 1
        keyboard.append([InlineKeyboardButton(text=f'Пост {count}', callback_data=f'{i[0]}')])
    keyboard.append([InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)