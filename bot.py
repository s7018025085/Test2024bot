import os
import random
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Получаем токен бота и ссылку на репозиторий из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
QUESTIONS_URL = "https://s7018025085.github.io/TelegramBotTest2024/"  # Замените на ваш URL с вопросами

def fetch_questions(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            questions = []

            # Находим все элементы с классом 'question'
            question_divs = soup.find_all('div', class_='question')

            for question_div in question_divs:
                question_text = question_div.text.strip()
                answers = []

                # Находим следующие элементы с классом 'answer'
                answer_divs = question_div.find_next_siblings('div', class_='answer')
                for answer_div in answer_divs:
                    answer_text = answer_div.text.strip()
                    answers.append(answer_text)

                # Находим правильный ответ с классом 'prav'
                correct_answer_div = question_div.find_next_sibling('div', class_='prav')
                if correct_answer_div:
                    correct_answer = correct_answer_div.text.replace("Правильный ответ: :", "").strip()
                else:
                    correct_answer = None

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
        context.user_data['current_question'] = random_question['question']
        update.message.reply_text(random_question['question'])
    else:
        update.message.reply_text("Извините, возникла проблема при загрузке вопроса.")

def check_answer(update, context):
    user_answer = update.message.text.strip().lower()
    current_question = context.user_data.get('current_question')
    
    if current_question:
        correct_answer = next((qd["correct_answer"].lower() for qd in context.user_data['questions'] if qd["question"].lower() == current_question.lower()), None)
        if correct_answer:
            if user_answer == correct_answer:
                update.message.reply_text("Правильно!")
            else:
                update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")
        else:
            update.message.reply_text("Не удалось найти правильный ответ на текущий вопрос.")
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
