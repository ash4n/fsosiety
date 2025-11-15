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

kandinsky = api.kandinsky.AsyncFusionBrainAPI("","")
giga = api.gigachat_api.GigaChatAPI("")

@router.message(StateFilter(None), Command('start'))
async def start_bot(message: types.Message, state: FSMContext):
    await create_profile(user_id=message.from_user.id)
    await state.set_state(MainStates.active)
    await message.answer(text=common_texts.welcome,
                         reply_markup=get_start_keyboard())

@router.callback_query(MainStates.active, F.data == "yes")
async def get_text(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.name_NPO)
    await callback.message.edit_text("Название пиши и описание")


@router.message(MainStates.name_NPO)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await show_main_menu(message, state)

@router.message(Command('start'), ~StateFilter(None))
async def handle_start_non_none(message: types.Message, state: FSMContext):
    await show_main_menu(message, state)

@router.message(MainStates.image_caption_input)
async def handle_start_non_none(message: types.Message, state: FSMContext):
    image_data = base64.b64decode(kandinsky.generate_image(generate_prompt.GeneratePrompt.generate_prompt_for_image(message.text,None,giga)))

    await message.answer_photo(message.from_user.id,caption="✅ Ваше сгенерированное изображение",photo=BufferedInputFile(image_data, filename="image.jpg"))

@router.callback_query(F.data == 'main_menu')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):

    await show_main_menu(callback, state)
    
@router.callback_query(F.data == 'image_generation')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.image_caption_input)
    await callback.message.edit_text(text=f"Введите текстовое описание картинки для генерации.",reply_markup=None)



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
    