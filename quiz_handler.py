from quiz_questions import quiz_questions
from message_sender import send_message, create_quiz_keyboard
user_progress = {}
user_correct_answers = {}
# Функция для отправки вопроса
def send_quiz_question(vk, user_id, question_index):
    question_data = quiz_questions[question_index]
    send_message(vk, user_id, question_data['question'], 
create_quiz_keyboard(question_data['options']))
# Функция для обработки ответа
def handle_quiz_response(text, vk, user_id, question_index):
    correct_answer = quiz_questions[question_index]['answer']
    if text == correct_answer.lower():
        send_message(vk, user_id, 'Правильно! Отличная работа!')
        user_correct_answers[user_id] += 1  # Увеличиваем счетчик правильных 
ответов
    else:
        send_message(vk, user_id, f'Неверно. Правильный ответ: 
{correct_answer}')
# Основная функция для обработки событий
def handle_event(event, vk):
    user_id = event.obj.message['from_id']
    text = event.obj.message['text'].strip().lower()
    # Команда для начала опроса
    if text == 'начать опрос':
        user_progress[user_id] = 0  # Начинаем с первого вопроса
        user_correct_answers[user_id] = 0  # Инициализируем счетчик 
правильных ответов
        send_quiz_question(vk, user_id, user_progress[user_id])
    elif user_id in user_progress:
        # Если пользователь проходит опрос, проверяем ответ
        question_index = user_progress[user_id]
        handle_quiz_response(text, vk, user_id, question_index)
        # Переход к следующему вопросу, если есть
        if question_index + 1 < len(quiz_questions):
            user_progress[user_id] += 1
            send_quiz_question(vk, user_id, user_progress[user_id])
        else:
            # Опрос завершен, выводим результат
            correct_count = user_correct_answers[user_id]
            total_questions = len(quiz_questions)
            send_message(vk, user_id, f'Опрос завершен! Вы ответили правильно 
на {correct_count} из {total_questions} вопросов.')
            # Сбрасываем прогресс пользователя
            del user_progress[user_id]
            del user_correct_answers[user_id]
