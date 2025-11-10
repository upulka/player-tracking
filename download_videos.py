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

        # "https://www.youtube.com/shorts/uXM4OovR9t0?feature=share",
        # "https://www.youtube.com/shorts/hnfTIna5Li8?feature=share",
        # "https://www.youtube.com/shorts/2-cSUG7oZWM?feature=share"

        "https://drive.google.com/file/d/19sLpwIDDZD7M9RuyTi3X2bjjNe4ZMVM5/view?usp=drive_link",
        "https://drive.google.com/file/d/1QWbH0w5kNudsQCFaQfqESomlWA92HUb1/view?usp=drive_link",
        "https://drive.google.com/file/d/1QodadGq-0BGSJKtGAX95JPmoebeOJF_u/view?usp=drive_link",
        "https://drive.google.com/file/d/1BfhrfemKyLGTUVAe2B2SdegRJaAoV9qF/view?usp=drive_link",
        "https://drive.google.com/file/d/1zJShupiWovFGGLBsJX8g2FydT5kPijlz/view?usp=drive_link",
        "https://drive.google.com/file/d/1psQvfJd0Ft8qN08wLi5vt6mXH1twf0sr/view?usp=drive_link",
        "https://drive.google.com/file/d/1jfdL5yiFj7SRr6MPbVqdhX93pwiEnQu3/view?usp=drive_link",
        "https://drive.google.com/file/d/15TtwkLyAnxV0eyZYFXuzj-ouj3LjbtSD/view?usp=drive_link"
    ]
    
    if not sports_videos:
        print("No URLs provided. Please add videos manually to data/videos/ folder.")
        print("Video naming format: sports_video_1.mp4, sports_video_2.mp4, etc.")
        return
    
    for i, url in enumerate(sports_videos):
        downloader.download_youtube_video(url, f"sports_video_{i+1}")

if __name__ == "__main__":
    download_sample_videos()