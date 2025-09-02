#!/usr/bin/env python3
"""
Test script for Wolf AI audio functionality
"""

import requests
import io
import wave
import numpy as np
from pathlib import Path
import tempfile
import os

def create_test_audio():
    """Create a simple test audio file"""
    # Generate a simple sine wave for testing
    sample_rate = 44100
    duration = 2  # seconds
    frequency = 440  # Hz (A note)
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Create temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    
    with wave.open(temp_file.name, 'wb') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    return temp_file.name

def test_audio_api():
    """Test the audio API endpoints"""
    print("🧪 Testing Wolf AI Audio Functionality")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI server is running")
            print(f"   Response: {response.json()}")
        else:
            print("❌ FastAPI server health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to FastAPI server: {e}")
        print("   Make sure to run: python fastapi_app.py")
        return False
    
    # Test 2: Audio endpoint (requires authentication)
    print("\n🎤 Audio endpoints require authentication")
    print("   To test audio functionality:")
    print("   1. Start the FastAPI server: python fastapi_app.py")
    print("   2. Start the React frontend: cd react-frontend && npm run dev")
    print("   3. Open browser and sign up/login")
    print("   4. Use the voice recording button in the chat interface")
    
    # Test 3: Create sample audio file for manual testing
    try:
        audio_file = create_test_audio()
        print(f"\n📁 Created test audio file: {audio_file}")
        print("   You can use this file to manually test the API")
        
        # Clean up
        os.unlink(audio_file)
        print("   ✅ Test audio file cleaned up")
        
    except Exception as e:
        print(f"❌ Failed to create test audio: {e}")
    
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking Dependencies")
    print("-" * 30)
    
    required_packages = ['groq', 'fastapi', 'uvicorn', 'pymongo', 'PyPDF2', 'requests', 'beautifulsoup4']
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').lower())
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Install with: pip install {package}")

def main():
    """Main test function"""
    print("🐺 Wolf AI - Audio Functionality Test")
    print("=" * 50)
    
    check_dependencies()
    test_audio_api()
    
    print("\n🚀 Test Complete!")
    print("\nTo start the application:")
    print("1. Backend:  python fastapi_app.py")
    print("2. Frontend: cd react-frontend && npm run dev")

if __name__ == "__main__":
    main()
