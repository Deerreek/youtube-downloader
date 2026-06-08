"""v0.1: Download a YouTube video's audio as an MP3.

Usage:
    python3 download.py <youtube-url>
"""
import os
import sys

import certifi

# macOS's python.org builds don't ship a CA bundle, which makes yt-dlp's
# HTTPS requests fail with CERTIFICATE_VERIFY_FAILED. Point at certifi's.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from yt_dlp import YoutubeDL

OUTPUT_DIR = "downloads"


def download_audio(url: str) -> None:
    options = {
        "format": "bestaudio/best",
        "outtmpl": f"{OUTPUT_DIR}/%(title)s.%(ext)s",
        # Borrow cookies from Chrome so YouTube treats us as a logged-in
        # browser instead of triggering its "confirm you're not a bot" check.
        "cookiesfrombrowser": ("chrome",),
        # Lets yt-dlp fetch YouTube's JS signature-challenge solver script,
        # required since YouTube started obfuscating audio/video URLs.
        "remote_components": ["ejs:github"],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 download.py <youtube-url>")
        sys.exit(1)

    download_audio(sys.argv[1])


if __name__ == "__main__":
    main()
