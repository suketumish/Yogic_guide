# Gemini API Integration Guide

This guide explains how to use the Gemini API in your Zen_Align project.

## 📋 Table of Contents
1. [Setup](#setup)
2. [Configuration](#configuration)
3. [Usage Examples](#usage-examples)
4. [API Reference](#api-reference)
5. [Integration Points](#integration-points)

## 🚀 Setup

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (you'll need it for the `.env` file)

### Step 2: Install Dependencies

```bash
pip install google-generativeai
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create or update your `.env` file in the project root:

```env
# Gemini API Configuration
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-pro
GEMINI_ENABLED=True
```

**Important**: 
- Replace `your-api-key-here` with your actual API key
- Never commit your `.env` file to version control
- Make sure `.env` is in your `.gitignore`

### Step 4: Verify Installation

Test if everything is working:

```python
from gemini_helper import get_gemini_helper

# Initialize Gemini helper
gemini = get_gemini_helper()

if gemini:
    print("✅ Gemini API is configured correctly!")
else:
    print("❌ Gemini API configuration failed. Check your API key.")
```

## ⚙️ Configuration

The Gemini API is configured in `config.py`:

- **GEMINI_API_KEY**: Your API key from Google AI Studio
- **GEMINI_MODEL**: Model to use (`gemini-pro` or `gemini-pro-vision`)
- **GEMINI_ENABLED**: Enable/disable Gemini features (True/False)

### Available Models

1. **gemini-pro**: For text-based tasks (feedback, recommendations, chat)
2. **gemini-pro-vision**: For image analysis tasks (pose analysis from images)

## 📚 Usage Examples

### Example 1: Generate Pose Feedback

```python
from gemini_helper import get_gemini_helper

# Initialize helper
gemini = get_gemini_helper()

if gemini:
    # Generate feedback for a pose
    feedback = gemini.generate_feedback(
        pose_name="Downward Dog",
        accuracy=75.5,
        errors=["knees not straight", "shoulders too forward"]
    )
    print(feedback)
```

### Example 2: Analyze Pose Safety

```python
from gemini_helper import get_gemini_helper

gemini = get_gemini_helper()

if gemini:
    # Analyze if a pose is safe for a user
    user_history = {
        "experience_level": "beginner",
        "injuries": ["lower back"],
        "practice_days": 10
    }
    
    analysis = gemini.analyze_pose_safety(
        pose_name="Headstand",
        user_history=user_history
    )
    print(f"Safety Level: {analysis['safety_level']}")
    print(f"Risks: {analysis['risks']}")
```

### Example 3: Generate Practice Recommendations

```python
from gemini_helper import get_gemini_helper

gemini = get_gemini_helper()

if gemini:
    recommendation = gemini.generate_practice_recommendation(
        user_level="intermediate",
        goals=["flexibility", "strength"],
        session_count=25
    )
    print(recommendation)
```

### Example 4: Answer Yoga Questions

```python
from gemini_helper import get_gemini_helper

gemini = get_gemini_helper()

if gemini:
    answer = gemini.chat_about_yoga(
        user_question="What is the benefit of practicing Surya Namaskar?",
        context="User is a beginner with 5 sessions completed"
    )
    print(answer)
```

### Example 5: Integrate with Flask Route

```python
from flask import jsonify
from gemini_helper import get_gemini_helper

@app.route('/api/pose/ai-feedback', methods=['POST'])
@require_auth
def get_ai_feedback():
    """Get AI-powered feedback for pose correction"""
    try:
        data = request.get_json()
        pose_name = data.get('pose_name')
        accuracy = data.get('accuracy', 0)
        errors = data.get('errors', [])
        
        gemini = get_gemini_helper()
        if gemini and app.config.get('GEMINI_ENABLED'):
            feedback = gemini.generate_feedback(pose_name, accuracy, errors)
            return jsonify({
                'success': True,
                'feedback': feedback,
                'source': 'ai'
            })
        else:
            # Fallback to default feedback
            return jsonify({
                'success': True,
                'feedback': f"Keep practicing {pose_name}!",
                'source': 'default'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 🔗 Integration Points in Your App

### 1. Enhanced Pose Validation (app.py)

You can enhance the `/api/pose/validate` endpoint:

```python
@app.route('/api/pose/validate', methods=['POST'])
@require_auth
def validate_pose():
    """Enhanced pose validation with AI feedback"""
    try:
        data = request.get_json()
        pose_name = data.get('pose_name', '')
        keypoints = data.get('keypoints', {})
        accuracy = calculate_pose_accuracy(keypoints)
        is_valid = accuracy >= 75
        
        # Get AI-powered feedback if enabled
        feedback = None
        if app.config.get('GEMINI_ENABLED'):
            gemini = get_gemini_helper()
            if gemini:
                errors = [] if is_valid else ["alignment issues detected"]
                feedback = gemini.generate_feedback(pose_name, accuracy, errors)
        
        result = {
            'valid': is_valid,
            'accuracy': accuracy,
            'pose_name': pose_name,
            'canContinue': is_valid,
            'feedback': feedback or generate_pose_feedback(pose_name, accuracy, is_valid)
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 2. Personalized Recommendations

Add to user dashboard or profile page:

```python
@app.route('/api/recommendations', methods=['GET'])
@require_auth
def get_recommendations():
    """Get personalized practice recommendations"""
    try:
        user_id = ObjectId(session['user_id'])
        user = db.users.find_one({'_id': user_id})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        gemini = get_gemini_helper()
        if gemini and app.config.get('GEMINI_ENABLED'):
            level = user.get('profile', {}).get('level', 'beginner')
            goals = user.get('goals', [])
            session_count = db.sessions.count_documents({'user_id': user_id})
            
            recommendation = gemini.generate_practice_recommendation(
                user_level=level,
                goals=goals,
                session_count=session_count
            )
            
            return jsonify({
                'success': True,
                'recommendation': recommendation
            })
        
        return jsonify({'success': False, 'message': 'AI not available'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 3. Yoga Chat Assistant

Create a chat endpoint:

```python
@app.route('/api/chat/yoga', methods=['POST'])
@require_auth
def yoga_chat():
    """Chat with AI yoga assistant"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        gemini = get_gemini_helper()
        if gemini and app.config.get('GEMINI_ENABLED'):
            # Get user context
            user_id = ObjectId(session['user_id'])
            user = db.users.find_one({'_id': user_id})
            context = f"User level: {user.get('profile', {}).get('level', 'beginner')}"
            
            answer = gemini.chat_about_yoga(question, context)
            
            return jsonify({
                'success': True,
                'answer': answer
            })
        
        return jsonify({
            'success': False,
            'message': 'AI chat is not available'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 🔐 Security Best Practices

1. **Never expose your API key**:
   - Store it only in `.env` file
   - Add `.env` to `.gitignore`
   - Never commit API keys to version control

2. **Rate Limiting**:
   - Gemini API has rate limits
   - Consider implementing caching for frequent requests
   - Use background tasks for non-critical AI features

3. **Error Handling**:
   - Always have fallback behavior when AI is unavailable
   - Gracefully degrade functionality if API fails

4. **Cost Management**:
   - Monitor API usage
   - Cache responses when appropriate
   - Use AI features judiciously

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Make sure your `.env` file exists and contains `GEMINI_API_KEY=your-key`

### Issue: "google-generativeai not installed"
**Solution**: Run `pip install google-generativeai`

### Issue: API requests failing
**Solution**: 
- Verify your API key is correct
- Check your internet connection
- Verify API quotas in Google AI Studio

### Issue: Import errors
**Solution**: 
- Ensure you're in the correct virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## 📖 Additional Resources

- [Google Generative AI Documentation](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/api)
- [Google AI Studio](https://makersuite.google.com/)

## 🎯 Next Steps

1. ✅ Set up your API key
2. ✅ Test basic functionality
3. ✅ Integrate into your pose validation flow
4. ✅ Add chat assistant feature
5. ✅ Implement personalized recommendations

---

**Note**: The Gemini API is a powerful tool that can enhance your yoga app with AI-powered features. Start with simple integrations and expand based on user feedback!

