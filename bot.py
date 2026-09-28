import os
import telebot
from flask import Flask, request
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Store links (you can later connect to Google Sheet)
tiktok_links = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 Welcome to The Growth Plugin!\n\nSend me any TikTok link and I'll save it for review.\n\nJust paste the link here 👇")

@bot.message_handler(func=lambda m: 'tiktok.com' in m.text.lower())
def save_link(message):
    link = message.text
    tiktok_links.append({"user": message.from_user.username, "link": link})
    print(f"New link from @{message.from_user.username}: {link}")
    bot.reply_to(message, f"✅ Got it! Saved!\n\n{link}\n\nSend another one or type /start")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if 'tiktok.com' not in message.text.lower():
        bot.reply_to(message, "Please send a valid TikTok link. Example:\nhttps://www.tiktok.com/@user/video/123456")

# Flask routes for Render
@app.route('/')
def home():
    return "The Growth Plugin Bot is LIVE!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200

def run_bot():
    # IMPORTANT: Remove webhook and use polling (works best on Render free tier)
    bot.remove_webhook()
    print("Bot removed webhook, starting polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Start bot in background thread
    threading.Thread(target=run_bot, daemon=True).start()
    # Start Flask for Render to keep it Live
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
