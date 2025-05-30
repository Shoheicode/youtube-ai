from multiprocessing import Pool, cpu_count
import random
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from isoduration import parse_duration
from youtube_transcript_api import YouTubeTranscriptApi

import os

import openai

from multiprocessing_hanlder import transcribe_file
from audio_to_transcript import audio_to_transcript_fast_whisper
from yt_audio_extractor import download_audio
from transcript_reader import (
    extract_highlights_with_openai,
    format_transcript_for_analysis,
)

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable not set.")
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPEN_AI_KEY
AUDIO_DIR = "downloads"  # Folder with .mp3 or .wav files
MODEL_SIZE = "base"  # tiny, base, small, medium, large
USE_GPU = True  # Set to False to run on CPU
NUM_WORKERS = cpu_count()  # Number of parallel processes

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend


def get_youtube_service():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_video():
    data = request.get_json()
    appearances = []

    # Check if the request contains JSON data
    if not data or "query" not in data or not data["query"]:
        return jsonify({"error": "Query is required"}), 400

    # Extract the query from the request data
    query = data["query"]
    name = query.split(",")[0]

    try:
        # STEP 1: Search for videos
        youtube = get_youtube_service()
        search_response = (
            youtube.search()
            .list(
                q=query,
                type="video",
                part="id,snippet",
                maxResults=50,
                order="date",
                videoDuration="medium",
                relevanceLanguage="en",
                regionCode="US",
            )
            .execute()
        )

        # Check if any videos were found
        if not search_response["items"]:
            print("No videos found matching the search criteria.")
            return []

        video_ids = [item["id"]["videoId"] for item in search_response["items"]]

        # Get video details (to extract exact duration)
        video_response = (
            youtube.videos()
            .list(part="snippet,contentDetails", id=",".join(video_ids))
            .execute()
        )

        # STEP 3: Filter videos by duration AND name in title
        filteredList = []
        for item in video_response["items"]:
            video_id = item["id"]
            title = item["snippet"]["title"]
            # print(item)
            if "duration" not in item["contentDetails"]:
                print("No duration found for video ID:", video_id)
                continue
            duration = parse_duration(item["contentDetails"]["duration"])
            # print(duration)
            # print(duration.time)
            total_seconds = (
                duration.time.minutes * 60
                + duration.time.hours * 60 * 60
                + duration.time.seconds
            )

            # print("DURATION", total_seconds, "TITLE", title)

            if total_seconds <= 600 and re.search(
                rf"\b{re.escape(name)}\b", title, re.IGNORECASE
            ):
                filteredList.append(item)
                if len(filteredList) >= 5:
                    break

        if not filteredList:
            print("No videos found matching the name in the title.")
            return jsonify({"error": "An unexpected error occurred"}), 500

        # STEP 3: Get video details and transcript
        ct = 0
        base_dir = os.path.dirname(__file__)
        count_path = os.path.join(base_dir, "count.txt")

        with open(count_path, "r") as file:
            ct = int(file.read().strip())
        # print("I", ct)

        video_info_list = [
            {
                "videoId": item["id"],
                "title": item["snippet"]["title"],
                "channelTitle": item["snippet"]["channelTitle"],
                "publishedAt": item["snippet"]["publishedAt"],
            }
            for item in filteredList
        ]

        args = [(info, name) for info in video_info_list]

        with Pool(processes=2) as pool:
            appearances = pool.starmap(transcribe_file, args)

        # for item in filteredList:
        #     # print("hi")
        #     print(item)
        #     video_id = item["id"]
        #     # print("Hi")
        #     # Check if video details were found
        #     if not video_response["items"]:
        #         print(f"No details found for video ID: {video_id}")
        #         return jsonify({"error": "An unexpected error occurred"}), 500

        #     # Get video details
        #     video_details = item

        #     # Process transcript and extract highlights
        #     highlights = None

        #     transcript_list = None

        #     # If transcript_list is not None, process it
        #     if transcript_list:
        #         # Format transcript for OpenAI
        #         formatted_transcript = format_transcript_for_analysis(transcript_list)
        #         # print(formatted_transcript)

        #         name = query.split(",")[
        #             0
        #         ]  # Example name, replace with actual name from query

        #         # Try to extract highlights with OpenAI
        #         if OPEN_AI_KEY:
        #             highlights = extract_highlights_with_openai(
        #                 formatted_transcript,
        #                 name,  # Use just the name part
        #                 num_highlights=5,
        #             )
        #     else:
        #         video_url = f"https://www.youtube.com/watch?v={video_id}"
        #         filepath = "audio" + str(ct)
        #         base_dir = os.path.dirname(__file__)
        #         out_path = os.path.join(base_dir, "downloads", name)
        #         file_name = download_audio(
        #             video_url, output_path=out_path, filename=filepath
        #         )
        #         path = f"downloads/{name}/{file_name}.mp3"
        #         appearances.append(
        #             {
        #                 "videoId": video_id,
        #                 "title": video_details["snippet"]["title"],
        #                 "channelTitle": video_details["snippet"]["channelTitle"],
        #                 "publishedAt": video_details["snippet"]["publishedAt"],
        #                 # "highlights": highlights,
        #             }
        #         )
        #         ct += 1
        # print("APPEARANCES", appearances)
        # AUDIO_DIR = os.path.join(os.path.dirname(__file__), f"downloads/{name}/")
        # audio_files = [
        #     os.path.join(AUDIO_DIR, f)
        #     for f in os.listdir(AUDIO_DIR)
        #     if f.endswith(".mp3") or f.endswith(".wav")
        # ]

        # print("POOL PARTY")
        # args = [(file, name) for file in audio_files]
        # with Pool(processes=NUM_WORKERS) as pool:
        #     results = pool.starmap(transcribe_file, args)

        # print("RESULTS:")
        # for res in results:
        #     print(res)

        # highlights = results

        # if not highlights:
        #     highlights = []

        # for i in range(len(appearances)):
        #     appearances[i]["highlights"] = highlights[i]

        base_dir = os.path.dirname(__file__)
        count_path = os.path.join(base_dir, "count.txt")

        with open(count_path, "w") as file:
            file.write(str(ct))
        return jsonify({"query": query, "appearances": appearances})
    except HttpError as e:
        print("An error occurred:", e)
        return jsonify({"error": "Failed to fetch video details"}), 500
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
