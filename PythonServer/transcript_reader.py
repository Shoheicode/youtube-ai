import os
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "J9mfhqHK3hE"

# transcript = YouTubeTranscriptApi.get_transcript(video_id)

# full_transcript = "".join([t["text"] for t in transcript])

# print(full_transcript)

# Add to requirements.txt: openai==0.28.1

import openai

# Make sure to add OPENAI_API_KEY to your .env file
openai.api_key = os.getenv("CHATGPT_API_KEY")


def extract_highlights_with_openai(transcript, person_name, num_highlights=5):
    try:
        prompt = f"""
        The following is a transcript from a video featuring {person_name}.
        Please identify the {num_highlights} most important points or moments from this transcript.
        For each highlight, provide:
        1. A brief description (20-30 words)
        2. The approximate timestamp where this highlight begins
        
        Transcript:
        {transcript[:4000]}  # Limit to avoid token limits
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
        )

        # Process the response to convert it into highlights
        # This would need custom parsing of the GPT response
        return parse_openai_response_to_highlights(
            response.choices[0].message["content"]
        )
    except Exception as e:
        print(f"Error using OpenAI for highlight extraction: {e}")
        return []


def format_transcript_for_analysis(transcript_list):
    if not transcript_list:
        return ""
    # Convert the transcript list into a single string for analysis
    formatted_transcript = ""
    for entry in transcript_list:
        formatted_transcript += f"{entry['start']} - {entry['text']} "
    return formatted_transcript


# Get video transcript
try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
except Exception as e:
    print(f"Error fetching transcript: {e}")
    transcript_list = None

# Process transcript and extract highlights
highlights = None

if transcript_list:
    # Format transcript for OpenAI
    formatted_transcript = format_transcript_for_analysis(transcript_list)

    # Try to extract highlights with OpenAI
    if OPENAI_API_KEY:
        highlights = extract_highlights_with_openai(
            formatted_transcript,
            query.split(",")[0],  # Use just the name part
            num_highlights=3,
        )
