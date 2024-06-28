import os
import random
import json
import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Получаем токен бота и ссылку на репозиторий из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
QUESTIONS_URL = "https://s7018025085.github.io/TelegramBotTest2024/test.json"  # Замените на ваш URL с JSON-файлом

def fetch_questions(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                questions = json.loads(response.text)
                return questions
            except json.JSONDecodeError:
                print("Error parsing JSON.")
                return None
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def start(update, context):
    update.message.reply_text('Привет! Я бот, который готов к работе. Используйте команду /ask для получения вопроса.')

def ask_question(update, context):
    questions = fetch_questions(QUESTIONS_URL)
    if questions:
        random_question = random.choice(questions)
        context.user_data['current_question'] = random_question
        question_text = random_question['vopros']
        theme = random_question['Thems']
        question_number = random_question['id']
        answers = [(f"{i}.  {random_question.get(f'o{i}', '')}") for i in range(1, 6) if random_question.get(f'o{i}', '')]

        # Проверяем, есть ли ответы
        if not answers:
            update.message.reply_text("Извините, не удалось загрузить варианты ответов.")
            return
        
        # Формируем сообщение с темой, номером вопроса, вопросом и ответами 
        message = f"<b>Тема:</b> {theme} "
        message += f"<b>Вопрос {question_number}:</b>\n\n<b>{question_text}</b>\n\n"
        message += "\n".join(answers)

        # Формируем список кнопок с номерами ответов в одной строке
        keyboard = []
        for i in range(1, 6):
            if random_question.get(f'o{i}', ''):
                keyboard.append(InlineKeyboardButton(f"{i}", callback_data=str(i)))

        # Создаем разметку с кнопками
        reply_markup = InlineKeyboardMarkup([keyboard])

        # Отправляем сообщение с темой, вопросом, ответами и кнопками ответов
        update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
    else:
        update.message.reply_text("Извините, возникла проблема при загрузке вопроса.")

def check_answer(update, context):
    user_answer = update.callback_query.data
    current_question = context.user_data.get('current_question')

    if current_question:
        try:
            answer_index = int(user_answer) - 1
            answers = [current_question.get(f'o{i}', '') for i in range(1, 6) if current_question.get(f'o{i}', '')]
            selected_answer = answers[answer_index] if 0 <= answer_index < len(answers) else None
            correct_answer = current_question["prav"].strip(":").strip()

            if selected_answer == correct_answer:
                update.callback_query.message.reply_text("Правильно!")
            else:
                update.callback_query.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")
            
            # Сразу задаем следующий вопрос
            ask_question(update.callback_query, context)
        except (ValueError, IndexError):
            update.callback_query.message.reply_text("Выберите ответ из предложенных вариантов.")
    else:
        update.callback_query.message.reply_text("Чтобы проверить ответ, сначала задайте вопрос командой /ask.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ask", ask_question))
    dp.add_handler(CallbackQueryHandler(check_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
