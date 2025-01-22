from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/extract', methods=['GET'])
def extract_audio_info():
    youtube_url = request.args.get('url')
    
    if youtube_url:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(youtube_url, download=False)
                playback_url = info_dict.get('url', None)
                title = info_dict.get('title', 'Unknown Title')
            
            if playback_url:
                return jsonify({
                    "status": "success",
                    "title": title,
                    "playback_url": playback_url
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Could not retrieve playback URL"
                }), 400
        except Exception as e:
            logging.error(f"Error extracting info: {e}")
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    else:
        return jsonify({
            "status": "error",
            "message": "No URL provided. Use '?url=YOUTUBE_URL' in the query."
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
