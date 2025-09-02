# Wolf AI Premium - FastAPI + React Application

A premium sales assistant chatbot with modern FastAPI backend and React frontend.

## 🚀 Features

- **Modern FastAPI Backend**: High-performance async API with automatic documentation
- **Premium React Frontend**: Beautiful UI with glassmorphism effects and professional colors
- **JWT Authentication**: Secure token-based authentication
- **PDF Upload**: Process product catalogs from PDF files
- **Website Scraping**: Load content from brand websites
- **Voice Input**: Speech-to-text functionality
- **Text-to-Speech**: Audio responses
- **Real-time Chat**: Interactive conversation with AI assistant
- **Multi-source Knowledge**: Combine PDF and website content

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or remote)

### Quick Start

1. **Clone and Setup**:
   ```bash
   cd D:\c7\c7\chatbot
   ```

2. **Run the Application**:
   ```bash
   start_app.bat
   ```
   This will automatically:
   - Create Python virtual environment
   - Install all dependencies
   - Start FastAPI backend on port 8000
   - Start React frontend on port 3001

3. **Access the Application**:
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements_fastapi.txt

# Run FastAPI server
python fastapi_app.py
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd react-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🎨 Premium Design Features

### Color Palette
- **Primary**: Indigo/Purple tones (#6366f1, #4f46e5)
- **Secondary**: Slate grays (#64748b, #475569, #334155)
- **Accent**: Orange highlights (#f37316, #ea580c)
- **Success**: Green (#22c55e)
- **Warning**: Amber (#f59e0b)
- **Danger**: Red (#ef4444)

### Design Elements
- **Glassmorphism**: Translucent cards with backdrop blur
- **Premium Gradients**: Multi-color gradients for buttons and accents
- **Smooth Animations**: Framer Motion powered transitions
- **Professional Typography**: Inter and Lexend fonts
- **Custom Shadows**: Premium shadow effects
- **Responsive Design**: Mobile-first approach

## 📡 API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/signup` - User registration
- `POST /api/logout` - User logout

### Chat & AI
- `POST /api/chat` - Send message to AI
- `GET /api/status` - Get system status
- `POST /api/clear_source` - Clear knowledge sources

### File Operations
- `POST /api/load_pdf` - Upload PDF catalog
- `POST /api/load_website` - Load website content

### Speech
- `POST /api/speech-to-text` - Convert audio to text
- `POST /api/text-to-speech` - Convert text to audio

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb://localhost:27017/
GROQ_API_KEY=your_groq_api_key_here
GROQ_CHAT_MODEL=llama-3.1-8b-instant
GROQ_WHISPER_MODEL=whisper-large-v3-turbo
```

### Database Setup
The application uses MongoDB. Make sure MongoDB is running locally or update the `MONGO_URI` in the environment variables.

## 🚦 Usage

1. **Sign Up/Login**: Create an account or sign in with existing credentials
2. **Upload Content**: Upload a PDF catalog or load website content
3. **Start Chatting**: Ask questions about products, pricing, features
4. **Voice Input**: Use microphone for voice queries
5. **Audio Output**: Click speaker icon to hear responses

## 🔒 Security Features

- JWT token authentication
- Secure password hashing
- CORS protection
- Input validation
- Error handling

## 📱 Browser Support

- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## 🛠️ Development

### Backend Development
```bash
# Run with auto-reload
uvicorn fastapi_app:app --reload --port 8000
```

### Frontend Development
```bash
cd react-frontend
npm run dev
```

### Building for Production
```bash
cd react-frontend
npm run build
```

## 📦 File Structure

```
chatbot/
├── fastapi_app.py              # FastAPI backend
├── requirements_fastapi.txt    # Python dependencies
├── start_app.bat              # Startup script
├── react-frontend/            # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── contexts/          # React contexts
│   │   ├── services/          # API services
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx          # Entry point
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── tailwind.config.js    # Tailwind CSS config
└── static/dist/              # Built frontend (production)
```

## 🆚 Migration from Flask

This application replaces the original Flask backend with FastAPI while maintaining all functionality:

- **Sessions → JWT Tokens**: More secure and stateless
- **Flask Routes → FastAPI Endpoints**: Better performance and auto-documentation
- **Template Rendering → React SPA**: Modern frontend framework
- **Same Business Logic**: All AI, PDF, and website functionality preserved

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Kill processes on ports
   netstat -ano | findstr :8000
   taskkill /PID <process_id> /F
   ```

2. **MongoDB Connection Error**:
   - Ensure MongoDB is running
   - Check MONGO_URI in environment variables

3. **CORS Errors**:
   - Verify frontend is running on port 3001
   - Check CORS settings in fastapi_app.py

4. **Module Not Found**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements_fastapi.txt`

## 📄 License

This project is private and proprietary.

---

**Wolf AI Premium** - Your Advanced Sales Assistant
