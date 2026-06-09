# YouTube Downloader

## Setup
Always activate the virtual environment before running anything:
```bash
source venv/bin/activate
```

## Run
```bash
python3 download.py <youtube-url>
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
- `SSL_CERT_FILE` is set inside `download.py` via certifi — do not remove this, macOS Python won't verify HTTPS otherwise
- Chrome cookies are borrowed at runtime via `cookiesfrombrowser: ("chrome",)` to bypass YouTube's bot-check — user must be logged into YouTube in Chrome
- `remote_components: ["ejs:github"]` lets yt-dlp fetch YouTube's JS challenge solver — required for format URLs to be accessible

## Project structure
```
download.py       # v0.1: CLI audio downloader
downloads/        # output folder — gitignored, created at runtime
venv/             # Python virtual environment — gitignored
```

## Versioning convention
Each version bump (v0.2, v0.3, ...) is developed on its own feature branch and merged into main via a pull request. See CHANGELOG.md for release notes.
