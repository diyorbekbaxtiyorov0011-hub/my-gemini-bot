import threading
from flask import Flask
import os
import io
import telebot
import requests
import pypdf
import docx2txt
import google.generativeai as genai
import time

app = Flask('')

@app.route('/')
def home():
    return "OK"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

bot = telebot.TeleBot("8678420801:AAGN8Z0EkieIDSrhxXd6EaJX5r187Q49AAc")
genai.configure(api_key="AQ.Ab8RN6JLw41xz9wj_IBP9on21D6PaIMX8qH1sqPm12y2Cf-x2Q")
model = genai.GenerativeModel("gemini-2.0-flash")

@bot.message_handler(content_types=["text", "photo", "document"])
def reply(m):
    try:
        prompt = m.caption if m.caption else "Bu faylni tahlil qilib ber."
        
        if m.content_type == "text":
            res = model.generate_content(m.text).text
            bot.reply_to(m, res, parse_mode="Markdown")
            
        elif m.content_type == "photo":
            file_info = bot.get_file(m.photo[-1].file_id)
            file_bytes = bot.download_file(file_info.file_path)
            res = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": file_bytes}]).text
            bot.reply_to(m, res, parse_mode="Markdown")
            
        elif m.content_type == "document" and m.document.file_name.endswith('.pdf'):
            file_info = bot.get_file(m.document.file_id)
            file_bytes = bot.download_file(file_info.file_path)
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = "".join([page.extract_text() for page in pdf_reader.pages])
            res = model.generate_content(f"{prompt}\n\nHujjat matni:\n{text}").text
            bot.reply_to(m, res, parse_mode="Markdown")
            
        elif m.content_type == "document" and m.document.file_name.endswith('.docx'):
            file_info = bot.get_file(m.document.file_id)
            file_bytes = bot.download_file(file_info.file_path)
            text = docx2txt.process(io.BytesIO(file_bytes))
            res = model.generate_content(f"{prompt}\n\nHujjat matni:\n{text}").text
            bot.reply_to(m, res, parse_mode="Markdown")
    except Exception as e:
        print(f"XABAR YUBORISHDA XATOLIK: {e}")  # <--- Mana shu yerda xato chiqadi!

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"POLLING XATOLIK: {e}")  # <--- Yoki bu yerda
            time.sleep(5)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    run_flask()
