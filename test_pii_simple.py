#!/usr/bin/env python3
"""
Simple PII Detection Test
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.security.privacy_controls import pii_detector, PIIType

def test_pii():
    """Test PII detection"""
    print("Testing PII detection...")
    
    # Test PII detection
    test_text = "My email is test@example.com and phone is 9876543210"
    pii_detected = pii_detector.detect_pii(test_text)
    
    print(f"PII detected: {pii_detected}")
    print(f"PII detected type: {type(pii_detected)}")
    
    if pii_detected:
        print("PII detection working correctly")
        print(f"Keys: {list(pii_detected.keys())}")
        
        # Check if keys are strings
        for key in pii_detected.keys():
            print(f"Key '{key}' type: {type(key)}")
    else:
        print("PII detection failed")
    
    return pii_detected is not None

if __name__ == "__main__":
    success = test_pii()
    print(f"Test result: {success}")
