from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/stream")
def get_audio_info():
    youtube_url = request.args.get("url")
    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'cookiefile': 'cookies.txt',  # Add your cookies file path here
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
