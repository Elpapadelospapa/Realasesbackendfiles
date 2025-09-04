from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ⭐ NUEVA IMPORTACIÓN
from telegram import Bot
import os

app = FastAPI()

# ⭐⭐ CONFIGURACIÓN CORS ⭐⭐
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desarrollo. En producción, usa tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "7924619096"

bot = Bot(token=BOT_TOKEN)

@app.post("/enviar-mensaje")
async def enviar_mensaje(mensaje: dict):
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"📩 Mensaje: {mensaje['texto']}"
        )
        return {"estado": "éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"mensaje": "Backend funcionando en Render"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)



