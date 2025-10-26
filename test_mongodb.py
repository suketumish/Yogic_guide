#!/usr/bin/env python3
"""
Test MongoDB Atlas Connection
"""

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test MongoDB Atlas connection"""
    try:
        mongo_uri = os.getenv('MONGO_URI')
        
        if not mongo_uri:
            print("❌ MONGO_URI not found in .env file")
            return False
        
        print(f"🔗 Connecting to MongoDB Atlas...")
        print(f"📍 URI: {mongo_uri[:50]}...")
        
        # Create client
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB Atlas connection successful!")
        
        # Get database
        db = client.yogic_guide
        print(f"📊 Database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📁 Collections: {collections if collections else 'No collections yet'}")
        
        # Count users
        user_count = db.users.count_documents({})
        print(f"👥 Total users: {user_count}")
        
        # Test insert (optional)
        print("\n🧪 Testing insert operation...")
        test_doc = {
            'test': True,
            'message': 'Connection test',
            'timestamp': 'test'
        }
        
        result = db.test_collection.insert_one(test_doc)
        print(f"✅ Test insert successful! ID: {result.inserted_id}")
        
        # Clean up test
        db.test_collection.delete_one({'_id': result.inserted_id})
        print("🧹 Test document cleaned up")
        
        print("\n✅ All tests passed! MongoDB Atlas is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MongoDB Atlas Connection Test")
    print("=" * 60)
    test_connection()
