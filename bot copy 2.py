import os
import random
import json
import requests
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Получаем токен бота и ссылку на репозиторий из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
QUESTIONS_URL = "https://s7018025085.github.io/TelegramBotTest2024/test.json"  # Замените на ваш URL с JSON-файлом

def fetch_questions(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            questions = json.loads(response.text)
            return questions
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def start(update, context):
    update.message.reply_text('Привет! Я бот, который готов к работе.')

def ask_question(update, context):
    questions = fetch_questions(QUESTIONS_URL)
    if questions:
        random_question = random.choice(questions)
        context.user_data['current_question'] = random_question
        question_text = random_question['vopros']
        answers = [random_question.get(f'o{i}', '') for i in range(1, 6) if random_question.get(f'o{i}', '')]

        # Формируем текст сообщения с вопросом и вариантами ответов
        message = f"{question_text}\n\n"
        for i, answer in enumerate(answers, start=1):
            message += f"{i}. {answer}\n"

        # Формируем кнопки с номерами ответов
        keyboard = [[KeyboardButton(str(i))] for i in range(1, len(answers) + 1)]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        update.message.reply_text(message, reply_markup=reply_markup)
    else:
        update.message.reply_text("Извините, возникла проблема при загрузке вопроса.")

def check_answer(update, context):
    user_answer = update.message.text.strip()
    current_question = context.user_data.get('current_question')

    if current_question:
        correct_answer = current_question["prav"].strip(":").strip()
        answer_index = int(user_answer) - 1 if user_answer.isdigit() else -1
        
        if 0 <= answer_index < len(current_question):
            selected_answer = current_question.get(f'o{answer_index + 1}', '').strip()
            
            if selected_answer == correct_answer:
                update.message.reply_text("Правильно!")
            else:
                update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")
        else:
            update.message.reply_text("Выберите ответ из предложенных вариантов.")
    else:
        update.message.reply_text("Чтобы проверить ответ, сначала задайте вопрос командой /ask.")

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
