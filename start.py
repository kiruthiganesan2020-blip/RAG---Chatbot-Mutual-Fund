#!/usr/bin/env python3
"""
Unified startup script for RAG Chatbot MVP
Usage: python start.py [backend|frontend|full]
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Add the project root to sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_environment():
    """Validate required environment variables"""
    required = ['GOOGLE_AI_STUDIO_API_KEY', 'ENCRYPTION_KEY']
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        logger.error(f"Missing required environment variables: {missing}")
        sys.exit(1)

def health_check_backend():
    """Check if backend is responding"""
    try:
        import requests
        response = requests.get('http://localhost:8000/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start FastAPI backend"""
    logger.info("Starting FastAPI backend...")
    os.chdir(Path(__file__).parent)
    subprocess.run([sys.executable, 'src/api/main.py'])

def start_frontend():
    """Start Next.js frontend"""
    logger.info("Starting Next.js frontend...")
    frontend_dir = Path(__file__).parent / 'frontend'
    os.chdir(frontend_dir)
    subprocess.run(['npm', 'run', 'dev'])

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'

    validate_environment()

    if mode in ['backend', 'full']:
        try:
            start_backend()
        except KeyboardInterrupt:
            logger.info("Backend stopped")

    if mode in ['frontend', 'full']:
        try:
            start_frontend()
        except KeyboardInterrupt:
            logger.info("Frontend stopped")

if __name__ == '__main__':
    main()
