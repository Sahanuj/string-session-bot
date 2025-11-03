# bot.py
import os
import urllib.parse
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

WEB_URL = os.getenv("WEB_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

print(f"[BOT] WEB_URL = {WEB_URL}")
print(f"[BOT] TOKEN = {BOT_TOKEN[:10]}...")

if not BOT_TOKEN or not WEB_URL:
    print("FATAL: Missing BOT_TOKEN or WEB_URL")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please share your phone number to login.", reply_markup=reply_markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("Invalid contact.")
        return

    phone = contact.phone_number
    user_id = update.effective_user.id
    url = f"{WEB_URL}?phone={urllib.parse.quote(phone)}&user_id={user_id}"

    button = InlineKeyboardMarkup([[InlineKeyboardButton("Open Login Page", url=url)]])
    await update.message.reply_text("Tap below to continue login:", reply_markup=button)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
