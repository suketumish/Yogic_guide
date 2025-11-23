@echo off
echo.
echo ========================================
echo   YOGA POSE DETECTION - SETUP
echo ========================================
echo.
echo This will create a Python 3.11 environment
echo with all dependencies for yoga detection.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

echo.
echo [1/4] Creating Python 3.11 environment...
conda create -n yoga_app python=3.11 -y

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create environment
    echo Make sure Conda is installed and in PATH
    pause
    exit /b 1
)

echo.
echo [2/4] Activating environment...
call conda activate yoga_app

echo.
echo [3/4] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Check requirements.txt and try again
    pause
    exit /b 1
)

echo.
echo [4/4] Running system check...
python check_system.py

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo To start the app:
echo   1. conda activate yoga_app
echo   2. python app.py
echo.
echo Then open: http://localhost:5000
echo.
pause
