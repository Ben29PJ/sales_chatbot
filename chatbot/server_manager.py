#!/usr/bin/env python3
"""
Wolf AI Server Manager - Easy start, stop, and monitoring
"""

import requests
import subprocess
import time
import psutil
import sys
import os
from pathlib import Path

SERVER_URL = "http://localhost:8000"
SERVER_SCRIPT = "fastapi_app_fixed.py"

def find_server_process():
    """Find the server process if it's running"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any(SERVER_SCRIPT in cmd for cmd in proc.info['cmdline']):
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def is_server_running():
    """Check if server is responding"""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Wolf AI Server...")
    
    if is_server_running():
        print("✅ Server is already running!")
        return True
    
    # Kill any existing process
    pid = find_server_process()
    if pid:
        print(f"🔄 Found existing process {pid}, stopping it...")
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            time.sleep(2)
            if proc.is_running():
                proc.kill()
        except:
            pass
    
    # Start new server process
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen([
                sys.executable, SERVER_SCRIPT
            ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix/Linux/Mac
            subprocess.Popen([sys.executable, SERVER_SCRIPT])
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(15):  # Wait up to 15 seconds
            time.sleep(1)
            if is_server_running():
                print("✅ Server started successfully!")
                print(f"🌐 Server running at: {SERVER_URL}")
                print(f"📊 Health check: {SERVER_URL}/health")
                return True
            print(f"   Waiting... ({i+1}/15)")
        
        print("❌ Server failed to start within 15 seconds")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def stop_server():
    """Stop the FastAPI server"""
    print("🛑 Stopping Wolf AI Server...")
    
    # Try graceful shutdown via API first
    try:
        response = requests.post(f"{SERVER_URL}/api/shutdown", timeout=3)
        if response.status_code == 200:
            print("✅ Server stopped gracefully via API")
            return True
    except:
        pass
    
    # Find and terminate process
    pid = find_server_process()
    if pid:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            time.sleep(2)
            
            if proc.is_running():
                proc.kill()
                time.sleep(1)
                
            print(f"✅ Server process {pid} stopped")
            return True
        except Exception as e:
            print(f"❌ Failed to stop process {pid}: {e}")
            return False
    else:
        print("ℹ️ No server process found")
        return True

def restart_server():
    """Restart the server"""
    print("🔄 Restarting Wolf AI Server...")
    stop_server()
    time.sleep(2)
    return start_server()

def server_status():
    """Show server status"""
    print("📊 Wolf AI Server Status")
    print("=" * 40)
    
    # Check if process is running
    pid = find_server_process()
    if pid:
        print(f"🟢 Process: Running (PID: {pid})")
    else:
        print("🔴 Process: Not found")
    
    # Check if server is responding
    if is_server_running():
        print("🟢 Server: Responding")
        try:
            response = requests.get(f"{SERVER_URL}/health")
            health_data = response.json()
            print(f"⏰ Timestamp: {health_data.get('timestamp', 'unknown')}")
        except:
            pass
    else:
        print("🔴 Server: Not responding")
    
    print(f"🌐 URL: {SERVER_URL}")

def interactive_menu():
    """Interactive server management menu"""
    while True:
        print("\n" + "="*50)
        print("🐺 WOLF AI SERVER MANAGER")
        print("="*50)
        print("1. 🚀 Start server")
        print("2. 🛑 Stop server")  
        print("3. 🔄 Restart server")
        print("4. 📊 Check status")
        print("5. 🧪 Run quick test")
        print("6. 📝 View logs")
        print("7. ❌ Exit")
        print()
        
        try:
            choice = input("👉 Choose an option (1-7): ").strip()
            
            if choice == "1":
                start_server()
            elif choice == "2":
                stop_server()
            elif choice == "3":
                restart_server()
            elif choice == "4":
                server_status()
            elif choice == "5":
                quick_test()
            elif choice == "6":
                print("📝 Check the terminal where the server is running for logs")
            elif choice == "7":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def quick_test():
    """Run a quick test on the server"""
    print("🧪 Running quick server test...")
    
    if not is_server_running():
        print("❌ Server is not running. Start it first.")
        return
    
    try:
        # Test health endpoint
        health_response = requests.get(f"{SERVER_URL}/health")
        if health_response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return
        
        print("✅ Quick test completed - server is working!")
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "start":
            start_server()
        elif command == "stop":
            stop_server()
        elif command == "restart":
            restart_server()
        elif command == "status":
            server_status()
        elif command == "test":
            quick_test()
        else:
            print("Usage: python server_manager.py [start|stop|restart|status|test]")
    else:
        interactive_menu()
