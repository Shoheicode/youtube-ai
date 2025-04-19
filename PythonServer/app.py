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

        # filter videos for videos that are shorter than 10 mins
        filtered_videos = []
        for item in search_response["items"]:
            duration = parse_duration(
                item["contentDetails"]["duration"]
            ).total_seconds()
            print("DURATION", duration)
            if duration <= 600:  # 600 seconds = 10 minutes
                filtered_videos.append(
                    {
                        "title": item["snippet"]["title"],
                        "videoId": item["id"],
                        "duration_seconds": duration,
                    }
                )

        # STEP 2: Get video details
        items = search_response["items"]
        filteredList = []
        for item in items:
            title = item["snippet"]["title"]
            if re.search(rf"\b{re.escape(name)}\b", title, re.IGNORECASE):
                filteredList.append(item)
            if len(filteredList) >= 5:
                break

        if not filteredList:
            print("No videos found matching the name in the title.")
            return jsonify({"error": "An unexpected error occurred"}), 500

        # STEP 3: Get video details and transcript
        i = 0
        with open("count.txt", "r") as file:
            i = int(file.read().strip())
        print("I", i)
        for item in filteredList:
            video_id = item["id"]["videoId"]
            video_response = (
                youtube.videos()
                .list(
                    part="snippet,contentDetails,statistics",
                    id=video_id,
                )
                .execute()
            )
            # Check if video details were found
            if not video_response["items"]:
                print(f"No details found for video ID: {video_id}")
                return jsonify({"error": "An unexpected error occurred"}), 500

            # Get video details
            video_details = video_response["items"][0]

            # Process transcript and extract highlights
            highlights = None

            transcript_list = None

            # If transcript_list is not None, process it
            if transcript_list:
                # Format transcript for OpenAI
                formatted_transcript = format_transcript_for_analysis(transcript_list)
                # print(formatted_transcript)

                name = query.split(",")[
                    0
                ]  # Example name, replace with actual name from query

                # Try to extract highlights with OpenAI
                if OPEN_AI_KEY:
                    highlights = extract_highlights_with_openai(
                        formatted_transcript,
                        name,  # Use just the name part
                        num_highlights=5,
                    )
            else:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                na = "audio" + str(i)
                file_name = download_audio(
                    video_url, output_path="downloads", filename=na
                )
                path = f"downloads/{file_name}.mp3"
                transcript = audio_to_transcript_fast_whisper(path)
                # print(transcript)
                if OPEN_AI_KEY:
                    highlights = extract_highlights_with_openai(
                        transcript,
                        name,  # Use just the name part
                        num_highlights=5,
                    )

            if not highlights:
                highlights = []

            appearances.append(
                {
                    "videoId": video_id,
                    "title": video_details["snippet"]["title"],
                    "channelTitle": video_details["snippet"]["channelTitle"],
                    "publishedAt": video_details["snippet"]["publishedAt"],
                    "highlights": highlights,
                }
            )
            i += 1
        with open("count.txt", "w") as file:
            file.write(str(i))
        return jsonify({"query": query, "appearances": appearances})
    except HttpError as e:
        print("An error occurred:", e)
        return jsonify({"error": "Failed to fetch video details"}), 500
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
