from fastapi import FastAPI, Query
import yt_dlp
import requests
import os

app = FastAPI()

# YouTube API Key (Render Environment Variable me set karo)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube_api(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY
    }
    res = requests.get(url, params=params).json()
    if "items" in res and res["items"]:
        video = res["items"][0]
        return video["id"]["videoId"], video["snippet"]["title"], video["snippet"]["thumbnails"]["high"]["url"]

def get_audio_url(video_id):
    ydl_opts = {"format": "bestaudio", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
        return info["url"]

@app.get("/search")
def search_song(title: str = Query(...)):
    video_id, title, thumbnail = search_youtube_api(title)
    audio_url = get_audio_url(video_id)
    return {
        "results": [{
            "title": title,
            "url": audio_url,
            "videoId": video_id,
            "thumbnail": thumbnail
        }]
  }
