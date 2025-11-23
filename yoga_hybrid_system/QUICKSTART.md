# 🚀 Quick Start Guide - Yoga Hybrid System

Get up and running in 10 minutes!

---

## ⚡ Installation (2 minutes)

```bash
# Clone or navigate to project
cd yoga_hybrid_system

# Create virtual environment
python -m venv venv

# Activate (choose your OS)
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 API Setup (1 minute)

### Option 1: Gemini API (Recommended - Free tier available)

```bash
# Get API key from: https://makersuite.google.com/app/apikey

# Set environment variable
export GEMINI_API_KEY='your-api-key-here'    # Linux/Mac
set GEMINI_API_KEY=your-api-key-here         # Windows CMD
$env:GEMINI_API_KEY='your-api-key-here'      # Windows PowerShell
```

### Option 2: Skip LLM (Use rule-based feedback)

```bash
# No API key needed - system will use fallback feedback
python complete_pipeline.py --image test.jpg --no-llm
```

---

## 📊 Option A: Use Pre-trained Models (Fastest)

If you have pre-trained models:

```bash
# Place models in models/ directory:
# - yoga_model_final.h5
# - keypoint_mlp_classifier.pkl
# - keypoint_mlp_scaler.pkl
# - keypoint_mlp_label_encoder.pkl
# - class_names.json
# - keypoint_mlp_metadata.json

# Run inference immediately
python complete_pipeline.py --image path/to/yoga_pose.jpg
```

---

## 🎓 Option B: Train Your Own Models (3-4 hours)

### Step 1: Prepare Dataset (30 minutes)

```bash
# Create directory structure
mkdir -p data/{train,validate,test}/{warrior2,downdog,tree,plank}

# Add images (minimum 100 per pose per split)
# data/train/warrior2/img001.jpg
# data/train/warrior2/img002.jpg
# ... etc
```

**Dataset Tips:**
- Use diverse angles, lighting, body types
- Clear view of full body
- JPG/PNG format, 640x480+ resolution
- Include both correct and slightly incorrect forms

### Step 2: Train Image Model (2-3 hours on GPU)

```bash
python train_image_model.py
```

**What happens:**
- Loads your dataset
- Trains MobileNetV2 with transfer learning
- Phase 1: Feature extraction (15 epochs)
- Phase 2: Fine-tuning (30 epochs)
- Saves model to `models/yoga_model_final.h5`
- Generates evaluation plots

**Output:**
```
Classes found: ['warrior2', 'downdog', 'tree', 'plank']
=== PHASE 1: Feature Extraction ===
Epoch 1/15: loss: 0.8234 - accuracy: 0.7123 - val_accuracy: 0.7456
...
=== PHASE 2: Fine-Tuning ===
Epoch 1/30: loss: 0.3421 - accuracy: 0.8912 - val_accuracy: 0.8734
...
Test Accuracy: 0.8723
✅ Training complete!
```

### Step 3: Extract Keypoints (30-60 minutes)

```bash
python extract_keypoints.py
```

**What happens:**
- Processes all images with MediaPipe
- Extracts 33 body landmarks per image
- Calculates joint angles
- Saves to `keypoints_dataset.csv`

**Output:**
```
Processing train/warrior2: 150 images
100%|████████████████| 150/150 [02:34<00:00,  1.03s/it]
Processing train/downdog: 142 images
...
✅ Keypoints saved to keypoints_dataset.csv
Total samples: 568
Features per sample: 119
```

### Step 4: Train Keypoint Model (10-30 minutes)

```bash
python train_keypoint_model.py
```

**What happens:**
- Loads keypoint CSV
- Trains MLP classifier
- Evaluates on test set
- Saves model to `models/keypoint_mlp_classifier.pkl`

**Output:**
```
Train samples: 400
Validation samples: 100
Test samples: 68
Features: 119
Classes: 4

Training MLP classifier...
Iteration 1, loss = 1.2345
...
Validation Accuracy: 0.8600
Test Accuracy: 0.8265
✅ Model saved!
```

---

## 🎯 Run Inference (30 seconds)

### Single Image

```bash
python complete_pipeline.py --image test_pose.jpg --level beginner
```

**Output:**
```
🧘 YOGA POSE ANALYSIS RESULT
============================================================

📸 Image: test_pose.jpg

🎯 FINAL PREDICTION: WARRIOR2
   Confidence: 89.3%
   Logic: HIGH_CONFIDENCE_AGREEMENT

📊 Model Breakdown:
   Image Model: warrior2 (92.1%)
   Keypoint Model: warrior2 (86.5%)

📐 Body Angles:
   Left Knee: 95.2°
   Right Knee: 178.4°
   Torso Vertical: 8.3°

⚠️  Issues Detected:
   • Front Knee Slightly Forward

💬 Feedback:
   Nice effort! Your front knee is tracking a bit forward. 
   Try shifting your hips back so your knee stays directly 
   over your ankle. This protects your knee joint.

============================================================
```

### Batch Processing

```bash
python complete_pipeline.py --batch path/to/image_folder --output results.json
```

**Output:**
```
📁 Processing 25 images from path/to/image_folder

✓ img_001.jpg: warrior2 (89.3%)
✓ img_002.jpg: downdog (92.1%)
✓ img_003.jpg: tree (87.4%)
...

✅ Batch analysis complete! Results saved to results.json
```

---

## 🌐 Deploy as Web API (5 minutes)

### Create API Server

```python
# Save as app_api.py
from flask import Flask, request, jsonify
from complete_pipeline import YogaPoseAnalyzer

app = Flask(__name__)
analyzer = YogaPoseAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    file.save('temp.jpg')
    result = analyzer.analyze_pose('temp.jpg', verbose=False)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Run Server

```bash
python app_api.py
```

### Test API

```bash
# Using curl
curl -X POST -F "image=@test_pose.jpg" http://localhost:5000/analyze

# Using Python
import requests
files = {'image': open('test_pose.jpg', 'rb')}
response = requests.post('http://localhost:5000/analyze', files=files)
print(response.json())
```

---

## 📱 Mobile Deployment (TFLite)

Models are automatically converted to TFLite during training:

```bash
# TFLite model location
models/yoga_model.tflite
```

**Android Integration:**
```kotlin
val model = Interpreter(loadModelFile("yoga_model.tflite"))
val input = preprocessImage(bitmap)
val output = Array(1) { FloatArray(numClasses) }
model.run(input, output)
```

**iOS Integration:**
```swift
// Convert TFLite to CoreML first
let model = try YogaClassifier(configuration: MLModelConfiguration())
let prediction = try model.prediction(image: pixelBuffer)
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'tensorflow'"

```bash
pip install tensorflow
```

### "No pose landmarks detected"

- Ensure full body is visible in image
- Improve lighting
- Try different camera angle
- Check image is not corrupted

### "FileNotFoundError: models/yoga_model_final.h5"

You need to train models first:
```bash
python train_image_model.py
python extract_keypoints.py
python train_keypoint_model.py
```

### Low accuracy

- Add more training data (300+ images per pose)
- Ensure diverse dataset (angles, lighting, body types)
- Check for mislabeled images
- Increase training epochs

### LLM feedback not working

```bash
# Check API key is set
echo $GEMINI_API_KEY

# Use fallback mode
python complete_pipeline.py --image test.jpg --no-llm
```

---

## 📚 Next Steps

1. **Read Full Documentation**
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [USAGE_GUIDE.md](USAGE_GUIDE.md) - Detailed usage
   - [sample_json_structures.json](sample_json_structures.json) - Data formats

2. **Customize System**
   - Add new poses to dataset
   - Adjust confidence thresholds
   - Customize feedback messages
   - Integrate with your app

3. **Optimize Performance**
   - Use GPU for faster inference
   - Batch process images
   - Cache LLM responses
   - Optimize model size

4. **Deploy to Production**
   - Docker containerization
   - Cloud deployment (AWS/GCP/Azure)
   - Mobile app integration
   - Real-time video analysis

---

## 🎉 You're Ready!

You now have a fully functional hybrid yoga posture detection system!

**Test it out:**
```bash
python complete_pipeline.py --image your_yoga_pose.jpg
```

**Need help?** Check the documentation or open an issue.

**Happy Yoga Coding! 🧘‍♀️🤖**
