import streamlit as st

# Enhanced error handling for pytube import
try:
    from pytube import YouTube
except ImportError:
    st.error(
        "The 'pytube' module is not installed. Please install it by running the following command in your terminal:\n\n"
        "`pip install pytube`"
    )
    raise SystemExit

def main():
    st.title("YouTube Video Downloader")

    # Input for YouTube URL
    url = st.text_input("Enter the YouTube video URL:")

    if url:
        try:
            # Fetch video details
            yt = YouTube(url)
            st.write(f"### {yt.title}")
            st.image(yt.thumbnail_url, use_column_width=True)

            # Select resolution
            streams = yt.streams.filter(progressive=True, file_extension='mp4')
            resolution_options = [stream.resolution for stream in streams]

            if not resolution_options:
                st.error("No downloadable resolutions are available for this video.")
                return

            selected_resolution = st.selectbox("Select a resolution:", resolution_options)

            if st.button("Download"):
                stream = streams.filter(res=selected_resolution).first()
                if stream:
                    # Download video
                    stream.download()
                    st.success(f"Video downloaded successfully! Saved as: {stream.default_filename}")
                else:
                    st.error("The selected resolution is not available.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
