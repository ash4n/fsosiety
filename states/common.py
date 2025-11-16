from aiogram.fsm.state import StatesGroup, State

class MainStates(StatesGroup):
    active = State()
    name_NPO = State()
    main_menu = State()
    image_caption_input = State()
    text_generation_state = State()
    content_plan_creation_state = State()
    saved_posts_state = State()
    edit_text_state = State()
    edit_post_text_state = State()
