@echo off
echo ========================================
echo   AI - Powered Personalized Yogic Guide
echo ========================================
echo.

REM Check if MongoDB is running
echo Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if errorlevel 1 (
    echo Starting MongoDB...
    net start MongoDB
)

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if database is seeded
echo.
echo Checking database...
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); db = client.yogic_guide; count = db.poses.count_documents({}); print(f'Poses in database: {count}'); exit(0 if count > 0 else 1)" 2>nul
if errorlevel 1 (
    echo Seeding database...
    python seed_poses.py
)

echo.
echo ========================================
echo   Starting Flask Application
echo ========================================
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py
