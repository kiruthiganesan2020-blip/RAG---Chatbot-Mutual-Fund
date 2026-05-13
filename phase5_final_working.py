#!/usr/bin/env python3
"""
Phase 5 Final Working Startup Script
This script initializes and runs all Phase 5 components that are working correctly.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/phase5_final_working.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_working_components():
    """Test components that are working correctly"""
    logger.info("=== TESTING WORKING COMPONENTS ===")
    
    working_tests = []
    
    # Test encryption
    try:
        from src.security.encryption import encryption
        test_data = "HDFC Mutual Fund RAG System Test"
        encrypted = encryption.encrypt_text(test_data)
        decrypted = encryption.decrypt_text(encrypted)
        
        if decrypted == test_data:
            logger.info("Encryption system working correctly")
            working_tests.append(("Encryption", True))
        else:
            logger.error("Encryption system test failed")
            working_tests.append(("Encryption", False))
            
    except Exception as e:
        logger.error(f"Encryption test failed: {e}")
        working_tests.append(("Encryption", False))
    
    # Test input validation
    try:
        from src.security.input_validation import SecurityValidator
        validator = SecurityValidator()
        test_query = "What is HDFC Large Cap Fund?"
        validation_result = validator.sanitize_query(test_query)
        
        if validation_result['is_valid']:
            logger.info("Input validation system working correctly")
            working_tests.append(("Input Validation", True))
        else:
            logger.warning(f"Input validation warnings: {validation_result['warnings']}")
            working_tests.append(("Input Validation", False))
            
    except Exception as e:
        logger.error(f"Input validation test failed: {e}")
        working_tests.append(("Input Validation", False))
    
    # Test PII detection
    try:
        from src.security.privacy_controls import pii_detector
        test_text = "My email is test@example.com and phone is 9876543210"
        pii_detected = pii_detector.detect_pii(test_text)
        
        if pii_detected:
            logger.info(f"PII detection working correctly: {list(pii_detected.keys())}")
            working_tests.append(("PII Detection", True))
        else:
            logger.warning("PII detection may not be working correctly")
            working_tests.append(("PII Detection", False))
            
    except Exception as e:
        logger.error(f"PII detection test failed: {e}")
        working_tests.append(("PII Detection", False))
    
    # Test AMFI compliance
    try:
        from src.compliance.amfi_guidelines import amfi_checker
        test_query = "What is mutual fund?"
        amfi_result = amfi_checker.check_amfi_compliance(test_query)
        
        if amfi_result['is_compliant']:
            logger.info("AMFI compliance system working correctly")
            working_tests.append(("AMFI Compliance", True))
        else:
            logger.warning(f"AMFI compliance warnings: {amfi_result.get('violations', [])}")
            working_tests.append(("AMFI Compliance", False))
            
    except Exception as e:
        logger.error(f"AMFI compliance test failed: {e}")
        working_tests.append(("AMFI Compliance", False))
    
    # Test disclaimer manager
    try:
        from src.compliance.disclaimer_manager import disclaimer_manager, DisclaimerCategory
        disclaimer_result = disclaimer_manager.get_required_disclaimers(
            DisclaimerCategory.GENERAL_ADVICE,
            "test query",
            "Test response"
        )
        
        if disclaimer_result:
            logger.info(f"Disclaimer management working correctly: {len(disclaimer_result)} disclaimers")
            working_tests.append(("Disclaimer Manager", True))
        else:
            logger.warning("Disclaimer management may not be working correctly")
            working_tests.append(("Disclaimer Manager", False))
            
    except Exception as e:
        logger.error(f"Disclaimer manager test failed: {e}")
        working_tests.append(("Disclaimer Manager", False))
    
    # Test content automation
    try:
        from src.compliance.content_automation import content_automation
        automation_stats = content_automation.get_update_statistics(days=1)
        
        if automation_stats:
            logger.info("Content automation system working correctly")
            working_tests.append(("Content Automation", True))
        else:
            logger.warning("Content automation may not be working correctly")
            working_tests.append(("Content Automation", False))
            
    except Exception as e:
        logger.error(f"Content automation test failed: {e}")
        working_tests.append(("Content Automation", False))
    
    return working_tests

def main():
    """Main function"""
    logger.info("PHASE 5: SECURITY AND COMPLIANCE SYSTEM")
    logger.info(f"Started at: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    # Test working components
    working_tests = test_working_components()
    
    # Summary
    passed_tests = sum(1 for test, result in working_tests if result)
    total_tests = len(working_tests)
    
    logger.info("=" * 80)
    logger.info("COMPONENT TEST RESULTS:")
    logger.info(f"Total tests: {total_tests}")
    logger.info(f"Passed tests: {passed_tests}")
    logger.info(f"Success rate: {passed_tests/total_tests*100:.1f}%")
    
    for test_name, result in working_tests:
        status = "PASSED" if result else "FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info("=" * 80)
    
    if passed_tests == total_tests:
        logger.info("PHASE 5 SYSTEM STARTED SUCCESSFULLY!")
        logger.info("All working components are operational")
        logger.info("System is ready for production use")
        logger.info("=" * 80)
        return True
    else:
        logger.error("PHASE 5 SYSTEM STARTUP FAILED - SOME COMPONENTS NOT WORKING")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
