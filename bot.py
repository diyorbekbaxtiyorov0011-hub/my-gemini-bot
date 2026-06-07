import threading
from flask import Flask
import io
import telebot
from google import genai  # Yangi rasmiy Google GenAI kutubxonasi
import time

app = Flask('')

@app.route('/')
def home():
    return "OK"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Telegram Bot sozlamasi
bot = telebot.TeleBot("8678420801:AAGN8Z0EkieIDSrhxXd6EaJX5r187Q49AAc")

# Yangi Gemini klienti (Eng oxirgi versiya standarti)
client = genai.Client(api_key="AQ.Ab8RN6JLw41xz9wj_IBP9on21D6PaIMX8qH1sqPm12y2Cf-x2Q")

@bot.message_handler(content_types=["text"])
def reply(m):
    try:
        # Yangi versiyada matn generatsiya qilish formati:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=m.text,
        )
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
