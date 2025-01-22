
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import re
import logging
from werkzeug.utils import secure_filename
import tempfile  # Add this import

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Replace invalid file characters
    filename = re.sub(r'[^\x00-\x7F]+', '_', filename)  # Replace non-ASCII characters
    filename = filename.replace(' ', '_')  # Replace spaces with underscores
    return filename

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.json.get('url')

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Create a temporary directory for downloads
        with tempfile.TemporaryDirectory() as temp_dir:
            # Configure yt-dlp options with temporary directory
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'quiet': True,
                'restrictfilenames': True,
            }

            # Create a yt-dlp object
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get('title', 'video')
                video_ext = info.get('ext', 'mp4')
                video_filename = sanitize_filename(f"{video_title}.{video_ext}")
                full_path = os.path.join(temp_dir, video_filename)

                # Log the downloaded file
                app.logger.debug(f"Downloaded file: {full_path}")

                # Check if the file exists
                if not os.path.exists(full_path):
                    app.logger.error(f"File not found: {full_path}")
                    return jsonify({"error": "File not found on server."}), 404

                # Serve the file directly instead of saving it
                return send_file(
                    full_path,
                    as_attachment=True,
                    download_name=video_filename,
                    mimetype='video/mp4'
                )

    except yt_dlp.utils.DownloadError as e:
        app.logger.error(f"DownloadError: {e}")
        return jsonify({"error": "The file wasn't available on the site."}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

# Remove the download-file route as it's no longer needed

# Remove the downloads directory creation as we're using temporary storage

app = app.wsgi_app  # Add this line for Vercel deployment