import flask
import threading
flask.Flask(__name__).route('/')(lambda: 'OK').__self__.run(host='0.0.0.0', port=10000, threading=True)
import os
import io
import telebot
import requests
import pypdf
import docx2txt
import google.generativeai as genai
import time

bot = telebot.TeleBot("8678420801:AAGN8Z0EKieIDSrhxXd6EaJX5r187Q49AAc")
genai.configure(api_key="AQ.Ab8RN6JLw4lxZ9wj_IBP9on21D6PaIMX8qHlsqPm12y2Cf-x2Q")
model = genai.GenerativeModel("gemini-2.0-flash")

@bot.message_handler(content_types=["text", "photo", "document"])
def reply(m):
    try:
        prompt = m.caption if m.caption else "Bu faylni tahlil qilib ber."
        if m.content_type == "text":
            res = model.generate_content(m.text).text
        elif m.content_type == "photo":
            file_info = bot.get_file(m.photo[-1].file_id)
            b = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}").content
            res = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": b}]).text
        elif m.content_type == "document":
            f_name = m.document.file_name.lower()
            f_info = bot.get_file(m.document.file_id)
            b = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{f_info.file_path}").content
            text_content = ""
            if f_name.endswith(".pdf"):
                pdf = pypdf.PdfReader(io.BytesIO(b))
                text_content = "".join([page.extract_text() for page in pdf.pages])
            elif f_name.endswith(".docx"):
                text_content = docx2txt.process(io.BytesIO(b))
            elif f_name.endswith(".txt"):
                text_content = b.decode("utf-8", errors="ignore")
            else:
                bot.reply_to(m, "Kechirasiz, faqat PDF, Word, TXT va rasmlarni tushunaman.")
                return
            res = model.generate_content(f"{prompt}\n\n{text_content}").text
        bot.reply_to(m, res if res else "Xatolik yuz berdi.")
    except Exception as e:
        bot.reply_to(m, f"Xato: {e}")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=30)
    except Exception as e:
        time.sleep(5)
