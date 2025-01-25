from flask import Flask, request, jsonify
import requests
import re
from typing import Optional


app = Flask(__name__)

# Dummy function to simulate data extraction
def extract_snapchat_spotlight_data(url: str) -> dict:
    # Your extraction logic here, based on the SnapchatSpotlightIE class
    # For now, returning dummy data (replace this with the real logic)
    
    video_data = {
        'id': 'W7_EDlXWTBiXAEEniNoMPwAAYYWtidGhudGZpAX1TKn0JAX1TKnXJAAAAAA',
        'ext': 'mp4',
        'title': 'Views 💕',
        'description': '',
        'thumbnail': 'https://cf-st.sc-cdn.net/d/kKJHIR1QAznRKK9jgYYDq.256.IRZXSOY',
        'duration': 4.665,
        'timestamp': 1637777831.369,
        'upload_date': '20211124',
        'repost_count': 50,
        'uploader': 'shreypatel57',
        'uploader_url': 'https://www.snapchat.com/add/shreypatel57',
    }

    return video_data

# Flask route to handle the GET request
@app.route('/extract', methods=['GET'])
def extract():
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'URL parameter is required.'}), 400
    
    try:
        # Simulate the extraction process
        video_data = extract_snapchat_spotlight_data(url)
        
        # Return the extracted video data as JSON
        return jsonify(video_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
