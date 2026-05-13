// Validation Service for Frontend

const ValidationService = {
    /**
     * Validate user message input
     * @param {string} message - Message to validate
     * @returns {Object} Validation result
     */
    validateMessage(message) {
        const result = {
            isValid: true,
            errors: [],
            warnings: []
        };

        // Check if message is empty
        if (!message || message.trim().length === 0) {
            result.isValid = false;
            result.errors.push('Message cannot be empty');
            return result;
        }

        const trimmedMessage = message.trim();

        // Check minimum length
        if (trimmedMessage.length < 3) {
            result.isValid = false;
            result.errors.push('Message must be at least 3 characters long');
        }

        // Check maximum length
        if (trimmedMessage.length > APP_CONFIG.MAX_MESSAGE_LENGTH) {
            result.isValid = false;
            result.errors.push(`Message cannot exceed ${APP_CONFIG.MAX_MESSAGE_LENGTH} characters`);
        }

        // Check for potentially sensitive information
        if (this.containsSensitiveInfo(trimmedMessage)) {
            result.warnings.push('Message may contain sensitive information');
        }

        // Check for investment advice requests
        if (this.containsInvestmentAdviceRequest(trimmedMessage)) {
            result.warnings.push('Investment advice questions will be redirected to educational resources');
        }

        return result;
    },

    /**
     * Validate API response
     * @param {Object} response - API response to validate
     * @returns {Object} Validation result
     */
    validateApiResponse(response) {
        const result = {
            isValid: true,
            errors: [],
            warnings: []
        };

        // Check if response exists
        if (!response) {
            result.isValid = false;
            result.errors.push('No response received');
            return result;
        }

        // Check required fields
        const requiredFields = ['response', 'confidence', 'intent'];
        for (const field of requiredFields) {
            if (!(field in response)) {
                result.isValid = false;
                result.errors.push(`Missing required field: ${field}`);
            }
        }

        // Validate confidence score
        if (response.confidence !== undefined) {
            if (typeof response.confidence !== 'number' || response.confidence < 0 || response.confidence > 1) {
                result.warnings.push('Invalid confidence score');
            }
        }

        // Validate intent
        if (response.intent && !Object.values(APP_CONFIG.INTENT_TYPES).includes(response.intent)) {
            result.warnings.push('Unknown intent type');
        }

        // Validate response content
        if (response.response && typeof response.response !== 'string') {
            result.isValid = false;
            result.errors.push('Invalid response content');
        }

        return result;
    },

    /**
     * Check if message contains sensitive information
     * @param {string} message - Message to check
     * @returns {boolean} Whether message contains sensitive info
     */
    containsSensitiveInfo(message) {
        const sensitivePatterns = [
            /\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/, // Credit card numbers
            /\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b/, // SSN pattern
            /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, // Email addresses
            /\b\d{10,}\b/, // Long numbers (phone, account numbers)
            /\bpassword\b/i,
            /\bsecret\b/i,
            /\bconfidential\b/i
        ];

        return sensitivePatterns.some(pattern => pattern.test(message));
    },

    /**
     * Check if message contains investment advice request
     * @param {string} message - Message to check
     * @returns {boolean} Whether message requests investment advice
     */
    containsInvestmentAdviceRequest(message) {
        const advicePatterns = [
            /\bshould i invest\b/i,
            /\brecommend\b/i,
            /\bbest fund\b/i,
            /\badvice\b/i,
            /\bsuggest\b/i,
            /\bwhich fund to buy\b/i,
            /\bgood investment\b/i,
            /\bshould i buy\b/i,
            /\bshould i sell\b/i
        ];

        return advicePatterns.some(pattern => pattern.test(message));
    },

    /**
     * Validate email format
     * @param {string} email - Email to validate
     * @returns {boolean} Whether email is valid
     */
    validateEmail(email) {
        const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$/;
        return emailPattern.test(email);
    },

    /**
     * Validate phone number format
     * @param {string} phone - Phone number to validate
     * @returns {boolean} Whether phone number is valid
     */
    validatePhone(phone) {
        const phonePattern = /^\+?[\d\s\-\(\)]+$/;
        return phonePattern.test(phone) && phone.replace(/\D/g, '').length >= 10;
    },

    /**
     * Sanitize user input
     * @param {string} input - Input to sanitize
     * @returns {string} Sanitized input
     */
    sanitizeInput(input) {
        if (!input) return '';
        
        return input
            .replace(/[<>]/g, '') // Remove HTML tags
            .replace(/javascript:/gi, '') // Remove javascript protocol
            .replace(/on\w+=/gi, ''); // Remove event handlers
    },

    /**
     * Validate URL format
     * @param {string} url - URL to validate
     * @returns {boolean} Whether URL is valid
     */
    validateURL(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    },

    /**
     * Check if message is too long for processing
     * @param {string} message - Message to check
     * @returns {boolean} Whether message is too long
     */
    isMessageTooLong(message) {
        return message.length > APP_CONFIG.MAX_MESSAGE_LENGTH;
    },

    /**
     * Get character count for message
     * @param {string} message - Message to count
     * @returns {number} Character count
     */
    getCharacterCount(message) {
        return message ? message.length : 0;
    },

    /**
     * Validate chat history for storage
     * @param {Array} chatHistory - Chat history to validate
     * @returns {Object} Validation result
     */
    validateChatHistory(chatHistory) {
        const result = {
            isValid: true,
            errors: [],
            warnings: []
        };

        if (!Array.isArray(chatHistory)) {
            result.isValid = false;
            result.errors.push('Chat history must be an array');
            return result;
        }

        // Check each message
        chatHistory.forEach((message, index) => {
            if (!message.id) {
                result.warnings.push(`Message ${index + 1} missing ID`);
            }
            
            if (!message.type || !Object.values(APP_CONFIG.MESSAGE_TYPES).includes(message.type)) {
                result.warnings.push(`Message ${index + 1} has invalid type`);
            }
            
            if (!message.content || typeof message.content !== 'string') {
                result.warnings.push(`Message ${index + 1} has invalid content`);
            }
            
            if (!message.timestamp) {
                result.warnings.push(`Message ${index + 1} missing timestamp`);
            }
        });

        return result;
    },

    /**
     * Check if browser supports required features
     * @returns {Object} Feature support status
     */
    checkBrowserSupport() {
        const features = {
            fetch: typeof fetch !== 'undefined',
            localStorage: typeof localStorage !== 'undefined',
            sessionStorage: typeof sessionStorage !== 'undefined',
            webSockets: typeof WebSocket !== 'undefined',
            promises: typeof Promise !== 'undefined',
            asyncAwait: (async () => {}) instanceof Function
        };

        const unsupported = Object.keys(features).filter(key => !features[key]);
        
        return {
            supported: unsupported.length === 0,
            features,
            unsupported
        };
    },

    /**
     * Validate API endpoint configuration
     * @param {string} endpoint - API endpoint to validate
     * @returns {boolean} Whether endpoint is valid
     */
    validateApiEndpoint(endpoint) {
        if (!endpoint || typeof endpoint !== 'string') {
            return false;
        }

        try {
            const url = new URL(endpoint);
            return ['http:', 'https:'].includes(url.protocol);
        } catch {
            return false;
        }
    }
};

// Export validation service
window.ValidationService = ValidationService;
