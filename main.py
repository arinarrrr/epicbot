import os
import telegram
import telegram.ext
import psycopg2
import threading
import random
from time import sleep

## Токен
BOT_TOKEN = os.environ.get('BOT_TOKEN')

## Всякая фигня
updater = telegram.ext.Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

## Подключение к БД
DATABASE = psycopg2.connect(dbname='dc9mv72g5rq199', user='expfuoggsoeeqp', password='8be9b873d53b0b38ba8fb3b7a0274db21e934813af12ecf4ed0bdee244422707', host='ec2-54-220-170-192.eu-west-1.compute.amazonaws.com')
CURSOR = DATABASE.cursor()

# Создать чайный гриб            
def cmd_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я культурный бот!")
    
## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler

start_handler = CommandHandler('nuclear', cmd_nuclear)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)

## Запускаем бота
updater.start_polling()
