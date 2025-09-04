# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde tu frontend

# Obtener el token directamente del entorno de Render
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Verifica que el token esté definido
if not BOT_TOKEN:
    raise RuntimeError("Error: La variable de entorno BOT_TOKEN no está definida en Render.")

@app.route('/api/send-telegram-message', methods=['POST'])
def send_telegram_message():
    try:
        # Obtiene el mensaje y el chat_id del cuerpo de la solicitud JSON del frontend
        data = request.json
        message = data.get('message')
        chat_id = data.get('chat_id')

        if not message or not chat_id:
            return jsonify({"error": "Faltan parámetros: 'message' y 'chat_id' son requeridos."}), 400

        # Construye la URL de la API de Telegram
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        # Prepara la carga útil (payload) para la solicitud
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        # Envía la solicitud a la API de Telegram
        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()

        print("Mensaje enviado a Telegram correctamente.")
        return jsonify({"success": True, "message": "Mensaje enviado."}), 200

    except requests.exceptions.RequestException as e:
        print(f"Error al enviar mensaje a Telegram: {e}")
        return jsonify({"success": False, "error": "Error al comunicarse con la API de Telegram."}), 500
    except Exception as e:
        print(f"Error interno del servidor: {e}")
        return jsonify({"success": False, "error": "Error interno del servidor."}), 500

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

