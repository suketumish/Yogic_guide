# Yoga Pose Detection Debugging Guide

## Issue: Pose detection nahi ho raha frontend pe

### Quick Diagnosis Steps

1. **Browser Console Check karo:**
   - Open browser (Chrome/Edge recommended)
   - Go to: http://127.0.0.1:5000/module/surya-namaskar
   - Press F12 to open Developer Tools
   - Go to Console tab
   - Check for these messages:

   **Expected Messages:**
   ```
   ✅ Video and canvas elements found
   ✅ MediaPipe Pose library loaded
   🧘 Checking yoga pose detector status...
   ✅ Camera access granted
   ✅ Video playback started
   ```

   **Error Messages to Look For:**
   ```
   ❌ Video element not found
   ❌ MediaPipe Pose library failed to load
   ❌ Camera access denied
   ⚠️ Yoga pose detector not ready
   ```

2. **Network Tab Check karo:**
   - Developer Tools → Network tab
   - Refresh page
   - Check if these files load:
     - `/static/js/pose-detection.js` (should be 200 OK)
     - `/static/js/yoga-pose-detector.js` (should be 200 OK)
     - MediaPipe files from CDN (should be 200 OK)
   - Check API calls:
     - `/api/yoga/status` (should return JSON)

3. **Camera Permission Check:**
   - Browser address bar mein camera icon check karo
   - Make sure camera permission "Allow" hai
   - If blocked, click icon and select "Allow"

### Common Issues & Solutions

#### Issue 1: Camera Not Working
**Symptoms:**
- Black screen
- "Camera Not Available" message
- No video feed

**Solutions:**
```bash
# Check if camera is being used by another app
# Close Zoom, Teams, Skype, etc.

# Try different browser
# Chrome/Edge work best for MediaPipe
```

**Browser Settings:**
- Chrome: Settings → Privacy and Security → Site Settings → Camera
- Edge: Settings → Cookies and site permissions → Camera
- Make sure site has camera permission

#### Issue 2: Yoga Detection Not Working
**Symptoms:**
- Video works but no AI pose detection
- Console shows: "Yoga pose detector not ready"

**Reason:**
- Models not trained yet
- Simple detector not initialized

**Solution:**
```bash
# Check if simple_pose_detector.py exists
python simple_pose_detector.py

# Or train full models:
cd yoga_hybrid_system
python train_image_model.py
python train_keypoint_model.py
```

#### Issue 3: MediaPipe Not Loading
**Symptoms:**
- Console error: "Pose is not defined"
- No skeleton overlay on video

**Solutions:**
1. **Check Internet Connection:**
   - MediaPipe loads from CDN
   - Need active internet

2. **Check CDN URLs in session.html:**
   ```html
   <script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js"></script>
   ```

3. **Try Alternative CDN:**
   ```html
   <script src="https://unpkg.com/@mediapipe/pose@0.5.1675469404/pose.js"></script>
   ```

#### Issue 4: Pose Validation Not Working
**Symptoms:**
- Video works
- Skeleton shows
- But pose not validated

**Debug Steps:**
1. Open Console
2. Look for angle calculations:
   ```
   Angles: Loading...
   leftElbow: 180° (target: 180° ±10°)
   ```

3. Check if pose sequence loaded:
   ```javascript
   console.log(poseSequences['surya-namaskar']);
   ```

### Testing Checklist

- [ ] Server running on http://127.0.0.1:5000
- [ ] Browser console shows no errors
- [ ] Camera permission granted
- [ ] Video feed visible
- [ ] Green skeleton overlay visible
- [ ] Angle display showing in top-left
- [ ] Pose name updating
- [ ] Timer counting down

### Manual Testing Commands

```bash
# 1. Start server
python app.py

# 2. Test API endpoints
curl http://127.0.0.1:5000/api/yoga/status

# 3. Check if models exist
dir yoga_hybrid_system\models

# 4. Test simple detector
python -c "from simple_pose_detector import SimplePoseDetector; d = SimplePoseDetector(); print('OK' if d.initialize() else 'FAIL')"
```

### Browser Console Commands

Open browser console (F12) and run:

```javascript
// Check if video is playing
console.log('Video playing:', !video.paused);
console.log('Video dimensions:', video.videoWidth, 'x', video.videoHeight);

// Check if MediaPipe loaded
console.log('MediaPipe Pose:', typeof Pose !== 'undefined');

// Check if yoga detector loaded
console.log('Yoga Detector:', typeof window.yogaPoseDetector !== 'undefined');

// Check current pose
console.log('Current pose:', currentPoseIndex, '/', poseSequences[currentModule]?.length);

// Force pose detection
detectYogaPoseFromFrame();
```

### Advanced Debugging

#### Enable Verbose Logging

Add to `pose-detection.js`:
```javascript
// At top of file
const DEBUG_MODE = true;

// In onPoseResults
if (DEBUG_MODE) {
    console.log('Pose results:', results);
    console.log('Landmarks count:', results.poseLandmarks?.length);
}
```

#### Check Pose Angles

```javascript
// In browser console
function debugAngles() {
    if (window.lastLandmarks) {
        const angles = calculateAngles(window.lastLandmarks);
        console.table(angles);
    }
}

// Store landmarks in onPoseResults
window.lastLandmarks = results.poseLandmarks;
```

### Performance Issues

If detection is slow:

1. **Reduce MediaPipe complexity:**
   ```javascript
   pose.setOptions({
       modelComplexity: 1,  // Change from 2 to 1
       minDetectionConfidence: 0.5,
       minTrackingConfidence: 0.5
   });
   ```

2. **Increase detection interval:**
   ```javascript
   const YOGA_DETECTION_INTERVAL = 3000; // Change from 2000 to 3000
   ```

3. **Reduce video resolution:**
   ```javascript
   const constraints = {
       video: {
           width: { ideal: 480 },  // Change from 640
           height: { ideal: 360 }   // Change from 480
       }
   };
   ```

### Still Not Working?

1. **Clear browser cache:**
   - Ctrl + Shift + Delete
   - Clear cached images and files
   - Reload page

2. **Try incognito/private mode:**
   - Rules out extension conflicts

3. **Check server logs:**
   ```bash
   # Look for errors in terminal where app.py is running
   ```

4. **Restart everything:**
   ```bash
   # Stop server (Ctrl+C)
   # Close browser
   # Restart server
   python app.py
   # Open fresh browser window
   ```

### Contact Support

If issue persists, provide:
1. Browser console screenshot
2. Network tab screenshot
3. Server terminal output
4. Browser and OS version
