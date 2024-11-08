from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# Функция для отправки сообщений с клавиатурой
def send_message(vk, user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard.get_keyboard() if keyboard else None
    )
# Обработка текстовых сообщений
def handle_message(user_id, text, vk):
    if text in ['привет', 'здравствуйте', 'добрый день']:
        send_message(
            vk,
            user_id,
            'Здравствуйте! Я бот, созданный для помощи педагогам.\n'
            'Вы можете узнать, что делать при травмах или пройти тест по материалу.',
            create_main_keyboard()
        )
    elif text == 'назад':
        send_message(
            vk,
            user_id,
            'Выберите категорию:',
            create_main_keyboard()
        )
    else:
        send_message(
            vk,
            user_id,
            'Извините, я не распознал ваш запрос. Пожалуйста, выберите из предложенных опций.',
            create_main_keyboard()
        )
# Создание клавиатуры главного меню
def create_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Учащийся получил травму', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Производственная травма', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard
