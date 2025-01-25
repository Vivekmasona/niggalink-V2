from flask import Flask, request, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Use the /tmp directory for serverless environments like Vercel
OUTPUT_FOLDER = "/tmp/downloads"
COOKIES_PATH = "/tmp/cookies.txt"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Copy cookies.txt to /tmp during initialization
if os.path.exists("./cookies.txt"):
    with open("./cookies.txt", "r") as f:
        with open(COOKIES_PATH, "w") as tmp_f:
            tmp_f.write(f.read())

@app.route('/api/download', methods=['GET'])
def download_mp3():
    """
    API endpoint to download and convert a YouTube video to MP3.
    Accepts a YouTube URL, title, and artist as query parameters.
    """
    try:
        # Get parameters from request
        youtube_url = request.args.get('youtube_url')
        title = request.args.get('title')
        artist = request.args.get('artist')

        if not youtube_url:
            return jsonify({"error": "Missing YouTube URL"}), 400

        # Generate a unique ID for the file
        file_id = str(uuid.uuid4())
        output_template = os.path.join(OUTPUT_FOLDER, f"{file_id}.%(ext)s")
        mp3_file = os.path.join(OUTPUT_FOLDER, f"{file_id}.mp3")

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            },
            'cookiefile': COOKIES_PATH,  # Use cookies in /tmp
        }

        # Download and convert to MP3
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Response with success message and file details
        return jsonify({
            "success": True,
            "message": "Download successful",
            "file_name": f"{file_id}.mp3",
            "file_path": mp3_file,
            "title": title,
            "artist": artist
        }), 200

    except Exception as e:
        # Log error and respond with failure
        print(f"Error: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
