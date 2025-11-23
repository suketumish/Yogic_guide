# 🚀 Gemini API Quick Start Guide

## Overview

This project is now configured to use Google's Gemini API for AI-powered yoga guidance features.

## Project Structure

```
major/
├── config.py              # ✅ Gemini API configuration added
├── requirements.txt       # ✅ google-generativeai package added
├── gemini_helper.py       # ✅ New helper module created
├── GEMINI_API_GUIDE.md    # 📖 Full documentation
└── .env                   # ⚠️  Add your API key here (not in git)
```

## Quick Setup (3 Steps)

### 1️⃣ Get Your API Key

Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and create an API key.

### 2️⃣ Add to .env File

Create or edit `.env` in the project root:

```env
# Gemini API Configuration
GEMINI_API_KEY=your-actual-api-key-here
GEMINI_MODEL=gemini-pro
GEMINI_ENABLED=True
```

**Replace `your-actual-api-key-here` with your real API key!**

### 3️⃣ Install Package

```bash
pip install google-generativeai
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

## ✅ Verify It Works

Run this in Python:

```python
from gemini_helper import get_gemini_helper

gemini = get_gemini_helper()
if gemini:
    print("✅ Gemini API is ready!")
    # Test it
    feedback = gemini.generate_feedback("Downward Dog", 75, ["alignment issues"])
    print(f"Feedback: {feedback}")
else:
    print("❌ Check your API key in .env file")
```

## 📝 Basic Usage Example

```python
from gemini_helper import get_gemini_helper

# Initialize
gemini = get_gemini_helper()

# Generate pose feedback
feedback = gemini.generate_feedback(
    pose_name="Warrior II",
    accuracy=80.5,
    errors=["front knee alignment", "hips not square"]
)
print(feedback)

# Get practice recommendations
recommendation = gemini.generate_practice_recommendation(
    user_level="intermediate",
    goals=["flexibility", "strength"],
    session_count=20
)
print(recommendation)

# Answer yoga questions
answer = gemini.chat_about_yoga(
    "What are the benefits of Surya Namaskar?",
    context="User is a beginner"
)
print(answer)
```

## 🔗 Integration in Flask Routes

### Example: Enhanced Pose Feedback

```python
from flask import jsonify, request
from gemini_helper import get_gemini_helper

@app.route('/api/pose/ai-feedback', methods=['POST'])
@require_auth
def ai_feedback():
    data = request.get_json()
    pose_name = data.get('pose_name')
    accuracy = data.get('accuracy', 0)
    errors = data.get('errors', [])
    
    gemini = get_gemini_helper()
    if gemini and app.config.get('GEMINI_ENABLED'):
        feedback = gemini.generate_feedback(pose_name, accuracy, errors)
        return jsonify({'feedback': feedback, 'source': 'ai'})
    
    return jsonify({'feedback': f"Keep practicing {pose_name}!", 'source': 'default'})
```

## 🎯 Available Features

The `gemini_helper.py` module provides:

1. **`generate_feedback()`** - AI-powered pose correction feedback
2. **`analyze_pose_safety()`** - Safety analysis for poses
3. **`generate_practice_recommendation()`** - Personalized practice suggestions
4. **`chat_about_yoga()`** - Answer yoga-related questions
5. **`analyze_pose_from_image()`** - Analyze poses from images (requires vision model)

## 📚 Full Documentation

See `GEMINI_API_GUIDE.md` for:
- Detailed setup instructions
- All available methods
- Integration examples
- Security best practices
- Troubleshooting guide

## ⚠️ Important Notes

1. **Never commit your `.env` file** - It's already in `.gitignore`
2. **API Key Security** - Keep your API key secret and secure
3. **Rate Limits** - Gemini API has usage limits (check Google AI Studio)
4. **Costs** - Free tier available, but check pricing for production

## 🆘 Need Help?

1. Check `GEMINI_API_GUIDE.md` for detailed documentation
2. Verify your API key is correct in `.env`
3. Ensure `google-generativeai` is installed
4. Check API quotas in [Google AI Studio](https://makersuite.google.com/app/apikey)

---

**That's it!** You're ready to use Gemini API in your Zen_Align project! 🧘‍♀️✨

