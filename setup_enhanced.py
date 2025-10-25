#!/usr/bin/env python3
"""
Enhanced Setup Script for Yogic Guide
Initializes database with comprehensive data structure
"""

import os
import sys
from datetime import datetime, timedelta
from bson import ObjectId

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import DatabaseManager, AchievementModel
from config import config

def setup_database():
    """Initialize database with enhanced schema and default data"""
    
    # Get configuration
    config_name = os.getenv('FLASK_ENV', 'development')
    app_config = config[config_name]
    
    # Initialize database manager
    db_manager = DatabaseManager(app_config.MONGO_URI)
    
    print("🚀 Setting up Enhanced Yogic Guide Database...")
    
    # 1. Create comprehensive pose library
    create_pose_library(db_manager)
    
    # 2. Create achievement system
    create_achievements(db_manager)
    
    # 3. Create sample challenges
    create_challenges(db_manager)
    
    # 4. Create sample users (for development)
    if config_name == 'development':
        create_sample_users(db_manager)
    
    # 5. Initialize system settings
    create_system_settings(db_manager)
    
    print("✅ Database setup completed successfully!")
    print("\n📋 Setup Summary:")
    print(f"   • Poses: {db_manager.poses.count_documents({})}")
    print(f"   • Achievements: {db_manager.achievements.count_documents({})}")
    print(f"   • Challenges: {db_manager.challenges.count_documents({})}")
    print(f"   • Users: {db_manager.users.count_documents({})}")

def create_pose_library(db_manager):
    """Create comprehensive pose library"""
    print("📚 Creating pose library...")
    
    poses = [
        # Standing Poses
        {
            'name': 'Mountain Pose',
            'sanskrit': 'Tadasana',
            'module': 'stretching',
            'sequence': 1,
            'difficulty': 'beginner',
            'category': 'standing',
            'duration': {'hold': 30, 'default': 30, 'minimum': 15, 'maximum': 60},
            'referenceImage': {'url': '/static/images/poses/mountain-pose.jpg'},
            'technique': {
                'startingPosition': 'Stand tall with feet hip-width apart',
                'steps': [
                    'Ground through your feet',
                    'Engage your leg muscles',
                    'Lengthen your spine',
                    'Relax your shoulders',
                    'Breathe deeply'
                ],
                'alignment': [
                    'Keep your weight evenly distributed',
                    'Maintain natural curves of spine',
                    'Crown of head reaching toward ceiling'
                ],
                'warnings': ['Avoid locking knees', 'Don\'t hold breath']
            },
            'benefits': {
                'primary': ['Improves posture', 'Builds foundation', 'Increases awareness'],
                'secondary': ['Calms mind', 'Reduces stress', 'Improves balance']
            },
            'muscles': {
                'primary': ['Core', 'Legs'],
                'secondary': ['Back', 'Shoulders'],
                'joints': ['Ankles', 'Knees', 'Hips', 'Spine']
            },
            'measurements': {
                'shoulderAngle': {'min': 170, 'max': 190, 'ideal': 180},
                'hipAngle': {'min': 170, 'max': 190, 'ideal': 180},
                'bodySymmetry': 0.9
            },
            'contraindications': ['Severe balance issues'],
            'modifications': [
                {
                    'name': 'Wall Support',
                    'difficulty': 'easier',
                    'description': 'Stand with back against wall for support'
                }
            ],
            'tags': ['beginner', 'foundation', 'posture', 'grounding'],
            'createdAt': datetime.now()
        },
        {
            'name': 'Downward Facing Dog',
            'sanskrit': 'Adho Mukha Svanasana',
            'module': 'stretching',
            'sequence': 2,
            'difficulty': 'beginner',
            'category': 'inversion',
            'duration': {'hold': 45, 'default': 45, 'minimum': 20, 'maximum': 90},
            'technique': {
                'startingPosition': 'Start on hands and knees',
                'steps': [
                    'Tuck toes under',
                    'Lift hips up and back',
                    'Straighten legs as much as possible',
                    'Press hands firmly into ground',
                    'Create inverted V shape'
                ],
                'alignment': [
                    'Hands shoulder-width apart',
                    'External rotation of arms',
                    'Long spine from hands to tailbone'
                ]
            },
            'benefits': {
                'primary': ['Stretches hamstrings', 'Strengthens arms', 'Lengthens spine'],
                'secondary': ['Calms nervous system', 'Improves circulation', 'Energizes body']
            },
            'measurements': {
                'shoulderAngle': {'min': 40, 'max': 60, 'ideal': 50},
                'hipAngle': {'min': 70, 'max': 90, 'ideal': 80},
                'elbowAngle': {'min': 170, 'max': 180, 'ideal': 175}
            },
            'contraindications': ['Wrist injuries', 'High blood pressure', 'Late pregnancy'],
            'tags': ['inversion', 'strength', 'flexibility', 'energizing'],
            'createdAt': datetime.now()
        },
        {
            'name': 'Warrior I',
            'sanskrit': 'Virabhadrasana I',
            'module': 'stretching',
            'sequence': 3,
            'difficulty': 'beginner',
            'category': 'standing',
            'duration': {'hold': 30, 'default': 30, 'minimum': 15, 'maximum': 60},
            'technique': {
                'startingPosition': 'Step left foot back 3-4 feet',
                'steps': [
                    'Turn left foot out 45 degrees',
                    'Bend right knee over ankle',
                    'Square hips toward front',
                    'Reach arms overhead',
                    'Hold and breathe'
                ]
            },
            'benefits': {
                'primary': ['Strengthens legs', 'Opens hips', 'Improves balance'],
                'secondary': ['Builds confidence', 'Increases focus', 'Energizes body']
            },
            'measurements': {
                'frontKnee': {'min': 85, 'max': 95, 'ideal': 90},
                'shoulderAngle': {'min': 170, 'max': 190, 'ideal': 180}
            },
            'contraindications': ['Knee injuries', 'High blood pressure'],
            'tags': ['warrior', 'strength', 'balance', 'grounding'],
            'createdAt': datetime.now()
        },
        
        # Breathing Exercises
        {
            'name': 'Deep Belly Breathing',
            'sanskrit': 'Dirgha Pranayama',
            'module': 'breathing',
            'sequence': 1,
            'difficulty': 'beginner',
            'category': 'pranayama',
            'duration': {'hold': 300, 'default': 300, 'minimum': 120, 'maximum': 600},
            'technique': {
                'startingPosition': 'Sit comfortably or lie down',
                'steps': [
                    'Place one hand on chest, one on belly',
                    'Breathe slowly through nose',
                    'Expand belly on inhale',
                    'Exhale slowly through nose',
                    'Keep chest relatively still'
                ]
            },
            'benefits': {
                'primary': ['Reduces stress', 'Calms nervous system', 'Improves focus'],
                'secondary': ['Lowers blood pressure', 'Aids digestion', 'Promotes sleep']
            },
            'contraindications': [],
            'tags': ['breathing', 'relaxation', 'stress-relief', 'beginner'],
            'createdAt': datetime.now()
        },
        
        # Surya Namaskar Sequence
        {
            'name': 'Prayer Pose',
            'sanskrit': 'Pranamasana',
            'module': 'surya-namaskar',
            'sequence': 1,
            'difficulty': 'beginner',
            'category': 'standing',
            'duration': {'hold': 10, 'default': 10, 'minimum': 5, 'maximum': 20},
            'technique': {
                'startingPosition': 'Stand at front of mat',
                'steps': [
                    'Bring palms together at heart center',
                    'Close eyes and center yourself',
                    'Set intention for practice'
                ]
            },
            'benefits': {
                'primary': ['Centers mind', 'Prepares for practice'],
                'secondary': ['Improves focus', 'Calms nervous system']
            },
            'measurements': {
                'shoulderAngle': {'min': 170, 'max': 190, 'ideal': 180}
            },
            'tags': ['surya-namaskar', 'centering', 'prayer', 'beginning'],
            'createdAt': datetime.now()
        }
    ]
    
    # Insert poses
    for pose in poses:
        db_manager.poses.update_one(
            {'name': pose['name']},
            {'$setOnInsert': pose},
            upsert=True
        )
    
    print(f"   ✓ Created {len(poses)} poses")

def create_achievements(db_manager):
    """Create comprehensive achievement system"""
    print("🏆 Creating achievement system...")
    
    achievements = [
        # Milestone Achievements
        {
            'code': 'first_session',
            'name': 'First Steps',
            'description': 'Complete your first yoga session',
            'icon': '🎯',
            'category': 'milestone',
            'criteria': {'type': 'count', 'threshold': 1, 'condition': 'sessions'},
            'rarity': 'common',
            'points': 10,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        {
            'code': 'week_warrior',
            'name': 'Week Warrior',
            'description': 'Practice for 7 consecutive days',
            'icon': '🔥',
            'category': 'streak',
            'criteria': {'type': 'streak', 'threshold': 7, 'condition': 'days'},
            'rarity': 'uncommon',
            'points': 50,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        {
            'code': 'monthly_master',
            'name': 'Monthly Master',
            'description': 'Practice for 30 consecutive days',
            'icon': '🏆',
            'category': 'streak',
            'criteria': {'type': 'streak', 'threshold': 30, 'condition': 'days'},
            'rarity': 'rare',
            'points': 200,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        {
            'code': 'centurion',
            'name': 'Centurion',
            'description': 'Complete 100 yoga sessions',
            'icon': '💯',
            'category': 'milestone',
            'criteria': {'type': 'count', 'threshold': 100, 'condition': 'sessions'},
            'rarity': 'epic',
            'points': 500,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        
        # Performance Achievements
        {
            'code': 'perfect_form',
            'name': 'Perfect Form',
            'description': 'Achieve 95% accuracy in a session',
            'icon': '⭐',
            'category': 'performance',
            'criteria': {'type': 'percentage', 'threshold': 95, 'condition': 'accuracy'},
            'rarity': 'epic',
            'points': 100,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        {
            'code': 'speed_demon',
            'name': 'Speed Demon',
            'description': 'Complete a session 20% faster than average',
            'icon': '⚡',
            'category': 'performance',
            'criteria': {'type': 'percentage', 'threshold': 120, 'condition': 'speed'},
            'rarity': 'rare',
            'points': 75,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        
        # Social Achievements
        {
            'code': 'social_butterfly',
            'name': 'Social Butterfly',
            'description': 'Add 10 friends',
            'icon': '🦋',
            'category': 'social',
            'criteria': {'type': 'count', 'threshold': 10, 'condition': 'friends'},
            'rarity': 'uncommon',
            'points': 30,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        {
            'code': 'mentor',
            'name': 'Mentor',
            'description': 'Help 5 beginners improve their practice',
            'icon': '👨‍🏫',
            'category': 'social',
            'criteria': {'type': 'count', 'threshold': 5, 'condition': 'mentoring'},
            'rarity': 'rare',
            'points': 150,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        
        # Specialized Achievements
        {
            'code': 'breathing_master',
            'name': 'Breathing Master',
            'description': 'Complete 50 breathing exercises',
            'icon': '🌬️',
            'category': 'specialized',
            'criteria': {'type': 'count', 'threshold': 50, 'condition': 'breathing_sessions'},
            'rarity': 'rare',
            'points': 100,
            'unlockedBy': [],
            'createdAt': datetime.now()
        },
        {
            'code': 'sun_salutation_champion',
            'name': 'Sun Salutation Champion',
            'description': 'Complete 100 Surya Namaskar rounds',
            'icon': '☀️',
            'category': 'specialized',
            'criteria': {'type': 'count', 'threshold': 100, 'condition': 'surya_rounds'},
            'rarity': 'epic',
            'points': 200,
            'unlockedBy': [],
            'createdAt': datetime.now()
        }
    ]
    
    for achievement in achievements:
        db_manager.achievements.update_one(
            {'code': achievement['code']},
            {'$setOnInsert': achievement},
            upsert=True
        )
    
    print(f"   ✓ Created {len(achievements)} achievements")

def create_challenges(db_manager):
    """Create sample challenges"""
    print("🎯 Creating challenges...")
    
    challenges = [
        {
            'title': '7-Day Morning Yoga Challenge',
            'description': 'Start your day with yoga for 7 consecutive days',
            'type': 'weekly',
            'difficulty': 'beginner',
            'duration': 7,
            'startDate': datetime.now(),
            'endDate': datetime.now() + timedelta(days=7),
            'rules': 'Practice any yoga module for at least 15 minutes each morning',
            'reward': {
                'points': 100,
                'badge': 'morning_warrior',
                'prize': 'Morning Warrior Badge'
            },
            'participants': [],
            'leaderboard': [],
            'createdAt': datetime.now()
        },
        {
            'title': 'Flexibility Focus Month',
            'description': 'Improve your flexibility with daily stretching',
            'type': 'monthly',
            'difficulty': 'intermediate',
            'duration': 30,
            'startDate': datetime.now(),
            'endDate': datetime.now() + timedelta(days=30),
            'rules': 'Complete stretching module at least 20 days out of 30',
            'reward': {
                'points': 300,
                'badge': 'flexibility_master',
                'prize': 'Flexibility Master Certificate'
            },
            'participants': [],
            'leaderboard': [],
            'createdAt': datetime.now()
        },
        {
            'title': 'Daily Mindfulness',
            'description': 'Practice breathing exercises daily for inner peace',
            'type': 'daily',
            'difficulty': 'beginner',
            'duration': 1,
            'startDate': datetime.now(),
            'endDate': datetime.now() + timedelta(days=1),
            'rules': 'Complete at least one breathing exercise',
            'reward': {
                'points': 20,
                'badge': 'mindful_moment',
                'prize': 'Daily Mindfulness Points'
            },
            'participants': [],
            'leaderboard': [],
            'createdAt': datetime.now()
        }
    ]
    
    for challenge in challenges:
        db_manager.challenges.insert_one(challenge)
    
    print(f"   ✓ Created {len(challenges)} challenges")

def create_sample_users(db_manager):
    """Create sample users for development"""
    print("👥 Creating sample users...")
    
    from auth import AuthManager
    
    # Create a mock auth manager for password hashing
    class MockAuthManager:
        def hash_password(self, password):
            import bcrypt
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    auth_manager = MockAuthManager()
    
    sample_users = [
        {
            'email': 'demo@yogicguide.com',
            'password': auth_manager.hash_password('demo123'),
            'profile': {
                'firstName': 'Demo',
                'lastName': 'User',
                'avatar': '',
                'bio': 'Demo user for testing',
                'dateOfBirth': datetime(1990, 1, 1),
                'gender': 'Other',
                'location': {
                    'city': 'Demo City',
                    'country': 'Demo Country',
                    'timezone': 'UTC'
                }
            },
            'physical': {
                'height': 170,
                'weight': 70,
                'bmi': 24.2,
                'weightHistory': [],
                'healthConditions': [],
                'injuries': []
            },
            'preferences': {
                'experienceLevel': 'Intermediate',
                'language': 'English',
                'voice': 'default',
                'theme': 'light',
                'notifications': {
                    'push': True,
                    'email': True,
                    'frequency': 'daily'
                }
            },
            'goals': [
                {
                    'type': 'flexibility',
                    'target': 80,
                    'deadline': datetime.now() + timedelta(days=90),
                    'progress': 45
                }
            ],
            'stats': {
                'totalSessions': 25,
                'totalMinutes': 750,
                'currentStreak': 5,
                'longestStreak': 12,
                'accuracy': 87.5,
                'level': 3,
                'xp': 450
            },
            'social': {
                'friends': [],
                'followers': [],
                'following': [],
                'achievements': ['first_session', 'week_warrior']
            },
            'integrations': {
                'googleFit': False,
                'appleHealth': False,
                'fitbit': False
            },
            'createdAt': datetime.now() - timedelta(days=30),
            'updatedAt': datetime.now(),
            'lastLogin': datetime.now(),
            'emailVerified': True,
            'phoneVerified': False,
            'twoFactorEnabled': False
        }
    ]
    
    for user in sample_users:
        existing_user = db_manager.users.find_one({'email': user['email']})
        if not existing_user:
            user_id = db_manager.users.insert_one(user).inserted_id
            
            # Create user progress
            db_manager.user_progress.insert_one({
                'userId': user_id,
                'dailyStats': {},
                'weeklyStats': {},
                'monthlyStats': {},
                'flexibilityScore': 75,
                'balanceScore': 68,
                'strengthScore': 72,
                'createdAt': datetime.now()
            })
    
    print(f"   ✓ Created {len(sample_users)} sample users")

def create_system_settings(db_manager):
    """Create system settings and configuration"""
    print("⚙️ Creating system settings...")
    
    settings = {
        'app_version': '2.0.0',
        'maintenance_mode': False,
        'features': {
            'social_features': True,
            'challenges': True,
            'custom_routines': True,
            'ai_recommendations': True,
            'health_integration': True
        },
        'limits': {
            'max_friends': 500,
            'max_custom_routines': 20,
            'max_session_duration': 7200,  # 2 hours
            'max_file_size': 16777216  # 16MB
        },
        'defaults': {
            'session_timeout': 1800,  # 30 minutes
            'pose_hold_time': 30,
            'accuracy_threshold': 85.0,
            'angle_tolerance': 15.0
        },
        'createdAt': datetime.now(),
        'updatedAt': datetime.now()
    }
    
    db_manager.db.system_settings.update_one(
        {'_id': 'main'},
        {'$setOnInsert': settings},
        upsert=True
    )
    
    print("   ✓ Created system settings")

if __name__ == '__main__':
    setup_database()