// API Service for Backend Communication

const APIService = {
    // Current session ID
    sessionId: null,
    
    // Request timeout
    timeout: 10000,
    lastSuccessfulRequestAt: 0,

    /**
     * Initialize API service
     */
    init() {
        this.sessionId = this.generateSessionId();
    },

    /**
     * Generate unique session ID
     * @returns {string} Session ID
     */
    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    },

    /**
     * Make API request with error handling
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Request options
     * @returns {Promise} API response
     */
    async makeRequest(endpoint, options = {}) {
        const url = `${APP_CONFIG.API_BASE_URL}${endpoint}`;
        
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': this.sessionId
            },
            timeout: this.timeout
        };

        const requestOptions = { ...defaultOptions, ...options };

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), requestOptions.timeout);

            const response = await fetch(url, {
                ...requestOptions,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            this.lastSuccessfulRequestAt = Date.now();
            return data;

        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            throw error;
        }
    },

    /**
     * Send chat message to backend
     * @param {string} message - User message
     * @returns {Promise} Chat response
     */
    async sendChatMessage(message) {
        // Additional validation to prevent empty messages
        if (!message || message.trim().length === 0) {
            throw new Error('Message cannot be empty');
        }
        
        if (message.trim().length < 3) {
            throw new Error('Message must be at least 3 characters long');
        }
        
        const validation = ValidationService.validateMessage(message);
        
        if (!validation.isValid) {
            throw new Error(validation.errors.join(', '));
        }

        const requestData = {
            query: message,
            session_id: this.sessionId,
            user_id: null // Could be implemented with user authentication
        };
        
        console.log('=== DEBUG: Frontend sending payload ===');
        console.log('Request data:', JSON.stringify(requestData, null, 2));

        try {
            const response = await this.makeRequest(APP_CONFIG.API_ENDPOINTS.CHAT, {
                method: 'POST',
                timeout: APP_CONFIG.CHAT_TIMEOUT,
                body: JSON.stringify(requestData)
            });

            const validation = ValidationService.validateApiResponse(response);
            
            if (!validation.isValid) {
                throw new Error('Invalid response from server');
            }

            return this.normalizeChatResponse(response);

        } catch (error) {
            console.error('Chat API error:', error);
            
            // Map different error types to user-friendly messages
            if (error.message.includes('timeout')) {
                throw new Error(ERROR_MESSAGES.TIMEOUT_ERROR);
            } else if (error.message.includes('Failed to fetch')) {
                throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
            } else if (error.message.includes('HTTP 429')) {
                throw new Error(ERROR_MESSAGES.RATE_LIMIT_ERROR);
            } else if (error.message.includes('HTTP 5')) {
                throw new Error(ERROR_MESSAGES.SERVER_ERROR);
            } else {
                throw error;
            }
        }
    },

    /**
     * Check API health status
     * @returns {Promise} Health status
     */
    async checkHealth() {
        try {
            const response = await this.makeRequest(APP_CONFIG.API_ENDPOINTS.HEALTH);
            return response;
        } catch (error) {
            console.error('Health check error:', error);
            throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
        }
    },

    /**
     * Get API statistics
     * @returns {Promise} API statistics
     */
    async getStats() {
        try {
            const response = await this.makeRequest(APP_CONFIG.API_ENDPOINTS.STATS);
            return response;
        } catch (error) {
            console.error('Stats API error:', error);
            throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
        }
    },

    /**
     * Test API connectivity
     * @returns {Promise<boolean}} Connection status
     */
    async testConnection() {
        try {
            await this.checkHealth();
            return true;
        } catch (error) {
            return Date.now() - this.lastSuccessfulRequestAt < 120000;
        }
    },

    /**
     * Get connection status with retry logic
     * @param {number} maxRetries - Maximum retry attempts
     * @param {number} retryDelay - Delay between retries in ms
     * @returns {Promise<boolean>} Connection status
     */
    async getConnectionStatus(maxRetries = 3, retryDelay = 1000) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                const isConnected = await this.testConnection();
                if (isConnected) {
                    return true;
                }
            } catch (error) {
                console.log(`Connection attempt ${attempt} failed:`, error.message);
            }
            
            if (attempt < maxRetries) {
                await new Promise(resolve => setTimeout(resolve, retryDelay));
            }
        }
        
        return false;
    },

    /**
     * Format chat request for API
     * @param {string} message - User message
     * @param {Object} metadata - Additional metadata
     * @returns {Object} Formatted request
     */
    formatChatRequest(message, metadata = {}) {
        return {
            query: message,
            session_id: this.sessionId,
            user_id: metadata.userId || null,
            metadata: {
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                ...metadata
            }
        };
    },

    /**
     * Handle API error responses
     * @param {Error} error - Error to handle
     * @returns {string} User-friendly error message
     */
    handleApiError(error) {
        const errorMessages = {
            'NetworkError': ERROR_MESSAGES.NETWORK_ERROR,
            'TimeoutError': ERROR_MESSAGES.NETWORK_ERROR,
            'ValidationError': ERROR_MESSAGES.VALIDATION_ERROR,
            'RateLimitError': ERROR_MESSAGES.RATE_LIMIT_ERROR,
            'ServerError': ERROR_MESSAGES.SERVER_ERROR
        };

        const errorType = error.name || 'UnknownError';
        return errorMessages[errorType] || ERROR_MESSAGES.UNKNOWN_ERROR;
    },

    /**
     * Normalize backend chat responses into the shape expected by the UI.
     * @param {Object} response - Backend response
     * @returns {Object} UI-friendly response
     */
    normalizeChatResponse(response) {
        const metadata = response.metadata || {};
        const sourceDocuments = Array.isArray(response.source_documents)
            ? response.source_documents
            : [];

        return {
            ...response,
            model_used: response.model_used || metadata.model_used || null,
            response_time: response.response_time ?? metadata.processing_time ?? null,
            sources: Array.isArray(response.sources)
                ? response.sources
                : sourceDocuments.map((sourceId, index) => {
                    const label = typeof sourceId === 'string'
                        ? sourceId.slice(0, 8)
                        : String(sourceId);
                    return `Document ${index + 1}: ${label}`;
                })
        };
    },

    /**
     * Retry failed request with exponential backoff
     * @param {Function} requestFunction - Function to retry
     * @param {number} maxRetries - Maximum retry attempts
     * @param {number} baseDelay - Base delay in ms
     * @returns {Promise} Request result
     */
    async retryRequest(requestFunction, maxRetries = 3, baseDelay = 1000) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                return await requestFunction();
            } catch (error) {
                if (attempt === maxRetries) {
                    throw error;
                }
                
                const delay = baseDelay * Math.pow(2, attempt - 1);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    },

    /**
     * Cancel ongoing requests
     */
    cancelRequests() {
        // Implementation for canceling ongoing requests
        // This would require tracking active requests
    },

    /**
     * Get request metrics
     * @returns {Object} Request metrics
     */
    getMetrics() {
        return {
            sessionId: this.sessionId,
            timeout: this.timeout,
            baseUrl: APP_CONFIG.API_BASE_URL
        };
    },

    /**
     * Update session ID
     */
    resetSession() {
        this.sessionId = this.generateSessionId();
    }
};

// Initialize API service
APIService.init();

// Export API service
window.APIService = APIService;
