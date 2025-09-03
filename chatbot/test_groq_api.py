#!/usr/bin/env python3
"""Test Groq API connectivity and model availability"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_api():
    """Test Groq API connection and model availability"""
    try:
        # Get API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ Error: GROQ_API_KEY not found in environment variables")
            return False
        
        print(f"✅ API Key found: {api_key[:20]}...")
        
        # Initialize client
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized successfully")
        
        # Test available models
        print("\n🔍 Testing available models...")
        try:
            models = client.models.list()
            print(f"✅ Found {len(models.data)} available models:")
            for model in models.data[:10]:  # Show first 10 models
                print(f"  - {model.id}")
        except Exception as e:
            print(f"⚠️  Could not list models: {e}")
        
        # Test chat completion
        print("\n🧪 Testing chat completion...")
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful business assistant."},
                    {"role": "user", "content": "Hello, can you help me with business strategy?"}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=100
            )
            
            response = chat_completion.choices[0].message.content
            print("✅ Chat completion successful!")
            print(f"📝 Response: {response[:100]}...")
            return True
            
        except Exception as e:
            print(f"❌ Chat completion failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error initializing Groq client: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Groq API Connectivity Test")
    print("=" * 30)
    
    success = test_groq_api()
    
    if success:
        print("\n✅ All tests passed! Groq API is working correctly.")
    else:
        print("\n❌ API test failed. Please check your configuration.")
