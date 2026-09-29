import telebot
import re

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

# Welcome message
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🔥 Welcome to The Growth Plugin! 🔌\n\n"
        "Send me ANY link and I'll save it for review:\n"
        "✅ TikTok\n"
        "✅ Instagram Reels / Posts\n"
        "✅ YouTube\n"
        "✅ Facebook\n\n"
        "Just paste the link here 👇"
    )

# Accept ALL links
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text
    
    # Check if it contains a link
    if "http" not in text and "tiktok.com" not in text and "instagram.com" not in text and "youtu" not in text and "facebook.com" not in text and "fb.watch" not in text:
        bot.reply_to(message, "Please send a valid link.\nExample:\nhttps://www.tiktok.com/@user/video/123\nor\nhttps://www.instagram.com/reel/...")
        return

    # Detect platform
    platform = "Unknown"
    if "tiktok.com" in text: platform = "TikTok"
    elif "instagram.com" in text: platform = "Instagram"
    elif "youtu" in text: platform = "YouTube"
    elif "facebook.com" in text or "fb.watch" in text: platform = "Facebook"

    # Save it (you will see it in logs)
    print(f"New Order: {platform} - {text} - From: @{message.from_user.username}")

    bot.reply_to(message, 
        f"✅ {platform} Link Received!\n\n"
        f"{text}\n\n"
        f"Saved for review. Our team will deliver your growth shortly.\n"
        f"Check our channel: @Thegrowthplug_in\n"
        f"Need help? Order here: https://thegrowthplugin.bumpa.shop/"
    )

bot.polling()
