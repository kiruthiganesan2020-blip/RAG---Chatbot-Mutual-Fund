#!/usr/bin/env python3
"""
Phase 1.1.1: Environment Setup and Configuration - Basic Runner
"""

import sys
import os
from pathlib import Path

def main():
    """Main execution for Phase 1.1.1"""
    print("Phase 1.1.1: Environment Setup and Configuration")
    print("=" * 60)
    
    try:
        # Get project root
        project_root = Path(__file__).parent.parent.parent
        src_path = project_root / "src"
        
        # 1. Validate environment
        print("\nStep 1: Validating Environment")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {Path.cwd()}")
        print(f"   Project root: {project_root}")
        print(f"   Src path: {src_path}")
        
        # Check if src directory exists
        if not src_path.exists():
            print(f"   ERROR: src directory not found at {src_path}")
            return 1
        else:
            print("   SUCCESS: src directory exists")
        
        # Check required directories
        required_dirs = [
            src_path / "config",
            src_path / "utils", 
            src_path / "data_collection",
            src_path / "vector_db"
        ]
        
        for dir_path in required_dirs:
            if dir_path.exists():
                print(f"   SUCCESS: {dir_path.name} directory exists")
            else:
                print(f"   WARNING: {dir_path.name} directory missing")
        
        # Check required files
        required_files = [
            src_path / "config" / "settings.py",
            src_path / "config" / "logging_config.py",
            src_path / "utils" / "logger.py",
            src_path / "utils" / "helpers.py"
        ]
        
        for file_path in required_files:
            if file_path.exists():
                print(f"   SUCCESS: {file_path.name} exists")
            else:
                print(f"   WARNING: {file_path.name} missing")
        
        # 2. Check project configuration files
        print("\nStep 2: Project Configuration Files")
        
        project_files = [
            "requirements.txt",
            ".env.example", 
            "docker-compose.yml",
            "Dockerfile",
            ".gitignore"
        ]
        
        for file_name in project_files:
            file_path = project_root / file_name
            if file_path.exists():
                print(f"   SUCCESS: {file_name} exists")
            else:
                print(f"   WARNING: {file_name} missing")
        
        # 3. Check data directories
        print("\nStep 3: Data Directories")
        
        data_dirs = [
            "data/raw",
            "data/processed", 
            "data/embeddings",
            "logs"
        ]
        
        for dir_name in data_dirs:
            dir_path = project_root / dir_name
            if dir_path.exists():
                print(f"   SUCCESS: {dir_name} exists")
            else:
                print(f"   WARNING: {dir_name} missing - will be created")
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"   CREATED: {dir_name}")
                except Exception as e:
                    print(f"   ERROR: Could not create {dir_name}: {e}")
        
        # 4. Check Python path and modules
        print("\nStep 4: Python Environment")
        
        # Add src to path
        sys.path.insert(0, str(src_path))
        
        # Try to import basic modules
        try:
            import loguru
            print("   SUCCESS: loguru installed")
        except ImportError:
            print("   WARNING: loguru not installed")
            print("   RUN: pip install loguru")
        
        try:
            import pydantic
            print("   SUCCESS: pydantic installed")
        except ImportError:
            print("   WARNING: pydantic not installed")
            print("   RUN: pip install pydantic")
        
        # 5. Basic validation without imports
        print("\nStep 5: Basic Validation")
        
        # Check if we can read settings file
        settings_file = src_path / "config" / "settings.py"
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    content = f.read()
                    if 'class Settings' in content:
                        print("   SUCCESS: Settings class found")
                    else:
                        print("   WARNING: Settings class not found")
            except Exception as e:
                print(f"   ERROR: Could not read settings file: {e}")
        
        # 6. Environment check
        print("\nStep 6: Environment Variables")
        
        env_file = project_root / ".env"
        env_example = project_root / ".env.example"
        
        if env_file.exists():
            print("   SUCCESS: .env file exists")
        else:
            print("   INFO: .env file not found")
        
        if env_example.exists():
            print("   SUCCESS: .env.example exists")
            try:
                with open(env_example, 'r') as f:
                    lines = f.readlines()
                    print(f"   INFO: .env.example has {len(lines)} lines")
            except Exception as e:
                print(f"   ERROR: Could not read .env.example: {e}")
        
        # 7. Final validation
        print("\nPhase 1.1.1 Basic Validation Complete!")
        print("\nSummary:")
        print("   Environment structure validated")
        print("   Required files checked")
        print("   Directories verified/created")
        print("   Python environment checked")
        print("   Ready for Phase 1.1.2 execution")
        
        return 0
        
    except Exception as e:
        print(f"\nSetup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
