"""Core download logic shared by the CLI and the web UI."""
import os

import certifi

os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from yt_dlp import YoutubeDL

OUTPUT_DIR = "downloads"

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

    with YoutubeDL(options) as ydl:
        ydl.download([url])
