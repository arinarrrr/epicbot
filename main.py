import os
import telegram
import telegram.ext 

#3 Токен
BOT_TOKEN = os.environ.get('BOT_TOKEN')

## Всякая фигня
updater = telegram.ext.Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

## Крутые функции
def cmd_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы не готовы к крутости такого уровня...")

def cmd_openmc(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы открыли мифический сундук")

## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler

start_handler = CommandHandler('start', cmd_start)
openmc_handler = CommandHandler('openmc', cmd_openmc)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)
dispatcher.add_handler(openmc_handler)

## Запускаем бота
updater.start_polling()
