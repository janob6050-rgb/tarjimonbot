import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator

bot = telebot.TeleBot("BOT_TOKEN")

user_text = {}

languages = {
    "uz": "🇺🇿 Uzbek",
    "ru": "🇷🇺 Russian",
    "en": "🇬🇧 English",
    "tr": "🇹🇷 Turkish",
    "de": "🇩🇪 German",
    "fr": "🇫🇷 French",
    "es": "🇪🇸 Spanish",
    "ar": "🇸🇦 Arabic",
    "zh-CN": "🇨🇳 Chinese",
    "hi": "🇮🇳 Hindi"
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🌍 Istalgan matnni yuboring — uni bir necha soniyada boshqa tilga tarjima qilaman.")

@bot.message_handler(func=lambda m: True)
def text(message):

    user_text[message.chat.id] = message.text

    keyboard = InlineKeyboardMarkup()

    for code, name in languages.items():
        keyboard.add(
            InlineKeyboardButton(name, callback_data=code)
        )

    bot.send_message(
        message.chat.id,
        "Qaysi tilga tarjima qilinsin?",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def translate(call):

    text = user_text.get(call.message.chat.id)

    lang = call.data

    translated = GoogleTranslator(source='auto', target=lang).translate(text)

    bot.send_message(call.message.chat.id, translated)

bot.infinity_polling()
