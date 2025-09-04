from fastapi import FastAPI, HTTPException
from telegram import Bot
import os

app = FastAPI()

# Solo el BOT_TOKEN en variables de entorno
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

# Chat ID hardcodeado (pero puedes cambiarlo según tu necesidad)
CHAT_ID = "7924619096"  # Reemplaza con TU chat ID real

@app.post("/enviar-mensaje")
async def enviar_mensaje(mensaje: dict):
    try:
        await bot.send_message(
            chat_id=CHAT_ID,  # 🛡️ Ahora está en el código, no en variables
            text=f"📩 Mensaje: {mensaje['texto']}"
        )
        return {"estado": "éxito", "mensaje": "Mensaje enviado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():

    return {"mensaje": "Backend funcionando en Railway"}
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


