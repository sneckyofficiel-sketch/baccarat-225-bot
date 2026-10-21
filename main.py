import os
import threading
from flask import Flask
import telebot
from telebot import types

app = Flask(__name__)

@app.route('/')
def home():
    return "Baccarat 225 Bot Live! ✅"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# LANCE FLASK EN ARRIERE PLAN
threading.Thread(target=run_flask, daemon=True).start()

# TOKEN - On le prend de Render, pas du code
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Si toujours pas de token, le bot ne peut pas démarrer
if not TOKEN:
    print("❌ ERREUR: BOT_TOKEN non trouvé dans Render!")

bot = telebot.TeleBot(TOKEN)

history = []
stats = {"B": 0, "P": 0, "T": 0}

def prediction():
    if len(history) < 3:
        return "🔮 Prédiction: 🔵 BANKER (Début de partie)"
    last = history[-5:]
    b = last.count("B")
    p = last.count("P")
    if b > p:
        return f"🔮 Prédiction: 🔵 BANKER ({b} vs {p} sur les 5 derniers)"
    elif p > b:
        return f"🔮 Prédiction: 🔴 PLAYER ({p} vs {b} sur les 5 derniers)"
    else:
        return "🔮 Prédiction: 🔵 BANKER (Égalité, on suit Banker)"

@bot.message_handler(commands=['start'])
def start_cmd(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔵 Banker", "🔴 Player")
    markup.row("🟢 Tie", "🔮 Prédire")
    markup.row("📊 Stats", "🗑️ Reset")
    bot.send_message(m.chat.id, "🎲 Baccarat 225 Prêt !\nEnvoie Banker / Player à chaque tour.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    txt = m.text or ""
    if "Banker" in txt:
        history.append("B"); stats["B"]+=1
        bot.reply_to(m, f"✅ Banker enregistré\nBANKER {stats['B']} vs {stats['P']}")
    elif "Player" in txt:
        history.append("P"); stats["P"]+=1
        bot.reply_to(m, f"✅ Player enregistré\nBANKER {stats['B']} vs {stats['P']}")
    elif "Tie" in txt:
        history.append("T"); stats["T"]+=1
        bot.reply_to(m, f"✅ Tie enregistré")
    elif "Prédire" in txt:
        bot.reply_to(m, prediction())
    elif "Stats" in txt:
        bot.reply_to(m, f"📊 Stats\nBanker: {stats['B']}\nPlayer: {stats['P']}\nTie: {stats['T']}\nTotal: {len(history)}")
    elif "Reset" in txt:
        history.clear(); stats["B"]=0; stats["P"]=0; stats["T"]=0
        bot.reply_to(m, "🗑️ Reset OK !")

print("Bot en démarrage...")
bot.infinity_polling()
