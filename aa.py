import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator
from flask import Flask
import threading
import os
import time

# 1. Sozlamalar
# Render sozlamalaridan tokenni o'qiydi (Xavfsizlik uchun)
TOKEN = os.environ.get('BOT_TOKEN', "8711550356:AAHzbpA0MQYfqemkwj8BsgMS6e0KRXMe8jo")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__) # Tuzatildi: name (2 ta pastki chiziq)

# Sizning Telegram ID raqamingiz (O'zingiznikini yozing)
MY_ID = 7696146906 

# 2. Flask server (Render uchun)
@app.route('/')
def home():
    return "Bot status: Active and Running!"

user_text = {}
languages = {
    "uz": "🇺🇿 Uzbek", "ru": "🇷🇺 Russian", "en": "🇬🇧 English",
    "tr": "🇹🇷 Turkish", "de": "🇩🇪 German", "fr": "🇫🇷 French",
    "es": "🇪🇸 Spanish", "ar": "🇸🇦 Arabic", "zh-CN": "🇨🇳 Chinese", "hi": "🇮🇳 Hindi"
}

# 3. Har 10 minutda (600 soniya) xabar yuborish
def send_periodic_messages():
    while True:
        try:
            bot.send_message(MY_ID, "⏰ 10 minut o'tdi! Bot hali ham faol.")
            time.sleep(600)
        except Exception as e:
            print(f"Taymerda xatolik: {e}")
            time.sleep(10)

# 4. Bot funksiyalari
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🌍 Salom! Matn yuboring, men uni tarjima qilaman.")

@bot.message_handler(func=lambda m: True)
def get_text(message):
    user_text[message.chat.id] = message.text
    keyboard = InlineKeyboardMarkup()
    for code, name in languages.items():
        keyboard.add(InlineKeyboardButton(name, callback_data=code))
    bot.send_message(message.chat.id, "Qaysi tilga tarjima qilamiz?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def translate(call):
    text = user_text.get(call.message.chat.id)
    if text:
        try:
            translated = GoogleTranslator(source='auto', target=call.data).translate(text)
            bot.send_message(call.message.chat.id, f"✅ Tarjima:\n\n{translated}")
        except Exception as e:
            bot.send_message(call.message.chat.id, "⚠️ Tarjimada xatolik yuz berdi.")
    else:
        bot.send_message(call.message.chat.id, "❌ Matn topilmadi.")

# 5. Ishga tushirish qismi
if __name__ == "__main__":
    threading.Thread(target=send_periodic_messages, daemon=True).start()
    
    # Botning pooling qismini alohida thread'da ishga tushirish
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    
    # Flask serverni Render portida ishga tushirish
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
