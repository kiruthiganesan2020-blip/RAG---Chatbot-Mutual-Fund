#!/usr/bin/env python3
"""
Test setup script for Phase 1
"""

import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Test Phase 1 setup"""
    print("🧪 Testing Phase 1 Setup")
    print("=" * 50)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Check if we're in the right directory
    if not Path("src").exists():
        print("❌ Not in project root directory")
        return 1
    
    # Test imports
    print("\n📦 Testing imports...")
    try:
        sys.path.insert(0, "src")
        from src.config import settings
        from src.data_collection import HDFCFundScraper, ContentProcessor
        from src.vector_db import ChromaManager
        from src.utils import get_logger
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return 1
    
    # Test settings
    print("\n⚙️  Testing configuration...")
    try:
        print(f"✅ HDFC URLs configured: {len(settings.hdfc_urls)}")
        print(f"✅ Data paths: {settings.raw_data_path}")
        print(f"✅ Logging level: {settings.log_level}")
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return 1
    
    # Test directory creation
    print("\n📁 Testing directory structure...")
    try:
        settings.ensure_directories()
        print("✅ Directories created/verified")
    except Exception as e:
        print(f"❌ Directory creation failed: {e}")
        return 1
    
    # Test logging
    print("\n📝 Testing logging...")
    try:
        logger = get_logger("test")
        logger.info("Test log message")
        print("✅ Logging working")
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return 1
    
    # Test requirements installation
    print("\n📋 Checking requirements...")
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return 1
    
    # Run basic tests
    print("\n🧪 Running basic tests...")
    if not run_command("python -m pytest tests/ -v --tb=short", "Running tests"):
        print("⚠️  Some tests failed, but setup may still work")
    
    print("\n🎉 Phase 1 Setup Test Complete!")
    print("\nTo run the full pipeline:")
    print("python scripts/run_phase1.py")
    print("\nOr run individual components:")
    print("python src/main.py --mode full")
    print("python src/main.py --mode collect --fund hdfc-large-cap")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
