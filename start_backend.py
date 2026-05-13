#!/usr/bin/env python3
"""
Backend API Startup Script
HDFC Mutual Fund RAG System
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_environment():
    """Check if environment is properly configured"""
    
    print("Checking HDFC Mutual Fund RAG Backend Environment")
    print("=" * 60)
    
    # Check required files
    required_files = [
        "src/api/main.py",
        "src/api/config.py",
        "src/api/middleware.py",
        ".env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"ERROR: Missing required files: {missing_files}")
        return False
    
    print("[SUCCESS] All required files present")
    
    # Check environment variables
    env_vars = {
        "API_HOST": os.getenv("API_HOST", "0.0.0.0"),
        "API_PORT": os.getenv("API_PORT", "8000"),
        "GOOGLE_AI_STUDIO_API_KEY": os.getenv("GOOGLE_AI_STUDIO_API_KEY", "")
    }
    
    print("\nEnvironment Configuration:")
    for var_name, var_value in env_vars.items():
        if var_name == "GOOGLE_AI_STUDIO_API_KEY":
            if var_value:
                print(f"[SUCCESS] {var_name}: configured")
            else:
                print(f"[WARNING] {var_name}: not configured (optional for testing)")
        else:
            print(f"[SUCCESS] {var_name}: {var_value}")
    
    # Check data directories
    data_dirs = ["data/embeddings", "data/processed", "logs"]
    for dir_path in data_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("[SUCCESS] Data directories ready")
    
    return True

def main():
    """Main startup function"""
    
    print("HDFC Mutual Fund RAG Backend API")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        print("\nEnvironment check failed. Please fix the issues above.")
        return 1
    
    # Import and run the API
    try:
        print("\nStarting FastAPI server...")
        print("API Documentation: http://localhost:8000/docs")
        print("ReDoc Documentation: http://localhost:8000/redoc")
        print("Health Check: http://localhost:8000/api/health")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 60)
        
        # Import and run the main application
        from api.main import app, get_config
        
        # Get configuration
        config = get_config()
        
        # Run with uvicorn
        import uvicorn
        
        uvicorn.run(
            app,
            host=config["host"],
            port=config["port"],
            workers=config["workers"],
            reload=config["reload"],
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 0
    except ImportError as e:
        import traceback
        print(f"\nImport error: {e}")
        traceback.print_exc()
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements-api.txt")
        return 1
    except Exception as e:
        print(f"\nServer startup failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
