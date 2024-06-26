import os
import random
import re
import requests
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Получаем токен бота и ссылку на репозиторий из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
QUESTIONS_URL = "https://s7018025085.github.io/TelegramBotTest2024/"  # Замените на ваш URL с вопросами

def fetch_questions(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            questions = []

            # Паттерн для поиска вопросов и ответов
            pattern = r'<div class="question">(.*?)</div>.*?<div class="answer">(.*?)</div>'
            matches = re.findall(pattern, html_content, re.DOTALL)

            for match in matches:
                question_text = match[0].strip()
                answers = [answer.strip() for answer in match[1].split("<div class=\"answer\">") if answer.strip()]
                correct_answer = None

                # Находим правильный ответ
                for answer in answers:
                    if "<div class=\"prav\">" in answer:
                        correct_answer = re.sub(r"<.*?>", "", answer).strip()

                questions.append({
                    "question": question_text,
                    "answers": answers,
                    "correct_answer": correct_answer
                })

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
        question_text = random_question['question']
        answers = random_question['answers']

        # Формируем клавиатуру с вариантами ответов
        keyboard = []
        for i, answer in enumerate(answers, start=1):
            keyboard.append([KeyboardButton(f"{i}. {answer}")])

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        update.message.reply_text(question_text, reply_markup=reply_markup)
    else:
        update.message.reply_text("Извините, возникла проблема при загрузке вопроса.")


def check_answer(update, context):
    user_answer = update.message.text.strip().lower()
    current_question = context.user_data.get('current_question')
    
    if current_question:
        correct_answer = current_question["correct_answer"].lower()
        
        # Проверяем ответ пользователя
        for i, answer in enumerate(current_question['answers'], start=1):
            if user_answer == f"{i}. {answer}".lower():
                if user_answer == f"{i}. {correct_answer}":
                    update.message.reply_text("Правильно!")
                else:
                    update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")
                return
        
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
