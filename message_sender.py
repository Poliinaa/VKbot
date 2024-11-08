import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
def send_message(vk, user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard.get_keyboard() if keyboard else None
    )
# Функция для создания клавиатуры с вариантами ответов
def create_quiz_keyboard(options):
    keyboard = VkKeyboard(one_time=True)
    for option in options:
        keyboard.add_button(option, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    return keyboard
