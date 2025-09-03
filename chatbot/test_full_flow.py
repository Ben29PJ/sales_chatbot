#!/usr/bin/env python3
"""
Complete test script for the FastAPI chatbot to verify:
1. User authentication (signup/login)
2. Chat functionality with business questions
3. Error handling and response quality
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_signup_login():
    """Test user signup and login"""
    print("🔐 Testing user authentication...")
    
    # Test signup
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    signup_response = requests.post(f"{BASE_URL}/api/signup", json=signup_data)
    print(f"Signup Status: {signup_response.status_code}")
    
    if signup_response.status_code == 200:
        result = signup_response.json()
        print(f"✅ Signup successful: {result['message']}")
        return result["token"]
    elif signup_response.status_code == 400 and "already registered" in signup_response.json().get("detail", ""):
        print("🔄 User already exists, trying login...")
        
        # Try login instead
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        login_response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            result = login_response.json()
            print(f"✅ Login successful: {result['message']}")
            return result["token"]
        else:
            print(f"❌ Login failed: {login_response.json()}")
            return None
    else:
        print(f"❌ Signup failed: {signup_response.json()}")
        return None

def test_chat_with_token(token):
    """Test chat functionality with authentication"""
    print("\n💬 Testing chat functionality...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test simple business question
    test_questions = [
        "What are the key factors to consider when pricing a new product?",
        "How can I improve customer retention in my business?",
        "What is a SWOT analysis and how can it help my company?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test Question {i}: {question}")
        
        chat_data = {
            "message": question,
            "session_id": "test_session"
        }
        
        try:
            chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers, timeout=30)
            print(f"Chat Status: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                response_text = result["response"]
                print(f"✅ Chat successful!")
                print(f"Response length: {len(response_text)} characters")
                print(f"First 200 chars: {response_text[:200]}...")
                
                # Check for fallback responses (indicates API issues)
                fallback_indicators = [
                    "high demand", 
                    "technical difficulties", 
                    "API configuration",
                    "experiencing temporary"
                ]
                
                if any(indicator in response_text.lower() for indicator in fallback_indicators):
                    print("⚠️  WARNING: Got fallback response - API may have issues!")
                    print(f"Full response: {response_text}")
                else:
                    print("✅ Got proper AI response!")
                    
            else:
                print(f"❌ Chat failed: {chat_response.json()}")
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out - this might indicate API issues")
        except Exception as e:
            print(f"❌ Chat request error: {str(e)}")

def test_api_configuration():
    """Test that API configuration is correct"""
    print("\n🔧 Testing API configuration...")
    
    # Test Groq API key
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print(f"✅ Groq API key found: {groq_key[:20]}...")
    else:
        print("❌ No Groq API key found in environment")
        
    # Test Groq model
    groq_model = os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant")
    print(f"✅ Groq model: {groq_model}")

def main():
    print("🧪 Wolf AI Chatbot - Complete System Test")
    print("=" * 50)
    
    # Test API configuration first
    test_api_configuration()
    
    # Test authentication
    token = test_signup_login()
    
    if not token:
        print("❌ Authentication failed - cannot continue with chat tests")
        return
    
    # Test chat functionality
    test_chat_with_token(token)
    
    print("\n" + "=" * 50)
    print("🏁 Test complete!")

if __name__ == "__main__":
    main()
