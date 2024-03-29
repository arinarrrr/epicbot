import os
import telegram
import telegram.ext
import psycopg2
import threading
import random
from time import sleep

## Токен
BOT_TOKEN = os.environ.get('BOT_TOKEN')

## Константы с номерами тем разговора
LEKCII_REPLY, DA_MEMY_REPLY, ARAMZAS_REPLY = range(3)

## Всякая фигня
updater = telegram.ext.Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

## Подключение к БД
DATABASE = psycopg2.connect(dbname='dc9mv72g5rq199', user='expfuoggsoeeqp', password='8be9b873d53b0b38ba8fb3b7a0274db21e934813af12ecf4ed0bdee244422707', host='ec2-54-220-170-192.eu-west-1.compute.amazonaws.com')
CURSOR = DATABASE.cursor()

# Создать чайный гриб
from telegram.ext import ConversationHandler

def cmd_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я культурный бот! Чем я могу тебе помочь? Чтобы начать напиши 'Привет'")

# Когда привет
def msg_greetings(update, context):
    if(update.effective_message.text == "Привет"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Привет!")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Мы можем предложить тебе пару развлечений на вечер. Что ты хочешь, на сегодня мы можем предложить тебе следующее: посмотреть лекцию, послушать подкасть или выбрать ближайщее мероприятие. Чтобы ответить на этот вопрос просто напиши действие!")
        context.bot.send_message(chat_id=update.effective_chat.id, text="У нашего бота есть несколько правил: Когда бот задает тебе вопрос отвечай 'да', либо 'нет' в зависимости от твоих желаний. Также, если ты передумал и не захотел ничего из предложенного, напиши вновь '/start'.")
    return LEKCII_REPLY

# Ответы на вопрос: посмотреть лекцию 
def msg_lekcii_reply(update, context):
    if(update.effective_message.text == "посмотреть лекцию"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Хочешь посмотреть лекцию про популярные философские мемы?")
                                 
    return DA_MEMY_REPLY
                                 
def  msg_memy_reply(update, context):
    if(update.effective_message.text == "да"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Супер, вот ссылка: https://arzamas.academy/materials/1771")
        return ConversationHandler.END
    elif(update.effective_message.text == "Нет"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Надеюсь, тебе нравится искусство ХIV - XV веков. Поэтому давай посмотрим лекцию про И. Босха: https://www.youtube.com/watch?v=YMRAdLVhiLE")
        return ARAMZAS_REPLY
    
# Ответы на вопрос о арамзамзам
def msg_aramzas_reply(update, context):
    if(update.effective_message.text == "Да"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Отлично, вот ссылка: https://arzamas.academy/materials/1771")
        return ConversationHandler.END
    elif(update.effective_message.text == "Нет"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ладно, тогда давай посмотрим эту: ")
        return ConversationHandler.END


## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

start_handler = CommandHandler('start', cmd_start)
conversation_handler = ConversationHandler(
    entry_points = [MessageHandler(filters.Filters.regex('^(Привет)$'), msg_greetings)],
# для возврата функций непонятно куда 
    states = {
        LEKCII_REPLY: [MessageHandler(filters.Filters.regex('^(посмотреть лекцию)$'), msg_lekcii_reply)],
        DA_MEMY_REPLY: [MessageHandler(filters.Filters.regex('^(да|Нет)$'), msg_memy_reply)], 
        ARAMZAS_REPLY: [MessageHandler(filters.Filters.regex('^(Да|Нет)$'), msg_aramzas_reply)]
    },

    fallbacks = []
)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)
dispatcher.add_handler(conversation_handler)

## Запускаем бота
updater.start_polling()
