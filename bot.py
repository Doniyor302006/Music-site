import telebot
import requests

API_TOKEN = '7548300887:AAHXTPfkHTiTwHQRoCwQ25dJNV50040bvAk'
bot = telebot.TeleBot(API_TOKEN)

FLASK_SERVER = "http://127.0.0.1:5000/upload_from_telegram"  # Flask server manzili (hostga qarab o'zgartiriladi)

@bot.message_handler(content_types=['audio', 'document'])
def handle_audio(message):
    file_info = bot.get_file(message.audio.file_id if message.audio else message.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
    
    file_name = message.audio.file_name if message.audio else message.document.file_name
    
    # Yuklash va Flask'ga yuborish
    try:
        file_data = requests.get(file_url)
        response = requests.post(FLASK_SERVER, files={'file': (file_name, file_data.content)})
        if response.status_code == 200:
            bot.reply_to(message, "Musiqa saytga yuklandi!")
        else:
            bot.reply_to(message, "Xatolik yuz berdi.")
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

bot.polling()
