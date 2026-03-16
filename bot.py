import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from openai import OpenAI

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not OPENAI_KEY or not TELEGRAM_TOKEN:
    raise ValueError("Не заданы переменные окружения OPENAI_API_KEY или TELEGRAM_TOKEN!")

client = OpenAI(api_key=OPENAI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-помощник по уходу за собаками 🐶"
    )

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run_polling()
