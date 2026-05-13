#!/usr/bin/env python3
"""
Debug Phase 5 startup to isolate the issue
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.security.privacy_controls import session_manager

def debug_security():
    """Debug security initialization step by step"""
    print("=== DEBUG: Security Initialization ===")
    
    try:
        # Test session manager creation
        print("Creating session...")
        session_id = session_manager.create_session(
            user_id="test_user",
            ip_address="192.168.1.100",
            user_agent="Test Browser"
        )
        print(f"Session created: {session_id}")
        print(f"Session type: {type(session_id)}")
        
        # Test session validation
        print("Validating session...")
        is_valid = session_manager.validate_session(session_id)
        print(f"Session valid: {is_valid}")
        print(f"Validation result type: {type(is_valid)}")
        
        return True
        
    except Exception as e:
        print(f"Error in security initialization: {e}")
        print(f"Error type: {type(e)}")
        return False

if __name__ == "__main__":
    success = debug_security()
    print(f"Security debug result: {success}")
