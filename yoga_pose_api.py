"""
Yoga Pose Detection API
Integrates the trained yoga hybrid system with Flask app
"""

import os
import sys
import json

# Add yoga_hybrid_system to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yoga_hybrid_system'))

# Try to use hybrid system first, fallback to simple detector
HYBRID_SYSTEM_AVAILABLE = False
SIMPLE_DETECTOR_AVAILABLE = False
YogaHybridSystem = None

def _lazy_import():
    """Lazy import of heavy dependencies"""
    global HYBRID_SYSTEM_AVAILABLE, SIMPLE_DETECTOR_AVAILABLE, YogaHybridSystem
    
    if YogaHybridSystem is not None:
        return HYBRID_SYSTEM_AVAILABLE
    
    # Try hybrid system first (needs MediaPipe)
    try:
        import numpy as np
        import cv2
        import base64
        from io import BytesIO
        from PIL import Image
        import mediapipe
        from hybrid_inference import YogaHybridSystem as YHS
        
        YogaHybridSystem = YHS
        HYBRID_SYSTEM_AVAILABLE = True
        print("✅ Yoga Hybrid System loaded successfully (with MediaPipe)")
        return True
    except ImportError as e:
        print(f"⚠️  MediaPipe not available: {e}")
        print(f"   Trying simple detector (image-only)...")
        
        # Try simple detector (no MediaPipe needed)
        try:
            from simple_pose_detector import SimplePoseDetector
            YogaHybridSystem = SimplePoseDetector
            SIMPLE_DETECTOR_AVAILABLE = True
            print("✅ Simple Pose Detector loaded (image-only mode)")
            return True
        except Exception as e2:
            print(f"❌ Simple detector also failed: {e2}")
            HYBRID_SYSTEM_AVAILABLE = False
            SIMPLE_DETECTOR_AVAILABLE = False
            return False
    except Exception as e:
        print(f"⚠️  Yoga Hybrid System not available: {e}")
        print(f"   Make sure you're running in the correct Python environment")
        HYBRID_SYSTEM_AVAILABLE = False
        return False

class YogaPoseDetector:
    """
    Wrapper class for yoga pose detection
    Integrates with existing Flask app
    """
    
    def __init__(self):
        self.system = None
        self.initialized = False
        
        # Lazy initialization - only load when first used
        self._init_attempted = False
    
    def _ensure_initialized(self):
        """Ensure system is initialized (lazy loading)"""
        if self._init_attempted:
            return self.initialized
        
        self._init_attempted = True
        
        # Try to import dependencies
        if not _lazy_import():
            return False
        
        try:
            # Check if using simple detector or hybrid system
            if SIMPLE_DETECTOR_AVAILABLE:
                print("Using Simple Pose Detector (image-only mode)")
                self.system = YogaHybridSystem()
                if self.system.initialize():
                    self.initialized = True
                    print("✅ Simple Pose Detector initialized")
                    return True
                else:
                    print("❌ Simple Pose Detector failed to initialize")
                    return False
            
            elif HYBRID_SYSTEM_AVAILABLE:
                # Initialize the hybrid system
                model_dir = os.path.join(os.path.dirname(__file__), 'yoga_hybrid_system', 'models')
                
                # Check if models exist
                image_model_path = os.path.join(model_dir, 'yoga_model_final.h5')
                keypoint_model_path = os.path.join(model_dir, 'keypoint_mlp_classifier.pkl')
                
                if os.path.exists(image_model_path) and os.path.exists(keypoint_model_path):
                    self.system = YogaHybridSystem(
                        image_model_path=image_model_path,
                        keypoint_model_path=keypoint_model_path,
                        use_llm=False  # Disable LLM for real-time detection
                    )
                    self.initialized = True
                    print("✅ Yoga Hybrid System initialized (full mode)")
                    return True
                else:
                    print("⚠️  Model files not found. Please train models first.")
                    print(f"   Looking for: {image_model_path}")
                    print(f"   Looking for: {keypoint_model_path}")
                    return False
            else:
                print("❌ No detection system available")
                return False
                
        except Exception as e:
            print(f"❌ Failed to initialize detection system: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def detect_pose_from_base64(self, image_base64):
        """
        Detect yoga pose from base64 encoded image
        
        Args:
            image_base64: Base64 encoded image string
            
        Returns:
            dict: Detection results with pose name, confidence, and feedback
        """
        # Ensure initialized
        if not self._ensure_initialized():
            return {
                'success': False,
                'error': 'Yoga detection system not initialized. Check server logs for details.'
            }
        
        try:
            # Use simple detector if available
            if SIMPLE_DETECTOR_AVAILABLE:
                result = self.system.detect_from_base64(image_base64)
                if result.get('success'):
                    result['feedback'] = self._generate_simple_feedback(result)
                    result['method'] = 'image_only'
                return result
            
            # Otherwise use hybrid system
            import numpy as np
            import cv2
            import base64
            from io import BytesIO
            from PIL import Image
            
            # Decode base64 image
            if ',' in image_base64:
                image_base64 = image_base64.split(',')[1]
            
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            
            # Convert to numpy array
            image_np = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            # Run inference
            result = self.system.predict(image_np)
            
            if result['success']:
                return {
                    'success': True,
                    'pose_name': result['predicted_pose'],
                    'confidence': float(result['confidence']),
                    'image_confidence': float(result.get('image_confidence', 0)),
                    'keypoint_confidence': float(result.get('keypoint_confidence', 0)),
                    'method': result.get('method', 'hybrid'),
                    'feedback': self._generate_simple_feedback(result)
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Unknown error')
                }
                
        except Exception as e:
            print(f"❌ Error in pose detection: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def detect_pose_from_file(self, image_path):
        """
        Detect yoga pose from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            dict: Detection results
        """
        # Ensure initialized
        if not self._ensure_initialized():
            return {
                'success': False,
                'error': 'Yoga detection system not initialized'
            }
        
        try:
            import cv2
            
            # Read image
            image = cv2.imread(image_path)
            
            if image is None:
                return {
                    'success': False,
                    'error': 'Failed to read image file'
                }
            
            # Run inference
            result = self.system.predict(image)
            
            if result['success']:
                return {
                    'success': True,
                    'pose_name': result['predicted_pose'],
                    'confidence': float(result['confidence']),
                    'image_confidence': float(result.get('image_confidence', 0)),
                    'keypoint_confidence': float(result.get('keypoint_confidence', 0)),
                    'method': result.get('method', 'unknown'),
                    'feedback': self._generate_simple_feedback(result)
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Unknown error')
                }
                
        except Exception as e:
            print(f"❌ Error in pose detection: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_simple_feedback(self, result):
        """Generate simple feedback based on detection result"""
        confidence = result.get('confidence', 0)
        pose_name = result.get('pose_name', result.get('predicted_pose', 'Unknown'))
        
        # Format pose name for display
        pose_display = pose_name.replace('_', ' ').title()
        
        if confidence >= 0.9:
            return f"बहुत बढ़िया! Perfect {pose_display} detected with {confidence*100:.1f}% confidence."
        elif confidence >= 0.75:
            return f"अच्छा! {pose_display} detected with {confidence*100:.1f}% confidence. Keep it steady."
        elif confidence >= 0.6:
            return f"{pose_display} detected with {confidence*100:.1f}% confidence. Form ko improve karein."
        else:
            return f"Pose detected but confidence low hai ({confidence*100:.1f}%). Position adjust karein."
    
    def get_available_poses(self):
        """Get list of available yoga poses"""
        # Try to initialize if not done
        self._ensure_initialized()
        
        if not self.initialized:
            return []
        
        try:
            # If using simple detector, get from it
            if SIMPLE_DETECTOR_AVAILABLE and hasattr(self.system, 'class_names'):
                return self.system.class_names
            
            # Otherwise load from file
            class_names_path = os.path.join(
                os.path.dirname(__file__), 
                'yoga_hybrid_system', 
                'models', 
                'class_names.json'
            )
            
            if os.path.exists(class_names_path):
                with open(class_names_path, 'r') as f:
                    class_names = json.load(f)
                return class_names
            else:
                return []
        except Exception as e:
            print(f"Error loading class names: {e}")
            return []

# Global detector instance
_detector = None

def get_detector():
    """Get or create global detector instance"""
    global _detector
    if _detector is None:
        _detector = YogaPoseDetector()
    return _detector

def detect_pose(image_base64=None, image_path=None):
    """
    Convenience function for pose detection
    
    Args:
        image_base64: Base64 encoded image (optional)
        image_path: Path to image file (optional)
        
    Returns:
        dict: Detection results
    """
    detector = get_detector()
    
    if image_base64:
        return detector.detect_pose_from_base64(image_base64)
    elif image_path:
        return detector.detect_pose_from_file(image_path)
    else:
        return {
            'success': False,
            'error': 'No image provided'
        }

def get_available_poses():
    """Get list of available yoga poses"""
    detector = get_detector()
    return detector.get_available_poses()

def is_system_ready():
    """Check if the yoga detection system is ready"""
    detector = get_detector()
    return detector.initialized
