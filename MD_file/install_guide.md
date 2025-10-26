# Installation & Setup Guide

## Prerequisites

### 1. Python 3.8+
Check if Python is installed:
```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/

### 2. MongoDB
Download and install MongoDB Community Edition:
https://www.mongodb.com/try/download/community

#### Windows
- Download the MSI installer
- Run installer with default settings
- MongoDB will start automatically as a service

#### Mac
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux (Ubuntu/Debian)
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### 3. Git (Optional)
For cloning the repository:
```bash
git --version
```

Download from: https://git-scm.com/downloads

## Installation Steps

### Step 1: Get the Project
```bash
# If using git
git clone <repository-url>
cd yogic-guide

# Or extract the ZIP file and navigate to the folder
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- pymongo (MongoDB driver)
- bcrypt (password hashing)
- python-dotenv (environment variables)
- mediapipe (pose detection)
- opencv-python (computer vision)

### Step 4: Configure Environment
Create a `.env` file in the project root:
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` file:
```
SECRET_KEY=your-random-secret-key-here-change-this
MONGO_URI=mongodb://localhost:27017/yogic_guide
```

Generate a secure secret key:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5: Verify MongoDB is Running
```bash
# Windows
net start MongoDB

# Mac
brew services list | grep mongodb

# Linux
sudo systemctl status mongod
```

### Step 6: Seed the Database
```bash
python seed_poses.py
```

You should see:
```
✅ Successfully seeded 18 poses to the database!
   - Stretching: 5 poses
   - Surya Namaskar: 12 poses
   - Breathing: 1 poses
```

### Step 7: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 8: Access the Application
Open your browser and go to:
```
http://localhost:5000
```

## First Time Usage

1. **Register Account**
   - Click "Register"
   - Fill in your details
   - Choose experience level

2. **Login**
   - Use your email and password
   - You'll be redirected to the dashboard

3. **Allow Camera Access**
   - When starting a session, allow camera permissions
   - This is required for pose detection

4. **Start Your First Session**
   - Choose "Full Body Stretching" for beginners
   - Show Namaste gesture (🙏) to start
   - Follow on-screen instructions

## Troubleshooting

### MongoDB Connection Error
```
pymongo.errors.ServerSelectionTimeoutError
```
**Solution:**
- Ensure MongoDB is running
- Check MONGO_URI in .env file
- Try: `mongodb://127.0.0.1:27017/yogic_guide`

### Camera Not Working
**Solution:**
- Check browser permissions (Settings > Privacy > Camera)
- Use HTTPS or localhost (required for camera access)
- Close other apps using the camera
- Try a different browser (Chrome recommended)

### MediaPipe Import Error
```
ImportError: No module named 'mediapipe'
```
**Solution:**
```bash
pip install --upgrade mediapipe opencv-python
```

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:**
```bash
# Find and kill the process
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Or change the port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Speech Synthesis Not Working
**Solution:**
- Check browser audio permissions
- Unmute the browser tab
- Try Chrome or Edge (best support)
- Check system volume

## Browser Compatibility

### Recommended Browsers
- ✅ Google Chrome (Best)
- ✅ Microsoft Edge
- ✅ Firefox
- ⚠️ Safari (Limited MediaPipe support)

### Required Features
- WebRTC (Camera access)
- Web Speech API (Audio feedback)
- Canvas API (Skeleton overlay)
- ES6+ JavaScript

## System Requirements

### Minimum
- CPU: Dual-core 2.0 GHz
- RAM: 4 GB
- Camera: 720p webcam
- Internet: For CDN resources

### Recommended
- CPU: Quad-core 2.5 GHz+
- RAM: 8 GB+
- Camera: 1080p webcam
- Internet: Stable connection

## Development Mode

### Enable Debug Mode
Already enabled in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### View Logs
Flask will show detailed logs in the terminal

### Auto-Reload
Changes to Python files will auto-reload the server

## Production Deployment

### Disable Debug Mode
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Use Production Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
Set proper SECRET_KEY and MONGO_URI for production

### HTTPS Required
Camera access requires HTTPS in production

## Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- MongoDB Documentation: https://docs.mongodb.com/
- MediaPipe Pose: https://google.github.io/mediapipe/solutions/pose
- Tailwind CSS: https://tailwindcss.com/docs

## Support

If you encounter issues:
1. Check this guide first
2. Review error messages carefully
3. Search for similar issues online
4. Create an issue in the repository

---

**Happy Coding! 🧘‍♀️**
