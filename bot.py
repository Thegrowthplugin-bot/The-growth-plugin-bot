import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
print(f"Token loaded: {bool(TOKEN)}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is LIVE ✅ Send /welcome to test")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome command works! ✅")

def run_bot():
    print("Starting Telegram bot polling...")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("welcome", welcome))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port)
