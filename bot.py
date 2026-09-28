import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"Token loaded: {BOT_TOKEN is not None}")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is Alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌱 The Growth Plugin Bot is LIVE!\n\nSend /welcome")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What is your welcome message?")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You sent: {update.message.text}")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Starting Telegram bot polling...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("welcome", welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()
