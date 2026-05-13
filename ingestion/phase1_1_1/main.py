#!/usr/bin/env python3
"""
Phase 1.1.1: Environment Setup and Configuration - Main Execution Script
"""

import sys
import os
from pathlib import Path

# Import local configuration
from . import config

def main():
    """Main execution for Phase 1.1.1"""
    print("🚀 Phase 1.1.1: Environment Setup and Configuration")
    print("=" * 60)
    
    try:
        # 1. Validate environment
        print("\n📋 Step 1: Validating Environment")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {Path.cwd()}")
        print(f"   Project root: {config.PROJECT_ROOT}")
        
        # 2. Check configuration
        print("\n⚙️  Step 2: Configuration Check")
        print(f"   Log level: {config.settings.log_level}")
        print(f"   Raw data path: {config.settings.raw_data_path}")
        print(f"   Processed data path: {config.settings.processed_data_path}")
        print(f"   Embeddings path: {config.settings.embeddings_path}")
        print(f"   Log file: {config.settings.log_file}")
        
        # 3. Create directories
        print("\n📁 Step 3: Creating Directory Structure")
        config.settings.ensure_directories()
        print("   ✅ All directories created/verified")
        
        # 4. Validate configuration files
        print("\n📄 Step 4: Configuration Files Validation")
        
        # Check requirements.txt
        req_file = config.PROJECT_ROOT / "requirements.txt"
        if req_file.exists():
            print("   ✅ requirements.txt exists")
        else:
            print("   ❌ requirements.txt missing")
            return 1
        
        # Check .env.example
        env_example = config.PROJECT_ROOT / ".env.example"
        if env_example.exists():
            print("   ✅ .env.example exists")
        else:
            print("   ❌ .env.example missing")
            return 1
        
        # Check Docker files
        docker_compose = config.PROJECT_ROOT / "docker-compose.yml"
        if docker_compose.exists():
            print("   ✅ docker-compose.yml exists")
        else:
            print("   ❌ docker-compose.yml missing")
            return 1
        
        dockerfile = config.PROJECT_ROOT / "Dockerfile"
        if dockerfile.exists():
            print("   ✅ Dockerfile exists")
        else:
            print("   ❌ Dockerfile missing")
            return 1
        
        # 5. Test logging
        print("\n📝 Step 5: Testing Logging System")
        logger = config.get_logger(__name__)
        logger.info("Phase 1.1.1 logging test - INFO level")
        logger.warning("Phase 1.1.1 logging test - WARNING level")
        logger.error("Phase 1.1.1 logging test - ERROR level")
        print("   ✅ Logging system operational")
        
        # 6. Validate settings
        print("\n🔍 Step 6: Settings Validation")
        
        # Test URL validation
        if config.settings.validate_urls():
            print("   ✅ HDFC URLs validation passed")
        else:
            print("   ❌ HDFC URLs validation failed")
            return 1
        
        # Test directory paths
        directories = [
            config.settings.raw_data_path,
            config.settings.processed_data_path,
            config.settings.embeddings_path
        ]
        
        for dir_path in directories:
            if Path(dir_path).exists():
                print(f"   ✅ Directory exists: {dir_path}")
            else:
                print(f"   ❌ Directory missing: {dir_path}")
                return 1
        
        # 7. Environment variables check
        print("\n🌍 Step 7: Environment Variables")
        env_file = config.PROJECT_ROOT / ".env"
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
        logger = config.get_logger(__name__)
        logger.error(f"Phase 1.1.1 setup failed: {e}")
        print(f"\n❌ Setup failed: {e}")
        return 1


    
    try:
        # 1. Validate environment
        print("\n📋 Step 1: Validating Environment")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {Path.cwd()}")
        print(f"   Project root: {Path(__file__).parent.parent.parent}")
        
        # 2. Check configuration
        print("\n⚙️  Step 2: Configuration Check")
        print(f"   Log level: {settings.log_level}")
        print(f"   Raw data path: {settings.raw_data_path}")
        print(f"   Processed data path: {settings.processed_data_path}")
        print(f"   Embeddings path: {settings.embeddings_path}")
        print(f"   Log file: {settings.log_file}")
        
        # 3. Create directories
        print("\n📁 Step 3: Creating Directory Structure")
        settings.ensure_directories()
        print("   ✅ All directories created/verified")
        
        # 4. Validate configuration files
        print("\n📄 Step 4: Configuration Files Validation")
        
        # Check requirements.txt
        req_file = Path(__file__).parent.parent.parent / "requirements.txt"
        if req_file.exists():
            print("   ✅ requirements.txt exists")
        else:
            print("   ❌ requirements.txt missing")
            return 1
        
        # Check .env.example
        env_example = Path(__file__).parent.parent.parent / ".env.example"
        if env_example.exists():
            print("   ✅ .env.example exists")
        else:
            print("   ❌ .env.example missing")
            return 1
        
        # Check Docker files
        docker_compose = Path(__file__).parent.parent.parent / "docker-compose.yml"
        if docker_compose.exists():
            print("   ✅ docker-compose.yml exists")
        else:
            print("   ❌ docker-compose.yml missing")
            return 1
        
        dockerfile = Path(__file__).parent.parent.parent / "Dockerfile"
        if dockerfile.exists():
            print("   ✅ Dockerfile exists")
        else:
            print("   ❌ Dockerfile missing")
            return 1
        
        # 5. Test logging
        print("\n📝 Step 5: Testing Logging System")
        logger.info("Phase 1.1.1 logging test - INFO level")
        logger.warning("Phase 1.1.1 logging test - WARNING level")
        logger.error("Phase 1.1.1 logging test - ERROR level")
        print("   ✅ Logging system operational")
        
        # 6. Validate settings
        print("\n🔍 Step 6: Settings Validation")
        
        # Test URL validation
        if settings.validate_urls():
            print("   ✅ HDFC URLs validation passed")
        else:
            print("   ❌ HDFC URLs validation failed")
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
        print("\n🌍 Step 7: Environment Variables")
        env_file = Path(__file__).parent.parent.parent / ".env"
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
        logger.error(f"Phase 1.1.1 setup failed: {e}")
        print(f"\n❌ Setup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
