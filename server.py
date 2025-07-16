from flask import Flask, request, send_file, jsonify
import requests
import uuid
import os

app = Flask(__name__)

# Clé API ElevenLabs récupérée via Render > Environment Variables
API_KEY = os.environ.get("ELEVEN_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Voix par défaut (Josh)

@app.route('/generate-mp3', methods=['POST'])
def generate_mp3():
    data = request.get_json()
    text = data.get("text")

    if not text:
        print("❌ Erreur : champ 'text' manquant ou vide")
        return jsonify({"error": "No text provided"}), 400

    print(f"📨 Texte reçu : {text}")
    print(f"🔐 Clé API présente : {bool(API_KEY)}")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        print(f"🔄 Status ElevenLabs : {response.status_code}")
        print(f"📦 Réponse ElevenLabs : {response.text[:300]}")

        if response.status_code == 200:
            filename = f"output_{uuid.uuid4().hex}.mp3"
            filepath = f"/tmp/{filename}"
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ Fichier enregistré : {filepath}")
            return send_file(filepath, mimetype="audio/mpeg")
        else:
            return jsonify({
                "error": response.status_code,
                "message": response.text
            }), 500
    except Exception as e:
        print(f"🔥 Exception serveur : {str(e)}")
        return jsonify({"error": "Server exception", "message": str(e)}), 500

@app.route('/')
def home():
    return "✅ Proxy ElevenLabs actif."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
