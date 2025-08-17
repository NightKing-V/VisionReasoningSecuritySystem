import telebot
import os
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

def send_telegram_alert(detected_classes, llm_analysis):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"""
🚨 **Security Alert**
🕒 Time: {ts}
📍 Objects: {', '.join(detected_classes)}

{llm_analysis}
    """
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def send_telegram_status(status):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🔔 Status Update ({ts}): {status}"
    bot.send_message(chat_id=CHAT_ID, text=message)
