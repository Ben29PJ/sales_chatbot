#!/usr/bin/env python3
"""Test the exact chat functionality that's failing"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_chat_with_actual_params():
    """Test chat with the exact parameters used in the app"""
    try:
        # Get configuration
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant").strip()
        
        print(f"🧪 Testing with:")
        print(f"  - API Key: {api_key[:20]}...")
        print(f"  - Model: {model}")
        
        # Initialize client
        client = Groq(api_key=api_key)
        
        # Test with simple system message first
        simple_messages = [
            {"role": "system", "content": "You are Wolf AI, a helpful business assistant."},
            {"role": "user", "content": "hello"}
        ]
        
        print("\n🧪 Testing simple chat...")
        try:
            response = client.chat.completions.create(
                messages=simple_messages,
                model=model,
                temperature=0.7,
                max_tokens=500
            )
            print("✅ Simple chat works!")
            print(f"📝 Response: {response.choices[0].message.content[:100]}...")
        except Exception as e:
            print(f"❌ Simple chat failed: {e}")
            return False
        
        # Test with complex system message
        complex_system = """You are Wolf AI, an elite MBA-level business intelligence consultant and sales strategist. You possess:

🎯 EXPERT COMPETENCIES:
- Strategic Business Analysis: McKinsey-level strategic thinking
- Financial Modeling: Advanced ROI, NPV, IRR calculations
- Market Intelligence: Porter's Five Forces, competitive analysis
- Sales Excellence: Consultative selling, solution architecture

📊 CURRENT SESSION INTELLIGENCE:
- Question Complexity Score: 3/20
- Question Categories: General business inquiry
- Analysis Required: No - Direct response appropriate
- Content Available: No - Using general business expertise

🔥 RESPONSE MANDATE:
- NEVER refuse to answer business questions due to lack of specific data
- ALWAYS provide valuable insights using business knowledge and frameworks
- MAINTAIN professional consultant-level quality in all responses"""

        complex_messages = [
            {"role": "system", "content": complex_system},
            {"role": "user", "content": "What are the key factors for successful digital transformation in retail?"}
        ]
        
        print("\n🧪 Testing complex business question...")
        try:
            response = client.chat.completions.create(
                messages=complex_messages,
                model=model,
                temperature=0.7,
                max_tokens=800,
                top_p=0.9
            )
            print("✅ Complex chat works!")
            print(f"📝 Response length: {len(response.choices[0].message.content)} characters")
            print(f"📝 Response preview: {response.choices[0].message.content[:200]}...")
            return True
        except Exception as e:
            print(f"❌ Complex chat failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Chat Function Test")
    print("=" * 30)
    
    success = test_chat_with_actual_params()
    
    if success:
        print("\n✅ Chat functionality is working correctly!")
        print("The issue might be in the FastAPI integration or error handling.")
    else:
        print("\n❌ Chat functionality test failed.")
        print("There's an issue with the Groq API configuration.")
