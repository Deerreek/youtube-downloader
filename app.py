"""Flask web UI for the YouTube downloader."""
import json
import threading
import time
import uuid

from flask import Flask, Response, render_template, request

from downloader import load_history, run_download

app = Flask(__name__)
app.secret_key = "yt-downloader-dev"

# In-memory store: job_id -> {status, percent, message}
_jobs: dict = {}


@app.route("/")
def index():
    return render_template("index.html", history=load_history())


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()
    mode = request.form.get("mode", "audio")
    quality = request.form.get("quality", "best")

    if not url:
        return {"error": "Please enter a YouTube URL."}, 400

    job_id = str(uuid.uuid4())[:8]
    _jobs[job_id] = {"status": "starting", "percent": 0}

    def do_download():
        def hook(d):
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                downloaded = d.get("downloaded_bytes", 0)
                pct = int(downloaded / total * 100) if total else 0
                _jobs[job_id] = {"status": "downloading", "percent": pct}
            elif d["status"] == "finished":
                _jobs[job_id] = {"status": "processing", "percent": 99}

        try:
            run_download(url, mode=mode, quality=quality, progress_hook=hook)
            _jobs[job_id] = {"status": "done", "percent": 100}
        except Exception as e:
            _jobs[job_id] = {"status": "error", "percent": 0, "message": str(e)}

    threading.Thread(target=do_download, daemon=True).start()
    return {"job_id": job_id}


@app.route("/progress/<job_id>")
def progress(job_id):
    def stream():
        while True:
            data = _jobs.get(job_id, {"status": "unknown"})
            yield f"data: {json.dumps(data)}\n\n"
            if data.get("status") in ("done", "error"):
                _jobs.pop(job_id, None)
                break
            time.sleep(0.4)

    return Response(
        stream(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
