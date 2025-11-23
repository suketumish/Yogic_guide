#!/usr/bin/env python3
"""
Quick test script to verify yoga detection API
"""

import sys
import os

print("="*60)
print("  YOGA DETECTION API TEST")
print("="*60)

# Test 1: Import check
print("\n[Test 1] Checking imports...")
try:
    from yoga_pose_api import get_detector
    print("✅ yoga_pose_api imported")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Get detector
print("\n[Test 2] Getting detector instance...")
try:
    detector = get_detector()
    print("✅ Detector instance created")
except Exception as e:
    print(f"❌ Failed to create detector: {e}")
    sys.exit(1)

# Test 3: Initialize
print("\n[Test 3] Initializing detector...")
try:
    initialized = detector._ensure_initialized()
    if initialized:
        print("✅ Detector initialized successfully")
    else:
        print("❌ Detector failed to initialize")
        sys.exit(1)
except Exception as e:
    print(f"❌ Initialization error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Get poses
print("\n[Test 4] Getting available poses...")
try:
    poses = detector.get_available_poses()
    print(f"✅ Found {len(poses)} poses")
    if len(poses) > 0:
        print(f"   Sample poses: {', '.join(poses[:5])}")
except Exception as e:
    print(f"❌ Failed to get poses: {e}")

# Test 5: Test detection with dummy image
print("\n[Test 5] Testing detection with dummy image...")
try:
    import base64
    import cv2
    import numpy as np
    
    # Create a dummy image (black square)
    dummy_img = np.zeros((224, 224, 3), dtype=np.uint8)
    
    # Convert to base64
    _, buffer = cv2.imencode('.jpg', dummy_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # Test detection
    result = detector.detect_pose_from_base64(f"data:image/jpeg;base64,{img_base64}")
    
    if result.get('success'):
        print(f"✅ Detection works!")
        print(f"   Detected: {result.get('pose_name')}")
        print(f"   Confidence: {result.get('confidence', 0)*100:.1f}%")
    else:
        print(f"⚠️  Detection returned: {result.get('error', 'Unknown error')}")
        
except Exception as e:
    print(f"❌ Detection test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("  TEST COMPLETE")
print("="*60)
print("\nIf all tests passed, the API should work!")
print("Now restart your Flask app: python app.py")
print("="*60)
