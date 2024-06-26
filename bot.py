import telebot
import requests
import random
import os

API_TOKEN ="7303306074:AAEMtjoNCucLezlv_f__79iMSlRqn7lP3JQ"  # Убедитесь, что токен настроен как переменная окружения
QUESTIONS_URL = 'https://raw.githubusercontent.com/USERNAME/REPO/main/questions.json'  # Замените на ваш URL

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Quiz Bot! Use /quiz to get a question.")

@bot.message_handler(commands=['quiz'])
def send_question(message):
    response = requests.get(QUESTIONS_URL)
    questions = response.json()
    question = random.choice(questions)
    options = '\n'.join([f"{i + 1}. {opt}" for i, opt in enumerate(question["options"])])
    msg = f"{question['question']}\n\n{options}"
    bot.send_message(message.chat.id, msg)

    bot.register_next_step_handler(message, lambda msg: check_answer(msg, question))

def check_answer(message, question):
    try:
        answer_index = int(message.text.strip()) - 1
        if question["options"][answer_index] == question["answer"]:
            bot.send_message(message.chat.id, "Correct!")
        else:
            bot.send_message(message.chat.id, "Wrong answer.")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Please enter a valid option number.")

bot.polling()
