#!/usr/bin/env python3
"""
Wolf AI - Complete Setup and Run Script
This script handles the complete setup and startup of Wolf AI
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def print_banner():
    print("""
🐺 Wolf AI - Premium Sales Assistant
====================================
Setup and Launch Script
""")

def check_python():
    """Check Python version"""
    print("🐍 Checking Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_node():
    """Check Node.js"""
    print("📦 Checking Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Node.js {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    print("   ❌ Node.js not found - Install from https://nodejs.org/")
    return False

def install_python_deps():
    """Install Python dependencies"""
    print("📚 Installing Python dependencies...")
    packages = [
        "fastapi", "uvicorn[standard]", "groq", "pymongo", 
        "PyPDF2", "requests", "beautifulsoup4", "python-multipart", 
        "PyJWT", "pydantic[email]", "flask", "flask-cors", "werkzeug"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True, check=True)
            print(f"   ✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Error installing {package}: {e}")
            return False
    
    return True

def install_node_deps():
    """Install Node.js dependencies"""
    print("🎨 Installing Frontend dependencies...")
    frontend_dir = Path("react-frontend")
    
    if not frontend_dir.exists():
        print("   ❌ Frontend directory not found")
        return False
    
    try:
        os.chdir(frontend_dir)
        result = subprocess.run(["npm", "install"], check=True)
        print("   ✅ Frontend dependencies installed")
        os.chdir("..")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Failed to install frontend dependencies")
        os.chdir("..")
        return False

def build_frontend():
    """Build React frontend"""
    print("🏗️  Building React frontend...")
    frontend_dir = Path("react-frontend")
    
    try:
        os.chdir(frontend_dir)
        result = subprocess.run(["npm", "run", "build"], check=True, capture_output=True, text=True)
        print("   ✅ Frontend built successfully")
        os.chdir("..")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Frontend build failed: {e}")
        print(f"   Error output: {e.stderr}")
        os.chdir("..")
        return False

def check_mongodb():
    """Check if MongoDB is accessible"""
    print("🍃 Checking MongoDB...")
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("   ✅ MongoDB is running")
        return True
    except Exception:
        print("   ⚠️  MongoDB not running - Install and start MongoDB")
        print("   Download from: https://www.mongodb.com/try/download/community")
        return False

def start_backend():
    """Start FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    try:
        # Check if static files exist
        static_dir = Path("static/dist")
        if not static_dir.exists():
            print("   ⚠️  React build not found - building frontend first...")
            if not build_frontend():
                return False
        
        print("   Starting server on http://localhost:8000")
        print("   Press Ctrl+C to stop")
        print("-" * 50)
        
        # Start FastAPI server
        subprocess.run([sys.executable, "fastapi_app.py"])
        
    except KeyboardInterrupt:
        print("\\n🛑 Server stopped by user")
    except Exception as e:
        print(f"   ❌ Failed to start backend: {e}")
        return False

def main():
    """Main setup and run function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check prerequisites
    if not check_python():
        return
    
    if not check_node():
        return
    
    # Setup phase
    print("\\n🔧 SETUP PHASE")
    print("=" * 30)
    
    if not install_python_deps():
        print("❌ Python dependency installation failed")
        return
    
    if not install_node_deps():
        print("❌ Frontend dependency installation failed")
        return
    
    if not build_frontend():
        print("❌ Frontend build failed")
        return
    
    check_mongodb()
    
    # Launch phase
    print("\\n🚀 LAUNCH PHASE")
    print("=" * 30)
    print("Starting Wolf AI application...")
    print("\\nAccess your application at:")
    print("🏠 Home Page: http://localhost:8000")
    print("🔐 Login: http://localhost:8000/login")
    print("📝 Signup: http://localhost:8000/signup")
    print("💬 Dashboard: http://localhost:8000/dashboard")
    print("🩺 Health: http://localhost:8000/health")
    print("")
    
    start_backend()

if __name__ == "__main__":
    main()
