import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from quiz_handler import handle_event

# Инициализация бота
vk_session = vk_api.VkApi(token="your_token")
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "your_group_id")

# Обработка событий
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
        handle_event(event, vk)
