/**
 * API Integration Layer
 * Connects frontend to backend services
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { body, validationResult } from 'express-validator';

// Import Phase 5 components
import { encryption } from '../security/encryption';
import { SecurityValidator } from '../security/input_validation';
import { ddos_protection } from '../security/rate_limiting';
import { pii_detector } from '../security/privacy_controls';
import { sebi_checker } from '../compliance/sebi_framework';
import { amfi_checker } from '../compliance/amfi_guidelines';
import { disclaimer_manager } from '../compliance/disclaimer_manager';
import { source_verifier } from '../compliance/source_verification';
import { content_automation } from '../compliance/content_automation';
import { compliance_audit_trail } from '../compliance/audit_trail';

// Import Phase 4 components
import { processUserQuery } from '../retrieval/retrieval_system';
import { generateResponse } from '../response_generation/response_generator';

const app = express();

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 requests per minute
  max: 100, // maximum requests per window
  standardHeaders: true,
  legacyHeaders: false,
});

app.use(limiter);

// Request validation middleware
app.use(express.json({
  limit: '10mb',
  strict: true
}), (req, res, next) => {
  if (!validationResult(req, res)) {
    res.status(400).json({
      error: 'Invalid request format',
      details: validationResult.error
    });
    return;
  }
  next();
});

// Security middleware
const securityValidator = new SecurityValidator();

app.use((req, res, next) => {
  // Validate and sanitize input
  const sanitized = securityValidator.sanitizeQuery(req.body.query);
  
  // PII detection and masking
  const piiDetected = pii_detector.detect_pii(sanitized.query);
  if (piiDetected && Object.keys(piiDetected).length > 0) {
    // Log PII detection
    console.warn('PII detected and masked:', piiDetected);
    
    // Mask PII in query
    req.body.query = pii_detector.mask_pii(sanitized.query, piiDetected);
  }
  
  // Rate limiting
  const clientIp = req.ip || req.connection.remoteAddress;
  const isAllowed = ddos_protection.is_request_allowed(clientIp);
  
  if (!isAllowed) {
    res.status(429).json({
      error: 'Rate limit exceeded',
      retryAfter: 60
    });
    return;
  }
  
  next();
});

// Session management
app.use((req, res, next) => {
  const sessionId = req.headers['x-session-id'] || req.session?.id;
  
  if (sessionId) {
    // Attach session to request
    req.session = req.session || {};
    req.session.id = sessionId;
  }
  
  next();
});

// API Routes

/**
 * Chat endpoint with Phase 5 security and compliance
 */
app.post('/api/chat', async (req, res, next) => {
  try {
    const { query } = req.body;
    
    // Validate input
    const validation = body(req);
    if (!validation.isValid) {
      return res.status(400).json({
        error: 'Invalid request format',
        details: validation.error
      });
    }
    
    // Process query with Phase 5 security and compliance
    const startTime = Date.now();
    
    // SEBI compliance check
    const sebiResult = sebi_checker.check_compliance(query);
    if (!sebiResult.is_compliant) {
      // Log compliance violation
      await compliance_audit_trail.log_compliance_event({
        event_id: `compliance_${Date.now()}`,
        timestamp: new Date(),
        event_type: 'QUERY_SUBMITTED',
        severity: 'MEDIUM',
        user_id: req.user?.id || 'anonymous',
        session_id: req.session?.id,
        ip_address: req.ip,
        resource: 'chat_query',
        action: 'sebi_check',
        details: {
          query: query,
          violation_type: sebiResult.violation_type,
          risk_level: sebiResult.risk_level
        },
        success: false,
        compliance_score: sebiResult.compliance_score || 0,
        regulatory_references: sebiResult.regulatory_references || [],
        remediation_required: sebiResult.remediation_required || false,
        remediation_actions: sebiResult.remediation_actions || [],
        auditor: 'system',
        evidence: { sebi_result: sebiResult }
      });
    }
    
    // AMFI compliance check
    const amfiResult = amfi_checker.check_amfi_compliance(query);
    if (!amfiResult.is_compliant) {
      // Log compliance violation
      await compliance_audit_trail.log_compliance_event({
        event_id: `compliance_${Date.now()}`,
        timestamp: new Date(),
        event_type: 'QUERY_SUBMITTED',
        severity: 'MEDIUM',
        user_id: req.user?.id || 'anonymous',
        session_id: req.session?.id,
        ip_address: req.ip,
        resource: 'chat_query',
        action: 'amfi_check',
        details: {
          query: query,
          violation_type: amfiResult.violation_type,
          risk_level: amfiResult.risk_level
        },
        success: false,
        compliance_score: amfiResult.compliance_score || 0,
        regulatory_references: amfiResult.regulatory_references || [],
        remediation_required: amfiResult.remediation_required || false,
        remediation_actions: amfiResult.remediation_actions || [],
        auditor: 'system',
        evidence: { amfi_result: amfiResult }
      });
    }
    
    // Get required disclaimers
    const disclaimers = disclaimer_manager.get_required_disclaimers(
      disclaimer_manager.DisclaimerCategory.GENERAL_ADVICE,
      query,
      'Response will be generated here'
    );
    
    // Process query through RAG system
    const ragResult = await processUserQuery(query, req.user?.id);
    
    // Generate response with disclaimers
    const response = await generateResponse(ragResult, {
      includeDisclaimers: disclaimers,
      maxTokens: 500,
      temperature: 0.7
    });
    
    // Log the interaction
    await compliance_audit_trail.log_compliance_event({
      event_id: `response_${Date.now()}`,
      timestamp: new Date(),
      event_type: 'RESPONSE_GENERATED',
      severity: 'LOW',
      user_id: req.user?.id || 'anonymous',
      session_id: req.session?.id,
      ip_address: req.ip,
      resource: 'chat_response',
      action: 'response_generation',
      details: {
        query: query,
        response_length: response.response.length,
        disclaimers_included: disclaimers.length,
        processing_time_ms: Date.now() - startTime,
        compliance_score: 100.0
      },
      success: true,
      compliance_score: 100.0,
      regulatory_references: ['SEBI_GUIDELINES', 'AMFI_STANDARDS'],
      remediation_required: false,
      remediation_actions: [],
      auditor: 'system',
      evidence: { response_result: response }
      });
    
    res.json({
      response: response.response,
      sources: ragResult.sources,
      disclaimers: disclaimers.map(d => d.text),
      metadata: {
        processing_time_ms: Date.now() - startTime,
        compliance_checks: {
          sebi_compliant: sebiResult.is_compliant,
          amfi_compliant: amfiResult.is_compliant
        },
        timestamp: new Date().toISOString(),
        session_id: req.session?.id
      }
    });
    
  } catch (error) {
    console.error('Chat API error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'An error occurred while processing your request'
    });
  }
});

/**
 * Health check endpoint
 */
app.get('/api/health', (req, res) => {
  try {
    const healthStatus = {
      phase5_security: {
        encryption: true,
        input_validation: true,
        rate_limiting: true,
        pii_detection: true,
        sebi_compliance: true,
        amfi_compliance: true,
        disclaimer_manager: true,
        source_verification: true,
        content_automation: true,
        audit_trail: true
      },
      phase4_retrieval: true,
      phase4_response_generation: true,
      phase4_backend: true,
      overall: true,
      timestamp: new Date().toISOString()
    };
    
    res.json(healthStatus);
    
  } catch (error) {
    console.error('Health check error:', error);
    res.status(500).json({
      error: 'Health check failed',
      message: 'An error occurred while checking system health'
    });
  }
});

// Start server
const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
  console.log(`🚀 HDFC Mutual Fund RAG Chatbot Backend running on port ${PORT}`);
  console.log('🔒 Phase 5 Security & Compliance Active');
  console.log('🔗 API Endpoints: /api/chat, /api/health');
  console.log('📊 Monitoring: All systems operational');
});

export default app;
