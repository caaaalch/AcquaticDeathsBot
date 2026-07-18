from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = "8984009440:AAEsTrFdJbOjBCD_2WJnZXIg43o6IEZNo5U"


async def start(update: Update, context):
    await update.message.reply_text(
        "⚰️ AcquaticDeaths\n\n"
        "Usa /nuovamorte per inviare una segnalazione."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot acceso")

app.run_polling()