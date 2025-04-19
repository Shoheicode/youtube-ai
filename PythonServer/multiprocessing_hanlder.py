import os
from multiprocessing import Pool, cpu_count
from faster_whisper import WhisperModel

# CONFIGS
AUDIO_DIR = "audio_files"  # Folder with .mp3 or .wav files
MODEL_SIZE = "base"  # tiny, base, small, medium, large
USE_GPU = True  # Set to False to run on CPU
NUM_WORKERS = cpu_count()  # Number of parallel processes


# TRANSCRIBER FUNCTION
def transcribe_file(audio_path):
    print(f"Processing: {audio_path}")

    # Load model inside the worker to avoid shared memory issues
    model = WhisperModel(
        MODEL_SIZE,
        device="cuda" if USE_GPU else "cpu",
        compute_type="float16" if USE_GPU else "int8",
    )

    segments, _ = model.transcribe(audio_path, beam_size=1)
    result = "\n".join([seg.text for seg in segments])

    output_path = audio_path + ".txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    return f"Finished: {audio_path}"


# MAIN: RUN WITH MULTIPROCESSING
if __name__ == "__main__":
    audio_files = [
        os.path.join(AUDIO_DIR, f)
        for f in os.listdir(AUDIO_DIR)
        if f.endswith(".mp3") or f.endswith(".wav")
    ]

    with Pool(processes=NUM_WORKERS) as pool:
        results = pool.map(transcribe_file, audio_files)

    for res in results:
        print(res)
