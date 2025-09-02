#!/usr/bin/env python3
"""
Server Management Script for Wolf AI FastAPI Backend
"""
import subprocess
import sys
import time
import signal
import psutil
import os
from pathlib import Path

def find_python_processes_on_port(port=8000):
    """Find Python processes using the specified port"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if f':{port}' in cmdline or 'fastapi' in cmdline.lower() or 'uvicorn' in cmdline.lower():
                    processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def kill_existing_servers():
    """Kill any existing FastAPI/Python servers"""
    print("🔍 Checking for existing server processes...")
    
    processes = find_python_processes_on_port(8000)
    
    if processes:
        print(f"Found {len(processes)} existing server process(es). Terminating...")
        for proc in processes:
            try:
                print(f"  → Killing process {proc.pid} ({proc.name()})")
                proc.terminate()
                proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                try:
                    proc.kill()
                except psutil.NoSuchProcess:
                    pass
        print("✅ Existing processes terminated.")
        time.sleep(2)  # Give processes time to fully terminate
    else:
        print("✅ No existing server processes found.")

def start_server():
    """Start the FastAPI server"""
    script_dir = Path(__file__).parent
    app_file = script_dir / "fastapi_app_fixed.py"
    
    if not app_file.exists():
        print(f"❌ Error: {app_file} not found!")
        return False
    
    print("🚀 Starting Wolf AI FastAPI server...")
    print("📍 URL: http://localhost:8000")
    print("⚡ Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to the script directory
        os.chdir(script_dir)
        
        # Start the server
        result = subprocess.run([
            sys.executable, 
            str(app_file)
        ], check=True)
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🐺 Wolf AI Server Manager")
    print("=" * 30)
    
    # Kill any existing servers first
    kill_existing_servers()
    
    # Start the new server
    success = start_server()
    
    if not success:
        print("\n❌ Server failed to start properly.")
        sys.exit(1)

if __name__ == "__main__":
    main()
