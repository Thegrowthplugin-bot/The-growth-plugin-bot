import os
import logging
import requests
import threading
import random
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
TERMII_KEY = os.getenv("TERMII_KEY")

if not TOKEN:
    raise ValueError("TOKEN not set")
if not TERMII_KEY:
    raise ValueError("TERMII_KEY not set")

logging.basicConfig(level=logging.INFO)
user_codes = {}

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to The Growth Plugin! 👋\n\nPlease send your phone number with country code.\nExample: +2348012345678")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    chat_id = update.effective_chat.id

    # If user is trying to verify code
    if chat_id in user_codes:
        saved = user_codes[chat_id]
        if text == saved["code"]:
            await update.message.reply_text("✅ Verified! Welcome to The Growth Plugin. You now have access!")
            del user_codes[chat_id]
        else:
            await update.message.reply_text("❌ Wrong code. Try again.")
        return

    # Otherwise treat text as phone number
    phone = text
    if not phone.startswith("+"):
        await update.message.reply_text("Please include country code. Example: +2348012345678")
        return

    code = str(random.randint(100000, 999999))
    user_codes[chat_id] = {"code": code, "phone": phone}

    url = "https://api.ng.termii.com/api/sms/send"
    data = {
        "api_key": TERMII_KEY,
        "to": phone,
        "from": "GrowthPlug",
        "sms": f"Your Growth Plugin code is: {code}. Valid for 5 minutes.",
        "type": "plain",
        "channel": "generic"
    }

    try:
        r = requests.post(url, json=data)
        if r.status_code == 200:
            await update.message.reply_text(f"📱 Code sent to {phone}! Please enter the 6-digit code.")
        else:
            await update.message.reply_text(f"Failed to send SMS: {r.text}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    print("Bot Starting...")
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
