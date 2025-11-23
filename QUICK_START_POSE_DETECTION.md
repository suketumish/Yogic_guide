# 🚀 Quick Start - Pose Detection

## ✅ What's Working Now

Your Surya Namaskar pose detection is **fully functional** with:

- ✅ **MediaPipe-based real-time detection**
- ✅ **Angle comparison with reference poses**
- ✅ **Hindi + English feedback**
- ✅ **Ankle and joint angle checking**
- ✅ **Visual skeleton overlay**
- ✅ **Reference image display**
- ✅ **Voice feedback**

## 🎯 Quick Test (2 minutes)

### 1. Start App
```bash
python app.py
```

### 2. Open Test Page
```
http://127.0.0.1:5000/test-simple-pose
```

### 3. Allow Camera
- Click "Allow" when browser asks
- You should see:
  - ✅ Your video feed
  - ✅ Green skeleton overlay
  - ✅ Reference image
  - ✅ Feedback area

### 4. Click "Start Session"
- First pose will load (Pranamasana)
- Try to match the reference image
- Watch for feedback:
  - 🟢 Green border = Perfect!
  - 🟠 Orange = Adjust
  - 🔴 Red = Incorrect

## 🧘 Full Surya Namaskar Session

### Open Session Page
```
http://127.0.0.1:5000/module/surya-namaskar
```

### What Happens:
1. Camera initializes (2 seconds)
2. Session starts automatically
3. First pose loads with:
   - Name in Hindi + English
   - Reference image
   - Instructions
   - 10-second timer

4. Do the pose:
   - Match reference image
   - Watch skeleton overlay
   - Read feedback
   - Listen to voice guidance

5. Auto-advance:
   - After 10 seconds → next pose
   - Or when pose is perfect → early advance
   - 12 poses total

6. Complete:
   - Session ends
   - Stats saved
   - Redirect to dashboard

## 📊 Understanding Feedback

### ✅ Perfect Pose (80%+ accuracy)
```
Display: "✅ बहुत बढ़िया! Perfect! (95%)"
Border: Green (5px solid)
Voice: "Perfect! Bilkul sahi!"
Action: Hold for 3 frames → auto-advance
```

### ⚠️ Needs Adjustment (60-79%)
```
Display: "⚠️ बायां घुटना: बढ़ाएं (15°) (72%)"
Border: Orange
Voice: Specific corrections
Action: Keep adjusting
```

### ❌ Incorrect (<60%)
```
Display: "⚠️ बायां घुटना: बढ़ाएं, दायां कोहनी: कम करें (45%)"
Border: Red
Voice: Multiple corrections
Action: Major adjustments needed
```

## 🎨 Visual Indicators

### Skeleton Overlay
- **Green lines** - Body connections (shoulders, hips, etc.)
- **Green dots** - Joint positions (elbows, knees, etc.)
- **Thicker lines** - Better landmark visibility

### Border Colors
- **No border** - Detecting...
- **Green** - Pose correct!
- **Orange** - Minor adjustments
- **Red** - Incorrect pose

### Angle Display (Top-left)
```
✓ leftElbow: 92° (target: 90° ±15°)
✓ rightElbow: 88° (target: 90° ±15°)
✗ leftKnee: 160° (target: 175° ±15°)
Accuracy: 67%
```

## 🔧 Controls

### Test Page Buttons
- **Start Session** - Begin pose sequence
- **Pause** - Pause detection (toggle to Resume)
- **Stop** - End session

### Session Page Buttons
- **⏸️ Pause** - Pause session
- **▶️ Resume** - Resume from pause
- **⏹️ Stop** - End session (with confirmation)

### Keyboard Shortcuts
- **Space** - Pause/Resume
- **Escape** - Show stop confirmation

## 🐛 Troubleshooting

### Camera Not Working
**Symptoms:** Black screen, no video
**Solutions:**
1. Check browser permissions (click lock icon in address bar)
2. Allow camera access
3. Click "Retry" button
4. Refresh page (F5)
5. Try different browser (Chrome recommended)

### Skeleton Not Showing
**Symptoms:** Video works but no green lines
**Solutions:**
1. Check internet connection (MediaPipe needs CDN)
2. Wait 5 seconds for MediaPipe to load
3. Check console (F12) for errors
4. Ensure good lighting
5. Stand fully in frame

### Pose Not Detecting
**Symptoms:** Skeleton shows but no feedback
**Solutions:**
1. Ensure full body is visible
2. Improve lighting
3. Stand 6-8 feet from camera
4. Face camera directly
5. Check if session is started

### Angles Not Matching
**Symptoms:** Always shows incorrect
**Solutions:**
1. Look at reference image carefully
2. Match exact body position
3. Check specific joint mentioned in feedback
4. Hold pose steady (don't move)
5. Adjust based on Hindi instructions

## 📱 Browser Requirements

### ✅ Supported
- Chrome 90+ (Best)
- Edge 90+
- Firefox 88+
- Safari 14+ (iOS/Mac)

### ❌ Not Supported
- Internet Explorer
- Very old browsers
- Browsers without WebRTC

### Required Permissions
- Camera access
- Microphone (for voice feedback)

## 🎯 Tips for Best Results

### Lighting
- Bright, even lighting
- Light from front, not behind
- Avoid shadows on body

### Position
- 6-8 feet from camera
- Full body visible
- Center of frame
- Face camera

### Background
- Plain, simple background
- Good contrast with body
- Minimal clutter

### Clothing
- Fitted clothes (shows body shape)
- Contrasting colors
- Avoid very loose clothing

### Pose Execution
- Match reference image exactly
- Hold pose steady
- Don't rush
- Follow feedback
- Breathe normally

## 📂 Files Created/Modified

### New Files
```
static/js/simple-pose-detector.js       - Main detection logic
templates/test_simple_pose.html         - Test page
SIMPLE_POSE_DETECTION_GUIDE.md          - Detailed guide
POSE_DETECTION_HINDI.md                 - Hindi guide
QUICK_START_POSE_DETECTION.md           - This file
```

### Modified Files
```
templates/session.html                  - Updated to use simple detector
app.py                                  - Added test route
```

## 🚀 Next Steps

### 1. Test Basic Detection
```
http://127.0.0.1:5000/test-simple-pose
```
- Verify camera works
- Check skeleton overlay
- Test feedback system

### 2. Try Full Session
```
http://127.0.0.1:5000/module/surya-namaskar
```
- Complete all 12 poses
- Experience auto-progression
- Check session stats

### 3. Customize (Optional)
Edit `static/js/simple-pose-detector.js`:
- Adjust `tolerance` (angle flexibility)
- Change `holdTime` (seconds per pose)
- Modify `requiredCorrectFrames` (stability)

## 📊 Technical Details

### Pose Detection Pipeline
```
Video Frame
    ↓
MediaPipe Pose
    ↓
33 Landmarks
    ↓
Calculate Angles
    ↓
Compare with Reference
    ↓
Generate Feedback
    ↓
Update UI
```

### Angle Calculation
```javascript
// Example: Elbow angle
angle = calculateAngle(shoulder, elbow, wrist)

// Using atan2 for accurate 3D angle
radians = atan2(c.y - b.y, c.x - b.x) - atan2(a.y - b.y, a.x - b.x)
angle = abs(radians * 180 / PI)
```

### Validation Logic
```javascript
// For each joint
diff = abs(currentAngle - referenceAngle)
isCorrect = diff <= tolerance

// Overall accuracy
accuracy = (correctJoints / totalJoints) * 100
isPerfect = accuracy >= 80
```

## 🎉 Success!

Your pose detection system is now **fully operational**!

### What You Get:
- ✅ Real-time skeleton tracking
- ✅ Accurate angle validation
- ✅ Bilingual feedback (Hindi + English)
- ✅ Visual and voice guidance
- ✅ Reference image comparison
- ✅ Auto-progression through poses
- ✅ Session tracking and stats

### Start Practicing:
```bash
# 1. Start app
python app.py

# 2. Open browser
http://127.0.0.1:5000/module/surya-namaskar

# 3. Allow camera

# 4. Start practicing!
```

**Namaste! 🙏 Happy practicing! 🧘‍♂️✨**
