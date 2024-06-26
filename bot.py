import telebot
import os

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот на Heroku.")

@bot.message_handler(commands=['quiz'])
def quiz(message):
    bot.send_message(message.chat.id, "Это тестовый вопрос.")

bot.polling()
