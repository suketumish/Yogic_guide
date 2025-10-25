# AI-Powered Yogic Guide 🧘‍♀️

Real-time yoga pose correction system with angle-based detection, visual guidance, and audio feedback using MediaPipe Pose.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** MongoDB
- **Pose Detection:** MediaPipe Pose
- **Audio:** Web Speech API (Text-to-Speech)

## Features ✨

### User Authentication
- Registration with health profile
- Secure login/logout
- Profile management
- Session history tracking

### 3 Yoga Modules
1. **Full Body Stretching** - 5 poses for flexibility
2. **Breathing Exercises** - 4 pranayama techniques
3. **Surya Namaskar** - Complete 12-pose sun salutation

### Real-Time Pose Detection
- MediaPipe skeleton overlay
- Angle-based pose validation
- Visual feedback (green/red indicators)
- Screen blink effect for incorrect poses
- Live angle measurements

### Audio Guidance
- Pose name announcements
- Benefits narration
- Correction instructions
- Encouragement messages

### Session Management
- Namaste gesture detection to start
- Pause/Resume functionality
- Progress tracking
- Session summary with stats
- Calorie estimation

## Setup Instructions

### 1. Install MongoDB
Download and install from https://www.mongodb.com/try/download/community

Start MongoDB service:
```bash
# Windows
net start MongoDB

# Mac/Linux
sudo systemctl start mongod
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file:
```
SECRET_KEY=your-secret-key-change-this
MONGO_URI=mongodb://localhost:27017/yogic_guide
```

### 4. Seed Database with Poses
```bash
python seed_poses.py
```

### 5. Run the Application
```bash
python app.py
```

Visit **http://localhost:5000**

## Project Structure
```
yogic-guide/
├── app.py                      # Flask backend
├── config.py                   # Configuration
├── seed_poses.py              # Database seeding
├── requirements.txt           # Dependencies
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   ├── js/
│   │   ├── pose-detection.js # MediaPipe integration
│   │   ├── session.js        # Session management
│   │   └── breathing-exercises.js
│   └── images/               # Pose references
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── profile.html
    ├── session.html
    ├── breathing.html
    └── session-complete.html
```

## Usage Guide

### First Time Setup
1. Register a new account
2. Fill in your profile (age, experience level)
3. Choose a module from dashboard

### Starting a Session
1. Click "Start Session" on any module
2. Allow camera permissions
3. Show Namaste gesture (🙏) for 5 seconds
4. Follow on-screen instructions
5. Hold each pose for the specified duration

### Pose Validation
- **Green skeleton** = Correct pose
- **Red skeleton** = Needs adjustment
- **Screen blink** = Incorrect posture
- **Angle display** = Real-time measurements

### Breathing Exercises
1. Select breathing module
2. Choose exercise type:
   - Anulom Vilom (2 min)
   - Bhramari (1 min)
   - Kapalbhati (1.5 min)
   - Silent Meditation (5 min)
3. Sit in cross-legged position
4. Follow audio instructions

## Database Collections

### users
- User credentials and profile
- Experience level
- Health conditions

### sessions
- Session history
- Duration and poses completed
- Accuracy scores
- Calories burned

### poses
- Pose details and instructions
- Ideal angles for validation
- Benefits and cautions

### user_progress
- Total sessions count
- Streak tracking
- Total minutes practiced
- Achievements/badges

## API Endpoints

### Authentication
- `POST /register` - Create account
- `POST /login` - User login
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - Main hub
- `GET /profile` - User profile

### Sessions
- `GET /module/<type>` - Start module
- `POST /session/start` - Initialize session
- `POST /session/complete` - End session
- `GET /session-complete` - Summary page

### API
- `POST /api/pose/validate` - Validate pose
- `GET /api/poses/<module>` - Get poses
- `GET /api/session/stats/<id>` - Session stats

## Pose Sequences

### Stretching Module (5 poses)
1. Mountain Pose (20s)
2. Forward Bend (25s)
3. Warrior I (30s)
4. Triangle Pose (25s)
5. Child's Pose (30s)

### Surya Namaskar (12 poses)
Each pose held for 5 seconds in continuous flow

### Breathing Exercises
- Seated position detection
- 4 different pranayama techniques
- Timed cycles with audio guidance

## Browser Requirements
- Modern browser with WebRTC support
- Camera access required
- Microphone for audio feedback (optional)
- Recommended: Chrome, Edge, Firefox

## Troubleshooting

### Camera Not Working
- Check browser permissions
- Ensure no other app is using camera
- Try refreshing the page

### Pose Not Detected
- Ensure good lighting
- Stand within camera frame
- Remove background clutter
- Only one person in frame

### Audio Not Playing
- Check browser audio permissions
- Unmute browser tab
- Check system volume

## Future Enhancements
- [ ] Add more pose sequences
- [ ] Implement pose reference images
- [ ] Add achievement badges
- [ ] Social sharing features
- [ ] Weekly challenges
- [ ] Video tutorials
- [ ] Multi-language support
- [ ] Mobile app version

## License
MIT License - Feel free to use and modify

## Support
For issues or questions, please create an issue in the repository.

---

**Namaste! 🙏 Start your yoga journey today!**
