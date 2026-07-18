import os
import re
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

TOKEN = os.getenv("TOKEN")

STAFF_CHANNEL = -1004388077811

NOME, LAVORO, MOTIVO, LUOGO, DATA, ORA = range(6)

async def start(update: Update, context):
    await update.message.reply_text(
        "⚰️ AcquaticDeaths\n\n"
        "Usa /nuovamorte per inviare una segnalazione."
    )

async def nuova_morte(update: Update, context):

    await update.message.reply_text(
        "👤 Inserisci il nome del deceduto:"
    )

    return NOME

async def nome(update, context):

    context.user_data["nome"] = update.message.text

    await update.message.reply_text(
        "💼 Inserisci il lavoro del deceduto:"
    )

    return LAVORO

async def lavoro(update, context):

    context.user_data["lavoro"] = update.message.text

    keyboard = [

        [
            InlineKeyboardButton(
                "🔫 Sparatoria",
                callback_data="Sparatoria"
            )
        ],

        [
            InlineKeyboardButton(
                "🗡️ Omicidio",
                callback_data="Omicidio"
            )
        ],

        [
            InlineKeyboardButton(
                "👮 Abbattimento FdO",
                callback_data="Abbattimento FdO"
            )
        ],

        [
            InlineKeyboardButton(
                "🪂 Caduta",
                callback_data="Caduta"
            )
        ],

        [
            InlineKeyboardButton(
                "🔥 Incendio",
                callback_data="Incendio"
            )
        ],

        [
            InlineKeyboardButton(
                "❓ Sconosciuta",
                callback_data="Sconosciuta"
            )
        ]

    ]


    await update.message.reply_text(

        "📝 Seleziona il motivo del decesso:",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )

    return MOTIVO

async def motivo(update, context):

    query = update.callback_query

    await query.answer()

    context.user_data["motivo"] = query.data

    await query.edit_message_text(

        f"✅ Motivo selezionato: {query.data}"

    )

    await query.message.reply_text(

        "📍 Inserisci il luogo del decesso:"

    )

    return LUOGO

async def luogo(update, context):

    context.user_data["luogo"] = update.message.text

    await update.message.reply_text(
        "📅 Inserisci la data (GG/MM/AA):"
    )

    return DATA

async def data(update, context):

    testo = update.message.text


    controllo = re.match(
        r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{2}$",
        testo
    )


    if not controllo:

        await update.message.reply_text(
            "❌ Data non valida.\n\n"
            "Usa il formato GG/MM/AA\n"
            "Esempio: 18/07/26"
        )

        return DATA


    context.user_data["data"] = testo


    await update.message.reply_text(
        "🕒 Inserisci l'ora (HH:MM):"
    )

    return ORA

async def ora(update, context):

    testo = update.message.text


    controllo = re.match(
        r"^([01][0-9]|2[0-3]):[0-5][0-9]$",
        testo
    )


    if not controllo:

        await update.message.reply_text(
            "❌ Ora non valida.\n\n"
            "Usa il formato HH:MM\n"
            "Esempio: 18:30"
        )

        return ORA


    context.user_data["ora"] = testo


    await update.message.reply_text(
        "✅ Grazie per la segnalazione. Verra' valutata da un membro dello staff a breve."
    )


    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

conv = ConversationHandler(

    entry_points=[
        CommandHandler("nuovamorte", nuova_morte)
    ],


    states={

        NOME:[
            MessageHandler(filters.TEXT, nome)
        ],

        LAVORO:[
            MessageHandler(filters.TEXT, lavoro)
        ],

        MOTIVO:[
            CallbackQueryHandler(motivo)
        ],

        LUOGO:[
            MessageHandler(filters.TEXT, luogo)
        ],

        DATA:[
            MessageHandler(filters.TEXT, data)
        ],

        ORA:[
            MessageHandler(filters.TEXT, ora)
        ],

    },


    fallbacks=[]

)


app.add_handler(conv)

print("Bot acceso")

app.run_polling()