import streamlit as st
import yt_dlp

def fetch_video_info(url):
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"Failed to fetch video info: {e}")
        return None

def download_video(url, resolution):
    ydl_opts = {
        'format': f'bestvideo[height={resolution}]+bestaudio/best[height={resolution}]',
        'outtmpl': '%(title)s.%(ext)s',
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

    # Input for YouTube URL
    url = st.text_input("Enter the YouTube video URL:")

    if url:
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
                if download_video(url, selected_resolution):
                    st.success("Video downloaded successfully!")

if __name__ == "__main__":
    main()
