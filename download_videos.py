# download_videos.py
import os
from src.utils.data_collection import VideoDownloader

def download_sample_videos():
    """Download sample sports videos - OPTIONAL: Use if you want to download videos via code"""
    downloader = VideoDownloader()
    
    # ADD YOUR YOUTUBE URLs HERE (Optional - you can manually add videos instead)
    sports_videos = [
        # Example format:
        # "https://www.youtube.com/shorts/ABC123",
        # "https://www.youtube.com/watch?v=XYZ789",
    ]
    
    if not sports_videos:
        print("No URLs provided. Please add videos manually to data/videos/ folder.")
        print("Video naming format: sports_video_1.mp4, sports_video_2.mp4, etc.")
        return
    
    for i, url in enumerate(sports_videos):
        downloader.download_youtube_video(url, f"sports_video_{i+1}")

if __name__ == "__main__":
    download_sample_videos()