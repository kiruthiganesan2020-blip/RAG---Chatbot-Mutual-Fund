"""
Local configuration for Phase 1.1.1 execution
"""
import sys
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Add src to Python path
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

# Import after path setup
try:
    from src.config import settings, setup_logging, get_logger
    from src.utils.helpers import create_safe_filename
except ImportError as e:
    print(f"Failed to import modules: {e}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Src path: {SRC_PATH}")
    sys.exit(1)

# Phase 1.1.1 specific configuration
PHASE_NAME = "Phase 1.1.1"
PHASE_DESCRIPTION = "Environment Setup and Configuration"

# Required files for this phase
REQUIRED_FILES = {
    "requirements.txt": PROJECT_ROOT / "requirements.txt",
    ".env.example": PROJECT_ROOT / ".env.example",
    "docker-compose.yml": PROJECT_ROOT / "docker-compose.yml",
    "Dockerfile": PROJECT_ROOT / "Dockerfile"
}

# Required directories
REQUIRED_DIRECTORIES = [
    PROJECT_ROOT / "src" / "config",
    PROJECT_ROOT / "src" / "utils",
    PROJECT_ROOT / "data" / "raw",
    PROJECT_ROOT / "data" / "processed",
    PROJECT_ROOT / "data" / "embeddings",
    PROJECT_ROOT / "logs"
]

# Validation functions
def validate_phase_requirements():
    """Validate all requirements for Phase 1.1.1"""
    results = {
        "files": {},
        "directories": {},
        "imports": {},
        "overall": True
    }
    
    # Check required files
    for name, path in REQUIRED_FILES.items():
        exists = path.exists()
        results["files"][name] = {
            "path": str(path),
            "exists": exists,
            "status": "✅" if exists else "❌"
        }
        if not exists:
            results["overall"] = False
    
    # Check required directories
    for path in REQUIRED_DIRECTORIES:
        exists = path.exists()
        results["directories"][str(path)] = {
            "path": str(path),
            "exists": exists,
            "status": "✅" if exists else "❌"
        }
        if not exists:
            results["overall"] = False
    
    # Check imports
    try:
        import settings
        results["imports"]["settings"] = {"status": "✅", "error": None}
    except Exception as e:
        results["imports"]["settings"] = {"status": "❌", "error": str(e)}
        results["overall"] = False
    
    try:
        import setup_logging
        results["imports"]["setup_logging"] = {"status": "✅", "error": None}
    except Exception as e:
        results["imports"]["setup_logging"] = {"status": "❌", "error": str(e)}
        results["overall"] = False
    
    try:
        import get_logger
        results["imports"]["get_logger"] = {"status": "✅", "error": None}
    except Exception as e:
        results["imports"]["get_logger"] = {"status": "❌", "error": str(e)}
        results["overall"] = False
    
    return results

def print_validation_results(results):
    """Print validation results in a formatted way"""
    print(f"\n📋 {PHASE_NAME} Validation Results")
    print("=" * 50)
    
    # Files validation
    print("\n📄 Required Files:")
    for name, info in results["files"].items():
        print(f"   {info['status']} {name}")
        if not info["exists"]:
            print(f"      Missing: {info['path']}")
    
    # Directories validation
    print("\n📁 Required Directories:")
    for path, info in results["directories"].items():
        dir_name = Path(path).name
        print(f"   {info['status']} {dir_name}")
        if not info["exists"]:
            print(f"      Missing: {info['path']}")
    
    # Imports validation
    print("\n📦 Module Imports:")
    for name, info in results["imports"].items():
        print(f"   {info['status']} {name}")
        if info["error"]:
            print(f"      Error: {info['error']}")
    
    # Overall status
    print(f"\n🎯 Overall Status: {'✅ PASS' if results['overall'] else '❌ FAIL'}")
    
    return results["overall"]
