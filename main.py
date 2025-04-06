import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

import os
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === FUNCIÓN GENERAL DE RESPUESTA ===
async def responder_ia(update: Update, context: ContextTypes.DEFAULT_TYPE, tipo: str):
    signo = ' '.join(context.args)
    if not signo:
        await update.message.reply_text(f"Escribe tu signo. Ejemplo:\n/{tipo} escorpión")
        return

    prompts = {
        "horoscopo": f"Dame el horóscopo de hoy para el signo {signo} con un tono espiritual, positivo y realista.",
        "semanal": f"Dame el horóscopo semanal para el signo {signo} con consejos útiles y predicciones.",
        "energia": f"Describe la energía del día para el signo {signo} en forma motivadora.",
        "color": f"¿Cuál es el color que potencia el día de una persona del signo {signo} y por qué?",
        "consejo": f"Dame un consejo espiritual para alguien del signo {signo}, profundo y útil.",
        "numero": f"¿Cuál es el número de la suerte hoy para el signo {signo}? Agrega una breve razón simbólica.",
    }

    prompt = prompts.get(tipo)

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        mensaje = respuesta.choices[0].message.content
        await update.message.reply_text(mensaje)
    except Exception as e:
        await update.message.reply_text("Ocurrió un error al generar la respuesta.")
        print(e)

# === COMANDOS INDIVIDUALES ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""¡Bienvenido al Horóscopo Astral IA!

Opciones disponibles:
/horoscopo signo
/semanal signo
/energia signo
/color signo
/consejo signo
/numero signo
""")

async def horoscopo(update, context): return await responder_ia(update, context, "horoscopo")
async def semanal(update, context): return await responder_ia(update, context, "semanal")
async def energia(update, context): return await responder_ia(update, context, "energia")
async def color(update, context): return await responder_ia(update, context, "color")
async def consejo(update, context): return await responder_ia(update, context, "consejo")
async def numero(update, context): return await responder_ia(update, context, "numero")

# === ARRANQUE ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("horoscopo", horoscopo))
    app.add_handler(CommandHandler("semanal", semanal))
    app.add_handler(CommandHandler("energia", energia))
    app.add_handler(CommandHandler("color", color))
    app.add_handler(CommandHandler("consejo", consejo))
    app.add_handler(CommandHandler("numero", numero))
    print("Bot activo con comandos IA...")
    app.run_polling()
