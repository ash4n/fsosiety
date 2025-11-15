from aiogram.fsm.state import StatesGroup, State

class MainStates(StatesGroup):
    active = State()
    name_NPO = State()
    main_menu = State()
    free_text = State()