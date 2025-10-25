# Quick Start Guide 🚀

Get your AI-Powered Yogic Guide running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher
- ✅ MongoDB installed and running
- ✅ A webcam
- ✅ Modern browser (Chrome recommended)

## Installation (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and set your SECRET_KEY
# You can generate one with:
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Seed Database
```bash
python seed_poses.py
```

## Running the App

### Option 1: Quick Start Script

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

```bash
# Start MongoDB (if not running)
# Windows: net start MongoDB
# Mac: brew services start mongodb-community
# Linux: sudo systemctl start mongod

# Run Flask app
python app.py
```

## First Use

1. **Open Browser**
   ```
   http://localhost:5000
   ```

2. **Register Account**
   - Click "Register"
   - Fill in your details
   - Choose experience level

3. **Start First Session**
   - Login with your credentials
   - Choose "Full Body Stretching" (beginner-friendly)
   - Allow camera access when prompted
   - Show Namaste gesture 🙏 to begin

## Module Overview

### 🧘‍♀️ Full Body Stretching
- **Duration:** 15-20 minutes
- **Poses:** 5 stretching poses
- **Level:** Beginner friendly
- **Best for:** Flexibility and relaxation

### 🌬️ Breathing Exercises
- **Duration:** 1-10 minutes
- **Exercises:** 4 pranayama techniques
- **Level:** All levels
- **Best for:** Stress relief and focus

### ☀️ Surya Namaskar
- **Duration:** 10-12 minutes
- **Poses:** 12-pose sequence
- **Level:** Intermediate
- **Best for:** Energy and full-body workout

## Tips for Best Experience

### Camera Setup
- ✅ Good lighting (natural light is best)
- ✅ Stand 6-8 feet from camera
- ✅ Full body visible in frame
- ✅ Plain background (no clutter)
- ✅ Wear contrasting clothes

### Audio
- 🔊 Enable sound for instructions
- 🎧 Use headphones for better clarity
- 🔇 Mute if you prefer silent practice

### Session Tips
- 🧘 Start with beginner module
- ⏸️ Use pause if you need a break
- 📊 Check your progress after each session
- 🔥 Build a daily streak for best results

## Troubleshooting

### Camera Not Working?
```bash
# Check browser permissions
# Chrome: Settings > Privacy > Camera
# Allow camera access for localhost
```

### MongoDB Connection Error?
```bash
# Check if MongoDB is running
# Windows: sc query MongoDB
# Mac: brew services list
# Linux: sudo systemctl status mongod

# If not running, start it:
# Windows: net start MongoDB
# Mac: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

### Port Already in Use?
```bash
# Change port in app.py
# Line: app.run(debug=True, host='0.0.0.0', port=5001)
```

### MediaPipe Not Loading?
```bash
# Reinstall dependencies
pip install --upgrade mediapipe opencv-python
```

## Quick Commands

```bash
# Check Python version
python --version

# Check MongoDB status
# Windows: sc query MongoDB
# Mac: brew services list | grep mongodb
# Linux: sudo systemctl status mongod

# View database
mongo
> use yogic_guide
> db.users.find()
> db.sessions.find()

# Clear database (reset)
mongo
> use yogic_guide
> db.dropDatabase()
# Then run: python seed_poses.py

# Stop Flask server
# Press Ctrl+C in terminal
```

## Project Structure

```
yogic-guide/
├── app.py              # Main Flask app
├── seed_poses.py       # Database seeding
├── templates/          # HTML templates
├── static/
│   ├── js/            # JavaScript files
│   └── css/           # Stylesheets
└── .env               # Configuration
```

## Next Steps

1. ✅ Complete your first session
2. 📊 Check your profile and stats
3. 🔥 Build a daily practice streak
4. 🎯 Try all three modules
5. 📈 Track your progress over time

## Support

- 📖 Full documentation: `README.md`
- 🔧 Installation guide: `install_guide.md`
- ✨ Features list: `FEATURES.md`
- 🧪 Testing guide: `TESTING.md`

## Common Questions

**Q: Do I need internet connection?**
A: Yes, for MediaPipe CDN and Tailwind CSS. Local hosting possible with modifications.

**Q: Can I use on mobile?**
A: Yes, but desktop/laptop recommended for better camera angle.

**Q: Is my data private?**
A: Yes, all data stored locally in your MongoDB instance.

**Q: Can I customize poses?**
A: Yes, edit `seed_poses.py` and re-run to add custom poses.

**Q: How accurate is pose detection?**
A: MediaPipe is highly accurate. Ensure good lighting and full body visibility.

---

**Ready to start your yoga journey? Let's go! 🧘‍♀️**

```bash
python app.py
```

Open http://localhost:5000 and begin! 🙏
