import os
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Bot is LIVE! 🚀")

async def help_cmd(update, context):
    await update.message.reply_text("Use /start")

async def echo(update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Bot polling started...")
    application.run_polling()

if __name__ == '__main__':
    main()
