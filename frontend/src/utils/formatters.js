// Utility Functions for Formatting and Display

const Formatters = {
    /**
     * Format timestamp to readable string
     * @param {Date|string} timestamp - Timestamp to format
     * @returns {string} Formatted time string
     */
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) {
            return 'Just now';
        } else if (diffMins < 60) {
            return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
        } else if (diffMins < 1440) {
            const hours = Math.floor(diffMins / 60);
            return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        } else {
            return date.toLocaleDateString();
        }
    },

    /**
     * Format confidence score to percentage
     * @param {number} confidence - Confidence score (0-1)
     * @returns {string} Formatted confidence percentage
     */
    formatConfidence(confidence) {
        if (typeof confidence !== 'number' || confidence < 0 || confidence > 1) {
            return '0%';
        }
        return `${Math.round(confidence * 100)}%`;
    },

    /**
     * Format response time
     * @param {number} responseTime - Response time in seconds
     * @returns {string} Formatted response time
     */
    formatResponseTime(responseTime) {
        if (typeof responseTime !== 'number') {
            return '0.0s';
        }
        
        if (responseTime < 1) {
            return `${Math.round(responseTime * 1000)}ms`;
        } else {
            return `${responseTime.toFixed(1)}s`;
        }
    },

    /**
     * Truncate text with ellipsis
     * @param {string} text - Text to truncate
     * @param {number} maxLength - Maximum length
     * @returns {string} Truncated text
     */
    truncateText(text, maxLength = 100) {
        if (!text || text.length <= maxLength) {
            return text;
        }
        return text.substring(0, maxLength) + '...';
    },

    /**
     * Format intent type for display
     * @param {string} intent - Intent type
     * @returns {string} Formatted intent
     */
    formatIntent(intent) {
        const intentMap = {
            'factual': 'Factual Question',
            'advisory': 'Advisory Question',
            'unknown': 'Unknown Intent'
        };
        return intentMap[intent] || 'Unknown Intent';
    },

    /**
     * Format model name for display
     * @param {string} model - Model identifier
     * @returns {string} Formatted model name
     */
    formatModel(model) {
        const modelMap = {
            'gemini-pro': 'Google Gemini Pro',
            'fallback': 'Fallback Model'
        };
        return modelMap[model] || model;
    },

    /**
     * Format source name for display
     * @param {string} source - Source identifier
     * @returns {string} Formatted source name
     */
    formatSource(source) {
        const sourceMap = {
            'hdfc': 'HDFC Mutual Fund',
            'amfi': 'AMFI India',
            'sebi': 'SEBI',
            'groww': 'Groww',
            'unknown': 'Unknown Source'
        };
        return sourceMap[source] || source;
    },

    /**
     * Sanitize HTML content
     * @param {string} text - Text to sanitize
     * @returns {string} Sanitized text
     */
    sanitizeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Format message content with proper line breaks
     * @param {string} text - Text to format
     * @returns {string} Formatted text
     */
    formatMessageContent(text) {
        if (!text) return '';
        
        // Convert newlines to <br> tags
        return text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    },

    /**
     * Generate a unique ID for messages
     * @returns {string} Unique ID
     */
    generateId() {
        return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    },

    /**
     * Format file size
     * @param {number} bytes - Size in bytes
     * @returns {string} Formatted file size
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    /**
     * Capitalize first letter of each word
     * @param {string} text - Text to capitalize
     * @returns {string} Capitalized text
     */
    capitalizeWords(text) {
        if (!text) return '';
        return text.replace(/\b\w/g, char => char.toUpperCase());
    },

    /**
     * Format error message for display
     * @param {Error|string} error - Error to format
     * @returns {string} Formatted error message
     */
    formatError(error) {
        if (typeof error === 'string') {
            return error;
        }
        
        if (error && error.message) {
            return error.message;
        }
        
        return 'An unknown error occurred';
    },

    /**
     * Check if text contains URLs
     * @param {string} text - Text to check
     * @returns {boolean} Whether text contains URLs
     */
    containsURL(text) {
        const urlPattern = /(https?:\/\/[^\s]+)/g;
        return urlPattern.test(text);
    },

    /**
     * Extract URLs from text
     * @param {string} text - Text to extract URLs from
     * @returns {string[]} Array of URLs
     */
    extractURLs(text) {
        const urlPattern = /(https?:\/\/[^\s]+)/g;
        return text.match(urlPattern) || [];
    },

    /**
     * Format URLs as clickable links
     * @param {string} text - Text containing URLs
     * @returns {string} Text with formatted URLs
     */
    formatURLs(text) {
        const urlPattern = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlPattern, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">$1</a>');
    }
};

// Export formatters
window.Formatters = Formatters;
