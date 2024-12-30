import streamlit as st
import yt_dlp
import shutil
import os
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    if not shutil.which("ffmpeg"):
        st.error(
            "FFmpeg is not installed or not accessible. Please install it and ensure it's added to your PATH.\n"
            "For Streamlit Cloud, add `imageio[ffmpeg]` to your requirements.txt and `ffmpeg` to your packages.txt."
        )
        return False
    return True

def fetch_video_info(url):
    """Fetch video information from the provided URL."""
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"Failed to fetch video info: {e}")
        return None

def download_video(url, resolution, download_path):
    """Download the video with the selected resolution to a specific path."""
    ydl_opts = {
        'format': f'bestvideo[height={resolution}]+bestaudio/best[height={resolution}]',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
    except Exception as e:
        st.error(f"Failed to download video: {e}")
        return False

def main():
    st.title("YouTube Video Downloader with yt-dlp")

    # Check for FFmpeg
    if not check_ffmpeg():
        st.stop()

    # Verify FFmpeg installation
    if not shutil.which("ffmpeg"):
        st.error("FFmpeg is not accessible. Please ensure it is properly installed and configured.")
        return
    else:
        st.success("FFmpeg is successfully installed and accessible!")

    # Input for YouTube URL
    url = st.text_input("Enter the YouTube video URL:")

    # Input for download location
    download_path = st.text_input(
        "Enter the download folder path (absolute path):", value=str(Path.home())
    )

    if url and download_path:
        video_info = fetch_video_info(url)
        if video_info:
            st.write(f"### {video_info['title']}")
            st.image(video_info['thumbnail'], use_column_width=True)

            # Get available resolutions
            resolutions = list(
                set(
                    f"{f['height']}"
                    for f in video_info['formats']
                    if f.get('height') and f.get('vcodec') != 'none'
                )
            )
            resolutions.sort(key=int)

            selected_resolution = st.selectbox("Select a resolution:", resolutions)

            if st.button("Download"):
                # Ensure the download path exists
                os.makedirs(download_path, exist_ok=True)

                if download_video(url, selected_resolution, download_path):
                    st.success(f"Video downloaded successfully to {download_path}!")

if __name__ == "__main__":
    main()
