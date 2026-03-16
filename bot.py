import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Загружаем ключи из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой помощник по собакам 🐶\n"
        "Задай мне вопрос о воспитании, здоровье или поведении твоей собаки."
    )

# Обработка всех текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Запрос к OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты эксперт по собакам. Давай давай советы по уходу, воспитанию и поведению собак."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
