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
# STATI
# ==========================

NOME, LAVORO, MOTIVO, LUOGO, DATA, ORA, ALLEGATO, CONFERMA = range(8)



# ==========================
# START
# ==========================

async def start(update: Update, context):

    await update.message.reply_text(
        "⚰️ AcquaticDeaths\n\n"
        "Usa /nuovamorte per creare una segnalazione."
    )



# ==========================
# NUOVA SEGNALAZIONE
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
# ELIMINA MESSAGGIO
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
# ERRORE TEMPORANEO
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

        [InlineKeyboardButton("🔫 Sparatoria", callback_data="Sparatoria")],

        [InlineKeyboardButton("🗡️ Omicidio", callback_data="Omicidio")],

        [InlineKeyboardButton("👮 Abbattimento FdO", callback_data="Abbattimento FdO")],

        [InlineKeyboardButton("🪂 Caduta", callback_data="Caduta")],

        [InlineKeyboardButton("🔥 Incendio", callback_data="Incendio")],

        [InlineKeyboardButton("❓ Sconosciuta", callback_data="Sconosciuta")]

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
# MOTIVO
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
            "Usa GG/MM/AA"

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
            "Usa HH:MM"

        )

        return ORA



    await elimina_messaggio(update)


    context.user_data["ora"] = testo


    tastiera = [

        [
            InlineKeyboardButton(
                "📷 Invia foto/video",
                callback_data="INVIA_ALLEGATO"
            )
        ],

        [
            InlineKeyboardButton(
                "⏭️ Salta allegato",
                callback_data="SALTA_ALLEGATO"
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
        "📎 Allegato del decesso:",

        reply_markup=InlineKeyboardMarkup(tastiera)

    )


    return ALLEGATO

# ==========================
# ALLEGATO FOTO / VIDEO
# ==========================

async def allegato(update, context):

    query = update.callback_query


    # Salta allegato

    if query and query.data == "SALTA_ALLEGATO":

        await query.answer()

        context.user_data["allegato"] = None


        await mostra_conferma(update, context)


        return CONFERMA



    # Richiesta allegato

    if query and query.data == "INVIA_ALLEGATO":

        await query.answer()


        await query.edit_message_text(

            "📎 Invia una foto o un video del decesso."

        )


        return ALLEGATO



    # Ricezione foto/video

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


        await mostra_conferma(update, context)


        return CONFERMA



    return ALLEGATO




# ==========================
# RECAP
# ==========================

async def mostra_conferma(update, context):


    if context.user_data.get("allegato"):


        tipo = context.user_data["allegato"][0]


        if tipo == "foto":

            stato = "Foto ricevuta 📷"


        else:

            stato = "Video ricevuto 🎥"


    else:

        stato = "Non ricevuto ❌"



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
        f"📎 Allegato: {stato}\n\n"

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


    await context.bot.edit_message_text(

        chat_id=update.effective_chat.id,

        message_id=context.user_data["messaggio_id"],

        text=testo,

        reply_markup=InlineKeyboardMarkup(tastiera)

    )



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
            f"🕒 Ora: {context.user_data['ora']}\n"

        )


        allegato = context.user_data.get("allegato")



        if allegato:


            tipo, file_id = allegato



            if tipo == "foto":


                await context.bot.send_photo(

                    chat_id=STAFF_CHANNEL,

                    photo=file_id,

                    caption=testo

                )



            else:


                await context.bot.send_video(

                    chat_id=STAFF_CHANNEL,

                    video=file_id,

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


            ALLEGATO:[

                MessageHandler(

                    filters.PHOTO | filters.VIDEO,

                    allegato

                ),

                CallbackQueryHandler(

                    allegato

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



    print("⚰️ AcquaticDeaths v1.2 online")


    app.run_polling()



if __name__ == "__main__":

    main()