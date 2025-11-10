# test_installation.py
import torch
import ultralytics
import cv2
import numpy as np

print("✓ PyTorch version:", torch.__version__)
print("✓ CUDA available:", torch.cuda.is_available())
print("✓ Ultralytics version:", ultralytics.__version__)
print("✓ OpenCV version:", cv2.__version__)
print("✓ All imports successful!")