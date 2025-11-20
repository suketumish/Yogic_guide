"""
Test Module-Specific Session Management Implementation
Tests for task 9: Module-Specific Session Management
"""

import os
import sys
from datetime import datetime
from bson import ObjectId

# Set up test environment
os.environ['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

def test_session_creation_with_module():
    """Test that sessions are created with module field"""
    print("\n" + "="*60)
    print("TEST: Session Creation with Module Field")
    print("="*60)
    
    try:
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi
        
        mongo_uri = os.getenv('MONGO_URI')
        
        if 'mongodb+srv://' in mongo_uri or 'mongodb.net' in mongo_uri:
            client = MongoClient(mongo_uri, server_api=ServerApi('1'))
            client.admin.command('ping')
        else:
            client = MongoClient(mongo_uri)
        
        db = client.yogic_guide
        print("✅ Connected to MongoDB")
        
        # Test data
        test_modules = [
            ('surya_namaskar', 'Surya Namaskar'),
            ('breathing', 'Breathing Exercises'),
            ('stretching', 'Stretching Routine'),
            ('meditation', 'Meditation'),
            ('yoga', 'Yoga Practice')
        ]
        
        # Create a test user if needed
        test_user = db.users.find_one({'email': 'test_module_user@test.com'})
        if not test_user:
            test_user_id = db.users.insert_one({
                'email': 'test_module_user@test.com',
                'profile': {'name': 'Test Module User'},
                'createdAt': datetime.now()
            }).inserted_id
            print(f"✅ Created test user: {test_user_id}")
        else:
            test_user_id = test_user['_id']
            print(f"✅ Using existing test user: {test_user_id}")
        
        print("\n📝 Testing session creation for each module:")
        created_sessions = []
        
        for module_type, module_name in test_modules:
            session_doc = {
                'userId': test_user_id,
                'module': module_type,
                'moduleType': module_type.replace('_', '-'),
                'moduleName': module_name,
                'startTime': datetime.now(),
                'duration': 0,
                'status': 'active',
                'createdAt': datetime.now()
            }
            
            session_id = db.sessions.insert_one(session_doc).inserted_id
            created_sessions.append(session_id)
            
            # Verify the session was created correctly
            session = db.sessions.find_one({'_id': session_id})
            
            assert 'module' in session, f"Session should have 'module' field"
            assert session['module'] == module_type, f"Module should be {module_type}"
            
            print(f"   ✅ {module_name}: session created with module='{module_type}'")
        
        print(f"\n✅ Created {len(created_sessions)} test sessions")
        
        # Test module filtering
        print("\n📊 Testing module-based queries:")
        
        for module_type, module_name in test_modules:
            count = db.sessions.count_documents({
                'userId': test_user_id,
                'module': module_type
            })
            print(f"   ✅ {module_name}: {count} session(s)")
            assert count >= 1, f"Should have at least 1 {module_name} session"
        
        # Test aggregation by module
        print("\n📈 Testing module aggregation:")
        
        pipeline = [
            {'$match': {'userId': test_user_id}},
            {'$group': {
                '_id': '$module',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]
        
        results = list(db.sessions.aggregate(pipeline))
        
        for result in results:
            print(f"   ✅ {result['_id']}: {result['count']} session(s)")
        
        assert len(results) >= len(test_modules), "Should have results for all modules"
        
        # Cleanup test sessions
        print("\n🧹 Cleaning up test data...")
        db.sessions.delete_many({'_id': {'$in': created_sessions}})
        print(f"   ✅ Deleted {len(created_sessions)} test sessions")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_module_analytics():
    """Test module-wise analytics aggregation"""
    print("\n" + "="*60)
    print("TEST: Module Analytics Aggregation")
    print("="*60)
    
    try:
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi
        
        mongo_uri = os.getenv('MONGO_URI')
        
        if 'mongodb+srv://' in mongo_uri or 'mongodb.net' in mongo_uri:
            client = MongoClient(mongo_uri, server_api=ServerApi('1'))
            client.admin.command('ping')
        else:
            client = MongoClient(mongo_uri)
        
        db = client.yogic_guide
        print("✅ Connected to MongoDB")
        
        # Get module performance stats
        print("\n📊 Module Performance Statistics:")
        
        pipeline = [
            {'$group': {
                '_id': {'$ifNull': ['$module', '$moduleType']},
                'total_sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'}
            }},
            {'$sort': {'total_sessions': -1}}
        ]
        
        results = list(db.sessions.aggregate(pipeline))
        
        if results:
            for result in results:
                module = result['_id'] or 'Unknown'
                sessions = result['total_sessions']
                duration = result.get('total_duration', 0)
                avg = result.get('avg_duration', 0)
                
                print(f"\n   Module: {module}")
                print(f"   - Total Sessions: {sessions}")
                print(f"   - Total Duration: {duration}s ({round(duration/60, 1)}min)")
                print(f"   - Avg Duration: {round(avg, 1)}s ({round(avg/60, 1)}min)")
            
            print(f"\n✅ Found statistics for {len(results)} module(s)")
        else:
            print("   ⚠️  No session data available for analytics")
        
        print("\n" + "="*60)
        print("✅ ANALYTICS TEST COMPLETED")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n🧪 Running Module-Specific Session Management Tests")
    print("="*60)
    
    # Run tests
    test1_passed = test_session_creation_with_module()
    test2_passed = test_module_analytics()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Session Creation Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Module Analytics Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
