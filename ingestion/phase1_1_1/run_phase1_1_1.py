#!/usr/bin/env python3
"""
Phase 1.1.1: Environment Setup and Configuration - Standalone Runner
"""

import sys
import os
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"

# Add src to Python path
sys.path.insert(0, str(src_path))

def main():
    """Main execution for Phase 1.1.1"""
    print("Phase 1.1.1: Environment Setup and Configuration")
    print("=" * 60)
    
    try:
        # Import after path setup
        from src.config import settings, setup_logging, get_logger
        from src.utils.helpers import create_safe_filename
        
        # Setup logging
        setup_logging(log_level=settings.log_level)
        logger = get_logger(__name__)
        
        # 1. Validate environment
        print("\nStep 1: Validating Environment")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {Path.cwd()}")
        print(f"   Project root: {project_root}")
        print(f"   Src path: {src_path}")
        
        # 2. Check configuration
        print("\nStep 2: Configuration Check")
        print(f"   Log level: {settings.log_level}")
        print(f"   Raw data path: {settings.raw_data_path}")
        print(f"   Processed data path: {settings.processed_data_path}")
        print(f"   Embeddings path: {settings.embeddings_path}")
        print(f"   Log file: {settings.log_file}")
        
        # 3. Create directories
        print("\nStep 3: Creating Directory Structure")
        settings.ensure_directories()
        print("   All directories created/verified")
        
        # 4. Validate configuration files
        print("\nStep 4: Configuration Files Validation")
        
        # Check requirements.txt
        req_file = project_root / "requirements.txt"
        if req_file.exists():
            print("   requirements.txt exists")
        else:
            print("   requirements.txt missing")
            return 1
        
        # Check .env.example
        env_example = project_root / ".env.example"
        if env_example.exists():
            print("   .env.example exists")
        else:
            print("   .env.example missing")
            return 1
        
        # Check Docker files
        docker_compose = project_root / "docker-compose.yml"
        if docker_compose.exists():
            print("   docker-compose.yml exists")
        else:
            print("   docker-compose.yml missing")
            return 1
        
        dockerfile = project_root / "Dockerfile"
        if dockerfile.exists():
            print("   Dockerfile exists")
        else:
            print("   Dockerfile missing")
            return 1
        
        # 5. Test logging
        print("\nStep 5: Testing Logging System")
        logger.info("Phase 1.1.1 logging test - INFO level")
        logger.warning("Phase 1.1.1 logging test - WARNING level")
        logger.error("Phase 1.1.1 logging test - ERROR level")
        print("   Logging system operational")
        
        # 6. Validate settings
        print("\nStep 6: Settings Validation")
        
        # Test URL validation
        if settings.validate_urls():
            print("   HDFC URLs validation passed")
        else:
            print("   HDFC URLs validation failed")
            return 1
        
        # Test directory paths
        directories = [
            settings.raw_data_path,
            settings.processed_data_path,
            settings.embeddings_path
        ]
        
        for dir_path in directories:
            if Path(dir_path).exists():
                print(f"   Directory exists: {dir_path}")
            else:
                print(f"   Directory missing: {dir_path}")
                return 1
        
        # 7. Environment variables check
        print("\nStep 7: Environment Variables")
        env_file = project_root / ".env"
        if env_file.exists():
            print("   .env file exists")
            print("   Using environment variables from .env")
        else:
            print("   .env file not found (using defaults)")
            print("   Copy .env.example to .env to customize settings")
        
        # 8. Final validation
        print("\nPhase 1.1.1 Setup Complete!")
        print("\nSummary:")
        print("   Environment validated")
        print("   Configuration loaded")
        print("   Directories created")
        print("   Logging system active")
        print("   Settings verified")
        print("   Ready for Phase 1.1.2")
        
        logger.info("Phase 1.1.1 environment setup completed successfully")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
