# 🧘 Pose Detection Test Guide

## Problem: Session mein pose detect nahi ho raha

## Solution: Integration Complete! ✅

### Changes Made:

1. **`templates/session.html`**
   - Added `yoga-pose-detector.js` script
   - Loads before `pose-detection.js`

2. **`static/js/pose-detection.js`**
   - Added yoga detection integration
   - Real-time pose detection every 2 seconds
   - Visual display of detected pose
   - Confidence meter

### How It Works Now:

```
MediaPipe Pose Detection (Skeleton)
         ↓
    Every 2 seconds
         ↓
Yoga Hybrid Model (AI Detection)
         ↓
Display: Pose Name + Confidence
```

## Testing Steps:

### 1. Ensure Models Are Trained

```bash
cd yoga_hybrid_system

# Check if models exist
dir models

# Should see:
# - yoga_model_final.h5 ✅
# - keypoint_mlp_classifier.pkl
# - keypoint_mlp_scaler.pkl
# - class_names.json
```

**If keypoint models missing:**
```bash
python extract_keypoints.py
python train_keypoint_model.py
```

### 2. Start Server

```bash
python app.py
```

Look for:
```
✅ Yoga Pose Detection API enabled
🌐 Server: http://0.0.0.0:5000
```

### 3. Test on Test Page First

```
http://localhost:5000/yoga-test
```

1. Click "Start Camera"
2. Allow camera permission
3. Click "Auto Detect: ON"
4. Do a yoga pose (like Tadasana - standing straight)
5. Check if detection works

**Expected:**
- Pose name appears
- Confidence percentage shows
- Updates every 2 seconds

### 4. Test in Session

```
http://localhost:5000/module/surya-namaskar
```

1. Login if needed
2. Start session
3. Allow camera
4. Look for **AI Detected Pose** box (top-right corner)
5. Do any yoga pose
6. Should see:
   - Pose name
   - Confidence bar
   - Percentage

## Visual Indicators:

### In Session View:

```
┌─────────────────────────────────┐
│  Video Feed                     │
│                                 │
│  ┌──────────────────┐          │
│  │ AI Detected Pose │ ← Look   │
│  │ Tadasana         │   here!  │
│  │ ████████░░ 85%   │          │
│  └──────────────────┘          │
│                                 │
│  [Skeleton overlay]             │
└─────────────────────────────────┘
```

### Confidence Colors:

- 🟢 **Green (85%+)**: Excellent detection
- 🟡 **Orange (70-85%)**: Good detection
- 🔴 **Red (<70%)**: Needs adjustment

## Troubleshooting:

### "AI Detected Pose" box not appearing

**Check browser console (F12):**

```javascript
// Should see:
✅ Yoga pose detector ready
✅ Video and canvas elements found
✅ Pose correction system initialized
```

**If you see:**
```
⚠️  Yoga pose detector not ready - models not trained
```

**Solution:**
```bash
cd yoga_hybrid_system
python extract_keypoints.py
python train_keypoint_model.py
```

### Detection not updating

**Check console for:**
```
Yoga Pose Detected: Tadasana (85.3%)
```

**If not appearing:**
1. Check if camera is working (skeleton visible?)
2. Check if models are loaded (test page works?)
3. Check network tab for API errors

### Low confidence (<50%)

**Improve detection:**
- Better lighting
- Full body in frame
- Clear background
- Hold pose steady for 2-3 seconds
- Face camera directly

### API Errors

**Check server logs:**
```bash
python app.py
# Look for errors in output
```

**Test API directly:**
```bash
curl http://localhost:5000/api/yoga/status
```

**Expected response:**
```json
{
  "ready": true,
  "message": "Yoga detection system is ready",
  "available_poses": 107
}
```

## Debug Mode:

### Enable detailed logging:

Open browser console (F12) and run:

```javascript
// Check detector status
window.yogaPoseDetector.isReady

// Get current pose
window.yogaPoseDetector.getCurrentPose()

// Manual detection
window.yogaPoseDetector.detectPoseFromCanvas(window.canvas)
```

### Check if script loaded:

```javascript
// Should return function
typeof window.yogaPoseDetector

// Should return object
window.yogaPoseDetector
```

## Performance Tips:

1. **Detection Interval**: Currently 2 seconds
   - Good balance between accuracy and performance
   - Can adjust in `pose-detection.js`:
   ```javascript
   const YOGA_DETECTION_INTERVAL = 2000; // Change this
   ```

2. **Canvas Quality**: 640x480 is optimal
   - Higher = better accuracy but slower
   - Lower = faster but less accurate

3. **Browser**: Chrome/Edge recommended
   - Better WebGL support
   - Faster inference

## What You Should See:

### Successful Detection:

```
Console:
✅ Yoga pose detector ready
Yoga Pose Detected: Tadasana (87.5%)
Yoga Pose Detected: Vriksasana (82.3%)
Yoga Pose Detected: Trikonasana (91.2%)

Screen:
┌──────────────────┐
│ AI Detected Pose │
│ Tadasana         │
│ ████████░░ 87%   │
└──────────────────┘
```

### Failed Detection:

```
Console:
⚠️  Yoga pose detector not ready - models not trained

Screen:
(No AI detection box appears)
```

## Next Steps:

1. ✅ Test on `/yoga-test` page
2. ✅ Verify models are trained
3. ✅ Test in actual session
4. ✅ Try different poses
5. ✅ Check confidence scores

## Quick Commands:

```bash
# Check if models exist
dir yoga_hybrid_system\models

# Train missing models
cd yoga_hybrid_system
python extract_keypoints.py
python train_keypoint_model.py

# Start server
cd ..
python app.py

# Test API
curl http://localhost:5000/api/yoga/status
```

## Support:

If still not working:

1. Check `YOGA_INTEGRATION_GUIDE.md` for detailed setup
2. Check `YOGA_SETUP_QUICK.md` for quick start
3. Verify all model files exist
4. Check browser console for errors
5. Check server logs for API errors

---

**Status Check Command:**
```bash
curl http://localhost:5000/api/yoga/status
```

**Expected if working:**
```json
{"ready": true, "message": "Yoga detection system is ready", "available_poses": 107}
```

**Expected if not ready:**
```json
{"ready": false, "message": "Yoga detection system not initialized. Please train models first."}
```
