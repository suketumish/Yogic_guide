# 🧘 Yogic Guide - Complete Functionality & Working Guide

## Project Overview

**Yogic Guide** is an AI-powered yoga assistant platform that provides real-time pose detection, voice guidance, and comprehensive analytics for yoga practitioners and instructors.

---

## 1. USER SYSTEM

### 1.1 Authentication & Registration
**Features:**
- Email/password registration with validation
- Unique 8-character user ID generation (e.g., "A3F7B2C9")
- Password hashing with bcrypt
- Login with session management
- Password reset via email token
- Admin and user role separation

**User Profile Fields:**
- Name, Age, Gender, Mobile, Email
- Experience Level (Beginner/Intermediate/Advanced)
- Profile stats (total sessions, minutes, poses)
- Badges (agent tags, skill badges, stickers)
- Voice-over preferences (enabled, speed, volume)

### 1.2 User Dashboard
**Displays:**
- Total sessions count
- Total practice minutes
- Current streak (consecutive days)
- Module-wise breakdown (sessions per module)
- Recent 5 sessions with details
- Quick access to practice modules

### 1.3 Profile Management
**Features:**
- View personal information
- Session history with module filtering
- Update voice-over preferences
- View earned badges and stickers
- Track progress metrics

---

## 2. YOGA MODULES

### 2.1 Available Modules
1. **Surya Namaskar** (Sun Salutation) - 12 poses
2. **Breathing Exercises** (Pranayama) - Seated breathing
3. **Stretching Routine** - 5 flexibility poses
4. **Meditation** - Mindfulness sessions
5. **Yoga Practice** - General yoga poses

### 2.2 Module Features
- Dedicated info pages with benefits
- Step-by-step pose sequences
- Hold duration for each pose
- Benefits and cautions listed
- Voice instructions
- Progress tracking per module
