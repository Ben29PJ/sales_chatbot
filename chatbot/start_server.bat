@echo off
echo Wolf AI Server Manager
echo ======================

REM Kill any existing Python processes that might be running the server
echo Checking for existing server processes...
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" ^| findstr python') do (
    echo Found Python process %%i, checking if it's our server...
    taskkill /F /PID %%i >nul 2>&1
)

REM Wait a moment for processes to terminate
timeout /t 2 /nobreak >nul

echo Starting Wolf AI FastAPI server...
echo URL: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Run the FastAPI application
python fastapi_app_fixed.py

pause
