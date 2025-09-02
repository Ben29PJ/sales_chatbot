# 🐺 Wolf AI - Premium Sales Assistant Chatbot

A sophisticated AI-powered sales assistant with voice interaction, document intelligence, and premium user experience.

## ✨ Features

### 🎯 Core Functionality
- **Intelligent Chat Assistant** - Powered by Groq's advanced language models
- **Voice Interaction** - Speech-to-text and text-to-speech capabilities
- **Document Intelligence** - Upload PDF catalogs for product knowledge
- **Website Integration** - Scrape and analyze website content
- **Multi-source Knowledge** - Combine PDFs and websites for comprehensive information

### 🔐 Authentication & Security
- **User Authentication** - Secure login/signup with JWT tokens
- **Session Management** - Persistent user sessions
- **MongoDB Integration** - Secure user data storage
- **Protected Routes** - Authentication-required API endpoints

### 🎨 Premium UI/UX
- **Premium Home Page** - Beautiful landing page with Wolf AI branding
- **Glassmorphism Design** - Modern glass-effect styling
- **Responsive Layout** - Works on desktop and mobile
- **Dark Theme** - Professional dark theme with premium gradients
- **Smooth Animations** - Framer Motion powered animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)

### 1. Install Python Dependencies
```bash
pip install fastapi uvicorn groq pymongo PyPDF2 requests beautifulsoup4 python-multipart PyJWT pydantic[email] flask flask-cors werkzeug numpy python-dotenv
```

### 2. Install Frontend Dependencies
```bash
cd react-frontend
npm install
```

### 3. Build Frontend
```bash
npm run build
```

### 4. Start Backend Server
```bash
# FastAPI (Recommended)
python fastapi_app.py

# Or Flask (Alternative)
python app.py
```

### 5. Start Frontend Development Server (Optional)
```bash
cd react-frontend
npm run dev
```

### 6. Access the Application
- **FastAPI Backend**: http://localhost:8000
- **React Frontend**: http://localhost:3001 (dev) or served by backend
- **Home Page**: Visit the root URL to see the premium landing page

## 🔧 Audio Functionality Fixes

### Issues Resolved:
1. **Audio Blob Handling** - Fixed state management in React recording
2. **File Format Support** - Enhanced support for WebM and WAV formats
3. **Error Handling** - Improved error messages and logging
4. **Recording State** - Fixed recording state persistence
5. **Groq API Integration** - Proper file handling for speech-to-text

### Audio Features:
- **Voice Recording** - Click microphone button to record
- **Automatic Transcription** - Speech converted to text using Groq Whisper
- **Text-to-Speech** - Browser-based speech synthesis
- **Recording Feedback** - Visual indicators for recording state
- **Error Recovery** - Graceful handling of audio failures

## 🏠 Home Page Features

### Premium Landing Page:
- **Wolf AI Branding** - Professional logo and branding
- **Hero Section** - Compelling value proposition
- **Feature Showcase** - Interactive feature demonstration
- **About Section** - Company information and AI capabilities
- **Testimonials** - Customer success stories
- **Call-to-Action** - Clear signup/login options
- **Responsive Design** - Mobile-friendly layout

### Navigation Flow:
1. **Home Page** (`/`) - Landing page for new visitors
2. **Login Page** (`/login`) - User authentication
3. **Signup Page** (`/signup`) - New user registration
4. **Dashboard** (`/dashboard`) - Main chat interface

## 📁 Project Structure

```
chatbot/
├── fastapi_app.py          # FastAPI backend (recommended)
├── app.py                  # Flask backend (alternative)
├── requirements.txt        # Python dependencies
├── test_audio.py          # Audio functionality test script
├── react-frontend/        # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.jsx        # NEW: Premium landing page
│   │   │   ├── ChatDashboard.jsx   # Main chat interface
│   │   │   ├── LoginPage.jsx       # User login
│   │   │   ├── SignupPage.jsx      # User registration
│   │   │   ├── ChatMessage.jsx     # Chat message component
│   │   │   ├── FileUpload.jsx      # File upload component
│   │   │   └── StatusPanel.jsx     # Status display
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx     # Authentication context
│   │   ├── services/
│   │   │   └── api.js             # API service functions
│   │   ├── App.jsx                # Main app component
│   │   ├── main.jsx               # App entry point
│   │   └── index.css              # Global styles
│   ├── package.json               # Node.js dependencies
│   └── vite.config.js            # Vite configuration
└── templates/                     # Flask templates (fallback)
    ├── index.html
    ├── login.html
    └── signup.html
```

## 🎤 Audio Configuration

### Browser Compatibility:
- **Chrome** - Full support (recommended)
- **Firefox** - Full support
- **Safari** - Limited support
- **Edge** - Full support

### Audio Formats:
- **Recording**: WebM with Opus codec (preferred) or WebM
- **Processing**: Groq Whisper API
- **Playback**: Browser Speech Synthesis API

### Troubleshooting Audio:
1. **Microphone Permissions** - Ensure browser has microphone access
2. **HTTPS Required** - Audio recording requires HTTPS in production
3. **File Size Limits** - Keep recordings under 25MB
4. **Network Timeout** - Check Groq API connectivity

## 🔧 Configuration

### Environment Variables:
```bash
GROQ_API_KEY=your_groq_api_key
GROQ_CHAT_MODEL=llama-3.1-8b-instant
GROQ_WHISPER_MODEL=whisper-large-v3-turbo
MONGO_URI=mongodb://localhost:27017/
```

### MongoDB Setup:
1. Install MongoDB locally or use MongoDB Atlas
2. Create database: `wolfai_chatbot`
3. Collection `users` will be created automatically

## 📚 API Endpoints

### Authentication:
- `POST /api/login` - User login
- `POST /api/signup` - User registration
- `POST /api/logout` - User logout

### Chat & Knowledge:
- `POST /api/chat` - Send chat message
- `POST /api/load_pdf` - Upload PDF catalog
- `POST /api/load_website` - Load website content
- `POST /api/clear_source` - Clear knowledge sources
- `GET /api/status` - Get system status

### Audio:
- `POST /api/speech-to-text` - Convert audio to text
- `POST /api/text-to-speech` - Text-to-speech (browser-based)

## 🐛 Bug Fixes & Improvements

### Audio Issues Fixed:
1. **State Management** - Fixed React state handling for audio chunks
2. **Blob Creation** - Proper audio blob creation and processing
3. **File Handling** - Enhanced file type detection and processing
4. **Error Recovery** - Better error handling and user feedback
5. **Recording UI** - Improved visual feedback during recording

### UI Enhancements:
1. **Premium Home Page** - Professional landing page
2. **Improved Animations** - Smooth transitions and effects
3. **Better Navigation** - Clear routing structure
4. **Enhanced Styling** - Glassmorphism and premium gradients
5. **Mobile Responsive** - Works on all device sizes

## 🚀 Deployment

### Development:
```bash
# Start backend
python fastapi_app.py

# Start frontend (in another terminal)
cd react-frontend
npm run dev
```

### Production:
```bash
# Build frontend
cd react-frontend
npm run build

# Start backend (serves built frontend)
python fastapi_app.py
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Support

For support and questions:
1. Check the test script: `python test_audio.py`
2. Review browser console for errors
3. Ensure all dependencies are installed
4. Verify MongoDB is running
5. Check Groq API key is valid

## 🎉 What's New

### Version 2.0 Features:
- ✅ Premium Home Page with Wolf AI branding
- ✅ Fixed audio recording and speech-to-text
- ✅ Enhanced error handling and user feedback
- ✅ Improved UI/UX with glassmorphism design
- ✅ Better routing and navigation structure
- ✅ Mobile-responsive design
- ✅ Professional animations and transitions
