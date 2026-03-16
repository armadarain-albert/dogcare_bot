import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Логи
logging.basicConfig(level=logging.INFO)

# Токены из окружения Railway
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Клиент OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой бот-помощник по собакам. "
        "Можешь задавать вопросы о поведении, тренировке, здоровье или уходе за собакой."
    )

# Обработчик любых текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Добавляем системное сообщение, чтобы OpenAI отвечал как эксперт по собакам
    messages = [
        {"role": "system", "content": "Ты эксперт по собакам. Даёшь полезные и практичные советы владельцам собак."},
        {"role": "user", "content": user_text}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Произошла ошибка при обращении к OpenAI: {e}"

    await update.message.reply_text(answer)

# Основная функция
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Бот-помощник по собакам запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
