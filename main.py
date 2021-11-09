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

## Бустеры
BRand = {}
BYest = {}
BGrow = {}

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
        return str(int(number / 60))+" ч "+str(int(number % 60))+" мин"

## Циклы гриба
def shroom_update_cycle(): # Цикл обновления игры
    while True:
        CURSOR.execute ("SELECT userid, balance, growlvl, lucklvl, yeastlvl, yeasts FROM users")

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
            yeastLvl = fetch[4]
            
            yeasts = fetch[5]
            
            # Изменение размера
            luckarr = [-2, -1, -1, -1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2]
            
            for i in range(luckLvl):
                if i % 12 == 0:
                    luckarr.append(3)
                    luckarr.append(-1)
                elif i % 6 == 0:
                    luckarr.append(2)
                    luckarr.append(0)
                elif i % 3 == 0:
                    luckarr.append(1)
            
            if userId in BGrow:
                growBoosterBonus = 4
            else:
                growBoosterBonus = 1
            
            for i in range(len(luckarr)):
                if luckarr[i] > 0:
                    luckarr[i] *= int((1.2**growLvl))*growBoosterBonus
                elif luckarr[i] < 0:
                    luckarr[i] *= int((1.3**growLvl)*(0.9**luckLvl))
            
            addValue = random.choice(luckarr)
            size += addValue
            
            # Рост дрожжей
            if userId in BYest:
                yeasts += (1 + int(1.5**yeastLvl))*3
            else:
                yeasts += 1 + int(1.5**yeastLvl)

            # Не даём грибу уйти в минус
            if size < 1:
                size = 1

            CURSOR.execute (f"UPDATE users SET balance = {size}, yeasts = {yeasts} WHERE userid = {userId}")

        DATABASE.commit()
        
        RandomCooldownCopy = RandomCooldown.copy()
        for timer in RandomCooldownCopy:
            RandomCooldown[timer] -= 5
            if RandomCooldown[timer] <= 0:
                del RandomCooldown[timer]
        
        BYestCopy = BYest.copy()
        for booster in BYestCopy:
            BYest[booster] -= 5
            if BYest[booster] <= 0:
                del BYest[booster]
        
        BGrowCopy = BGrow.copy()
        for booster in BGrowCopy:
            BGrow[booster] -= 5
            if BGrow[booster] <= 0:
                del BGrow[booster]

        sleep(300)
    
## Крутые функции
# Команда, выводящая какую-то фразу
def cmd_shop(update, context):
    userId = update.message.from_user.id;
    
    CURSOR.execute ("SELECT algae FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет чайного гриба, мы Вам ничего продавать не собираемся")
    
    else:
        algae = fetch[0]
        
        value = int((1.4**(randLvl+growLvl+luckLvl+yeastLvl+randSpeedLvl))*100)
        
        if len(context.args) == 0:
            bRandPrice = 2
            bYestPrice = 3
            bGrowPrice = 2
            sizeupPrice = 10
            bombPrice = 7
            
            message = f"(Нажмите на команду, чтобы скопировать)" + "\n\n"
            message += f"`/shop brand` - купить бустер рандома за {bRandPrice} водорослей" + "\n\n" + "Увеличивает награду на следующие два рандома" + "\n\n"
            message += f"`/shop byest` - купить бустер дрожжей за {bYestPrice} водорослей" + "\n\n" + "Увеличивает добычу дрожжей на два часа в три раза" + "\n\n"
            message += f"`/shop bgrow` - купить бустер роста за {bGrowPrice} водорослей" + "\n\n" + "Увеличивает рост размера гриба на три часа" + "\n\n"
            message += f"`/shop sizeup` - увеличить гриб в полтора раза за {bSizeupPrice} водорослей" + "\n\n"
            message += f"`/shop bomb` - купить бомбу за {bombPrice} водорослей" + "\n\n" + "Подрывает гриб нескольким участникам (может и Вас задеть)" + "\n\n"
            
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown")
        else:
            heckmessage = "Вам не хватает водорослей! Проваливайте, нищук."
            if context.args[0] == "brand":
                if algae >= bRandPrice:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы приобрели бустер рандома")
                    algae -= bRandPrice
                    if userId in BRand:
                        BRand.userId += 2
                    else:
                        BRand.update({userId: 2})
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=heckmessage, parse_mode="Markdown")
            elif context.args[0] == "byest":
                if algae >= bYestPrice:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы приобрели бустер дрожжей")
                    algae -= bYestPrice
                    if userId in BYest:
                        BYest.userId += 120
                    else:
                        BYest.update({userId: 120})
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=heckmessage, parse_mode="Markdown")
            elif context.args[0] == "bgrow":
                if algae >= bGrowPrice:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы приобрели бустер роста")
                    algae -= bGrowPrice
                    if userId in BGrow:
                        BGrow.userId += 180
                    else:
                        BGrow.update({userId: 180})
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=heckmessage, parse_mode="Markdown")
            elif context.args[0] == "sizeup":
                if algae >= sizeupPrice:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы увеличили гриб")
                    algae -= sizeupPrice
                    
                    CURSOR.execute ("SELECT balance FROM users WHERE userid="+str(userId))
                    fetch = CURSOR.fetchone()
                    
                    CURSOR.execute (f"UPDATE users SET balance={fetch[0]*1.5} WHERE userid="+str(userId))
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=heckmessage, parse_mode="Markdown")
            elif context.args[0] == "bomb":
                if algae >= bombPrice:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас не бомбит")
                    algae -= bombPrice
                    
                    CURSOR.execute ("SELECT userid FROM users")
                    fetchall = CURSOR.fetchall()
                    
                    random.shuffle(fetchall)
                    
                    for i in range(3):
                        victimId = fetchall[i][0]
                        
                        CURSOR.execute ("SELECT balance FROM users WHERE userid="+str(victimId))
                        fetch = CURSOR.fetchone()
                        CURSOR.execute (f"UPDATE users SET balance={fetch[0]*0.75} WHERE userid="+str(victimId))
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=heckmessage, parse_mode="Markdown")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Мы такое не продаём")

# Ядерный гриб
def cmd_nuclear(update, context):
    userId = update.message.from_user.id
    CURSOR.execute(f"SELECT balance FROM users WHERE userid = {userId}")

    fetch = CURSOR.fetchone()
    
    balance = fetch[0]

    if(balance < 1000000):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Слишком рано...")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Вы уничтожили мир!")
        
        CURSOR.execute ("SELECT userid, growlvl, lucklvl, randlvl, yeastlvl, randspeedlvl, yeasts, algae FROM users")
        
        fetchall = CURSOR.fetchall()
        
        for fetch in fetchall:
            userid = fetch[0]
            growLvl = fetch[1]
            luckLvl = fetch[2]
            randLvl = fetch[3]
            yeastLvl = fetch[4]
            randSpeedLvl = fetch[5]
            yeasts = fetch[6]
            algae = fetch[7]
            
            algae += 3*(growLvl+luckLvl+randLvl+yeastLvl+randSpeedLvl) + int(yeasts/1000)
            
            CURSOR.execute (f"UPDATE users SET growlvl=0, lucklvl=0, randlvl=0, yeastlvl=0, randspeedlvl=0, yeasts=0, algae={algae} WHERE userid={userid}")

            

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
        CURSOR.execute ("SELECT balance, randlvl, randspeedlvl, luckLvl, algae FROM users WHERE userid="+str(userId))
        fetch = CURSOR.fetchone()

        if fetch == None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="У вас нет чайного гриба!")

        else:
            randLvl = fetch[1]
            randSpeedLvl = fetch[2]
            luckLvl = fetch[3]

            algae = fetch[4]
            
            size = fetch[0]
            
            if(userId in BRand):
                deltaSize = int(random.randrange(int(-50*(1.1**randLvl)*(0.8**luckLvl)), int(250*(1.1**randLvl))))
                
                BRand[userId] -= 1
                if BRand[userId] == 0:
                    del BRand[userId]
            else:
                deltaSize = int(random.randrange(int(-50*(1.1**randLvl)*(0.8**luckLvl)), int(80*(1.1**randLvl))))
            
            if size + deltaSize < 1:
                size = 1
                deltaSize = 0
                specialMessage = True
            else:
                specialMessage = False

            if (deltaSize > 0):
                algae += int(deltaSize/300)

            CURSOR.execute (f"UPDATE users SET balance = {size+deltaSize}, algae = {algae} WHERE userid = {userId}")
            DATABASE.commit()

            RandomCooldown.update({userId: int(36*(0.8**randSpeedLvl))*5})
            
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
    
    CURSOR.execute ("SELECT balance, algae, yeasts FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="У вас ещё нет чайного гриба")
    
    else:
        size = fetch[0]
        algae = fetch[1]
        yeasts = fetch[2]
        
        balanceMessage = f"Размер чайного гриба: {len_stylish(size)}\nБаланс водорослей: {algae}\nБаланс дрожжей: {yeasts}"
        
        if userId in LastVisit:
            if size > LastVisit[userId]:
                balanceMessage += f"\n\nС момента последнего посещения ваш гриб вырос на {len_stylish(size - LastVisit[userId])}"
            elif size == LastVisit[userId]:
                balanceMessage += f"\n\nС момента последнего посещения ваш гриб не изменился"
            else:
                balanceMessage += f"\n\nС момента последнего посещения ваш гриб уменбшился на {len_stylish(LastVisit[userId] - size)}"
            
            LastVisit[userId] = size
        else:
            LastVisit.update({userId: size})
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=balanceMessage)


# Улучшения
def cmd_upgrade(update, context):
    userId = update.message.from_user.id;
    
    CURSOR.execute ("SELECT yeasts, randlvl, growlvl, lucklvl, yeastlvl, randspeedlvl FROM users WHERE userid="+str(userId))
    fetch = CURSOR.fetchone()
    
    if fetch == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="У вас ещё нет чайного гриба, вам нечего улучшать")
    
    else:
        yeasts = fetch[0]
        randLvl = fetch[1]
        growLvl = fetch[2]
        luckLvl = fetch[3]
        yeastLvl = fetch[4]
        randSpeedLvl = fetch[5]
        
        value = int((1.15**(randLvl+growLvl+luckLvl+yeastLvl+randSpeedLvl))*100)
        
        if len(context.args) == 0:
            message = f"Улучшение стоит {value} дрожжей" + "\n\n"
            message += f"(Нажмите на команду, чтобы скопировать)" + "\n\n"
            message += f"`/upgrade luck` - улучшить уровень удачи\nВаш уровень удачи: {luckLvl}" + "\n\n" + "Уменьшает шанс уменьшения гриба" + "\n\n"
            message += f"`/upgrade grow` - улучшить гриб\nВаш уровень гриба: {growLvl}" + "\n\n" + "Увеличивает пассивное изменение размера гриба" + "\n\n"
            message += f"`/upgrade rand` - улучшить рандом\n\nВаш уровень рандома: {randLvl}" + "\n\n" + "Увеличивает награду от рандома" + "\n\n"
            message += f"`/upgrade yest` - улучшить ферму дрожжей\n\nВаш уровень фермы: {yeastLvl}" + "\n\n" + "Увеличивает количество получаемых дрожжей" + "\n\n"
            message += f"`/upgrade rans` - улучшить скорость рандома\n\nВаш уровень скорости: {randSpeedLvl}" + "\n\n" + "Уменьшает паузу между рандомами" + "\n\n"
            
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown")
        else:
            if yeasts >= value:
                yeasts -= value
                
                if context.args[0] == "luck": # Игрок улучшает удачу
                    luckLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваша удача была улучшена до уровня {luckLvl}")
                elif context.args[0] == "grow": # Игрок улучшает скорость роста гриба
                    growLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваш гриб был улучшен до уровня {growLvl}")
                elif context.args[0] == "rand": # Игрок улучшает рандом
                    randLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваш чайгрибрандом был улучшен до уровня {randLvl}")
                elif context.args[0] == "yest": # Игрок улучшает дрожжи
                    yeastLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваша ферма дрожжей была улучшена до уровня {yeastLvl}")
                elif context.args[0] == "rans": # Игрок улучшает скорость рандома
                    randomSpeedLvl += 1
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваша скорость рандома была улучшена до уровня {randSpeedLvl}")
                else:
                    yeasts += int(0.75*value)
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы отправили нам непонятно что, Вы потратили время людей, мы забираем у Вас четверть цены улучшения")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Не хватает дрожжей")
        
            CURSOR.execute (f"UPDATE users SET yeasts = {yeasts}, lucklvl = {luckLvl}, growlvl = {growLvl}, randLvl = {randLvl}, yeastlvl = {yeastLvl}, randspeedlvl = {randSpeedLvl} WHERE userid = {userId}")
            DATABASE.commit()
                
    
## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler

nuclear_handler = CommandHandler('nuclear', cmd_nuclear)
top_handler = CommandHandler('top', cmd_top)
start_handler = CommandHandler('start', cmd_createshroom)
shop_handler = CommandHandler('shop', cmd_shop)
checkshroom_handler = CommandHandler('checkshroom', cmd_checkshroom)
random_handler = CommandHandler('random', cmd_random)
upgrade_handler = CommandHandler('upgrade', cmd_upgrade)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(nuclear_handler)
dispatcher.add_handler(top_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(shop_handler)
dispatcher.add_handler(checkshroom_handler)
dispatcher.add_handler(random_handler)
dispatcher.add_handler(upgrade_handler)

# Запускаем автообновлялку
threading.Thread(target=shroom_update_cycle).start()

## Запускаем бота
updater.start_polling()
