from aiogram.exceptions import TelegramBadRequest

import generate_prompt
import keyboards.common_keyboards
from helpers import escape_markdown_v2
from base64 import b64decode
from api import giga,kandinsky
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from io import BytesIO
from aiogram.types import BufferedInputFile

from keyboards.common_keyboards import get_saved_posts_keyboard
from services import create_profile, set_nko_information, get_npo_information, create_post, get_posts_id, get_post
from states import MainStates
from keyboards import *
from texts import common_texts

router = Router()

#/start (первый запуск)
@router.message(StateFilter(None), Command('start'))
async def start_bot(message: types.Message, state: FSMContext):
    await create_profile(user_id=message.from_user.id)
    await state.set_state(MainStates.active)
    await message.answer(text=common_texts.welcome,
                         reply_markup=get_start_keyboard())

#/start (после первого запуска)
@router.message(Command('start'), ~StateFilter(None))
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await show_main_menu(message, state)

#/start -> ⏩ Пропустить → Главное меню
@router.callback_query(F.data == 'main_menu')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)

#/start -> 🏢 Настроить профиль НКО -> обработка текста
@router.message(MainStates.name_NPO)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await set_nko_information(message.from_user.id,message.text)
    await message.answer(text="Изменения сохранены!",reply_markup=back_to_main_keyboard())
    await state.set_state(MainStates.main_menu)

#функция запуска основного меню
async def show_main_menu(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(MainStates.main_menu)
    if isinstance(event, types.CallbackQuery):
        try:
            await event.message.edit_text(
                "меню крч",
                reply_markup=get_menu_keyboard()
            )
        except TelegramBadRequest:
            await event.message.answer(
                "меню крч",
                reply_markup=get_menu_keyboard()
            )
    else:
        text = event.text
        

        if text != "/start":
            await set_nko_information(event.from_user.id,text)
            await event.edit_text(text=f'{text}',
                            reply_markup=get_menu_keyboard())
            
        else:
            await event.answer(text=f'{text}',
                            reply_markup=get_menu_keyboard())
    
#/start -> 🏢 Настроить профиль НКО
@router.callback_query(F.data == "input_nko_info")
async def get_text(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.name_NPO)
    await callback.message.answer("Название пиши и описание")

#menu->📝 Генерация текста
@router.callback_query(MainStates.main_menu, F.data == 'text_generation')
async def choose_form(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text(text="Выберите стиль",
                                  reply_markup=get_text_styles_keyboard())

#menu->📝 Генерация текста -> Выберите стиль
@router.callback_query(F.data.startswith('style'))
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    style_number = int(callback.data.replace('style', ''))
    styles = ['Информационный / Образовательный','Развлекательный / Юмористический','Вовлекающий (для вовлечения аудитории)','Вдохновляющий / Мотивирующий','Личный / История','Новостной / Анонсирующий']
    
    selected_style = styles[style_number]
    await state.set_state(MainStates.text_generation_state)
    await state.update_data(style=selected_style)

    
    await callback.message.edit_text(text="Выберите форму",
                                  reply_markup=get_text_generation_keyboard())

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму
@router.callback_query(MainStates.text_generation_state, F.data == 'text_gen_input')
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введите свою идею для поста:",reply_markup=back_to_main_keyboard())
    await state.update_data(type = "free")

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму
@router.callback_query(MainStates.text_generation_state, F.data == 'text_gen_input_structurized')
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введите что за событие, дата, место, кто приглашён, дополнительные детали:",reply_markup=back_to_main_keyboard())
    await state.update_data(type = "structurized")

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму
@router.callback_query(MainStates.text_generation_state, F.data == 'text_gen_input_copy')
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введите пример поста который следует изменить, а также данные для изменения:",reply_markup=back_to_main_keyboard())
    await state.update_data(type = "copy")
@router.callback_query(MainStates.text_generation_state, F.data == 'text_gen_input_idea')
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Какие идеи вы хотите получить? Идеи визуала? Или может быть что другое?:",reply_markup=back_to_main_keyboard())
    await state.update_data(type = "idea")

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму -> генерация текста
@router.message(MainStates.text_generation_state)
async def generate_texts(message: types.Message, state: FSMContext):
    await message.answer(text="Генерирую текст, пожалуйста подождите")
    data = await state.get_data()
    style = data.get("style")
    print(message.text)
    if data.get("type") == "free" or data.get("type") == "structurized":
        prompt = await generate_prompt.GeneratePrompt.generate_post_prompt(message.text,style,await get_npo_information(message.from_user.id))
        response = await giga.generate_text(prompt)
    elif data.get("type") == "copy":
        response = await giga.generate_text(await generate_prompt.GeneratePrompt.generate_copy_of_post_prompt(message.text,style,await get_npo_information(message.from_user.id)))
    elif data.get("type") == "idea":
        prompt = await generate_prompt.GeneratePrompt.generate_idea_prompt(message.text,style,await get_npo_information(message.from_user.id))
        print(prompt)
        response = await giga.generate_text(prompt)
    await message.answer(text=escape_markdown_v2(response),parse_mode="MarkdownV2",reply_markup=generate_text_post_keyboard())
    await state.clear()
    await state.update_data(text=escape_markdown_v2(response))
    await state.set_state(MainStates.main_menu)





@router.callback_query(F.data == 'save_text')
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    await create_post(callback.from_user.id, text=text)
    await callback.message.edit_text(text="Успешно сохранено!",reply_markup=back_to_main_keyboard())
    await state.clear()
    await state.set_state(MainStates.main_menu)

@router.callback_query(F.data == 'saved_posts')
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.saved_posts_state)
    ids = await get_posts_id(callback.from_user.id)
    await callback.message.edit_text(text="Ваши посты",reply_markup=get_saved_posts_keyboard(ids))

@router.callback_query(MainStates.saved_posts_state)
async def handle_style_callback(callback: types.CallbackQuery):
    _id = int(callback.data)
    image, text = await get_post(user_id=callback.from_user.id, _id=_id)
    await callback.message.edit_text(text=f"{text}",reply_markup=back_to_main_keyboard(), parse_mode="MarkdownV2")


#меню ->  🎨 Генерация картинки 
@router.callback_query(F.data.startswith("image_generation"))
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.image_caption_input)
    if callback.data != "image_generation":
        await callback.message.answer(text=f"Введите текстовое описание картинки для генерации.",
                                         reply_markup=back_to_main_keyboard())
    else:
        await callback.message.edit_text(text=f"Введите текстовое описание картинки для генерации.",reply_markup=back_to_main_keyboard())

#меню ->  🎨 Генерация картинки -> картинка сгенерирована. Сделаем еще одну?
@router.message(MainStates.image_caption_input)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await message.answer(text="Генерирую изображение, пожалуйста подождите")
    caption = "✅Ваше сгенерированное изображение"
    reply_markup = None
    data = await state.get_data()
    data_text = data.get("text")
    text = message.text
    if data_text:
        reply_markup = generate_post_keyboard()
        caption = data_text
        text += data_text

    prompt = await generate_prompt.GeneratePrompt.generate_prompt_for_image(
        user_request=text,
        nko_information=await get_npo_information(message.from_user.id), 
        giga=giga
    )
    print(prompt)
    # Используем асинхронный контекстный менеджер для kandinsky
    async with kandinsky as api:
        image_data_base64 = await api.generate_image(text)
        image_data = b64decode(image_data_base64)
        
        await message.answer_photo(
            photo=BufferedInputFile(image_data, filename="image.jpg"),
            caption=caption,
            reply_markup=reply_markup)

    await state.set_state(MainStates.main_menu)
    if not data_text:
        await message.answer("❓Сгенерировать еще одно фото?", reply_markup=generate_another_one_image_keyboard())


#меню ->  ⏳ Создание контент-плана
@router.callback_query(F.data == 'content_plan_creator')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.content_plan_creation_state)
    await callback.message.edit_text(text=f"Введите текстовое описание контент плана для создания",reply_markup=back_to_main_keyboard())

#/start -> ⏳ Создание контент-плана -> текст сгенерирован
@router.message(MainStates.content_plan_creation_state)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    prompt = await generate_prompt.GeneratePrompt.generate_content_plan_prompt(message.text,await get_npo_information(message.from_user.id))
    print(prompt)
    response = await giga.generate_text(prompt)
    await message.answer(text=escape_markdown_v2(response),parse_mode="MarkdownV2",reply_markup=generate_content_plan_keyboard())
    await state.set_state(MainStates.main_menu)

#меню ->  📝 Редактор текста
@router.callback_query(F.data == 'text_editor')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=f"Выберите что вы хотите изменить: ",reply_markup=text_editor_menu())

#меню ->  📝 Редактор текста -> 📝 Исправить отправленный текст -> ввод пользователя
@router.callback_query(F.data == 'edit_sended_text')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.edit_text_state)
    await callback.message.edit_text(text=f"Введите исходный текст поста и изменения которые вы хотите применить. Например: исправить ошибки, добавить смайлики, предложения по улучшению поста: ",reply_markup=back_to_main_keyboard())

@router.message(MainStates.edit_text_state)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    prompt = await generate_prompt.GeneratePrompt.generate_edit_text_prompt(message.text,await get_npo_information(message.from_user.id))
    print(prompt)
    response = await giga.generate_text(prompt)
    await message.answer(text=escape_markdown_v2(response),parse_mode="MarkdownV2",reply_markup=generate_content_plan_keyboard())
    await state.set_state(MainStates.main_menu)
