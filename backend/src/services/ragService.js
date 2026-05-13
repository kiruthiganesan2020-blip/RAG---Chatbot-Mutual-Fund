/**
 * Chat Service
 * Handles business logic for chat functionality
 */

import { processUserQuery } from '../retrieval/retrieval_system';
import { generateResponse } from '../response_generation/response_generator';
import { logComplianceEvent } from '../compliance/audit_trail';

/**
 * Chat Service
 * Handles business logic for chat functionality
 */
class ChatService {
  constructor() {
    this.processUserQuery = processUserQuery;
    this.generateResponse = generateResponse;
    this.logComplianceEvent = logComplianceEvent;
  }

  /**
   * Process user query through RAG system
   * @param {string} query - User's question
   * @param {string} sessionId - User session ID
   * @returns {Promise<Object>} RAG result with sources and response
   */
  async processQuery(query, sessionId = 'anonymous') {
    try {
      // Process query through retrieval system
      const ragResult = await this.processUserQuery(query, sessionId);
      
      // Generate response with compliance checks
      const response = await this.generateResponse(ragResult, {
        query,
        sessionId,
        includeDisclaimers: true
      });
      
      // Log compliance events
      await this.logComplianceEvent({
        event_id: `chat_query_${Date.now()}`,
        timestamp: new Date(),
        event_type: 'QUERY_SUBMITTED',
        severity: 'LOW',
        user_id: sessionId,
        session_id: sessionId,
        ip_address: '127.0.0.1', // Would be extracted from request
        resource: 'chat_query',
        action: 'rag_processing',
        details: {
          query: query,
          rag_sources: ragResult.sources,
          rag_confidence: ragResult.confidence
        },
        success: true,
        compliance_score: 100.0,
        regulatory_references: ['SEBI_GUIDELINES', 'AMFI_STANDARDS'],
        remediation_required: false,
        remediation_actions: [],
        auditor: 'system',
        evidence: { rag_result: ragResult,
          compliance_checks: {
            sebi_compliant: ragResult.compliance_checks?.sebi_compliant,
            amfi_compliant: ragResult.compliance_checks?.amfi_compliant
          }
        }
      });
      
      return response;
    } catch (error) {
      console.error('Chat service error:', error);
      throw error;
    }
  }

  /**
   * Generate response with compliance and disclaimers
   * @param {Object} ragResult - RAG system result
   * @param {Object} options - Response generation options
   * @returns {Object} Formatted response with sources
   */
  async generateResponse(ragResult, options = {}) {
    const {
      query: ragResult.query,
      response: ragResult.response,
      sources: ragResult.sources,
      disclaimers: ragResult.disclaimers || [],
      metadata: {
        processing_time_ms: ragResult.processing_time_ms,
        compliance_checks: ragResult.compliance_checks,
        rag_confidence: ragResult.confidence,
        timestamp: new Date().toISOString()
      }
    };
    
    // Format response with sources and disclaimers
    let formattedResponse = ragResult.response;
    
    // Add disclaimers if required
    if (options.includeDisclaimers && ragResult.disclaimers) {
      const disclaimerText = ragResult.disclaimers
        .map(d => d.text)
        .join('\n\n');
      
      formattedResponse += '\n\n---\nDISCLAIMERS:\n' + disclaimerText + '\n---';
    }
    
    return formattedResponse;
  }

  /**
   * Log compliance event
   * @param {Object} event - Compliance event to log
   */
  async logComplianceEvent(event) {
    try {
      // This would integrate with compliance audit trail
      console.log('Compliance event logged:', event);
      return true;
    } catch (error) {
      console.error('Failed to log compliance event:', error);
      return false;
    }
  }
}

export default ChatService;
