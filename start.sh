#!/bin/bash

echo "========================================"
echo "  AI-Powered Yogic Guide"
echo "========================================"
echo ""

# Check if MongoDB is running
echo "Checking MongoDB..."
if ! pgrep -x "mongod" > /dev/null; then
    echo "Starting MongoDB..."
    if command -v brew &> /dev/null; then
        brew services start mongodb-community
    else
        sudo systemctl start mongod
    fi
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if database is seeded
echo ""
echo "Checking database..."
python3 -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); db = client.yogic_guide; count = db.poses.count_documents({}); print(f'Poses in database: {count}'); exit(0 if count > 0 else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Seeding database..."
    python3 seed_poses.py
fi

echo ""
echo "========================================"
echo "  Starting Flask Application"
echo "========================================"
echo ""
echo "Open your browser and go to:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python3 app.py
