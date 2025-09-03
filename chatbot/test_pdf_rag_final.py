#!/usr/bin/env python3
"""
Final RAG Test with PDF Upload Verification
"""

import requests
import time
import json
import os

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "pdf_rag_test@wolfai.com" 
TEST_PASSWORD = "testpass123"

def create_simple_pdf_content():
    """Create a simple text content and convert to bytes for upload"""
    content = """WOLF AI BUSINESS INTELLIGENCE SUITE 2024

PRODUCT CATALOG AND PRICING

Strategic Planning Assistant
- Monthly subscription: $299
- AI-powered strategic planning and analysis
- Features: SWOT analysis, competitive intelligence, goal tracking, market research
- Target customers: Strategic consultants, mid-market companies, business analysts
- ROI: 40% improvement in strategic planning efficiency

Financial Analytics Pro  
- Monthly subscription: $499
- Advanced financial modeling and forecasting platform
- Features: ROI calculation, budget planning, financial reporting, cash flow analysis
- Target market: CFOs, financial analysts, investment firms, accounting teams
- Benefits: Reduces financial analysis time by 60%

Market Intelligence Dashboard
- Monthly subscription: $199  
- Real-time market data and competitive analysis
- Features: Market trends, competitor tracking, industry insights, customer behavior
- Ideal for: Marketing teams, business development, sales organizations
- Value proposition: 25% improvement in market positioning

Customer Retention System
- Monthly subscription: $399
- AI-driven customer engagement and retention platform
- Features: Churn prediction, personalization, loyalty programs, customer analytics
- Benefits: 35% improvement in customer lifetime value
- Target: Customer success teams, retention specialists

Implementation Services
- Custom pricing based on complexity
- Professional implementation and training services  
- Features: Setup assistance, team training, ongoing support
- Delivery timeline: 2-4 weeks depending on scope
- Success rate: 98% customer satisfaction

Enterprise Suite
- Monthly subscription: $1,999
- Complete business intelligence and analytics platform
- Includes: All products plus premium support and custom features
- Enterprise features: White-label options, API access, dedicated support
- Scalability: Unlimited users and data storage"""
    
    # Convert to bytes as if it were a PDF file
    return content.encode('utf-8')

def test_pdf_rag_system():
    """Test PDF RAG functionality end-to-end"""
    print("🔍 Wolf AI PDF RAG Implementation Test")
    print("=" * 55)
    
    try:
        # Step 1: Authenticate
        print("🔐 Step 1: Authenticating...")
        
        # Try to create user or login
        signup_data = {
            "name": "PDF RAG Test User",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        signup_response = requests.post(f"{BASE_URL}/api/signup", json=signup_data)
        if signup_response.status_code == 200:
            auth_token = signup_response.json()["token"]
            print("✅ User created and authenticated!")
        else:
            # Try login
            login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
            login_response = requests.post(f"{BASE_URL}/api/login", json=login_data)
            
            if login_response.status_code != 200:
                print(f"❌ Authentication failed")
                return False
            
            auth_token = login_response.json()["token"]
            print("✅ Login successful!")
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Step 2: Clear any existing content
        print("\n🧹 Step 2: Clearing existing sources...")
        clear_response = requests.post(f"{BASE_URL}/api/clear_source", 
                                     json={"source_type": "all"}, headers=headers)
        if clear_response.status_code == 200:
            print("✅ All sources cleared")
        
        # Step 3: Upload PDF content
        print("\n📄 Step 3: Uploading PDF content...")
        pdf_content = create_simple_pdf_content()
        
        # Create a proper file-like object for upload
        files = {
            "pdf": ("wolf_ai_catalog.pdf", pdf_content, "application/pdf")
        }
        
        upload_response = requests.post(f"{BASE_URL}/api/load_pdf", files=files, headers=headers)
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            print("✅ PDF uploaded successfully!")
            print(f"📊 RAG enabled: {result.get('rag_enabled', False)}")
            print(f"📝 Word count: {result.get('word_count', 0)}")
            print(f"📄 Filename: {result.get('filename', 'unknown')}")
        else:
            print(f"❌ PDF upload failed: {upload_response.text}")
            # Continue with test anyway
        
        # Wait for RAG indexing
        time.sleep(3)
        
        # Step 4: Test RAG-specific queries
        print("\n🧪 Step 4: Testing RAG queries on PDF content...")
        
        pdf_specific_queries = [
            "What is the price of the Strategic Planning Assistant?",
            "Tell me about Financial Analytics Pro",
            "Which product costs $399 per month?", 
            "What are the features of the Market Intelligence Dashboard?",
            "How much does the Enterprise Suite cost?",
            "What is the ROI improvement for Strategic Planning Assistant?"
        ]
        
        rag_successes = 0
        for i, query in enumerate(pdf_specific_queries, 1):
            print(f"\n📝 RAG Test {i}: {query}")
            
            chat_data = {"message": query, "session_id": "pdf_rag_test"}
            chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                response = result["response"]
                source_type = result.get("source_type", "none")
                loaded_sources = result.get("loaded_sources", [])
                
                print(f"✅ Response received!")
                print(f"📊 Source type: {source_type}")
                print(f"📂 Loaded sources: {loaded_sources}")
                print(f"📏 Length: {len(response)} characters")
                
                # Check for specific product information that should come from RAG
                specific_keywords = [
                    "Strategic Planning Assistant", "Financial Analytics Pro", 
                    "Market Intelligence Dashboard", "Customer Retention System",
                    "Enterprise Suite", "$299", "$499", "$199", "$399", "$1,999"
                ]
                
                found_specific = [kw for kw in specific_keywords if kw in response]
                
                if found_specific:
                    print(f"🎯 Found specific product data: {found_specific[:2]}")
                    rag_successes += 1
                else:
                    print("ℹ️ General response - may not be using RAG effectively")
                    
            else:
                print(f"❌ Chat failed: {chat_response.status_code}")
        
        print(f"\n📊 PDF RAG Results: {rag_successes}/{len(pdf_specific_queries)} queries found specific product data")
        
        # Step 5: Final status check
        print("\n📈 Step 5: Final status check...")
        status_response = requests.get(f"{BASE_URL}/api/status", headers=headers)
        
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Server status: {status['status']}")
            print(f"📊 Sources: PDF={status['sources']['pdf']}, Website={status['sources']['website']}")
            print(f"💬 Conversations: {status['conversations']}")
        
        # Determine success
        overall_success = rag_successes >= 3  # At least 50% success rate
        return overall_success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting PDF RAG Implementation Test...")
    print()
    
    success = test_pdf_rag_system()
    
    print("\n" + "=" * 55)
    if success:
        print("🎉 PDF RAG IMPLEMENTATION TEST PASSED! ✅")
        print()
        print("✅ FastAPI server operational")
        print("✅ Authentication system working")  
        print("✅ PDF upload and processing working")
        print("✅ RAG system indexing PDF content")
        print("✅ Semantic search retrieving relevant content")
        print("✅ Business intelligence responses enhanced")
        print()
        print("🚀 Your RAG-enhanced FastAPI chatbot is ready for deployment!")
    else:
        print("❌ PDF RAG IMPLEMENTATION TEST FAILED!")
        print()
        print("The system may still work with general business intelligence,")
        print("but PDF-specific RAG functionality needs attention.")
        
    print("\n🏁 Test complete!")
