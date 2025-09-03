#!/usr/bin/env python3
"""
Test complex business question to verify advanced capabilities
"""

import requests
import json

def test_complex_question():
    """Test a complex strategic business question"""
    print("🧪 Testing complex business question...")
    
    # Login first
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        login_response = requests.post("http://localhost:8000/api/login", json=login_data)
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.json()}")
            return
            
        token = login_response.json()["token"]
        print("✅ Login successful!")
        
        # Test complex strategic question
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        complex_question = "I'm launching a SaaS product in a competitive market. How should I approach pricing strategy, and what are the key factors for market penetration against established competitors?"
        
        chat_data = {
            "message": complex_question,
            "session_id": "strategic_test"
        }
        
        print(f"📝 Complex Question: {complex_question}")
        
        chat_response = requests.post("http://localhost:8000/api/chat", json=chat_data, headers=headers, timeout=45)
        print(f"Chat Status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            response_text = result["response"]
            print(f"✅ Chat successful!")
            print(f"Response length: {len(response_text)} characters")
            print(f"\\n📋 RESPONSE:")
            print("=" * 60)
            print(response_text)
            print("=" * 60)
            
            # Analyze response quality
            quality_indicators = [
                "strategy", "pricing", "competitive", "market", "penetration",
                "SWOT", "Porter", "ROI", "framework", "analysis"
            ]
            
            found_indicators = [indicator for indicator in quality_indicators if indicator.lower() in response_text.lower()]
            print(f"\\n📊 Quality Analysis:")
            print(f"- Business keywords found: {', '.join(found_indicators)}")
            print(f"- Response quality: {'✅ HIGH - Contains strategic analysis' if len(found_indicators) >= 5 else '⚠️  MEDIUM - Basic response'}")
            
        else:
            print(f"❌ Chat failed: {chat_response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_complex_question()
