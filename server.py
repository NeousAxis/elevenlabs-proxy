from flask import Flask, request, send_file, jsonify
import requests
import uuid
import os

app = Flask(__name__)

API_KEY = os.environ.get("ELEVEN_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Josh

@app.route('/generate-mp3', methods=['POST'])
def generate_mp3():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400

        eleven_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
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

        response = requests.post(eleven_url, headers=headers, json=body)

        if response.status_code == 200:
            filename = f"output_{uuid.uuid4().hex}.mp3"
            filepath = f"/tmp/{filename}"
            with open(filepath, "wb") as f:
                f.write(response.content)
            return send_file(filepath, mimetype="audio/mpeg")
        else:
            return jsonify({"error": "Failed to fetch from ElevenLabs", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "exception": str(e)}), 500

@app.route('/')
def index():
    return "Proxy is up"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
