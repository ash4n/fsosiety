from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services import create_profile
from states import MainStates

from keyboards import get_start_keyboard, get_menu_keyboard
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
        await event.message.answer(text='меню крч',
                                   reply_markup=get_menu_keyboard())
    else:
        text = event.text
        # if text != "/start": твоя функця тут

        await event.edit_text(text=f'{text}',
                           reply_markup=get_menu_keyboard())
    
    

