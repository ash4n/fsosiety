import generate_prompt
import textTypes.common_types as styleTypes
from base64 import b64decode
from api import giga,kandinsky
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from keyboards.common_keyboards import get_saved_posts_keyboard
from services import create_profile, set_nko_information, get_npo_information, create_post, get_posts_id, get_post, \
    add_text
from states import MainStates
from keyboards import *
from texts import common_texts
from callbacks import common_callbacks
from aiogram.exceptions import TelegramBadRequest
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
@router.callback_query(F.data == common_callbacks.main_menu)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)

#/start -> 🏢 Настроить профиль НКО -> обработка текста
@router.message(MainStates.name_NPO)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await set_nko_information(message.from_user.id,message.text)
    await message.answer(text=common_texts.saved_succesfully,reply_markup=back_to_main_keyboard())
    await state.set_state(MainStates.main_menu)

#функция запуска основного меню
async def show_main_menu(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(MainStates.main_menu)
    if isinstance(event, types.CallbackQuery):
        try:
            await event.message.edit_text(
                f"{common_texts.your_nko} {await get_npo_information(event.from_user.id)}",
                reply_markup=get_menu_keyboard()
            )
        except TelegramBadRequest:
            await event.message.answer(
                f"{common_texts.your_nko} {await get_npo_information(event.from_user.id)}",
                reply_markup=get_menu_keyboard()
            )
    else:
        text = event.text
        

        if text != "/start":
            await set_nko_information(event.from_user.id,text)
            await event.edit_text(text=f"{common_texts.your_nko} {await get_npo_information(event.from_user.id)}",
                            reply_markup=get_menu_keyboard())
            
        else:
            await event.answer(text=f"{common_texts.your_nko} {await get_npo_information(event.from_user.id)}",
                            reply_markup=get_menu_keyboard())
    
#/start -> 🏢 Настроить профиль НКО
@router.callback_query(F.data == common_callbacks.input_nko_info)
async def get_text(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.name_NPO)
    await callback.message.answer(common_texts.input_name_and_descryption)

#menu->📝 Генерация текста
@router.callback_query(MainStates.main_menu, F.data == common_callbacks.text_generation)
async def choose_form(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text(text=common_texts.choose_style,
                                  reply_markup=get_text_styles_keyboard())

#menu->📝 Генерация текста -> Выберите стиль
@router.callback_query(F.data.startswith('style'))
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    style_number = int(callback.data.replace('style', ''))
    styles = ['Информационный / Образовательный','Развлекательный / Юмористический','Вовлекающий (для вовлечения аудитории)','Вдохновляющий / Мотивирующий','Личный / История','Новостной / Анонсирующий']
    
    selected_style = styles[style_number]
    await state.set_state(MainStates.text_generation_state)
    await state.update_data(style=selected_style)

    
    await callback.message.edit_text(text=common_texts.choose_form,
                                  reply_markup=get_text_generation_keyboard())

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму
@router.callback_query(MainStates.text_generation_state, F.data == common_callbacks.text_gen_input)
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=common_texts.input_your_idea,reply_markup=back_to_main_keyboard())
    await state.set_state(MainStates.generating_text_state)
    await state.update_data(type = styleTypes.free)

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму
@router.callback_query(MainStates.text_generation_state, F.data == common_callbacks.text_gen_input_structurized)
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.generating_text_state)
    await callback.message.edit_text(text=common_texts.which_type_of_event,reply_markup=back_to_main_keyboard())
    await state.update_data(type = styleTypes.structurized)

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму
@router.callback_query(MainStates.text_generation_state, F.data == common_callbacks.text_gen_input_copy)
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.generating_text_state)
    await callback.message.edit_text(text=common_texts.example_of_post_and_improvements,reply_markup=back_to_main_keyboard())
    await state.update_data(type = styleTypes.copy)

@router.callback_query(MainStates.text_generation_state, F.data == common_callbacks.text_gen_input_idea)
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.generating_text_state)
    await callback.message.edit_text(text=common_texts.which_ideas,reply_markup=back_to_main_keyboard())
    await state.update_data(type = styleTypes.idea)

#menu->📝 Генерация текста -> Выберите стиль -> Выберите форму -> генерация текста
@router.message(MainStates.generating_text_state)
async def generate_texts(message: types.Message, state: FSMContext):
    await message.answer(text=common_texts.generating_text)
    data = await state.get_data()
    image = data.get("image") if data.get("image") else None
    style = data.get("style")
    print(message.text)
    if data.get("type") == styleTypes.free or data.get("type") == styleTypes.structurized:
        prompt = await generate_prompt.GeneratePrompt.generate_post_prompt(message.text,style,await get_npo_information(message.from_user.id))
        response = await giga.generate_text(prompt)
    elif data.get("type") == styleTypes.copy:
        response = await giga.generate_text(await generate_prompt.GeneratePrompt.generate_copy_of_post_prompt(message.text,style,await get_npo_information(message.from_user.id)))
    elif data.get("type") == styleTypes.idea:
        prompt = await generate_prompt.GeneratePrompt.generate_idea_prompt(message.text,style,await get_npo_information(message.from_user.id))
        response = await giga.generate_text(prompt)
    if image:
        image_data = b64decode(image)
        await message.answer_photo(
            photo=BufferedInputFile(image_data, filename="image.jpg"))
        await message.answer(response, reply_markup=generate_text_post_keyboard())
    else:
        await message.answer(text=response,reply_markup=generate_text_post_keyboard())
    await state.clear()
    await state.update_data(text=response)
    await state.update_data(image=image)
    await state.update_data(user_request=message.text)
    await state.set_state(MainStates.main_menu)

@router.callback_query(F.data == common_callbacks.save_text)
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    image = data.get("image") if data.get("image") else None
    await create_post(callback.from_user.id, text=text, image=image)
    await callback.message.edit_text(text=common_texts.saved_succesfully,reply_markup=back_to_main_keyboard())
    await state.clear()
    await state.set_state(MainStates.main_menu)

@router.callback_query(F.data == common_callbacks.saved_posts)
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.saved_posts_state)
    ids = await get_posts_id(callback.from_user.id)
    await callback.message.edit_text(text=common_texts.your_posts,reply_markup=get_saved_posts_keyboard(ids))

@router.callback_query(MainStates.saved_posts_state)
async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.main_menu)
    _id = int(callback.data)
    await state.update_data(_id = _id)
    image_data_base64, text = await get_post(user_id=callback.from_user.id, _id=_id)
    if not text:
        text = "Текст отсутствует"
    await state.update_data(text=text)
    await state.update_data(image=image_data_base64)
    if image_data_base64:
        image_data = b64decode(image_data_base64)
        await callback.message.answer_photo(
            photo=BufferedInputFile(image_data, filename="image.jpg"))
        await callback.message.answer(text, reply_markup=change_text_keyboard())
    else:
        await callback.message.edit_text(text=text,reply_markup=change_text_keyboard())

@router.callback_query(F.data == common_callbacks.change_text)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.edit_post_text_state)
    await callback.message.answer(text=common_texts.what_we_will_edit, reply_markup=back_to_main_keyboard())

@router.message(MainStates.edit_post_text_state)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    if data.get("text") != "Текст отсутствует":
        text = data.get("text") + message.text
    prompt = await generate_prompt.GeneratePrompt.generate_edit_text_prompt(text,await get_npo_information(message.from_user.id))
    response = await giga.generate_text(prompt)
    print(prompt)
    await state.update_data(text=response)
    await message.answer(text=response,reply_markup=change_text_post_keyboard())

@router.callback_query(F.data == common_callbacks.save_text_changes)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Успешно сохранено",reply_markup=back_to_main_keyboard())
    data = await state.get_data()
    text = data.get("text")
    _id = data.get("_id")
    await add_text(user_id=callback.from_user.id, _id=_id, info=text)
    await state.clear()
    await state.set_state(MainStates.main_menu)


#меню ->  🎨 Генерация картинки
@router.callback_query(F.data.startswith("image_generation"))
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.image_caption_input)
    if callback.data != common_callbacks.image_generation:
        await callback.message.answer(text=common_texts.text_descryption_for_picture,
                                         reply_markup=back_to_main_keyboard())
    else:
        await callback.message.edit_text(text=common_texts.text_descryption_for_picture,reply_markup=back_to_main_keyboard())

#меню ->  🎨 Генерация картинки 
@router.callback_query(F.data.startswith(common_callbacks.image_generation))
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.image_caption_input)
    if callback.data != common_callbacks.image_generation:
        await callback.message.answer(text=common_texts.text_descryption_for_picture,
                                         reply_markup=back_to_main_keyboard())
    else:
        await callback.message.edit_text(text=common_texts.text_descryption_for_picture,reply_markup=back_to_main_keyboard())

#меню ->  🎨 Генерация картинки -> картинка сгенерирована. Сделаем еще одну?
@router.message(MainStates.image_caption_input)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await message.answer(text=common_texts.wait_picture_generating)
    caption = common_texts.your_picture
    reply_markup = None
    data = await state.get_data()
    data_text = data.get("text")
    text = message.text
    if data_text:
        reply_markup = generate_post_keyboard()
        caption = data_text
        text += data_text 
    # Используем асинхронный контекстный менеджер для kandinsky
    async with kandinsky as api:

        image_data_base64 = await api.generate_image(message.text)
        image_data = b64decode(image_data_base64)

        await state.update_data(image=image_data_base64)
        if caption == common_texts.your_picture:
            await message.answer_photo(photo=BufferedInputFile(image_data, filename="image.jpg"),caption = caption)
            
        else:
            await message.answer_photo(photo=BufferedInputFile(image_data, filename="image.jpg"))
            await message.answer(caption, reply_markup=reply_markup)   
            
    await state.set_state(MainStates.main_menu)
    if not data_text:
        await message.answer(common_texts.generate_another_picture, reply_markup=generate_another_one_image_keyboard())


@router.callback_query(F.data == common_callbacks.save_post)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=common_texts.saved_succesfully,reply_markup=back_to_main_keyboard())
    data = await state.get_data()
    image = data.get("image")
    text = data.get("text")
    await create_post(user_id=callback.from_user.id, image=image, text=text)
    await state.clear()
    await state.set_state(MainStates.main_menu)

#меню ->  ⏳ Создание контент-плана
@router.callback_query(F.data == common_callbacks.content_plan_creator)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.content_plan_creation_state)
    await callback.message.edit_text(text=common_texts.text_descryption_for_plan,reply_markup=back_to_main_keyboard())

#/start -> ⏳ Создание контент-плана -> текст сгенерирован
@router.message(MainStates.content_plan_creation_state)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    prompt = await generate_prompt.GeneratePrompt.generate_content_plan_prompt(message.text,await get_npo_information(message.from_user.id))
    response = await giga.generate_text(prompt)
    await state.update_data(text=response)
    await message.answer(text=response,reply_markup=generate_content_plan_keyboard())
    await state.set_state(MainStates.main_menu)

#меню ->  📝 Редактор текста
@router.callback_query(F.data == common_callbacks.text_editor)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=common_texts.what_we_will_edit,reply_markup=text_editor_menu())

#меню ->  📝 Редактор текста -> 📝 Исправить отправленный текст -> ввод пользователя
@router.callback_query(F.data == common_callbacks.edit_sended_text)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.edit_text_state)
    await callback.message.edit_text(text=common_texts.input_post_for_improvement,reply_markup=back_to_main_keyboard())

@router.callback_query(F.data == common_callbacks.visual_ideas)
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(common_texts.generating_text)
    data = await state.get_data()
    response = await giga.generate_text(await generate_prompt.GeneratePrompt.generate_idea_prompt(data.get("user_request") + " идеи оформления",data.get("style"),await get_npo_information(callback.from_user.id)))
    await callback.message.answer(text=response,reply_markup=back_to_main_keyboard())

@router.message(MainStates.edit_text_state)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    prompt = await generate_prompt.GeneratePrompt.generate_edit_text_prompt(message.text,await get_npo_information(message.from_user.id))
    response = await giga.generate_text(prompt)
    await state.update_data(text=response)
    await message.answer(text=response,reply_markup=generate_content_plan_keyboard())
    await state.set_state(MainStates.main_menu)
