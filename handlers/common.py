from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services import create_profile
from states import MainStates

from keyboards import get_start_menu
from texts import common_texts

router = Router()


@router.message(StateFilter(None), Command('start'))
async def start_bot(message: types.Message):
    await create_profile(user_id=message.from_user.id)
    button = [[InlineKeyboardButton(text='Продолжить', callback_data='start_instruction')]]
    await message.answer(text=common_texts.welcome,
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=button))



@router.callback_query(StateFilter(None), F.data == "start_instruction")
async def read_instruction(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.instruction)
    await callback.message.answer(text='🎁 Вам начислено 7 дней! ')
    await callback.message.answer(text=common_texts.instruction, disable_web_page_preview=True,
                                     reply_markup=get_start_menu())

@router.callback_query(F.data == "instruction")
async def read_instruction(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainStates.instruction)
    await callback.message.answer(text=common_texts.instruction, disable_web_page_preview=True,
                                     reply_markup=get_start_menu())