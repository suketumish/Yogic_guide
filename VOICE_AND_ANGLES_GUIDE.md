# 🎙️ Voice Feedback & Angle Display Guide

## ✅ What's New

### 1. Bilingual Voice Feedback (Hindi + English)
Ab voice feedback **Hindi aur English dono mein** milta hai!

**Examples:**
```
✅ Perfect Pose:
   Hindi: "बहुत बढ़िया! बिल्कुल सही!"
   English: "Perfect! Excellent!"

⚠️ Adjustment Needed:
   Hindi: "बायां घुटना: बढ़ाएं"
   English: "Left Knee: increase"

🎯 Pose Change:
   Hindi: "अगले pose पर जा रहे हैं"
   English: "Moving to next pose"

🎉 Session Complete:
   Hindi: "सत्र पूरा हुआ! बहुत बढ़िया!"
   English: "Session complete! Excellent work!"
```

### 2. Visual Angle Display on Body
Ab **body pe directly angles dikhte hain**!

**Features:**
- 🟢 **Green circles** - Angle correct hai
- 🔴 **Red circles** - Angle incorrect hai
- **Current angle** - Circle ke andar (e.g., "92°")
- **Joint label** - Circle ke neeche (e.g., "L Elbow")
- **Target angle** - Label ke neeche (e.g., "Target: 90°")

**Example Display:**
```
     🟢
     92°
   L Elbow
  Target: 90°
```

### 3. Detailed Angle Panel
Right side panel mein **detailed angle information**:

```
📊 Accuracy: 85%
🎯 प्रणामासन
⏱️ Time: 8s
━━━━━━━━━━━━━━━━

📐 Angle Details:
✅ बायां कोहनी
   Current: 92°
   Target: 90°
   Diff: 2°

✅ दायां कोहनी
   Current: 88°
   Target: 90°
   Diff: 2°

❌ बायां घुटना
   Current: 160°
   Target: 175°
   Diff: 15°

⚠️ सुधार चाहिए:
1. बायां घुटना: बढ़ाएं (15°)
   Left Knee: increase (15°)
```

## 🎨 Visual Feedback System

### Border Colors
```
🔵 Blue (5px)   - Getting close (holding steady)
🟢 Green (5px)  - Perfect! All angles correct
🔴 Red (5px)    - Incorrect, needs adjustment
```

### Skeleton Colors
```
🟢 Green lines  - Body connections
🟢 Green dots   - Joint positions (5px radius)
```

### Angle Indicators
```
🟢 Green circle (25px) - Angle within tolerance
🔴 Red circle (25px)   - Angle needs adjustment
⚪ White text          - Current angle value
🟢/🔴 Colored text     - Joint label
⚫ Black text          - Target angle
```

## 🎙️ Voice Feedback Timing

### When Voice Speaks:

1. **Pose Load** (Every pose)
   ```
   Hindi: "छाती पर हाथ जोड़कर खड़े हों"
   English: "Stand with palms together at chest"
   ```

2. **Perfect Pose** (When stable)
   ```
   Hindi: "बहुत बढ़िया! बिल्कुल सही!"
   English: "Perfect! Excellent!"
   ```

3. **Major Corrections** (Accuracy < 60%, throttled to 8 seconds)
   ```
   Hindi: "बायां घुटना: बढ़ाएं"
   English: "Left Knee: increase"
   ```

4. **Pose Transition** (Moving to next)
   ```
   Hindi: "अगले pose पर जा रहे हैं"
   English: "Moving to next pose"
   ```

5. **Session Complete** (End)
   ```
   Hindi: "सत्र पूरा हुआ! बहुत बढ़िया!"
   English: "Session complete! Excellent work!"
   ```

### Voice Settings:
```javascript
Hindi:
  - Language: 'hi-IN'
  - Rate: 0.85 (slightly slower)
  - Pitch: 1.0 (normal)
  - Volume: 1.0 (full)

English:
  - Language: 'en-US'
  - Rate: 0.9 (normal)
  - Pitch: 1.0 (normal)
  - Volume: 1.0 (full)
```

## 📐 Angle Calculation

### Joints Tracked:
1. **Elbows** (कोहनी)
   - Left: Shoulder → Elbow → Wrist
   - Right: Shoulder → Elbow → Wrist

2. **Knees** (घुटना)
   - Left: Hip → Knee → Ankle
   - Right: Hip → Knee → Ankle

3. **Shoulders** (कंधा)
   - Left: Elbow → Shoulder → Hip
   - Right: Elbow → Shoulder → Hip

4. **Hips** (कूल्हा)
   - Left: Shoulder → Hip → Knee
   - Right: Shoulder → Hip → Knee

5. **Ankles** (टखना)
   - Left: Knee → Ankle → Foot
   - Right: Knee → Ankle → Foot

### Angle Formula:
```javascript
angle = atan2(c.y - b.y, c.x - b.x) - atan2(a.y - b.y, a.x - b.x)
angle = abs(angle * 180 / PI)
if (angle > 180) angle = 360 - angle
```

### Validation:
```javascript
diff = abs(currentAngle - referenceAngle)
isCorrect = diff <= tolerance  // ±15° default
```

## 🎯 Accuracy Calculation

### Formula:
```javascript
accuracy = (correctJoints / totalJoints) * 100
```

### Thresholds:
```
≥ 80% - ✅ Perfect! (Green)
60-79% - ⚠️ Good, minor adjustments (Orange)
< 60%  - ❌ Needs correction (Red)
```

### Stability:
```
requiredCorrectFrames = 3
// Need 3 consecutive frames with 80%+ accuracy
```

## 🔧 Customization

### Adjust Tolerance:
```javascript
// In simple-pose-detector.js
{
    name: 'Pranamasana',
    referenceAngles: { ... },
    tolerance: 15  // Change this (default: 15°)
}
```

### Adjust Voice Rate:
```javascript
// In speak() function
utterance.rate = 0.85;  // 0.5 to 2.0
```

### Adjust Feedback Throttle:
```javascript
// In checkPose() function
if (Date.now() - this.lastVoiceFeedback > 8000) {
    // Change 8000 (8 seconds) to your preference
}
```

## 📊 Display Examples

### Perfect Pose (85% accuracy):
```
Video Feed:
  - Green skeleton
  - Green border (5px)
  - Green circles on joints
  - All angles showing in green

Feedback:
  "✅ बहुत बढ़िया! Perfect! (85%)"

Angle Panel:
  📊 Accuracy: 85%
  ✅ सभी angles सही हैं!
  ✅ All angles perfect!

Voice:
  "बहुत बढ़िया! बिल्कुल सही!"
  "Perfect! Excellent!"
```

### Needs Adjustment (72% accuracy):
```
Video Feed:
  - Green skeleton
  - Red border (5px)
  - Mix of green/red circles
  - Incorrect angles in red

Feedback:
  "⚠️ बायां घुटना: बढ़ाएं (15°) (72%)"

Angle Panel:
  📊 Accuracy: 72%
  ⚠️ सुधार चाहिए:
  1. बायां घुटना: बढ़ाएं (15°)
     Left Knee: increase (15°)

Voice (if < 60%):
  "बायां घुटना: बढ़ाएं"
  "Left Knee: increase"
```

## 🎮 User Experience Flow

```
1. Pose Loads
   ↓
   Voice: "छाती पर हाथ जोड़कर खड़े हों"
   Voice: "Stand with palms together at chest"
   
2. User Does Pose
   ↓
   Skeleton appears (green)
   Angles show on body
   
3. Checking Angles
   ↓
   Red circles: Incorrect
   Green circles: Correct
   Border: Red (adjusting)
   
4. Getting Close
   ↓
   More green circles
   Border: Blue (holding steady)
   Feedback: "⏳ Hold steady... 2/3"
   
5. Perfect!
   ↓
   All green circles
   Border: Green
   Feedback: "✅ बहुत बढ़िया! Perfect!"
   Voice: "बहुत बढ़िया! बिल्कुल सही!"
   Voice: "Perfect! Excellent!"
   
6. Next Pose
   ↓
   Voice: "अगले pose पर जा रहे हैं"
   Voice: "Moving to next pose"
   (2 second pause)
   Next pose loads...
```

## 🐛 Troubleshooting

### Voice Not Working
**Problem:** No voice feedback
**Solutions:**
1. Check browser audio permissions
2. Unmute browser tab
3. Check system volume
4. Try Chrome (best support)
5. Check console for errors

### Angles Not Showing
**Problem:** No circles on body
**Solutions:**
1. Ensure session is started
2. Check if skeleton is visible
3. Verify pose has referenceAngles
4. Check canvas is not covered

### Wrong Angle Values
**Problem:** Angles seem incorrect
**Solutions:**
1. Ensure full body is visible
2. Face camera directly
3. Check lighting
4. Stand 6-8 feet away
5. Verify reference pose

## 💡 Tips for Best Experience

### For Voice Feedback:
1. **Quiet environment** - Reduce background noise
2. **Good speakers** - Clear audio output
3. **Listen carefully** - Both Hindi and English
4. **Follow instructions** - Adjust as told

### For Angle Display:
1. **Watch circles** - Green = good, Red = adjust
2. **Read values** - Current vs Target
3. **Check panel** - Detailed breakdown
4. **Focus on red** - Fix incorrect angles first

### For Accuracy:
1. **Match reference** - Look at image
2. **Hold steady** - Don't move too much
3. **Adjust slowly** - Small movements
4. **Be patient** - Wait for green border

## 🎉 Success Indicators

### You're Doing Great When:
- ✅ All circles are green
- ✅ Border is green (5px)
- ✅ Accuracy ≥ 80%
- ✅ Voice says "Perfect!"
- ✅ Feedback shows "बहुत बढ़िया!"
- ✅ Auto-advances to next pose

## 📞 Quick Reference

### Voice Commands (What You'll Hear):
```
Hindi                          | English
------------------------------|---------------------------
बहुत बढ़िया! बिल्कुल सही!      | Perfect! Excellent!
बायां घुटना: बढ़ाएं            | Left Knee: increase
दायां कोहनी: कम करें           | Right Elbow: decrease
अगले pose पर जा रहे हैं        | Moving to next pose
सत्र पूरा हुआ!                | Session complete!
```

### Angle Display Legend:
```
Symbol | Meaning
-------|------------------
🟢     | Correct angle
🔴     | Incorrect angle
✅     | Joint is perfect
❌     | Joint needs fix
⏳     | Hold steady
📊     | Accuracy meter
🎯     | Target pose
⏱️     | Time remaining
```

## 🚀 Start Using

```bash
# 1. Start app
python app.py

# 2. Open session
http://127.0.0.1:5000/module/surya-namaskar

# 3. Allow camera & audio

# 4. Watch for:
   - Green skeleton
   - Angle circles on body
   - Feedback in Hindi + English
   - Voice instructions

# 5. Follow feedback:
   - Match reference image
   - Adjust red circles to green
   - Listen to voice guidance
   - Hold until auto-advance
```

**Enjoy your enhanced yoga practice with bilingual voice feedback and visual angle display! 🧘‍♂️✨**
