import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
import logging

# Настройка логирования для отслеживания ошибок
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Инициализация бота
try:
    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, os.getenv("GROUP_ID"))
except Exception as e:
    logging.error("Ошибка при инициализации VK API: %s", e)
    raise

# Функция для отправки сообщений с клавиатурой
def send_message(user_id, message, keyboard=None):
    try:
        vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=0,
            keyboard=keyboard.get_keyboard() if keyboard else None
        )
    except vk_api.exceptions.ApiError as e:
        logging.error("Ошибка при отправке сообщения: %s", e)

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
    for injury in injuries:
        keyboard.add_button(injury, color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard

# Квизовые вопросы
quiz_questions = [
    {
        'question': 'Какие действия необходимо предпринять при ушибе головы?',
        'options': ['Положить пострадавшего в горизонтальное положение', 
                    'Позвонить родителям', 
                    'Немедленно вызвать полицию'],
        'answer': 0
    },
    {
        'question': 'Какое действие НЕ нужно делать при носовом кровотечении?',
        'options': ['Наклонить голову вперед', 
                    'Приложить холод к переносицы', 
                    'Запрокинуть голову назад'],
        'answer': 2
    },
    # Добавьте больше вопросов по аналогии
]

# Функция для создания клавиатуры для квиза
def create_quiz_keyboard(options):
    keyboard = VkKeyboard(one_time=True)
    for option in options:
        keyboard.add_button(option, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    return keyboard

# Основная функция для обработки событий
user_quiz_progress = {}  # Словарь для отслеживания прогресса квиза пользователей

try:
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
                    '1. Немедленно позвоните заместителю директора Зиновьевой Евгении Васильевне (89505654776). '
                    'Если она недоступна, позвоните директору Матухно Наталье Николаевне (89042015742).\n'
                    '2. Оповестите родителей (законных представителей).\n'
                    '3. Вызовите скорую медицинскую помощь, если это необходимо (03, 103, 112).',
                    create_main_keyboard()
                )

            elif text == 'назад':
                send_message(
                    user_id,
                    'Выберите категорию:',
                    create_main_keyboard()
                )

            # Обработка нажатия кнопки «Квиз»
            elif text == 'квиз':
                user_quiz_progress[user_id] = {'current_question': 0, 'correct_answers': 0}
                question_data = quiz_questions[0]
                send_message(
                    user_id,
                    f'Вопрос 1: {question_data["question"]}',
                    create_quiz_keyboard(question_data['options'])
                )

            # Обработка ответов на вопросы квиза
            elif user_id in user_quiz_progress:
                progress = user_quiz_progress[user_id]
                question_index = progress['current_question']
                question_data = quiz_questions[question_index]

                # Проверка правильности ответа
                if text == question_data['options'][question_data['answer']].lower():
                    progress['correct_answers'] += 1

                # Переход к следующему вопросу или окончание квиза
                if question_index + 1 < len(quiz_questions):
                    progress['current_question'] += 1
                    next_question_data = quiz_questions[progress['current_question']]
                    send_message(
                        user_id,
                        f'Вопрос {progress["current_question"] + 1}: {next_question_data["question"]}',
                        create_quiz_keyboard(next_question_data['options'])
                    )
                else:
                    correct_answers = progress['correct_answers']
                    send_message(
                        user_id,
                        f'Квиз завершен! Вы правильно ответили на {correct_answers} из {len(quiz_questions)} вопросов.',
                        create_main_keyboard()
                    )
                    del user_quiz_progress[user_id]

            # Обработка конкретных травм у учащихся с добавлением инструкций
            elif text in ['ушиб головы', 'ушиб ноги', 'носовое кровотечение', 'ушиб руки',
                          'ушиб позвоночника', 'защемление шеи', 'царапина, порез', 'обморок']:
                # Универсальная часть перед каждым инструктажем
                send_message(
                    user_id,
                    '1. Немедленно позвоните заместителю директора Зиновьевой Евгении Васильевне (89505654776). '
                    'Если она недоступна, позвоните директору Матухно Наталье Николаевне (89042015742).\n'
                    '2. Оповестите родителей (законных представителей).\n'
                    '3. Вызовите скорую медицинскую помощь, если это необходимо (03, 103, 112).'
                )

                # Индивидуальная инструкция по каждой травме
                if text == 'ушиб головы':
                    send_message(
                        user_id,
                        'Действия при ушибе головы:\n'
                        '1. Положите ребенка в горизонтальное положение.\n'
                        '2. Обеспечьте покой травмированной части.\n'
                        '3. Приложите холод к травмированному участку не более чем на 20 минут.'
                    )
                    send_message(
                        user_id,
                        'Возможные симптомы сотрясения мозга:\n'
                        '- Головокружение;\n- Тошнота;\n- Нарушение координации;\n'
                        '- Изменение речи;\n- Проблемы со слухом.'
                    )

                elif text == 'ушиб ноги':
                    send_message(
                        user_id,
                        'Действия при ушибе ноги:\n'
                        '1. Обеспечьте покой травмированной части.\n'
                        '2. Приложите холод к травмированному участку не более чем на 20 минут.\n'
                        '3. Зафиксируйте ногу, если это необходимо.'
                    )

                elif text == 'носовое кровотечение':
                    send_message(
                        user_id,
                        'Действия при носовом кровотечении:\n'
                        '1. Попросите ребенка наклонить голову вперед.\n'
                        '2. Приложите бинт к ноздрям и прижмите одну ноздрю к носовой перегородке на 5-10 минут.\n'
                        '3. Приложите холод к области переносицы на 15-20 минут.'
                    )

                elif text == 'ушиб руки':
                    send_message(
                        user_id,
                        'Действия при ушибе руки:\n'
                        '1. Обеспечьте покой травмированной части.\n'
                        '2. Приложите холод к травмированному участку не более чем на 20 минут.\n'
                        '3. Зафиксируйте руку, если это необходимо.'
                    )

                elif text == 'ушиб позвоночника':
                    send_message(
                        user_id,
                        'Действия при ушибе позвоночника:\n'
                        '1. Положите пострадавшего на твердую поверхность.\n'
                        '2. Вызовите скорую медицинскую помощь.'
                    )

                elif text == 'защемление шеи':
                    send_message(
                        user_id,
                        'Действия при защемлении шеи:\n'
                        '1. Положите пострадавшего на твердую поверхность.\n'
                        '2. Вызовите скорую медицинскую помощь.'
                    )

                elif text == 'царапина, порез':
                    send_message(
                        user_id,
                        'Действия при царапине или порезе:\n'
                        '1. Промойте рану чистой водой.\n'
                        '2. Наложите лейкопластырь.'
                    )

                elif text == 'обморок':
                    send_message(
                        user_id,
                        'Действия при обмороке:\n'
                        '1. Положите ребенка в горизонтальное положение с приподнятыми ногами.\n'
                        '2. Обеспечьте приток свежего воздуха.\n'
                        '3. Ослабьте стесняющую одежду.\n'
                        '4. Если ребенок не приходит в сознание в течение 3-5 минут, вызовите скорую помощь.'
                    )

            else:
                send_message(
                    user_id,
                    'Извините, я не распознал ваш запрос. Пожалуйста, выберите одну из предложенных опций.',
                    create_main_keyboard()
                )
except Exception as e:
    logging.error("Ошибка в основном цикле: %s", e)
