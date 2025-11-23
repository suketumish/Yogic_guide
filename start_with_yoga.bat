@echo off
echo ============================================
echo Starting Zen_Align with Yoga Detection
echo ============================================
echo.

echo Checking Python environment...
python --version
echo.

echo Checking TensorFlow...
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)" 2>nul
if errorlevel 1 (
    echo WARNING: TensorFlow not found in current environment
    echo Please activate the correct conda environment:
    echo   conda activate major
    echo.
    pause
    exit /b 1
)
echo.

echo Starting Flask server...
echo Server will start at: http://localhost:5000
echo.
echo Test pages:
echo   - Yoga Test: http://localhost:5000/yoga-test
echo   - Session: http://localhost:5000/module/surya-namaskar
echo.
echo Press Ctrl+C to stop
echo.

python app.py
