import threading
from flask import Flask
import io
import telebot
import google.generativeai as genai
import time

app = Flask('')

@app.route('/')
def home():
    return "OK"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Telegram Bot sozlamasi
bot = telebot.TeleBot("8678420801:AAEVgWVFMa3aVECE4aPR7gMCuJYnFpf0ABk")

# Gemini sozlamasi
genai.configure(api_key="AQ.Ab8RN6JLw41xz9wj_IBP9on21D6PaIMX8qH1sqPm12y2Cf-x2Q")
model = genai.GenerativeModel("gemini-2.0-flash")

@bot.message_handler(content_types=["text"])
def reply(m):
    try:
        response = model.generate_content(m.text)
        bot.reply_to(m, response.text)
    except Exception as e:
        print(f"XABAR YUBORISHDA XATOLIK: {e}")

def run_bot():
    try:
        bot.remove_webhook(drop_pending_updates=True)
        time.sleep(1)
    except:
        pass

    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"POLLING XATOLIK: {e}")
            time.sleep(5)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    run_flask()
