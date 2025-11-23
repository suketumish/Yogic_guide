# Yoga Hybrid System Integration Guide

## Overview
Aapke existing Surya Namaskar pose detection system mein trained yoga model ko integrate kar diya gaya hai.

## Files Created

### 1. `yoga_pose_api.py`
- Main API wrapper for yoga hybrid system
- Handles image processing and pose detection
- Base64 aur file-based detection support

### 2. `yoga_api_routes.py`
- Flask API endpoints
- Real-time detection support
- System status checking

### 3. `static/js/yoga-pose-detector.js`
- Frontend JavaScript integration
- Canvas-based detection
- Throttling aur performance optimization

## API Endpoints

### 1. Check System Status
```
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

### 2. Detect Pose (Real-time)
```
POST /api/yoga/detect-realtime
```
Request:
```json
{
  "frame": "base64_encoded_image"
}
```
Response:
```json
{
  "success": true,
  "pose_name": "tadasana",
  "display_name": "Tadasana",
  "confidence": 0.95,
  "method": "hybrid"
}
```

### 3. Detect Pose (Full)
```
POST /api/yoga/detect
```
Request:
```json
{
  "image": "base64_encoded_image"
}
```
Response:
```json
{
  "success": true,
  "pose_name": "tadasana",
  "confidence": 0.95,
  "image_confidence": 0.93,
  "keypoint_confidence": 0.97,
  "method": "fusion",
  "feedback": "Excellent! Perfect Tadasana detected..."
}
```

### 4. Get Available Poses
```
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

## Integration Steps

### Step 1: Complete Model Training

Pehle ensure karo ki dono models trained hain:

```bash
cd yoga_hybrid_system

# 1. Extract keypoints (if not done)
python extract_keypoints.py

# 2. Train keypoint model (if not done)
python train_keypoint_model.py
```

Required files in `yoga_hybrid_system/models/`:
- `yoga_model_final.h5` ✓ (Already trained)
- `keypoint_mlp_classifier.pkl`
- `keypoint_mlp_scaler.pkl`
- `keypoint_mlp_label_encoder.pkl`
- `class_names.json`
- `keypoint_mlp_metadata.json`

### Step 2: Test API

Server start karo:
```bash
python app.py
```

Test endpoints:
```bash
# Check status
curl http://localhost:5000/api/yoga/status

# Get available poses
curl http://localhost:5000/api/yoga/poses
```

### Step 3: Frontend Integration

Existing `pose-detection.js` mein add karo:

```javascript
// Load yoga detector
const yogaDetector = window.yogaPoseDetector;

// In your pose detection loop
async function detectYogaPose() {
    if (canvas && yogaDetector.isReady) {
        const result = await yogaDetector.detectPoseFromCanvas(canvas);
        
        if (result.success) {
            console.log('Detected:', result.display_name);
            console.log('Confidence:', result.confidence);
            
            // Update UI
            updatePoseDisplay(result.display_name, result.confidence);
        }
    }
}

// Call every 1-2 seconds
setInterval(detectYogaPose, 1000);
```

### Step 4: Update Session Template

`templates/session.html` mein add karo:

```html
<!-- Add yoga detector script -->
<script src="{{ url_for('static', filename='js/yoga-pose-detector.js') }}"></script>

<!-- Add pose display -->
<div id="yogaPoseDisplay" class="pose-info">
    <h3 id="detectedPose">Detecting...</h3>
    <div class="confidence-bar">
        <div id="confidenceLevel" style="width: 0%"></div>
    </div>
    <p id="poseConfidence">0%</p>
</div>
```

## Usage Example

### Simple Detection
```javascript
// Initialize
const detector = new YogaPoseDetector();

// Wait for ready
await detector.checkSystemStatus();

// Detect from canvas
const result = await detector.detectPoseFromCanvas(myCanvas);

if (result.success) {
    console.log(`Pose: ${result.display_name}`);
    console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
}
```

### With Surya Namaskar Sequence
```javascript
// In your existing pose sequence
const suryaNamaskarPoses = [
    'tadasana',
    'urdhva_hastasana',
    'uttanasana',
    'ashwa_sanchalanasana',
    // ... etc
];

let currentPoseIndex = 0;

async function checkPose() {
    const result = await yogaDetector.detectPoseFromCanvas(canvas);
    
    if (result.success) {
        const expectedPose = suryaNamaskarPoses[currentPoseIndex];
        
        if (result.pose_name === expectedPose && result.confidence > 0.75) {
            // Correct pose detected!
            console.log('✅ Correct pose!');
            currentPoseIndex++;
            
            // Move to next pose
            if (currentPoseIndex < suryaNamaskarPoses.length) {
                showNextPose();
            } else {
                completeSequence();
            }
        }
    }
}
```

## Performance Tips

1. **Throttling**: Detection har 1-2 seconds mein karo, har frame mein nahi
2. **Image Quality**: 640x480 resolution sufficient hai
3. **Confidence Threshold**: 0.75+ ko accept karo
4. **Error Handling**: Network errors ko gracefully handle karo

## Troubleshooting

### System Not Ready
```
⚠️  Yoga Detection System Not Ready
```
**Solution**: Models train karo:
```bash
cd yoga_hybrid_system
python extract_keypoints.py
python train_keypoint_model.py
```

### Low Confidence
```
Confidence: 45%
```
**Solution**:
- Better lighting ensure karo
- Full body visible ho
- Camera se proper distance maintain karo

### API Errors
```
Error: 500 Internal Server Error
```
**Solution**:
- Check server logs
- Verify model files exist
- Check Python dependencies

## Next Steps

1. ✅ Models train karo (if not done)
2. ✅ API test karo
3. ✅ Frontend integrate karo
4. ✅ UI update karo
5. ✅ Test with real poses

## Support

Issues face ho to:
1. Check server logs: `python app.py`
2. Check browser console
3. Verify model files in `yoga_hybrid_system/models/`
4. Test API endpoints directly

## Available Poses (107 total)

Kuch popular poses:
- tadasana (Mountain Pose)
- vriksasana (Tree Pose)
- trikonasana (Triangle Pose)
- virabhadrasana (Warrior Poses)
- adho_mukha_svanasana (Downward Dog)
- bhujangasana (Cobra Pose)
- balasana (Child's Pose)
- savasana (Corpse Pose)
- ... and 99 more!

Full list: `GET /api/yoga/poses`
