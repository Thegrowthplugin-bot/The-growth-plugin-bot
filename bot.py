import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
TERMII_KEY = os.getenv("TERMII_KEY")

if not TOKEN:
    raise ValueError("TOKEN not set")
if not TERMII_KEY:
    raise ValueError("TERMII_KEY not set")

logging.basicConfig(level=logging.INFO)

# Simple memory for codes
user_codes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to The Growth Plugin Bot!\nSend your phone number with country code, e.g. +2348012345678")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    chat_id = update.effective_chat.id
    
    # If user is sending OTP to verify
    if chat_id in user_codes:
        saved = user_codes[chat_id]
        if phone == saved["code"]:
            await update.message.reply_text("✅ Verified! Welcome!")
            del user_codes[chat_id]
        else:
            await update.message.reply_text("❌ Wrong code. Try again.")
        return

    # Send OTP via Termii
    import random
    code = str(random.randint(100000, 999999))
    user_codes[chat_id] = {"code": code, "phone": phone}

    url = "https://api.ng.termii.com/api/sms/otp/send"
    data = {
        "api_key": TERMII_KEY,
        "message_type": "NUMERIC",
        "to": phone,
        "from": "GrowthPlug",
        "channel": "generic",
        "pin_attempts": 3,
        "pin_time_to_live": 5,
        "pin_length": 6,
        "pin_placeholder": f"< {code} >",
        "message_text": f"Your Growth Plugin verification code is < {code} >. Valid for 5 mins.",
        "pin_type": "NUMERIC"
    }
    
    try:
        r = requests.post(url, json=data)
        if r.status_code == 200:
            await update.message.reply_text(f"Code sent to {phone}. Please enter the 6-digit code.")
        else:
            await update.message.reply_text(f"Failed to send SMS: {r.text}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    print("Bot starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
