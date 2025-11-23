# 📹 Camera & Pose Detection Troubleshooting

## Issue: "Pose detection on camera angle is not loading"

This means the camera feed or skeleton overlay isn't showing up. Here's how to fix it:

## 🔍 Quick Diagnosis

### Step 1: Test MediaPipe Loading

Visit the diagnostic page:
```
http://localhost:5000/mediapipe-test
```

This will show you:
- ✅ Which libraries loaded successfully
- ❌ Which libraries failed to load
- 📹 Live camera feed test
- 🦴 Skeleton detection test

### Step 2: Check Browser Console

1. Open browser console (F12)
2. Look for these messages:

**Good signs:**
```
✅ MediaPipe Pose library loaded
✅ Video and canvas elements found
✅ Camera access granted
✅ Video playback started
```

**Bad signs:**
```
❌ MediaPipe Pose library not loaded
❌ Camera initialization failed
⚠️  Waiting for MediaPipe Pose library...
```

## 🔧 Common Issues & Solutions

### Issue 1: MediaPipe Not Loading

**Symptoms:**
- Console shows "Waiting for MediaPipe Pose library..."
- No skeleton overlay appears
- Camera might work but no pose detection

**Causes:**
- Internet connection issues
- CDN blocked by firewall/proxy
- Browser cache issues

**Solutions:**

1. **Check Internet Connection**
   ```bash
   # Test if CDN is accessible
   curl https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js
   ```

2. **Clear Browser Cache**
   - Chrome: Ctrl+Shift+Delete → Clear cached images and files
   - Firefox: Ctrl+Shift+Delete → Cached Web Content
   - Edge: Ctrl+Shift+Delete → Cached images and files

3. **Try Different Browser**
   - Chrome (recommended)
   - Edge
   - Firefox

4. **Disable VPN/Proxy temporarily**
   - Some VPNs block CDN access
   - Try without VPN

5. **Check Firewall**
   - Allow access to `cdn.jsdelivr.net`
   - Allow WebRTC for camera access

### Issue 2: Camera Permission Denied

**Symptoms:**
- "Camera permission denied" error
- Video feed shows black screen
- Browser shows camera icon with X

**Solutions:**

1. **Grant Camera Permission**
   - Chrome: Click camera icon in address bar → Allow
   - Firefox: Click camera icon → Allow
   - Edge: Click camera icon → Allow

2. **Check System Settings**
   - Windows: Settings → Privacy → Camera → Allow apps
   - Mac: System Preferences → Security & Privacy → Camera
   - Linux: Check browser has camera access

3. **Use HTTPS or Localhost**
   - Camera only works on HTTPS or localhost
   - If using IP address, switch to localhost

### Issue 3: Camera In Use

**Symptoms:**
- "Camera is being used by another application"
- Camera works in other apps but not here

**Solutions:**

1. **Close Other Apps**
   - Close Zoom, Skype, Teams, etc.
   - Close other browser tabs using camera
   - Restart browser

2. **Check Task Manager**
   - Windows: Ctrl+Shift+Esc → Look for apps using camera
   - Mac: Activity Monitor → Search for camera apps
   - Linux: `lsof /dev/video0`

### Issue 4: No Camera Found

**Symptoms:**
- "No camera found" error
- Camera works in other apps

**Solutions:**

1. **Check Camera Connection**
   - Unplug and replug USB camera
   - Check if camera is enabled in BIOS
   - Try different USB port

2. **Update Drivers**
   - Windows: Device Manager → Camera → Update driver
   - Mac: Usually automatic
   - Linux: Check `v4l2` drivers

3. **Test Camera**
   - Windows: Camera app
   - Mac: Photo Booth
   - Linux: `cheese` or `guvcview`

### Issue 5: Skeleton Not Showing

**Symptoms:**
- Camera works
- No skeleton overlay
- Console shows MediaPipe loaded

**Solutions:**

1. **Check Canvas Element**
   - Open console
   - Type: `document.getElementById('poseCanvas')`
   - Should return canvas element, not null

2. **Check Video Dimensions**
   - Console: `video.videoWidth` and `video.videoHeight`
   - Should be > 0
   - If 0, video metadata not loaded

3. **Refresh Page**
   - Hard refresh: Ctrl+F5
   - Clear cache and refresh

4. **Check Lighting**
   - MediaPipe needs good lighting
   - Face camera directly
   - Remove obstructions

## 🧪 Testing Steps

### 1. Basic Test
```
http://localhost:5000/mediapipe-test
```
- Click "Start Camera"
- Should see video feed
- Should see skeleton overlay
- Should see green/red dots on joints

### 2. Full Test
```
http://localhost:5000/yoga-test
```
- Click "Start Camera"
- Allow camera access
- Click "Auto Detect: ON"
- Do a yoga pose (stand straight)
- Should see pose name and confidence

### 3. Session Test
```
http://localhost:5000/module/surya-namaskar
```
- Start session
- Allow camera
- Look for skeleton overlay
- Look for "AI Detected Pose" box

## 📊 Expected Behavior

### When Working Correctly:

1. **Camera Feed**
   - Live video showing you
   - Clear and smooth
   - No lag

2. **Skeleton Overlay**
   - Green lines connecting joints
   - Green dots on body points
   - Follows your movement

3. **Pose Detection**
   - "AI Detected Pose" box appears
   - Pose name updates every 2 seconds
   - Confidence percentage shows
   - Color-coded (green/orange/red)

4. **Console Output**
   ```
   ✅ MediaPipe Pose library loaded
   ✅ Video and canvas elements found
   ✅ Camera access granted
   ✅ Video playback started
   ✅ Yoga pose detector ready
   Yoga Pose Detected: Tadasana (87.3%)
   ```

## 🔍 Debug Commands

### Browser Console

```javascript
// Check MediaPipe
typeof Pose !== 'undefined'  // Should be true

// Check video
video.readyState  // Should be 4 (HAVE_ENOUGH_DATA)
video.videoWidth  // Should be > 0
video.videoHeight // Should be > 0

// Check canvas
canvas.width  // Should match video width
canvas.height // Should match video height

// Check yoga detector
window.yogaPoseDetector.isReady  // Should be true
```

### Python Console

```python
# Check if MediaPipe is installed
python -c "import mediapipe; print('OK')"

# Check TensorFlow
python -c "import tensorflow; print('OK')"

# Check yoga system
python -c "from yoga_pose_api import get_detector; d = get_detector(); print('Ready:', d._ensure_initialized())"
```

## 🆘 Still Not Working?

### Collect Debug Info

1. **Browser Console Log**
   - F12 → Console tab
   - Copy all messages
   - Look for errors (red text)

2. **Network Tab**
   - F12 → Network tab
   - Refresh page
   - Look for failed requests (red)
   - Check if MediaPipe scripts loaded

3. **System Info**
   - Browser: Chrome/Firefox/Edge + version
   - OS: Windows/Mac/Linux + version
   - Camera: Built-in/USB + model
   - Python: `python --version`

### Try These URLs

1. **MediaPipe Test**: `http://localhost:5000/mediapipe-test`
2. **Yoga Test**: `http://localhost:5000/yoga-test`
3. **API Status**: `http://localhost:5000/api/yoga/status`

### Check Server Logs

```bash
# Start app with verbose logging
python app.py

# Look for:
✅ Yoga API module loaded
✅ Yoga API routes registered
✅ Yoga Pose Detection API enabled
```

## 💡 Pro Tips

1. **Use Chrome** - Best MediaPipe support
2. **Good Lighting** - Helps detection accuracy
3. **Full Body in Frame** - Better skeleton tracking
4. **Stable Internet** - For CDN loading
5. **Close Other Apps** - Free up camera
6. **Allow Permissions** - Camera + microphone
7. **Use Localhost** - Not IP address
8. **Clear Cache** - If scripts won't load

## 📞 Quick Fixes

### Quick Fix 1: Hard Refresh
```
Ctrl + F5 (Windows/Linux)
Cmd + Shift + R (Mac)
```

### Quick Fix 2: Clear Cache
```
Ctrl + Shift + Delete
→ Clear cached images and files
→ Refresh page
```

### Quick Fix 3: Restart Browser
```
Close all browser windows
Reopen browser
Try again
```

### Quick Fix 4: Check Python Environment
```bash
# Make sure you're in the right environment
conda activate yoga_app  # If using conda

# Check dependencies
python check_system.py
```

## ✅ Success Checklist

- [ ] MediaPipe scripts loaded (check console)
- [ ] Camera permission granted (check browser icon)
- [ ] Video feed showing (see yourself)
- [ ] Skeleton overlay visible (green lines/dots)
- [ ] Pose detection working (see pose names)
- [ ] Confidence scores updating (every 2 seconds)
- [ ] No errors in console (no red text)

---

**If you've tried everything and it still doesn't work, visit `/mediapipe-test` for detailed diagnostics!**
