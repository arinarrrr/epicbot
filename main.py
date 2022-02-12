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
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я культурный бот! Чем я могу тебе помочь?")

def msg_analysis(update, context):
    if(update.effective_message.text == "Привет"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Привет!")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Мы можем предложить тебе пару развлечений на вечер. Как тебе идея виртуальной прогулки по Эрмитажу? Ответь да/нет")
        
    elif(update.effective_message.text == "Нет"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Хорошо, что на счет лекции про основные философские вопросы на Арзамас?")
         if(update.effective_message.text == "Да"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Отлично, вот ссылка: ---")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Мы можем предложить тебе пару развлечений на вечер. Как тебе идея виртуальной прогулки по Эрмитажу? Ответь да/нет")
        
        
    
## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

start_handler = CommandHandler('start', cmd_start)
msg_handler = MessageHandler(filters.Filters.all, msg_analysis)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)
dispatcher.add_handler(msg_handler)

## Запускаем бота
updater.start_polling()
