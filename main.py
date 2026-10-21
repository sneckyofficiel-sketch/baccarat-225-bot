import os
import telebot
from telebot import types
import threading
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return "Baccarat 225 Bot Live!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    TOKEN = "8926516710:AAEKPlGDOQr9NFZCEuCybrG4ThnEElpx8yo"

bot = telebot.TeleBot(TOKEN)
history = []

def prediction():
    if len(history) < 3:
        return "🔮 Prédiction: 🔵 BANKER"
    last = history[-5:]
    b = last.count("B")
    p = last.count("P")
    if len(history) >= 2 and history[-1] == history[-2]:
        who = "BANKER" if history[-1] == "B" else "PLAYER"
        return f"🔮 SUIVI DE SÉRIE: {who} 🔥"
    if b > p:
        return f"🔮 BANKER ({b} vs {p})"
    else:
        return f"🔮 PLAYER ({p} vs {b})"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔵 Banker", "🔴 Player")
    markup.row("🟢 Tie", "🔮 Prédire")
    markup.row("📊 Stats", "🗑️ Reset")
    bot.send_message(message.chat.id, "🎰 BACCARAT 225 V2 PRÊT 🎰\nEnvoie les résultats", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def all_msg(message):
    global history
    t = message.text
    if "Banker" in t:
        history.append("B")
        bot.reply_to(message, f"✅ Banker\n{prediction()}")
    elif "Player" in t:
        history.append("P")
        bot.reply_to(message, f"✅ Player\n{prediction()}")
    elif "Tie" in t:
        history.append("T")
        bot.reply_to(message, f"✅ Tie\n{prediction()}")
    elif "Prédire" in t:
        bot.reply_to(message, prediction())
    elif "Stats" in t:
        bot.reply_to(message, f"📊 {len(history)} mains: {''.join(history[-20:])}")
    elif "Reset" in t:
        history.clear()
        bot.reply_to(message, "🗑️ Reset OK")

print("Bot lancé...")
bot.infinity_polling()
