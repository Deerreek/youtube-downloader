"""Flask web UI for the YouTube downloader."""
from flask import Flask, flash, redirect, render_template, request, url_for

from downloader import run_download

app = Flask(__name__)
app.secret_key = "yt-downloader-dev"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()
    mode = request.form.get("mode", "audio")
    quality = request.form.get("quality", "best")

    if not url:
        flash("Please enter a YouTube URL.", "error")
        return redirect(url_for("index"))

    try:
        run_download(url, mode=mode, quality=quality)
        flash(f"Downloaded successfully as {mode.upper()} ({quality}).", "success")
    except Exception as e:
        flash(f"Download failed: {e}", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
