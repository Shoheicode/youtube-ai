import os
from multiprocessing import Pool, cpu_count
from faster_whisper import WhisperModel

from transcript_reader import extract_highlights_with_openai
from audio_to_transcript import audio_to_transcript_fast_whisper

# CONFIGS
AUDIO_DIR = "downloads"  # Folder with .mp3 or .wav files
MODEL_SIZE = "base"  # tiny, base, small, medium, large
USE_GPU = True  # Set to False to run on CPU
NUM_WORKERS = cpu_count()  # Number of parallel processes


# TRANSCRIBER FUNCTION
def transcribe_file(audio_path, name=""):
    # name = "Factor"
    transcript = audio_to_transcript_fast_whisper(audio_path)
    highlights = extract_highlights_with_openai(
        transcript,
        name,  # Use just the name part
        num_highlights=5,
    )
    return highlights


# MAIN: RUN WITH MULTIPROCESSING
if __name__ == "__main__":
    AUDIO_DIR = os.path.join(os.path.dirname(__file__), "downloads")
    audio_files = [
        os.path.join(AUDIO_DIR, f)
        for f in os.listdir(AUDIO_DIR)
        if f.endswith(".mp3") or f.endswith(".wav")
    ]

    print(audio_files)

    with Pool(processes=NUM_WORKERS) as pool:
        results = pool.map(transcribe_file, audio_files)

    for res in results:
        print(res)
