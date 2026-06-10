# YouTube Downloader

## Setup
Always activate the virtual environment before running anything:
```bash
source venv/bin/activate
```

## Run
```bash
# Web UI (recommended)
python3 app.py
# then open http://127.0.0.1:5000

# CLI — Audio (MP3, default)
python3 download.py <youtube-url>

# CLI — Video (MP4) at specific quality
python3 download.py <youtube-url> --mode video --quality 720
```

## Stack
- **Python 3.12** inside a local `venv/`
- **yt-dlp** — handles all YouTube extraction and downloading
- **Flask** — will power the web UI (v0.3+)
- **certifi** — provides the CA certificate bundle (fixes macOS SSL errors)
- **ffmpeg** (system, via Homebrew) — converts audio to MP3
- **deno** (system, via Homebrew) — JS runtime yt-dlp needs to solve YouTube's signature challenges

## System requirements
Both must be installed on the system (not in the venv):
```bash
brew install ffmpeg deno
```

## Key quirks
- `SSL_CERT_FILE` is set inside `downloader.py` via certifi — do not remove this, macOS Python won't verify HTTPS otherwise
- Chrome cookies are borrowed at runtime via `cookiesfrombrowser: ("chrome",)` to bypass YouTube's bot-check — user must be logged into YouTube in Chrome
- `remote_components: ["ejs:github"]` lets yt-dlp fetch YouTube's JS challenge solver — required for format URLs to be accessible

## Testing
```bash
pytest
```
Tests are offline (no real YouTube calls) and run automatically on every push via GitHub Actions (`.github/workflows/test.yml`).

## Project structure
```
app.py                    # Flask web UI + SSE progress endpoint
downloader.py             # shared download + history logic (used by CLI and web UI)
download.py               # CLI entry point
templates/
  index.html              # web form + history table
tests/                    # pytest test suite
.github/workflows/test.yml # CI: runs pytest on every push
downloads/                # output folder — gitignored, created at runtime
history.json              # download history log — gitignored, created at runtime
venv/                     # Python virtual environment — gitignored
```

## Versioning convention
Each version bump (v0.2, v0.3, ...) is developed on its own feature branch and merged into main via a pull request. Notable versions are tagged and released via `gh release create`. See README.md's version history table for release notes.
