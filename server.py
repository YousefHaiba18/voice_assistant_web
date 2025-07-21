from flask import Flask, request, send_file, render_template_string
import whisper
import tempfile
import os
import asyncio
import edge_tts

app = Flask(__name__)
model = whisper.load_model("base")
VOICE = "en-US-AriaNeural"

@app.route("/")
def index():
    return render_template_string(open("static/index.html", encoding="utf-8").read())

@app.route("/upload", methods=["POST"])
def upload():
    if "audio" not in request.files:
        return "No audio", 400
    audio = request.files["audio"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio.save(temp_audio.name)
        result = model.transcribe(temp_audio.name)
        text = result["text"]
        print(f"Transcript: {text}")
        tts_path = asyncio.run(text_to_speech(text))
        return send_file(tts_path, mimetype="audio/mpeg")

async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    out_path = tempfile.mktemp(suffix=".mp3")
    await communicate.save(out_path)
    return out_path

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
