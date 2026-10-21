import os
import uuid
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English", "ta": "Tamil", "hi": "Hindi", "te": "Telugu",
    "ml": "Malayalam", "kn": "Kannada", "bn": "Bengali", "mr": "Marathi",
    "gu": "Gujarati", "pa": "Punjabi", "de": "German", "fr": "French",
    "es": "Spanish", "it": "Italian", "pt": "Portuguese", "ja": "Japanese",
    "ko": "Korean", "zh-Hans": "Chinese (Simplified)", "ar": "Arabic", "ru": "Russian"
}

app.config["MAX_CONTENT_LENGTH"] = 20 * 1024


def azure_translate(text: str, source: str, target: str):
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    if not key or not region:
        return None

    params = {"api-version": "3.0", "to": target}
    if source and source != "auto":
        params["from"] = source
    url = endpoint.rstrip("/") + "/translate"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }
    response = requests.post(url, params=params, headers=headers, json=[{"text": text}], timeout=20)
    response.raise_for_status()
    data = response.json()
    return data[0]["translations"][0]["text"]


def mymemory_translate(text: str, source: str, target: str):
    # Keyless fallback for development/demo use. For production, configure Azure Translator.
    source_code = "auto" if source == "auto" else source
    pair = f"{source_code}|{target}"
    url = "https://api.mymemory.translated.net/get"
    response = requests.get(url, params={"q": text, "langpair": pair}, timeout=20)
    response.raise_for_status()
    data = response.json()
    if data.get("responseStatus") not in (200, "200"):
        raise RuntimeError(data.get("responseDetails", "Translation service error"))
    return data["responseData"]["translatedText"]


@app.get("/")
def home():
    return render_template("index.html", languages=LANGUAGES)


@app.post("/api/translate")
def translate():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    source = payload.get("source", "auto")
    target = payload.get("target", "en")

    if not text:
        return jsonify({"error": "Please enter some text to translate."}), 400
    if target == "auto":
        return jsonify({"error": "Target language cannot be Auto Detect."}), 400
    if source not in LANGUAGES or target not in LANGUAGES:
        return jsonify({"error": "Unsupported language selection."}), 400

    try:
        provider = "Microsoft Azure Translator"
        translated = azure_translate(text, source, target)
        if translated is None:
            provider = "MyMemory (demo fallback)"
            translated = mymemory_translate(text, source, target)
        return jsonify({"translated_text": translated, "provider": provider})
    except requests.RequestException as exc:
        return jsonify({"error": f"Translation service is unavailable: {exc}"}), 502
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.post("/api/speak")
def speak_note():
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
