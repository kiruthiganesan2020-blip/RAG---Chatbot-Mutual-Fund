#!/usr/bin/env python3
"""
Minimal Phase 5 Startup Script
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/phase5_minimal.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main startup function"""
    logger.info("STARTING PHASE 5: SECURITY AND COMPLIANCE SYSTEM")
    logger.info("=" * 60)
    
    try:
        # Set encryption key for testing if not present
        if not os.getenv('ENCRYPTION_KEY'):
            os.environ['ENCRYPTION_KEY'] = 'test_encryption_key_for_phase5_startup'
        
        # Test encryption
        from src.security.encryption import encryption
        test_data = "HDFC Mutual Fund RAG System Test"
        encrypted = encryption.encrypt_text(test_data)
        decrypted = encryption.decrypt_text(encrypted)
        
        if decrypted == test_data:
            logger.info("Encryption system working correctly")
        else:
            logger.error("Encryption system test failed")
            return False
        
        # Test session management
        from src.security.privacy_controls import session_manager
        session_id = session_manager.create_session(
            user_id="test_user",
            ip_address="192.168.1.100",
            user_agent="Test Browser"
        )
        
        if session_id and isinstance(session_id, str):
            logger.info(f"Session management working correctly: {session_id}")
        else:
            logger.error("Session management test failed")
            return False
        
        logger.info("Phase 5 security components initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Security initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("=" * 60)
        logger.info("PHASE 5 SECURITY SYSTEM STARTED SUCCESSFULLY!")
        logger.info("All security components are operational")
        logger.info("=" * 60)
    else:
        logger.error("Phase 5 security system startup failed")
    
    sys.exit(0 if success else 1)
