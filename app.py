from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import boto3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# AWS S3 Configuration (Make sure to set up AWS credentials properly)
s3_client = boto3.client('s3', aws_access_key_id='YOUR_AWS_ACCESS_KEY', 
                         aws_secret_access_key='YOUR_AWS_SECRET_KEY', 
                         region_name='us-west-1')

BUCKET_NAME = 'your-s3-bucket-name'

# Function to download and extract information using yt-dlp
def download_video(url: str):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Where to save the file
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)  # Extracts info and downloads the video
        return info_dict  # Returns info dictionary containing video details

# Function to upload file to S3
def upload_to_s3(local_file_path: str, s3_key: str):
    try:
        s3_client.upload_file(local_file_path, BUCKET_NAME, s3_key)
        return f"File uploaded successfully to s3://{BUCKET_NAME}/{s3_key}"
    except Exception as e:
        return str(e)

# Endpoint to handle video extraction and uploading
@app.route('/extract', methods=['GET'])
def extract_video():
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'URL parameter is required.'}), 400
    
    try:
        # Download video info using yt-dlp
        video_info = download_video(url)
        video_title = video_info['title']
        video_file_path = f'downloads/{video_title}.mp4'  # Assuming video is saved as .mp4

        # Upload the video to S3 (if necessary)
        upload_response = upload_to_s3(video_file_path, f"videos/{video_title}.mp4")
        
        return jsonify({
            'title': video_title,
            'duration': video_info['duration'],
            'url': video_info['url'],
            'thumbnail': video_info.get('thumbnail', ''),
            'upload_to_s3': upload_response
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
