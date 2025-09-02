# 🐺 Wolf AI - Activation Guide

## 🚀 Step-by-Step Activation Instructions

### Method 1: Automatic Setup (Recommended)
```bash
# Run the automated setup script
python setup_and_run.py
```

### Method 2: Manual Setup

#### Step 1: Install Python Dependencies
```bash
cd D:\c7\c7\chatbot
python -m pip install fastapi uvicorn groq pymongo PyPDF2 requests beautifulsoup4 python-multipart PyJWT "pydantic[email]" flask flask-cors werkzeug
```

#### Step 2: Install Frontend Dependencies
```bash
cd react-frontend
npm install
```

#### Step 3: Build React Frontend
```bash
npm run build
```

#### Step 4: Start FastAPI Backend
```bash
cd ..
python fastapi_app.py
```

### Method 3: Windows Batch File
```bash
# Double-click or run:
start_wolfai.bat
```

## 🔧 Troubleshooting Common Issues

### Issue 1: "Page Not Found" Error
**Cause**: React build files not found or FastAPI not serving static files

**Solutions**:
1. Ensure React build exists:
   ```bash
   cd react-frontend
   npm run build
   ```

2. Check if `static/dist/index.html` exists:
   ```bash
   dir static\dist\index.html
   ```

3. Restart FastAPI server:
   ```bash
   python fastapi_app.py
   ```

### Issue 2: CORS Errors
**Cause**: Frontend and backend running on different ports with CORS issues

**Solutions**:
1. Use only FastAPI server on port 8000 (serves both API and frontend)
2. Don't run separate React dev server on port 3001
3. Access application at: `http://localhost:8000`

### Issue 3: Audio Not Working
**Cause**: Browser permissions or audio processing issues

**Solutions**:
1. Allow microphone access in browser
2. Use Chrome or Firefox (best compatibility)
3. Ensure HTTPS in production (localhost works for development)
4. Check browser console for errors

### Issue 4: MongoDB Connection Error
**Cause**: MongoDB not running

**Solutions**:
1. Install MongoDB Community Edition
2. Start MongoDB:
   ```bash
   mongod --dbpath "C:\data\db"
   ```
3. Or use MongoDB Atlas (cloud)

### Issue 5: Dependencies Missing
**Cause**: Python packages not installed

**Solutions**:
1. Install pip if missing:
   ```bash
   python -m ensurepip --upgrade
   ```
2. Install all dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## 📋 Verification Checklist

### ✅ Pre-Launch Checklist:
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] MongoDB running (or Atlas configured)
- [ ] React frontend built (`static/dist/index.html` exists)
- [ ] Python dependencies installed
- [ ] Groq API key configured

### ✅ Post-Launch Checklist:
- [ ] FastAPI server running on port 8000
- [ ] Home page loads at `http://localhost:8000`
- [ ] Can navigate to login page
- [ ] Can create new account
- [ ] Can access dashboard after login
- [ ] Voice recording works (microphone button)
- [ ] PDF upload works
- [ ] Website loading works

## 🌐 Endpoint Testing

### Test API Endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Test homepage (should return HTML)
curl http://localhost:8000/

# Test API endpoint (will require auth token)
curl -X POST http://localhost:8000/api/login -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"password"}'
```

## 🎯 Quick Fix Commands

### Rebuild Everything:
```bash
cd react-frontend
npm install
npm run build
cd ..
python fastapi_app.py
```

### Clean Start:
```bash
# Remove old build
rmdir /s static\dist
cd react-frontend
npm run build
cd ..
python fastapi_app.py
```

### Check Build Files:
```bash
dir static\dist
# Should show: index.html and assets folder
```

## 🔍 Debug Mode

### Enable Debug Logging:
1. Open `fastapi_app.py`
2. Find line: `uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)`
3. Add debug: `uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="debug")`

### Check Browser Console:
1. Open browser Developer Tools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests

## 📞 Emergency Fallback

If nothing works, use the Flask version:
```bash
python app.py
# Then access: http://localhost:3000
```

## 🎉 Success Indicators

You know it's working when you see:
1. **Home Page**: Beautiful landing page with Wolf AI logo
2. **Navigation**: Login/Signup buttons work
3. **Authentication**: Can create account and login
4. **Dashboard**: Chat interface loads
5. **Audio**: Microphone button shows recording animation
6. **Features**: PDF upload and website loading work

## 📱 Access URLs

Once running, access these URLs in your browser:
- **🏠 Home**: http://localhost:8000
- **🔐 Login**: http://localhost:8000/login  
- **📝 Signup**: http://localhost:8000/signup
- **💬 Chat**: http://localhost:8000/dashboard
- **🩺 API Health**: http://localhost:8000/health
- **📚 API Docs**: http://localhost:8000/docs

## 🆘 Still Having Issues?

1. **Check Windows Firewall**: Allow Python and Node.js
2. **Check Antivirus**: Whitelist the project folder
3. **Run as Administrator**: Try running PowerShell as admin
4. **Check Ports**: Ensure ports 8000 and 27017 are available
5. **Restart Computer**: Sometimes helps with port conflicts

## 🎤 Testing Audio Specifically

1. Open `http://localhost:8000`
2. Click "Sign Up" and create account
3. Go to dashboard
4. Click microphone button
5. Allow browser microphone access
6. Speak clearly for 2-3 seconds
7. Click microphone again to stop
8. Text should appear in input field

**Audio Requirements**:
- Chrome/Firefox browser (recommended)
- Microphone access allowed
- Valid Groq API key
- Internet connection for Groq API
