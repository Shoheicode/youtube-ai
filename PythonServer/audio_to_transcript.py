from faster_whisper import WhisperModel
import whisper
import subprocess
import time

# Load model (options: tiny, base, small, medium, large)
# model = whisper.load_model("medium")


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"


def audio_to_transcript_whisper(audio_file):
    """
    Convert audio to transcript using Whisper model.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        str: Transcript of the audio.
    """
    # Load the Whisper model
    model = whisper.load_model("medium")

    # Transcribe the audio file
    result = model.transcribe(audio_file, word_timestamps=True)

    output_string = ""

    # Access segments with timestamps
    for segment in result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        output_string += f"[{start_time:.2f}s -> {end_time:.2f}s] {text}\n"
        # print(f"[{format_time(start_time)} --> {format_time(end_time)}] {text}")

    # Extract and return the transcript
    return output_string


def audio_to_transcript_fast_whisper(audio_file):
    """
    Convert audio to transcript using Whisper model.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        str: Transcript of the audio.
    """
    # Choose model: tiny, base, small, medium, large-v2
    model_size = "medium"

    # Set compute_type to "int8" for max speed on CPU, or "float16" for GPU
    model = WhisperModel(model_size, compute_type="int8", device="cpu")

    # Transcribe the audio file
    result = model.transcribe(audio_file, word_timestamps=True)

    output_string = ""

    # Access segments with timestamps
    for segment in result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        output_string += f"[{start_time:.2f}s -> {end_time:.2f}s] {text}\n"
        # print(f"[{format_time(start_time)} --> {format_time(end_time)}] {text}")

    # Extract and return the transcript
    return output_string


def convert_to_wav(mp3_path, wav_path):
    subprocess.run(["ffmpeg", "-i", mp3_path, "-ar", "16000", "-ac", "1", wav_path])
    return None


# Generate transcript with timestamps
audio_file = "audio1.mp3"
path = f"PythonServer/downloads/{audio_file}"
wav_path = "PythonServer/wav/audio1.wav"
convert_to_wav(path, wav_path)

print("FOR mp3")
start_time = time.time()

print(audio_to_transcript_whisper(path))

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Transcription took {elapsed_time:.2f} seconds")

print("FOR WAV")
start_time = time.time()

print(audio_to_transcript_fast_whisper(path))

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Transcription took {elapsed_time:.2f} seconds")
# result = model.transcribe(f"PythonServer/downloads/{audio_file}", word_timestamps=True)
