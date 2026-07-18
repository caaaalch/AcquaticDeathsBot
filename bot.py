import os
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("TOKEN")

STAFF_CHANNEL = -1004388077811

async def start(update: Update, context):
    await update.message.reply_text(
        "⚰️ AcquaticDeaths\n\n"
        "Usa /nuovamorte per inviare una segnalazione."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot acceso")

app.run_polling()