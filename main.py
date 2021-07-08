import os
import telegram
import telegram.ext
import psycopg2

## Токен
BOT_TOKEN = os.environ.get('BOT_TOKEN')

## Всякая фигня
updater = telegram.ext.Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

## Подключение к БД
DATABASE = psycopg2.connect(dbname='dc9mv72g5rq199', user='expfuoggsoeeqp', password='8be9b873d53b0b38ba8fb3b7a0274db21e934813af12ecf4ed0bdee244422707', host='ec2-54-220-170-192.eu-west-1.compute.amazonaws.com')
CURSOR = DATABASE.cursor()

## Крутые функции
def cmd_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы не готовы к крутости такого уровня...")

def cmd_selldata(update, context):
    userId = update.message.from_user.id;
    userName = update.message.from_user.first_name;
    
    CURSOR.execute ("SELECT * FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        CURSOR.execute ("INSERT INTO users (userid, name, balance) VALUES ("+str(userId)+", '"+userName+"', 3)")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Вы продали свои данные за три фальшивых рубля")
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Вы уже продавали свои данные")
        print(fetch)

## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler

start_handler = CommandHandler('start', cmd_start)
selldata_handler = CommandHandler('selldata', cmd_selldata, pass_user_data=True)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)
dispatcher.add_handler(selldata_handler)

## Запускаем бота
updater.start_polling()
