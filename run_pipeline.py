# run_pipeline.py
import sys
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import from src
from src.main_pipeline import SportsPlayerTracker

def generate_report(results, performance_metrics, video_name):
    """Generate comprehensive report"""
    # Calculate basic metrics
    total_detections = sum(len(frame['detections']) for frame in results)
    total_tracks = len(set(track['track_id'] for frame in results for track in frame['tracks']))
    avg_confidence = np.mean([d['confidence'] for frame in results for d in frame['detections']]) if any(frame['detections'] for frame in results) else 0
    
    # Create metrics plot
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    confidences = []
    for frame in results:
        if frame['detections']:
            confidences.append(np.mean([d['confidence'] for d in frame['detections']]))
        else:
            confidences.append(0)
    plt.plot(confidences)
    plt.title('Detection Confidence Over Time')
    plt.xlabel('Frame Number')
    plt.ylabel('Average Confidence')
    
    plt.subplot(1, 2, 2)
    detections_per_frame = [len(frame['detections']) for frame in results]
    plt.plot(detections_per_frame)
    plt.title('Number of Detections Per Frame')
    plt.xlabel('Frame Number')
    plt.ylabel('Number of Detections')
    
    plt.tight_layout()
    plt.savefig(f'outputs/{video_name}_metrics.png')
    plt.close()
    
    # Create report
    report = f"""
# SC549 Player Tracking Report - {video_name}

## Performance Summary
- **Total Frames Processed:** {len(results)}
- **Total Detections:** {total_detections}
- **Average Detections per Frame:** {total_detections/len(results):.2f}
- **Total Unique Tracks:** {total_tracks}
- **Average Detection Confidence:** {avg_confidence:.3f}

## System Performance
- **Average Detection Time:** {performance_metrics['average_detection_time']*1000:.2f} ms
- **Average Pose Time:** {performance_metrics['average_pose_time']*1000:.2f} ms  
- **Average Tracking Time:** {performance_metrics['average_tracking_time']*1000:.2f} ms
- **Processing FPS:** {performance_metrics['fps']:.2f}

## Model Architecture
- **Player Detection:** YOLOv8
- **Pose Estimation:** MediaPipe Pose
- **Tracking:** Simple ID Assignment

## Sample Output
![Metrics]({video_name}_metrics.png)

*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    # Save report
    with open(f'outputs/{video_name}_report.md', 'w') as f:
        f.write(report)
    
    # Save results as JSON
    with open(f'outputs/{video_name}_results.json', 'w') as f:
        json.dump({
            'detection_metrics': {
                'total_detections': total_detections,
                'average_confidence': avg_confidence,
                'detections_per_frame': total_detections/len(results)
            },
            'tracking_metrics': {
                'total_tracks': total_tracks
            },
            'performance_metrics': performance_metrics,
            'frame_count': len(results)
        }, f, indent=2)
    
    return report

def main():
    print("Starting Sports Player Tracking Pipeline...")
    
    # Create outputs directory
    os.makedirs('outputs', exist_ok=True)
    
    # Initialize tracker
    tracker = SportsPlayerTracker()
    
    # VIDEO FILES CONFIGURATION - MODIFY THIS SECTION FOR YOUR VIDEOS
    video_files = [
        "data/videos/sports_video_1.mp4",
        "data/videos/sports_video_2.mp4", 
        "data/videos/sports_video_3.mp4",
        # Add more videos as needed
    ]
    
    # Remove videos that don't exist
    existing_videos = [v for v in video_files if os.path.exists(v)]
    
    if not existing_videos:
        print("No video files found!")
        print("Please:")
        print("1. Download sports videos (5-10 seconds each)")
        print("2. Save them in 'data/videos/' folder")
        print("3. Name them: sports_video_1.mp4, sports_video_2.mp4, etc.")
        print("4. Update the video_files list in run_pipeline.py")
        return
    
    print(f"Found {len(existing_videos)} video(s) to process")
    
    all_results = {}
    
    for video_path in existing_videos:
        print(f"\n{'='*50}")
        print(f"📹 PROCESSING: {os.path.basename(video_path)}")
        print(f"{'='*50}")
        
        # Output path for processed video
        output_path = f"outputs/tracked_{os.path.basename(video_path)}"
        
        # Process video (50 frames for quick testing)
        results = tracker.process_video(video_path, output_path, max_frames=50)
        all_results[video_path] = results
        
        if results:
            # Calculate performance metrics
            performance_metrics = tracker.calculate_performance_metrics()
            
            # Generate report
            video_name = os.path.basename(video_path).replace('.mp4', '')
            report = generate_report(results, performance_metrics, video_name)
            
            print(f"COMPLETED: {os.path.basename(video_path)}")
            print(f"Performance: {performance_metrics['fps']:.2f} FPS")
    
    print(f"\n PIPELINE COMPLETED!")
    print(f"   Processed {len(existing_videos)} video(s)")
    print(f"   Outputs saved in 'outputs' folder")
    print(f"   Check the generated reports and videos")

if __name__ == "__main__":
    main()