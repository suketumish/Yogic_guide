# Quick Fix for Yogic Guide Startup Issue

## Problem
The enhanced version had dependency conflicts with Flask-Limiter and missing optional packages.

## Solution
Created a basic working version with fallback functionality.

## Quick Start

### Option 1: Test First (Recommended)
```bash
# Test if everything works
python test_basic.py

# If tests pass, start the app
python start_basic.py
```

### Option 2: Direct Start
```bash
# Install basic dependencies
pip install -r requirements_basic.txt

# Start the application
python app.py
```

## What's Working

✅ **Basic Features:**
- User registration and login
- Dashboard with basic stats
- Profile management
- Module selection (Stretching, Breathing, Surya Namaskar)
- Session pages
- Basic pose validation API
- Health check endpoint

✅ **Database:**
- MongoDB connection
- User management
- Basic data storage

✅ **UI:**
- Professional clean design (no gradients)
- Responsive layout
- All templates working

## Demo Account
- **Email:** demo@yogicguide.com
- **Password:** demo123

## Enhanced Features (Available but commented out)
The enhanced features are in the code but commented out to avoid dependency issues:
- Advanced authentication (2FA, OAuth)
- Social features (friends, challenges)
- Advanced analytics
- Real-time features
- Email/SMS integration

## To Enable Enhanced Features

1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up services:**
   ```bash
   # Start Redis (for caching)
   redis-server
   
   # Configure email/SMS in .env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   TWILIO_ACCOUNT_SID=your-twilio-sid
   ```

3. **Uncomment enhanced routes in app.py:**
   - Find the comment block starting with `"""` around line 300
   - Remove the comment markers to enable enhanced features

4. **Run setup:**
   ```bash
   python setup_enhanced.py
   ```

## Troubleshooting

### MongoDB Issues
```bash
# Start MongoDB
mongod

# Or install MongoDB
# Windows: Download from mongodb.com
# Mac: brew install mongodb-community
# Linux: sudo apt install mongodb
```

### Dependency Issues
```bash
# Install basic version
pip install -r requirements_basic.txt

# Or full version
pip install -r requirements.txt
```

### Port Issues
If port 5000 is busy, edit app.py and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

## Current Status
- ✅ Basic app working
- ✅ Professional UI theme applied
- ✅ Core functionality available
- 🔄 Enhanced features ready to enable
- 📚 Comprehensive documentation provided

The application now starts successfully with basic functionality and can be enhanced step by step as needed.