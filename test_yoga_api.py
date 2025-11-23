"""
Quick test script to check yoga API initialization
"""

import os
import sys

print("=" * 60)
print("YOGA API INITIALIZATION TEST")
print("=" * 60)

# Check current directory
print(f"\n1. Current Directory: {os.getcwd()}")

# Check if yoga_hybrid_system exists
yoga_dir = os.path.join(os.getcwd(), 'yoga_hybrid_system')
print(f"\n2. Yoga System Directory: {yoga_dir}")
print(f"   Exists: {os.path.exists(yoga_dir)}")

# Check models directory
models_dir = os.path.join(yoga_dir, 'models')
print(f"\n3. Models Directory: {models_dir}")
print(f"   Exists: {os.path.exists(models_dir)}")

# Check model files
if os.path.exists(models_dir):
    print("\n4. Model Files:")
    image_model = os.path.join(models_dir, 'yoga_model_final.h5')
    keypoint_model = os.path.join(models_dir, 'keypoint_mlp_classifier.pkl')
    
    print(f"   Image Model: {os.path.exists(image_model)} - {image_model}")
    print(f"   Keypoint Model: {os.path.exists(keypoint_model)} - {keypoint_model}")

# Try importing
print("\n5. Testing Import:")
sys.path.insert(0, yoga_dir)

try:
    from hybrid_inference import YogaHybridSystem
    print("   ✅ YogaHybridSystem imported successfully")
    
    # Try initializing
    print("\n6. Testing Initialization:")
    system = YogaHybridSystem(
        image_model_path=os.path.join(models_dir, 'yoga_model_final.h5'),
        keypoint_model_path=os.path.join(models_dir, 'keypoint_mlp_classifier.pkl'),
        use_llm=False
    )
    print("   ✅ System initialized successfully")
    print(f"   Available poses: {len(system.class_names)}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
