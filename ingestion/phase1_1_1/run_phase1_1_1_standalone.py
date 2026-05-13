#!/usr/bin/env python3
"""
Phase 1.1.1: Environment Setup and Configuration - Standalone Runner
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
        
        # Add src to Python path
        sys.path.insert(0, str(src_path))
        
        # 1. Validate environment
        print("\nStep 1: Validating Environment")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {Path.cwd()}")
        print(f"   Project root: {project_root}")
        print(f"   Src path: {src_path}")
        
        # Check if src directory exists and has required modules
        if not src_path.exists():
            print(f"   ERROR: src directory not found at {src_path}")
            return 1
        
        # Check required files in src
        required_files = [
            src_path / "config" / "settings.py",
            src_path / "config" / "logging_config.py",
            src_path / "utils" / "logger.py"
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                print(f"   WARNING: Required file not found: {file_path}")
        
        # Try to import modules with error handling
        try:
            # Import settings directly
            sys.path.insert(0, str(src_path / "config"))
            from settings import Settings
            from logging_config import setup_logging
            import loguru
            
            # Create settings instance
            settings = Settings()
            
            # Setup logging
            setup_logging(log_level=settings.log_level)
            
            # Get logger directly from loguru
            logger = loguru.logger
            
            print("   ✅ Successfully imported required modules")
            
        except ImportError as e:
            print(f"   ❌ Import error: {e}")
            print("   ⚠️  Running in validation mode without full functionality")
            return 1
        except Exception as e:
            print(f"   ❌ Configuration error: {e}")
            return 1
        
        # 2. Check configuration
        print("\nStep 2: Configuration Check")
        print(f"   Log level: {settings.log_level}")
        print(f"   Raw data path: {settings.raw_data_path}")
        print(f"   Processed data path: {settings.processed_data_path}")
        print(f"   Embeddings path: {settings.embeddings_path}")
        print(f"   Log file: {settings.log_file}")
        
        # 3. Create directories
        print("\nStep 3: Creating Directory Structure")
        try:
            settings.ensure_directories()
            print("   ✅ All directories created/verified")
        except Exception as e:
            print(f"   ❌ Directory creation failed: {e}")
            return 1
        
        # 4. Validate configuration files
        print("\nStep 4: Configuration Files Validation")
        
        # Check requirements.txt
        req_file = project_root / "requirements.txt"
        if req_file.exists():
            print("   ✅ requirements.txt exists")
        else:
            print("   ❌ requirements.txt missing")
            return 1
        
        # Check .env.example
        env_example = project_root / ".env.example"
        if env_example.exists():
            print("   ✅ .env.example exists")
        else:
            print("   ❌ .env.example missing")
            return 1
        
        # Check Docker files
        docker_compose = project_root / "docker-compose.yml"
        if docker_compose.exists():
            print("   ✅ docker-compose.yml exists")
        else:
            print("   ❌ docker-compose.yml missing")
            return 1
        
        dockerfile = project_root / "Dockerfile"
        if dockerfile.exists():
            print("   ✅ Dockerfile exists")
        else:
            print("   ❌ Dockerfile missing")
            return 1
        
        # 5. Test logging
        print("\nStep 5: Testing Logging System")
        try:
            logger.info("Phase 1.1.1 logging test - INFO level")
            logger.warning("Phase 1.1.1 logging test - WARNING level")
            logger.error("Phase 1.1.1 logging test - ERROR level")
            print("   ✅ Logging system operational")
        except Exception as e:
            print(f"   ❌ Logging test failed: {e}")
            return 1
        
        # 6. Validate settings
        print("\nStep 6: Settings Validation")
        
        # Test URL validation
        try:
            if settings.validate_urls():
                print("   ✅ HDFC URLs validation passed")
            else:
                print("   ❌ HDFC URLs validation failed")
                return 1
        except Exception as e:
            print(f"   ❌ URL validation failed: {e}")
            return 1
        
        # Test directory paths
        directories = [
            settings.raw_data_path,
            settings.processed_data_path,
            settings.embeddings_path
        ]
        
        for dir_path in directories:
            if Path(dir_path).exists():
                print(f"   ✅ Directory exists: {dir_path}")
            else:
                print(f"   ❌ Directory missing: {dir_path}")
                return 1
        
        # 7. Environment variables check
        print("\nStep 7: Environment Variables")
        env_file = project_root / ".env"
        if env_file.exists():
            print("   ✅ .env file exists")
            print("   ℹ️  Using environment variables from .env")
        else:
            print("   ⚠️  .env file not found (using defaults)")
            print("   💡 Copy .env.example to .env to customize settings")
        
        # 8. Final validation
        print("\n✅ Phase 1.1.1 Setup Complete!")
        print("\n📊 Summary:")
        print("   • Environment validated")
        print("   • Configuration loaded")
        print("   • Directories created")
        print("   • Logging system active")
        print("   • Settings verified")
        print("   • Ready for Phase 1.1.2")
        
        logger.info("Phase 1.1.1 environment setup completed successfully")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
