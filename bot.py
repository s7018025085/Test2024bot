import os
import random
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Получаем токен бота и ссылку на репозиторий из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def start(update, context):
    update.message.reply_text('Привет! Я бот, который готов к работе.')

def get_random_question():
    # Получаем случайный вопрос из репозитория на GitHub
    try:
        response = requests.get(f"{GITHUB_REPO}/questions.json")
        questions = response.json()
        random_question = random.choice(questions)
        return random_question
    except Exception as e:
        print(f"Error fetching questions: {e}")
        return None

def ask_question(update, context):
    question_data = get_random_question()
    if question_data:
        question = question_data["question"]
        context.user_data['current_question'] = question
        update.message.reply_text(question)
    else:
        update.message.reply_text("Извините, возникла проблема при загрузке вопроса.")

def check_answer(update, context):
    user_answer = update.message.text.strip()
    correct_answer = next((qd["answer"] for qd in questions if qd["question"] == context.user_data['current_question']), None)
    if user_answer.lower() == correct_answer.lower():
        update.message.reply_text("Правильно!")
    else:
        update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ask", ask_question))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
