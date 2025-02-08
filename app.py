from fastapi import FastAPI, Query
from yt_dlp import YoutubeDL
import os

app = FastAPI()

# Directory to store downloaded files
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.get("/download")
async def download(url: str = Query(..., title="Video URL")):
    try:
        # Fixed filename for download
        video_filename = "video.mp4"
        video_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

        ydl_opts = {
            "cookiefile": "cookies.txt",
            "format": "bestvideo+bestaudio/best",
            "outtmpl": video_path,
            "merge_output_format": "mp4",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Return playback URL
        return {"url": f"/downloads/{video_filename}"}

    except Exception as e:
        return {"error": str(e)}
