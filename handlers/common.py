from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from api import giga
from services import create_profile, add_npo_information
from states import MainStates

from keyboards import get_start_keyboard, get_menu_keyboard, get_text_generation_keyboard
from texts import common_texts
router = Router()


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

@router.callback_query(F.data == 'main_menu')
async def handle_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)
    

async def show_main_menu(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.main_menu)

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text='меню крч',
                                   reply_markup=get_menu_keyboard())
    else:
        text = event.text
        if text != "/start":
            await add_npo_information(info=text, user_id=event.from_user.id)
        await event.answer(text='меню тип',
                            reply_markup=get_menu_keyboard())


@router.callback_query(MainStates.main_menu, F.data == 'text_generation')
async def choose_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Выберите форму",
                                  reply_markup=get_text_generation_keyboard())

@router.callback_query(MainStates.main_menu, F.data == 'free')
async def text_input(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.free_text)
    await callback.message.answer(text="Введите текст:")

@router.message(MainStates.free_text)
async def generate_texts(message: types.Message, state: FSMContext):
    await state.set_state(MainStates.free_text)
    await message.answer(text="Генерирую текст, пожалуйста подождите")
    response = await giga.generate_text(message.text)
    await message.answer(text=response)
