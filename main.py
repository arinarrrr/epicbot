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

## Таймер
RandomCooldown = {}

## Циклы гриба
def shroom_update_cycle():
    sleep(300)
    print("Шаг цикла!")
    
    CURSOR.execute ("SELECT * FROM users")
    
    fetch = CURSOR.fetchone()
    while fetch != None:
        userId = fetch[0]
        size = fetch[2]
        
        size += random.choice([0, 0, 0, 1, 1, 2, 3])
        
        CURSOR.execute (f"UPDATE users SET balance = {size} WHERE userid = {userId}")
        DATABASE.commit()
        
        fetch = CURSOR.fetchone()
    
    for timer in RandomCooldown:
        RandomCooldown[timer] -= 5
        
        if RandomCooldown[timer] <= 0:
            del RandomCooldown[timer]
    
## Крутые функции
def cmd_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я чайный бот!")

def cmd_top(update, context):
    CURSOR.execute ("SELECT * FROM users")
    fetch = CURSOR.fetchone()
    
    users = []
    
    while fetch != None:
        userName = fetch[1]
        size = fetch[2]
        
        users.append([userName, size])
        
        fetch = CURSOR.fetchone()
    
    users = sorted(users, key = lambda x: x[1], reverse=True)
    
    message = "**Топ чайных грибов**"
    for entry in users:
        message += f"\n{entry[1]}мм у {entry[0]}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    

def cmd_random(update, context):
    userId = update.message.from_user.id;
    
    if userId in RandomCooldown:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Полегче-полегче! Следующий рандом вам будет доступен примерно через {RandomCooldown[userId]} минут")
        
    else:
        CURSOR.execute ("SELECT balance FROM users WHERE userid="+str(userId))
        fetch = CURSOR.fetchone()

        if fetch == None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="У вас нет чайного гриба!")

        else:
            size = fetch[0]
            deltaSize = int(random.randrange(-10, 12))
            
            if size + deltaSize < 1:
                size = 1
                deltaSize = 0
                specialMessage = True
            else:
                specialMessage = False

            CURSOR.execute (f"UPDATE users SET balance = {size+deltaSize} WHERE userid = {userId}")
            DATABASE.commit()

            RandomCooldown.update({userId: 45})
            
            if specialMessage:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Холи шит! Ваш чайный гриб уменьшился до минимального размера!")
            elif deltaSize > 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ого! Ваш чайный гриб увеличился на {deltaSize}мм!")
            elif deltaSize == 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Кринж! Ваш чайный гриб не изменился")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Жесть! Ваш чайный гриб уменьшился на {-deltaSize}мм!")
                       
def cmd_createshroom(update, context):
    userId = update.message.from_user.id;
    userName = update.message.from_user.first_name;
    
    CURSOR.execute ("SELECT * FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        CURSOR.execute ("INSERT INTO users (userid, name, balance) VALUES ("+str(userId)+", '"+userName+"', 1)")
        DATABASE.commit()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Чайный гриб создан")
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас уже есть чайный гриб, имейте совесть")
        print(fetch)

def cmd_checkshroom(update, context):
    userId = update.message.from_user.id;
    
    CURSOR.execute ("SELECT balance FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="У вас ещё нет чайного гриба")
    
    else:
        bmsg_balance = str(fetch[0])
        context.bot.send_message(chat_id=update.effective_chat.id, text="Размер чайного гриба: "+bmsg_balance+"мм")
    
## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler

top_handler = CommandHandler('top', cmd_top)
start_handler = CommandHandler('start', cmd_start)
createshroom_handler = CommandHandler('createshroom', cmd_createshroom)
checkshroom_handler = CommandHandler('checkshroom', cmd_checkshroom)
random_handler = CommandHandler('random', cmd_random)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(top_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(createshroom_handler)
dispatcher.add_handler(checkshroom_handler)
dispatcher.add_handler(random_handler)

# Запускаем автообновлялку
threading.Thread(target=shroom_update_cycle).start()

## Запускаем бота
updater.start_polling()
