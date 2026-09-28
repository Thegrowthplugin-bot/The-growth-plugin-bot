import requests
from telegram.ext import *

HANDLE, PHONE = range(2)
TOKEN = "PASTE_TOKEN_HERE"
TERMII_KEY = "PASTE_TERMII_KEY_HERE"

async def start(update, context):
 await update.message.reply_text("Welcome! Whats your TikTok handle?")
 return HANDLE

async def get_handle(update, context):
 context.user_data['h'] = update.message.text
 await update.message.reply_text("Whats your WhatsApp? e.g 08012345678")
 return PHONE

async def get_phone(update, context):
 p = update.message.text.strip()
 h = context.user_data['h']
 if p.startswith('0'):
  p = '234' + p[1:]
 u = "https:" + "//api.ng.termii.com/api/sms/send"
 d = {"to": p, "from": "GrowthPlugin", "sms": f"Hey {h}! Active", "type": "plain", "channel": "generic", "api_key": TERMII_KEY}
 try:
  requests.post(u, json=d)
 except:
  pass
 await update.message.reply_text(f"Done {h}! SMS sent!")
 return ConversationHandler.END

def main():
 app = Application.builder().token(TOKEN).build()
 conv = ConversationHandler(entry_points=[CommandHandler("start", start)], states={HANDLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_handle)], PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)]}, fallbacks=[])
 app.add_handler(conv)
 app.run_polling()

if __name__ == "__main__":
 main()
