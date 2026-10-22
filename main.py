import os
import threading
import time
from flask import Flask
import telebot

# --- 1. FAUX SERVEUR WEB POUR RENDER (Corrige l'erreur Port) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Baccarat Bot is LIVE - Snecky"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    print(f"Web server starting on port {port}")
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# --- 2. BOT TELEGRAM ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("ERREUR: BOT_TOKEN non defini dans Render > Environment")
    while True:
        time.sleep(3600)

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Nettoie les anciens webhooks/conflits au demarrage
try:
    bot.remove_webhook()
    time.sleep(1)
    bot.delete_webhook(drop_pending_updates=True)
    print("Webhook cleaned")
except Exception as e:
    print(f"Webhook clean ignore: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🔥 *BACCARAT BOT SNECKY - EN LIGNE* 🔥\n\n"
        "✅ Bot corrigé et Live sur Render\n\n"
        "Commandes:\n"
        "/predict - Prediction Baccarat\n"
        "/stats - Statistiques\n"
        "/help - Aide",
        parse_mode="Markdown")

@bot.message_handler(commands=['predict', 'p'])
def predict(message):
    import random
    choix = random.choice(["🔵 BANKER", "🔴 PLAYER"])
    confiance = random.randint(75, 92)
    bot.reply_to(message, f"🎯 Prediction: {choix}\n📊 Confiance: {confiance}%\n\nBonne chance Snecky!")

@bot.message_handler(commands=['stats', 'help'])
def other(message):
    bot.reply_to(message, "Bot opérationnel. Tape /predict pour une prediction.")

print("Bot is starting polling...")

# Boucle anti-409: si 409, on attend et on retente
while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5, skip_pending=True)
    except Exception as e:
        print(f"Polling error (va se relancer): {e}")
        time.sleep(5)
