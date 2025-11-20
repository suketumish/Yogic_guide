#!/usr/bin/env python3
"""
Test script for database schema enhancements
Verifies that the new fields work correctly in the models
"""

import os
import sys
from datetime import datetime
from bson import ObjectId

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import DatabaseManager, UserModel, SessionModel

def test_user_creation():
    """Test creating a user with new schema fields"""
    print("\n" + "="*60)
    print("TEST: User Creation with Enhanced Schema")
    print("="*60)
    
    try:
        # Initialize database
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_manager = DatabaseManager(mongo_uri)
        user_model = UserModel(db_manager)
        
        # Create test user
        test_email = f"test_user_{datetime.now().timestamp()}@example.com"
        
        print(f"\n📝 Creating test user: {test_email}")
        
        user_id = user_model.create_user({
            'email': test_email,
            'password': 'test_password_123',
            'firstName': 'Test',
            'lastName': 'User',
            'experienceLevel': 'Intermediate',
            'role': 'user'
        })
        
        print(f"✅ User created with ID: {user_id}")
        
        # Retrieve and verify user
        user = db_manager.users.find_one({'_id': user_id})
        
        # Check uniqueId
        if 'uniqueId' in user:
            print(f"✅ uniqueId: {user['uniqueId']} (length: {len(user['uniqueId'])})")
            assert len(user['uniqueId']) == 8, "uniqueId should be 8 characters"
            assert user['uniqueId'].isupper(), "uniqueId should be uppercase"
        else:
            print("❌ uniqueId: MISSING")
            return False
        
        # Check badges
        if 'badges' in user and len(user['badges']) > 0:
            print(f"✅ badges: {len(user['badges'])} badge(s)")
            for badge in user['badges']:
                print(f"   - {badge['type']}: {badge['label']} ({badge['color']})")
                assert 'type' in badge, "Badge should have type"
                assert 'label' in badge, "Badge should have label"
                assert 'color' in badge, "Badge should have color"
                assert 'earnedAt' in badge, "Badge should have earnedAt"
        else:
            print("❌ badges: MISSING or EMPTY")
            return False
        
        # Check stickers
        if 'stickers' in user:
            print(f"✅ stickers: {len(user['stickers'])} sticker(s)")
            assert isinstance(user['stickers'], list), "Stickers should be a list"
        else:
            print("❌ stickers: MISSING")
            return False
        
        # Check voice-over preferences
        prefs = user.get('preferences', {})
        if all(key in prefs for key in ['voiceOverEnabled', 'voiceOverSpeed', 'voiceOverVolume']):
            print(f"✅ voiceOverEnabled: {prefs['voiceOverEnabled']}")
            print(f"✅ voiceOverSpeed: {prefs['voiceOverSpeed']}")
            print(f"✅ voiceOverVolume: {prefs['voiceOverVolume']}")
            assert isinstance(prefs['voiceOverEnabled'], bool), "voiceOverEnabled should be boolean"
            assert 0.5 <= prefs['voiceOverSpeed'] <= 2.0, "voiceOverSpeed should be between 0.5 and 2.0"
            assert 0.0 <= prefs['voiceOverVolume'] <= 1.0, "voiceOverVolume should be between 0.0 and 1.0"
        else:
            print("❌ Voice-over preferences: INCOMPLETE")
            return False
        
        # Clean up test user
        db_manager.users.delete_one({'_id': user_id})
        print(f"\n🧹 Cleaned up test user")
        
        print("\n✅ User creation test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ User creation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_creation():
    """Test creating a session with module field"""
    print("\n" + "="*60)
    print("TEST: Session Creation with Module Field")
    print("="*60)
    
    try:
        # Initialize database
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_manager = DatabaseManager(mongo_uri)
        user_model = UserModel(db_manager)
        session_model = SessionModel(db_manager)
        
        # Create test user
        test_email = f"test_session_user_{datetime.now().timestamp()}@example.com"
        user_id = user_model.create_user({
            'email': test_email,
            'password': 'test_password_123',
            'firstName': 'Session',
            'lastName': 'Test'
        })
        
        print(f"\n📝 Creating test session for user: {user_id}")
        
        # Test different module types
        module_types = ['surya_namaskar', 'breathing', 'stretching']
        
        for module_type in module_types:
            print(f"\n   Testing module: {module_type}")
            
            session_id = session_model.create_session(
                user_id=user_id,
                module_type=module_type
            )
            
            print(f"   ✅ Session created with ID: {session_id}")
            
            # Retrieve and verify session
            session = db_manager.sessions.find_one({'_id': session_id})
            
            # Check module field
            if 'module' in session:
                print(f"   ✅ module: {session['module']}")
                assert session['module'] == module_type, f"Module should be {module_type}"
            else:
                print(f"   ❌ module: MISSING")
                return False
            
            # Check moduleName
            if 'moduleName' in session:
                print(f"   ✅ moduleName: {session['moduleName']}")
            else:
                print(f"   ⚠️  moduleName: Not present (optional)")
            
            # Clean up test session
            db_manager.sessions.delete_one({'_id': session_id})
        
        # Clean up test user
        db_manager.users.delete_one({'_id': user_id})
        print(f"\n🧹 Cleaned up test user and sessions")
        
        print("\n✅ Session creation test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Session creation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_badge_operations():
    """Test badge operations"""
    print("\n" + "="*60)
    print("TEST: Badge Operations")
    print("="*60)
    
    try:
        # Initialize database
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_manager = DatabaseManager(mongo_uri)
        user_model = UserModel(db_manager)
        
        # Create test user
        test_email = f"test_badge_user_{datetime.now().timestamp()}@example.com"
        user_id = user_model.create_user({
            'email': test_email,
            'password': 'test_password_123',
            'experienceLevel': 'Advanced',
            'role': 'admin'
        })
        
        print(f"\n📝 Testing badge operations for user: {user_id}")
        
        # Verify default badges
        user = db_manager.users.find_one({'_id': user_id})
        print(f"\n   Default badges: {len(user['badges'])}")
        
        # Add a new badge
        print(f"\n   Adding achievement badge...")
        db_manager.users.update_one(
            {'_id': user_id},
            {
                '$push': {
                    'badges': {
                        'type': 'process',
                        'label': '100 Sessions',
                        'color': '#38b2ac',
                        'earnedAt': datetime.now()
                    }
                }
            }
        )
        
        # Verify badge was added
        user = db_manager.users.find_one({'_id': user_id})
        print(f"   ✅ Total badges after addition: {len(user['badges'])}")
        
        # Find badge by type
        process_badges = [b for b in user['badges'] if b['type'] == 'process']
        assert len(process_badges) == 1, "Should have one process badge"
        print(f"   ✅ Process badge found: {process_badges[0]['label']}")
        
        # Query users by badge type
        users_with_process_badges = db_manager.users.count_documents({
            'badges': {
                '$elemMatch': {
                    'type': 'process'
                }
            }
        })
        print(f"   ✅ Users with process badges: {users_with_process_badges}")
        
        # Clean up
        db_manager.users.delete_one({'_id': user_id})
        print(f"\n🧹 Cleaned up test user")
        
        print("\n✅ Badge operations test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Badge operations test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_module_queries():
    """Test module-based queries"""
    print("\n" + "="*60)
    print("TEST: Module-Based Queries")
    print("="*60)
    
    try:
        # Initialize database
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_manager = DatabaseManager(mongo_uri)
        user_model = UserModel(db_manager)
        session_model = SessionModel(db_manager)
        
        # Create test user
        test_email = f"test_module_user_{datetime.now().timestamp()}@example.com"
        user_id = user_model.create_user({
            'email': test_email,
            'password': 'test_password_123'
        })
        
        print(f"\n📝 Creating test sessions for module queries")
        
        # Create sessions for different modules
        modules = {
            'surya_namaskar': 3,
            'breathing': 2,
            'stretching': 1
        }
        
        session_ids = []
        for module_type, count in modules.items():
            for i in range(count):
                session_id = session_model.create_session(
                    user_id=user_id,
                    module_type=module_type
                )
                session_ids.append(session_id)
        
        print(f"   ✅ Created {len(session_ids)} test sessions")
        
        # Query sessions by module
        for module_type, expected_count in modules.items():
            count = db_manager.sessions.count_documents({
                'userId': user_id,
                'module': module_type
            })
            print(f"   ✅ {module_type}: {count} sessions (expected: {expected_count})")
            assert count == expected_count, f"Should have {expected_count} {module_type} sessions"
        
        # Test aggregation by module
        print(f"\n   Testing module aggregation...")
        pipeline = [
            {'$match': {'userId': user_id}},
            {'$group': {
                '_id': '$module',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]
        
        results = list(db_manager.sessions.aggregate(pipeline))
        print(f"   ✅ Aggregation results:")
        for result in results:
            print(f"      - {result['_id']}: {result['count']} sessions")
        
        # Clean up
        for session_id in session_ids:
            db_manager.sessions.delete_one({'_id': session_id})
        db_manager.users.delete_one({'_id': user_id})
        print(f"\n🧹 Cleaned up test data")
        
        print("\n✅ Module queries test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Module queries test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("DATABASE SCHEMA ENHANCEMENTS - TEST SUITE")
    print("="*60)
    
    tests = [
        ("User Creation", test_user_creation),
        ("Session Creation", test_session_creation),
        ("Badge Operations", test_badge_operations),
        ("Module Queries", test_module_queries)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests PASSED! Schema enhancements are working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) FAILED. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
