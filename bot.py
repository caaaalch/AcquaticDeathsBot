import os
import re
import asyncio

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
# START
# ==========================

async def start(update: Update, context):

    await update.message.reply_text(

        "⚰️ AcquaticDeaths\n\n"
        "Usa /nuovamorte per creare una segnalazione."

    )



# ==========================
# NUOVA MORTE
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
# ELIMINA MESSAGGIO UTENTE
# ==========================

async def elimina_messaggio(update):

    try:

        await update.message.delete()

    except:

        pass



# ==========================
# AGGIORNA MESSAGGIO PRINCIPALE
# ==========================

async def aggiorna_messaggio(update, context, testo):

    await context.bot.edit_message_text(

        chat_id=update.effective_chat.id,

        message_id=context.user_data["messaggio_id"],

        text=testo

    )



# ==========================
# MESSAGGIO ERRORE TEMPORANEO
# ==========================

async def errore_temporaneo(update, testo):

    messaggio = await update.message.reply_text(testo)


    await asyncio.sleep(3)


    try:

        await messaggio.delete()

    except:

        pass
    
# ==========================
# NOME
# ==========================

async def nome(update, context):

    await elimina_messaggio(update)


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

    await elimina_messaggio(update)


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
# MOTIVO BOTTONI
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

    await elimina_messaggio(update)


    context.user_data["luogo"] = update.message.text


    await aggiorna_messaggio(

        update,

        context,

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 5/7\n\n"
        "📅 Inserisci la data.\n\n"
        "Formato: GG/MM/AA\n"
        "Esempio: 18/07/26"

    )


    return DATA



# ==========================
# DATA
# ==========================

async def data(update, context):

    testo = update.message.text


    controllo = re.match(

        r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{2}$",

        testo

    )


    if not controllo:

        await elimina_messaggio(update)

        await errore_temporaneo(

            update,

            "❌ Data non valida.\n"
            "Usa GG/MM/AA\n"
            "Esempio: 18/07/26"

        )

        return DATA



    await elimina_messaggio(update)


    context.user_data["data"] = testo


    await aggiorna_messaggio(

        update,

        context,

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 6/7\n\n"
        "🕒 Inserisci l'ora.\n\n"
        "Formato: HH:MM\n"
        "Esempio: 18:30"

    )


    return ORA



# ==========================
# ORA
# ==========================

async def ora(update, context):

    testo = update.message.text


    controllo = re.match(

        r"^([01][0-9]|2[0-3]):[0-5][0-9]$",

        testo

    )


    if not controllo:

        await elimina_messaggio(update)


        await errore_temporaneo(

            update,

            "❌ Ora non valida.\n"
            "Usa HH:MM\n"
            "Esempio: 18:30"

        )


        return ORA



    await elimina_messaggio(update)


    context.user_data["ora"] = testo


    tastiera = [

        [

            InlineKeyboardButton(

                "📷 Invia foto",

                callback_data="FOTO"

            )

        ],

        [

            InlineKeyboardButton(

                "⏭️ Salta foto",

                callback_data="NO_FOTO"

            )

        ]

    ]


    await context.bot.edit_message_text(

        chat_id=update.effective_chat.id,

        message_id=context.user_data["messaggio_id"],

        text=

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 7/7\n\n"
        "📷 Foto del decesso:",

        reply_markup=InlineKeyboardMarkup(tastiera)

    )


    return FOTO


# ==========================
# FOTO
# ==========================

async def foto(update, context):

    query = update.callback_query


    # Se arriva dal bottone "Salta foto"

    if query and query.data == "NO_FOTO":

        await query.answer()


        context.user_data["foto"] = None


        await mostra_conferma(

            update,

            context

        )


        return CONFERMA



    # Se arriva dal bottone "Invia foto"

    if query and query.data == "FOTO":

        await query.answer()


        await query.edit_message_text(

            "📷 Invia ora la foto del decesso."

        )


        return FOTO



    # Se arriva una vera foto

    if update.message and (update.message.photo or update.message.video):


    if update.message.photo:

        context.user_data["allegato"] = (
            "foto",
            update.message.photo[-1].file_id
        )


    elif update.message.video:

        context.user_data["allegato"] = (
            "video",
            update.message.video.file_id
        )


    await elimina_messaggio(update)


    await mostra_conferma(

        update,

        context

    )


    return CONFERMA



    return FOTO





# ==========================
# MOSTRA CONFERMA
# ==========================

async def mostra_conferma(update, context):


    if context.user_data.get("allegato"):

    tipo = context.user_data["allegato"][0]

    if tipo == "foto":

        stato_foto = "Foto ricevuta 📷"

    else:

        stato_foto = "Video ricevuto 🎥"

else:

    stato_foto = "Non ricevuta ❌"



    testo = (

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📋 RIEPILOGO DECESSO\n\n"

        f"👤 {context.user_data['nome']}\n"
        f"💼 {context.user_data['lavoro']}\n"
        f"📝 {context.user_data['motivo']}\n"
        f"📍 {context.user_data['luogo']}\n"
        f"📅 {context.user_data['data']}\n"
        f"🕒 {context.user_data['ora']}\n"
        f"📷 Foto: {stato_foto}\n\n"

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



    if update.callback_query:


        await update.callback_query.edit_message_text(

            testo,

            reply_markup=InlineKeyboardMarkup(tastiera)

        )


    else:


        await context.bot.edit_message_text(

            chat_id=update.effective_chat.id,

            message_id=context.user_data["messaggio_id"],

            text=testo,

            reply_markup=InlineKeyboardMarkup(tastiera)

        )





# ==========================
# CONFERMA INVIO
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
            f"🕒 Ora: {context.user_data['ora']}\n"

        )


        if context.user_data.get("foto"):


            await context.bot.send_photo(

                chat_id=STAFF_CHANNEL,

                photo=context.user_data["foto"],

                caption=testo

            )


        else:


            await context.bot.send_message(

                chat_id=STAFF_CHANNEL,

                text=testo

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
                    filters.PHOTO | filters.VIDEO,
                    
                    foto
                ),

                CallbackQueryHandler(
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



    print("⚰️ AcquaticDeaths v1.1 online")


    app.run_polling()




if __name__ == "__main__":

    main()