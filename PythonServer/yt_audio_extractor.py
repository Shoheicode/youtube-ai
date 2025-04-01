import os
import subprocess


def download_audio(youtube_url, output_path=".", filename=None, file_extension="mp3"):
    """
    Download audio from a YouTube video using yt-dlp.

    Parameters:
    - youtube_url: URL of the YouTube video
    - output_path: Directory to save the audio file (default is current directory)
    - filename: Name for the output file (without extension)
    - file_extension: File extension for the output (default is mp3)

    Returns:
    - Path to the downloaded audio file
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Prepare output filename
        output_file = os.path.join(
            output_path,
            (
                f"{filename}.{file_extension}"
                if filename
                else f"%(title)s.{file_extension}"
            ),
        )

        # Prepare yt-dlp command
        cmd = [
            "yt-dlp",
            "--extract-audio",
            f"--audio-format={file_extension}",
            "--audio-quality=0",  # Best quality
            "-o",
            output_file,
            youtube_url,
        ]

        # Execute command
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Error in yt-dlp: {result.stderr}")

        print("Audio downloaded successfully!")

        # If output file used the template, find the actual filename from yt-dlp output
        if filename is None:
            # Look for "[download] Destination: " in the output
            for line in result.stdout.split("\n"):
                if "[download] Destination:" in line:
                    output_file = line.split("[download] Destination:")[1].strip()
                    break

        return output_file

    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None


# Test Code:
video_url = "https://www.youtube.com/watch?v=8B1EtVPBSMw"  # Replace with your video URL
download_audio(video_url, output_path="downloads")
