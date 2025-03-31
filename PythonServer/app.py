from flask import Flask, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    filename = video.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    video.save(filepath)

    return jsonify({"message": f'Video "{filename}" uploaded successfully!'})
