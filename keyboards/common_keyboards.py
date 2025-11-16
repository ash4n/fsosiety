from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callbacks import common_callbacks

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏢 Настроить профиль НКО', callback_data=common_callbacks.input_nko_info)],
        [InlineKeyboardButton(text='⏩ Пропустить → Главное меню', callback_data=common_callbacks.main_menu)]
    ])

def get_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🤖 Написание текста', callback_data=common_callbacks.text_generation)],
        [InlineKeyboardButton(text='🎨 Нарисовать картинку', callback_data=common_callbacks.image_generation)],
        [InlineKeyboardButton(text='📝 Исправление текста', callback_data=common_callbacks.text_editor)],
        [InlineKeyboardButton(text='⏳ Создание контент-плана', callback_data=common_callbacks.content_plan_creator)],
        [InlineKeyboardButton(text='💾 Сохраненные посты', callback_data=common_callbacks.saved_posts)],
        [InlineKeyboardButton(text='⚙️ Настройки НКО', callback_data=common_callbacks.input_nko_info)]
    ])

def text_editor_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📝 Исправить отправленный текст', callback_data=common_callbacks.edit_sended_text)],
        [InlineKeyboardButton(text='💾 Исправить сохраненные посты', callback_data=common_callbacks.saved_posts)],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)] 
    ])

def get_text_generation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔓 Свободная', callback_data=common_callbacks.text_gen_input)],
        [InlineKeyboardButton(text='🏗 Структурированная', callback_data=common_callbacks.text_gen_input_structurized)],
        [InlineKeyboardButton(text='📄 Сделать пост на основе другого', callback_data=common_callbacks.text_gen_input_copy)],
        [InlineKeyboardButton(text='💡 Попросить идею чего-либо (визуал)', callback_data=common_callbacks.text_gen_input_idea)],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)]
    ])

def get_text_styles_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📚 Информационный / Образовательный', callback_data='style0')],
        [InlineKeyboardButton(text='😄 Развлекательный / Юмористический', callback_data='style1')],
        [InlineKeyboardButton(text='👥 Вовлекающий (для вовлечения аудитории)', callback_data='style2')],
        [InlineKeyboardButton(text='✨ Вдохновляющий / Мотивирующий', callback_data='style3')],
        [InlineKeyboardButton(text='👤 Личный / История', callback_data='style4')],
        [InlineKeyboardButton(text='📰 Новостной / Анонсирующий', callback_data='style5')],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)]     
    ])
def back_to_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)]
    ])
def change_text_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Изменить текст', callback_data='change_text')]
    ])
def generate_another_one_image_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💾 Сохранить', callback_data=common_callbacks.save_post)],
        [InlineKeyboardButton(text='🎨 Создание картинки', callback_data=common_callbacks.image_generation)],
        [InlineKeyboardButton(text='📝 Написать текст', callback_data=common_callbacks.text_generation)],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)]
    ])
def generate_text_post_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔄 Создать заново', callback_data=common_callbacks.text_generation)],
        [InlineKeyboardButton(text='💾 Сохранить', callback_data=common_callbacks.save_text)],
        [InlineKeyboardButton(text='📚 Идеи оформления', callback_data=common_callbacks.visual_ideas)],
        [InlineKeyboardButton(text='🎨 Создание картинки', callback_data=common_callbacks.image_generation_text)],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)]        
    ])

def generate_post_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)],
        [InlineKeyboardButton(text='💾 Сохранить', callback_data=common_callbacks.save_post)],
    ])

def change_text_post_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='💾 Сохранить', callback_data='save_text_changes')],
    ])

def generate_content_plan_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💾 Сохранить', callback_data=common_callbacks.save_text)],
        [InlineKeyboardButton(text='🎨 Создание картинки', callback_data=common_callbacks.image_generation)],
        [InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)]
    ])

def get_saved_posts_keyboard(ids: list):
    keyboard = []
    count = 0
    for i in ids:
        count += 1
        keyboard.append([InlineKeyboardButton(text=f'Пост {count}', callback_data=f'{i[0]}')])
    keyboard.append([InlineKeyboardButton(text='⏩ Главное меню', callback_data=common_callbacks.main_menu)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)