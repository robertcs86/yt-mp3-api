import os
import subprocess
import tempfile
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing url"}), 400

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "%(title)s.%(ext)s")

        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--add-metadata",
            "-o", out,
            url
        ]

        subprocess.run(cmd, check=True)

        # troba l’mp3 generat
        for f in os.listdir(tmp):
            if f.endswith(".mp3"):
                return send_file(
                    os.path.join(tmp, f),
                    as_attachment=True
                )

    return jsonify({"error": "failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
