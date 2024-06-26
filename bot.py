import telebot
import requests
import os
from flask import Flask, request, abort

API_TOKEN="7303306074:AAEMtjoNCucLezlv_f__79iMSlRqn7lP3JQ"
WEBHOOK_URL = "https://Test2024bot.up.railway.app/webhook" # URL вебхука с Railway


QUESTIONS_URL = 'https://raw.githubusercontent.com/USERNAME/REPO/main/questions.json'  # Замените на ваш URL

bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    else:
        abort(403)

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

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

