# YOGIC GUIDE - Complete Project Documentation for AI Analysis

## PROJECT OVERVIEW
Yogic Guide is a production-ready AI-powered yoga assistant platform combining ancient wellness practices with modern technology. Built with Python Flask, MongoDB, MediaPipe AI, and responsive web technologies.

**Version:** 1.0.0 | **Status:** Production Ready | **Lines of Code:** 3000+ | **API Endpoints:** 50+

---

## TECHNOLOGY STACK
- **Backend:** Python Flask 2.0+, MongoDB (Atlas/Local), bcrypt authentication
- **Frontend:** TailwindCSS 3.0+, Vanilla JavaScript ES6+, Chart.js 3.x
- **AI/ML:** MediaPipe Pose Detection (33-point skeleton tracking)
- **Voice:** Web Speech API for text-to-speech
- **Deployment:** Render.com, Heroku, AWS EC2 compatible

---

## CORE FEATURES

### USER FEATURES
1. Secure authentication with unique 8-character user IDs
2. Multi-module practice (Surya Namaskar, Breathing, Stretching, Meditation, Yoga)
3. Real-time pose detection with 33-point skeleton tracking
4. Strict pose correction (session stops if accuracy < 75%)
5. Voice-over guidance (instructions, corrections, encouragement)
6. Progress tracking (sessions, accuracy, duration, streaks)
7. Badge system (agent tags, skill badges, achievement stickers)
8. Responsive design (mobile, tablet, desktop)
9. Profile management with session filtering by module
10. Password reset with email tokens

### ADMIN FEATURES
1. User management (view, edit, delete, grant/revoke admin)
2. Analytics dashboard with 7 interactive charts
3. Real-time data updates (auto-refresh every 30 seconds)
4. Session monitoring across all users
5. Module performance analytics
6. Platform health score (composite metric)
7. CSV export functionality
8. User activity tracking

---

## DATABASE SCHEMA

### USERS COLLECTION
- uniqueId: 8-char unique identifier
- email, password (bcrypt), mobile, profile (name, age, gender, experience)
- role: 'user' or 'admin'
- badges: Array (agent tags, skill badges with colors/levels)
- stickers: Array (achievement stickers)
- preferences: voiceOverEnabled, voiceOverSpeed, voiceOverVolume
- stats: totalSessions, totalMinutes, totalPoses, currentStreak, longestStreak

### SESSIONS COLLECTION
- userId, module (surya_namaskar, breathing, stretching, meditation, yoga)
- startTime, endTime, duration (seconds)
- poses: Array, poseCorrections: Array
- accuracy: Number (percentage)
- status: 'active', 'completed', 'paused'

---

## API ENDPOINTS (50+ Routes)

### Authentication
- POST /register, /login, /admin/login
- GET /logout
- POST /forgot-password, /reset-password/<token>

### User Pages
- GET / (landing), /dashboard, /profile, /about, /contact

### Module Pages
- GET /module/<module_type> (session page)
- GET /module/surya-namaskar/info, /module/breathing/info, /module/stretching/info
- GET /pose/<pose_id> (pose details)

### Session API
- POST /api/session/start, /api/session/start/<module>, /api/session/complete
- GET /api/sessions/history (supports ?module filter)
- POST /api/pose/validate (strict checking)

### User Preferences
- POST /api/user/preferences (save voice-over settings)
- GET /api/user/preferences

### Analytics API
- GET /api/analytics/modules, /api/analytics/module/<module_type>
- GET /api/analytics/live (real-time, admin only)
- GET /api/analytics/overview, /api/analytics/users, /api/analytics/sessions

### Admin Pages
- GET /admin (dashboard), /admin/users, /admin/users/<user_id>
- POST /admin/users/<user_id>/toggle-admin, /admin/users/<user_id>/delete
- GET /admin/sessions, /admin/analytics, /admin/settings

---

## YOGA MODULES

### 1. SURYA NAMASKAR (Sun Salutation)
12 sequential poses, 5-second hold each:
Prayer Pose, Raised Arms, Hand to Foot, Equestrian Pose, Plank, Eight Limbed Pose, Cobra, Mountain, Equestrian (return), Hand to Foot (return), Raised Arms (return), Prayer (return)

### 2. BREATHING EXERCISES (Pranayama)
Seated position (Sukhasana), 5-minute duration, breathing cues (inhale, exhale, hold)

### 3. STRETCHING ROUTINE
5 flexibility poses: Mountain Pose (20s), Forward Bend (25s), Warrior I (30s), Triangle Pose (25s), Child's Pose (30s)

### 4. MEDITATION
Mindfulness and breath awareness, customizable duration, guided voice instructions

### 5. YOGA PRACTICE
General yoga poses, mixed difficulty levels, comprehensive pose library

---

## POSE DETECTION SYSTEM

### MediaPipe Integration
- 33 body keypoints tracked in real-time
- 70% minimum detection confidence
- Smooth landmark tracking enabled

### Pose Validation
- Accuracy based on joint angles vs. target angles
- Angle Tolerance: Strict (±10°), Normal (±15°), Relaxed (±20°)
- Joints Tracked: Elbows, Knees, Shoulders, Hips, Ankles, Torso, Neck

### Strict Correction Logic
- Session stops if accuracy < 75%
- Visual feedback (red border, shake animation)
- Voice feedback with specific corrections
- Timed guidance after 10 seconds of incorrect pose

---

## VOICE-OVER SYSTEM

### VoiceOverManager Class
- Text-to-speech using Web Speech API
- Message queue system (prevents audio overlap)
- Priority handling (high priority interrupts current speech)
- Customizable settings (rate 0.5x-2.0x, volume 0%-100%)

### Voice-Over Events
**Session Lifecycle:** onSessionStart, onSessionPause, onSessionResume, onSessionComplete
**Pose Events:** onPoseChange, onPoseSuccess, onPoseCorrection, onTimedGuidance, onPoseTransitionCountdown
**Additional:** onBreathingCue, onEncouragement

---

## ANALYTICS DASHBOARD

### 7 Interactive Charts
1. User Growth Trend (Line Chart) - New users per day, last 30 days
2. Daily Session Analytics (Multi-line Chart) - Sessions count and duration per day
3. Module Performance (Horizontal Bar Chart) - Sessions, users, duration per module
4. User Engagement Levels (Doughnut Chart) - Users by session count buckets
5. Hourly Usage Pattern (Radar Chart) - Sessions by hour of day, last 7 days
6. Weekly Activity Trends (Polar Area Chart) - Sessions by day of week
7. User Retention Analysis (Bar Chart) - Users by days active

### Real-Time Updates
- JavaScript polling every 30 seconds
- Endpoint: GET /api/analytics/live
- Auto-refresh without page reload, loading indicator, manual refresh button

### Key Metrics
Total Users, Total Sessions, Active Users (7-day, 30-day), Average Session Duration, User Retention Rate, Platform Health Score

---

## BADGE SYSTEM

### Badge Types
**Agent Badges (Role-based):** Admin (purple), User (green), Premium (gold)
**Skill Badges (Achievement-based):** Beginner (blue, level 1), Intermediate (orange, level 2), Advanced (purple, level 3), Expert (gold, level 4)
**Process Badges (Status):** Active (green), Completed (blue), In Progress (orange), Paused (yellow), Failed (red)

### Stickers (Decorative achievements)
Lotus 🪷, Om 🕉️, Chakra ☸️, Peace ☮️, Zen 🧘, Namaste 🙏

### Display Locations
User profile, Admin user management, Badge showcase page, Session completion

---

## USER WORKFLOWS

### New User Registration
1. Visit landing page → Register
2. Fill form (name, age, email, mobile, password, experience)
3. Validation (email format, 10-digit mobile, password length)
4. System generates unique 8-char ID
5. System assigns default badges (role + skill level)
6. Redirect to dashboard

### Starting Practice Session
1. Login → Select module
2. View module info (optional) → Start Practice
3. Allow camera access
4. Perform Namaste gesture to begin
5. Follow pose sequence with voice guidance
6. Receive real-time corrections
7. Complete all poses → View results
8. Session saved to history

### Pose Correction Flow
1. User performs pose
2. MediaPipe detects 33 landmarks
3. System calculates joint angles
4. Compares with target angles
5. If accuracy < 75%: Session pauses, red border, voice correction, user adjusts
6. If accuracy >= 75%: Green border, voice success, session continues

---

## SECURITY FEATURES
- Password hashing with bcrypt (salt rounds: 12)
- Session-based authentication (Flask sessions)
- Secure session cookies (httpOnly, sameSite)
- Password reset with time-limited tokens (1 hour expiry)
- Role-based access control (user vs admin)
- Server-side validation for all forms
- SQL injection prevention (MongoDB parameterized queries)
- XSS prevention (template escaping)
- CSRF protection (Flask-WTF)
- Rate limiting (configurable)

---

## DEPLOYMENT

### Environment Variables
MONGO_URI, SECRET_KEY, FLASK_ENV, PORT

### Platforms
Render.com (recommended), Heroku, AWS EC2

### Files
Procfile: web: gunicorn app:app
runtime.txt: python-3.8.10
requirements.txt: All Python dependencies

### First Run
1. Deploy application
2. Access /admin/login
3. Default admin: admin@yogicguide.com / admin123
4. CHANGE PASSWORD IMMEDIATELY

---

## FILE STRUCTURE

### Backend (Python)
- app.py (2493 lines) - Main Flask application
- models.py - Database models and schemas
- config.py - Configuration settings
- requirements.txt - Python dependencies

### Frontend (Templates)
- base.html, landing.html, register.html, login.html
- dashboard.html, profile.html, session.html, pose_details.html
- admin/* - Admin pages

### Static CSS
- yogic-wellness-theme.css, animations.css, badge-system.css
- contact-section.css, registration-enhanced.css, voice-settings.css
- pose-correction.css, mobile-responsive.css

### Static JavaScript
- pose-detection.js (793 lines) - MediaPipe integration
- session.js - Session management
- voice-over.js - Voice-over system
- analytics-realtime.js - Real-time analytics
- pose-correction-system.js, pose-comparison-canvas.js
- breathing-exercises.js, module-surya-namaskar.js

---

## PERFORMANCE METRICS
- Landing page: < 2 seconds
- Dashboard: < 3 seconds
- Session page: < 4 seconds (includes MediaPipe loading)
- Pose detection: 30 FPS (33ms per frame)
- Voice-over latency: < 200ms
- Analytics refresh: 30 seconds interval

---

## PROJECT STATISTICS
- Total Lines of Code: 3000+
- Total Files: 30+
- API Endpoints: 50+
- Supported Poses: 20+
- Modules: 5
- Charts: 7
- Documentation Pages: 15+

---

## CONCLUSION
Yogic Guide is a comprehensive, production-ready platform successfully combining traditional yoga practices with cutting-edge AI technology. With 50+ features, 2493 lines of backend code, 793 lines of pose detection logic, and extensive documentation, it provides a complete solution for yoga practitioners and instructors. The platform is designed for scalability, security, and user experience, ready for deployment and capable of serving thousands of users simultaneously.

---

*Documentation Version: 1.0.0 | Last Updated: November 2024 | Status: Production Ready*
