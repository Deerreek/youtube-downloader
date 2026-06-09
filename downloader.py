"""Core download logic shared by the CLI and the web UI."""
import json
import os
from datetime import datetime

import certifi

os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from yt_dlp import YoutubeDL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "downloads")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

QUALITY_TO_FORMAT = {
    "best": "bestvideo+bestaudio/best",
    "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720":  "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480":  "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360":  "bestvideo[height<=360]+bestaudio/best[height<=360]",
}

SHARED_OPTIONS = {
    "outtmpl": f"{OUTPUT_DIR}/%(title)s.%(ext)s",
    "cookiesfrombrowser": ("chrome",),
    "remote_components": ["ejs:github"],
}


def _append_history(entry: dict) -> None:
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    history.insert(0, entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE) as f:
        return json.load(f)


def run_download(url: str, mode: str = "audio", quality: str = "best") -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if mode == "audio":
        options = {
            **SHARED_OPTIONS,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    else:
        options = {
            **SHARED_OPTIONS,
            "format": QUALITY_TO_FORMAT.get(quality, QUALITY_TO_FORMAT["best"]),
            "merge_output_format": "mp4",
        }

    info = {}
    with YoutubeDL({**options, "quiet": False}) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        info = {
            "title": info_dict.get("title", url),
            "url": url,
        }

    _append_history({
        "title": info.get("title", url),
        "url": url,
        "mode": mode,
        "quality": quality,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
