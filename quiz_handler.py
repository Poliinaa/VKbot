questions = [
    {"question": "Как оказать первую помощь при ушибе головы?", "correct_answer": "1"},
    {"question": "Как вызвать скорую помощь?", "correct_answer": "112"},
    # Добавьте еще 8 вопросов
]
# Обработка опросов
def handle_quiz_event(user_id, vk):
    score = 0
    for i, question in enumerate(questions):
        vk.messages.send(
            user_id=user_id,
            message=f"Вопрос {i + 1}: {question['question']}",
            random_id=0
        )
        # Задержка или логика получения ответа пользователя (можно улучшить)
        # Вставьте логику ожидания ответа пользователя и проверки его ответа
    vk.messages.send(
        user_id=user_id,
        message=f"Ваш результат: {score} из {len(questions)} правильных ответов.",
        random_id=0
    )
