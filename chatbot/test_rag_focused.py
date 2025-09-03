#!/usr/bin/env python3
"""
Enhanced RAG Implementation Test with actual PDF content
"""

import requests
import time
from io import BytesIO
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "rag_test@wolfai.com"
TEST_PASSWORD = "testpass123"

def create_simple_text_file():
    """Create a simple text file that can be converted to PDF-like content"""
    content = """WOLF AI PRODUCT CATALOG 2024

Strategic Planning Assistant - $299/month
AI-powered strategic planning tool with market analysis
Features: SWOT analysis, competitive intelligence, goal tracking
Perfect for: Mid-market companies, strategic consultants

Financial Analytics Pro - $499/month
Advanced financial modeling and forecasting platform
Features: ROI calculation, budget planning, financial reporting
Target market: CFOs, financial analysts, investment firms

Market Intelligence Dashboard - $199/month
Real-time market data and competitive analysis
Features: Market trends, competitor tracking, industry insights
Ideal for: Marketing teams, business development

Customer Retention System - $399/month
AI-driven customer engagement and retention platform
Features: Churn prediction, personalization, loyalty programs
Benefits: 35% improvement in customer lifetime value

Implementation Services - Custom pricing
Professional implementation and training services
Features: Setup assistance, team training, ongoing support
Delivery: 2-4 weeks depending on complexity

Enterprise Suite - $1,999/month
Complete business intelligence and analytics platform
Includes all products plus premium support
Custom features: White-label options, API access, dedicated support"""
    
    # Write to a temporary file that will be used as text content
    with open("test_catalog.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    return "test_catalog.txt", content

def test_rag_with_actual_pdf():
    """Test RAG implementation with actual PDF upload"""
    print("🔍 Wolf AI RAG Implementation Test - With Actual PDF")
    print("=" * 60)
    
    try:
        # Step 1: Create user and login
        print("🔐 Step 1: Creating test user and authenticating...")
        
        # First create the user
        signup_data = {
            "name": "RAG Test User",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        signup_response = requests.post(f"{BASE_URL}/api/signup", json=signup_data)
        if signup_response.status_code == 200:
            # Use token from signup
            auth_token = signup_response.json()["token"]
            print("✅ User created and authenticated!")
        else:
            # User might already exist, try login
            login_data = {
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
            
            login_response = requests.post(f"{BASE_URL}/api/login", json=login_data)
            if login_response.status_code != 200:
                print(f"❌ Authentication failed: {login_response.text}")
                return False
            
            auth_token = login_response.json()["token"]
            print("✅ Login successful!")
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Step 2: Create and upload PDF
        print("\n📄 Step 2: Creating and uploading test PDF...")
        pdf_buffer = create_test_pdf_content()
        
        files = {"pdf": ("wolf_ai_catalog.pdf", pdf_buffer, "application/pdf")}
        upload_response = requests.post(f"{BASE_URL}/api/load_pdf", files=files, headers=headers)
        
        if upload_response.status_code != 200:
            print(f"❌ PDF upload failed: {upload_response.text}")
            return False
            
        upload_result = upload_response.json()
        print(f"✅ PDF uploaded successfully!")
        print(f"📊 RAG enabled: {upload_result.get('rag_enabled', False)}")
        print(f"📝 Word count: {upload_result.get('word_count', 0)}")
        
        # Wait for RAG indexing
        time.sleep(3)
        
        # Step 3: Test RAG queries
        print("\n🧪 Step 3: Testing RAG queries...")
        
        test_queries = [
            "What is the pricing for the Strategic Planning Assistant?",
            "Tell me about Financial Analytics Pro features",
            "Which product costs $399 per month?",
            "What are the benefits of the Customer Retention System?",
            "How much does the Market Intelligence Dashboard cost?"
        ]
        
        successful_tests = 0
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 RAG Test {i}: {query}")
            
            chat_data = {"message": query, "session_id": "rag_test"}
            chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
            
            if chat_response.status_code != 200:
                print(f"❌ Chat failed: {chat_response.text}")
                continue
                
            result = chat_response.json()
            response_text = result["response"]
            retrieval_method = result.get("source_type", "none")
            
            print(f"✅ Response received!")
            print(f"📊 Retrieval method: {retrieval_method}")
            print(f"📏 Length: {len(response_text)} characters")
            print(f"📝 First 150 chars: {response_text[:150]}...")
            
            # Check if response contains specific product information
            product_keywords = ["Strategic Planning Assistant", "Financial Analytics Pro", 
                              "Market Intelligence Dashboard", "Customer Retention System",
                              "$299", "$499", "$199", "$399"]
            
            found_products = [kw for kw in product_keywords if kw.lower() in response_text.lower()]
            
            if found_products:
                print(f"🎯 Found product-specific info: {found_products}")
                successful_tests += 1
            else:
                print("ℹ️ General business response - no specific product data retrieved")
        
        print(f"\n📊 RAG Test Results: {successful_tests}/{len(test_queries)} tests found specific product info")
        
        # Step 4: Test status endpoint
        print("\n📈 Step 4: Checking server status...")
        status_response = requests.get(f"{BASE_URL}/api/status", headers=headers)
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Server status: {status['status']}")
            print(f"📊 Sources loaded: {status['sources']}")
            print(f"💬 Active conversations: {status['conversations']}")
        
        return successful_tests > 0
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_rag_with_actual_pdf()
    if success:
        print("\n🎉 RAG implementation test PASSED! ✅")
    else:
        print("\n❌ RAG implementation test FAILED!")
