"""
Setup script for Yoga Hybrid System
Automates environment setup and validation
"""

import os
import sys
import subprocess
import json

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    print("✅ Python version OK")
    return True

def install_dependencies():
    """Install required packages with fallback options"""
    print_header("Installing Dependencies")
    
    # First, upgrade pip
    print("Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Try default PyPI first
    print("Attempting to install from PyPI...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print("\n⚠️  Default installation failed")
        
        # Check if it's a network issue
        if "getaddrinfo failed" in str(e) or "connection" in str(e).lower():
            print("\n🔍 Network connectivity issue detected")
            print("\nTroubleshooting options:")
            print("  1. Check your internet connection")
            print("  2. Try flushing DNS: ipconfig /flushdns")
            print("  3. Disable VPN/proxy temporarily")
            print("  4. Try alternative mirrors (see below)")
            
            # Try alternative mirrors
            mirrors = [
                ("Tsinghua (China)", "https://pypi.tuna.tsinghua.edu.cn/simple"),
                ("Aliyun (China)", "https://mirrors.aliyun.com/pypi/simple/"),
                ("Douban (China)", "http://pypi.douban.com/simple/")
            ]
            
            print("\n🔄 Attempting alternative PyPI mirrors...")
            for name, url in mirrors:
                print(f"\nTrying {name}...")
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", 
                        "--index-url", url,
                        "--trusted-host", url.split("//")[1].split("/")[0],
                        "-r", "requirements.txt"
                    ], timeout=120)
                    print(f"\n✅ Dependencies installed successfully from {name}")
                    return True
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    print(f"   ✗ {name} failed")
                    continue
        
        # If all attempts fail
        print("\n❌ Failed to install dependencies automatically")
        print("\n📋 Manual installation steps:")
        print("  1. Check network connection")
        print("  2. Try manual install:")
        print("     pip install tensorflow>=2.13.0")
        print("     pip install opencv-python mediapipe flask")
        print("     pip install flask-login flask-sqlalchemy")
        print("     pip install python-dotenv google-generativeai pillow")
        print("\n  3. Or download wheels offline and install locally")
        print("  4. Re-run this setup after manual installation")
        
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    dirs = [
        'models',
        'data/train',
        'data/validate',
        'data/test',
        'outputs',
        'logs'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ {dir_path}")
    
    print("\n✅ Directories created")
    return True

def check_api_key():
    """Check for API key"""
    print_header("Checking API Configuration")
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key:
        print(f"✅ GEMINI_API_KEY found: {api_key[:10]}...")
        return True
    else:
        print("⚠️  GEMINI_API_KEY not set")
        print("\nTo enable LLM feedback:")
        print("  export GEMINI_API_KEY='your-key-here'  # Linux/Mac")
        print("  set GEMINI_API_KEY=your-key-here       # Windows")
        print("\nOr use --no-llm flag for rule-based feedback")
        return False

def verify_installation():
    """Verify key packages are installed"""
    print_header("Verifying Installation")
    
    packages = {
        'tensorflow': 'TensorFlow',
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'sklearn': 'scikit-learn',
        'pandas': 'Pandas',
        'numpy': 'NumPy'
    }
    
    all_ok = True
    missing = []
    
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} not found")
            all_ok = False
            missing.append(name)
    
    if not all_ok:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nYou can continue setup and install these manually later.")
        print("The system will work with partial functionality.")
    
    return all_ok

def check_dataset():
    """Check if dataset exists"""
    print_header("Checking Dataset")
    
    train_dir = 'data/train'
    
    if not os.path.exists(train_dir):
        print("⚠️  No training data found")
        print("\nTo train models, add images to:")
        print("  data/train/<pose_name>/image.jpg")
        print("  data/validate/<pose_name>/image.jpg")
        print("  data/test/<pose_name>/image.jpg")
        return False
    
    classes = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    
    if not classes:
        print("⚠️  No pose classes found in data/train/")
        return False
    
    print(f"✅ Found {len(classes)} pose classes:")
    for cls in classes:
        img_count = len([f for f in os.listdir(os.path.join(train_dir, cls)) 
                        if f.endswith(('.jpg', '.png', '.jpeg'))])
        print(f"   • {cls}: {img_count} images")
    
    return True

def check_models():
    """Check if trained models exist"""
    print_header("Checking Models")
    
    required_files = [
        'models/yoga_model_final.h5',
        'models/keypoint_mlp_classifier.pkl',
        'models/keypoint_mlp_scaler.pkl',
        'models/keypoint_mlp_label_encoder.pkl',
        'models/class_names.json',
        'models/keypoint_mlp_metadata.json'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} not found")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Models not found. To train:")
        print("  1. python train_image_model.py")
        print("  2. python extract_keypoints.py")
        print("  3. python train_keypoint_model.py")
    
    return all_exist

def create_sample_config():
    """Create sample configuration file"""
    print_header("Creating Sample Configuration")
    
    config = {
        "model_config": {
            "image_model_path": "models/yoga_model_final.h5",
            "keypoint_model_path": "models/keypoint_mlp_classifier.pkl",
            "img_size": 224,
            "confidence_threshold": 0.5
        },
        "inference_config": {
            "use_llm": True,
            "llm_provider": "gemini",
            "user_level": "beginner",
            "max_feedback_words": 60
        },
        "fusion_config": {
            "high_confidence_threshold": 0.85,
            "keypoint_confidence_threshold": 0.80,
            "disagreement_threshold": 0.2
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created config.json")
    return True

def print_next_steps(has_dataset, has_models):
    """Print next steps based on setup status"""
    print_header("Setup Complete!")
    
    if not has_dataset:
        print("📁 NEXT STEP: Prepare your dataset")
        print("   1. Create pose folders in data/train/")
        print("   2. Add 100+ images per pose")
        print("   3. Repeat for data/validate/ and data/test/")
        print("\n   Then run: python train_image_model.py")
    
    elif not has_models:
        print("🎓 NEXT STEP: Train your models")
        print("   1. python train_image_model.py      (2-3 hours)")
        print("   2. python extract_keypoints.py      (30-60 min)")
        print("   3. python train_keypoint_model.py   (10-30 min)")
    
    else:
        print("🎯 READY TO USE!")
        print("   python complete_pipeline.py --image your_pose.jpg")
        print("\n   Or start API server:")
        print("   python app_api.py")
    
    print("\n📚 Documentation:")
    print("   • QUICKSTART.md - Quick start guide")
    print("   • USAGE_GUIDE.md - Detailed usage")
    print("   • ARCHITECTURE.md - System design")

def main():
    """Main setup routine"""
    print("\n" + "🧘 "*20)
    print("  YOGA HYBRID SYSTEM - SETUP")
    print("🧘 "*20)
    
    # Run checks
    checks = [
        ("Python Version", check_python_version, True),  # Critical
        ("Dependencies", install_dependencies, False),    # Can be manual
        ("Directories", create_directories, True),        # Critical
        ("Installation", verify_installation, False),     # Can be partial
        ("API Key", check_api_key, False),               # Optional
        ("Configuration", create_sample_config, True)     # Critical
    ]
    
    failed_critical = False
    for name, check_func, is_critical in checks:
        result = check_func()
        if not result and is_critical:
            print(f"\n❌ Critical check failed: {name}")
            failed_critical = True
            break
    
    if failed_critical:
        print("\n⚠️  Setup incomplete due to critical failure")
        print("Please resolve the issue above and re-run setup.py")
        sys.exit(1)
    
    # Optional checks
    has_dataset = check_dataset()
    has_models = check_models()
    
    # Print next steps
    print_next_steps(has_dataset, has_models)
    
    print("\n✅ Setup complete!\n")

if __name__ == '__main__':
    main()
