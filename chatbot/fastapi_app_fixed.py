# fastapi_app.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from groq import Groq
import os
import PyPDF2
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import time
from pathlib import Path
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import jwt
from typing import Optional, Dict, Any
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# FastAPI app instance
app = FastAPI(title="Wolf AI Chatbot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001", 
        "http://localhost:3000", 
        "http://localhost:8000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(32))  # use env if set, fallback to random
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client_mongo = MongoClient(MONGO_URI)
db = client_mongo.wolfai_chatbot
users_collection = db.users

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant").strip()
GROQ_WHISPER_MODEL = os.getenv("GROQ_WHISPER_MODEL", "whisper-large-v3-turbo").strip()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Global variables (same as Flask)
knowledge_sources = {
    'pdf': {'content': '', 'filename': '', 'loaded': False},
    'website': {'content': '', 'url': '', 'loaded': False}
}
conversations = {}
server_start_time = datetime.now()

# Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class WebsiteRequest(BaseModel):
    url: str

class ClearSourceRequest(BaseModel):
    source_type: str = "all"

class TextToSpeechRequest(BaseModel):
    text: str

# JWT token functions
def create_jwt_token(user_data: dict) -> str:
    payload = {
        "user_id": user_data["user_id"],
        "email": user_data["email"],
        "name": user_data["name"],
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Authentication dependency
async def get_current_user(token: str = Depends(security)):
    return verify_jwt_token(token.credentials)

# Helper functions (same as Flask)
def load_pdf_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def scrape_website_content(url: str) -> str:
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/124.0.0.0 Safari/537.36')
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:15000]
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def find_relevant_content(user_message: str, max_context_tokens: int = 2500):
    user_words = user_message.lower().split()
    combined_content = ""
    loaded_sources = []

    for source_type, source_data in knowledge_sources.items():
        if source_data['loaded'] and source_data['content']:
            combined_content += f"\n\n=== {source_type.upper()} SOURCE ===\n{source_data['content']}"
            loaded_sources.append(source_type)

    if not combined_content:
        return "", "none", loaded_sources

    max_words = int(max_context_tokens * 0.75)
    all_words = combined_content.split()
    if len(all_words) > max_words:
        paragraphs = combined_content.split('\n\n')
        scored = []
        for para in paragraphs:
            p = para.strip()
            if len(p) < 50:
                continue
            score = sum(1 for w in user_words if w in p.lower())
            score += min(len(p) // 500, 2)
            scored.append((score, p))

        scored.sort(key=lambda x: x[0], reverse=True)

        selected = []
        count_words = 0
        for score, p in scored:
            w = len(p.split())
            if count_words + w > max_words:
                break
            selected.append(p)
            count_words += w

        combined_content = ("\n\n".join(selected)).strip() or " ".join(all_words[:max_words])

    return combined_content, "combined", loaded_sources

def filter_technical_content(response: str) -> str:
    technical_keywords = {
        'jquery', 'javascript', 'js', 'code', 'function', 'script', 'html', 'css',
        'programming', 'developer', 'implementation', 'technical', 'syntax', 'api',
        'framework', 'library', 'dom', 'element', 'selector', 'event', 'callback'
    }

    rl = response.lower()
    if any(k in rl for k in technical_keywords):
        return (
            "I'm here to help you with product information and sales support! "
            "Let me focus on what I do best—helping you understand our products and their benefits.\n\n"
            "What specific product information can I help you with today? I can provide details about:\n"
            "• Product features and specifications\n"
            "• Pricing and availability\n"
            "• Product comparisons\n"
            "• Recommendations based on your needs\n"
            "• Customer support and service options"
        )
    return response

# Health check endpoint (defined early)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# API Routes
@app.post("/api/login")
async def login(credentials: LoginRequest):
    try:
        email = credentials.email.lower().strip()
        password = credentials.password
        
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")
        
        user = users_collection.find_one({"email": email})
        
        if user and check_password_hash(user['password'], password):
            user_data = {
                "user_id": str(user['_id']),
                "email": user['email'],
                "name": user['name']
            }
            token = create_jwt_token(user_data)
            
            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "name": user['name'],
                    "email": user['email']
                },
                "token": token
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/signup")
async def signup(user_data: SignupRequest):
    try:
        name = user_data.name.strip()
        email = user_data.email.lower().strip()
        password = user_data.password
        
        if not name or not email or not password:
            raise HTTPException(status_code=400, detail="All fields are required")
        
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        # Check if user already exists
        if users_collection.find_one({"email": email}):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        new_user_data = {
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "created_at": datetime.now()
        }
        
        result = users_collection.insert_one(new_user_data)
        
        # Create JWT token for auto login
        user_token_data = {
            "user_id": str(result.inserted_id),
            "email": email,
            "name": name
        }
        token = create_jwt_token(user_token_data)
        
        return {
            "success": True,
            "message": "Account created successfully",
            "user": {
                "name": name,
                "email": email
            },
            "token": token
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    return {"success": True, "message": "Logged out successfully"}

@app.post("/api/load_pdf")
async def load_pdf(
    current_user: dict = Depends(get_current_user),
    pdf: UploadFile = File(...)
):
    try:
        if not pdf.filename:
            raise HTTPException(status_code=400, detail="No file selected")

        if not pdf.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        # Save temporary file
        temp_path = f"temp_{int(datetime.now().timestamp())}_{pdf.filename}"
        with open(temp_path, "wb") as f:
            content = await pdf.read()
            f.write(content)

        # Extract PDF content
        pdf_content = load_pdf_from_file(temp_path)
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except Exception:
            pass

        if pdf_content.startswith("Error reading PDF"):
            raise HTTPException(status_code=500, detail=pdf_content)

        knowledge_sources['pdf'] = {
            'content': pdf_content,
            'filename': pdf.filename,
            'loaded': True
        }

        return {
            "success": True,
            "message": "Product catalog PDF loaded successfully",
            "filename": pdf.filename,
            "text_length": len(pdf_content),
            "word_count": len(pdf_content.split()),
            "source_type": "pdf"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/load_website")
async def load_website(
    website_data: WebsiteRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        url = website_data.url.strip()
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        content = scrape_website_content(url)

        if content.startswith("Error scraping website"):
            raise HTTPException(status_code=500, detail=content)

        knowledge_sources['website'] = {
            'content': content,
            'url': url,
            'loaded': True
        }

        return {
            "success": True,
            "message": "Brand website content loaded successfully",
            "url": url,
            "text_length": len(content),
            "word_count": len(content.split()),
            "source_type": "website"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/speech-to-text")
async def speech_to_text(
    current_user: dict = Depends(get_current_user),
    audio: UploadFile = File(...)
):
    try:
        if not audio or not audio.filename:
            raise HTTPException(status_code=400, detail="No audio file provided")

        # Get original filename and determine extension
        original_filename = audio.filename
        file_extension = ".webm" if "webm" in audio.content_type else ".wav"
        temp_path = f"temp_audio_{int(datetime.now().timestamp())}{file_extension}"
        
        print(f"Processing audio file: {original_filename}, Content-Type: {audio.content_type}")
        
        # Save audio file
        content = await audio.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Audio file is empty")
            
        with open(temp_path, "wb") as f:
            f.write(content)
        
        print(f"Audio file saved: {temp_path}, Size: {len(content)} bytes")

        try:
            # Open file for Groq API
            with open(temp_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model=GROQ_WHISPER_MODEL,
                    prompt="This is a customer service conversation about products and sales.",
                    response_format="json",
                    language="en"
                )
                text_out = getattr(transcription, "text", "") or ""
                
            print(f"Transcription result: {text_out}")
            
        finally:
            try:
                os.remove(temp_path)
            except Exception as cleanup_error:
                print(f"Failed to cleanup temp file: {cleanup_error}")

        if not text_out.strip():
            return {
                "success": False,
                "text": "",
                "error": "No speech detected in audio"
            }

        return {
            "success": True,
            "text": text_out.strip(),
            "confidence": 0.95
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Speech-to-text error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech recognition failed: {str(e)}")

@app.post("/api/text-to-speech")
async def text_to_speech(
    tts_data: TextToSpeechRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        text = tts_data.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")

        return {
            "success": True,
            "message": "Use browser speech synthesis",
            "text": text
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(
    chat_data: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not any(source['loaded'] for source in knowledge_sources.values()):
            raise HTTPException(
                status_code=400, 
                detail="No product information loaded. Please upload a PDF catalog or add a brand website URL first."
            )

        user_message = chat_data.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")

        session_id = chat_data.session_id
        relevant_content, source_type, loaded_sources = find_relevant_content(user_message)

        if session_id not in conversations:
            conversations[session_id] = []

        system_message = {
            "role": "system",
            "content": f"""You are Wolf AI, a professional sales assistant. You MUST follow these rules:

PRODUCT INFORMATION (only what you may cite):
{relevant_content}

STRICT RULES:
1. ONLY discuss products and information from the loaded content above
2. NEVER mention technical implementation details
3. Focus EXCLUSIVELY on sales, products, features, pricing, and customer service
4. Be a sales expert, not a technical expert
5. Always stay in character as Wolf AI sales representative

YOUR ROLE:
- You are Wolf AI, a knowledgeable sales assistant
- Help customers understand products and make purchasing decisions
- Provide accurate information based ONLY on the loaded product content
- Highlight key benefits, features, and value propositions
- Address customer concerns professionally
- Suggest products based on customer needs
- Be enthusiastic but professional
- Keep responses focused on sales and products (100-200 words)
- Always end with a helpful next step or question about the products"""
        }

        recent_messages = [system_message]
        recent_messages.extend(conversations[session_id][-8:])
        recent_messages.append({"role": "user", "content": user_message})

        max_retries = 3
        retry_delay = 2
        last_error = None

        for attempt in range(max_retries):
            try:
                chat_completion = client.chat.completions.create(
                    messages=recent_messages,
                    model=GROQ_CHAT_MODEL,
                    temperature=0.3,
                    max_completion_tokens=400,
                    top_p=0.8,
                )

                assistant_response = chat_completion.choices[0].message.content
                filtered_response = filter_technical_content(assistant_response)
                last_error = None
                break

            except Exception as api_error:
                last_error = str(api_error)
                if any(k in last_error.lower() for k in ["rate", "limit", "timeout", "temporarily"]):
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    raise

        if last_error and 'filtered_response' not in locals():
            filtered_response = (
                "I'm experiencing temporary high demand. Please try again in a moment.\n\n"
                "Meanwhile, I can help with:\n"
                "• Product information & specifications\n"
                "• Pricing & availability\n"
                "• Feature comparisons\n"
                "• Recommendations based on your needs"
            )

        conversations[session_id].append({"role": "user", "content": user_message})
        conversations[session_id].append({"role": "assistant", "content": filtered_response})
        conversations[session_id] = conversations[session_id][-10:]

        return {
            "success": True,
            "response": filtered_response,
            "session_id": session_id,
            "source_type": source_type,
            "loaded_sources": loaded_sources,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/api/clear_source")
async def clear_source(
    clear_data: ClearSourceRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        source_type = clear_data.source_type

        if source_type == 'all':
            for source in knowledge_sources.values():
                source['content'] = ''
                source['loaded'] = False
            conversations.clear()
            return {"success": True, "message": "All sources cleared"}
        elif source_type in knowledge_sources:
            knowledge_sources[source_type]['content'] = ''
            knowledge_sources[source_type]['loaded'] = False
            return {"success": True, "message": f"{source_type.title()} source cleared"}
        else:
            raise HTTPException(status_code=400, detail="Invalid source type")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def status(current_user: dict = Depends(get_current_user)):
    uptime = datetime.now() - server_start_time
    loaded_sources = {k: v['loaded'] for k, v in knowledge_sources.items()}

    return {
        "status": "running",
        "uptime": str(uptime).split('.')[0],
        "sources": loaded_sources,
        "conversations": len(conversations),
        "total_sources_loaded": sum(1 for v in loaded_sources.values() if v)
    }

# Static file serving setup
static_dir = Path("static/dist")
if static_dir.exists():
    # Mount static assets first
    app.mount("/assets", StaticFiles(directory="static/dist/assets"), name="assets")
    app.mount("/static", StaticFiles(directory="static/dist"), name="static")

# Frontend routes (only if static directory exists)
@app.get("/")
async def serve_home():
    if static_dir.exists():
        return FileResponse("static/dist/index.html")
    else:
        return {"message": "Wolf AI Backend is running. Please build the React frontend first."}

@app.get("/home")
async def serve_home_alt():
    return FileResponse("static/dist/index.html")

@app.get("/login")
async def serve_login():
    return FileResponse("static/dist/index.html")

@app.get("/signup")
async def serve_signup():
    return FileResponse("static/dist/index.html")

@app.get("/dashboard")
async def serve_dashboard():
    return FileResponse("static/dist/index.html")

# Catch-all route for React Router (MUST BE LAST!)
@app.get("/{path:path}")
async def serve_react_app(path: str):
    # Skip API routes
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Skip already handled endpoints
    if path in ["health"]:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    # Serve React index.html for all other routes
    if static_dir.exists():
        return FileResponse("static/dist/index.html")
    else:
        raise HTTPException(status_code=404, detail="Frontend not built")

if __name__ == "__main__":
    import uvicorn
    print("Wolf AI - Sales Assistant Chatbot (FastAPI)")
    print("Supports: PDF Catalogs, Brand Websites, Speech-to-Text, Text-to-Speech")
    print("FastAPI Backend: http://localhost:8000")
    print("React Frontend: http://localhost:3001")
    print("\nStarting server...")
    uvicorn.run("fastapi_app_fixed:app", host="0.0.0.0", port=8000, reload=True)
