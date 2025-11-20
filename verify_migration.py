#!/usr/bin/env python3
"""
Verification script to check migration results
"""

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

def connect_to_database():
    """Connect to MongoDB database"""
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    
    try:
        if 'mongodb+srv://' in mongo_uri or 'mongodb.net' in mongo_uri:
            client = MongoClient(mongo_uri, server_api=ServerApi('1'))
            client.admin.command('ping')
            print("✅ Connected to MongoDB Atlas")
        else:
            client = MongoClient(mongo_uri)
            print("✅ Connected to local MongoDB")
        
        return client.yogic_guide
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return None

def verify_user_schema(db):
    """Verify user schema enhancements"""
    print("\n" + "="*60)
    print("USER SCHEMA VERIFICATION")
    print("="*60)
    
    # Get a sample user
    user = db.users.find_one()
    
    if not user:
        print("❌ No users found in database")
        return
    
    print(f"\n📋 Sample User: {user.get('email', 'Unknown')}")
    print("-" * 60)
    
    # Check uniqueId
    if 'uniqueId' in user:
        print(f"✅ uniqueId: {user['uniqueId']}")
    else:
        print("❌ uniqueId: MISSING")
    
    # Check badges
    if 'badges' in user:
        print(f"✅ badges: {len(user['badges'])} badge(s)")
        for badge in user['badges']:
            print(f"   - {badge.get('type', 'unknown')}: {badge.get('label', 'unknown')} ({badge.get('color', 'no color')})")
    else:
        print("❌ badges: MISSING")
    
    # Check stickers
    if 'stickers' in user:
        print(f"✅ stickers: {len(user['stickers'])} sticker(s)")
    else:
        print("❌ stickers: MISSING")
    
    # Check voice-over preferences
    preferences = user.get('preferences', {})
    if 'voiceOverEnabled' in preferences:
        print(f"✅ voiceOverEnabled: {preferences['voiceOverEnabled']}")
        print(f"✅ voiceOverSpeed: {preferences.get('voiceOverSpeed', 'N/A')}")
        print(f"✅ voiceOverVolume: {preferences.get('voiceOverVolume', 'N/A')}")
    else:
        print("❌ Voice-over preferences: MISSING")
    
    # Show full user document structure
    print("\n📄 Full User Document Structure:")
    print("-" * 60)
    print_dict_structure(user, indent=0)

def verify_session_schema(db):
    """Verify session schema enhancements"""
    print("\n" + "="*60)
    print("SESSION SCHEMA VERIFICATION")
    print("="*60)
    
    # Get a sample session
    session = db.sessions.find_one()
    
    if not session:
        print("❌ No sessions found in database")
        return
    
    print(f"\n📋 Sample Session: {session.get('_id', 'Unknown')}")
    print("-" * 60)
    
    # Check module field
    if 'module' in session:
        print(f"✅ module: {session['module']}")
    else:
        print("❌ module: MISSING")
    
    # Check moduleName
    if 'moduleName' in session:
        print(f"✅ moduleName: {session['moduleName']}")
    else:
        print("⚠️  moduleName: Not present (optional)")
    
    # Show module distribution
    print("\n📊 Module Distribution:")
    print("-" * 60)
    pipeline = [
        {'$group': {
            '_id': '$module',
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}}
    ]
    
    module_stats = list(db.sessions.aggregate(pipeline))
    for stat in module_stats:
        print(f"   {stat['_id']}: {stat['count']} session(s)")
    
    # Show full session document structure
    print("\n📄 Full Session Document Structure:")
    print("-" * 60)
    print_dict_structure(session, indent=0)

def verify_indexes(db):
    """Verify database indexes"""
    print("\n" + "="*60)
    print("INDEX VERIFICATION")
    print("="*60)
    
    # User indexes
    print("\n📋 Users Collection Indexes:")
    print("-" * 60)
    user_indexes = db.users.index_information()
    for index_name, index_info in user_indexes.items():
        keys = index_info.get('key', [])
        unique = index_info.get('unique', False)
        sparse = index_info.get('sparse', False)
        
        key_str = ', '.join([f"{k[0]}: {k[1]}" for k in keys])
        flags = []
        if unique:
            flags.append('unique')
        if sparse:
            flags.append('sparse')
        
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        print(f"   ✅ {index_name}: {key_str}{flag_str}")
    
    # Session indexes
    print("\n📋 Sessions Collection Indexes:")
    print("-" * 60)
    session_indexes = db.sessions.index_information()
    for index_name, index_info in session_indexes.items():
        keys = index_info.get('key', [])
        key_str = ', '.join([f"{k[0]}: {k[1]}" for k in keys])
        print(f"   ✅ {index_name}: {key_str}")

def print_dict_structure(d, indent=0, max_depth=3):
    """Print dictionary structure in a readable format"""
    if indent > max_depth:
        return
    
    for key, value in d.items():
        if isinstance(value, dict):
            print("   " * indent + f"├─ {key}: {{")
            print_dict_structure(value, indent + 1, max_depth)
            print("   " * indent + "   }")
        elif isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                print("   " * indent + f"├─ {key}: [{len(value)} items]")
                if len(value) > 0:
                    print("   " * indent + "   └─ Sample item:")
                    print_dict_structure(value[0], indent + 2, max_depth)
            else:
                print("   " * indent + f"├─ {key}: [{len(value)} items] {value[:3] if len(value) <= 3 else value[:3] + ['...']}")
        elif isinstance(value, ObjectId):
            print("   " * indent + f"├─ {key}: ObjectId({str(value)[:8]}...)")
        else:
            value_str = str(value)
            if len(value_str) > 50:
                value_str = value_str[:50] + "..."
            print("   " * indent + f"├─ {key}: {value_str}")

def main():
    """Main verification function"""
    print("="*60)
    print("DATABASE SCHEMA MIGRATION VERIFICATION")
    print("="*60)
    
    db = connect_to_database()
    if db is None:
        return
    
    verify_user_schema(db)
    verify_session_schema(db)
    verify_indexes(db)
    
    print("\n" + "="*60)
    print("✅ VERIFICATION COMPLETE")
    print("="*60)

if __name__ == '__main__':
    main()
