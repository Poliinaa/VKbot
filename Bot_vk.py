import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os

# Инициализация бота
vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, os.getenv("GROUP_ID"))

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
    keyboard.add_button('Квиз', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard

# Функция для создания клавиатуры с вариантами ответа
def create_quiz_keyboard(options):
    keyboard = VkKeyboard(one_time=False)
    for option in options:
        keyboard.add_button(option, color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    return keyboard

# Вопросы и варианты ответов для квиза
quiz_questions = [
    {
        'question': 'Что делать при ушибе головы?',
        'options': ['Положить ребенка в горизонтальное положение', 
                    'Дать выпить воды', 
                    'Уложить на живот'],
        'correct': 'Положить ребенка в горизонтальное положение'
    },
    {
        'question': 'Какой номер телефона скорой помощи?',
        'options': ['112', '101', '103'],
        'correct': '103'
    },
    {
        'question': 'Как проверить сознание пострадавшего?',
        'options': ['Потрясти пострадавшего', 'Спросить его имя', 'Проверить пульс'],
        'correct': 'Потрясти пострадавшего'
    },
    {
        'question': 'Что нужно сделать при носовом кровотечении?',
        'options': ['Наклонить голову вперед', 'Приложить холод к голове', 'Лежать на спине'],
        'correct': 'Наклонить голову вперед'
    },
    {
        'question': 'Что нужно делать при защемлении шеи?',
        'options': ['Положить пострадавшего на твердую поверхность', 'Массажировать шею', 'Немедленно вызвать скорую помощь'],
        'correct': 'Положить пострадавшего на твердую поверхность'
    },
    {
        'question': 'Как действовать при обмороке?',
        'options': ['Положить пострадавшего на спину', 'Дать выпить воды', 'Приложить холод'],
        'correct': 'Положить пострадавшего на спину'
    },
    {
        'question': 'Какой номер телефона для вызова пожарных?',
        'options': ['101', '103', '112'],
        'correct': '101'
    },
    {
        'question': 'Каковы симптомы сотрясения головного мозга?',
        'options': ['Головокружение', 'Нарушение слуха', 'Учащенное сердцебиение'],
        'correct': 'Головокружение'
    },
    {
        'question': 'Что делать при ушибе руки?',
        'options': ['Обеспечить покой и прикладывать холод', 'Дать отдых руке', 'Массажировать руку'],
        'correct': 'Обеспечить покой и прикладывать холод'
    },
    {
        'question': 'Каковы первые действия при производственной травме?',
        'options': ['Позвонить директору', 'Вызвать скорую помощь', 'Поставить в покой пострадавшего'],
        'correct': 'Позвонить директору'
    },
]

# Основная функция для обработки событий
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
        user_id = event.obj.message['from_id']
        text = event.obj.message['text'].strip().lower()

        # Обработка приветственных сообщений
        if text in ['привет', 'здравствуйте', 'добрый день', 'добрый вечер']:
            send_message(
                user_id,
                'Здравствуйте! Я бот, созданный Полиной Максимовной.\n'
                'Я помогу вам узнать, что делать в случае различных травм учащихся или сотрудников.\n'
                'Вы можете:\n'
                '- Узнать последовательность действий при травмах у учащихся.\n'
                '- Получить инструкции по производственным травмам.\n\n'
                'Педагог несет ответственность за жизнь и здоровье учащегося не только во время занятия, но и в перерывах!\n'
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

        elif text == 'квиз':
            # Запуск квиза
            question_index = 0
            correct_answers = 0

            # Вспомогательная функция для отправки вопросов и получения ответов
            def ask_question(question_index):
                if question_index < len(quiz_questions):
                    question = quiz_questions[question_index]
                    send_message(
                        user_id,
                        question['question'],
                        create_quiz_keyboard(question['options'])
                    )
                else:
                    # Выводим результат
                    send_message(
                        user_id,
                        f'Квиз завершен! Ваш результат: {correct_answers} из 10 правильных ответов.',
                        create_main_keyboard()
                    )

            # Начало квиза
            ask_question(question_index)

        elif text == 'назад':
            send_message(
                user_id,
                'Выберите категорию:',
                create_main_keyboard()
            )

        # Обработка ответов на вопросы квиза
        elif text in [question['options'][0].lower(), question['options'][1].lower(), 
                      question['options'][2].lower(), question['options'][3].lower()]:
            # Проверяем правильность ответа
            current_question = quiz_questions[question_index]
            if text == current_question['correct'].lower():
                correct_answers += 1
            question_index += 1

            # Переходим к следующему вопросу или завершению квиза
            ask_question(question_index)

        else:
            send_message(
                user_id,
                'Извините, я не распознал ваш запрос. Пожалуйста, выберите из предложенных опций.',
                create_main_keyboard()
            )
