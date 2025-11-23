# Yoga Posture Detection System - Complete Architecture

## Project Overview

This is a **hybrid AI system** that combines three powerful approaches for accurate yoga posture detection and intelligent feedback:

1. **Image-based Deep Learning Classifier** - Visual pattern recognition
2. **Pose Keypoint Analysis** - Geometric body alignment verification
3. **LLM-based Feedback Generator** - Natural language coaching

---

## Why Hybrid Approach is Superior

### Single Model Limitations:
- **Image-only**: Can misclassify similar-looking poses, struggles with occlusion
- **Keypoint-only**: Fails with poor lighting, requires visible joints, no context understanding
- **LLM-only**: Cannot "see" the pose, relies entirely on descriptions

### Hybrid Advantages:
✅ **Redundancy**: If one model fails, others compensate  
✅ **Accuracy**: Cross-validation between visual and geometric features  
✅ **Explainability**: Keypoints provide measurable angles for feedback  
✅ **Natural Coaching**: LLM converts technical data into human-friendly tips  
✅ **Robustness**: Works in varied lighting, angles, and body types

---

## SECTION 1: PIPELINE EXPLANATION

### A) IMAGE CLASSIFICATION MODEL

#### Dataset Structure
```
data/
├── train/
│   ├── warrior2/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   ├── tree/
│   ├── downdog/
│   └── ...
├── validate/
│   ├── warrior2/
│   ├── tree/
│   └── ...
└── test/
    ├── warrior2/
    ├── tree/
    └── ...
```

#### Image Preprocessing
- Resize to 224x224 (MobileNetV2) or 240x240 (EfficientNet)
- Normalize pixel values to [0, 1]
- Data augmentation:
  - Random rotation (±15°)
  - Random zoom (0.8-1.2x)
  - Horizontal flip
  - Brightness adjustment (±20%)
  - Slight translation

#### Transfer Learning Strategy
**Base Model**: MobileNetV2 (lightweight) or EfficientNetB0 (higher accuracy)

**Phase 1 - Feature Extraction (Freeze Base)**:
- Load pretrained ImageNet weights
- Freeze all convolutional layers
- Add custom classification head:
  - GlobalAveragePooling2D
  - Dense(256, activation='relu')
  - Dropout(0.5)
  - Dense(num_classes, activation='softmax')
- Train only the head for 10-15 epochs

**Phase 2 - Fine-Tuning**:
- Unfreeze last 30-50 layers of base model
- Use very low learning rate (1e-5)
- Train for 20-30 more epochs
- Monitor validation accuracy to prevent overfitting

#### Loss & Optimizer
- **Loss**: Categorical Crossentropy (multi-class)
- **Optimizer**: Adam with learning rate schedule
  - Phase 1: lr=1e-3
  - Phase 2: lr=1e-5
- **Metrics**: Accuracy, Top-3 Accuracy, F1-Score per class

#### Evaluation
- Confusion matrix on test set
- Per-class precision/recall
- Misclassification analysis
- Confidence distribution plots

---

### B) KEYPOINT MODEL

#### MediaPipe Pose Landmarks (33 keypoints)
```
0: nose, 1-2: eyes, 3-4: ears, 5-6: shoulders
7-8: elbows, 9-10: wrists, 11-12: hips
13-14: knees, 15-16: ankles, 17-22: feet
23-28: hands, 29-32: feet details
```

#### Keypoint Extraction Pipeline
1. **Detection**: MediaPipe Pose detects person in frame
2. **Landmark Extraction**: 33 (x, y, z, visibility) coordinates
3. **Normalization**: 
   - Center on hip midpoint
   - Scale by torso height
   - Rotation-invariant alignment
4. **Feature Engineering**:
   - Raw coordinates (99 features: 33 × 3)
   - Joint angles (15-20 key angles)
   - Limb ratios
   - Symmetry scores

#### Key Angle Calculations

**Knee Angle** (for Warrior poses):
```python
angle = calculate_angle(hip, knee, ankle)
# Ideal: 90° for Warrior2, 120-140° for Warrior1
```

**Hip Angle** (for lunges):
```python
angle = calculate_angle(shoulder, hip, knee)
# Ideal: 170-180° for straight back leg
```

**Elbow Angle** (for Plank, Chaturanga):
```python
angle = calculate_angle(shoulder, elbow, wrist)
# Ideal: 90° for Chaturanga, 180° for Plank
```

**Torso Alignment** (for standing poses):
```python
angle = calculate_angle(hip, shoulder, vertical_reference)
# Ideal: 0-10° for upright poses
```

**Spine Curvature**:
```python
spine_angle = calculate_angle(hip, mid_back, shoulder)
# Detect rounded back vs. neutral spine
```

#### Keypoint Classifier
- **Model**: Multi-Layer Perceptron (MLP) or SVM
- **Input**: 99 normalized coordinates + 20 angles = 119 features
- **Architecture** (MLP):
  - Dense(256, relu) → Dropout(0.3)
  - Dense(128, relu) → Dropout(0.3)
  - Dense(64, relu)
  - Dense(num_classes, softmax)
- **Training**: 80/20 train/val split on keypoint CSV
- **Advantage**: Fast inference, interpretable features

---

### C) LLM FEEDBACK SYSTEM

#### Input JSON Structure
```json
{
  "pose_detected": "warrior2",
  "confidence": {
    "image_model": 0.92,
    "keypoint_model": 0.87,
    "hybrid": 0.89
  },
  "keypoint_angles": {
    "front_knee": 95,
    "back_knee": 178,
    "front_hip": 88,
    "back_hip": 175,
    "torso_vertical": 8,
    "arms_horizontal": 172
  },
  "ideal_angles": {
    "front_knee": 90,
    "back_knee": 180,
    "front_hip": 90,
    "back_hip": 180,
    "torso_vertical": 0,
    "arms_horizontal": 180
  },
  "issues_detected": [
    "front_knee_slightly_forward",
    "torso_slight_lean"
  ],
  "user_level": "beginner"
}
```

#### LLM Prompt Template
```
You are a certified yoga instructor providing posture feedback.

Pose: {pose_name}
User Level: {user_level}

Current Angles:
- Front knee: {front_knee}° (ideal: 90°)
- Back leg: {back_knee}° (ideal: 180°)
- Torso alignment: {torso}° from vertical (ideal: 0°)

Issues Detected: {issues_list}

Provide 2-3 friendly, actionable corrections in simple language. 
Be encouraging and specific. Keep it under 50 words.
```

#### Sample LLM Feedback Messages

**Warrior 2 - Good Form**:
> "Excellent Warrior 2! Your front knee is perfectly aligned over your ankle at 90°, and your back leg is strong and straight. Your arms are beautifully extended. Hold this for 5 more breaths!"

**Warrior 2 - Knee Forward**:
> "Nice effort! Your front knee is tracking a bit forward (95°). Try shifting your hips back slightly so your knee stays directly over your ankle. This protects your knee joint."

**Downward Dog - Rounded Back**:
> "Good start! I notice your spine is slightly rounded (25° curve). Try bending your knees a bit and lifting your tailbone higher. Focus on lengthening your spine rather than straightening your legs."

**Tree Pose - Balance Issue**:
> "You're doing great! Your standing leg is strong. If you're wobbling, try focusing on a fixed point ahead and engaging your core. It's okay to use a wall for support while building strength."

**Plank - Hips Low**:
> "Strong plank! Your hips are dipping about 15° below neutral. Engage your core and imagine a straight line from head to heels. Think about lifting your belly button toward your spine."

**Triangle Pose - Torso Rotation**:
> "Beautiful extension! Your torso is rotated about 30° forward. Try opening your chest more toward the ceiling by stacking your shoulders. Imagine your body between two panes of glass."

**Cobra - Shoulders Tense**:
> "Nice backbend! Your shoulders are slightly elevated (15° higher than ideal). Roll them back and down, away from your ears. This opens your chest and protects your neck."

**Chair Pose - Knees Forward**:
> "Powerful Chair Pose! Your knees are tracking forward past your toes (105° angle). Sit back more like you're sitting in a chair, keeping your weight in your heels. You should be able to see your toes."

**Warrior 1 - Hip Alignment**:
> "Strong stance! Your back hip is open about 35° to the side. Try rotating your back foot in slightly and squaring both hips forward. This deepens the hip flexor stretch."

**Child's Pose - Tension**:
> "Restful pose! I notice some tension in your shoulders (20° elevation). Let your forehead rest completely on the mat and allow your shoulders to melt down. This is your recovery pose—fully surrender."

**Bridge Pose - Knees Wide**:
> "Great lift! Your knees are splaying outward about 25°. Place a block between your thighs or imagine squeezing a ball. This engages your inner thighs and protects your lower back."

**Pigeon Pose - Uneven Hips**:
> "Deep stretch! Your hips are tilted about 18° to one side. Try placing a folded blanket under your right hip to level your pelvis. Even hips = safer, deeper stretch."

**Crow Pose - Weight Distribution**:
> "Brave attempt! Your weight is too far back (center of gravity 12cm behind hands). Shift forward more, bringing your shoulders over your wrists. Look forward, not down!"

**Camel Pose - Neck Compression**:
> "Beautiful backbend! Be careful not to drop your head too far back (35° hyperextension). Keep length in your neck by lifting through your chest first. Your gaze can be slightly upward."

**Side Plank - Hip Drop**:
> "Strong hold! Your hips are sagging about 20° below alignment. Engage your obliques and lift your hips higher. Imagine pushing the floor away with your supporting hand."

---

### D) HYBRID DECISION LOGIC

#### Confidence-Based Fusion

**Rule 1: High Confidence Agreement**
```python
if image_conf > 0.85 and keypoint_conf > 0.80:
    if image_pred == keypoint_pred:
        final_pred = image_pred
        final_conf = (image_conf + keypoint_conf) / 2
        status = "HIGH_CONFIDENCE"
```

**Rule 2: Disagreement - Favor Higher Confidence**
```python
if image_pred != keypoint_pred:
    if abs(image_conf - keypoint_conf) > 0.2:
        final_pred = max(image_conf, keypoint_conf)
        final_conf = max(image_conf, keypoint_conf) * 0.9
        status = "MODERATE_CONFIDENCE"
```

**Rule 3: Both Low Confidence**
```python
if image_conf < 0.6 and keypoint_conf < 0.6:
    final_pred = "UNCERTAIN"
    final_conf = 0.0
    status = "NEEDS_BETTER_IMAGE"
```

**Rule 4: Keypoint Priority for Geometric Poses**
```python
geometric_poses = ["warrior2", "triangle", "tree", "plank"]
if pose in geometric_poses and keypoint_conf > 0.75:
    final_pred = keypoint_pred
    final_conf = keypoint_conf
    status = "KEYPOINT_PRIORITY"
```

#### Error Detection Rules

**Knee Alignment** (Warrior poses):
```python
if front_knee_angle < 85:
    issues.append("knee_too_bent")
elif front_knee_angle > 100:
    issues.append("knee_not_bent_enough")

if knee_over_ankle_distance > 5cm:
    issues.append("knee_forward_of_ankle")
```

**Back Alignment**:
```python
if spine_curvature > 20:
    issues.append("rounded_back")
elif spine_curvature < -15:
    issues.append("excessive_arch")
```

**Hip Alignment**:
```python
hip_tilt = abs(left_hip_y - right_hip_y)
if hip_tilt > 10:
    issues.append("uneven_hips")
```

**Shoulder Position**:
```python
if shoulder_elevation > 15:
    issues.append("shoulders_raised")
```

---

## SECTION 2: DATASET DESCRIPTION

### Required Structure
- **Minimum**: 100 images per pose class
- **Recommended**: 300-500 images per pose class
- **Image Format**: JPG/PNG, RGB
- **Resolution**: Minimum 224x224, recommended 640x480+
- **Variety**: Different people, angles, lighting, backgrounds

### Data Collection Tips
1. Multiple angles (front, side, 45°)
2. Different body types and flexibility levels
3. Indoor and outdoor lighting
4. Plain and complex backgrounds
5. Correct and slightly incorrect forms (for error detection)

---

## SECTION 3: TRAINING STRATEGY

### Phase 1: Image Model Training (2-3 hours on GPU)
1. Load and preprocess dataset
2. Train classification head (10 epochs)
3. Fine-tune base model (20 epochs)
4. Evaluate on test set
5. Convert to TFLite for deployment

### Phase 2: Keypoint Model Training (30 minutes)
1. Extract keypoints from all training images
2. Save as CSV with labels
3. Train MLP classifier
4. Validate on test keypoints
5. Export model

### Phase 3: Hybrid Integration (1 hour)
1. Load both models
2. Implement fusion logic
3. Test on validation set
4. Tune confidence thresholds
5. Benchmark inference speed

### Phase 4: LLM Integration (30 minutes)
1. Set up API credentials (Gemini/OpenAI)
2. Create prompt templates
3. Test feedback generation
4. Implement caching for common poses

---

## SECTION 4: EVALUATION METRICS

### Image Model
- **Accuracy**: Overall classification accuracy
- **Per-Class F1**: Identify weak classes
- **Confusion Matrix**: See misclassification patterns
- **Top-3 Accuracy**: Useful for similar poses

### Keypoint Model
- **Accuracy**: On keypoint-only classification
- **Angle RMSE**: Root mean square error for angle predictions
- **Detection Rate**: % of images where keypoints detected

### Hybrid System
- **Agreement Rate**: % where both models agree
- **Confidence Distribution**: Histogram of final confidences
- **Error Detection Accuracy**: % of real errors caught
- **User Satisfaction**: Feedback quality ratings

---

## SECTION 5: DEPLOYMENT GUIDE

### Web Deployment (Flask/FastAPI)
```python
# app.py
@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['image']
    result = hybrid_inference(image)
    feedback = generate_llm_feedback(result)
    return jsonify({
        'pose': result['pose'],
        'confidence': result['confidence'],
        'feedback': feedback
    })
```

### Mobile Deployment (TFLite)
1. Convert models to TFLite format
2. Integrate MediaPipe for keypoints
3. Run inference on-device
4. Send only angles to server for LLM feedback
5. Reduces latency and bandwidth

### Performance Optimization
- **Image Model**: 30-50ms on mobile GPU
- **Keypoint Extraction**: 20-30ms with MediaPipe
- **Hybrid Decision**: <5ms
- **LLM Feedback**: 500-1000ms (cached: <50ms)
- **Total**: ~1 second end-to-end

---

## SECTION 6: FUTURE IMPROVEMENTS

1. **Real-time Video Analysis**: Track pose transitions
2. **Sequence Detection**: Recognize yoga flows (Sun Salutation)
3. **Personalized Feedback**: Learn user's common mistakes
4. **Voice Coaching**: Text-to-speech feedback during practice
5. **Progress Tracking**: Store angle improvements over time
6. **Multi-person Detection**: Group class analysis
7. **AR Overlay**: Show ideal pose skeleton overlay
8. **Injury Prevention**: Detect dangerous alignments
9. **Breathing Guidance**: Sync breath with movement
10. **Gamification**: Points, streaks, challenges

---

## Technology Stack

- **Deep Learning**: TensorFlow/Keras, MobileNetV2
- **Pose Estimation**: MediaPipe Pose
- **LLM**: Google Gemini API / OpenAI GPT
- **Backend**: Flask/FastAPI
- **Frontend**: HTML/CSS/JavaScript, WebRTC
- **Mobile**: TFLite, Flutter/React Native
- **Database**: SQLite/PostgreSQL for user data
- **Deployment**: Docker, Heroku/AWS/GCP

---

## Project Timeline

- **Week 1**: Data collection and preprocessing
- **Week 2**: Image model training and evaluation
- **Week 3**: Keypoint extraction and classifier training
- **Week 4**: Hybrid system integration and testing
- **Week 5**: LLM feedback system implementation
- **Week 6**: Web/mobile deployment and optimization
- **Week 7**: User testing and refinement
- **Week 8**: Documentation and launch

---

*This architecture provides a robust, scalable foundation for an intelligent yoga coaching system that combines the best of computer vision, geometric analysis, and natural language AI.*
