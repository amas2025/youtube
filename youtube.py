import streamlit as st
import yt_dlp
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Authenticate Google Drive
def authenticate_gdrive():
    credentials = service_account.Credentials.from_service_account_file(
        "credentials.json", scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

# Upload file to Google Drive
def upload_to_gdrive(service, file_path, folder_id):
    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [folder_id],
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

# Download video to local and upload to Google Drive
def download_and_upload(url, resolution, folder_id, service):
    ydl_opts = {
        'format': f'bestvideo[height={resolution}]+bestaudio/best[height={resolution}]',
        'outtmpl': '%(title)s.%(ext)s',  # Save locally
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            local_file = ydl.prepare_filename(info)

            # Upload to Google Drive
            file_id = upload_to_gdrive(service, local_file, folder_id)
            st.success(f"Video uploaded to Google Drive successfully! File ID: {file_id}")
    except Exception as e:
        st.error(f"Failed to download or upload video: {e}")

def main():
    st.title("YouTube to Google Drive Downloader")

    # Input YouTube URL
    url = st.text_input("Enter the YouTube video URL:")
    folder_id = st.text_input("Enter the Google Drive folder ID:")

    if url and folder_id:
        # Fetch video resolutions
        ydl_opts = {}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                st.write(f"### {info['title']}")
                st.image(info['thumbnail'], use_container_width=True)

                # Get available resolutions
                resolutions = list(
                    set(
                        f"{f['height']}"
                        for f in info["formats"]
                        if f.get("height") and f.get("vcodec") != "none"
                    )
                )
                resolutions.sort(key=int)

                selected_resolution = st.selectbox("Select a resolution:", resolutions)

                if st.button("Download and Upload"):
                    service = authenticate_gdrive()
                    download_and_upload(url, selected_resolution, folder_id, service)
        except Exception as e:
            st.error(f"Error fetching video info: {e}")

if __name__ == "__main__":
    main()
