# 🧘 Yogic Guide - Complete Project Documentation

## 📖 Executive Summary

**Yogic Guide** is a production-ready AI-powered yoga assistant platform combining ancient wellness practices with modern technology. Built with Python Flask, MongoDB, MediaPipe AI, and responsive web technologies.

**Version:** 1.0.0 | **Status:** ✅ Production Ready | **License:** MIT

---

## 🎯 Core Features

### User Features
- **Secure Authentication** - Registration, login, password reset, 2FA support
- **Unique User IDs** - 8-character alphanumeric identifiers
- **Multi-Module Practice** - Surya Namaskar, Breathing, Stretching, Meditation, Yoga
- **Real-Time Pose Detection** - MediaPipe AI with 33-point skeleton tracking
- **Strict Pose Correction** - Session stops if accuracy < 75%
- **Voice-Over Guidance** - Text-to-speech instructions and feedback
- **Progress Tracking** - Session history, accuracy metrics, duration
- **Badge System** - Agent tags, skill badges, achievement stickers
- **Responsive Design** - Mobile, tablet, desktop optimized

### Admin Features
- **User Management** - View, edit, delete users; manage permissions
- **Analytics Dashboard** - 7 interactive charts with real-time data
- **Session Monitoring** - Track all sessions with user details
- **Module Performance** - Analytics by module type
- **Platform Health Score** - Composite engagement metrics
- **Export Functionality** - Download analytics as CSV
- **Real-Time Updates** - Auto-refresh every 30 seconds

---

## 🏗️ Technical Architecture

### Backend Stack
- **Framework:** Flask 2.0+ (Python 3.8+)
- **Database:** MongoDB Atlas / Local MongoDB
- **Authentication:** bcrypt, Flask sessions
- **API:** RESTful JSON endpoints
- **AI/ML:** MediaPipe Pose Detection

### Frontend Stack
- **UI Framework:** TailwindCSS 3.0+
- **JavaScript:** Vanilla JS (ES6+)
- **Charts:** Chart.js 3.x
- **Icons:** Font Awesome 6.x
- **Voice:** Web Speech API
