# Database Schema Enhancements - Developer Guide

## Quick Reference

This guide provides quick examples for working with the enhanced database schema.

## New User Fields

### Unique User ID

Every user now has an 8-character unique identifier:

```python
# Accessing unique ID
user = db.users.find_one({'email': 'user@example.com'})
print(user['uniqueId'])  # Output: "A3F7B2C9"

# Finding user by unique ID
user = db.users.find_one({'uniqueId': 'A3F7B2C9'})
```

### Badges

Users have badges for roles, skills, and achievements:

```python
# Badge structure
{
    'type': 'agent',  # or 'skill', 'process'
    'label': 'Admin',
    'color': '#667eea',
    'level': 3,  # optional, for skill badges
    'earnedAt': datetime.now()
}

# Accessing badges
user = db.users.find_one({'email': 'user@example.com'})
for badge in user['badges']:
    print(f"{badge['type']}: {badge['label']}")

# Adding a new badge
db.users.update_one(
    {'_id': user_id},
    {
        '$push': {
            'badges': {
                'type': 'process',
                'label': 'Completed 100 Sessions',
                'color': '#38b2ac',
                'earnedAt': datetime.now()
            }
        }
    }
)

# Querying users by badge type
users_with_skill_badges = db.users.find({'badges.type': 'skill'})
```

### Stickers

Decorative achievement stickers:

```python
# Adding stickers
db.users.update_one(
    {'_id': user_id},
    {'$addToSet': {'stickers': 'lotus'}}
)

# Multiple stickers
db.users.update_one(
    {'_id': user_id},
    {'$addToSet': {'stickers': {'$each': ['om', 'chakra', 'mandala']}}}
)

# Checking if user has sticker
user = db.users.find_one({'_id': user_id})
if 'lotus' in user.get('stickers', []):
    print("User has lotus sticker!")
```

### Voice-Over Preferences

User preferences for audio guidance:

```python
# Accessing voice-over settings
user = db.users.find_one({'_id': user_id})
preferences = user['preferences']

enabled = preferences['voiceOverEnabled']  # Boolean
speed = preferences['voiceOverSpeed']      # 0.5 - 2.0
volume = preferences['voiceOverVolume']    # 0.0 - 1.0

# Updating voice-over settings
db.users.update_one(
    {'_id': user_id},
    {
        '$set': {
            'preferences.voiceOverEnabled': False,
            'preferences.voiceOverSpeed': 1.2,
            'preferences.voiceOverVolume': 0.8
        }
    }
)
```

## Session Module Tracking

### Creating Sessions with Module Type

```python
from models import SessionModel, DatabaseManager

# Initialize
db_manager = DatabaseManager(mongo_uri)
session_model = SessionModel(db_manager)

# Create session with module type
session_id = session_model.create_session(
    user_id=user_id,
    module_type='surya_namaskar'  # Required
)

# Module types available:
# - 'surya_namaskar': Sun Salutation
# - 'breathing': Pranayama exercises
# - 'stretching': Flexibility routines
# - 'meditation': Mindfulness sessions
# - 'custom': User-created routines
```

### Querying Sessions by Module

```python
# Get all Surya Namaskar sessions for a user
sessions = db.sessions.find({
    'userId': user_id,
    'module': 'surya_namaskar'
}).sort('startTime', -1)

# Get session count by module
pipeline = [
    {'$match': {'userId': user_id}},
    {'$group': {
        '_id': '$module',
        'count': {'$sum': 1},
        'avgAccuracy': {'$avg': '$sessionStats.totalAccuracy'}
    }}
]
module_stats = list(db.sessions.aggregate(pipeline))

# Get recent sessions across all modules
recent_sessions = db.sessions.find({
    'userId': user_id
}).sort('startTime', -1).limit(10)

for session in recent_sessions:
    print(f"{session['module']}: {session['sessionStats']['totalAccuracy']}%")
```

### Module-Specific Analytics

```python
# Get user progress by module
def get_module_progress(user_id, module_type):
    pipeline = [
        {'$match': {
            'userId': user_id,
            'module': module_type
        }},
        {'$group': {
            '_id': None,
            'totalSessions': {'$sum': 1},
            'avgAccuracy': {'$avg': '$sessionStats.totalAccuracy'},
            'totalDuration': {'$sum': '$duration'},
            'completedSessions': {
                '$sum': {'$cond': [{'$ne': ['$endTime', None]}, 1, 0]}
            }
        }}
    ]
    
    result = list(db.sessions.aggregate(pipeline))
    return result[0] if result else None

# Usage
progress = get_module_progress(user_id, 'breathing')
print(f"Breathing sessions: {progress['totalSessions']}")
print(f"Average accuracy: {progress['avgAccuracy']}%")
```

## Using Enhanced Models

### Creating a New User

```python
from models import UserModel, DatabaseManager

# Initialize
db_manager = DatabaseManager(mongo_uri)
user_model = UserModel(db_manager)

# Create user (automatically includes new fields)
user_id = user_model.create_user({
    'email': 'newuser@example.com',
    'password': 'secure_password',
    'firstName': 'John',
    'lastName': 'Doe',
    'experienceLevel': 'Intermediate',
    'role': 'user'
})

# User will automatically have:
# - uniqueId: Generated 8-char ID
# - badges: Default role and skill badges
# - stickers: Empty array
# - preferences.voiceOverEnabled: True
# - preferences.voiceOverSpeed: 1.0
# - preferences.voiceOverVolume: 1.0
```

### Displaying User Info in Templates

```html
<!-- Flask/Jinja2 template example -->
<div class="user-profile">
    <h2>{{ user.profile.firstName }} {{ user.profile.lastName }}</h2>
    <p class="user-id">ID: {{ user.uniqueId }}</p>
    
    <!-- Display badges -->
    <div class="badges">
        {% for badge in user.badges %}
        <span class="badge badge-{{ badge.type }}" 
              style="background: {{ badge.color }}">
            {{ badge.label }}
            {% if badge.level %}
                <span class="badge-level">Lv.{{ badge.level }}</span>
            {% endif %}
        </span>
        {% endfor %}
    </div>
    
    <!-- Display stickers -->
    <div class="stickers">
        {% for sticker in user.stickers %}
        <img src="/static/stickers/{{ sticker }}.png" 
             alt="{{ sticker }}" 
             class="sticker">
        {% endfor %}
    </div>
    
    <!-- Voice-over settings -->
    <div class="voice-settings">
        <label>
            <input type="checkbox" 
                   {% if user.preferences.voiceOverEnabled %}checked{% endif %}>
            Enable Voice Guidance
        </label>
        <input type="range" 
               min="0.5" max="2" step="0.1"
               value="{{ user.preferences.voiceOverSpeed }}">
    </div>
</div>
```

## Database Queries

### Finding Users with Specific Badges

```python
# Find all admin users
admins = db.users.find({
    'badges': {
        '$elemMatch': {
            'type': 'agent',
            'label': 'Admin'
        }
    }
})

# Find advanced practitioners
advanced_users = db.users.find({
    'badges': {
        '$elemMatch': {
            'type': 'skill',
            'label': 'Advanced'
        }
    }
})
```

### Module-Based Leaderboards

```python
# Top users by module accuracy
def get_module_leaderboard(module_type, limit=10):
    pipeline = [
        {'$match': {'module': module_type}},
        {'$group': {
            '_id': '$userId',
            'avgAccuracy': {'$avg': '$sessionStats.totalAccuracy'},
            'totalSessions': {'$sum': 1}
        }},
        {'$sort': {'avgAccuracy': -1}},
        {'$limit': limit},
        {'$lookup': {
            'from': 'users',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'user'
        }},
        {'$unwind': '$user'}
    ]
    
    return list(db.sessions.aggregate(pipeline))

# Usage
leaderboard = get_module_leaderboard('surya_namaskar')
for rank, entry in enumerate(leaderboard, 1):
    user = entry['user']
    print(f"{rank}. {user['profile']['firstName']} - {entry['avgAccuracy']:.1f}%")
```

## API Endpoints Examples

### User Profile Endpoint

```python
@app.route('/api/user/<user_id>')
def get_user_profile(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'uniqueId': user['uniqueId'],
        'email': user['email'],
        'profile': user['profile'],
        'badges': user['badges'],
        'stickers': user['stickers'],
        'preferences': {
            'voiceOverEnabled': user['preferences']['voiceOverEnabled'],
            'voiceOverSpeed': user['preferences']['voiceOverSpeed'],
            'voiceOverVolume': user['preferences']['voiceOverVolume']
        },
        'stats': user['stats']
    })
```

### Module Analytics Endpoint

```python
@app.route('/api/analytics/module/<module_type>')
def get_module_analytics(module_type):
    user_id = ObjectId(session['user_id'])
    
    # Get module-specific stats
    pipeline = [
        {'$match': {
            'userId': user_id,
            'module': module_type
        }},
        {'$group': {
            '_id': None,
            'totalSessions': {'$sum': 1},
            'avgAccuracy': {'$avg': '$sessionStats.totalAccuracy'},
            'totalMinutes': {'$sum': {'$divide': ['$duration', 60]}},
            'bestAccuracy': {'$max': '$sessionStats.totalAccuracy'}
        }}
    ]
    
    result = list(db.sessions.aggregate(pipeline))
    stats = result[0] if result else {
        'totalSessions': 0,
        'avgAccuracy': 0,
        'totalMinutes': 0,
        'bestAccuracy': 0
    }
    
    return jsonify(stats)
```

## Testing

### Unit Test Examples

```python
import unittest
from models import UserModel, SessionModel, DatabaseManager

class TestSchemaEnhancements(unittest.TestCase):
    
    def setUp(self):
        self.db_manager = DatabaseManager('mongodb://localhost:27017/')
        self.user_model = UserModel(self.db_manager)
        self.session_model = SessionModel(self.db_manager)
    
    def test_user_creation_with_unique_id(self):
        """Test that new users get unique IDs"""
        user_id = self.user_model.create_user({
            'email': 'test@example.com',
            'password': 'password123',
            'experienceLevel': 'Beginner'
        })
        
        user = self.db_manager.users.find_one({'_id': user_id})
        
        self.assertIn('uniqueId', user)
        self.assertEqual(len(user['uniqueId']), 8)
        self.assertTrue(user['uniqueId'].isupper())
    
    def test_user_has_default_badges(self):
        """Test that new users get default badges"""
        user_id = self.user_model.create_user({
            'email': 'test2@example.com',
            'password': 'password123',
            'experienceLevel': 'Intermediate'
        })
        
        user = self.db_manager.users.find_one({'_id': user_id})
        
        self.assertIn('badges', user)
        self.assertGreater(len(user['badges']), 0)
        
        # Check for agent badge
        agent_badges = [b for b in user['badges'] if b['type'] == 'agent']
        self.assertEqual(len(agent_badges), 1)
        
        # Check for skill badge
        skill_badges = [b for b in user['badges'] if b['type'] == 'skill']
        self.assertEqual(len(skill_badges), 1)
        self.assertEqual(skill_badges[0]['label'], 'Intermediate')
    
    def test_session_has_module_field(self):
        """Test that sessions include module field"""
        user_id = self.user_model.create_user({
            'email': 'test3@example.com',
            'password': 'password123'
        })
        
        session_id = self.session_model.create_session(
            user_id=user_id,
            module_type='breathing'
        )
        
        session = self.db_manager.sessions.find_one({'_id': session_id})
        
        self.assertIn('module', session)
        self.assertEqual(session['module'], 'breathing')
    
    def test_voice_over_preferences(self):
        """Test voice-over preferences are set"""
        user_id = self.user_model.create_user({
            'email': 'test4@example.com',
            'password': 'password123'
        })
        
        user = self.db_manager.users.find_one({'_id': user_id})
        prefs = user['preferences']
        
        self.assertIn('voiceOverEnabled', prefs)
        self.assertIn('voiceOverSpeed', prefs)
        self.assertIn('voiceOverVolume', prefs)
        
        self.assertTrue(prefs['voiceOverEnabled'])
        self.assertEqual(prefs['voiceOverSpeed'], 1.0)
        self.assertEqual(prefs['voiceOverVolume'], 1.0)

if __name__ == '__main__':
    unittest.main()
```

## Common Patterns

### Award Badge to User

```python
def award_badge(user_id, badge_type, label, color):
    """Award a badge to a user"""
    db.users.update_one(
        {'_id': user_id},
        {
            '$push': {
                'badges': {
                    'type': badge_type,
                    'label': label,
                    'color': color,
                    'earnedAt': datetime.now()
                }
            }
        }
    )
```

### Get User's Module Progress

```python
def get_all_module_progress(user_id):
    """Get progress across all modules"""
    modules = ['surya_namaskar', 'breathing', 'stretching']
    progress = {}
    
    for module in modules:
        stats = db.sessions.aggregate([
            {'$match': {'userId': user_id, 'module': module}},
            {'$group': {
                '_id': None,
                'count': {'$sum': 1},
                'avgAccuracy': {'$avg': '$sessionStats.totalAccuracy'}
            }}
        ])
        
        result = list(stats)
        progress[module] = result[0] if result else {'count': 0, 'avgAccuracy': 0}
    
    return progress
```

## Migration Checklist

- [x] Run migration script
- [x] Verify all users have uniqueId
- [x] Verify all users have badges
- [x] Verify all users have stickers array
- [x] Verify all users have voice-over preferences
- [x] Verify all sessions have module field
- [x] Verify indexes are created
- [ ] Update UI to display unique IDs
- [ ] Update UI to display badges
- [ ] Implement voice-over settings page
- [ ] Update analytics to use module field
- [ ] Test session creation with modules
- [ ] Deploy to production

## Support

For questions or issues with the schema enhancements:
1. Check this guide for examples
2. Review the migration README
3. Run the verification script
4. Contact the development team
