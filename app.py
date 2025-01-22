from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import yt_dlp
import os
import re
import logging
import tempfile

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'[^\x00-\x7F]+', '_', filename)
    filename = filename.replace(' ', '_')
    return filename

@app.route('/')
def index():
    # Inline HTML template for simplicity
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Downloader</title>
    </head>
    <body>
        <h1>Download Video</h1>
        <form id="downloadForm" method="post" action="/download">
            <label for="url">Video URL:</label><br>
            <input type="url" id="url" name="url" required><br><br>
            <button type="submit">Download</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'quiet': True,
                'restrictfilenames': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get('title', 'audio')
                video_ext = info.get('ext', 'mp3')
                video_filename = sanitize_filename(f"{video_title}.{video_ext}")
                full_path = os.path.join(temp_dir, video_filename)

                if not os.path.exists(full_path):
                    return jsonify({"error": "File not found on server."}), 404

                return send_file(
                    full_path,
                    as_attachment=True,
                    download_name=video_filename,
                    mimetype='audio/mp3'
                )

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": "The file wasn't available on the site."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app = app.wsgi_app
