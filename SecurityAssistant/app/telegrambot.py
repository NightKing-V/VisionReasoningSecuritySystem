import telebot 
import os

# Replace with your values
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

def send_telegram_alert(detected_classes):
    message = f"⚠️ Weapon Detected: {', '.join(detected_classes)}"
    bot.send_message(chat_id=CHAT_ID, text=message)

def send_telegram_status(status):
    message = f"🔔 Status Update: {status}"
    bot.send_message(chat_id=CHAT_ID, text=message)