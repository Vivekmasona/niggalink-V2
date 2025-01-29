from flask import Flask, request, Response
import yt_dlp

app = Flask(__name__)

@app.route("/stream")
def stream_audio():
    youtube_url = request.args.get("url")
    if not youtube_url:
        return {"error": "No URL provided"}, 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            playback_url = info.get("url")

        if not playback_url:
            return {"error": "Failed to retrieve audio URL"}, 500

        def generate():
            with requests.get(playback_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=1024):
                    yield chunk

        return Response(generate(), content_type="audio/mpeg")

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
