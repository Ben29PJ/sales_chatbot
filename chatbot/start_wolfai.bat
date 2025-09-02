@echo off
echo.
echo 🐺 Wolf AI - Premium Sales Assistant
echo ===================================
echo.

echo 📦 Checking dependencies...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
) else (
    echo ✅ Python is available
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js
    pause
    exit /b 1
) else (
    echo ✅ Node.js is available
)

echo.
echo 🏗️  Building React frontend...
cd react-frontend
npm install
npm run build
cd ..

echo.
echo 🍃 Checking MongoDB...
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe" >NUL
if "%ERRORLEVEL%"=="1" (
    echo ⚠️  MongoDB is not running.
    echo    Install MongoDB and run: mongod --dbpath "C:\data\db"
    echo    Or use MongoDB Atlas cloud service
    echo.
) else (
    echo ✅ MongoDB is running
)

echo.
echo 🚀 Starting Wolf AI...
echo.
echo 📍 Access your application at:
echo    🏠 Home Page: http://localhost:8000
echo    🔐 Login: http://localhost:8000/login
echo    📝 Signup: http://localhost:8000/signup
echo    💬 Dashboard: http://localhost:8000/dashboard
echo    🩺 Health Check: http://localhost:8000/health
echo.
echo 🎤 Features Available:
echo    ✅ Voice Recording & Speech-to-Text
echo    ✅ PDF Document Upload
echo    ✅ Website Content Scraping
echo    ✅ Premium UI with Wolf AI Branding
echo.
echo Press Ctrl+C to stop the server
echo =====================================
echo.

python fastapi_app.py

echo.
echo 🛑 Wolf AI stopped
pause
