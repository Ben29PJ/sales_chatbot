#!/usr/bin/env python3
"""
Simple test for a single chat request
"""

import requests
import json

def test_single_chat():
    """Test a single chat request"""
    print("🧪 Testing single chat request...")
    
    # First login to get token
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        login_response = requests.post("http://localhost:8000/api/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.json()}")
            return
            
        token = login_response.json()["token"]
        print("✅ Login successful!")
        
        # Test chat
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        chat_data = {
            "message": "What is ROI and how do I calculate it?",
            "session_id": "test"
        }
        
        chat_response = requests.post("http://localhost:8000/api/chat", json=chat_data, headers=headers, timeout=30)
        print(f"Chat Status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            response_text = result["response"]
            print(f"✅ Chat successful!")
            print(f"Response length: {len(response_text)} characters")
            print(f"Response: {response_text}")
            
            # Check if it's a fallback response
            if "high demand" in response_text.lower() or "technical difficulties" in response_text.lower():
                print("⚠️  Still getting fallback response")
            else:
                print("✅ Got proper AI response!")
        else:
            print(f"❌ Chat failed: {chat_response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_single_chat()
