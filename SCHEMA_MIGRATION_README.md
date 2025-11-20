# Database Schema Enhancement Migration

## Overview

This migration script updates the Yogic Guide database schema to support new platform enhancements including:

1. **Unique User IDs** - 8-character alphanumeric identifiers for each user
2. **Badge System** - Visual badges for roles, skills, and achievements
3. **Sticker System** - Decorative achievement stickers
4. **Module Tracking** - Specific module types for session tracking
5. **Voice-Over Preferences** - User preferences for audio guidance

## What Gets Updated

### Users Collection

#### New Fields Added:
- `uniqueId` (String) - Unique 8-character ID (e.g., "A3F7B2C9")
- `badges` (Array) - Collection of earned badges
  ```javascript
  {
    type: 'agent' | 'skill' | 'process',
    label: String,
    color: String,
    level: Number (optional),
    earnedAt: DateTime
  }
  ```
- `stickers` (Array) - Array of earned sticker identifiers
- `preferences.voiceOverEnabled` (Boolean) - Enable/disable voice guidance
- `preferences.voiceOverSpeed` (Number) - Speech speed (0.5-2.0)
- `preferences.voiceOverVolume` (Number) - Speech volume (0-1.0)

#### Default Values:
- **Admin users** get "Admin" agent badge (purple)
- **Regular users** get "User" agent badge (green)
- **Skill badges** assigned based on experience level:
  - Beginner: Blue (#4299e1)
  - Intermediate: Orange (#ed8936)
  - Advanced: Purple (#9f7aea)
- **Voice-over** enabled by default with speed 1.0 and volume 1.0

### Sessions Collection

#### New Fields Added:
- `module` (String) - Module type identifier
  - `surya_namaskar` - Sun Salutation sequences
  - `breathing` - Pranayama exercises
  - `stretching` - Flexibility routines
  - `meditation` - Mindfulness sessions
  - `custom` - User-created routines

#### Migration Logic:
- Existing sessions analyzed by `moduleName` field
- Module type inferred from name keywords
- Unknown sessions default to `surya_namaskar`

### Database Indexes

#### New Indexes Created:
1. `users.uniqueId` - Unique index for user IDs
2. `users.badges.type` - Index for badge queries
3. `sessions.module` - Index for module filtering
4. `sessions.module + sessions.userId` - Compound index for user-module queries

## Running the Migration

### Prerequisites

1. Python 3.7 or higher
2. MongoDB connection (local or Atlas)
3. Required packages: `pymongo`, `python-dotenv`

### Environment Setup

Set your MongoDB connection string:

```bash
# For MongoDB Atlas
export MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/"

# For local MongoDB
export MONGO_URI="mongodb://localhost:27017/"
```

Or create a `.env` file:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### Execute Migration

```bash
# Make script executable (Unix/Linux/Mac)
chmod +x migrate_schema_enhancements.py

# Run migration
python migrate_schema_enhancements.py
```

### Expected Output

```
============================================================
Database Schema Enhancement Migration
============================================================
✅ Connected to MongoDB Atlas

📋 Migrating users collection...
   ✓ Generated uniqueId for user john@example.com: A3F7B2C9
   ✓ Added default badges for user john@example.com
   ✓ Added stickers array for user john@example.com
   ✓ Added voice-over preferences for user john@example.com
   ...

   ✅ Users migration complete: 15 updated, 0 skipped

📋 Migrating sessions collection...
   ✓ Added module 'surya_namaskar' to session 507f1f77bcf86cd799439011
   ✓ Added module 'breathing' to session 507f1f77bcf86cd799439012
   ...

   ✅ Sessions migration complete: 42 updated, 0 skipped

📋 Creating database indexes...
   ✓ Created unique index on users.uniqueId
   ✓ Created unique index on users.email
   ✓ Created index on users.badges.type
   ✓ Created compound index on sessions.userId and sessions.startTime
   ✓ Created index on sessions.module
   ✓ Created compound index on sessions.module and sessions.userId

   ✅ All indexes created successfully

📋 Verifying migration...

   Users Collection:
   - Total users: 15
   - Users with uniqueId: 15
   - Users with badges: 15
   - Users with stickers: 15
   - Users with voice-over preferences: 15

   Sessions Collection:
   - Total sessions: 42
   - Sessions with module field: 42

   Indexes:
   - User indexes: 6
   - Session indexes: 4

   ✅ All users migrated successfully!
   ✅ All sessions migrated successfully!

============================================================
✅ Migration completed successfully!
============================================================
```

## Safety Features

### Non-Destructive
- Only adds new fields, never removes existing data
- Skips users/sessions that already have new fields
- Uses `$set` operations to preserve existing data

### Idempotent
- Safe to run multiple times
- Checks for existing fields before updating
- Won't duplicate data on re-runs

### Unique ID Generation
- Generates truly unique 8-character IDs
- Checks database for collisions before assigning
- Uses UUID4 for randomness

## Verification

After migration, verify the changes:

```python
# Connect to MongoDB
from pymongo import MongoClient
client = MongoClient('your_mongo_uri')
db = client.yogic_guide

# Check a user
user = db.users.find_one({'email': 'test@example.com'})
print(f"Unique ID: {user['uniqueId']}")
print(f"Badges: {user['badges']}")
print(f"Voice-over enabled: {user['preferences']['voiceOverEnabled']}")

# Check a session
session = db.sessions.find_one()
print(f"Module: {session['module']}")
```

## Rollback (If Needed)

If you need to rollback the migration:

```python
# Remove new fields from users
db.users.update_many(
    {},
    {
        '$unset': {
            'uniqueId': '',
            'badges': '',
            'stickers': '',
            'preferences.voiceOverEnabled': '',
            'preferences.voiceOverSpeed': '',
            'preferences.voiceOverVolume': ''
        }
    }
)

# Remove module field from sessions
db.sessions.update_many(
    {},
    {'$unset': {'module': ''}}
)

# Drop indexes
db.users.drop_index('uniqueId_1')
db.users.drop_index('badges.type_1')
db.sessions.drop_index('module_1')
db.sessions.drop_index('module_1_userId_1')
```

## Troubleshooting

### Connection Issues
```
❌ Failed to connect to MongoDB: ...
```
**Solution**: Check your `MONGO_URI` environment variable and network connection.

### Duplicate Key Errors
```
E11000 duplicate key error collection: yogic_guide.users index: uniqueId_1
```
**Solution**: This shouldn't happen due to collision checking, but if it does, the script will generate a new ID.

### Missing Fields
```
⚠️  Some users may not have all new fields
```
**Solution**: Re-run the migration script. It's safe to run multiple times.

## Integration with Application

After migration, update your application code:

### User Registration
```python
# models.py already updated to include new fields
user_id = user_model.create_user({
    'email': 'user@example.com',
    'password': 'hashed_password',
    'experienceLevel': 'Beginner',
    'role': 'user'
})
```

### Session Creation
```python
# Specify module type when creating sessions
session_id = session_model.create_session(
    user_id=user_id,
    module_type='surya_namaskar'
)
```

### Querying by Module
```python
# Get all breathing sessions for a user
sessions = db.sessions.find({
    'userId': user_id,
    'module': 'breathing'
})
```

### Displaying Badges
```python
# In templates
{% for badge in user.badges %}
    <span class="badge badge-{{ badge.type }}" style="background: {{ badge.color }}">
        {{ badge.label }}
    </span>
{% endfor %}
```

## Next Steps

After successful migration:

1. ✅ Test user registration with new fields
2. ✅ Test session creation with module types
3. ✅ Implement badge display in UI
4. ✅ Add voice-over settings page
5. ✅ Update analytics to use module field
6. ✅ Deploy to production

## Support

For issues or questions:
- Check the migration output for specific errors
- Review the verification section
- Ensure MongoDB connection is stable
- Contact development team if problems persist
