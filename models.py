"""
Enhanced Database Models for Zen_Align
Implements the comprehensive schema from the specification
"""

from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import MongoClient
import bcrypt
from typing import Dict, List, Optional, Any

class DatabaseManager:
    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.yogic_guide
        
        # Collections
        self.users = self.db.users
        self.sessions = self.db.sessions
        self.poses = self.db.poses
        self.achievements = self.db.achievements
        self.leaderboards = self.db.leaderboards
        self.challenges = self.db.challenges
        self.social_activities = self.db.social_activities
        self.user_progress = self.db.user_progress
        self.custom_routines = self.db.custom_routines
        
        # Create indexes for performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for optimal performance"""
        # User indexes
        self.users.create_index("email", unique=True)
        self.users.create_index("uniqueId", unique=True, sparse=True)  # NEW: Unique user ID
        self.users.create_index("phone", unique=True, sparse=True)
        self.users.create_index([("social.friends", 1)])
        self.users.create_index([("badges.type", 1)])  # NEW: Badge type index
        
        # Session indexes
        self.sessions.create_index([("userId", 1), ("startTime", -1)])
        self.sessions.create_index([("module", 1)])
        self.sessions.create_index([("module", 1), ("userId", 1)])  # NEW: Module + user compound index
        
        # Leaderboard indexes
        self.leaderboards.create_index([("type", 1), ("rank", 1)])
        self.leaderboards.create_index([("userId", 1), ("type", 1)])
        
        # Achievement indexes
        self.achievements.create_index("code", unique=True)
        
        # Challenge indexes
        self.challenges.create_index([("type", 1), ("startDate", -1)])

class UserModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.collection = db_manager.users
    
    def create_user(self, user_data: Dict) -> ObjectId:
        """Create a new user with enhanced profile"""
        import uuid
        
        # Hash password
        if 'password' in user_data:
            user_data['password'] = bcrypt.hashpw(
                user_data['password'].encode('utf-8'), 
                bcrypt.gensalt()
            )
        
        # Generate unique user ID
        unique_user_id = str(uuid.uuid4())[:8].upper()
        
        # Set defaults
        user_doc = {
            'uniqueId': unique_user_id,  # Unique 8-character ID
            'email': user_data['email'],
            'password': user_data['password'],
            'phone': user_data.get('phone'),
            'profile': {
                'firstName': user_data.get('firstName', ''),
                'lastName': user_data.get('lastName', ''),
                'avatar': user_data.get('avatar', ''),
                'bio': user_data.get('bio', ''),
                'dateOfBirth': user_data.get('dateOfBirth'),
                'gender': user_data.get('gender', ''),
                'location': {
                    'city': user_data.get('city', ''),
                    'country': user_data.get('country', ''),
                    'timezone': user_data.get('timezone', 'UTC')
                }
            },
            'physical': {
                'height': user_data.get('height', 0),
                'weight': user_data.get('weight', 0),
                'bmi': self._calculate_bmi(user_data.get('height', 0), user_data.get('weight', 0)),
                'weightHistory': [],
                'healthConditions': user_data.get('healthConditions', []),
                'injuries': []
            },
            'badges': [  # NEW: Default badges based on role and experience
                {
                    'type': 'agent',
                    'label': 'Admin' if user_data.get('role') == 'admin' else 'User',
                    'color': '#667eea' if user_data.get('role') == 'admin' else '#48bb78',
                    'earnedAt': datetime.now()
                },
                {
                    'type': 'skill',
                    'label': user_data.get('experienceLevel', 'Beginner'),
                    'color': '#4299e1' if user_data.get('experienceLevel', 'Beginner') == 'Beginner' else '#ed8936' if user_data.get('experienceLevel') == 'Intermediate' else '#9f7aea',
                    'level': 1 if user_data.get('experienceLevel', 'Beginner') == 'Beginner' else 2 if user_data.get('experienceLevel') == 'Intermediate' else 3,
                    'earnedAt': datetime.now()
                }
            ],
            'stickers': [],  # NEW: Empty array for earned stickers
            'preferences': {
                'experienceLevel': user_data.get('experienceLevel', 'Beginner'),
                'language': user_data.get('language', 'English'),
                'voice': user_data.get('voice', 'default'),
                'theme': user_data.get('theme', 'light'),
                'voiceOverEnabled': user_data.get('voiceOverEnabled', True),  # NEW: Voice-over preference
                'voiceOverSpeed': user_data.get('voiceOverSpeed', 1.0),  # NEW: Voice speed (0.5-2.0)
                'voiceOverVolume': user_data.get('voiceOverVolume', 1.0),  # NEW: Voice volume (0-1)
                'notifications': {
                    'push': True,
                    'email': True,
                    'frequency': 'daily'
                }
            },
            'goals': [],
            'stats': {
                'totalSessions': 0,
                'totalMinutes': 0,
                'currentStreak': 0,
                'longestStreak': 0,
                'accuracy': 0,
                'level': 1,
                'xp': 0
            },
            'social': {
                'friends': [],
                'followers': [],
                'following': [],
                'achievements': []
            },
            'integrations': {
                'googleFit': False,
                'appleHealth': False,
                'fitbit': False
            },
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'lastLogin': datetime.now(),
            'emailVerified': False,
            'phoneVerified': False,
            'twoFactorEnabled': False
        }
        
        result = self.collection.insert_one(user_doc)
        
        # Initialize user progress
        self.db.user_progress.insert_one({
            'userId': result.inserted_id,
            'dailyStats': {},
            'weeklyStats': {},
            'monthlyStats': {},
            'flexibilityScore': 0,
            'balanceScore': 0,
            'strengthScore': 0,
            'createdAt': datetime.now()
        })
        
        return result.inserted_id
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with enhanced security"""
        user = self.collection.find_one({'email': email})
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # Update last login
            self.collection.update_one(
                {'_id': user['_id']},
                {'$set': {'lastLogin': datetime.now()}}
            )
            return user
        return None
    
    def update_user_stats(self, user_id: ObjectId, session_data: Dict):
        """Update user statistics after session completion"""
        duration_minutes = session_data.get('duration', 0) // 60
        accuracy = session_data.get('accuracy', 0)
        
        # Calculate XP based on performance
        xp_gained = self._calculate_xp(duration_minutes, accuracy)
        
        update_data = {
            '$inc': {
                'stats.totalSessions': 1,
                'stats.totalMinutes': duration_minutes,
                'stats.xp': xp_gained
            },
            '$set': {
                'updatedAt': datetime.now()
            }
        }
        
        # Update accuracy (weighted average)
        user = self.collection.find_one({'_id': user_id})
        if user:
            current_accuracy = user.get('stats', {}).get('accuracy', 0)
            total_sessions = user.get('stats', {}).get('totalSessions', 0)
            
            new_accuracy = ((current_accuracy * total_sessions) + accuracy) / (total_sessions + 1)
            update_data['$set']['stats.accuracy'] = round(new_accuracy, 2)
        
        self.collection.update_one({'_id': user_id}, update_data)
        
        # Check for level up
        self._check_level_up(user_id)
        
        # Update streak
        self._update_streak(user_id)
    
    def _calculate_bmi(self, height_cm: float, weight_kg: float) -> float:
        """Calculate BMI from height and weight"""
        if height_cm > 0 and weight_kg > 0:
            height_m = height_cm / 100
            return round(weight_kg / (height_m ** 2), 2)
        return 0
    
    def _calculate_xp(self, duration_minutes: int, accuracy: float) -> int:
        """Calculate XP based on session performance"""
        base_xp = duration_minutes * 2  # 2 XP per minute
        accuracy_bonus = int(accuracy / 10) * 5  # Bonus for accuracy
        return base_xp + accuracy_bonus
    
    def _check_level_up(self, user_id: ObjectId):
        """Check if user should level up based on XP"""
        user = self.collection.find_one({'_id': user_id})
        if not user:
            return
        
        current_xp = user.get('stats', {}).get('xp', 0)
        current_level = user.get('stats', {}).get('level', 1)
        
        # XP required for next level (exponential growth)
        xp_required = current_level * 100 + (current_level - 1) * 50
        
        if current_xp >= xp_required:
            new_level = current_level + 1
            self.collection.update_one(
                {'_id': user_id},
                {'$set': {'stats.level': new_level}}
            )
            
            # Award level up achievement
            self._award_achievement(user_id, f'level_{new_level}')
    
    def _update_streak(self, user_id: ObjectId):
        """Update user's practice streak"""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        # Check if user practiced yesterday or today
        recent_session = self.db.sessions.find_one({
            'userId': user_id,
            'startTime': {
                '$gte': datetime.combine(yesterday, datetime.min.time()),
                '$lt': datetime.combine(today + timedelta(days=1), datetime.min.time())
            }
        })
        
        user = self.collection.find_one({'_id': user_id})
        current_streak = user.get('stats', {}).get('currentStreak', 0)
        longest_streak = user.get('stats', {}).get('longestStreak', 0)
        
        if recent_session:
            # Continue or start streak
            new_streak = current_streak + 1
            new_longest = max(longest_streak, new_streak)
            
            self.collection.update_one(
                {'_id': user_id},
                {'$set': {
                    'stats.currentStreak': new_streak,
                    'stats.longestStreak': new_longest
                }}
            )
            
            # Check for streak achievements
            if new_streak in [7, 30, 100, 365]:
                self._award_achievement(user_id, f'streak_{new_streak}')
        else:
            # Reset streak if no practice yesterday
            self.collection.update_one(
                {'_id': user_id},
                {'$set': {'stats.currentStreak': 0}}
            )
    
    def _award_achievement(self, user_id: ObjectId, achievement_code: str):
        """Award achievement to user"""
        achievement = self.db.achievements.find_one({'code': achievement_code})
        if not achievement:
            return
        
        # Check if user already has this achievement
        user = self.collection.find_one({'_id': user_id})
        if achievement_code in user.get('social', {}).get('achievements', []):
            return
        
        # Award achievement
        self.collection.update_one(
            {'_id': user_id},
            {
                '$push': {'social.achievements': achievement_code},
                '$inc': {'stats.xp': achievement.get('points', 0)}
            }
        )
        
        # Add to achievement tracking
        self.db.achievements.update_one(
            {'code': achievement_code},
            {'$push': {'unlockedBy': user_id}}
        )

class SessionModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.collection = db_manager.sessions
    
    def create_session(self, user_id: ObjectId, module_type: str, module_name: str = None) -> ObjectId:
        """Create a new practice session with module tracking
        
        Args:
            user_id: User's ObjectId
            module_type: Module type (surya_namaskar, breathing, stretching, etc.)
            module_name: Optional display name for the module
        """
        # If module_name not provided, generate from module_type
        if not module_name:
            module_name_map = {
                'surya_namaskar': 'Surya Namaskar',
                'breathing': 'Breathing Exercises',
                'stretching': 'Stretching Routine',
                'meditation': 'Meditation',
                'custom': 'Custom Routine'
            }
            module_name = module_name_map.get(module_type, module_type.replace('_', ' ').title())
        
        session_doc = {
            'userId': user_id,
            'module': module_type,  # REQUIRED: Module type for tracking
            'moduleName': module_name,
            'startTime': datetime.now(),
            'endTime': None,
            'duration': 0,
            'poses': [],
            'sessionStats': {
                'totalAccuracy': 0,
                'caloriesBurned': 0,
                'rating': 0,
                'difficulty': 'medium',
                'energyLevel': {
                    'before': 0,
                    'after': 0
                }
            },
            'feedback': {
                'rating': 0,
                'difficulty': '',
                'notes': '',
                'bodyParts': {
                    'sore': [],
                    'tight': [],
                    'improved': []
                }
            },
            'deviceInfo': {
                'type': 'unknown',
                'cameraQuality': 'medium',
                'lighting': 'good'
            },
            'isPublic': False,
            'sharedWith': [],
            'createdAt': datetime.now()
        }
        
        result = self.collection.insert_one(session_doc)
        return result.inserted_id
    
    def complete_session(self, session_id: ObjectId, completion_data: Dict):
        """Complete a session with final statistics"""
        end_time = datetime.now()
        
        # Calculate duration if not provided
        session = self.collection.find_one({'_id': session_id})
        if session:
            duration = completion_data.get('duration') or int((end_time - session['startTime']).total_seconds())
        else:
            duration = completion_data.get('duration', 0)
        
        update_data = {
            'endTime': end_time,
            'duration': duration,
            'sessionStats.totalAccuracy': completion_data.get('accuracy', 0),
            'sessionStats.caloriesBurned': completion_data.get('calories', 0),
            'sessionStats.rating': completion_data.get('rating', 0)
        }
        
        if 'poses' in completion_data:
            update_data['poses'] = completion_data['poses']
        
        self.collection.update_one(
            {'_id': session_id},
            {'$set': update_data}
        )
        
        # Update user statistics
        if session:
            user_model = UserModel(self.db)
            user_model.update_user_stats(session['userId'], {
                'duration': duration,
                'accuracy': completion_data.get('accuracy', 0)
            })

class PoseModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.collection = db_manager.poses
    
    def get_poses_by_module(self, module_type: str) -> List[Dict]:
        """Get all poses for a specific module"""
        return list(self.collection.find({'module': module_type}).sort('sequence', 1))
    
    def get_pose_by_name(self, pose_name: str) -> Optional[Dict]:
        """Get specific pose by name"""
        return self.collection.find_one({'name': pose_name})
    
    def search_poses(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search poses with filters"""
        search_filter = {'$text': {'$search': query}}
        
        if filters:
            search_filter.update(filters)
        
        return list(self.collection.find(search_filter))

class AchievementModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.collection = db_manager.achievements
    
    def create_default_achievements(self):
        """Create default achievement set"""
        achievements = [
            {
                'code': 'first_session',
                'name': 'First Steps',
                'description': 'Complete your first yoga session',
                'icon': '🎯',
                'category': 'milestone',
                'criteria': {'type': 'count', 'threshold': 1, 'condition': 'sessions'},
                'rarity': 'common',
                'points': 10,
                'unlockedBy': []
            },
            {
                'code': 'streak_7',
                'name': 'Week Warrior',
                'description': 'Practice for 7 consecutive days',
                'icon': '🔥',
                'category': 'streak',
                'criteria': {'type': 'streak', 'threshold': 7, 'condition': 'days'},
                'rarity': 'uncommon',
                'points': 50,
                'unlockedBy': []
            },
            {
                'code': 'streak_30',
                'name': 'Monthly Master',
                'description': 'Practice for 30 consecutive days',
                'icon': '🏆',
                'category': 'streak',
                'criteria': {'type': 'streak', 'threshold': 30, 'condition': 'days'},
                'rarity': 'rare',
                'points': 200,
                'unlockedBy': []
            },
            {
                'code': 'accuracy_95',
                'name': 'Perfect Form',
                'description': 'Achieve 95% accuracy in a session',
                'icon': '⭐',
                'category': 'performance',
                'criteria': {'type': 'percentage', 'threshold': 95, 'condition': 'accuracy'},
                'rarity': 'epic',
                'points': 100,
                'unlockedBy': []
            }
        ]
        
        for achievement in achievements:
            achievement['createdAt'] = datetime.now()
            self.collection.update_one(
                {'code': achievement['code']},
                {'$setOnInsert': achievement},
                upsert=True
            )

class SocialModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.users = db_manager.users
        self.activities = db_manager.social_activities
    
    def send_friend_request(self, from_user_id: ObjectId, to_user_id: ObjectId):
        """Send friend request"""
        # Check if already friends or request exists
        existing = self.activities.find_one({
            'type': 'friend_request',
            'fromUser': from_user_id,
            'toUser': to_user_id,
            'status': {'$in': ['pending', 'accepted']}
        })
        
        if existing:
            return False
        
        self.activities.insert_one({
            'type': 'friend_request',
            'fromUser': from_user_id,
            'toUser': to_user_id,
            'status': 'pending',
            'createdAt': datetime.now()
        })
        return True
    
    def accept_friend_request(self, request_id: ObjectId):
        """Accept friend request and update both users"""
        request = self.activities.find_one({'_id': request_id})
        if not request or request['status'] != 'pending':
            return False
        
        # Update request status
        self.activities.update_one(
            {'_id': request_id},
            {'$set': {'status': 'accepted', 'acceptedAt': datetime.now()}}
        )
        
        # Add to friends lists
        self.users.update_one(
            {'_id': request['fromUser']},
            {'$addToSet': {'social.friends': request['toUser']}}
        )
        self.users.update_one(
            {'_id': request['toUser']},
            {'$addToSet': {'social.friends': request['fromUser']}}
        )
        
        return True
    
    def get_activity_feed(self, user_id: ObjectId, limit: int = 20) -> List[Dict]:
        """Get activity feed for user's friends"""
        user = self.users.find_one({'_id': user_id})
        if not user:
            return []
        
        friend_ids = user.get('social', {}).get('friends', [])
        friend_ids.append(user_id)  # Include own activities
        
        activities = list(self.activities.find({
            'userId': {'$in': friend_ids},
            'type': {'$in': ['session_complete', 'achievement_unlock', 'level_up']}
        }).sort('createdAt', -1).limit(limit))
        
        return activities