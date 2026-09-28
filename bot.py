import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"Token loaded: {BOT_TOKEN is not None}")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is Alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting Flask on port {port}")
    app_flask.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"/start from {update.effective_user.id}")
    await update.message.reply_text("🌱 The Growth Plugin Bot is LIVE!\n\nSend me a channel @username to check\nUse /welcome to setup welcome message")

async def welcome_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome setup! What is your welcome message?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"Message: {text}")
    if "@" in text:
        await update.message.reply_text(f"✅ Got it: {text}\n\nChecking channel...")
    else:
        await update.message.reply_text(f"You said: {text}\nSend @channel to check")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Starting Telegram bot polling...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("welcome", welcome_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)
