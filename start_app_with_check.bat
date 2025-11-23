@echo off
echo.
echo ========================================
echo   YOGA APP STARTUP WITH DETECTION CHECK
echo ========================================
echo.

echo [1/2] Testing detection system...
python test_detection_api.py

if errorlevel 1 (
    echo.
    echo ERROR: Detection system test failed!
    echo Please fix the errors above before starting the app.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting Flask app...
echo.
echo App will start at: http://localhost:5000
echo.
echo Test pages:
echo   - Simple Test: http://localhost:5000/simple-yoga-test
echo   - Full Session: http://localhost:5000/module/surya-namaskar
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
