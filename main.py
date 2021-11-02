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

## Просто функции
def len_stylish(number):
    if number < 10:
        return str(number)+" мм"
    elif number < 100:
        return str(number/10)+" см"
    elif number < 1000:
        return str(number/100)+" дм"
    elif number < 1000000:
        return str(number/1000)+" м"
    else:
        return str(number/1000000)+" км"

def time_stylish(number):
    if number < 60:
        return str(number)+" мин"
    elif number % 60 == 0:
        return str(number / 60)+" ч"
    else:
        return str(int(number / 60))+" ч "+str(number % 60)+" мин"

## Циклы гриба
def shroom_update_cycle():
    while True:
        CURSOR.execute ("SELECT * FROM users")

        fetchall = CURSOR.fetchall()
        for fetch in fetchall:
            userId = fetch[0]
            size = fetch[2]

            size += random.choice([-2, -1, -1, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 5])
            if size < 1:
                size = 1

            CURSOR.execute (f"UPDATE users SET balance = {size} WHERE userid = {userId}")

        DATABASE.commit()
        
        RandomCooldownCopy = RandomCooldown.copy()

        for timer in RandomCooldownCopy:
            RandomCooldown[timer] -= 5

            if RandomCooldown[timer] <= 0:
                del RandomCooldown[timer]

        sleep(300)
    
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
    
    message = "<b>Топ чайных грибов</b>\n"
    for entry in users:
        message += f"\n{len_stylish(entry[1])} у <b>{entry[0]}</b>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="html")
    

def cmd_random(update, context):
    userId = update.message.from_user.id;
    
    if userId in RandomCooldown:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Полегче-полегче! Следующий рандом вам будет доступен примерно через {time_stylish(RandomCooldown[userId])}")
        
    else:
        CURSOR.execute ("SELECT balance FROM users WHERE userid="+str(userId))
        fetch = CURSOR.fetchone()

        if fetch == None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="У вас нет чайного гриба!")

        else:
            size = fetch[0]
            deltaSize = int(random.randrange(-24, 45))
            
            if size + deltaSize < 1:
                size = 1
                deltaSize = 0
                specialMessage = True
            else:
                specialMessage = False

            CURSOR.execute (f"UPDATE users SET balance = {size+deltaSize} WHERE userid = {userId}")
            DATABASE.commit()

            RandomCooldown.update({userId: 240})
            
            if specialMessage:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Холи шит! Ваш чайный гриб уменьшился до минимального размера!")
            elif deltaSize > 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ого! Ваш чайный гриб увеличился на {len_stylish(deltaSize)}!")
            elif deltaSize == 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Кринж! Ваш чайный гриб не изменился")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Жесть! Ваш чайный гриб уменьшился на {len_stylish(-deltaSize)}!")
                       
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
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Размер чайного гриба: {len_stylish(bmsg_balance)}")
    
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
