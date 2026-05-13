#!/usr/bin/env python3
"""
Frontend Startup Script
HDFC Mutual Fund RAG System
"""

import os
import sys
from pathlib import Path
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS support"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.end_headers()

def find_free_port(start_port=8001):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def check_frontend_files():
    """Check if frontend files exist"""
    
    frontend_dir = Path(__file__).parent / "frontend"
    required_files = [
        "index.html",
        "src/utils/constants.js",
        "src/utils/formatters.js",
        "src/services/validation.js",
        "src/services/api.js",
        "src/components/SourceCitation.js",
        "src/components/MessageDisplay.js",
        "src/components/ChatInterface.js",
        "src/components/Disclaimer.js",
        "src/app.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = frontend_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    return missing_files

def check_backend_connection():
    """Check if backend is running"""
    
    try:
        import requests
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_frontend_server():
    """Start the frontend development server"""
    
    print("HDFC Mutual Fund RAG Frontend")
    print("=" * 50)
    
    # Check frontend files
    print("Checking frontend files...")
    missing_files = check_frontend_files()
    if missing_files:
        print(f"ERROR: Missing frontend files: {missing_files}")
        print("Please ensure all frontend files are present.")
        return 1
    
    print("[SUCCESS] All frontend files present")
    
    # Check backend connection
    print("\nChecking backend connection...")
    backend_running = check_backend_connection()
    if backend_running:
        print("[SUCCESS] Backend is running on http://localhost:8000")
    else:
        print("[WARNING] Backend is not running. Some features may not work.")
        print("  Start the backend with: python start_backend.py")
    
    # Find free port
    port = find_free_port()
    if port is None:
        print("ERROR: Could not find a free port")
        return 1
    
    print(f"[SUCCESS] Found free port: {port}")
    
    # Change to frontend directory
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    # Start server
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    
    print(f"\nStarting frontend server...")
    print(f"Frontend URL: http://localhost:{port}")
    print(f"Backend URL: http://localhost:8000")
    print(f"API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(1)
        webbrowser.open(f'http://localhost:{port}')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 0
    except Exception as e:
        print(f"\nServer error: {e}")
        return 1
    finally:
        httpd.server_close()
    
    return 0

def main():
    """Main function"""
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        return 1
    
    return start_frontend_server()

if __name__ == "__main__":
    sys.exit(main())
