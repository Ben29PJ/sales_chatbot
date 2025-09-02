#!/usr/bin/env python3
"""
Test script to verify FastAPI endpoints are working correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, headers=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        print(f"✅ {method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
        return response
    except Exception as e:
        print(f"❌ {method} {endpoint}: Error - {str(e)}")
        return None

def main():
    print("🧪 Testing Wolf AI FastAPI Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint:")
    test_endpoint("GET", "/health")
    
    # Test signup endpoint
    print("\n2. Testing Signup Endpoint:")
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    }
    signup_response = test_endpoint("POST", "/api/signup", signup_data)
    
    # If signup successful, get token for authenticated tests
    token = None
    if signup_response and signup_response.status_code == 200:
        token = signup_response.json().get("token")
        print(f"   Token received: {token[:50]}..." if token else "No token received")
    
    # Test login endpoint
    print("\n3. Testing Login Endpoint:")
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    login_response = test_endpoint("POST", "/api/login", login_data)
    
    # Update token from login if needed
    if login_response and login_response.status_code == 200:
        token = login_response.json().get("token")
    
    # Test authenticated endpoints
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n4. Testing Status Endpoint (Authenticated):")
        test_endpoint("GET", "/api/status", headers=headers)
        
        print("\n5. Testing Chat Endpoint (should fail without sources):")
        chat_data = {"message": "Hello", "session_id": "test"}
        test_endpoint("POST", "/api/chat", chat_data, headers)
        
        print("\n6. Testing Clear Source Endpoint:")
        clear_data = {"source_type": "all"}
        test_endpoint("POST", "/api/clear_source", clear_data, headers)
        
    else:
        print("\n❌ No token available for authenticated tests")
    
    print("\n" + "=" * 50)
    print("🎯 API Testing Complete!")
    print(f"FastAPI Server: {BASE_URL}")
    print(f"API Documentation: {BASE_URL}/docs")

if __name__ == "__main__":
    main()
