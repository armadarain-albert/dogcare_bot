from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = "8551970999:AAExkhw1NGu5uBM2TWYMTZOVRazOrhzMxjM"
OPENAI_KEY = "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"

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = """
Ты AI ассистент ветеринара и кинолога.

Помогаешь владельцам собак понять здоровье и поведение их питомцев.

Правила:
- отвечай простым языком
- не ставь окончательный диагноз
- если есть риск для здоровья — советуй обратиться к ветеринару
- при необходимости задавай уточняющие вопросы
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
