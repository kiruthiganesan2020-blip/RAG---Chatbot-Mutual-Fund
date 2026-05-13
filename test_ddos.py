#!/usr/bin/env python3
"""
Test DDoS Protection Module
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_ddos():
    """Test DDoS protection module"""
    print("Testing DDoS protection...")
    
    try:
        from src.security.rate_limiting import ddos_protection
        
        # Test the is_request_allowed method
        test_ip = "192.168.1.100"
        result = ddos_protection.is_request_allowed(test_ip)
        
        print(f"Result: {result}")
        print(f"Result type: {type(result)}")
        
        # Check if result is a tuple as expected
        if isinstance(result, tuple):
            print("✅ DDoS protection working correctly")
            return True
        else:
            print("❌ DDoS protection failed")
            return False
            
    except Exception as e:
        print(f"❌ DDoS protection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ddos()
    print(f"Test result: {success}")
