import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Клиент OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-помощник 🐶")

# Любое текстовое сообщение
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=200
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Ошибка OpenAI: {e}"

    await update.message.reply_text(answer)

# Создание приложения Telegram (без Updater)
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling()
