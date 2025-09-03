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
from typing import Optional, Dict, Any, List
import uuid
from dotenv import load_dotenv

# RAG imports
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np
from chromadb.config import Settings

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

# Enhanced conversation storage with business context
conversation_analytics = {}

# ================================
# RAG (Retrieval-Augmented Generation) System
# ================================

# Initialize RAG components
try:
    # Initialize embedding model (lightweight model for faster processing)
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize ChromaDB client
    chroma_client = chromadb.Client()
    
    # Create or get collections for each source type
    pdf_collection = None
    website_collection = None
    rag_initialized = True
    print("[OK] RAG system initialized successfully")
except Exception as e:
    print(f"[WARN] RAG initialization failed: {e}")
    embedding_model = None
    chroma_client = None
    pdf_collection = None
    website_collection = None
    rag_initialized = False

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks for better RAG performance"""
    if not text or len(text.strip()) == 0:
        return []
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.strip()) > 50:  # Only include substantial chunks
            chunks.append(chunk.strip())
    
    return chunks

def create_pdf_vector_store(pdf_content: str, filename: str) -> bool:
    """Create vector store for PDF content using RAG"""
    global pdf_collection
    
    if not rag_initialized or not pdf_content:
        return False
    
    try:
        # Clear existing collection if it exists
        try:
            chroma_client.delete_collection(name="pdf_documents")
        except Exception:
            pass
        
        # Create new collection
        pdf_collection = chroma_client.create_collection(
            name="pdf_documents",
            metadata={"description": "PDF document embeddings for RAG retrieval"}
        )
        
        # Split PDF content into chunks
        chunks = chunk_text(pdf_content, chunk_size=400, overlap=50)
        
        if not chunks:
            return False
        
        print(f"[PDF] Processing PDF: {filename} -> {len(chunks)} chunks")
        
        # Generate embeddings for chunks
        embeddings = embedding_model.encode(chunks).tolist()
        
        # Create IDs for chunks
        ids = [f"chunk_{i}_{filename}" for i in range(len(chunks))]
        
        # Prepare metadata for chunks
        metadatas = [{
            "source": "pdf",
            "filename": filename,
            "chunk_index": i,
            "content_preview": chunk[:100] + "..." if len(chunk) > 100 else chunk
        } for i, chunk in enumerate(chunks)]
        
        # Add to vector store
        pdf_collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"[OK] PDF vector store created: {len(chunks)} chunks indexed")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating PDF vector store: {e}")
        return False

def rag_search_pdf(query: str, n_results: int = 3) -> List[str]:
    """Perform semantic search on PDF content using RAG"""
    if not rag_initialized or not pdf_collection:
        return []
    
    try:
        # Generate embedding for the query
        query_embedding = embedding_model.encode([query]).tolist()
        
        # Search for similar content
        results = pdf_collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Return the most relevant chunks
        if results['documents'] and len(results['documents']) > 0:
            return results['documents'][0]  # First result set
        
        return []
        
    except Exception as e:
        print(f"[ERROR] RAG search error: {e}")
        return []

def create_website_vector_store(website_content: str, url: str) -> bool:
    """Create vector store for website content using RAG"""
    global website_collection
    
    if not rag_initialized or not website_content:
        return False
    
    try:
        # Clear existing website collection if it exists
        try:
            chroma_client.delete_collection(name="website_documents")
        except Exception:
            pass
        
        # Create new collection for website content
        website_collection = chroma_client.create_collection(
            name="website_documents",
            metadata={"description": "Website content embeddings for RAG retrieval"}
        )
        
        # Split website content into chunks
        chunks = chunk_text(website_content, chunk_size=400, overlap=50)
        
        if not chunks:
            return False
        
        print(f"[WEBSITE] Processing website: {url} -> {len(chunks)} chunks")
        
        # Generate embeddings for chunks
        embeddings = embedding_model.encode(chunks).tolist()
        
        # Create IDs for chunks
        ids = [f"chunk_{i}_{url.replace('/', '_').replace(':', '')}" for i in range(len(chunks))]
        
        # Prepare metadata for chunks
        metadatas = [{
            "source": "website",
            "url": url,
            "chunk_index": i,
            "content_preview": chunk[:100] + "..." if len(chunk) > 100 else chunk
        } for i, chunk in enumerate(chunks)]
        
        # Add to vector store
        website_collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"[OK] Website vector store created: {len(chunks)} chunks indexed")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating website vector store: {e}")
        return False

def rag_search_website(query: str, n_results: int = 3) -> List[str]:
    """Perform semantic search on website content using RAG"""
    if not rag_initialized or not website_collection:
        return []
    
    try:
        # Generate embedding for the query
        query_embedding = embedding_model.encode([query]).tolist()
        
        # Search for similar content
        results = website_collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Return the most relevant chunks
        if results['documents'] and len(results['documents']) > 0:
            return results['documents'][0]  # First result set
        
        return []
        
    except Exception as e:
        print(f"[ERROR] Website RAG search error: {e}")
        return []

def analyze_question_complexity(user_message: str) -> dict:
    """Analyze the complexity and type of business question"""
    analysis_indicators = {
        'strategic': ['strategy', 'strategic', 'vision', 'mission', 'goals', 'objectives', 'planning', 'roadmap'],
        'financial': ['revenue', 'profit', 'cost', 'budget', 'roi', 'investment', 'margin', 'financial', 'pricing'],
        'market': ['market', 'competition', 'industry', 'trend', 'segment', 'positioning', 'share'],
        'operational': ['process', 'efficiency', 'workflow', 'operations', 'productivity', 'scalability'],
        'analytical': ['analyze', 'analysis', 'insights', 'metrics', 'performance', 'data', 'statistics'],
        'predictive': ['forecast', 'predict', 'future', 'trend', 'projection', 'scenario', 'what if']
    }
    
    complexity_score = 0
    question_types = []
    
    message_lower = user_message.lower()
    
    for category, keywords in analysis_indicators.items():
        matches = sum(1 for keyword in keywords if keyword in message_lower)
        if matches > 0:
            question_types.append(category)
            complexity_score += matches * 2
    
    # Additional complexity indicators
    if any(word in message_lower for word in ['why', 'how', 'explain', 'compare', 'versus']):
        complexity_score += 3
    
    if len(user_message.split()) > 15:  # Long questions are typically more complex
        complexity_score += 2
    
    return {
        'complexity_score': complexity_score,
        'question_types': question_types,
        'is_complex': complexity_score > 5,
        'requires_analysis': any(t in question_types for t in ['strategic', 'analytical', 'predictive'])
    }

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
    except Exception as pdf_error:
        # If PDF parsing fails, try to read as text file (for testing)
        try:
            with open(file_path, 'r', encoding='utf-8') as text_file:
                content = text_file.read()
                if len(content.strip()) > 0:
                    print(f"[WARN] PDF parsing failed, treating as text file: {str(pdf_error)[:100]}")
                    return content.strip()
        except Exception as text_error:
            print(f"[ERROR] Both PDF and text parsing failed: {str(text_error)}")
        
        return f"Error reading PDF: {str(pdf_error)}"

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

def extract_business_insights(content: str) -> dict:
    """Extract key business insights from loaded content"""
    insights = {
        'products': [],
        'pricing': [],
        'features': [],
        'benefits': [],
        'target_markets': [],
        'competitive_advantages': [],
        'company_info': []
    }
    
    # Business-focused keyword extraction
    business_patterns = {
        'products': r'(?i)(product|service|solution|offering|item)s?\s+[^\n]{0,100}',
        'pricing': r'(?i)(price|cost|fee|rate|\$|USD|pricing|budget|investment)\s+[^\n]{0,100}',
        'features': r'(?i)(feature|capability|function|includes|offers|provides)\s+[^\n]{0,100}',
        'benefits': r'(?i)(benefit|advantage|value|helps|improves|increases|reduces)\s+[^\n]{0,100}',
        'target_markets': r'(?i)(market|customer|client|industry|sector|audience)\s+[^\n]{0,100}',
        'competitive_advantages': r'(?i)(unique|competitive|advantage|better|superior|leading)\s+[^\n]{0,100}'
    }
    
    for category, pattern in business_patterns.items():
        matches = re.findall(pattern, content)
        insights[category] = matches[:10]  # Limit to top 10 matches per category
    
    return insights

def find_relevant_content(user_message: str, max_context_tokens: int = 1500):
    """Enhanced content finder with RAG and business intelligence"""
    user_words = user_message.lower().split()
    combined_content = ""
    loaded_sources = []
    business_insights = {}
    retrieval_method = "none"

    for source_type, source_data in knowledge_sources.items():
        if source_data['loaded'] and source_data['content']:
            loaded_sources.append(source_type)
            
            if source_type == 'pdf' and rag_initialized and pdf_collection:
                # Use RAG for PDF content - semantic search
                print(f"[RAG] Using RAG semantic search for PDF content...")
                rag_chunks = rag_search_pdf(user_message, n_results=5)
                
                if rag_chunks:
                    # Join the most relevant chunks
                    rag_content = "\n\n".join(rag_chunks[:3])  # Top 3 most relevant chunks
                    combined_content += f"\n\n=== {source_type.upper()} SOURCE (RAG) ===\n{rag_content}"
                    retrieval_method = "rag"
                    print(f"[OK] PDF RAG found {len(rag_chunks)} relevant chunks")
                else:
                    # Fallback to traditional keyword search for PDF
                    print("[FALLBACK] PDF RAG found no results, falling back to keyword search...")
                    content = source_data['content']
                    combined_content += f"\n\n=== {source_type.upper()} SOURCE (KEYWORD) ===\n{content}"
                    retrieval_method = "keyword_fallback"
            elif source_type == 'website' and rag_initialized and website_collection:
                # Use RAG for website content - semantic search
                print(f"[RAG] Using RAG semantic search for website content...")
                rag_chunks = rag_search_website(user_message, n_results=5)
                
                if rag_chunks:
                    # Join the most relevant chunks
                    rag_content = "\n\n".join(rag_chunks[:3])  # Top 3 most relevant chunks
                    combined_content += f"\n\n=== {source_type.upper()} SOURCE (RAG) ===\n{rag_content}"
                    retrieval_method = "rag"
                    print(f"[OK] Website RAG found {len(rag_chunks)} relevant chunks")
                else:
                    # Fallback to traditional keyword search for website
                    print("[FALLBACK] Website RAG found no results, falling back to keyword search...")
                    content = source_data['content']
                    combined_content += f"\n\n=== {source_type.upper()} SOURCE (KEYWORD) ===\n{content}"
                    retrieval_method = "keyword_fallback" if retrieval_method == "none" else retrieval_method
            else:
                # Use traditional method when RAG is unavailable
                content = source_data['content']
                combined_content += f"\n\n=== {source_type.upper()} SOURCE ===\n{content}"
                retrieval_method = "keyword" if retrieval_method == "none" else retrieval_method
            
            # Extract business insights (works for both RAG and traditional content)
            insights = extract_business_insights(source_data['content'])
            business_insights[source_type] = insights

    if not combined_content:
        return "", "none", loaded_sources, {}

    # Enhanced scoring with business context (only needed for non-RAG content)
    max_words = int(max_context_tokens * 0.75)
    all_words = combined_content.split()
    
    if len(all_words) > max_words and retrieval_method != "rag":
        # Traditional keyword-based filtering for website content
        paragraphs = combined_content.split('\n\n')
        scored = []
        
        # Business-focused scoring
        business_keywords = {
            'analysis': ['analysis', 'analyze', 'insights', 'trends', 'metrics', 'performance'],
            'strategy': ['strategy', 'strategic', 'planning', 'goals', 'objectives', 'vision'],
            'financial': ['revenue', 'profit', 'roi', 'cost', 'budget', 'financial', 'investment'],
            'market': ['market', 'competition', 'industry', 'customers', 'segments'],
            'operations': ['process', 'efficiency', 'workflow', 'operations', 'productivity']
        }
        
        for para in paragraphs:
            p = para.strip()
            if len(p) < 50:
                continue
                
            score = 0
            
            # Basic keyword matching
            score += sum(1 for w in user_words if w in p.lower()) * 2
            
            # Business context scoring
            for category, keywords in business_keywords.items():
                if any(keyword in user_message.lower() for keyword in keywords):
                    score += sum(1 for keyword in keywords if keyword in p.lower()) * 3
            
            # Length bonus for substantial content
            score += min(len(p) // 300, 3)
            
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
    elif len(all_words) > max_words:
        # For RAG content, simply truncate if too long (RAG already selected most relevant)
        combined_content = " ".join(all_words[:max_words])

    return combined_content, retrieval_method, loaded_sources, business_insights

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
        
        # Create RAG vector store for enhanced retrieval
        rag_success = create_pdf_vector_store(pdf_content, pdf.filename)
        rag_status = "✅ RAG enabled" if rag_success else "⚠️ RAG unavailable (fallback to keyword search)"

        return {
            "success": True,
            "message": f"Product catalog PDF loaded successfully - {rag_status}",
            "filename": pdf.filename,
            "text_length": len(pdf_content),
            "word_count": len(pdf_content.split()),
            "source_type": "pdf",
            "rag_enabled": rag_success
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
        
        # Create RAG vector store for enhanced website retrieval
        rag_success = create_website_vector_store(content, url)
        rag_status = "✅ RAG enabled" if rag_success else "⚠️ RAG unavailable (fallback to keyword search)"

        return {
            "success": True,
            "message": f"Brand website content loaded successfully - {rag_status}",
            "url": url,
            "text_length": len(content),
            "word_count": len(content.split()),
            "source_type": "website",
            "rag_enabled": rag_success
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
        user_message = chat_data.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Check if we have loaded content, but don't require it
        has_loaded_content = any(source['loaded'] for source in knowledge_sources.values())

        session_id = chat_data.session_id
        relevant_content, source_type, loaded_sources, business_insights = find_relevant_content(user_message)
        
        # Analyze question complexity
        question_analysis = analyze_question_complexity(user_message)

        if session_id not in conversations:
            conversations[session_id] = []
            conversation_analytics[session_id] = {'questions': [], 'complexity_scores': []}
        
        # Store question analytics
        conversation_analytics[session_id]['questions'].append({
            'message': user_message,
            'analysis': question_analysis,
            'timestamp': datetime.now().isoformat()
        })
        conversation_analytics[session_id]['complexity_scores'].append(question_analysis['complexity_score'])

        # Enhanced system message with business intelligence capabilities
        insights_summary = ""
        if business_insights:
            insights_summary = "\n\nBUSINESS INSIGHTS EXTRACTED:\n"
            for source, insights in business_insights.items():
                for category, items in insights.items():
                    if items:
                        insights_summary += f"- {category.title()}: {', '.join(items[:3])}\n"
        
        # Simplified conversation context to save tokens
        context_summary = ""
        if len(conversation_analytics[session_id]['questions']) > 1:
            recent_types = []
            for q in conversation_analytics[session_id]['questions'][-2:]:
                recent_types.extend(q['analysis']['question_types'])
            if recent_types:
                unique_types = list(set(recent_types))[:3]  # Convert set to list before slicing
                context_summary = f"\nPrevious topics: {', '.join(unique_types)}\n"

        # Determine response approach based on question complexity and available content
        is_complex_question = question_analysis['is_complex']
        question_types = question_analysis['question_types']
        
        # Enhanced system prompt based on question complexity
        if is_complex_question or question_analysis['requires_analysis']:
            max_tokens = 2000  # Longer responses for complex questions
            temperature = 0.8  # Higher creativity for analysis
        else:
            max_tokens = 800   # Standard responses for simple questions
            temperature = 0.6  # Moderate creativity

        # Enhanced system message that adapts based on available content
        content_context = ""
        if has_loaded_content and relevant_content:
            content_context = f"\n\n📈 SPECIFIC BUSINESS DATA AVAILABLE:\n{relevant_content}\n{insights_summary}"
        else:
            content_context = "\n\n📋 MODE: General Business Intelligence (No specific product data loaded)\n- Draw from extensive business knowledge and industry best practices\n- Provide strategic insights and analytical frameworks\n- Offer actionable business recommendations"

        # Significantly reduced system prompt to fit within Groq token limits
        system_message = {
            "role": "system",
            "content": f"""You are Wolf AI, an expert business consultant with MBA-level expertise.

🎯 EXPERTISE: Strategic analysis, financial modeling, market intelligence, sales strategy, and operational excellence.

📊 SESSION CONTEXT:
- Question Complexity: {question_analysis['complexity_score']}/20
- Categories: {', '.join(question_types) if question_types else 'General business'}
- Analysis Level: {'Deep' if question_analysis['requires_analysis'] else 'Standard'}
- Data: {'Specific business data available' if has_loaded_content else 'General business knowledge'}
{context_summary}
{content_context}

🧠 FRAMEWORKS: Apply SWOT, Porter's Five Forces, ROI analysis, market segmentation, competitive analysis, and strategic planning as appropriate.

💼 RESPONSE APPROACH:
- Strategic questions: Multi-framework analysis with implementation roadmap
- Financial questions: Detailed calculations with assumptions and scenarios
- Market questions: Competitive analysis with positioning recommendations
- Operational questions: Process optimization with efficiency metrics

📋 STANDARDS:
- Use clear structure with headings and bullet points
- Provide actionable recommendations with next steps
- Include quantitative analysis when possible
- Maintain professional consultant-level quality
- Focus on business value and ROI

🔥 MANDATE: Always provide valuable business insights using proven frameworks and best practices. Never refuse to answer due to lack of specific data - leverage extensive business knowledge instead."""
        }

        recent_messages = [system_message]
        recent_messages.extend(conversations[session_id][-4:])  # Reduced conversation history
        recent_messages.append({"role": "user", "content": user_message})

        max_retries = 3
        retry_delay = 2
        last_error = None

        filtered_response = None
        for attempt in range(max_retries):
            try:
                print(f"Chat attempt {attempt + 1}: Sending request to Groq API...")
                
                # Adaptive parameters based on question complexity - using only supported Groq parameters
                chat_completion = client.chat.completions.create(
                    messages=recent_messages,
                    model=GROQ_CHAT_MODEL,
                    temperature=temperature,  # Use the dynamic temperature
                    max_tokens=max_tokens,    # Use the dynamic max_tokens
                    top_p=0.9,
                    stream=False  # Ensure we get complete responses
                )

                assistant_response = chat_completion.choices[0].message.content
                print(f"✅ Got response from Groq API: {len(assistant_response)} characters")
                
                # Remove restrictive filtering - let the AI provide full business intelligence
                filtered_response = assistant_response
                last_error = None
                break

            except Exception as api_error:
                last_error = str(api_error)
                print(f"⚠️  API Error (attempt {attempt + 1}): {last_error}")
                
                # Check for specific error types that warrant retry
                if any(k in last_error.lower() for k in ["rate", "limit", "timeout", "temporarily", "overloaded"]):
                    print(f"🔄 Retrying in {retry_delay * (attempt + 1)} seconds...")
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    # For other errors, provide a helpful response
                    print(f"❌ Non-retryable error: {last_error}")
                    break

        # Handle case where we couldn't get a response
        if not filtered_response:
            if last_error:
                # Provide a more helpful error message based on the actual error
                if "api key" in last_error.lower():
                    filtered_response = "I'm having trouble with my API configuration. Please check that the Groq API key is valid and properly configured."
                elif "model" in last_error.lower():
                    filtered_response = "I'm having trouble with the AI model configuration. Please check that the model name is correct."
                elif "rate" in last_error.lower() or "limit" in last_error.lower():
                    filtered_response = "I'm experiencing high demand right now. Please try again in a moment."
                else:
                    filtered_response = f"I encountered an issue: {last_error}. I'm still learning to handle complex business questions better."
            else:
                filtered_response = "I'm having technical difficulties. Please try asking your question again."
            
            print(f"🚨 Using fallback response: {filtered_response[:100]}...")

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
        global pdf_collection, website_collection
        source_type = clear_data.source_type

        if source_type == 'all':
            for source in knowledge_sources.values():
                source['content'] = ''
                source['loaded'] = False
            conversations.clear()
            
            # Clear all RAG vector stores
            if rag_initialized:
                try:
                    if pdf_collection:
                        chroma_client.delete_collection(name="pdf_documents")
                        pdf_collection = None
                    if website_collection:
                        chroma_client.delete_collection(name="website_documents")
                        website_collection = None
                    print("✅ All RAG vector stores cleared")
                except Exception as e:
                    print(f"⚠️ Could not clear RAG vector stores: {e}")
            
            return {"success": True, "message": "All sources and RAG data cleared"}
        elif source_type == 'pdf':
            knowledge_sources['pdf']['content'] = ''
            knowledge_sources['pdf']['loaded'] = False
            
            # Clear PDF RAG vector store
            if rag_initialized and pdf_collection:
                try:
                    chroma_client.delete_collection(name="pdf_documents")
                    pdf_collection = None
                    print("✅ PDF RAG vector store cleared")
                except Exception as e:
                    print(f"⚠️ Could not clear PDF RAG vector store: {e}")
            
            return {"success": True, "message": "PDF source and RAG data cleared"}
        elif source_type == 'website':
            knowledge_sources['website']['content'] = ''
            knowledge_sources['website']['loaded'] = False
            
            # Clear website RAG vector store
            if rag_initialized and website_collection:
                try:
                    chroma_client.delete_collection(name="website_documents")
                    website_collection = None
                    print("✅ Website RAG vector store cleared")
                except Exception as e:
                    print(f"⚠️ Could not clear website RAG vector store: {e}")
            
            return {"success": True, "message": "Website source and RAG data cleared"}
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

# Add shutdown endpoint for manual control
@app.post("/api/shutdown")
async def shutdown_server():
    """Endpoint to manually shutdown the server"""
    import os
    print("[SHUTDOWN] Manual shutdown requested")
    os._exit(0)  # Force exit

if __name__ == "__main__":
    import uvicorn
    import sys
    import platform
    
    # Windows-specific signal handling
    if platform.system() == "Windows":
        try:
            import signal
            def signal_handler(sig, frame):
                print("\n[SHUTDOWN] Graceful shutdown initiated...")
                try:
                    # Clean up resources
                    if rag_initialized and pdf_collection:
                        print("[CLEANUP] Clearing RAG resources...")
                        chroma_client.delete_collection(name="pdf_documents")
                except Exception:
                    pass
                print("[SHUTDOWN] Server stopped gracefully.")
                sys.exit(0)
            
            # Register Windows-compatible signal handlers
            signal.signal(signal.SIGINT, signal_handler)
            if hasattr(signal, 'SIGBREAK'):
                signal.signal(signal.SIGBREAK, signal_handler)
                
        except Exception as e:
            print(f"[WARN] Signal handler setup failed: {e}")
    
    print("Wolf AI - Sales Assistant Chatbot (FastAPI)")
    print("Supports: PDF Catalogs, Brand Websites, Speech-to-Text, Text-to-Speech")
    print("FastAPI Backend: http://localhost:8000")
    print("React Frontend: http://localhost:3001")
    print("\nStarting server...")
    print("[INFO] Press Ctrl+C to stop, or POST to /api/shutdown")
    print("[INFO] Server will run until manually stopped\n")
    
    try:
        # Use uvicorn.Config and Server for better control
        config = uvicorn.Config(
            "fastapi_app_fixed:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            access_log=True,
            log_level="info",
            timeout_keep_alive=30,
            timeout_graceful_shutdown=5,
            lifespan="on"  # Enable lifespan events
        )
        
        server = uvicorn.Server(config)
        server.run()
        
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server stopped by user (Ctrl+C)")
        sys.exit(0)
    except SystemExit:
        print("\n[SHUTDOWN] Server stopped via system exit")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Server error: {e}")
        sys.exit(1)
    finally:
        print("[CLEANUP] Server shutdown complete")
