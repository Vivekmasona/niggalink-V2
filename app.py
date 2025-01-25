from flask import Blueprint, request, jsonify, send_file
import yt_dlp
import os
import uuid
from models.playlist import Playlist
from models.base_model import BaseModel

download_blueprint = Blueprint('apps', __name__, url_prefix='/api')

OUTPUT_FOLDER = "./downloads"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@download_blueprint.route('/download', methods=['GET'])
def download_mp3():
    """
    API endpoint to download and convert a YouTube video to MP3.
    Accepts a YouTube URL, judul, and artis as query parameters.
    """
    try:
        # Get the YouTube URL and metadata from query parameters
        youtube_url = request.args.get('youtube_url')
        judul = request.args.get('judul')
        artis = request.args.get('artis')
        if not youtube_url:
            return jsonify({"error": "Missing YouTube URL"}), 400

        # Generate a unique file ID
        file_id = str(uuid.uuid4())
        output_template = os.path.join(OUTPUT_FOLDER, f"{file_id}.%(ext)s")
        mp3_file = os.path.join(OUTPUT_FOLDER, f"{file_id}.mp3")

        # yt-dlp options with cookie support
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
            'cookiefile': './cookies.txt',  # Specify the cookie file
            'ffmpeg_location': '/usr/bin/ffmpeg',  # Update this if FFmpeg is in a different path
        }

        # Download and convert video to MP3
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Save metadata in the database
        with BaseModel.db.transaction():
            playlist = Playlist()
            playlist.genre_id = 0
            playlist.judul = judul
            playlist.artis = artis
            playlist.file_name = f"{file_id}.mp3"
            playlist.url_path = mp3_file
            playlist.save()

        # Serve the MP3 file as a response
        return send_file(mp3_file, as_attachment=True, download_name=f"{judul or file_id}.mp3")

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
