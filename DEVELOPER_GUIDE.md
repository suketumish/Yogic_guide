# Developer Guide - Yogic Guide

## Quick Start

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MONGO_URI="your_mongodb_connection_string"
export SECRET_KEY="your_secret_key"

# Run the application
python app.py
```

The application will start on `http://localhost:5000`

---

## Project Structure

```
yogic-guide/
├── app.py                          # Main Flask application
├── models.py                       # Database models
├── config.py                       # Configuration
├── requirements.txt                # Python dependencies
│
├── static/
│   ├── css/
│   │   ├── animations.css          # Animation styles
│   │   ├── yogic-wellness-theme.css # Theme styles
│   │   └── mobile-responsive.css   # Responsive styles
│   │
│   ├── js/
│   │   ├── voice-over.js           # Voice-over functionality
│   │   ├── pose-correction-enhanced.js # Pose correction logic
│   │   ├── pose-detection.js       # Pose detection
│   │   └── session.js              # Session management
│   │
│   └── images/                     # Static images
│
└── templates/
    ├── base.html                   # Base template
    ├── landing.html                # Landing page
    ├── register.html               # Registration
    ├── login.html                  # Login
    ├── dashboard.html              # User dashboard
    ├── profile.html                # User profile
    ├── contact.html                # Contact page
    ├── pose_details.html           # Pose details
    │
    └── admin/
        ├── base.html               # Admin base
        ├── dashboard.html          # Admin dashboard
        ├── users.html              # User management
        ├── analytics.html          # Analytics
        └── sessions.html           # Session management
```

---

## Key Features Implementation

### 1. Voice-Over System

```javascript
// Include in your HTML
<script src="{{ url_for('static', filename='js/voice-over.js') }}"></script>

// Basic usage
voiceOver.welcomeMessage();
voiceOver.sessionStart('Yoga Practice');
voiceOver.poseInstruction('Mountain Pose', 'Stand with feet together');
voiceOver.poseSuccess('Mountain Pose');
voiceOver.sessionComplete({ duration: 15, accuracy: 92 });

// Toggle voice-over
voiceOver.toggle();

// Adjust settings
voiceOver.setRate(1.2);  // Speed: 0.5 to 2.0
voiceOver.setPitch(1.0); // Pitch: 0.5 to 2.0
voiceOver.setVolume(0.8); // Volume: 0 to 1.0
```

### 2. Pose Correction Engine

```javascript
// Include in your HTML
<script src="{{ url_for('static', filename='js/pose-correction-enhanced.js') }}"></script>

// Start a session
poseCorrectionEngine.startSession();

// Validate a pose
const poseData = {
  keypoints: {
    nose: { x: 100, y: 50, confidence: 0.9 },
    left_shoulder: { x: 80, y: 100, confidence: 0.85 },
    // ... more keypoints
  }
};

const expectedPose = {
  name: 'Mountain Pose',
  type: 'standing'
};

const result = poseCorrectionEngine.validatePose(poseData, expectedPose);

if (result.valid) {
  console.log('Pose correct! Continue session');
  console.log('Accuracy:', result.accuracy);
} else {
  console.log('Pose incorrect! Session stopped');
  console.log('Feedback:', result.feedback);
  console.log('Can retry:', result.retryAllowed);
}

// Get session statistics
const stats = poseCorrectionEngine.getSessionStats();
console.log('Total poses:', stats.totalPoses);
console.log('Correct poses:', stats.correctPoses);
console.log('Average accuracy:', stats.avgAccuracy);
```

### 3. API Endpoints

#### Start Session
```javascript
fetch('/api/session/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    module_type: 'yoga',
    module_name: 'Yoga Practice'
  })
})
.then(res => res.json())
.then(data => {
  console.log('Session ID:', data.session_id);
});
```

#### Validate Pose
```javascript
fetch('/api/pose/validate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    pose_name: 'Mountain Pose',
    keypoints: poseData.keypoints,
    session_id: sessionId
  })
})
.then(res => res.json())
.then(data => {
  if (data.valid) {
    // Continue session
  } else {
    // Stop session
  }
});
```

#### Complete Session
```javascript
fetch('/api/session/complete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: sessionId,
    duration: 900, // seconds
    accuracy: 85,
    poses_completed: ['Mountain Pose', 'Warrior Pose']
  })
})
.then(res => res.json())
.then(data => {
  console.log('Session completed!');
});
```

---

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  uniqueId: String,           // 8-character unique ID
  email: String,
  mobile: String,
  password: Hash,
  profile: {
    name: String,
    age: Number,
    gender: String,
    experience: String
  },
  tags: Array,                // Agent tags
  skills: Array,              // Skill badges
  role: String,               // 'user' or 'admin'
  stats: {
    totalSessions: Number,
    totalMinutes: Number,
    totalPoses: Number
  },
  preferences: {
    notifications: Boolean,
    theme: String,
    voiceOver: Boolean
  },
  createdAt: Date
}
```

### Sessions Collection
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  moduleType: String,         // 'breathing', 'yoga', etc.
  moduleName: String,
  startTime: Date,
  endTime: Date,
  duration: Number,           // seconds
  poses: Array,
  poseCorrections: Array,     // Failed pose attempts
  accuracy: Number,           // 0-100
  status: String,             // 'active', 'completed', 'stopped'
  createdAt: Date
}
```

---

## Adding New Features

### Adding a New Pose

1. Add pose data in `app.py`:
```python
poses_data = {
    'new-pose': {
        'name': 'New Pose',
        'sanskrit_name': 'Sanskrit Name',
        'icon': '🧘',
        'difficulty': 'Beginner',
        'category': 'Standing',
        'duration': 30,
        'module': 'yoga',
        'instructions': [...],
        'benefits': [...],
        'importance': '...',
        'precautions': [...],
        'tips': [...]
    }
}
```

2. Access via URL: `/pose/new-pose`

### Adding a New Module

1. Update `valid_modules` in `app.py`:
```python
valid_modules = {
    'new-module': 'New Module Name'
}
```

2. Create template: `templates/module_new_module.html`

3. Add route:
```python
@app.route('/module/new-module/info')
@require_auth
def module_new_module_info():
    return render_template('module_new_module.html')
```

### Adding Voice-Over Messages

In `static/js/voice-over.js`:
```javascript
customMessage(text) {
    this.speak(text);
}

// Usage
voiceOver.customMessage('Your custom message here');
```

---

## Admin Features

### User Management
- View all users with unique IDs
- See user badges (tags, skills, experience)
- Toggle admin privileges
- Delete users
- View user details

### Analytics Dashboard
- User growth trends
- Session analytics
- Module performance
- User engagement
- Hourly usage patterns
- Weekly trends
- Retention analysis
- Export to CSV

### Session Management
- View all sessions
- Filter by module
- See session details
- Track pose corrections

---

## Customization

### Changing Theme Colors

Edit `templates/admin/base.html` or any template:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
```

### Adjusting Pose Accuracy Threshold

In `static/js/pose-correction-enhanced.js`:
```javascript
const poseCorrectionEngine = new PoseCorrectionEngine({
    strictMode: true,
    accuracyThreshold: 75,  // Change this (50-100)
    maxRetries: 3
});
```

### Customizing Voice Settings

In `static/js/voice-over.js`:
```javascript
const voiceOver = new VoiceOverManager();
voiceOver.setRate(1.0);    // 0.5 to 2.0
voiceOver.setPitch(1.0);   // 0.5 to 2.0
voiceOver.setVolume(1.0);  // 0 to 1.0
```

---

## Testing

### Manual Testing Checklist

#### User Features:
- [ ] Registration with unique ID generation
- [ ] Login/Logout
- [ ] Profile page (footer aligned, no practice button)
- [ ] Contact page (all social links clickable)
- [ ] Pose details page (all sections visible)
- [ ] Voice-over functionality
- [ ] Pose correction (session stops on incorrect pose)

#### Admin Features:
- [ ] User management (badges visible)
- [ ] Analytics (all charts loading)
- [ ] Session management
- [ ] Export functionality

### API Testing

```bash
# Test session start
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"module_type":"yoga","module_name":"Yoga Practice"}'

# Test pose validation
curl -X POST http://localhost:5000/api/pose/validate \
  -H "Content-Type: application/json" \
  -d '{"pose_name":"Mountain Pose","keypoints":{},"session_id":"..."}'
```

---

## Troubleshooting

### Voice-Over Not Working
- Check browser compatibility (Chrome, Edge, Safari)
- Ensure HTTPS (required for some browsers)
- Check browser permissions
- Verify voice-over.js is loaded

### Pose Correction Not Stopping Session
- Check `strictMode` is enabled
- Verify `accuracyThreshold` setting
- Check console for errors
- Ensure pose-correction-enhanced.js is loaded

### Database Connection Issues
- Verify MONGO_URI environment variable
- Check MongoDB Atlas whitelist
- Test connection string
- Check network connectivity

### Footer Not Aligned
- Ensure parent has `flex flex-col` classes
- Check `min-h-screen` on body
- Verify `mt-auto` on footer

---

## Performance Optimization

### Database Queries
- Use indexes on frequently queried fields
- Implement pagination for large datasets
- Use aggregation pipelines efficiently
- Cache frequently accessed data

### Frontend
- Lazy load images
- Minimize JavaScript bundle size
- Use CDN for libraries
- Implement service workers for offline support

---

## Security Best Practices

1. **Never commit sensitive data**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Validate all inputs**
   - Server-side validation
   - Sanitize user inputs
   - Use parameterized queries

3. **Secure sessions**
   - Use strong secret keys
   - Implement CSRF protection
   - Set secure cookie flags

4. **Password security**
   - Use bcrypt for hashing
   - Enforce strong passwords
   - Implement rate limiting

---

## Deployment

### Environment Variables
```bash
MONGO_URI=mongodb+srv://...
SECRET_KEY=your-secret-key
FLASK_ENV=production
PORT=5000
```

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Set up logging
- [ ] Enable rate limiting
- [ ] Configure CORS if needed

---

## Support

For issues or questions:
- Check this guide first
- Review code comments
- Check console for errors
- Review MongoDB logs
- Test in different browsers

---

## Contributing

When adding new features:
1. Follow existing code style
2. Add comments for complex logic
3. Update this guide
4. Test thoroughly
5. Update requirements.txt if needed

---

*Last Updated: 2024*
*Version: 1.0.0*
