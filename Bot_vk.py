import vk_api
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Инициализация бота
vk_session = vk_api.VkApi(token='vk1.a.I94bi_Xeu5lQ59AkBxt4O2bkkifXAmLyazWQXGVivVyaiyREJNt_dpXh_EmmIU8LpQB0XL9Vj3EJ2VwqSz9JVoRLEfy2DDuPjGzygJYFm6NUu_n4nba5GDdDnUMBjhre3ixmWib-CVgaqrQkhjkS1yavf_RFCMmqjhUm-g6DXEpDSe7MT3yASLgk_Z7_POrpl7vVE7boqvL4yx-hWAH5Ew')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, '228157636')
token = os.getenv("VK_TOKEN")
group_id = os.getenv("GROUP_ID")

# Функция для отправки сообщений с клавиатурой
def send_message(user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard.get_keyboard() if keyboard else None
    )

# Создание клавиатуры для главного меню с вертикальным расположением кнопок
def create_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Учащийся получил травму', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Производственная травма', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard

# Создание клавиатуры для выбора травм у учащегося
def create_student_injury_keyboard():
    keyboard = VkKeyboard(one_time=False)
    injuries = ['Ушиб головы', 'Ушиб ноги', 'Носовое кровотечение', 
                'Ушиб руки', 'Ушиб позвоночника', 'Защемление шеи', 
                'Царапина, порез', 'Обморок']
    for injury in injuries:
        keyboard.add_button(injury, color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard

# Основная функция для обработки событий
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
        user_id = event.obj.message['from_id']
        text = event.obj.message['text'].strip().lower()

        if text == 'начать':
            # Приветственное сообщение, когда пользователь впервые открывает диалог
            send_message(
                user_id,
                'Здравствуйте! Я бот, созданный Полиной Максимовной.\n'
                'Я помогу вам узнать, что делать в случае различных травм учащихся или сотрудников.\n'
                'Вы можете:\n'
                '- Узнать последовательность действий при травмах у учащихся.\n'
                '- Получить инструкции по производственным травмам.\n\n'
                'Педагог несет ответственность за жизнь и здоровье учащегося не только во время занятия, но и в перерывах тоже!\n'
                'Выберите нужную опцию ниже:',
                create_main_keyboard()
            )

        elif text == 'учащийся получил травму':
            send_message(
                user_id,
                'Выберите тип травмы у учащегося:',
                create_student_injury_keyboard()
            )

        elif text == 'производственная травма':
            send_message(
                user_id,
                'Действия при производственной травме с сотрудниками:\n'
                '1. Немедленно позвонить заместителю директора Зиновьевой Евгении Васильевне 89505654776, '
                'если не отвечает, директору Матухно Наталье Николаевне 89042015742 и сообщить о происшествии.\n'
                '2. Обратиться к врачу, вызов скорой помощи. Оформить обращение письменно.\n'
                '3. Оказать первую помощь пострадавшему или себе.',
                create_main_keyboard()
            )

        elif text == 'назад':
            send_message(
                user_id,
                'Выберите категорию:',
                create_main_keyboard()
            )

        # Обработка конкретных травм у учащихся
        elif text == 'ушиб головы':
            send_message(
                user_id,
                'Действия при ушибе головы:\n'
                '1. Ребенок должен принять горизонтальное положение.\n'
                '2. Обеспечить покой травмированной части.\n'
                '3. Приложить холод к травмированному участку не более чем на 20 минут.'
            )
            send_message(
                user_id,
                'Возможные симптомы сотрясения головного мозга:\n'
                '- головокружение;\n- тошнота;\n- нарушение координации движения;\n'
                '- изменение голоса;\n- нарушение слуха.'
            )

        elif text == 'ушиб ноги':
            send_message(
                user_id,
                'Действия при ушибе ноги:\n'
                '1. Обеспечить покой травмированной части.\n'
                '2. Приложить холод к травмированному участку не более чем на 20 минут.\n'
                '3. Сохранять покой, не двигать ногой. Если есть необходимость, зафиксировать ногу бинтом.'
            )

        elif text == 'носовое кровотечение':
            send_message(
                user_id,
                'Действия при носовом кровотечении:\n'
                '1. Попросить ребенка наклонить голову вперед, приложить бинт к ноздрям.\n'
                '2. Прижать одну ноздрю к носовой перегородке не более чем на 5-10 минут.\n'
                '3. Приложить холод к области переносицы на 15-20 минут.\n'
                '4. Если не помогает, скрутить марлевую повязку и вставить в носовой ход.'
            )

        elif text == 'ушиб руки':
            send_message(
                user_id,
                'Действия при ушибе руки:\n'
                '1. Обеспечить покой травмированной части.\n'
                '2. Приложить холод к травмированному участку не более чем на 20 минут.\n'
                '3. Сохранять покой, не двигать рукой.\n'
                '4. Если есть необходимость, зафиксировать руку бинтом.'
            )

        elif text == 'ушиб позвоночника':
            send_message(
                user_id,
                'Действия при ушибе позвоночника:\n'
                '1. Положить пострадавшего на твердую поверхность.\n'
                '2. Вызвать скорую медицинскую помощь.'
            )

        elif text == 'защемление шеи':
            send_message(
                user_id,
                'Действия при защемлении шеи:\n'
                '1. Положить пострадавшего на твердую поверхность.\n'
                '2. Вызвать скорую медицинскую помощь.'
            )

        elif text == 'царапина, порез':
            send_message(
                user_id,
                'Действия при царапине или порезе:\n'
                '1. Промыть рану чистой водой.\n'
                '2. Заклеить лейкопластырем.'
            )

        elif text == 'обморок':
            send_message(
                user_id,
                'Действия при обмороке:\n'
                '1. Положить ребенка в горизонтальное положение с приподнятыми ногами.\n'
                '2. Обеспечить приток свежего воздуха.\n'
                '3. Расстегнуть стесняющую одежду.\n'
                '4. Если в сознание не приходит в течение 3-5 минут, вызвать скорую помощь.'
            )

        else:
            send_message(
                user_id,
                'Извините, я не распознал ваш запрос. Пожалуйста, выберите из предложенных опций.',
                create_main_keyboard()
            )
