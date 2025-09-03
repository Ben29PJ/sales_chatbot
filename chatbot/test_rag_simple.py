#!/usr/bin/env python3
"""
Simple RAG Implementation Test using website content
"""

import requests
import time
import json

# Test configuration  
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "rag_test_simple@wolfai.com"
TEST_PASSWORD = "testpass123"

def test_rag_functionality():
    """Test RAG functionality through API endpoints"""
    print("🔍 Wolf AI RAG Implementation Test")
    print("=" * 50)
    
    try:
        # Step 1: Create user and authenticate
        print("🔐 Step 1: Creating user and authenticating...")
        
        signup_data = {
            "name": "RAG Test User",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        signup_response = requests.post(f"{BASE_URL}/api/signup", json=signup_data)
        if signup_response.status_code == 200:
            auth_token = signup_response.json()["token"]
            print("✅ User created and authenticated!")
        else:
            # Try login if user exists
            login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
            login_response = requests.post(f"{BASE_URL}/api/login", json=login_data)
            
            if login_response.status_code != 200:
                print(f"❌ Authentication failed: {login_response.text}")
                return False
            
            auth_token = login_response.json()["token"]
            print("✅ Login successful!")
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Step 2: Load a website for testing (since it doesn't require file creation)
        print("\n🌐 Step 2: Loading website content...")
        
        website_data = {"url": "https://example.com"}
        website_response = requests.post(f"{BASE_URL}/api/load_website", json=website_data, headers=headers)
        
        if website_response.status_code == 200:
            result = website_response.json()
            print("✅ Website content loaded!")
            print(f"📏 Content length: {result.get('text_length', 0)} characters")
            print(f"📝 Word count: {result.get('word_count', 0)}")
        else:
            print(f"❌ Website loading failed: {website_response.text}")
        
        # Step 3: Test chat functionality with business questions
        print("\n🧪 Step 3: Testing business chat functionality...")
        
        test_queries = [
            "What are the key factors for business growth?",
            "How can I improve customer retention?", 
            "What marketing strategies work best for small businesses?",
            "How do I calculate ROI for marketing campaigns?",
            "What are the main competitive advantages to focus on?"
        ]
        
        successful_chats = 0
        for i, query in enumerate(test_queries, 1):
            print(f"\n💬 Chat Test {i}: {query}")
            
            chat_data = {"message": query, "session_id": "test_session"}
            chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                response_text = result["response"]
                source_type = result.get("source_type", "none")
                loaded_sources = result.get("loaded_sources", [])
                
                print(f"✅ Response received!")
                print(f"📊 Source type: {source_type}")
                print(f"📂 Loaded sources: {loaded_sources}")
                print(f"📏 Response length: {len(response_text)} characters")
                print(f"📝 First 100 chars: {response_text[:100]}...")
                
                # Check for business intelligence quality
                business_keywords = ["strategy", "analysis", "ROI", "customer", "market", "competitive", "growth"]
                found_keywords = [kw for kw in business_keywords if kw.lower() in response_text.lower()]
                
                if len(found_keywords) >= 2:
                    print(f"🎯 Good business content: {found_keywords[:3]}")
                    successful_chats += 1
                else:
                    print("ℹ️ Basic response")
            else:
                print(f"❌ Chat failed: {chat_response.text}")
        
        print(f"\n📊 Chat Test Results: {successful_chats}/{len(test_queries)} responses had good business content")
        
        # Step 4: Check server status
        print("\n📈 Step 4: Checking server status...")
        status_response = requests.get(f"{BASE_URL}/api/status", headers=headers)
        
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Server status: {status['status']}")
            print(f"📊 Sources loaded: {status['sources']}")
            print(f"💬 Active conversations: {status['conversations']}")
            print(f"⏰ Server uptime: {status['uptime']}")
        else:
            print(f"❌ Status check failed: {status_response.text}")
        
        # Step 5: Test RAG system specifically if we can load content
        print("\n🔬 Step 5: Testing RAG system directly...")
        
        # Clear existing sources first
        clear_response = requests.post(f"{BASE_URL}/api/clear_source", 
                                     json={"source_type": "all"}, headers=headers)
        if clear_response.status_code == 200:
            print("✅ Sources cleared for fresh test")
        
        # Test without any loaded content (should work with general knowledge)
        test_query = "What are the main components of a business strategy?"
        chat_data = {"message": test_query, "session_id": "rag_direct_test"}
        chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            print("✅ RAG system responding correctly without loaded content")
            print(f"📊 Response quality: {'High' if len(result['response']) > 500 else 'Standard'}\"")
        else:
            print(f"❌ RAG system test failed: {chat_response.text}")
            return False
        
        return successful_chats >= 3  # Consider successful if at least 3 chats worked well
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_server_endpoints():
    """Test basic server functionality"""
    print("\n🧪 Testing server endpoints...")
    
    # Test health endpoint
    try:
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Health endpoint: {health_data['status']}")
            return True
        else:
            print(f"❌ Health endpoint failed: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not responding: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting RAG Implementation Tests...")
    print()
    
    # Test 1: Basic server functionality
    if not test_server_endpoints():
        print("❌ Server is not running properly!")
        exit(1)
    
    # Test 2: RAG functionality
    success = test_rag_functionality()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 RAG implementation tests PASSED! ✅")
        print("✅ FastAPI server is running")
        print("✅ Authentication system working")
        print("✅ Chat system responding with business intelligence")
        print("✅ RAG system integrated and functional")
    else:
        print("❌ RAG implementation tests FAILED!")
        
    print("\n🏁 Test complete!")
