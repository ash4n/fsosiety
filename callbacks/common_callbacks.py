from dataclasses import dataclass

@dataclass
class CommonCallbacks:
    input_nko_info: str = "input_nko_info"
    main_menu: str = "main_menu"
    text_generation: str = "text_generation"
    image_generation: str = "image_generation"
    text_editor: str = "text_editor"
    content_plan_creator: str = "content_plan_creator"
    saved_posts: str = "saved_posts"
    edit_sended_text: str = "edit_sended_text"
    text_gen_input: str = "text_gen_input"
    text_gen_input_structurized: str = "text_gen_input_structurized"
    text_gen_input_copy: str = "text_gen_input_copy"
    text_gen_input_idea: str = "text_gen_input_idea"
    save_text: str = "save_text"
    visual_ideas: str = "visual_ideas"
    image_generation_text: str = "image_generation_text"
    save_post: str = "save_post"

callbacks = CommonCallbacks()