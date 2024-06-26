import telebot
from flask import Flask, request
import os

API_TOKEN="7303306074:AAEMtjoNCucLezlv_f__79iMSlRqn7lP3JQ"
WEBHOOK_URL = "https://Test2024bot.up.railway.app/webhook" # URL вебхука с Railway


bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start']) 
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в бот!")

@bot.message_handler(commands=['quiz'])
def send_question(message):
    # Ваша логика викторины здесь
    pass

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Неверный Content-Type'

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
