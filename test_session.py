#!/usr/bin/env python3
"""
Test session manager to isolate the issue
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.security.privacy_controls import session_manager

def test_session():
    """Test session manager functionality"""
    print("Testing session manager...")
    
    # Test creating session
    session_id = session_manager.create_session(
        user_id="test_user",
        ip_address="192.168.1.100",
        user_agent="Test Browser"
    )
    
    print(f"Created session: {session_id}")
    print(f"Session ID type: {type(session_id)}")
    
    # Test validating session
    is_valid = session_manager.validate_session(session_id)
    print(f"Session valid: {is_valid}")
    print(f"Return type: {type(is_valid)}")
    
    return session_id is not None and isinstance(session_id, str) and is_valid

if __name__ == "__main__":
    success = test_session()
    print(f"Test passed: {success}")
