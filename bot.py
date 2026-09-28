import os
import random
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Flask to keep Render happy (binds a port) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Telegram Bot Logic ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to The Growth Plugin! 🚀\n\n"
        "Your journey to better YouTube growth starts here.\n\n"
        "Send /help to see what I can do."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/verify - Get verification code"
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = random.randint(100000, 999999)
    await update.message.reply_text(f"Your verification code is: {code}")

def main():
    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Start Bot
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("verify", verify))
    
    print("Bot is polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
