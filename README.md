# YouTube Downloader

![Tests](https://github.com/Deerreek/youtube-downloader/actions/workflows/test.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

A small local tool for downloading audio/video from YouTube — paste a URL, pick audio (MP3) or video (MP4), and watch it download with a live progress bar. Built incrementally as a personal project to learn `yt-dlp`, Flask, and git/GitHub.

> **For personal use only.** Only download videos you have the right to download (e.g. your own content, Creative Commons, or for personal offline viewing per YouTube's terms). Respect copyright.

## Requirements

- **macOS** (the setup commands below use Homebrew; other platforms may need different steps for ffmpeg/deno)
- Python 3.10+
- Google Chrome, logged into YouTube (the app borrows its cookies to get past YouTube's bot-check)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
brew install ffmpeg deno
```

- **ffmpeg** — converts/merges audio and video
- **deno** — JS runtime yt-dlp uses to solve YouTube's signature challenges

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

## Troubleshooting

- **SSL: CERTIFICATE_VERIFY_FAILED** — make sure `certifi` installed correctly (`pip install -r requirements.txt`); the app sets `SSL_CERT_FILE` automatically.
- **"Sign in to confirm you're not a bot"** — make sure you're logged into YouTube in Chrome. The app reuses that session.
- **"Requested format is not available"** — make sure `deno` is installed (`brew install deno`) and on your `PATH`.

## Testing

```bash
pytest
```

Tests cover the history log and the Flask routes — they don't hit YouTube, so they run fast and offline. They run automatically on every push via GitHub Actions (see badge above).

## Version history

| Version | Feature |
|---------|---------|
| v0.7 | Public release prep — LICENSE, troubleshooting docs |
| v0.6 | Tests + GitHub Actions CI |
| v0.5 | Real-time download progress bar |
| v0.4 | Download history — JSON log shown in the web UI |
| v0.3 | Flask web UI |
| v0.2 | Video download + quality selection |
| v0.1 | Audio downloader (CLI) |

## License

[MIT](LICENSE)
