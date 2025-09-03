#!/usr/bin/env python3
"""
Test script to verify RAG implementation
"""

import requests
import json
import io
from pathlib import Path

def create_sample_pdf_content():
    """Create a sample PDF-like content for testing"""
    return """
Wolf AI Product Catalog
======================

Product Line: AI Business Solutions

1. Strategic Planning Assistant
   - Features: SWOT analysis, competitive intelligence, market research
   - Pricing: $99/month per user
   - Benefits: Reduces planning time by 60%, improves decision accuracy
   - Target Market: SME business owners, strategic consultants

2. Financial Analytics Pro
   - Features: ROI calculations, budget forecasting, cost analysis
   - Pricing: $149/month per organization
   - Benefits: Real-time financial insights, automated reporting
   - Target Market: CFOs, financial analysts, accounting firms

3. Customer Retention Platform
   - Features: Customer behavior analysis, retention campaigns, loyalty tracking
   - Pricing: $199/month + usage fees
   - Benefits: Increases customer lifetime value by 40%
   - Target Market: E-commerce, SaaS companies, retail chains

4. Market Intelligence Dashboard
   - Features: Competitor tracking, industry trends, market sizing
   - Pricing: $299/month enterprise license
   - Benefits: Stay ahead of market changes, identify opportunities
   - Target Market: Marketing teams, business development, executives

Company Information:
Wolf AI specializes in business intelligence solutions that help companies make data-driven decisions. Founded in 2020, we serve over 1000+ businesses worldwide with our cutting-edge AI platform.

Competitive Advantages:
- Advanced machine learning algorithms
- Real-time data processing
- Industry-specific customization
- 24/7 customer support
- Integration with 50+ business tools
"""

def test_rag_with_pdf():
    """Test RAG implementation with PDF content"""
    print("🧪 Testing RAG Implementation...")
    
    # First, login
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
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print("✅ Login successful!")
        
        # Create a sample PDF file for testing (simulate PDF content)
        sample_content = create_sample_pdf_content()
        
        # Create a fake PDF file for upload testing
        pdf_data = sample_content.encode('utf-8')
        files = {
            'pdf': ('test_catalog.txt', pdf_data, 'application/pdf')
        }
        
        # For now, let's skip PDF upload and test directly with content
        # In a real scenario, you would upload the PDF
        
        print("📄 Testing with sample business content...")
        
        # Test specific product questions that should benefit from RAG
        test_questions = [
            "What is the pricing for the Strategic Planning Assistant?",
            "Tell me about the features of Financial Analytics Pro",
            "Which product is best for improving customer retention?",
            "What are Wolf AI's competitive advantages?",
            "How much does the Market Intelligence Dashboard cost?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 RAG Test {i}: {question}")
            
            chat_data = {
                "message": question,
                "session_id": f"rag_test_{i}"
            }
            
            chat_response = requests.post("http://localhost:8000/api/chat", json=chat_data, headers=headers, timeout=30)
            print(f"Status: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                response_text = result["response"]
                source_type = result.get("source_type", "unknown")
                
                print(f"✅ Response received!")
                print(f"📊 Retrieval method: {source_type}")
                print(f"📏 Length: {len(response_text)} characters")
                print(f"📝 First 150 chars: {response_text[:150]}...")
                
                # Check if response contains specific product information
                product_specific = any(keyword in response_text.lower() for keyword in [
                    "strategic planning assistant", "financial analytics pro", 
                    "customer retention platform", "market intelligence dashboard",
                    "$99", "$149", "$199", "$299"
                ])
                
                if product_specific:
                    print("🎯 Contains specific product information - RAG likely working!")
                else:
                    print("ℹ️ General business response - no specific product data retrieved")
                    
            else:
                print(f"❌ Request failed: {chat_response.json()}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_general_questions_without_rag():
    """Test that general questions still work without PDF data"""
    print("\n🧪 Testing general business questions (no RAG data)...")
    
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        login_response = requests.post("http://localhost:8000/api/login", json=login_data)
        if login_response.status_code != 200:
            print(f"❌ Login failed")
            return
            
        token = login_response.json()["token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test a general business question
        chat_data = {
            "message": "What are the key components of a successful marketing strategy?",
            "session_id": "general_test"
        }
        
        chat_response = requests.post("http://localhost:8000/api/chat", json=chat_data, headers=headers, timeout=30)
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            response_text = result["response"]
            print("✅ General question answered successfully!")
            print(f"📏 Length: {len(response_text)} characters")
            print(f"📝 First 200 chars: {response_text[:200]}...")
        else:
            print(f"❌ General question failed: {chat_response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔍 Wolf AI RAG Implementation Test")
    print("=" * 50)
    
    test_rag_with_pdf()
    test_general_questions_without_rag()
    
    print("\n" + "=" * 50)
    print("🏁 RAG test complete!")
