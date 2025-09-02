#!/usr/bin/env python3
"""
Wolf AI - Setup Verification Script
Quick verification that everything is configured correctly
"""

import os
import sys
from pathlib import Path
import subprocess

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"   ✅ {description}")
        return True
    else:
        print(f"   ❌ {description} - Missing: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if Path(dirpath).exists():
        print(f"   ✅ {description}")
        return True
    else:
        print(f"   ❌ {description} - Missing: {dirpath}")
        return False

def main():
    print("🐺 Wolf AI - Setup Verification")
    print("=" * 40)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    print("\n📁 Checking Project Structure...")
    all_good = True
    
    # Check main files
    all_good &= check_file_exists("fastapi_app.py", "FastAPI Backend")
    all_good &= check_file_exists("app.py", "Flask Backend (fallback)")
    all_good &= check_file_exists("requirements.txt", "Python Requirements")
    all_good &= check_file_exists("README.md", "Documentation")
    
    # Check React frontend
    all_good &= check_directory_exists("react-frontend", "React Frontend Directory")
    all_good &= check_file_exists("react-frontend/package.json", "Frontend Package Config")
    all_good &= check_file_exists("react-frontend/src/App.jsx", "React App Component")
    all_good &= check_file_exists("react-frontend/src/components/HomePage.jsx", "Home Page Component")
    all_good &= check_file_exists("react-frontend/src/components/ChatDashboard.jsx", "Chat Dashboard")
    
    # Check build output
    all_good &= check_directory_exists("static/dist", "React Build Directory")
    all_good &= check_file_exists("static/dist/index.html", "Built Frontend HTML")
    
    print("\\n🔧 Checking Configuration...")
    
    # Check if Groq API key is set
    if "gsk_" in open("fastapi_app.py").read():
        print("   ✅ Groq API Key configured")
    else:
        print("   ❌ Groq API Key not found")
        all_good = False
    
    # Check if React build points to correct API
    api_config = open("react-frontend/src/services/api.js").read()
    if "localhost:8000" in api_config:
        print("   ✅ Frontend API configuration")
    else:
        print("   ❌ Frontend API not pointing to localhost:8000")
        all_good = False
    
    print("\\n🚀 Quick Start Commands:")
    print("-" * 30)
    
    if all_good:
        print("✅ All files found! Ready to launch.")
        print("\\nTo start Wolf AI:")
        print("   Option 1: python setup_and_run.py")
        print("   Option 2: start_wolfai.bat")
        print("   Option 3: python fastapi_app.py")
        
        print("\\n🌐 Once running, visit:")
        print("   🏠 http://localhost:8000 (Home Page)")
        print("   🔐 http://localhost:8000/login")
        print("   📝 http://localhost:8000/signup")
        
    else:
        print("❌ Some files are missing. Please check the project setup.")
        print("\\nMissing files need to be created or the build needs to be run.")
        
        # Suggest fixes
        if not Path("static/dist/index.html").exists():
            print("\\n🔨 To fix missing build:")
            print("   cd react-frontend")
            print("   npm install")
            print("   npm run build")
    
    print("\\n" + "=" * 40)
    print("Verification complete!")

if __name__ == "__main__":
    main()
