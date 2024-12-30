import shutil

if shutil.which("ffmpeg"):
    print("FFmpeg is installed and accessible.")
else:
    print("FFmpeg is NOT installed or accessible.")
