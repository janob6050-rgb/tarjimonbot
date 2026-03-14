import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator
from flask import Flask
import threading
import os

# BotFather'dan olingan token
TOKEN = "8711550356:AAHzbpA0MQYfqemkwj8BsgMS6e0KRXMe8jo"
bot = telebot.TeleBot(TOKEN)

# Flask ilovasini yaratish (name ikkita chiziqcha bilan)
app = Flask(__name__)

# Render serverni o'chirib qo'ymasligi uchun manzil
@app.route('/')
def home():
    return "Bot status: Active and Running!"

user_text = {}
languages = {
    "uz": "🇺🇿 Uzbek", "ru": "🇷🇺 Russian", "en": "🇬🇧 English",
    "tr": "🇹🇷 Turkish", "de": "🇩🇪 German", "fr": "🇫🇷 French",
    "es": "🇪🇸 Spanish", "ar": "🇸🇦 Arabic", "zh-CN": "🇨🇳 Chinese", "hi": "🇮🇳 Hindi"
}

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
            bot.send_message(call.message.chat.id, f"✅ Tarjima:\n\n{translated}", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(call.message.chat.id, "⚠️ Tarjimada xatolik yuz berdi.")
    else:
        bot.send_message(call.message.chat.id, "❌ Matn topilmadi. Iltimos, qayta yuboring.")

# Botni alohida thread'da ishga tushirish funksiyasi
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # 1. Botni ishga tushirish
    threading.Thread(target=run_bot).start()
    
    # 2. Flask serverni Render bergan portda ishga tushirish
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)