#!/usr/bin/env python3
"""
Simple Phase 5 Startup Script
Tests individual components to isolate issues
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
        logging.FileHandler('logs/phase5_simple.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_encryption():
    """Test encryption component"""
    logger.info("=== TESTING ENCRYPTION ===")
    
    try:
        # Set encryption key
        if not os.getenv('ENCRYPTION_KEY'):
            os.environ['ENCRYPTION_KEY'] = 'test_encryption_key_for_phase5_startup'
        
        from src.security.encryption import encryption
        test_data = "HDFC Mutual Fund RAG System Test"
        encrypted = encryption.encrypt_text(test_data)
        decrypted = encryption.decrypt_text(encrypted)
        
        if decrypted == test_data:
            logger.info("✅ Encryption system working correctly")
            return True
        else:
            logger.error("❌ Encryption system test failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Encryption test failed: {e}")
        return False

def test_input_validation():
    """Test input validation component"""
    logger.info("=== TESTING INPUT VALIDATION ===")
    
    try:
        from src.security.input_validation import SecurityValidator
        validator = SecurityValidator()
        test_query = "What is HDFC Large Cap Fund?"
        validation_result = validator.sanitize_query(test_query)
        
        if validation_result['is_valid']:
            logger.info("✅ Input validation system working correctly")
            return True
        else:
            logger.warning(f"⚠️ Input validation warnings: {validation_result['warnings']}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Input validation test failed: {e}")
        return False

def test_rate_limiting():
    """# Test rate limiting"""
    logger.info("=== TESTING RATE LIMITING ===")
    
    try:
        from src.security.rate_limiting import ddos_protection
        test_ip = "192.168.1.100"
        result = ddos_protection.is_request_allowed(test_ip)
        
        if isinstance(result, tuple):
            is_allowed, reason = result
        else:
            is_allowed, reason = result, "Unknown error"
        
        if is_allowed:
            logger.info("✅ Rate limiting system working correctly")
            return True
        else:
            logger.warning(f"⚠️ Rate limiting: {reason}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Rate limiting test failed: {e}")
        return False

def test_pii_detection():
    """Test PII detection component"""
    logger.info("=== TESTING PII DETECTION ===")
    
    try:
        from src.security.privacy_controls import pii_detector
        test_text = "My email is test@example.com and phone is 9876543210"
        pii_detected = pii_detector.detect_pii(test_text)
        
        if pii_detected:
            logger.info(f"✅ PII detection working correctly: {list(pii_detected.keys())}")
            return True
        else:
            logger.warning("⚠️ PII detection may not be working correctly")
            return False
            
    except Exception as e:
        logger.error(f"❌ PII detection test failed: {e}")
        return False

def test_sebi_compliance():
    """Test SEBI compliance component"""
    logger.info("=== TESTING SEBI COMPLIANCE ===")
    
    try:
        from src.compliance.sebi_framework import sebi_checker
        test_query = "Should I invest in HDFC Large Cap Fund?"
        sebi_result = sebi_checker.check_compliance(test_query)
        
        if not sebi_result['is_compliant']:
            logger.info("✅ SEBI compliance system working correctly (detected advice query)")
            return True
        else:
            logger.warning("⚠️ SEBI compliance may not be detecting advice queries properly")
            return False
            
    except Exception as e:
        logger.error(f"❌ SEBI compliance test failed: {e}")
        return False

def test_amfi_compliance():
    """Test AMFI compliance component"""
    logger.info("=== TESTING AMFI COMPLIANCE ===")
    
    try:
        from src.compliance.amfi_guidelines import amfi_checker
        test_query = "What is mutual fund?"
        amfi_result = amfi_checker.check_amfi_compliance(test_query)
        
        if amfi_result['is_compliant']:
            logger.info("✅ AMFI compliance system working correctly")
            return True
        else:
            logger.warning(f"⚠️ AMFI compliance warnings: {amfi_result.get('violations', [])}")
            return False
            
    except Exception as e:
        logger.error(f"❌ AMFI compliance test failed: {e}")
        return False

def test_disclaimer_manager():
    """Test disclaimer manager component"""
    logger.info("=== TESTING DISCLAIMER MANAGER ===")
    
    try:
        from src.compliance.disclaimer_manager import disclaimer_manager, DisclaimerCategory
        disclaimer_result = disclaimer_manager.get_required_disclaimers(
            DisclaimerCategory.GENERAL_ADVICE,
            "test query",
            "Test response"
        )
        
        if disclaimer_result:
            logger.info(f"✅ Disclaimer management working correctly: {len(disclaimer_result)} disclaimers")
            return True
        else:
            logger.warning("⚠️ Disclaimer management may not be working correctly")
            return False
            
    except Exception as e:
        logger.error(f"❌ Disclaimer manager test failed: {e}")
        return False

def test_source_verification():
    """Test source verification component"""
    logger.info("=== TESTING SOURCE VERIFICATION ===")
    
    try:
        from src.compliance.source_verification import source_verifier
        test_url = "https://www.hdfcfund.com/scheme-information"
        verification_result = source_verifier.verify_source(test_url)
        
        if verification_result['is_verified']:
            logger.info("✅ Source verification working correctly")
            return True
        else:
            logger.warning(f"⚠️ Source verification issues: {verification_result.get('issues', [])}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Source verification test failed: {e}")
        return False

def test_content_automation():
    """Test content automation component"""
    logger.info("=== TESTING CONTENT AUTOMATION ===")
    
    try:
        from src.compliance.content_automation import content_automation
        automation_stats = content_automation.get_update_statistics(days=1)
        
        if automation_stats:
            logger.info("✅ Content automation system working correctly")
            return True
        else:
            logger.warning("⚠️ Content automation may not be working correctly")
            return False
            
    except Exception as e:
        logger.error(f"❌ Content automation test failed: {e}")
        return False

def main():
    """Main function"""
    logger.info("🚀 PHASE 5: SECURITY AND COMPLIANCE SYSTEM")
    logger.info(f"📅 Started at: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    # Test all components
    tests = [
        ("Encryption", test_encryption),
        ("Input Validation", test_input_validation),
        ("Rate Limiting", test_rate_limiting),
        ("PII Detection", test_pii_detection),
        ("SEBI Compliance", test_sebi_compliance),
        ("AMFI Compliance", test_amfi_compliance),
        ("Disclaimer Manager", test_disclaimer_manager),
        ("Source Verification", test_source_verification),
        ("Content Automation", test_content_automation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} test failed: {e}")
            results[test_name] = False
    
    # Summary
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(tests)
    
    logger.info("=" * 80)
    logger.info("📊 TEST RESULTS:")
    logger.info(f"Total tests: {total_tests}")
    logger.info(f"Passed tests: {passed_tests}")
    logger.info(f"Success rate: {passed_tests/total_tests*100:.1f}%")
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info("=" * 80)
    
    if passed_tests == total_tests:
        logger.info("🎉 PHASE 5 SYSTEM STARTED SUCCESSFULLY!")
        logger.info("✅ All security and compliance components are operational")
        logger.info("✅ System is ready for production use")
        logger.info("=" * 80)
        return True
    else:
        logger.error("❌ Phase 5 system startup failed - some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
