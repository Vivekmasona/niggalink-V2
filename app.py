from flask import Flask, request, Response
import subprocess

app = Flask(__name__)

@app.route('/stream', methods=['GET'])
def stream_audio():
    # Get the YouTube URL from query parameters
    video_url = request.args.get('url')
    if not video_url:
        return "Please provide a YouTube URL in the 'url' query parameter.", 400

    # yt-dlp command to extract and stream the best audio
    command = [
        'yt-dlp',
        '-f', 'bestaudio',  # Best audio format
        '-o', '-',          # Output to stdout
        video_url
    ]

    def generate():
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            while True:
                output = process.stdout.read(1024)
                if not output:
                    break
                yield output
        except GeneratorExit:
            process.terminate()
        finally:
            process.wait()

    # Set response headers for audio streaming
    return Response(generate(), content_type='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
