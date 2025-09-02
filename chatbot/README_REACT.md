# Wolf AI - Premium React Frontend

This is the React conversion of your Wolf AI chatbot with enhanced premium UI and modern features.

## 🚀 Features

### Premium UI Enhancements
- **Glass-morphism design** with backdrop blur effects
- **Smooth animations** using Framer Motion
- **Responsive layout** that works on all devices
- **Premium color scheme** with Wolf AI branding
- **Enhanced typography** with Inter font
- **Gradient effects** and glow animations
- **Improved accessibility** and user experience

### Maintained Functionalities
- ✅ **User Authentication** (login/signup with MongoDB)
- ✅ **PDF Catalog Upload** with drag & drop
- ✅ **Website Content Loading** 
- ✅ **AI Chat Interface** with Wolf AI assistant
- ✅ **Voice Recording** (speech-to-text)
- ✅ **Text-to-Speech** playback
- ✅ **Quick Action Buttons**
- ✅ **Source Management** and status tracking
- ✅ **Session Management**

## 📁 Project Structure

```
chatbot/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/         # Login/Signup components
│   │   │   ├── chat/         # Chat interface components
│   │   │   ├── layout/       # Header and layout components
│   │   │   └── ui/           # Reusable UI components
│   │   ├── contexts/         # React context for state management
│   │   ├── hooks/            # Custom React hooks
│   │   └── utils/            # API utilities
│   ├── package.json
│   └── vite.config.js
├── templates/                # Original HTML templates (kept as fallback)
├── static/dist/              # React build output
├── app_updated.py            # Updated Flask backend
└── setup_react.bat           # Setup script
```

## 🛠️ Setup Instructions

### Option 1: Quick Setup (Windows)
```bash
# Run the setup script
./setup_react.bat
```

### Option 2: Manual Setup
```bash
# 1. Install React dependencies
cd frontend
npm install

# 2. Create directories
mkdir -p ../static/dist

# 3. Build React app
npm run build

# 4. Start Flask backend
cd ..
python app_updated.py
```

## 🏃‍♂️ Running the Application

### Development Mode (React + Flask)
```bash
# Terminal 1: Start Flask backend
python app_updated.py

# Terminal 2: Start React frontend
cd frontend
npm run dev
```

- React dev server: http://localhost:3001
- Flask backend: http://localhost:3000

### Production Mode (Flask serves React build)
```bash
# Build React app
cd frontend
npm run build

# Start Flask (serves React build)
cd ..
python app_updated.py
```

- Application: http://localhost:3000

## 🎨 UI Improvements

### Login/Signup Pages
- **Floating background animations**
- **Enhanced password strength indicator**
- **Smooth form transitions**
- **Premium feature showcase**
- **Better error handling with toast notifications**

### Main Dashboard
- **Improved header** with animated Wolf logo
- **Enhanced source panel** with drag & drop support
- **Premium chat interface** with better message bubbles
- **Advanced voice recording modal**
- **Smooth animations** throughout the interface

### Chat Features
- **Better message formatting** with markdown support
- **Enhanced text-to-speech** controls
- **Improved typing indicators**
- **Source badges** showing data sources
- **Quick action buttons** with hover effects

## 🔧 Configuration

### Backend Configuration
The Flask app (`app_updated.py`) includes:
- React build serving at `/`
- API routes at `/api/*`
- Fallback to HTML templates
- CORS enabled for development

### Frontend Configuration
The React app includes:
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Router** for navigation
- **Axios** for API calls
- **React Hot Toast** for notifications

## 🚨 Important Notes

1. **Keep both versions**: The original HTML templates are preserved as fallback
2. **Environment variables**: Update any environment variables in `app_updated.py`
3. **MongoDB**: Ensure MongoDB is running for authentication
4. **API Keys**: Update your Groq API key in the backend
5. **CORS**: The backend is configured to work with React development server

## 📱 Browser Support

- **Chrome** 90+ ✅
- **Firefox** 88+ ✅  
- **Safari** 14+ ✅
- **Edge** 90+ ✅

## 🔒 Security Features

- **Session-based authentication**
- **CORS protection**
- **Input validation**
- **XSS protection**
- **Secure file upload**

## 🆘 Troubleshooting

### React Build Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Flask Serving Issues
- Ensure `static/dist` directory exists
- Check that React build completed successfully
- Verify Flask is updated to use `app_updated.py`

### Development Issues
- React dev server: http://localhost:3001
- Flask backend: http://localhost:3000
- Check browser console for errors
- Verify API calls are reaching Flask backend

## 🎯 Next Steps

1. Run `setup_react.bat` to get started
2. Test both development and production modes
3. Customize the UI colors/branding as needed
4. Deploy with your preferred hosting solution

The React version provides a more modern, responsive, and premium user experience while maintaining all the original functionality!
