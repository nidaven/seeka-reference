import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there! I'm Navia, How can I help you?")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help!")

async def search_sermon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.me
    await update.message.reply_text("Searching for sermon")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    
    application.run_polling()