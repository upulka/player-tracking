# src/main_pipeline.py
import cv2
import numpy as np
import json
import time
from datetime import datetime
import os
from detection.player_detector import PlayerDetector
from keypoints.pose_estimator import PoseEstimator
from tracking.player_tracker import PlayerTracker

class SportsPlayerTracker:
    def __init__(self):
        print("Initializing Sports Player Tracker...")
        self.detector = PlayerDetector()
        self.pose_estimator = PoseEstimator()
        self.tracker = PlayerTracker()
        self.metrics = {
            'detection_times': [],
            'pose_times': [],
            'tracking_times': [],
            'frame_counts': 0
        }
        print("✓ Sports Player Tracker initialized!")
    
    def process_video(self, video_path: str, output_path: str = None, max_frames: int = 100):
        """
        Process video with all components
        
        Args:
            video_path: Path to input video file
            output_path: Path to save output video (optional)
            max_frames: Maximum number of frames to process
        """
        # VIDEO PATH USAGE: video_path should be like "data/videos/sports_video_1.mp4"
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Error: Could not open video file {video_path}")
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        if output_path:
            # Create outputs directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_results = []
        frame_count = 0
        
        print(f"Processing video: {os.path.basename(video_path)}")
        
        while True:
            ret, frame = cap.read()
            if not ret or frame_count >= max_frames:
                break
            
            frame_count += 1
            if frame_count % 10 == 0:
                print(f"  Frame {frame_count}")
            
            # Player Detection
            start_time = time.time()
            detections = self.detector.detect_players(frame)
            det_time = time.time() - start_time
            
            # Pose Estimation
            pose_time = 0
            poses = []
            if detections:
                start_time = time.time()
                poses = self.pose_estimator.process_frame(frame)
                pose_time = time.time() - start_time
            
            # Tracking
            start_time = time.time()
            tracks = self.tracker.update(detections)
            track_time = time.time() - start_time
            
            # Update metrics
            self.metrics['detection_times'].append(det_time)
            self.metrics['pose_times'].append(pose_time)
            self.metrics['tracking_times'].append(track_time)
            self.metrics['frame_counts'] = frame_count
            
            # Annotate frame
            annotated_frame = self.annotate_frame(frame, detections, poses, tracks)
            
            if output_path:
                out.write(annotated_frame)
            
            # Store results
            frame_results.append({
                'frame_number': frame_count,
                'detections': detections,
                'poses': [self._serialize_pose(pose) for pose in poses],
                'tracks': tracks
            })
        
        cap.release()
        if output_path:
            out.release()
        
        print(f"✓ Processed {frame_count} frames from {os.path.basename(video_path)}")
        return frame_results
    
    def _serialize_pose(self, pose):
        return {
            'keypoints': pose['keypoints'].tolist(),
            'scores': pose['scores'].tolist()
        }
    
    def annotate_frame(self, frame, detections, poses, tracks):
        annotated_frame = frame.copy()
        
        # Draw detections (green)
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        
        # Draw poses
        annotated_frame = self.pose_estimator.draw_poses(annotated_frame, poses)
        
        # Draw tracks (colored by ID)
        annotated_frame = self.tracker.draw_tracks(annotated_frame, tracks)
        
        # Add performance info
        if len(self.metrics['detection_times']) > 0:
            avg_det_time = np.mean(self.metrics['detection_times'][-10:]) * 1000
            avg_pose_time = np.mean(self.metrics['pose_times'][-10:]) * 1000
            avg_track_time = np.mean(self.metrics['tracking_times'][-10:]) * 1000
            
            info_text = [
                f"Detection: {avg_det_time:.1f}ms",
                f"Pose: {avg_pose_time:.1f}ms", 
                f"Tracking: {avg_track_time:.1f}ms",
                f"Players: {len(tracks)}"
            ]
            
            for i, text in enumerate(info_text):
                cv2.putText(annotated_frame, text, (10, 30 + i * 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return annotated_frame
    
    def calculate_performance_metrics(self):
        return {
            'average_detection_time': np.mean(self.metrics['detection_times']),
            'average_pose_time': np.mean(self.metrics['pose_times']),
            'average_tracking_time': np.mean(self.metrics['tracking_times']),
            'total_frames': self.metrics['frame_counts'],
            'fps': self.metrics['frame_counts'] / sum(self.metrics['detection_times']) if self.metrics['detection_times'] else 0
        }