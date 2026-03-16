import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

# Берём ключи из переменных окружения
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Проверка наличия ключей
if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY не найден в переменных окружения!")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения!")

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_KEY)

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-помощник по уходу за собаками 🐶\n"
        "Задавай вопросы о поведении, кормлении или здоровье своей собаки."
    )

# Простейший обработчик команд
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Запуск бота
app.run_polling()
