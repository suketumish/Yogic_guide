# 🧘 Yoga Pose Detection System

## Overview

This Flask application includes an **AI-powered yoga pose detection system** that can identify 107 different yoga poses in real-time using your webcam. The system uses a hybrid approach combining:

- **Image Classification** (CNN) - Analyzes the overall pose appearance
- **Keypoint Detection** (MediaPipe + MLP) - Tracks body joint positions
- **Intelligent Fusion** - Combines both methods for accurate results

## 🎯 Features

- ✅ **107 Yoga Poses** - Comprehensive pose library
- ✅ **Real-time Detection** - Live feedback during practice
- ✅ **Confidence Scoring** - Know how well you're doing
- ✅ **Session Integration** - Works with Surya Namaskar and other modules
- ✅ **Visual Feedback** - Color-coded confidence indicators
- ✅ **REST API** - Easy integration with other apps

## 🚀 Quick Start

### Step 1: Check Your System

```bash
# Run system check
python check_system.py

# Or on Windows
check_system.bat
```

This will tell you exactly what's working and what needs to be fixed.

### Step 2: Fix Python Version (if needed)

If you're on Python 3.13, create a Python 3.11 environment:

```bash
conda create -n yoga_app python=3.11 -y
conda activate yoga_app
pip install -r requirements.txt
```

### Step 3: Start the App

```bash
python app.py
```

### Step 4: Test It!

1. Open: `http://localhost:5000/yoga-test`
2. Click "Start Camera"
3. Allow camera access
4. Click "Auto Detect: ON"
5. Do a yoga pose!

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User's Webcam                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              MediaPipe Pose Detection                   │
│              (Extracts 33 keypoints)                    │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ▼                            ▼
┌────────────────────────┐  ┌────────────────────────────┐
│   Image Classifier     │  │  Keypoint Classifier       │
│   (CNN - TensorFlow)   │  │  (MLP - scikit-learn)      │
│   Confidence: 0.87     │  │  Confidence: 0.92          │
└────────────┬───────────┘  └────────────┬───────────────┘
             │                            │
             └──────────┬─────────────────┘
                        ▼
              ┌─────────────────────┐
              │  Intelligent Fusion │
              │  Final: Tadasana    │
              │  Confidence: 89%    │
              └─────────────────────┘
```

## 🎓 Supported Poses

The system can detect 107 yoga poses including:

**Standing Poses**:
- Tadasana (Mountain Pose)
- Vriksasana (Tree Pose)
- Trikonasana (Triangle Pose)
- Virabhadrasana I, II, III (Warrior Poses)

**Seated Poses**:
- Padmasana (Lotus Pose)
- Sukhasana (Easy Pose)
- Dandasana (Staff Pose)

**Prone Poses**:
- Bhujangasana (Cobra Pose)
- Dhanurasana (Bow Pose)
- Salabhasana (Locust Pose)

**Supine Poses**:
- Savasana (Corpse Pose)
- Setu Bandhasana (Bridge Pose)
- Halasana (Plow Pose)

**Balancing Poses**:
- Bakasana (Crow Pose)
- Natarajasana (Dancer Pose)
- Garudasana (Eagle Pose)

And 87 more!

## 🔌 API Endpoints

### Check System Status
```bash
GET /api/yoga/status
```

Response:
```json
{
  "ready": true,
  "message": "Yoga detection system is ready",
  "available_poses": 107
}
```

### Get Available Poses
```bash
GET /api/yoga/poses
```

Response:
```json
{
  "success": true,
  "poses": ["tadasana", "vriksasana", ...],
  "count": 107
}
```

### Detect Pose from Image
```bash
POST /api/yoga/detect
Content-Type: application/json

{
  "image": "base64_encoded_image_data"
}
```

Response:
```json
{
  "success": true,
  "pose_name": "tadasana",
  "confidence": 0.87,
  "feedback": "Excellent! Perfect Tadasana detected..."
}
```

### Real-time Detection
```bash
POST /api/yoga/detect-realtime
Content-Type: application/json

{
  "frame": "base64_encoded_frame_data"
}
```

Response:
```json
{
  "success": true,
  "pose_name": "tadasana",
  "display_name": "Tadasana (Mountain Pose)",
  "confidence": 0.87,
  "method": "hybrid"
}
```

## 🎨 Frontend Integration

### JavaScript Usage

```javascript
// Initialize detector
const detector = new YogaPoseDetector();

// Wait for initialization
await detector.waitForReady();

// Detect pose from canvas
const result = await detector.detectPoseFromCanvas(canvas);

if (result.success) {
    console.log(`Detected: ${result.display_name}`);
    console.log(`Confidence: ${result.confidence * 100}%`);
}
```

### HTML Integration

```html
<!-- Include the detector -->
<script src="/static/js/yoga-pose-detector.js"></script>

<!-- Display results -->
<div id="pose-display">
    <h3>AI Detected Pose</h3>
    <div id="pose-name">-</div>
    <div id="confidence-bar"></div>
    <div id="confidence-text">0%</div>
</div>
```

## 📁 File Structure

```
your-app/
├── app.py                          # Main Flask application
├── yoga_pose_api.py                # Yoga detection wrapper
├── yoga_api_routes.py              # API route definitions
├── check_system.py                 # System checker script
├── requirements.txt                # Python dependencies
│
├── yoga_hybrid_system/             # AI Model System
│   ├── models/                     # Trained models
│   │   ├── yoga_model_final.h5    # Image classifier (25MB)
│   │   ├── keypoint_mlp_*.pkl     # Keypoint models
│   │   └── class_names.json       # Pose names
│   ├── hybrid_inference.py        # Detection logic
│   ├── train_image_model.py       # Training scripts
│   └── extract_keypoints.py       # Keypoint extraction
│
├── static/
│   └── js/
│       ├── yoga-pose-detector.js  # Frontend detector
│       └── pose-detection.js      # MediaPipe integration
│
├── templates/
│   ├── session.html               # Session with detection
│   └── yoga_test.html             # Test page
│
└── docs/                           # Documentation
    ├── START_HERE.md              # Quick start guide
    ├── INTEGRATION_STATUS.md      # Current status
    ├── YOGA_SETUP_QUICK.md        # Setup instructions
    └── TEST_POSE_DETECTION.md     # Testing guide
```

## 🔧 Troubleshooting

### Issue: "Yoga detection system not initialized"

**Cause**: MediaPipe not available for Python 3.13

**Solution**:
```bash
conda create -n yoga_app python=3.11 -y
conda activate yoga_app
pip install -r requirements.txt
```

### Issue: "No module named 'mediapipe'"

**Solution**:
```bash
pip install mediapipe opencv-python
```

### Issue: Low detection confidence

**Tips**:
- Ensure good lighting
- Keep full body in frame
- Use plain background
- Hold pose steady for 2-3 seconds
- Face camera directly

### Issue: Camera not working

**Solutions**:
- Check browser permissions
- Use HTTPS or localhost
- Try Chrome browser
- Check if camera is in use by another app

## 📊 Performance

- **Detection Speed**: ~2 seconds per pose
- **Accuracy**: 85-95% for well-lit, clear poses
- **Model Size**: ~28 MB total
- **Memory Usage**: ~500 MB during inference
- **Supported Browsers**: Chrome, Edge, Firefox

## 🛠️ Development

### Training New Models

```bash
cd yoga_hybrid_system

# Train image classifier
python train_image_model.py

# Extract keypoints from dataset
python extract_keypoints.py

# Train keypoint classifier
python train_keypoint_model.py
```

### Testing

```bash
# Run system check
python check_system.py

# Test API
curl http://localhost:5000/api/yoga/status

# Test in browser
# Open: http://localhost:5000/yoga-test
```

## 📚 Documentation

- **Quick Start**: `START_HERE.md`
- **Integration Status**: `INTEGRATION_STATUS.md`
- **Setup Guide**: `YOGA_SETUP_QUICK.md`
- **Testing Guide**: `TEST_POSE_DETECTION.md`
- **Complete System**: `YOGA_HYBRID_SYSTEM_COMPLETE.md`

## 🤝 Contributing

To add new poses:

1. Add images to `yoga_hybrid_system/data/train/<pose_name>/`
2. Retrain models: `python train_image_model.py`
3. Update class names in `models/class_names.json`

## 📝 License

This yoga detection system is part of the Zen_Align application.

## 🆘 Support

Run the system checker for diagnostics:
```bash
python check_system.py
```

Check the documentation in the `docs/` folder for detailed guides.

## 🎉 Ready to Start?

1. **Check**: `python check_system.py`
2. **Fix**: Follow recommendations
3. **Start**: `python app.py`
4. **Test**: `http://localhost:5000/yoga-test`
5. **Enjoy**: Real-time yoga pose detection! 🧘‍♀️

---

**Made with ❤️ for yoga practitioners everywhere**
