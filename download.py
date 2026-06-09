"""YouTube downloader — audio and video.

Usage:
    python3 download.py <youtube-url> [--mode audio|video] [--quality best|1080|720|480|360]

Defaults: --mode audio --quality best
"""
import argparse
import os
import sys

import certifi

# macOS's python.org builds don't ship a CA bundle, which makes yt-dlp's
# HTTPS requests fail with CERTIFICATE_VERIFY_FAILED. Point at certifi's.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from yt_dlp import YoutubeDL

OUTPUT_DIR = "downloads"

QUALITY_TO_FORMAT = {
    "best":  "bestvideo+bestaudio/best",
    "1080":  "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720":   "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480":   "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360":   "bestvideo[height<=360]+bestaudio/best[height<=360]",
}

SHARED_OPTIONS = {
    "outtmpl": f"{OUTPUT_DIR}/%(title)s.%(ext)s",
    "cookiesfrombrowser": ("chrome",),
    # Lets yt-dlp fetch YouTube's JS signature-challenge solver script,
    # required since YouTube started obfuscating audio/video URLs.
    "remote_components": ["ejs:github"],
}


def download_audio(quality: str) -> dict:
    return {
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


def download_video(quality: str) -> dict:
    return {
        **SHARED_OPTIONS,
        "format": QUALITY_TO_FORMAT.get(quality, QUALITY_TO_FORMAT["best"]),
        "merge_output_format": "mp4",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Download audio or video from YouTube.")
    parser.add_argument("url", help="YouTube URL to download")
    parser.add_argument(
        "--mode",
        choices=["audio", "video"],
        default="audio",
        help="Download as audio (MP3) or video (MP4). Default: audio",
    )
    parser.add_argument(
        "--quality",
        choices=["best", "1080", "720", "480", "360"],
        default="best",
        help="Quality/resolution. For audio this is ignored. Default: best",
    )
    args = parser.parse_args()

    if args.mode == "audio":
        options = download_audio(args.quality)
        print(f"Downloading audio (MP3): {args.url}")
    else:
        options = download_video(args.quality)
        print(f"Downloading video (MP4, {args.quality}p): {args.url}")

    with YoutubeDL(options) as ydl:
        ydl.download([args.url])


if __name__ == "__main__":
    main()
