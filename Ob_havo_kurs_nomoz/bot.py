import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7063903269:AAFjfaCXE0TjgvL1MGCRzR5eRAIItPK83zg"  # o'zingizning token
EXCHANGE_API_KEY = "7f37f0204d4886badbb1dbdc"   # exchangerate-api.com dan olingan API kalit
WEATHER_API_KEY = "528bc3e9e4adffb3c734c74d6ab2f8a6"      # openweathermap.org dan olingan API kalit

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum!\n\n"
        "Men sizga quyidagi ma'lumotlarni beraman:\n"
        "☁️ Ob-havo\n💵 Valyuta kursi\n🕌 Namoz vaqtlari\n\n"
        "Quyidagi komandalarni sinab ko‘ring:\n"
        "/obhavo\n/kurs\n/namoz",
        parse_mode="HTML"
    )

# /kurs komandasi
async def kurs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
        r = requests.get(url)
        data = r.json()
        if data["result"] == "success":
            rate = data["conversion_rates"]["UZS"]
            await update.message.reply_text(
                f"💵 <b>Valyuta kursi:</b>\n\n1 USD = <b>{rate}</b> so'm",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text("Valyuta ma'lumotini olishda xatolik yuz berdi.")
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

# /obhavo komandasi
async def obhavo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        city = "Tashkent"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        r = requests.get(url)
        data = r.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        await update.message.reply_text(
            f"☁️ <b>Toshkent shahri uchun ob-havo:</b>\n\n"
            f"{description.capitalize()}, {temp}°C",
            parse_mode="HTML"
        )
    except:
        await update.message.reply_text("Ob-havo ma'lumotini olishda xatolik yuz berdi.")

# /namoz komandasi
async def namoz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "http://api.aladhan.com/v1/timingsByCity?city=Tashkent&country=Uzbekistan&method=2"
        r = requests.get(url)
        data = r.json()["data"]["timings"]
        javob = (
            f"🕌 <b>Toshkent shahri uchun bugungi namoz vaqtlari:</b>\n\n"
            f"Bomdod: {data['Fajr']}\n"
            f"Quyosh: {data['Sunrise']}\n"
            f"Peshin: {data['Dhuhr']}\n"
            f"Asr: {data['Asr']}\n"
            f"Shom: {data['Maghrib']}\n"
            f"Xufton: {data['Isha']}"
        )
        await update.message.reply_text(javob, parse_mode="HTML")
    except:
        await update.message.reply_text("Namoz vaqtlarini olishda xatolik yuz berdi.")

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("kurs", kurs))
app.add_handler(CommandHandler("obhavo", obhavo))
app.add_handler(CommandHandler("namoz", namoz))
app.run_polling()
