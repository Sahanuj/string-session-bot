# bot.py
import os
import urllib.parse
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === RAILWAY ENV VARS ===
WEB_URL = os.getenv("WEB_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("FATAL: BOT_TOKEN missing")
    exit(1)
if not WEB_URL:
    print("FATAL: WEB_URL missing")
    exit(1)

print(f"[BOT] WEB_URL = {WEB_URL}")
print(f"[BOT] TOKEN = {BOT_TOKEN[:15]}...")

# === /start → SHOW KEYBOARD ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Welcome! Please share your phone number to continue.",
        reply_markup=reply_markup
    )

# === CONTACT RECEIVED → SEND LOGIN BUTTON ===
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("Please share a valid contact.")
        return

    phone = contact.phone_number
    user_id = update.effective_user.id
    login_url = f"{WEB_URL}?phone={urllib.parse.quote(phone)}&user_id={user_id}"

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Open Login", url=login_url)]
    ])

    await update.message.reply_text(
        "Login page ready.\nTap below to open:",
        reply_markup=button
    )

# === MAIN ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Bot is RUNNING...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
