import os
import telegram.ext as tg

BOT_TOKEN = os.environ.get('BOT_TOKEN')

UPDATER = tg.Updater(token=BOT_TOKEN, use_context=True)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Этот мир не дорос до крутых вещей!")
