"""CLI entry point — delegates to downloader.py.

Usage:
    python3 download.py <youtube-url> [--mode audio|video] [--quality best|1080|720|480|360]
"""
import argparse

from downloader import run_download


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
        help="Quality/resolution (video only). Default: best",
    )
    args = parser.parse_args()
    print(f"Downloading {args.mode} ({args.quality}): {args.url}")
    run_download(args.url, mode=args.mode, quality=args.quality)


if __name__ == "__main__":
    main()
