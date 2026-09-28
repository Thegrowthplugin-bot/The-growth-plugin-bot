import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is LIVE! 🚀"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is LIVE! 🚀 Send /welcome")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to The Growth Plugin! What is your TikTok handle? (e.g. @ayukcreator)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"✓ View reply: /welcome__answer1\nYou sent: {text}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start web server for Render
    Thread(target=run_flask, daemon=True).start()
    
    # Start Telegram bot
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("welcome", welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot polling started...")
    application.run_polling()
