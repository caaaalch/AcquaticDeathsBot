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


# ==========================
# CONFIGURAZIONE
# ==========================

TOKEN = os.getenv("TOKEN")

STAFF_CHANNEL = -1004388077811


# ==========================
# STATI CONVERSAZIONE
# ==========================

NOME, LAVORO, MOTIVO, LUOGO, DATA, ORA, FOTO, CONFERMA = range(8)


# ==========================
# COMANDO START
# ==========================

async def start(update: Update, context):

    await update.message.reply_text(
        "⚰️ Benvenuto in AcquaticDeaths\n\n"
        "Usa /nuovamorte per segnalare un decesso."
    )


# ==========================
# INIZIO SEGNALAZIONE
# ==========================

async def nuova_morte(update: Update, context):

    context.user_data.clear()

    messaggio = await update.message.reply_text(
        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 1/7\n\n"
        "👤 Inserisci il nome del deceduto."
    )


    context.user_data["messaggio_id"] = messaggio.message_id


    return NOME


# ==========================
# AGGIORNA MESSAGGIO
# ==========================

async def aggiorna_messaggio(update, context, testo):

    chat_id = update.effective_chat.id

    message_id = context.user_data["messaggio_id"]


    await context.bot.edit_message_text(

        chat_id=chat_id,

        message_id=message_id,

        text=testo

    )
    

# ==========================
# NOME
# ==========================

async def nome(update, context):

    context.user_data["nome"] = update.message.text


    await aggiorna_messaggio(

        update,

        context,

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 2/7\n\n"
        "💼 Inserisci il lavoro del deceduto."

    )


    return LAVORO



# ==========================
# LAVORO
# ==========================

async def lavoro(update, context):

    context.user_data["lavoro"] = update.message.text


    tastiera = [

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


    await context.bot.edit_message_text(

        chat_id=update.effective_chat.id,

        message_id=context.user_data["messaggio_id"],

        text=

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 3/7\n\n"
        "📝 Seleziona il motivo del decesso:",

        reply_markup=InlineKeyboardMarkup(tastiera)

    )


    return MOTIVO



# ==========================
# MOTIVO (BOTTONI)
# ==========================

async def motivo(update, context):

    query = update.callback_query

    await query.answer()


    context.user_data["motivo"] = query.data


    await aggiorna_messaggio(

        update,

        context,

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 4/7\n\n"
        "📍 Inserisci il luogo del decesso."

    )


    return LUOGO



# ==========================
# LUOGO
# ==========================

async def luogo(update, context):

    context.user_data["luogo"] = update.message.text


    await aggiorna_messaggio(

        update,

        context,

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 5/7\n\n"
        "📅 Inserisci la data.\n\n"
        "Formato obbligatorio: GG/MM/AA\n"
        "Esempio: 18/07/26"

    )


    return DATA



# ==========================
# DATA CON CONTROLLO
# ==========================

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



    await aggiorna_messaggio(

        update,

        context,

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 6/7\n\n"
        "🕒 Inserisci l'ora.\n\n"
        "Formato obbligatorio: HH:MM\n"
        "Esempio: 18:30"

    )


    return ORA



# ==========================
# ORA CON CONTROLLO
# ==========================

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


    await aggiorna_messaggio(

        update,

        context,

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 7/7\n\n"
        "📷 Invia la foto del decesso."

    )


    return FOTO


# ==========================
# FOTO
# ==========================

async def foto(update, context):

    if not update.message.photo:

        await update.message.reply_text(
            "❌ Devi inviare una foto."
        )

        return FOTO


    context.user_data["foto"] = update.message.photo[-1].file_id


    testo = (

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📋 RIEPILOGO DECESSO\n\n"

        f"👤 {context.user_data['nome']}\n"
        f"💼 {context.user_data['lavoro']}\n"
        f"📝 {context.user_data['motivo']}\n"
        f"📍 {context.user_data['luogo']}\n"
        f"📅 {context.user_data['data']}\n"
        f"🕒 {context.user_data['ora']}\n\n"

        "Confermare l'invio?"
    )


    tastiera = [

        [

            InlineKeyboardButton(
                "✅ Invia",
                callback_data="INVIA"
            )

        ],

        [

            InlineKeyboardButton(
                "❌ Annulla",
                callback_data="ANNULLA"
            )

        ]

    ]


    await update.message.reply_text(

        testo,

        reply_markup=InlineKeyboardMarkup(tastiera)

    )


    return CONFERMA



# ==========================
# CONFERMA
# ==========================

async def conferma(update, context):

    query = update.callback_query

    await query.answer()


    if query.data == "ANNULLA":

        await query.edit_message_text(

            "❌ Segnalazione annullata."

        )

        context.user_data.clear()

        return ConversationHandler.END



    if query.data == "INVIA":


        testo = (

            "⚰️ NUOVA SEGNALAZIONE\n\n"

            f"👤 Deceduto: {context.user_data['nome']}\n"
            f"💼 Lavoro: {context.user_data['lavoro']}\n"
            f"📝 Motivo: {context.user_data['motivo']}\n"
            f"📍 Luogo: {context.user_data['luogo']}\n"
            f"📅 Data: {context.user_data['data']}\n"
            f"🕒 Ora: {context.user_data['ora']}\n\n"

            "In attesa di approvazione."
        )


        await context.bot.send_photo(

            chat_id=STAFF_CHANNEL,

            photo=context.user_data["foto"],

            caption=testo

        )


        await query.edit_message_text(

            "✅ Segnalazione inviata allo staff."

        )


        context.user_data.clear()


        return ConversationHandler.END



# ==========================
# AVVIO BOT
# ==========================

def main():

    app = Application.builder().token(TOKEN).build()



    conversazione = ConversationHandler(

        entry_points=[

            CommandHandler(
                "nuovamorte",
                nuova_morte
            )

        ],


        states={


            NOME:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    nome
                )

            ],


            LAVORO:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    lavoro
                )

            ],


            MOTIVO:[

                CallbackQueryHandler(
                    motivo
                )

            ],


            LUOGO:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    luogo
                )

            ],


            DATA:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    data
                )

            ],


            ORA:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    ora
                )

            ],


            FOTO:[

                MessageHandler(
                    filters.PHOTO,
                    foto
                )

            ],


            CONFERMA:[

                CallbackQueryHandler(
                    conferma
                )

            ]

        },


        fallbacks=[]

    )



    app.add_handler(

        CommandHandler(
            "start",
            start
        )

    )


    app.add_handler(conversazione)



    print("⚰️ AcquaticDeaths online")


    app.run_polling()



if __name__ == "__main__":

    main()