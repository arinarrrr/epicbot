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

## Таймер и прочее
RandomCooldown = {}
LastVisit = {}

## Просто функции
def len_stylish(number):
    if number < 10:
        return str(number)+"мм"
    elif number < 100:
        return str(number/10)+"см"
    elif number < 1000:
        return str(number/100)+"дм"
    elif number < 1000000:
        return str(number/1000)+"м"
    else:
        return str(number/1000000)+"км"

def time_stylish(number):
    if number < 60:
        return str(number)+"мин"
    elif number % 60 == 0:
        return str(int(number / 60))+"ч"
    else:
        return str(int(number / 60))+" ч "+str(number % 60)+" мин"

## Циклы гриба
def shroom_update_cycle(): # Цикл обновления игры
    while True:
        CURSOR.execute ("SELECT userid, balance, growlvl, lucklvl FROM users")

        fetchall = CURSOR.fetchall()
        
        average = 0
        for fetch in fetchall:
            average += fetch[1]
        average = int(average/len(fetchall))
        
        for fetch in fetchall:
            userId = fetch[0]
            size = fetch[1]
            
            growLvl = fetch[2]
            luckLvl = fetch[3]
            
            # Изменение размера
            if size > (average*3):
                luckarr = [-10, -8, -7, -3, -2, -2, -1, -1, 0, 1, 1, 2, 2, 3]
            elif size > (average*2):
                luckarr = [-6, -3, -2, -2, -1, -1, 0, 0, 0, 1, 1, 1, 2]
            elif size > (average*1.5):
                luckarr = [-5, -2, -2, -1, -1, 0, 0, 0, 1, 1, 1, 2, 2]
            elif size > (average*1.25):
                luckarr = [-3, -2, -2, -1, -1, 0, 0, 1, 1, 1, 2, 2, 2, 2]
            elif size > (average*0.75):
                luckarr = [-2, -1, -1, -1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 5]
            elif size > (average*0.5):
                luckarr = [-1, -1, 0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 5, 5]
            elif size > (average*0.2):
                luckarr = [0, 1, 1, 1, 2, 2, 3, 3, 4, 5, 8, 10]
            else:
                luckarr = [2, 2, 3, 3, 3, 4, 4, 5, 5, 7, 8, 10, 12]
            
            for i in range(luckLvl):
                if i % 16 == 0:
                    luckarr.append(3)
                elif i % 8 == 0:
                    luckarr.append(2)
                elif i % 2 == 0:
                    luckarr.append(1)
            
            for i in range(len(luckarr)):
                if luckarr[i] > 0:
                    luckarr[i] *= int((1.2*growLvl)*(1.1*luckLvl))
                elif luckarr[i] < 0:
                    luckarr[i] *= int((1.4*growLvl)*(0.9*luckLvl))
            
            size += random.choice(luckarr)
            
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
# Команда, выводящая какую-то фразу
def cmd_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я чайный бот!")


# Команда, выводящая топ чайных грибов
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
    

# Чай гриб рандом
def cmd_random(update, context):
    userId = update.message.from_user.id;
    
    if userId in RandomCooldown:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Полегче-полегче! Следующий рандом вам будет доступен примерно через {time_stylish(RandomCooldown[userId])}")
        
    else:
        CURSOR.execute ("SELECT (balance, randlvl, luckLvl) FROM users WHERE userid="+str(userId))
        fetch = CURSOR.fetchone()

        if fetch == None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="У вас нет чайного гриба!")

        else:
            randLvl = fetch[1]
            luckLvl = fetch[2]
            
            size = fetch[0]
            deltaSize = int(random.randrange(-50*(1.2**randLvl)*(0.9**luckLvl), 80*(1.1**randLvl)*(1.1**luckLvl)))
            
            if size + deltaSize < 1:
                size = 1
                deltaSize = 0
                specialMessage = True
            else:
                specialMessage = False

            CURSOR.execute (f"UPDATE users SET balance = {size+deltaSize} WHERE userid = {userId}")
            DATABASE.commit()

            RandomCooldown.update({userId: 240*(0.95**randLvl)})
            
            if specialMessage:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Холи шит! Ваш чайный гриб уменьшился до минимального размера!")
            elif deltaSize > 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ого! Ваш чайный гриб увеличился на {len_stylish(deltaSize)}!")
            elif deltaSize == 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Кринж! Ваш чайный гриб не изменился")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Жесть! Ваш чайный гриб уменьшился на {len_stylish(-deltaSize)}!")

                
# Создать чайный гриб            
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


# Проверить размер чайного гриба
def cmd_checkshroom(update, context): 
    userId = update.message.from_user.id;
    
    CURSOR.execute ("SELECT balance FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="У вас ещё нет чайного гриба")
    
    else:
        size = fetch[0]
        
        if userId in LastVisit:
            if size > LastVisit[userId]:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Размер чайного гриба: {len_stylish(size)}\nС момента последнего посещения ваш гриб вырос на {len_stylish(size - LastVisit[userId])}")
            elif size == LastVisit[userId]:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Размер чайного гриба: {len_stylish(size)}\nС момента последнего посещения ваш гриб не изменился")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Размер чайного гриба: {len_stylish(size)}\nС момента последнего посещения ваш гриб уменбшился на {len_stylish(LastVisit[userId] - size)}")
            
            LastVisit[userId] = size
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Размер чайного гриба: {len_stylish(size)}")
            LastVisit.update({userId: size})


# Улучшения
def cmd_upgrade(update, context):
    userId = update.message.from_user.id;
    
    CURSOR.execute ("SELECT balance, randlvl, growlvl, lucklvl FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="У вас ещё нет чайного гриба, вам нечего улучшать")
    
    else:
        size = fetch[0]
        randLvl = fetch[1]
        growLvl = fetch[2]
        luckLvl = fetch[3]
        
        if len(context.args) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"/upgrade luck - улучшить уровень удачи\nВаш уровень удачи: {luckLvl}\nЦена улучшения: {len_stylish(int(100*(1.3**luckLvl)))}")
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"/upgrade grow - улучшить гриб\nВаш уровень гриба: {growLvl}\nЦена улучшения: {len_stylish(int(100*(1.15**growLvl)))}")
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"/upgrade rand - улучшить чайгрибрандом\nВаш уровень чайгрибрандома: {randLvl}\nЦена улучшения: {len_stylish(int(100*(1.5**randLvl)))}")
        else:
            if context.args[0] == "luck": # Игрок улучшает удачу
                if size >= int(100*(1.3**luckLvl))+1:
                    size -= int(100*(1.3**luckLvl))
                    luckLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваша удача была улучшена до уровня {luckLvl}")
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Гриб слишком мал")
            if context.args[0] == "grow": # Игрок улучшает скорость роста гриба
                if size >= int(100*(1.15**growLvl))+1:
                    size -= int(100*(1.15**growLvl))
                    growLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваш гриб был улучшен до уровня {growLvl}")
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Гриб слишком мал")
            if context.args[0] == "rand": # Игрок улучшает скорость роста гриба
                if size >= int(100*(1.5**randLvl))+1:
                    size -= int(100*(1.5**randLvl))
                    growLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваш чайгрибрандом был улучшен до уровня {randLvl}")
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Гриб слишком мал")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Вы чё улучшать собрались? Нифига не понятно")
        
            CURSOR.execute (f"UPDATE users SET balance = {size}, lucklvl = {luckLvl}, growlvl = {growLvl}, randLvl = {randLvl} WHERE userid = {userId}")
            DATABASE.commit()
                
    
## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler

top_handler = CommandHandler('top', cmd_top)
start_handler = CommandHandler('start', cmd_start)
createshroom_handler = CommandHandler('createshroom', cmd_createshroom)
checkshroom_handler = CommandHandler('checkshroom', cmd_checkshroom)
random_handler = CommandHandler('random', cmd_random)
upgrade_handler = CommandHandler('random', cmd_upgrade)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(top_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(createshroom_handler)
dispatcher.add_handler(checkshroom_handler)
dispatcher.add_handler(random_handler)
dispatcher.add_handler(upgrade_handler)

# Запускаем автообновлялку
threading.Thread(target=shroom_update_cycle).start()

## Запускаем бота
updater.start_polling()
