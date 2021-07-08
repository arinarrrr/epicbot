import os
import telegram
import telegram.ext 
import logging

# Логи
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Токен
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Всякая фигня
updater = telegram.ext.Updater(token=BOT_TOKEN, use_context=True)
dispatcher = UPDATER.dispatcher

# Устанавливаем какие-то держатели
from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)

# Крутая функция
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Этот мир не дорос до крутых вещей!")

# Запускаем бота
updater.start_polling()
