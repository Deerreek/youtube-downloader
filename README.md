# YouTube Downloader

A small project for downloading audio/video from YouTube — built incrementally as a way to learn `yt-dlp`, Flask, and git/GitHub along the way.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install yt-dlp flask certifi
```

Also requires on the system (not in the venv):
- **ffmpeg** — for MP3 conversion (`brew install ffmpeg`)
- **deno** — JS runtime yt-dlp uses to solve YouTube's signature challenges (`brew install deno`)

You'll also need to be logged into YouTube in **Chrome**, since the script borrows its cookies to get past YouTube's "confirm you're not a bot" check.

## Usage

### Web UI (recommended)

```bash
source venv/bin/activate
python3 app.py
# then open http://127.0.0.1:5000 in your browser
```

### CLI

```bash
# Download audio (MP3) — default
python3 download.py <youtube-url>

# Download video (MP4) at a specific quality
python3 download.py <youtube-url> --mode video --quality 720

# Available modes: audio, video
# Available qualities: best, 1080, 720, 480, 360
```

Output is saved to `downloads/<video title>.(mp3|mp4)`.

## Version history

| Version | Feature |
|---------|---------|
| v0.4 | Download history — JSON log shown in the web UI |
| v0.3 | Flask web UI |
| v0.2 | Video download + quality selection |
| v0.1 | Audio downloader (CLI) |

## Roadmap

- v0.5+ — Playlists, progress bars, tests, GitHub Actions CI
