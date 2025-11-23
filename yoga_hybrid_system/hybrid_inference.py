"""
Hybrid Inference Engine
Combines image model + keypoint model predictions with confidence-based fusion
"""

import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
import joblib
import json
from extract_keypoints import KeypointExtractor

class HybridYogaClassifier:
    def __init__(self):
        self.image_model = None
        self.keypoint_model = None
        self.keypoint_scaler = None
        self.keypoint_label_encoder = None
        self.image_class_names = None
        self.keypoint_extractor = KeypointExtractor()
        self.img_size = 224
        
    def load_models(self):
        """Load both image and keypoint models"""
        # Load image model
        self.image_model = keras.models.load_model('models/yoga_model_final.h5')
        
        with open('models/class_names.json', 'r') as f:
            self.image_class_names = json.load(f)
        
        print("✅ Image model loaded")
        
        # Load keypoint model
        self.keypoint_model = joblib.load('models/keypoint_mlp_classifier.pkl')
        self.keypoint_scaler = joblib.load('models/keypoint_mlp_scaler.pkl')
        self.keypoint_label_encoder = joblib.load('models/keypoint_mlp_label_encoder.pkl')
        
        with open('models/keypoint_mlp_metadata.json', 'r') as f:
            self.keypoint_metadata = json.load(f)
        
        print("✅ Keypoint model loaded")
        
    def preprocess_image_for_cnn(self, image_path):
        """Preprocess image for CNN model"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.img_size, self.img_size))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict_image_model(self, image_path):
        """Get prediction from image model"""
        img = self.preprocess_image_for_cnn(image_path)
        predictions = self.image_model.predict(img, verbose=0)[0]
        
        pred_class_idx = np.argmax(predictions)
        pred_class = self.image_class_names[pred_class_idx]
        confidence = float(predictions[pred_class_idx])
        
        return pred_class, confidence, predictions
    
    def predict_keypoint_model(self, image_path):
        """Get prediction from keypoint model"""
        # Extract keypoints
        landmarks = self.keypoint_extractor.extract_landmarks(image_path)
        
        if landmarks is None:
            return None, 0.0, None
        
        # Normalize
        normalized = self.keypoint_extractor.normalize_landmarks(landmarks)
        
        # Extract angles
        angles = self.keypoint_extractor.extract_angles(landmarks)
        
        # Combine features (must match training feature order)
        features = list(normalized) + [angles[k] for k in sorted(angles.keys())]
        features = np.array(features).reshape(1, -1)
        
        # Scale
        features_scaled = self.keypoint_scaler.transform(features)
        
        # Predict
        if hasattr(self.keypoint_model, 'predict_proba'):
            proba = self.keypoint_model.predict_proba(features_scaled)[0]
            pred_class_idx = np.argmax(proba)
            confidence = float(proba[pred_class_idx])
        else:
            pred_class_idx = self.keypoint_model.predict(features_scaled)[0]
            confidence = 1.0
        
        pred_class = self.keypoint_label_encoder.inverse_transform([pred_class_idx])[0]
        
        return pred_class, confidence, angles
    
    def hybrid_fusion(self, image_pred, image_conf, keypoint_pred, keypoint_conf):
        """Combine predictions using confidence-based fusion logic"""
        
        result = {
            'image_prediction': image_pred,
            'image_confidence': image_conf,
            'keypoint_prediction': keypoint_pred,
            'keypoint_confidence': keypoint_conf,
            'final_prediction': None,
            'final_confidence': 0.0,
            'decision_logic': ''
        }
        
        # Rule 1: Keypoint detection failed
        if keypoint_pred is None:
            result['final_prediction'] = image_pred
            result['final_confidence'] = image_conf * 0.85  # Slight penalty
            result['decision_logic'] = 'KEYPOINT_FAILED_USE_IMAGE'
            return result
        
        # Rule 2: High confidence agreement
        if image_pred == keypoint_pred and image_conf > 0.85 and keypoint_conf > 0.80:
            result['final_prediction'] = image_pred
            result['final_confidence'] = (image_conf + keypoint_conf) / 2
            result['decision_logic'] = 'HIGH_CONFIDENCE_AGREEMENT'
            return result
        
        # Rule 3: Disagreement - favor higher confidence
        if image_pred != keypoint_pred:
            if abs(image_conf - keypoint_conf) > 0.2:
                if image_conf > keypoint_conf:
                    result['final_prediction'] = image_pred
                    result['final_confidence'] = image_conf * 0.9
                    result['decision_logic'] = 'IMAGE_HIGHER_CONFIDENCE'
                else:
                    result['final_prediction'] = keypoint_pred
                    result['final_confidence'] = keypoint_conf * 0.9
                    result['decision_logic'] = 'KEYPOINT_HIGHER_CONFIDENCE'
            else:
                # Similar confidence but disagreement - weighted average
                result['final_prediction'] = image_pred if image_conf >= keypoint_conf else keypoint_pred
                result['final_confidence'] = max(image_conf, keypoint_conf) * 0.75
                result['decision_logic'] = 'DISAGREEMENT_UNCERTAIN'
            return result
        
        # Rule 4: Agreement but moderate confidence
        if image_pred == keypoint_pred:
            result['final_prediction'] = image_pred
            result['final_confidence'] = (image_conf + keypoint_conf) / 2
            result['decision_logic'] = 'MODERATE_AGREEMENT'
            return result
        
        # Rule 5: Both low confidence
        if image_conf < 0.6 and keypoint_conf < 0.6:
            result['final_prediction'] = 'UNCERTAIN'
            result['final_confidence'] = 0.0
            result['decision_logic'] = 'BOTH_LOW_CONFIDENCE'
            return result
        
        # Default: use image model
        result['final_prediction'] = image_pred
        result['final_confidence'] = image_conf
        result['decision_logic'] = 'DEFAULT_IMAGE'
        return result
    
    def detect_posture_issues(self, pose_name, angles):
        """Detect common posture issues based on angles"""
        issues = []
        
        if angles is None:
            return issues
        
        # Warrior 2 specific checks
        if 'warrior' in pose_name.lower():
            # Front knee should be ~90 degrees
            front_knee = min(angles.get('left_knee', 180), angles.get('right_knee', 180))
            if front_knee < 85:
                issues.append('front_knee_too_bent')
            elif front_knee > 100:
                issues.append('front_knee_not_bent_enough')
            
            # Back leg should be straight (~180)
            back_knee = max(angles.get('left_knee', 0), angles.get('right_knee', 0))
            if back_knee < 170:
                issues.append('back_knee_bent')
        
        # Downward dog checks
        if 'down' in pose_name.lower() or 'dog' in pose_name.lower():
            # Knees should be relatively straight
            avg_knee = (angles.get('left_knee', 180) + angles.get('right_knee', 180)) / 2
            if avg_knee < 160:
                issues.append('knees_too_bent')
            
            # Elbows should be straight
            avg_elbow = (angles.get('left_elbow', 180) + angles.get('right_elbow', 180)) / 2
            if avg_elbow < 160:
                issues.append('elbows_bent')
        
        # Plank checks
        if 'plank' in pose_name.lower():
            # Elbows should be straight for high plank
            avg_elbow = (angles.get('left_elbow', 180) + angles.get('right_elbow', 180)) / 2
            if avg_elbow < 160:
                issues.append('elbows_bent_in_plank')
            
            # Hips should be aligned
            avg_hip = (angles.get('left_hip', 180) + angles.get('right_hip', 180)) / 2
            if avg_hip < 160:
                issues.append('hips_sagging')
        
        # General posture checks
        torso_angle = angles.get('torso_vertical', 0)
        if torso_angle > 15 and 'tree' not in pose_name.lower():
            issues.append('torso_leaning')
        
        spine_alignment = angles.get('spine_alignment', 180)
        if spine_alignment < 160:
            issues.append('rounded_back')
        
        return issues
    
    def predict(self, image_path):
        """Complete hybrid prediction pipeline"""
        print(f"\n🔍 Analyzing: {image_path}")
        
        # Get image model prediction
        image_pred, image_conf, _ = self.predict_image_model(image_path)
        print(f"📸 Image Model: {image_pred} ({image_conf:.3f})")
        
        # Get keypoint model prediction
        keypoint_pred, keypoint_conf, angles = self.predict_keypoint_model(image_path)
        if keypoint_pred:
            print(f"🦴 Keypoint Model: {keypoint_pred} ({keypoint_conf:.3f})")
        else:
            print(f"🦴 Keypoint Model: Failed to detect pose")
        
        # Hybrid fusion
        result = self.hybrid_fusion(image_pred, image_conf, keypoint_pred, keypoint_conf)
        print(f"🎯 Final: {result['final_prediction']} ({result['final_confidence']:.3f})")
        print(f"📊 Logic: {result['decision_logic']}")
        
        # Detect issues
        issues = self.detect_posture_issues(result['final_prediction'], angles)
        result['issues_detected'] = issues
        result['angles'] = angles
        
        if issues:
            print(f"⚠️  Issues: {', '.join(issues)}")
        
        return result


def main():
    """Demo hybrid inference"""
    classifier = HybridYogaClassifier()
    classifier.load_models()
    
    # Example prediction
    test_image = 'data/test/warrior2/example.jpg'  # Replace with actual path
    result = classifier.predict(test_image)
    
    # Print full result
    print("\n" + "="*50)
    print("COMPLETE RESULT:")
    print(json.dumps(result, indent=2, default=str))


if __name__ == '__main__':
    main()
