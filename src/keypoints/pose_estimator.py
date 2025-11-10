# src/keypoints/pose_estimator.py
import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict

class PoseEstimator:
    def __init__(self):
        print("Initializing MediaPipe Pose...")
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5
        )
        print("✓ MediaPipe Pose initialized!")
    
    def process_frame(self, frame: np.ndarray) -> List[Dict]:
        """Process frame for pose estimation"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        poses = []
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            h, w = frame.shape[:2]
            
            keypoints = []
            scores = []
            
            for landmark in landmarks:
                x = landmark.x * w
                y = landmark.y * h
                keypoints.append([x, y])
                scores.append(landmark.visibility)
            
            poses.append({
                'keypoints': np.array(keypoints),
                'scores': np.array(scores)
            })
        
        return poses
    
    def draw_poses(self, frame: np.ndarray, poses: List[Dict]) -> np.ndarray:
        """Draw poses on frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        annotated_frame = frame.copy()
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
        
        return annotated_frame