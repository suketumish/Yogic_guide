"""
Simple Pose Detector - Works without MediaPipe
Uses only the trained yoga model for detection
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# Add yoga_hybrid_system to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yoga_hybrid_system'))

class SimplePoseDetector:
    """Simple pose detector using only image classification"""
    
    def __init__(self):
        self.model = None
        self.class_names = []
        self.initialized = False
        
    def initialize(self):
        """Initialize the model"""
        try:
            import tensorflow as tf
            import json
            
            model_path = os.path.join('yoga_hybrid_system', 'models', 'yoga_model_final.h5')
            class_names_path = os.path.join('yoga_hybrid_system', 'models', 'class_names.json')
            
            if not os.path.exists(model_path):
                print(f"❌ Model not found: {model_path}")
                return False
            
            if not os.path.exists(class_names_path):
                print(f"❌ Class names not found: {class_names_path}")
                return False
            
            # Load model
            print("Loading model...")
            self.model = tf.keras.models.load_model(model_path)
            print("✅ Model loaded")
            
            # Load class names
            with open(class_names_path, 'r') as f:
                self.class_names = json.load(f)
            print(f"✅ Loaded {len(self.class_names)} pose classes")
            
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Error initializing: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def preprocess_image(self, image):
        """Preprocess image for model"""
        # Resize to 224x224
        image = cv2.resize(image, (224, 224))
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Normalize
        image = image.astype('float32') / 255.0
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        return image
    
    def detect_from_frame(self, frame):
        """Detect pose from video frame"""
        if not self.initialized:
            return None
        
        try:
            # Preprocess
            processed = self.preprocess_image(frame)
            
            # Predict
            predictions = self.model.predict(processed, verbose=0)
            
            # Get top prediction
            top_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][top_idx])
            pose_name = self.class_names[top_idx]
            
            return {
                'success': True,
                'pose_name': pose_name,
                'confidence': confidence,
                'display_name': pose_name.replace('_', ' ').title()
            }
            
        except Exception as e:
            print(f"Detection error: {e}")
            return None
    
    def detect_from_base64(self, image_base64):
        """Detect pose from base64 image"""
        if not self.initialized:
            return {'success': False, 'error': 'Not initialized'}
        
        try:
            # Decode base64
            if ',' in image_base64:
                image_base64 = image_base64.split(',')[1]
            
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            
            # Convert to numpy array
            frame = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Detect
            result = self.detect_from_frame(frame)
            
            if result:
                return result
            else:
                return {'success': False, 'error': 'Detection failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Global instance
_detector = None

def get_simple_detector():
    """Get or create detector instance"""
    global _detector
    if _detector is None:
        _detector = SimplePoseDetector()
        _detector.initialize()
    return _detector

if __name__ == '__main__':
    # Test
    detector = SimplePoseDetector()
    if detector.initialize():
        print("✅ Detector ready!")
        print(f"Can detect {len(detector.class_names)} poses")
    else:
        print("❌ Detector failed to initialize")
