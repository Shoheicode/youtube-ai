import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generate_simulated_highlights(video_id):
    # In a real application, these would be generated based on actual video content analysis
    simulated_highlights = [
        {
            "startTime": 120,  # 2 minutes in
            "endTime": 140,  # 20 second clip
            "text": "Discussing current market conditions and their impact on investment strategies.",
        },
        {
            "startTime": 360,  # 6 minutes in
            "endTime": 380,  # 20 second clip
            "text": "Explaining the concept of risk assessment in today's economic environment.",
        },
        {
            "startTime": 780,  # 13 minutes in
            "endTime": 800,  # 20 second clip
            "text": "Sharing personal insights on successful long-term investment approaches.",
        },
        {
            "startTime": 1200,  # 20 minutes in
            "endTime": 1220,  # 20 second clip
            "text": "Answering questions about emerging market opportunities and potential risks.",
        },
        {
            "startTime": 1800,  # 30 minutes in
            "endTime": 1820,  # 20 second clip
            "text": "Concluding with key takeaways for investors to consider in the coming months.",
        },
    ]

    # Return a subset of the highlights (random number between 3 and 5)
    num_highlights = random.randint(3, 5)
    return simulated_highlights[:num_highlights]


@app.route("/upload", methods=["POST"])
def upload_video():
    data = request.get_json()
    print(data)

    # Check if the request contains JSON data
    if not data or "query" not in data or not data["query"]:
        return jsonify({"error": "Query is required"}), 400

    query = data["query"]

    print("Query received:", query)
    appearances = []
    a = {
        "videoId": query,
        "title": "Sample Video Title",
        "channelTitle": "Sample Channel",
        "publishedAt": "url",
        "highlights": generate_simulated_highlights("video_id"),
    }
    appearances.append(a)
    print("APPEARENCES", appearances)
    return jsonify({"appearances": appearances})

    # if "video" not in request.files:
    #     print("NOT WORKING")
    #     return jsonify({"error": "No video file provided"}), 400

    # video = request.files["video"]
    # filename = video.filename
    # filepath = os.path.join(UPLOAD_FOLDER, filename)
    # video.save(filepath)

    # print("Video saved to:", filepath)

    # return jsonify({"message": f'Video "{filename}" uploaded successfully!'})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
