#!/usr/bin/env python3
"""
Simple Test to Isolate Rate Limiting Issue
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_ddos_protection():
    """Test DDoS protection directly"""
    print("Testing DDoS protection...")
    
    try:
        from src.security.rate_limiting import ddos_protection
        
        # Test the is_request_allowed method directly
        test_ip = "192.168.1.100"
        result = ddos_protection.is_request_allowed(test_ip)
        
        print(f"Raw result: {result}")
        print(f"Result type: {type(result)}")
        
        # Check if result is a tuple as expected
        if isinstance(result, tuple):
            print("✅ DDoS protection working correctly")
            print(f"Tuple length: {len(result)}")
            
            # Check tuple contents
            if len(result) == 2:
                is_allowed, reason = result
                print(f"  is_allowed: {is_allowed}")
                print(f"  reason: {reason}")
        else:
            print("❌ DDoS protection failed")
            return False
            
    except Exception as e:
        print(f"❌ DDoS protection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ddos_protection()
    print(f"Test result: {success}")
