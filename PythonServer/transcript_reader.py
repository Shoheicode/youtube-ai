import json
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
import time
from datetime import timedelta
from dotenv import load_dotenv

video_id = "J9mfhqHK3hE"

# transcript = YouTubeTranscriptApi.get_transcript(video_id)

# full_transcript = "".join([t["text"] for t in transcript])

# print(full_transcript)

# Add to requirements.txt: openai==0.28.1

import openai

# load_dotenv()
# # Make sure to add OPENAI_API_KEY to your .env file
# OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
# openai.api_key = OPEN_AI_KEY


def extract_highlights_with_openai(transcript_text, person_name, num_highlights=5):
    load_dotenv()
    OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPEN_AI_KEY
    print(OPEN_AI_KEY)
    try:
        # Limit transcript length to avoid token limits
        truncated_transcript = (
            transcript_text[:8000] if len(transcript_text) > 8000 else transcript_text
        )

        prompt = f"""
        The following is a transcript from a video featuring {person_name}.
        Identify exactly {num_highlights} key moments from this transcript that includes this only person. IMPORTANT: Make sure to include their name in the summary. 
        
        For each highlight:
        1. Find an important statement or discussion point
        2. Extract the timestamp from the beginning of that section
        3. Write a brief 15-25 word summary of what's being discussed
        4. Make sure they are 20 second highlights
        
        Format your response as a JSON array with objects containing:
        - "timestamp": The timestamp in the format [HH:MM:SS] exactly as it appears in the transcript
        - "summary": Your brief summary of the highlight
        
        Example:
        [
          {{"timestamp": "[00:03:24]", "summary": "Discussion of portfolio diversification strategies in volatile markets"}},
          {{"timestamp": "[00:15:45]", "summary": "Analysis of current Federal Reserve policy and its impact on bond yields"}}
        ]
        Transcript:
        {transcript_text}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that analyzes video transcripts to find key moments.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()
        # print("RESPONSE", content)

        def fix_gpt_json(text):
            # Replace single quotes with double quotes
            text = re.sub(r"(?<!\\)'", "'", text)
            # Add quotes around unquoted keys (e.g. {title: → {"title":)
            text = re.sub(r"([{,]\s*)([a-zA-Z0-9_]+)(\s*:\s*)", r'\1"\2"\3', text)
            return text

        # Extract JSON from the response (in case there's additional text)
        json_match = re.search(r"\[.*\]", content, re.DOTALL)
        # print(json_match)
        if json_match:
            # print("HEYKJKJKJ")
            json_str = json_match.group(0)
            cleaned_json_str = fix_gpt_json(json_str)
            # print("CLEANED JSON", cleaned_json_str)
            cleaned_json_str = re.sub(r",\s*([\]}])", r"\1", cleaned_json_str)
            # print("CLEANED JSON", cleaned_json_str)
            highlights_data = json.loads(cleaned_json_str)
        else:
            # print("NO MATCH")
            # Try to parse the entire response as JSON
            highlights_data = json.loads(content)
        # print("EAAAAAAAAAAAA")
        # print("CONTENT", content)
        # print("HIGHLIGHTS DATA", highlights_data)
        highlights = []
        for highlight in highlights_data:
            # Convert timestamp to seconds
            timestamp_str = highlight["timestamp"].strip("[]")
            time_parts = timestamp_str.split(":")
            if len(time_parts) == 3:
                hours, minutes, seconds = map(int, time_parts)
                total_seconds = hours * 3600 + minutes * 60 + seconds
                highlights.append(
                    {
                        "startTime": total_seconds,
                        "endTime": total_seconds
                        + 20,  # Assuming each highlight is 20 seconds
                        "text": highlight["summary"],
                    }
                )
        # print("HIGHLIGHTS", highlights)
        return highlights  # Limit to num_highlights

    except Exception as e:
        print(f"Error using OpenAI for highlight extraction: {e}")
        return []


def format_transcript_for_analysis(transcript_list):
    if not transcript_list:
        return ""
    # Convert the transcript list into a single string for analysis
    formatted_transcript = ""
    # print("TRANSCRIPT LIST", transcript_list)
    for item in transcript_list:
        time_str = str(timedelta(seconds=int(item["start"])))
        formatted_transcript += f"{time_str}: {item['text']}\n"
    return formatted_transcript


# # Get video transcript
# try:
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
# except Exception as e:
#     print(f"Error fetching transcript: {e}")
#     transcript_list = None

# # Process transcript and extract highlights
# highlights = None

# if transcript_list:
#     appearances = []
#     # Format transcript for OpenAI
#     formatted_transcript = format_transcript_for_analysis(transcript_list)
#     print(formatted_transcript)

#     name = "Jimmy Butler"  # Example name, replace with actual name from query

#     # Try to extract highlights with OpenAI
#     if OPEN_AI_KEY:
#         highlights = extract_highlights_with_openai(
#             formatted_transcript,
#             name,  # Use just the name part
#             num_highlights=5,
#         )
#     if not highlights:
#         highlights = []

#     appearances.append(
#         {
#             "videoId": video_id,
#             "highlights": highlights,
#         }
#     )
