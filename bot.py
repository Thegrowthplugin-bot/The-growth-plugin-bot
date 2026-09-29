import os
import telebot
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 Welcome to The Growth Plugin! 🔌\n\nSend me ANY link and I'll save it for review:\n✅ TikTok\n✅ Instagram Reels / Posts\n✅ YouTube\n✅ Facebook\n\nJust paste the link here 👇")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text
    if "http" not in text:
        bot.reply_to(message, "Please send a valid link.")
        return
    platform = "Link"
    if "tiktok.com" in text: platform = "TikTok"
    elif "instagram.com" in text: platform = "Instagram"
    elif "youtu" in text: platform = "YouTube"
    elif "facebook.com" in text or "fb.watch" in text: platform = "Facebook"
    print(f"New Order: {platform} - {text}")
    bot.reply_to(message, f"✅ {platform} Link Received!\n\n{text}\n\nSaved for review. Check: @Thegrowthplug_in")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
