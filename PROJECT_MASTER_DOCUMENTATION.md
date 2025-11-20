# Yogic Guide - Master Project Documentation

## EXECUTIVE SUMMARY
Yogic Guide is a production-ready AI-powered yoga assistant platform that combines ancient wellness practices with modern technology. Built with Python Flask, MongoDB, MediaPipe AI, and responsive web technologies, it provides real-time pose detection, voice guidance, comprehensive analytics, and multi-module yoga practice support for users of all skill levels.

**Version:** 1.0.0 | **Status:** Production Ready | **Tech Stack:** Python Flask, MongoDB, JavaScript, MediaPipe, TailwindCSS

---

## 1. CORE FEATURES

### USER FEATURES
- Secure authentication (registration, login, password reset)
- Unique 8-character user IDs for easy reference
- Multi-module practice (Surya Namaskar, Breathing, Stretching, Meditation, Yoga)
- Real-time pose detection with MediaPipe AI (33-point skeleton tracking)
- Strict pose correction (session stops if accuracy below 75%)
- Voice-over guidance (text-to-speech instructions, corrections, encouragement)
- Progress tracking (session history, accuracy metrics, duration, streaks)
- Badge system (agent tags, skill badges, achievement stickers)
- Responsive design (mobile, tablet, desktop optimized)
- Profile management with session filtering

### ADMIN FEATURES
- User management (view, edit, delete, grant/revoke admin privileges)
- Analytics dashboard with 7 interactive charts
- Real-time data updates (auto-refresh every 30 seconds)
- Session monitoring across all users
- Module performance analytics
- Platform health score (composite metric)
- CSV export functionality
- User activity tracking

---

## 2. TECHNICAL ARCHITECTURE

### BACKEND
**Framework:** Flask 2.0+ (Python 3.8+)
**Database:** MongoDB (Atlas cloud or local)
**Authentication:** bcrypt password hashing, Flask sessions
**API:** RESTful JSON endpoints
**AI/ML:** MediaPipe Pose Detection
**Key Files:** app.py (2493 lines), models.py (enhanced schemas), config.py (environment settings)

### FRONTEND
**UI Framework:** TailwindCSS 3.0+
**JavaScript:** Vanilla JS (ES6+), MediaPipe integration
**Charts:** Chart.js 3.x for analytics visualization
**Icons:** Font Awesome 6.x
**Voice:** Web Speech API for text-to-speech
**Key Files:** pose-detection.js, session.js, voice-over.js, analytics-realtime.js
"Continuing documentation..." 
