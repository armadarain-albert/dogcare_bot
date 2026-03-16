# bot.py
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-помощник по собакам 🐶\nЗадавай вопросы о воспитании, здоровье и уходе за собаками!"
    )

# Обработка всех сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты эксперт по собакам, даешь советы владельцам собак."},
                {"role": "user", "content": user_text}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        logging.error(e)
        answer = "Извини, что-то пошло не так. Попробуй позже."

    await update.message.reply_text(answer)

def main():
    # Создаем приложение через ApplicationBuilder
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Добавляем хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    app.run_polling()  # <- Никакого Updater не нужно!

if __name__ == "__main__":
    main()
