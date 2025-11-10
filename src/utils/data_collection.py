# src/utils/data_collection.py
import yt_dlp
import os
import cv2

class VideoDownloader:
    def __init__(self, output_dir="data/videos"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def download_youtube_video(self, url, output_name):
        """Download video from YouTube"""
        try:
            ydl_opts = {
                'format': 'best[height<=720]',
                'outtmpl': f'{self.output_dir}/{output_name}.%(ext)s',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"✓ Downloaded: {output_name}")
            return True
        except Exception as e:
            print(f"✗ Error downloading {url}: {e}")
            return False