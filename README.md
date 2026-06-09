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
# Download audio (MP3) — default
python3 download.py <youtube-url>

# Download video (MP4) at a specific quality
python3 download.py <youtube-url> --mode video --quality 720

# Available modes: audio, video
# Available qualities: best, 1080, 720, 480, 360
```

Output is saved to `downloads/<video title>.(mp3|mp4)`.

## v0.3 — Web UI ✓

A local Flask web app. Paste a URL, pick mode and quality, hit Download.

```bash
source venv/bin/activate
python3 app.py
# then open http://127.0.0.1:5000 in your browser
```

## v0.2 — Audio + video with quality selection ✓

Added `--mode` (audio/video) and `--quality` (best/1080/720/480/360) flags.

## Roadmap

- v0.4 — Download history
- v0.3 — Web UI (Flask)
- v0.4 — Download history
- v0.5+ — Playlists, progress bars, tests, CI
