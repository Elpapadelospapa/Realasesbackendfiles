from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from telegram import Bot
import os

app = FastAPI()

# ✅ Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Token SEGURO en variables de entorno
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ ERROR: BOT_TOKEN no está configurado")

bot = Bot(token=BOT_TOKEN)

@app.post("/enviar-mensaje")
async def enviar_mensaje(mensaje: dict):
    try:
        # ✅ Recibe CHAT_ID desde el frontend
        await bot.send_message(
            chat_id=mensaje["chat_id"],
            text=f"📩 Mensaje: {mensaje['texto']}"
        )
        return {"estado": "éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"mensaje": "Backend funcionando"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
