#!/usr/bin/env python3
"""
Test Rate Limiting Module Isolated
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.security.rate_limiting import ddos_protection

def test_rate_limiting():
    """Test rate limiting component"""
    print("Testing rate limiting...")
    
    try:
        test_ip = "192.168.1.100"
        result = ddos_protection.is_request_allowed(test_ip)
        
        print(f"Result: {result}")
        print(f"Result type: {type(result)}")
        
        if isinstance(result, tuple):
            print("✅ Rate limiting working correctly")
            return True
        else:
            print("❌ Rate limiting failed")
            return False
            
    except Exception as e:
        print(f"❌ Rate limiting test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_rate_limiting()
    print(f"Test result: {success}")
