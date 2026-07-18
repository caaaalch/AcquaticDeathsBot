import os
import re
import asyncio
import sqlite3
import random
import string


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

PUBLIC_CHANNEL = -1004357018672



# ==========================
# STATI
# ==========================

NOME, LAVORO, MOTIVO, LUOGO, DATA, ORA, ALLEGATO, CONFERMA = range(8)



# ==========================
# GENERATORE ID
# ==========================

def genera_id():

    caratteri = string.ascii_uppercase + string.digits

    return ''.join(
        random.choice(caratteri)
        for _ in range(5)
    )



# ==========================
# DATABASE
# ==========================

def database():

    conn = sqlite3.connect("deaths.db")

    cursor = conn.cursor()


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS deaths (

        id TEXT PRIMARY KEY,

        user_id INTEGER,

        nome TEXT,

        lavoro TEXT,

        motivo TEXT,

        luogo TEXT,

        data TEXT,

        ora TEXT,

        allegato_tipo TEXT,

        allegato_id TEXT,

        stato TEXT DEFAULT 'in_attesa'

    )

    """)


    conn.commit()

    conn.close()




def crea_decesso(dati):

    conn = sqlite3.connect("deaths.db")

    cursor = conn.cursor()


    death_id = genera_id()


    cursor.execute("""

    INSERT INTO deaths (

        id,
        user_id,
        nome,
        lavoro,
        motivo,
        luogo,
        data,
        ora,
        allegato_tipo,
        allegato_id

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """,

    (

        death_id,

        dati["utente_id"],

        dati["nome"],

        dati["lavoro"],

        dati["motivo"],

        dati["luogo"],

        dati["data"],

        dati["ora"],


        dati["allegato"][0]
        if dati.get("allegato")
        else None,


        dati["allegato"][1]
        if dati.get("allegato")
        else None

    ))


    conn.commit()

    conn.close()


    return death_id




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


    context.user_data["utente_id"] = update.effective_user.id


    messaggio = await update.message.reply_text(

        "⚰️ AcquaticDeaths\n\n"
        "━━━━━━━━━━━━━━\n"
        "📊 Progresso: 1/7\n\n"
        "👤 Inserisci il nome del deceduto."

    )


    context.user_data["messaggio_id"] = messaggio.message_id


    return NOME




# ==========================
# UTILITA'
# ==========================

async def elimina_messaggio(update):

    try:

        await update.message.delete()

    except:

        pass




async def aggiorna_messaggio(update, context, testo):

    await context.bot.edit_message_text(

        chat_id=update.effective_chat.id,

        message_id=context.user_data["messaggio_id"],

        text=testo

    )




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
        "Formato: GG/MM/AA"

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

            "❌ Data non valida.\nFormato: GG/MM/AA"

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
        "Formato: HH:MM"

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

            "❌ Ora non valida.\nFormato: HH:MM"

        )


        return ORA



    await elimina_messaggio(update)


    context.user_data["ora"] = testo



    tastiera = [

        [

            InlineKeyboardButton(

                "📎 Invia foto/video",

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
# ALLEGATO
# ==========================

async def allegato(update, context):

    query = update.callback_query



    if query and query.data == "SALTA_ALLEGATO":

        await query.answer()


        context.user_data["allegato"] = None


        await mostra_conferma(update, context)


        return CONFERMA




    if query and query.data == "INVIA_ALLEGATO":

        await query.answer()


        await query.edit_message_text(

            "📎 Invia ora foto o video del decesso."

        )


        return ALLEGATO




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
# RIEPILOGO
# ==========================

async def mostra_conferma(update, context):

    if context.user_data.get("allegato"):

        if context.user_data["allegato"][0] == "foto":
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
# INVIO STAFF
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




    death_id = crea_decesso(context.user_data)



    testo = (

        "⚰️ NUOVA SEGNALAZIONE\n\n"

        f"🆔 ID: {death_id}\n\n"

        f"👤 Deceduto: {context.user_data['nome']}\n"
        f"💼 Lavoro: {context.user_data['lavoro']}\n"
        f"📝 Motivo: {context.user_data['motivo']}\n"
        f"📍 Luogo: {context.user_data['luogo']}\n"
        f"📅 Data: {context.user_data['data']}\n"
        f"🕒 Ora: {context.user_data['ora']}\n"

    )



    tastiera = [

        [

            InlineKeyboardButton(
                "✅ APPROVA",
                callback_data=f"APPROVA_{death_id}"
            ),

            InlineKeyboardButton(
                "❌ RIFIUTA",
                callback_data=f"RIFIUTA_{death_id}"
            )

        ]

    ]



    allegato = context.user_data.get("allegato")



    if allegato:

        tipo, file_id = allegato


        if tipo == "foto":

            await context.bot.send_photo(

                chat_id=STAFF_CHANNEL,

                photo=file_id,

                caption=testo,

                reply_markup=InlineKeyboardMarkup(tastiera)

            )


        else:

            await context.bot.send_video(

                chat_id=STAFF_CHANNEL,

                video=file_id,

                caption=testo,

                reply_markup=InlineKeyboardMarkup(tastiera)

            )



    else:

        await context.bot.send_message(

            chat_id=STAFF_CHANNEL,

            text=testo,

            reply_markup=InlineKeyboardMarkup(tastiera)

        )



    await query.edit_message_text(
        "✅ Segnalazione inviata allo staff."
    )


    context.user_data.clear()


    return ConversationHandler.END





# ==========================
# DECISIONE STAFF
# ==========================

async def decisione_staff(update, context):

    query = update.callback_query

    await query.answer()



    if query.data == "gia_deciso":

        await query.answer(
            "Questa segnalazione è già stata valutata.",
            show_alert=True
        )

        return



    azione, death_id = query.data.split("_")



    conn = sqlite3.connect("deaths.db")

    cursor = conn.cursor()



    cursor.execute(

        """

        SELECT user_id, nome, lavoro, motivo, luogo, data, ora, allegato_tipo, allegato_id

        FROM deaths

        WHERE id=?

        """,

        (death_id,)

    )



    morte = cursor.fetchone()



    if not morte:

        conn.close()

        return



    user_id = morte[0]



    nome_staff = update.effective_user.username


    if nome_staff:

        staff = f"@{nome_staff}"

    else:

        staff = update.effective_user.first_name



    testo_pubblico = (

        "⚰️ DECESSO\n\n"

        f"👤 {morte[1]}\n"
        f"💼 {morte[2]}\n"
        f"📝 {morte[3]}\n"
        f"📍 {morte[4]}\n"
        f"📅 {morte[5]}\n"
        f"🕒 {morte[6]}"

    )



    if azione == "APPROVA":


        cursor.execute(

            "UPDATE deaths SET stato='approvato' WHERE id=?",

            (death_id,)

        )


        bottone = "✅ APPROVATA"



        await context.bot.send_message(

            chat_id=user_id,

            text="✅ La tua segnalazione è stata approvata dallo staff."

        )



        if morte[7] == "foto":

            await context.bot.send_photo(

                chat_id=PUBLIC_CHANNEL,

                photo=morte[8],

                caption=testo_pubblico

            )


        elif morte[7] == "video":

            await context.bot.send_video(

                chat_id=PUBLIC_CHANNEL,

                video=morte[8],

                caption=testo_pubblico

            )


        else:

            await context.bot.send_message(

                chat_id=PUBLIC_CHANNEL,

                text=testo_pubblico

            )



        nuovo_testo = query.message.caption + f"\n\n✅ APPROVATA da {staff}"



    else:


        cursor.execute(

            "UPDATE deaths SET stato='rifiutato' WHERE id=?",

            (death_id,)

        )


        bottone = "❌ RIFIUTATA"



        await context.bot.send_message(

            chat_id=user_id,

            text="❌ La tua segnalazione è stata rifiutata dallo staff."

        )



        nuovo_testo = query.message.caption + f"\n\n❌ RIFIUTATA da {staff}"




    conn.commit()

    conn.close()



    tastiera = [

        [

            InlineKeyboardButton(

                bottone,

                callback_data="gia_deciso"

            )

        ]

    ]



    if query.message.photo:

        await query.edit_message_caption(

            caption=nuovo_testo,

            reply_markup=InlineKeyboardMarkup(tastiera)

        )

    else:

        await query.edit_message_text(

            text=nuovo_testo,

            reply_markup=InlineKeyboardMarkup(tastiera)

        )





# ==========================
# MAIN
# ==========================

def main():

    database()



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
                MessageHandler(filters.TEXT & ~filters.COMMAND, nome)
            ],


            LAVORO:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, lavoro)
            ],


            MOTIVO:[
                CallbackQueryHandler(motivo)
            ],


            LUOGO:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, luogo)
            ],


            DATA:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, data)
            ],


            ORA:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, ora)
            ],


            ALLEGATO:[

                MessageHandler(
                    filters.PHOTO | filters.VIDEO,
                    allegato
                ),

                CallbackQueryHandler(allegato)

            ],


            CONFERMA:[

                CallbackQueryHandler(
                    conferma,
                    pattern="^(INVIA|ANNULLA)$"
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



    app.add_handler(

        CallbackQueryHandler(

            decisione_staff,

            pattern="^(APPROVA|RIFIUTA)_"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            decisione_staff,

            pattern="^gia_deciso$"

        )

    )



    print("⚰️ AcquaticDeaths v1.5 online")

    app.run_polling()




if __name__ == "__main__":

    main()