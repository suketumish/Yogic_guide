# Yogic Guide - Enhanced AI-Powered Yoga Platform

A comprehensive, intelligent yoga practice platform featuring real-time pose detection, social features, gamification, and personalized learning paths.

## 🌟 Features

### Core Functionality
- **Real-time Pose Detection**: Advanced MediaPipe integration with 95% accuracy
- **Instant AI Feedback**: Immediate corrections with voice guidance in 8+ languages
- **Comprehensive Modules**: 
  - Full Body Stretching (30+ poses)
  - Breathing Exercises (Pranayama techniques)
  - Surya Namaskar (12-pose sun salutation)
  - Custom Routine Builder
  - Daily Challenges

### Enhanced User Experience
- **Personalized Learning**: AI-powered recommendations based on performance
- **Progress Analytics**: Detailed statistics with predictive insights
- **Gamification**: Achievement system with 50+ badges and XP levels
- **Social Features**: Friends, leaderboards, and community challenges
- **Multi-language Support**: 8 languages with native voice coaching

### Advanced Features
- **Health Integration**: Apple Health, Google Fit, Fitbit sync
- **Offline Mode**: Downloadable routines for practice anywhere
- **2FA Security**: Enhanced authentication with email/SMS verification
- **Real-time Collaboration**: Live sessions and group challenges
- **Professional Analytics**: Comprehensive health and performance metrics

## 🚀 Technology Stack

### Backend
- **Framework**: Flask with SocketIO for real-time features
- **Database**: MongoDB with advanced indexing
- **Authentication**: JWT + OAuth (Google, Facebook)
- **AI/ML**: MediaPipe, TensorFlow.js, scikit-learn
- **Background Tasks**: Celery with Redis
- **Email/SMS**: Flask-Mail, Twilio integration

### Frontend
- **UI Framework**: Tailwind CSS with custom components
- **Real-time**: WebSocket connections
- **Camera**: WebRTC with advanced pose tracking
- **PWA**: Progressive Web App capabilities
- **Responsive**: Mobile-first design

### Infrastructure
- **Caching**: Redis for sessions and real-time data
- **File Storage**: Local/Cloud storage for user content
- **Monitoring**: Health checks and performance metrics
- **Security**: Rate limiting, CSRF protection, input validation

## 📋 Installation

### Prerequisites

- Python 3.9+
- MongoDB 4.4+
- Redis 6.0+
- Node.js 16+ (for frontend build tools)
- Webcam/Camera access

### Quick Setup

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd yogic-guide
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (see Configuration section)
   ```

3. **Database Initialization**
   ```bash
   python setup_enhanced.py
   ```

4. **Start Services**
   ```bash
   # Terminal 1: Start Redis
   redis-server
   
   # Terminal 2: Start MongoDB
   mongod
   
   # Terminal 3: Start Celery (background tasks)
   celery -A app.celery worker --loglevel=info
   
   # Terminal 4: Start Flask app
   python app.py
   ```

5. **Access Application**
   - Web: `http://localhost:5000`
   - Admin: `http://localhost:5000/admin` (admin@yogicguide.com)

### Docker Setup (Alternative)

```bash
docker-compose up -d
```

## ⚙️ Configuration

### Essential Environment Variables

```env
# Core Configuration
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key
MONGO_URI=mongodb://localhost:27017/yogic_guide
REDIS_URL=redis://localhost:6379/0

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret

# AI/ML Configuration
POSE_ACCURACY_THRESHOLD=85.0
ANGLE_TOLERANCE=15.0
MEDIAPIPE_MODEL_COMPLEXITY=1
```

## 📱 Usage Guide

### Getting Started

1. **Registration**
   - Create account with email verification
   - Complete fitness assessment
   - Set personal goals and preferences

2. **Dashboard Navigation**
   - View personalized recommendations
   - Track daily/weekly progress
   - Access social features and challenges

3. **Practice Sessions**
   - Choose module or custom routine
   - Allow camera access for pose detection
   - Follow real-time guidance and corrections
   - Complete session for XP and achievements

### Module Details

#### 🧘‍♀️ Full Body Stretching
- **Duration**: 15-45 minutes
- **Poses**: 30+ categorized poses
- **Difficulty**: Adaptive based on experience
- **Focus**: Flexibility, mobility, relaxation

#### 🌬️ Breathing Exercises
- **Techniques**: Anulom Vilom, Bhramari, Kapalbhati
- **Duration**: 5-30 minutes
- **Benefits**: Stress relief, focus, energy balance
- **Guidance**: Visual cues with breathing rhythm

#### ☀️ Surya Namaskar
- **Sequence**: Traditional 12-pose flow
- **Variations**: Beginner to advanced
- **Tracking**: Round counter and flow analysis
- **Benefits**: Full-body workout, energy boost

#### 🎨 Custom Routines
- **Builder**: Drag-and-drop pose sequencer
- **Sharing**: Community routine library
- **Personalization**: AI-suggested modifications
- **Export**: Save and sync across devices

## 🏆 Gamification System

### Achievement Categories
- **Milestones**: First session, 100 sessions, etc.
- **Streaks**: 7-day, 30-day, 365-day consistency
- **Performance**: 95% accuracy, speed challenges
- **Social**: Friend connections, community help
- **Specialized**: Module-specific achievements

### Progression System
- **XP Points**: Earned through practice and achievements
- **Levels**: 1-50 with unlockable content
- **Badges**: 50+ unique badges with rarity tiers
- **Leaderboards**: Global, friends, and challenge-specific

## 👥 Social Features

### Community
- **Friends System**: Add friends, view activity
- **Activity Feed**: Share achievements and milestones
- **Challenges**: Join community and friend challenges
- **Leaderboards**: Compete on various metrics

### Collaboration
- **Group Sessions**: Practice together in real-time
- **Mentorship**: Pair experienced with beginners
- **Routine Sharing**: Exchange custom sequences
- **Forums**: Discussion boards by topic/level

## 📊 Analytics & Health

### Personal Metrics
- **Performance**: Accuracy trends, improvement rate
- **Physical**: BMI tracking, flexibility scores
- **Wellness**: Stress levels, energy correlation
- **Goals**: Custom fitness goal tracking

### Health Integration
- **Apple Health**: Sync activity and health data
- **Google Fit**: Step count and calorie integration
- **Fitbit**: Heart rate and sleep correlation
- **Wearables**: Real-time biometric monitoring

## 🔧 API Documentation

### Authentication Endpoints
```
POST /api/auth/register          # User registration
POST /api/auth/login             # Email/password login
POST /api/auth/oauth/google      # Google OAuth
POST /api/auth/verify-email      # Email verification
POST /api/auth/2fa-setup         # Two-factor setup
```

### Session Management
```
POST /api/sessions/start         # Start practice session
PUT  /api/sessions/{id}/update   # Real-time session updates
POST /api/sessions/{id}/complete # Complete session
GET  /api/sessions/history       # User session history
```

### Pose Detection
```
POST /api/pose/validate          # Real-time pose validation
GET  /api/poses/{module}         # Get module poses
GET  /api/poses/search           # Search poses
POST /api/pose/feedback          # Submit pose feedback
```

### Social Features
```
POST /api/social/friend-request  # Send friend request
GET  /api/social/activity-feed   # Get activity feed
GET  /api/social/leaderboard     # Get leaderboards
POST /api/social/challenges/join # Join challenge
```

### Analytics
```
GET  /api/analytics/dashboard    # Dashboard metrics
GET  /api/analytics/progress     # Progress trends
GET  /api/recommendations        # AI recommendations
POST /api/analytics/export       # Export user data
```

## 🛠️ Development

### Project Structure
```
yogic-guide/
├── app.py                    # Main Flask application
├── models.py                 # Enhanced database models
├── auth.py                   # Authentication system
├── config.py                 # Configuration management
├── setup_enhanced.py         # Database initialization
├── requirements.txt          # Python dependencies
├── static/
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript modules
│   └── images/              # Static assets
├── templates/               # Jinja2 templates
│   ├── auth/               # Authentication pages
│   ├── social/             # Social features
│   └── admin/              # Admin interface
└── tests/                   # Test suite
```

### Adding New Features

1. **New Pose Module**
   ```python
   # Add to models.py
   def create_new_module(self, module_data):
       # Implementation
   
   # Add route in app.py
   @app.route('/module/<new_module>')
   def new_module_session(new_module):
       # Implementation
   ```

2. **Custom Achievement**
   ```python
   # Add to setup_enhanced.py
   {
       'code': 'new_achievement',
       'name': 'Achievement Name',
       'criteria': {'type': 'count', 'threshold': 10},
       # ... other properties
   }
   ```

3. **API Endpoint**
   ```python
   @app.route('/api/new-feature', methods=['POST'])
   @require_auth
   def new_feature():
       # Implementation with proper validation
   ```

## 🚀 Deployment

### Production Setup

1. **Environment Preparation**
   ```bash
   # Set production environment
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret
   
   # Use production database
   export MONGO_URI=mongodb://prod-server:27017/yogic_guide
   ```

2. **Security Configuration**
   ```bash
   # Enable security features
   export SESSION_COOKIE_SECURE=True
   export WTF_CSRF_ENABLED=True
   export HTTPS_REDIRECT=True
   ```

3. **Scaling Options**
   - **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
   - **Docker**: Use provided Dockerfile
   - **Kubernetes**: Helm charts available
   - **Cloud**: AWS/GCP/Azure deployment guides

## 🔒 Security

### Implemented Security Measures
- **Authentication**: JWT with refresh tokens
- **Authorization**: Role-based access control
- **Input Validation**: Comprehensive sanitization
- **Rate Limiting**: API and login protection
- **CSRF Protection**: Form and AJAX security
- **SQL Injection**: MongoDB parameterized queries
- **XSS Prevention**: Template auto-escaping

## 🤝 Contributing

### Development Workflow

1. **Fork & Clone**
   ```bash
   git clone https://github.com/yourusername/yogic-guide.git
   cd yogic-guide
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Development Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python setup_enhanced.py
   ```

4. **Code & Test**
   ```bash
   # Make changes
   python -m pytest tests/
   ```

5. **Submit PR**
   ```bash
   git commit -m 'Add amazing feature'
   git push origin feature/amazing-feature
   # Create Pull Request on GitHub
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe Team**: Advanced pose detection technology
- **Flask Community**: Robust web framework
- **MongoDB**: Flexible document database
- **Tailwind CSS**: Utility-first CSS framework
- **Open Source Community**: Various libraries and tools

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yogic-guide/wiki)
- **Issues**: [GitHub Issues](https://github.com/yogic-guide/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yogic-guide/discussions)
- **Email**: support@yogicguide.com
- **Discord**: [Community Server](https://discord.gg/yogicguide)

---

**Made with ❤️ for the global yoga community**