import logging
import openai
import os
import pytz
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# Configuración
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
CHANNEL_ID = "@horoscopoSM"

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)

# Signos y emojis
signos = {
    "Aries": "♈", "Tauro": "♉", "Géminis": "♊", "Cáncer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Escorpio": "♏",
    "Sagitario": "♐", "Capricornio": "♑", "Acuario": "♒", "Piscis": "♓"
}

# Función para generar horóscopo con OpenAI
def generar_horoscopo(signo):
    prompt = f"Dame el horóscopo de hoy para el signo {signo} con un tono espiritual, positivo y realista. Usa máximo 4 líneas."
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
        )
        mensaje = respuesta.choices[0].message.content.strip()
        return f"{signos[signo]} {signo.upper()} – Horóscopo del Día\n✨ {mensaje}\n\n—\n📸 Síguenos en Instagram: @botanicayerberism"
    except Exception as e:
        logging.error(f"Error generando horóscopo para {signo}: {e}")
        return None

# Función programada diaria
def enviar_horoscopos():
    for signo in signos:
        texto = generar_horoscopo(signo)
        if texto:
            try:
                bot.send_message(chat_id=CHANNEL_ID, text=texto)
                logging.info(f"Publicado horóscopo de {signo}")
            except Exception as e:
                logging.error(f"Error enviando horóscopo de {signo}: {e}")

# Programador con zona horaria de Houston
scheduler = BlockingScheduler(timezone=pytz.timezone("America/Chicago"))
scheduler.add_job(enviar_horoscopos, 'cron', hour=7, minute=0)

if __name__ == "__main__":
    logging.info("Bot iniciado y esperando la hora programada...")
    scheduler.start()
