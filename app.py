from flask import Flask, request, jsonify
import yt_dlp
import requests
import os

app = Flask(__name__)

COOKIES_URL = "https://pastebin.com/raw/your_cookies"

def download_cookies():
    response = requests.get(COOKIES_URL)
    with open("cookies.txt", "w") as f:
        f.write(response.text)

@app.route("/stream")
def get_audio_info():
    youtube_url = request.args.get("url")
    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Agar local hai toh cookies.txt ka path specify karo
        cookie_path = "cookies.txt"

        if not os.path.exists(cookie_path):
            download_cookies()  # Read-Only server fix

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'cookiefile': cookie_path,  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
