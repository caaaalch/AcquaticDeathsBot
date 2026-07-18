import os
import re
import asyncio
import sqlite3


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

PUBLIC_CHANNEL = -1003993420312



# ==========================
# STATI
# ==========================

NOME, LAVORO, MOTIVO, LUOGO, DATA, ORA, ALLEGATO, CONFERMA = range(8)



# ==========================
# DATABASE
# ==========================

def database():

    conn = sqlite3.connect("deaths.db")

    cursor = conn.cursor()


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS deaths (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        nome TEXT,

        lavoro TEXT,

        motivo TEXT,

        luogo TEXT,

        data TEXT,

        ora TEXT,

        allegato_tipo TEXT,

        allegato_id TEXT,

        stato TEXT DEFAULT 'in_attesa',

        staff_message INTEGER

    )

    """)


    conn.commit()

    conn.close()



def crea_decesso(dati):

    conn = sqlite3.connect("deaths.db")

    cursor = conn.cursor()


    cursor.execute("""

    INSERT INTO deaths (

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

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

    """,

    (

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


    death_id = cursor.lastrowid


    conn.commit()

    conn.close()


    return death_id




def salva_staff_message(death_id, message_id):

    conn = sqlite3.connect("deaths.db")

    cursor = conn.cursor()


    cursor.execute(

        """

        UPDATE deaths

        SET staff_message = ?

        WHERE id = ?

        """,

        (

            message_id,

            death_id

        )

    )


    conn.commit()

    conn.close()




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
# ELIMINA MESSAGGIO
# ==========================

async def elimina_messaggio(update):

    try:

        await update.message.delete()

    except:

        pass




# ==========================
# AGGIORNA MESSAGGIO
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

            "❌ Data non valida"

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

            "❌ Ora non valida"

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

            "📎 Invia una foto o un video."

        )


        return ALLEGATO



    if update.message and (update.message.photo or update.message.video):


        if update.message.photo:

            context.user_data["allegato"] = (

                "foto",

                update.message.photo[-1].file_id

            )


        else:

            context.user_data["allegato"] = (

                "video",

                update.message.video.file_id

            )


        await elimina_messaggio(update)


        await mostra_conferma(update, context)


        return CONFERMA



    return ALLEGATO

# ==========================
# CONFERMA UTENTE
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
# INVIO STAFF / APPROVA
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


        death_id = crea_decesso(context.user_data)



        testo = (

            f"⚰️ NUOVA SEGNALAZIONE #{death_id:03}\n\n"

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

                messaggio = await context.bot.send_photo(

                    chat_id=STAFF_CHANNEL,

                    photo=file_id,

                    caption=testo,

                    reply_markup=InlineKeyboardMarkup(tastiera)

                )


            else:


                messaggio = await context.bot.send_video(

                    chat_id=STAFF_CHANNEL,

                    video=file_id,

                    caption=testo,

                    reply_markup=InlineKeyboardMarkup(tastiera)

                )



        else:


            messaggio = await context.bot.send_message(

                chat_id=STAFF_CHANNEL,

                text=testo,

                reply_markup=InlineKeyboardMarkup(tastiera)

            )



        salva_staff_message(

            death_id,

            messaggio.message_id

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



    dati = query.data.split("_")

    azione = dati[0]

    death_id = int(dati[1])



    conn = sqlite3.connect("deaths.db")

    cursor = conn.cursor()



    cursor.execute(

        "SELECT user_id, nome, lavoro, motivo, luogo, data, ora, allegato_tipo, allegato_id FROM deaths WHERE id=?",

        (death_id,)

    )


    morte = cursor.fetchone()



    if not morte:

        conn.close()

        return



    user_id = morte[0]



    if azione == "APPROVA":


        cursor.execute(

            "UPDATE deaths SET stato='approvato' WHERE id=?",

            (death_id,)

        )


        messaggio = (

            f"⚰️ DECESSO #{death_id:03}\n\n"

            f"👤 {morte[1]}\n"
            f"💼 {morte[2]}\n"
            f"📝 {morte[3]}\n"
            f"📍 {morte[4]}\n"
            f"📅 {morte[5]}\n"
            f"🕒 {morte[6]}"

        )


        await context.bot.send_message(

            chat_id=PUBLIC_CHANNEL,

            text=messaggio

        )


        await context.bot.send_message(

            chat_id=user_id,

            text="✅ La tua segnalazione è stata approvata dallo staff."

        )


        await query.edit_message_text(

            query.message.text + "\n\n✅ APPROVATA"

        )



    else:


        cursor.execute(

            "UPDATE deaths SET stato='rifiutato' WHERE id=?",

            (death_id,)

        )


        await context.bot.send_message(

            chat_id=user_id,

            text="❌ La tua segnalazione è stata rifiutata dallo staff."

        )


        await query.edit_message_text(

            query.message.text + "\n\n❌ RIFIUTATA"

        )



    conn.commit()

    conn.close()




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

                CallbackQueryHandler(conferma)

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



    print("⚰️ AcquaticDeaths v1.3 online")


    app.run_polling()




if __name__ == "__main__":

    main()