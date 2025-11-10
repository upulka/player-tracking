# src/detection/player_detector.py
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict

class PlayerDetector:
    def __init__(self, model_size='yolov8m.pt', conf_threshold=0.3):
        print("Loading YOLO model...")
        self.model = YOLO(model_size)
        self.conf_threshold = conf_threshold
        self.class_names = self.model.names
        print("✓ YOLO model loaded successfully!")
        
    def detect_players(self, frame: np.ndarray) -> List[Dict]:
        """Detect players in a single frame"""
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    confidence = box.conf.item()
                    class_id = int(box.cls.item())
                    class_name = self.class_names[class_id]
                    
                    if class_name == 'person' and confidence > self.conf_threshold:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        detections.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': confidence,
                            'class_name': class_name
                        })
        
        return detections