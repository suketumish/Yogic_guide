#!/usr/bin/env python3
"""
System Check for Yoga Pose Detection
Verifies all dependencies and provides helpful feedback
"""

import sys
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check Python version"""
    print_header("Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11 and version.minor <= 12:
        print("✅ Perfect! Python 3.11-3.12 is ideal for this project")
        return True
    elif version.major == 3 and version.minor == 13:
        print("⚠️  Python 3.13 detected")
        print("   MediaPipe is not yet available for Python 3.13")
        print("   Recommendation: Use Python 3.11 or 3.12")
        return False
    elif version.major == 3 and version.minor < 11:
        print("⚠️  Python version is older than 3.11")
        print("   Some features may not work correctly")
        return False
    else:
        print("❌ Unsupported Python version")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False

def check_dependencies():
    """Check all required dependencies"""
    print_header("Dependencies")
    
    packages = {
        'Flask': 'flask',
        'TensorFlow': 'tensorflow',
        'NumPy': 'numpy',
        'OpenCV': 'cv2',
        'MediaPipe': 'mediapipe',
        'scikit-learn': 'sklearn',
        'Pandas': 'pandas',
        'Pillow': 'PIL',
        'joblib': 'joblib',
    }
    
    results = {}
    for display_name, import_name in packages.items():
        results[display_name] = check_package(display_name, import_name)
    
    return results

def check_models():
    """Check if trained models exist"""
    print_header("Trained Models")
    
    model_dir = os.path.join('yoga_hybrid_system', 'models')
    
    if not os.path.exists(model_dir):
        print(f"❌ Model directory not found: {model_dir}")
        return False
    
    required_files = [
        'yoga_model_final.h5',
        'keypoint_mlp_classifier.pkl',
        'keypoint_mlp_scaler.pkl',
        'keypoint_mlp_label_encoder.pkl',
        'class_names.json',
        'keypoint_mlp_metadata.json'
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = os.path.join(model_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            size_mb = size / (1024 * 1024)
            print(f"✅ {filename} ({size_mb:.1f} MB)")
        else:
            print(f"❌ {filename}: Not found")
            all_exist = False
    
    return all_exist

def check_yoga_system():
    """Check if yoga detection system can initialize"""
    print_header("Yoga Detection System")
    
    try:
        from yoga_pose_api import get_detector
        detector = get_detector()
        ready = detector._ensure_initialized()
        
        if ready:
            print("✅ Yoga detection system is ready!")
            poses = detector.get_available_poses()
            print(f"✅ {len(poses)} yoga poses available")
            return True
        else:
            print("⚠️  Yoga detection system not initialized")
            print("   Check dependencies and models above")
            return False
    except Exception as e:
        print(f"❌ Error initializing yoga system: {e}")
        return False

def print_recommendations(python_ok, deps_ok, models_ok, system_ok):
    """Print recommendations based on check results"""
    print_header("Recommendations")
    
    if not python_ok:
        print("\n🔧 Python Version Issue:")
        print("   1. Create Python 3.11 environment:")
        print("      conda create -n yoga_app python=3.11 -y")
        print("      conda activate yoga_app")
        print("   2. Reinstall dependencies:")
        print("      pip install -r requirements.txt")
    
    if not deps_ok:
        print("\n🔧 Missing Dependencies:")
        print("   Install all requirements:")
        print("      pip install -r requirements.txt")
    
    if not models_ok:
        print("\n🔧 Missing Models:")
        print("   Train the models:")
        print("      cd yoga_hybrid_system")
        print("      python train_image_model.py")
        print("      python extract_keypoints.py")
        print("      python train_keypoint_model.py")
    
    if python_ok and deps_ok and models_ok and system_ok:
        print("\n🎉 Everything is ready!")
        print("\n   Start the app:")
        print("      python app.py")
        print("\n   Then open:")
        print("      http://localhost:5000")
        print("\n   Test yoga detection:")
        print("      http://localhost:5000/yoga-test")

def main():
    """Main check routine"""
    print("\n" + "🧘 "*20)
    print("  YOGA POSE DETECTION - SYSTEM CHECK")
    print("🧘 "*20)
    
    # Run all checks
    python_ok = check_python_version()
    
    deps_results = check_dependencies()
    deps_ok = all(deps_results.values())
    
    models_ok = check_models()
    
    system_ok = False
    if python_ok and deps_ok and models_ok:
        system_ok = check_yoga_system()
    else:
        print_header("Yoga Detection System")
        print("⏭️  Skipped (fix issues above first)")
    
    # Print summary
    print_header("Summary")
    print(f"Python Version: {'✅' if python_ok else '❌'}")
    print(f"Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"Trained Models: {'✅' if models_ok else '❌'}")
    print(f"Yoga System: {'✅' if system_ok else '❌'}")
    
    # Print recommendations
    print_recommendations(python_ok, deps_ok, models_ok, system_ok)
    
    print("\n" + "="*60)
    print()

if __name__ == '__main__':
    main()
