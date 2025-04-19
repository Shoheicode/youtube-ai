import os
from multiprocessing import Pool, cpu_count
from faster_whisper import WhisperModel

from yt_audio_extractor import download_audio
from transcript_reader import extract_highlights_with_openai
from audio_to_transcript import audio_to_transcript_fast_whisper

# CONFIGS
AUDIO_DIR = "downloads"  # Folder with .mp3 or .wav files
MODEL_SIZE = "base"  # tiny, base, small, medium, large
USE_GPU = True  # Set to False to run on CPU
NUM_WORKERS = cpu_count()  # Number of parallel processes


# TRANSCRIBER FUNCTION
def transcribe_file(video_info, name=""):
    print(f"[START] {video_info['videoId']}")
    video_id = video_info["videoId"]
    # print(f"[{video_id}] Downloading...")
    video_id = video_info["videoId"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    filepath = f"audio_{video_id}"

    base_dir = os.path.dirname(__file__)
    out_path = os.path.join(base_dir, "downloads", name)
    os.makedirs(out_path, exist_ok=True)

    # print("Audio file path:", audio_path)
    print(f"[{video_id}] Downloading...")
    file_name = download_audio(video_url, output_path=out_path, filename=filepath)
    audio_path = os.path.join(out_path, f"{file_name}.mp3")

    print(f"[{video_id}] Transcribing...")
    transcript = audio_to_transcript_fast_whisper(audio_path)
    print(f"[{video_id}] Extracting highlights...")
    highlights = extract_highlights_with_openai(transcript, name, num_highlights=5)

    print("end")

    return {
        "videoId": video_id,
        "highlights": highlights,
        "title": video_info["title"],
        "channelTitle": video_info["channelTitle"],
        "publishedAt": video_info["publishedAt"],
    }


# MAIN: RUN WITH MULTIPROCESSING
# if __name__ == "__main__":
#     AUDIO_DIR = os.path.join(os.path.dirname(__file__), "downloads")
#     audio_files = [
#         os.path.join(AUDIO_DIR, f)
#         for f in os.listdir(AUDIO_DIR)
#         if f.endswith(".mp3") or f.endswith(".wav")
#     ]

#     print(audio_files)

#     with Pool(processes=NUM_WORKERS) as pool:
#         results = pool.map(transcribe_file, audio_files)

#     for res in results:
#         print(res)
