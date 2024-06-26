import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Получаем токен бота из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update, context):
    update.message.reply_text('Привет! Я бот, который готов к работе.')

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    # Создаем экземпляр Updater и передаем токен бота
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков команд и сообщений
    dp = updater.dispatcher

    # Регистрируем обработчик для команды /start
    dp.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик для эхо-ответов на текстовые сообщения
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
