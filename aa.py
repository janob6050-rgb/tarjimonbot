import telebot
from deep_translator import GoogleTranslator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8711550356:AAHzbpA0MQYfqemkwj8BsgMS6e0KRXMe8jo"
bot = telebot.TeleBot(TOKEN)

user_text = {}

languages = {
    "uz": "🇺🇿 Uzbek",
    "ru": "🇷🇺 Russian",
    "en": "🇬🇧 English",
    "tr": "🇹🇷 Turkish"
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Matn yuboring.")

@bot.message_handler(func=lambda m: True)
def get_text(message):
    user_text[message.chat.id] = message.text
    
    keyboard = InlineKeyboardMarkup()
    
    for code, name in languages.items():
        keyboard.add(InlineKeyboardButton(name, callback_data=code))
    
    bot.send_message(message.chat.id, "Qaysi tilga tarjima?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def translate(call):
    text = user_text.get(call.message.chat.id)

    translated = GoogleTranslator(source='auto', target=call.data).translate(text)

    bot.send_message(call.message.chat.id, translated)

bot.infinity_polling()
