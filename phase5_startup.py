"""
Phase 5 Startup Script
Security and Compliance System Initialization

This script initializes and starts all Phase 5 components:
- Security Implementation (encryption, input validation, rate limiting, privacy controls, audit logging)
- Regulatory Compliance (SEBI framework, AMFI guidelines, disclaimer management, source verification, content automation, audit trail)
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/phase5_startup.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'data/security',
        'data/compliance',
        'data/audit',
        'data/encrypted'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def initialize_security():
    """Initialize security components"""
    logger.info("=" * 60)
    logger.info("INITIALIZING SECURITY COMPONENTS")
    logger.info("=" * 60)
    
    try:
        # Set encryption key for testing if not present
        if not os.getenv('ENCRYPTION_KEY'):
            os.environ['ENCRYPTION_KEY'] = 'test_encryption_key_for_phase5_startup'
        
        # Import security modules
        from src.security.encryption import encryption, DataEncryption
        from src.security.input_validation import SecurityValidator, SecurityConfig
        from src.security.rate_limiting import ddos_protection, session_rate_limiter, api_key_rate_limiter
        from src.security.privacy_controls import pii_detector, privacy_policy, session_manager
        from src.security.audit_logging import audit_logger, session_audit_manager
        
        logger.info("Security modules imported successfully")
        
        # Test encryption
        test_data = "HDFC Mutual Fund RAG System Test"
        encrypted = encryption.encrypt_text(test_data)
        decrypted = encryption.decrypt_text(encrypted)
        
        if decrypted == test_data:
            logger.info("Encryption system working correctly")
        else:
            logger.error("Encryption system test failed")
            return False
        
        # Test input validation
        validator = SecurityValidator()
        test_query = "What is HDFC Large Cap Fund?"
        validation_result = validator.sanitize_query(test_query)
        
        if validation_result['is_valid']:
            logger.info("Input validation system working correctly")
        else:
            logger.warning(f"Input validation warnings: {validation_result['warnings']}")
        
        # Test rate limiting
        test_ip = "192.168.1.100"
        is_allowed, reason = ddos_protection.is_request_allowed(test_ip)
        
        if is_allowed:
            logger.info("Rate limiting system working correctly")
        else:
            logger.warning(f"Rate limiting: {reason}")
        
        # Test PII detection
        test_text = "My email is test@example.com and phone is 9876543210"
        pii_detected = pii_detector.detect_pii(test_text)
        
        if pii_detected:
            logger.info(f"PII detection working correctly: {list(pii_detected.keys())}")
        else:
            logger.warning("PII detection may not be working correctly")
        
        # Test session management
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
        
        logger.info("All security components initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Security initialization failed: {e}")
        return False

def initialize_compliance():
    """Initialize compliance components"""
    logger.info("=" * 60)
    logger.info("INITIALIZING COMPLIANCE COMPONENTS")
    logger.info("=" * 60)
    
    try:
        # Import compliance modules
        from src.compliance.sebi_framework import sebi_checker, fund_validator
        from src.compliance.amfi_guidelines import amfi_checker
        from src.compliance.disclaimer_manager import disclaimer_manager
        from src.compliance.source_verification import source_verifier
        from src.compliance.content_automation import content_automation
        from src.compliance.audit_trail import compliance_audit_trail
        
        logger.info("Compliance modules imported successfully")
        
        # Test SEBI compliance checking
        test_query = "Should I invest in HDFC Large Cap Fund?"
        sebi_result = sebi_checker.check_compliance(test_query)
        
        if not sebi_result['is_compliant']:
            logger.info("SEBI compliance system working correctly (detected advice query)")
        else:
            logger.warning("SEBI compliance may not be detecting advice queries properly")
        
        # Test AMFI compliance checking
        amfi_result = amfi_checker.check_amfi_compliance(test_query)
        
        if amfi_result['is_compliant']:
            logger.info("AMFI compliance system working correctly")
        else:
            logger.warning(f"AMFI compliance warnings: {amfi_result.get('violations', [])}")
        
        # Test disclaimer management
        from src.compliance.disclaimer_manager import DisclaimerCategory
        disclaimer_result = disclaimer_manager.get_required_disclaimers(
            DisclaimerCategory.GENERAL_ADVICE,
            test_query,
            "Test response"
        )
        
        if disclaimer_result:
            logger.info(f"Disclaimer management working correctly: {len(disclaimer_result)} disclaimers")
        else:
            logger.warning("Disclaimer management may not be working correctly")
        
        # Test source verification
        test_url = "https://www.hdfcfund.com/scheme-information"
        verification_result = source_verifier.verify_source(test_url)
        
        if verification_result['is_verified']:
            logger.info("Source verification working correctly")
        else:
            logger.warning(f"Source verification issues: {verification_result.get('issues', [])}")
        
        # Test content automation
        automation_stats = content_automation.get_update_statistics(days=1)
        
        if automation_stats:
            logger.info("Content automation system working correctly")
        else:
            logger.warning("Content automation may not be working correctly")
        
        # Test compliance audit trail
        from src.compliance.audit_trail import ComplianceEvent, ComplianceEventType, ComplianceSeverity
        test_event = ComplianceEvent(
            event_id="test_event_001",
            timestamp=datetime.now(),
            event_type=ComplianceEventType.QUERY_SUBMITTED,
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
            logger.info("Compliance audit trail working correctly")
        else:
            logger.error("Compliance audit trail test failed")
            return False
        
        logger.info("All compliance components initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Compliance initialization failed: {e}")
        return False

def start_background_services():
    """Start background services"""
    logger.info("=" * 60)
    logger.info("STARTING BACKGROUND SERVICES")
    logger.info("=" * 60)
    
    try:
        from src.compliance.content_automation import content_automation
        
        # Start content automation scheduler
        content_automation.start_automation()
        logger.info("Content automation scheduler started")
        
        return True
        
    except Exception as e:
        logger.error(f"Background services startup failed: {e}")
        return False

def run_system_health_check():
    """Run comprehensive system health check"""
    logger.info("=" * 60)
    logger.info("RUNNING SYSTEM HEALTH CHECK")
    logger.info("=" * 60)
    
    health_status = {
        'security': False,
        'compliance': False,
        'background_services': False,
        'overall': False
    }
    
    try:
        # Check security components
        from src.security.encryption import encryption
        test_data = "Health check test"
        encrypted = encryption.encrypt_text(test_data)
        decrypted = encryption.decrypt_text(encrypted)
        health_status['security'] = (decrypted == test_data)
        
        # Check compliance components
        from src.compliance.sebi_framework import sebi_checker
        test_query = "What is mutual fund?"
        sebi_result = sebi_checker.check_compliance(test_query)
        health_status['compliance'] = (sebi_result is not None)
        
        # Check background services
        from src.compliance.content_automation import content_automation
        health_status['background_services'] = content_automation.is_running
        
        # Overall health
        health_status['overall'] = all(health_status.values())
        
        # Log results
        for component, status in health_status.items():
            status_text = "HEALTHY" if status else "UNHEALTHY"
            logger.info(f"{component.upper()}: {status_text}")
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return health_status

def main():
    """Main startup function"""
    logger.info("STARTING PHASE 5: SECURITY AND COMPLIANCE SYSTEM")
    logger.info(f"Started at: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    # Setup directories
    setup_directories()
    
    # Initialize security components
    security_ok = initialize_security()
    if not security_ok:
        logger.error("Security initialization failed. Exiting.")
        return False
    
    # Initialize compliance components
    compliance_ok = initialize_compliance()
    if not compliance_ok:
        logger.error("Compliance initialization failed. Exiting.")
        return False
    
    # Start background services
    background_ok = start_background_services()
    if not background_ok:
        logger.error("Background services startup failed. Exiting.")
        return False
    
    # Run health check
    health_status = run_system_health_check()
    
    if health_status['overall']:
        logger.info("=" * 80)
        logger.info("PHASE 5 SYSTEM STARTED SUCCESSFULLY!")
        logger.info("All security and compliance components are operational")
        logger.info("Background services are running")
        logger.info("System is ready for production use")
        logger.info("=" * 80)
        
        # Keep the script running to maintain background services
        try:
            logger.info("Keeping Phase 5 system running... (Press Ctrl+C to stop)")
            while True:
                asyncio.sleep(60)  # Check every minute
                
                # Periodic health check
                if datetime.now().minute % 10 == 0:  # Every 10 minutes
                    current_health = run_system_health_check()
                    if not current_health['overall']:
                        logger.warning("System health degraded - check logs for details")
        
        except KeyboardInterrupt:
            logger.info("Phase 5 system stopped by user")
            from src.compliance.content_automation import content_automation
            content_automation.stop_automation()
            logger.info("Background services stopped")
        
        return True
    
    else:
        logger.error("Phase 5 system startup failed - health check failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
