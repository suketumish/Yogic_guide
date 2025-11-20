#!/usr/bin/env python3
"""
Database Schema Migration Script
Adds enhancements for platform improvements:
- Unique user IDs
- Badges and stickers
- Module field for sessions
- Voice-over preferences
"""

import os
import sys
import uuid
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from pymongo.server_api import ServerApi
from bson import ObjectId

def generate_unique_user_id():
    """Generate an 8-character unique user ID"""
    return str(uuid.uuid4())[:8].upper()

def connect_to_database():
    """Connect to MongoDB database"""
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    
    try:
        if 'mongodb+srv://' in mongo_uri or 'mongodb.net' in mongo_uri:
            # MongoDB Atlas connection
            client = MongoClient(mongo_uri, server_api=ServerApi('1'))
            client.admin.command('ping')
            print("✅ Connected to MongoDB Atlas")
        else:
            # Local MongoDB connection
            client = MongoClient(mongo_uri)
            print("✅ Connected to local MongoDB")
        
        return client.yogic_guide
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        sys.exit(1)

def migrate_users_collection(db):
    """Migrate users collection with new fields"""
    print("\n📋 Migrating users collection...")
    
    users_collection = db.users
    users = list(users_collection.find({}))
    
    if not users:
        print("   ℹ️  No users found to migrate")
        return
    
    updated_count = 0
    skipped_count = 0
    
    for user in users:
        user_id = user['_id']
        updates = {}
        
        # Add unique user ID if not present
        if 'uniqueId' not in user:
            # Generate unique ID and ensure it's unique
            while True:
                unique_id = generate_unique_user_id()
                existing = users_collection.find_one({'uniqueId': unique_id})
                if not existing:
                    break
            updates['uniqueId'] = unique_id
            print(f"   ✓ Generated uniqueId for user {user.get('email', 'unknown')}: {unique_id}")
        
        # Add badges array if not present
        if 'badges' not in user:
            # Assign default badge based on user role or status
            default_badges = []
            
            # Add role-based badge
            if user.get('role') == 'admin':
                default_badges.append({
                    'type': 'agent',
                    'label': 'Admin',
                    'color': '#667eea',
                    'earnedAt': user.get('createdAt', datetime.now())
                })
            else:
                default_badges.append({
                    'type': 'agent',
                    'label': 'User',
                    'color': '#48bb78',
                    'earnedAt': user.get('createdAt', datetime.now())
                })
            
            # Add skill badge based on experience level
            experience_level = user.get('preferences', {}).get('experienceLevel', 'Beginner')
            skill_colors = {
                'Beginner': '#4299e1',
                'Intermediate': '#ed8936',
                'Advanced': '#9f7aea'
            }
            default_badges.append({
                'type': 'skill',
                'label': experience_level,
                'color': skill_colors.get(experience_level, '#4299e1'),
                'level': 1 if experience_level == 'Beginner' else 2 if experience_level == 'Intermediate' else 3,
                'earnedAt': user.get('createdAt', datetime.now())
            })
            
            updates['badges'] = default_badges
            print(f"   ✓ Added default badges for user {user.get('email', 'unknown')}")
        
        # Add stickers array if not present
        if 'stickers' not in user:
            # Start with empty stickers array - users can earn these
            updates['stickers'] = []
            print(f"   ✓ Added stickers array for user {user.get('email', 'unknown')}")
        
        # Add voice-over preferences if not present
        if 'preferences' in user:
            preferences = user['preferences']
            if 'voiceOverEnabled' not in preferences:
                updates['preferences.voiceOverEnabled'] = True
                updates['preferences.voiceOverSpeed'] = 1.0
                updates['preferences.voiceOverVolume'] = 1.0
                print(f"   ✓ Added voice-over preferences for user {user.get('email', 'unknown')}")
        else:
            # Create preferences object with voice-over settings
            updates['preferences'] = {
                'experienceLevel': 'Beginner',
                'language': 'English',
                'voice': 'default',
                'theme': 'light',
                'voiceOverEnabled': True,
                'voiceOverSpeed': 1.0,
                'voiceOverVolume': 1.0,
                'notifications': {
                    'push': True,
                    'email': True,
                    'frequency': 'daily'
                }
            }
            print(f"   ✓ Created preferences with voice-over for user {user.get('email', 'unknown')}")
        
        # Update timestamp
        updates['updatedAt'] = datetime.now()
        
        # Apply updates if any
        if updates:
            users_collection.update_one(
                {'_id': user_id},
                {'$set': updates}
            )
            updated_count += 1
        else:
            skipped_count += 1
    
    print(f"\n   ✅ Users migration complete: {updated_count} updated, {skipped_count} skipped")

def migrate_sessions_collection(db):
    """Migrate sessions collection with module field"""
    print("\n📋 Migrating sessions collection...")
    
    sessions_collection = db.sessions
    sessions = list(sessions_collection.find({}))
    
    if not sessions:
        print("   ℹ️  No sessions found to migrate")
        return
    
    updated_count = 0
    skipped_count = 0
    
    for session in sessions:
        session_id = session['_id']
        updates = {}
        
        # Add module field if not present
        if 'module' not in session:
            # Try to infer module from moduleName or set default
            module_name = session.get('moduleName', '').lower()
            
            if 'surya' in module_name or 'sun' in module_name:
                module_type = 'surya_namaskar'
            elif 'breath' in module_name or 'pranayama' in module_name:
                module_type = 'breathing'
            elif 'stretch' in module_name:
                module_type = 'stretching'
            else:
                # Default to surya_namaskar for unknown
                module_type = 'surya_namaskar'
            
            updates['module'] = module_type
            print(f"   ✓ Added module '{module_type}' to session {session_id}")
        
        # Apply updates if any
        if updates:
            sessions_collection.update_one(
                {'_id': session_id},
                {'$set': updates}
            )
            updated_count += 1
        else:
            skipped_count += 1
    
    print(f"\n   ✅ Sessions migration complete: {updated_count} updated, {skipped_count} skipped")

def create_indexes(db):
    """Create necessary database indexes"""
    print("\n📋 Creating database indexes...")
    
    try:
        # User indexes
        db.users.create_index("uniqueId", unique=True, sparse=True)
        print("   ✓ Created unique index on users.uniqueId")
        
        db.users.create_index("email", unique=True)
        print("   ✓ Created unique index on users.email")
        
        db.users.create_index([("badges.type", ASCENDING)])
        print("   ✓ Created index on users.badges.type")
        
        # Session indexes
        db.sessions.create_index([("userId", ASCENDING), ("startTime", -1)])
        print("   ✓ Created compound index on sessions.userId and sessions.startTime")
        
        db.sessions.create_index([("module", ASCENDING)])
        print("   ✓ Created index on sessions.module")
        
        db.sessions.create_index([("module", ASCENDING), ("userId", ASCENDING)])
        print("   ✓ Created compound index on sessions.module and sessions.userId")
        
        print("\n   ✅ All indexes created successfully")
    except Exception as e:
        print(f"   ⚠️  Warning: Some indexes may already exist: {e}")

def verify_migration(db):
    """Verify that migration was successful"""
    print("\n📋 Verifying migration...")
    
    # Check users
    users_with_unique_id = db.users.count_documents({'uniqueId': {'$exists': True}})
    users_with_badges = db.users.count_documents({'badges': {'$exists': True}})
    users_with_stickers = db.users.count_documents({'stickers': {'$exists': True}})
    users_with_voice_prefs = db.users.count_documents({'preferences.voiceOverEnabled': {'$exists': True}})
    total_users = db.users.count_documents({})
    
    print(f"\n   Users Collection:")
    print(f"   - Total users: {total_users}")
    print(f"   - Users with uniqueId: {users_with_unique_id}")
    print(f"   - Users with badges: {users_with_badges}")
    print(f"   - Users with stickers: {users_with_stickers}")
    print(f"   - Users with voice-over preferences: {users_with_voice_prefs}")
    
    # Check sessions
    sessions_with_module = db.sessions.count_documents({'module': {'$exists': True}})
    total_sessions = db.sessions.count_documents({})
    
    print(f"\n   Sessions Collection:")
    print(f"   - Total sessions: {total_sessions}")
    print(f"   - Sessions with module field: {sessions_with_module}")
    
    # Check indexes
    user_indexes = db.users.index_information()
    session_indexes = db.sessions.index_information()
    
    print(f"\n   Indexes:")
    print(f"   - User indexes: {len(user_indexes)}")
    print(f"   - Session indexes: {len(session_indexes)}")
    
    # Verify success
    if total_users > 0:
        if (users_with_unique_id == total_users and 
            users_with_badges == total_users and 
            users_with_stickers == total_users and
            users_with_voice_prefs == total_users):
            print("\n   ✅ All users migrated successfully!")
        else:
            print("\n   ⚠️  Some users may not have all new fields")
    
    if total_sessions > 0:
        if sessions_with_module == total_sessions:
            print("   ✅ All sessions migrated successfully!")
        else:
            print("   ⚠️  Some sessions may not have module field")

def main():
    """Main migration function"""
    print("=" * 60)
    print("Database Schema Enhancement Migration")
    print("=" * 60)
    
    # Connect to database
    db = connect_to_database()
    
    # Run migrations
    migrate_users_collection(db)
    migrate_sessions_collection(db)
    create_indexes(db)
    
    # Verify migration
    verify_migration(db)
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
