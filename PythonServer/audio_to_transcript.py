import whisper

# Load model (options: tiny, base, small, medium, large)
model = whisper.load_model("medium")

# Generate transcript with timestamps
audio_file = "audio1.mp3"
result = model.transcribe(f"PythonServer/downloads/{audio_file}", word_timestamps=True)


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"


def audio_to_transcript(audio_file):
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
    result = model.transcribe(audio_file)

    output_string = ""

    # Access segments with timestamps
    for segment in result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        output_string += f"[{start_time:.2f}s -> {end_time:.2f}s] {text}\n"
        # print(f"[{format_time(start_time)} --> {format_time(end_time)}] {text}")

    # Extract and return the transcript
    print(output_string)
    return output_string
