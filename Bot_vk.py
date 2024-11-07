import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Инициализация бота
vk_session = vk_api.VkApi(token='VK_TOKEN')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 'GROUP_ID')

# Функция для отправки сообщений с клавиатурой
def send_message(user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard.get_keyboard() if keyboard else None
    )

# Создание клавиатуры для главного меню
def create_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Учащийся получил травму', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Производственная травма', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Квиз', color=VkKeyboardColor.SECONDARY)
    return keyboard

# Создание клавиатуры для выбора травм у учащегося
def create_student_injury_keyboard():
    keyboard = VkKeyboard(one_time=False)
    injuries = ['Ушиб головы', 'Ушиб ноги', 'Носовое кровотечение',
                'Ушиб руки', 'Ушиб позвоночника', 'Защемление шеи',
                'Царапина, порез', 'Обморок']
    for i, injury in enumerate(injuries):
        keyboard.add_button(injury, color=VkKeyboardColor.POSITIVE)
        if (i + 1) % 4 == 0 and i != len(injuries) - 1:
            keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard

# Функция для создания клавиатуры для квиза
def create_quiz_keyboard(options):
    keyboard = VkKeyboard(one_time=True)
    for i, option in enumerate(options):
        keyboard.add_button(option, color=VkKeyboardColor.PRIMARY)
        if (i + 1) % 4 == 0 and i != len(options) - 1:
            keyboard.add_line()
    return keyboard

# Словарь с вопросами и ответами для квиза
quiz_questions = [
    {
        'question': 'Какие действия нужно предпринять при ушибе головы?',
        'options': ['Приложить холод', 'Наложить повязку', 'Оставить без внимания'],
        'correct': 'Приложить холод'
    },
    # Добавьте больше вопросов по аналогии
]

# Основная функция для обработки событий
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
        user_id = event.obj.message['from_id']
        text = event.obj.message['text'].strip().lower()

        if text == 'начать':
            send_message(
                user_id,
                'Здравствуйте! Я бот, созданный Полиной Максимовной.\n'
                'Я помогу вам узнать, что делать в случае различных травм учащихся или сотрудников.\n'
                'Вы можете:\n'
                '- Узнать последовательность действий при травмах у учащихся.\n'
                '- Получить инструкции по производственным травмам.\n'
                'Выберите нужную опцию ниже:',
                create_main_keyboard()
            )

        elif text in ['привет', 'здравствуйте', 'добрый день']:
            send_message(
                user_id,
                'Здравствуйте! Я могу:\n'
                '- Показать последовательность действий при травмах у учащихся.\n'
                '- Дать инструкции по производственным травмам.\n'
                '- Провести квиз на знание первой помощи.\n'
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
                'Действия при производственной травме:\n'
                '1. Немедленно позвоните заместителю директора Зиновьевой Евгении Васильевне 89505654776, '
                'если не отвечает, директору Матухно Наталье Николаевне 89042015742.\n'
                '2. Оповестите родителей.\n'
                '3. Вызовите скорую помощь при необходимости.',
                create_main_keyboard()
            )

        elif text == 'квиз':
            # Начало квиза
            send_message(
                user_id,
                'Начнем квиз! Вот первый вопрос:\n' + quiz_questions[0]['question'],
                create_quiz_keyboard(quiz_questions[0]['options'])
            )
            # Логика для обработки ответов и подсчета правильных ответов должна быть добавлена здесь

        elif text == 'назад':
            send_message(
                user_id,
                'Выберите категорию:',
                create_main_keyboard()
            )

        # Примеры обработки конкретных травм
        elif text == 'ушиб головы':
            send_message(
                user_id,
                '1. Необходимо незамедлительно позвонить заместителю директора Зиновьевой Евгении Васильевне '
                '89505654776, если не отвечает директору Матухно Наталье Николаевне 89042015742.\n'
                '2. Оповестите родителей.\n'
                '3. Вызовите скорую помощь при необходимости.'
            )
            send_message(
                user_id,
                'Действия при ушибе головы:\n'
                '1. Положите ребенка горизонтально.\n'
                '2. Обеспечьте покой травмированной части.\n'
                '3. Приложите холод к травмированному участку не более чем на 20 минут.\n'
                'Возможные симптомы сотрясения мозга:\n'
                '- головокружение;\n'
                '- тошнота;\n'
                '- нарушение координации;\n'
                '- изменение голоса;\n'
                '- нарушение слуха.'
            )

        # Добавьте аналогичные блоки для других травм

        else:
            send_message(
                user_id,
                'Извините, я не распознал ваш запрос. Пожалуйста, выберите одну из предложенных опций.',
                create_main_keyboard()
            )
