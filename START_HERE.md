# 🚀 Quick Start Guide - Yoga Pose Detection

## ⚡ Current Status

Your yoga pose detection system is **99% ready**! Here's what's working:

✅ Flask app running  
✅ MongoDB connected  
✅ TensorFlow 2.20.0 installed  
✅ 107 yoga poses trained  
✅ API routes registered  
✅ Frontend integrated  

⚠️ **One Issue**: MediaPipe not available for Python 3.13

## 🎯 Choose Your Path

### Option A: Quick Fix (Recommended) - Use Python 3.11

```bash
# Create new environment with Python 3.11
conda create -n yoga_app python=3.11 -y
conda activate yoga_app

# Install all dependencies
pip install -r requirements.txt

# Start the app
python app.py
```

Then open: `http://localhost:5000`

### Option B: Continue with Python 3.13 (Limited)

The app works but yoga detection is disabled until MediaPipe supports Python 3.13.

```bash
# Just run the app
python app.py
```

Everything works except real-time pose detection.

## 🧪 Test Yoga Detection

### 1. Check System Status

```bash
curl http://localhost:5000/api/yoga/status
```

**If working**, you'll see:
```json
{
  "ready": true,
  "message": "Yoga detection system is ready",
  "available_poses": 107
}
```

### 2. Test in Browser

1. Go to: `http://localhost:5000/yoga-test`
2. Click **"Start Camera"**
3. Allow camera access
4. Click **"Auto Detect: ON"**
5. Do a yoga pose (like standing straight for Tadasana)
6. Watch the detection results!

### 3. Use in Real Session

1. Login/Register at `http://localhost:5000`
2. Go to **Surya Namaskar** module
3. Start a session
4. Look for **"AI Detected Pose"** box (top-right)
5. Perform yoga poses
6. See real-time detection with confidence scores!

## 📊 What You'll See

```
┌──────────────────────┐
│  AI Detected Pose    │
│  Tadasana            │
│  ████████░░ 87%      │
└──────────────────────┘
```

**Confidence Colors**:
- 🟢 Green (85%+): Excellent
- 🟡 Orange (70-85%): Good
- 🔴 Red (<70%): Needs adjustment

## 🔧 Troubleshooting

### "Yoga detection system not initialized"

**Solution**: You're on Python 3.13. Use Python 3.11:
```bash
conda create -n yoga_app python=3.11 -y
conda activate yoga_app
pip install -r requirements.txt
python app.py
```

### "No module named 'mediapipe'"

**Solution**: Install MediaPipe:
```bash
pip install mediapipe opencv-python
```

### Camera not working

**Solution**: 
- Check browser permissions
- Use HTTPS or localhost
- Try different browser (Chrome recommended)

### Low detection confidence

**Tips**:
- Better lighting
- Full body in frame
- Clear background
- Hold pose steady for 2-3 seconds
- Face camera directly

## 📁 Project Structure

```
your-app/
├── app.py                          # Main Flask app
├── yoga_pose_api.py                # Yoga detection wrapper
├── yoga_api_routes.py              # API endpoints
├── requirements.txt                # Dependencies
│
├── yoga_hybrid_system/             # AI Models
│   ├── models/
│   │   ├── yoga_model_final.h5    # Image model (25MB)
│   │   ├── keypoint_mlp_*.pkl     # Keypoint models
│   │   └── class_names.json       # 107 poses
│   └── hybrid_inference.py        # Detection logic
│
├── static/js/
│   ├── yoga-pose-detector.js      # Frontend detection
│   └── pose-detection.js          # MediaPipe integration
│
└── templates/
    ├── session.html               # Session with detection
    └── yoga_test.html             # Test page
```

## 🎓 Available Poses (107 total)

Sample poses the system can detect:
- Tadasana (Mountain Pose)
- Vriksasana (Tree Pose)
- Trikonasana (Triangle Pose)
- Adho Mukha Svanasana (Downward Dog)
- Bhujangasana (Cobra Pose)
- Balasana (Child's Pose)
- Savasana (Corpse Pose)
- And 100 more!

## 📚 Documentation

- **Integration Status**: `INTEGRATION_STATUS.md`
- **Setup Guide**: `YOGA_SETUP_QUICK.md`
- **Testing Guide**: `TEST_POSE_DETECTION.md`
- **Complete System**: `YOGA_HYBRID_SYSTEM_COMPLETE.md`

## 🆘 Need Help?

### Quick Checks

```bash
# Check Python version
python --version

# Check TensorFlow
python -c "import tensorflow as tf; print(tf.__version__)"

# Check MediaPipe
python -c "import mediapipe; print('MediaPipe OK')"

# Test yoga detector
python -c "from yoga_pose_api import get_detector; d = get_detector(); print('Ready:', d._ensure_initialized())"
```

### Common Commands

```bash
# Start app
python app.py

# Install dependencies
pip install -r requirements.txt

# Create Python 3.11 environment
conda create -n yoga_app python=3.11 -y
conda activate yoga_app
```

## 🎉 You're Ready!

Once you have Python 3.11 with all dependencies installed:

1. **Start**: `python app.py`
2. **Open**: `http://localhost:5000`
3. **Test**: Go to `/yoga-test`
4. **Use**: Start a Surya Namaskar session
5. **Enjoy**: Real-time yoga pose detection! 🧘‍♀️

---

**Pro Tip**: The system detects poses every 2 seconds during sessions. Hold each pose steady for best results!
