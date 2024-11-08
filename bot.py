import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from message_handler import handle_message
from quiz_handler import handle_quiz_event
# Инициализация бота
vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, os.getenv("GROUP_ID"))
# Основная функция обработки событий
if __name__ == "__main__":
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            user_id = event.obj.message['from_id']
            text = event.obj.message['text'].strip().lower()
            if "вопрос" in text:
                handle_quiz_event(user_id, vk)
            else:
                handle_message(user_id, text, vk)
