# src/tracking/player_tracker.py
import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import List, Dict
import cv2

class Track:
    def __init__(self, track_id, bbox):
        self.track_id = track_id
        self.bbox = bbox
        self.history = [bbox]
        
class PlayerTracker:
    def __init__(self, iou_threshold=0.3):
        self.iou_threshold = iou_threshold
        self.tracks = []
        self.next_id = 1
    
    def _calculate_iou(self, box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0
    
    def update(self, detections: List[Dict]) -> List[Dict]:
        """Simple tracking - assign IDs to detections"""
        tracks = []
        for i, detection in enumerate(detections):
            tracks.append({
                'track_id': self.next_id + i,
                'bbox': detection['bbox']
            })
        self.next_id += len(detections)
        return tracks
    
    def draw_tracks(self, frame: np.ndarray, tracks: List[Dict]) -> np.ndarray:
        """Draw tracking information on frame"""
        annotated_frame = frame.copy()
        
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                 (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        
        for track in tracks:
            track_id = track['track_id']
            bbox = track['bbox']
            color = colors[track_id % len(colors)]
            
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            label = f"ID: {track_id}"
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return annotated_frame