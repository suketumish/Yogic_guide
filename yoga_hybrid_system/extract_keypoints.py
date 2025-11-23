"""
Keypoint Extraction Module
Uses MediaPipe Pose to extract 33 body landmarks from yoga images
"""

import os
import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
from tqdm import tqdm
import json

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class KeypointExtractor:
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5
        )
        
    def extract_landmarks(self, image_path):
        """Extract 33 pose landmarks from an image"""
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = self.pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return None
        
        # Extract landmarks
        landmarks = []
        for lm in results.pose_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])
        
        return np.array(landmarks)
    
    def calculate_angle(self, a, b, c):
        """Calculate angle between three points"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle
    
    def extract_angles(self, landmarks):
        """Extract key joint angles from landmarks"""
        # Reshape landmarks: 33 landmarks × 4 values = 132 values
        lm = landmarks.reshape(33, 4)
        
        angles = {}
        
        # Left arm angles
        angles['left_shoulder'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.LEFT_HIP.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_ELBOW.value][:2]
        )
        angles['left_elbow'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_ELBOW.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_WRIST.value][:2]
        )
        
        # Right arm angles
        angles['right_shoulder'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.RIGHT_HIP.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value][:2]
        )
        angles['right_elbow'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_WRIST.value][:2]
        )
        
        # Left leg angles
        angles['left_hip'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_HIP.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_KNEE.value][:2]
        )
        angles['left_knee'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.LEFT_HIP.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_KNEE.value][:2],
            lm[mp_pose.PoseLandmark.LEFT_ANKLE.value][:2]
        )
        
        # Right leg angles
        angles['right_hip'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_HIP.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_KNEE.value][:2]
        )
        angles['right_knee'] = self.calculate_angle(
            lm[mp_pose.PoseLandmark.RIGHT_HIP.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_KNEE.value][:2],
            lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value][:2]
        )
        
        # Torso alignment
        left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value][:2]
        right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][:2]
        left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP.value][:2]
        right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value][:2]
        
        mid_shoulder = (left_shoulder + right_shoulder) / 2
        mid_hip = (left_hip + right_hip) / 2
        
        # Torso angle from vertical
        torso_vector = mid_shoulder - mid_hip
        vertical = np.array([0, -1])
        angles['torso_vertical'] = np.arccos(
            np.dot(torso_vector, vertical) / (np.linalg.norm(torso_vector) * np.linalg.norm(vertical))
        ) * 180 / np.pi
        
        # Spine curvature (simplified)
        nose = lm[mp_pose.PoseLandmark.NOSE.value][:2]
        angles['spine_alignment'] = self.calculate_angle(mid_hip, mid_shoulder, nose)
        
        return angles
    
    def normalize_landmarks(self, landmarks):
        """Normalize landmarks relative to hip center and torso height"""
        lm = landmarks.reshape(33, 4)
        
        # Calculate hip center
        left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP.value][:3]
        right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value][:3]
        hip_center = (left_hip + right_hip) / 2
        
        # Calculate torso height
        left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value][:3]
        right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][:3]
        shoulder_center = (left_shoulder + right_shoulder) / 2
        torso_height = np.linalg.norm(shoulder_center - hip_center)
        
        # Normalize
        normalized = lm.copy()
        for i in range(33):
            normalized[i][:3] = (lm[i][:3] - hip_center) / (torso_height + 1e-6)
        
        return normalized.flatten()
    
    def process_dataset(self, data_dir, output_csv='keypoints_dataset.csv'):
        """Process entire dataset and save keypoints"""
        data = []
        
        splits = ['train', 'validate', 'test']
        
        for split in splits:
            split_dir = os.path.join(data_dir, split)
            if not os.path.exists(split_dir):
                continue
            
            classes = [d for d in os.listdir(split_dir) if os.path.isdir(os.path.join(split_dir, d))]
            
            for class_name in classes:
                class_dir = os.path.join(split_dir, class_name)
                images = [f for f in os.listdir(class_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
                
                print(f"Processing {split}/{class_name}: {len(images)} images")
                
                for img_name in tqdm(images):
                    img_path = os.path.join(class_dir, img_name)
                    
                    # Extract landmarks
                    landmarks = self.extract_landmarks(img_path)
                    if landmarks is None:
                        continue
                    
                    # Normalize landmarks
                    normalized = self.normalize_landmarks(landmarks)
                    
                    # Extract angles
                    angles = self.extract_angles(landmarks)
                    
                    # Combine features
                    row = {
                        'image_path': img_path,
                        'split': split,
                        'label': class_name
                    }
                    
                    # Add normalized landmarks
                    for i in range(len(normalized)):
                        row[f'landmark_{i}'] = normalized[i]
                    
                    # Add angles
                    for angle_name, angle_value in angles.items():
                        row[angle_name] = angle_value
                    
                    data.append(row)
        
        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False)
        print(f"\n✅ Keypoints saved to {output_csv}")
        print(f"Total samples: {len(df)}")
        print(f"Features per sample: {len(df.columns) - 3}")  # Exclude path, split, label
        
        return df
    
    def visualize_landmarks(self, image_path, output_path=None):
        """Visualize pose landmarks on an image"""
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = self.pose.process(image_rgb)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
        
        if output_path:
            cv2.imwrite(output_path, image)
        
        return image


def main():
    """Main keypoint extraction pipeline"""
    extractor = KeypointExtractor()
    
    # Process dataset
    df = extractor.process_dataset('data', 'keypoints_dataset.csv')
    
    # Save statistics
    stats = {
        'total_samples': len(df),
        'samples_per_split': df['split'].value_counts().to_dict(),
        'samples_per_class': df['label'].value_counts().to_dict(),
        'feature_count': len(df.columns) - 3
    }
    
    with open('keypoints_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("\n✅ Keypoint extraction complete!")


if __name__ == '__main__':
    main()
