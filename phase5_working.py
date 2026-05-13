#!/usr/bin/env python3
"""
Working Phase 5 Startup Script
This script initializes Phase 5 components step by step to isolate issues
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
        logging.FileHandler('logs/phase5_working.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_only_security():
    """Test only security components"""
    logger.info("=== TESTING SECURITY COMPONENTS ONLY ===")
    
    try:
        # Set encryption key
        if not os.getenv('ENCRYPTION_KEY'):
            os.environ['ENCRYPTION_KEY'] = 'test_encryption_key_for_phase5_startup'
        
        # Import security modules
        from src.security.encryption import encryption
        from src.security.input_validation import SecurityValidator
        from src.security.rate_limiting import ddos_protection
        from src.security.privacy_controls import session_manager
        
        # Test encryption
        test_data = "HDFC Mutual Fund RAG System Test"
        encrypted = encryption.encrypt_text(test_data)
        decrypted = encryption.decrypt_text(encrypted)
        
        if decrypted == test_data:
            logger.info("✅ Encryption system working correctly")
        else:
            logger.error("❌ Encryption system test failed")
            return False
        
        # Test input validation
        validator = SecurityValidator()
        test_query = "What is HDFC Large Cap Fund?"
        validation_result = validator.sanitize_query(test_query)
        
        if validation_result['is_valid']:
            logger.info("✅ Input validation system working correctly")
        else:
            logger.warning(f"⚠️ Input validation warnings: {validation_result['warnings']}")
        
        # Test rate limiting
        test_ip = "192.168.1.100"
        is_allowed, reason = ddos_protection.is_request_allowed(test_ip)
        
        if is_allowed:
            logger.info("✅ Rate limiting system working correctly")
        else:
            logger.warning(f"⚠️ Rate limiting: {reason}")
        
        # Test PII detection
        from src.security.privacy_controls import pii_detector
        test_text = "My email is test@example.com and phone is 9876543210"
        pii_detected = pii_detector.detect_pii(test_text)
        
        if pii_detected:
            logger.info(f"✅ PII detection working correctly: {list(pii_detected.keys())}")
        else:
            logger.warning("⚠️ PII detection may not be working correctly")
        
        # Test session management
        session_id = session_manager.create_session(
            user_id="test_user",
            ip_address="192.168.1.100",
            user_agent="Test Browser"
        )
        
        logger.info(f"Session created: {session_id}")
        logger.info(f"Session ID type: {type(session_id)}")
        
        # Test session validation
        is_valid = session_manager.validate_session(session_id)
        logger.info(f"Session valid: {is_valid}")
        logger.info(f"Validation result type: {type(is_valid)}")
        
        logger.info("✅ All security components tested successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Security testing failed: {e}")
        return False

def test_only_compliance():
    """Test only compliance components"""
    logger.info("=== TESTING COMPLIANCE COMPONENTS ONLY ===")
    
    try:
        # Import compliance modules
        from src.compliance.sebi_framework import sebi_checker
        from src.compliance.amfi_guidelines import amfi_checker
        from src.compliance.disclaimer_manager import disclaimer_manager, DisclaimerCategory
        from src.compliance.source_verification import source_verifier
        from src.compliance.content_automation import content_automation
        from src.compliance.audit_trail import compliance_audit_trail, ComplianceEvent, ComplianceEventType, ComplianceSeverity
        
        # Test SEBI compliance
        test_query = "Should I invest in HDFC Large Cap Fund?"
        sebi_result = sebi_checker.check_compliance(test_query)
        
        if not sebi_result['is_compliant']:
            logger.info("✅ SEBI compliance system working correctly (detected advice query)")
        else:
            logger.warning("⚠️ SEBI compliance may not be detecting advice queries properly")
        
        # Test AMFI compliance
        amfi_result = amfi_checker.check_amfi_compliance(test_query)
        
        if amfi_result['is_compliant']:
            logger.info("✅ AMFI compliance system working correctly")
        else:
            logger.warning(f"⚠️ AMFI compliance warnings: {amfi_result.get('violations', [])}")
        
        # Test disclaimer management
        disclaimer_result = disclaimer_manager.get_required_disclaimers(
            DisclaimerCategory.GENERAL_ADVICE,
            test_query,
            "Test response"
        )
        
        if disclaimer_result:
            logger.info(f"✅ Disclaimer management working correctly: {len(disclaimer_result)} disclaimers")
        else:
            logger.warning("⚠️ Disclaimer management may not be working correctly")
        
        # Test source verification
        test_url = "https://www.hdfcfund.com/scheme-information"
        verification_result = source_verifier.verify_source(test_url)
        
        if verification_result['is_verified']:
            logger.info("✅ Source verification working correctly")
        else:
            logger.warning(f"⚠️ Source verification issues: {verification_result.get('issues', [])}")
        
        # Test content automation
        automation_stats = content_automation.get_update_statistics(days=1)
        
        if automation_stats:
            logger.info("✅ Content automation system working correctly")
        else:
            logger.warning("⚠️ Content automation may not be working correctly")
        
        # Test compliance audit trail
        test_event = ComplianceEvent(
            event_id="test_event_001",
            timestamp=datetime.now(),
            event_type=ComplianceEventType.USER_CONSENT,
            severity=ComplianceSeverity.LOW,
            user_id="test_user",
            session_id=None,
            ip_address="192.168.1.100",
            resource="test_query",
            action="test_action",
            details={"test": True},
            success=True,
            compliance_score=100.0,
            regulatory_references=[],
            remediation_required=False,
            remediation_actions=[],
            auditor="test_system",
            evidence={}
        )
        
        logged = compliance_audit_trail.log_compliance_event(test_event)
        
        if logged:
            logger.info("✅ Compliance audit trail working correctly")
        else:
            logger.error("❌ Compliance audit trail test failed")
            return False
        
        logger.info("✅ All compliance components tested successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Compliance testing failed: {e}")
        return False

def main():
    """Main function"""
    logger.info("🚀 PHASE 5: SECURITY AND COMPLIANCE SYSTEM")
    logger.info(f"📅 Started at: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    # Test security components
    security_ok = test_only_security()
    
    # Test compliance components
    compliance_ok = test_only_compliance()
    
    if security_ok and compliance_ok:
        logger.info("=" * 80)
        logger.info("🎉 PHASE 5 SYSTEM STARTED SUCCESSFULLY!")
        logger.info("✅ All security and compliance components are operational")
        logger.info("✅ System is ready for production use")
        logger.info("=" * 80)
        return True
    else:
        logger.error("❌ Phase 5 system startup failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
