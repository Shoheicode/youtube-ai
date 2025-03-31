from flask import Flask, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_video():
    data = request.get_json()
    print(data)

    # Check if the request contains JSON data
    if not data or 'query' not in data or not data['query']:
        return jsonify({"error": "Query is required"}), 400

    query = data['query']

    print("Query received:", query)
    return jsonify({"message": f"Query '{query}' received successfully!"})

    # if "video" not in request.files:
    #     print("NOT WORKING")
    #     return jsonify({"error": "No video file provided"}), 400

    # video = request.files["video"]
    # filename = video.filename
    # filepath = os.path.join(UPLOAD_FOLDER, filename)
    # video.save(filepath)

    # print("Video saved to:", filepath)

    # return jsonify({"message": f'Video "{filename}" uploaded successfully!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)