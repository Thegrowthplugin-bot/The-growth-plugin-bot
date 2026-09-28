import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Get token from Render Environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# --- Your bot commands here ---
async def start(update, context):
    await update.message.reply_text("Hello! Bot is Live! 🚀 Use /help")

async def help_command(update, context):
    await update.message.reply_text("I am The Growth Plugin Bot! Send me a message.")

async def echo(update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

# --- Flask for Render port ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Run bot ---
def main():
    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Build bot application (NEW way - no Updater)
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Bot starting... Flask running too!")
    application.run_polling()

if __name__ == '__main__':
    main()
