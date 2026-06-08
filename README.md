# YouTube Downloader

A small project for downloading audio/video from YouTube — built incrementally as a way to learn `yt-dlp`, Flask, and git/GitHub along the way.

## v0.1 — Audio downloader (CLI)

Downloads the best available audio from a YouTube URL and saves it as an MP3 in `downloads/`.

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install yt-dlp flask certifi
```

Also requires, on the system (not in the venv):
- **ffmpeg** — for MP3 conversion (`brew install ffmpeg`)
- **deno** — JS runtime yt-dlp uses to solve YouTube's signature challenges (`brew install deno`)

You'll also need to be logged into YouTube in **Chrome**, since the script borrows
its cookies to get past YouTube's "confirm you're not a bot" check.

### Usage

```bash
python3 download.py <youtube-url>
```

The MP3 will be saved to `downloads/<video title>.mp3`.

## Roadmap

- v0.2 — Video downloads + format selection
- v0.3 — Web UI (Flask)
- v0.4 — Download history
- v0.5+ — Playlists, progress bars, tests, CI
