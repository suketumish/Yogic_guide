# 🧘 Hybrid Yoga Posture Detection System

## Complete AI-Powered Yoga Assistant with Image Classification, Pose Keypoints & LLM Feedback

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Why Hybrid Approach?](#why-hybrid-approach)
3. [System Architecture](#system-architecture)
4. [Dataset Description](#dataset-description)
5. [Pipeline Explanation](#pipeline-explanation)
6. [Training Strategy](#training-strategy)
7. [Evaluation Metrics](#evaluation-metrics)
8. [LLM Feedback System](#llm-feedback-system)
9. [Installation & Setup](#installation--setup)
10. [Usage Guide](#usage-guide)
11. [Deployment](#deployment)
12. [Future Improvements](#future-improvements)

---

## 🎯 Project Overview

This project implements a **state-of-the-art hybrid yoga posture detection system** that combines:

1. **Deep Learning Image Classifier** (MobileNetV2/EfficientNet) - 107 yoga poses
2. **Pose Keypoint Extraction** (MediaPipe) - 33 body landmarks
3. **LLM-Powered Feedback** (Gemini/GPT) - Natural language corrections

### Key Features

✅ **107 Yoga Poses** - Comprehensive coverage from beginner to advanced  
✅ **Real-time Detection** - Fast inference (<100ms)  
✅ **Accurate Feedback** - Combines visual + skeletal analysis  
✅ **Natural Language** - LLM generates human-friendly corrections  
✅ **Mobile-Ready** - TFLite conversion for edge deployment  
✅ **Production-Grade** - Modular, documented, tested code  

---

## 🚀 Why Hybrid Approach?

### Problem with Single-Model Systems

| Approach | Strengths | Weaknesses |
|----------|-----------|------------|
| **Image-Only** | Good at recognizing poses from appearance | F