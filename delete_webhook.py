# delete_webhook.py
import telebot
import os

API_TOKEN="7303306074:AAEMtjoNCucLezlv_f__79iMSlRqn7lP3JQ"
bot = telebot.TeleBot(API_TOKEN)

bot.remove_webhook()
print("Webhook removed.")