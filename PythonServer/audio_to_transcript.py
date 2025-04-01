import whisper

# Load model (options: tiny, base, small, medium, large)
model = whisper.load_model("medium")

# Generate transcript with timestamps
audio_file = "A Minecraft Movie ｜ Final Trailer"
result = model.transcribe(f"PythonServer/downloads/{audio_file}", word_timestamps=True)


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"


# Access segments with timestamps
for segment in result["segments"]:
    start_time = segment["start"]
    end_time = segment["end"]
    text = segment["text"]
    print(f"[{format_time(start_time)} --> {format_time(end_time)}] {text}")
