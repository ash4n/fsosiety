from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from io import BytesIO
import api.kandinsky
from aiogram.types import BufferedInputFile
import api.gigachat_api
import generate_prompt
from services import create_profile
from states import MainStates
import base64
from keyboards import get_start_keyboard, get_menu_keyboard
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
    
#функция запуска основного меню
async def show_main_menu(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.main_menu)

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text='меню крч',
                                   reply_markup=get_menu_keyboard())
    else:
        text = event.text
        # if text != "/start": твоя функця тут
        if text != "/start":
            await event.edit_text(text=f'{text}',
                            reply_markup=get_menu_keyboard())
        else:
            await event.answer(text=f'{text}',
                            reply_markup=get_menu_keyboard())
    
#/start -> 🏢 Настроить профиль НКО
@router.callback_query(MainStates.active, F.data == "input_nko_info")
async def get_text(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.name_NPO)
    await callback.message.edit_text("Название пиши и описание")

#menu->📝 Генерация текста
@router.callback_query(MainStates.main_menu, F.data == 'text_generation')
async def choose_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Выберите форму",
                                  reply_markup=get_text_generation_keyboard())

#menu->📝 Генерация текста -> Выберите форму
@router.callback_query(MainStates.main_menu, F.data == 'text_gen_input')
async def text_input(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.text_generation_state)
    await callback.message.edit_text(text="Какое событие? Когда оно проходит? Где оно проходит? Кто приглашен? Какие-то дополнительные детали?")

#menu->📝 Генерация текста -> Выберите форму -> после ввода текста
@router.message(MainStates.text_generation_state)
async def generate_texts(message: types.Message, state: FSMContext):
    await message.answer(text="Генерирую текст, пожалуйста подождите")
    response = await giga.generate_text(generate_prompt.generate_content_prompt(message.text))
    await message.answer(text=response)
    await state.set_state(MainStates.main_menu)

#/start -> 🏢 Настроить профиль НКО -> обработка текста
@router.message(MainStates.name_NPO)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await show_main_menu(message, state)

#меню ->  🎨 Генерация картинки 
@router.callback_query(F.data == 'image_generation')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.image_caption_input)
    await callback.message.edit_text(text=f"Введите текстовое описание картинки для генерации.",reply_markup=None)

#меню ->  🎨 Генерация картинки -> обработка текста
@router.message(MainStates.image_caption_input)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await message.answer(text="Генерирую изображение, пожалуйста подождите")
    
    prompt = await generate_prompt.GeneratePrompt.generate_prompt_for_image(
        user_request=message.text, 
        nko_information=None, 
        giga=giga
    )
    
    # Используем асинхронный контекстный менеджер для kandinsky
    async with kandinsky as api:
        image_data_base64 = await api.generate_image(prompt)
        image_data = base64.b64decode(image_data_base64)
        
        await message.answer_photo(
            photo=BufferedInputFile(image_data, filename="image.jpg"),
            caption="✅ Ваше сгенерированное изображение"
        )

