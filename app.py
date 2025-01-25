import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if necessary

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')  # URL of the video to download
    cookies_file = request.args.get('cookies')  # Path to cookies.txt file (optional)

    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    ydl_opts = {
        'format': 'best',  # You can specify the format you want to download
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output folder and filename template
        'noplaylist': True,  # Avoid downloading playlists (optional)
    }

    # If cookies file is provided, pass it to yt-dlp options
    if cookies_file:
        ydl_opts['cookies'] = cookies_file

    try:
        # Set up yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_url = info_dict.get('url', None)
            title = info_dict.get('title', None)

            # Return video download details
            return jsonify({
                'title': title,
                'url': video_url,
                'status': 'success'
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
