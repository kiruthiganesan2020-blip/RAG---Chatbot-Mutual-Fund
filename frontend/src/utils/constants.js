// Application Constants
const APP_CONFIG = {
    // API Configuration
    API_BASE_URL: 'http://localhost:8000',
    API_ENDPOINTS: {
        CHAT: '/api/chat',
        HEALTH: '/api/health',
        STATS: '/api/stats'
    },
    
    // UI Configuration
    MAX_MESSAGE_LENGTH: 500,
    CHAT_TIMEOUT: 120000,
    TYPING_DELAY: 1000,
    ANIMATION_DURATION: 300,
    
    // Message Types
    MESSAGE_TYPES: {
        USER: 'user',
        ASSISTANT: 'assistant',
        SYSTEM: 'system',
        ERROR: 'error'
    },
    
    // Intent Types
    INTENT_TYPES: {
        FACTUAL: 'factual',
        ADVISORY: 'advisory',
        ENTITY_SPECIFIC: 'entity_specific',
        COMPARISON: 'comparison',
        PROCEDURAL: 'procedural',
        UNKNOWN: 'unknown'
    },
    
    // Source Types
    SOURCE_TYPES: {
        HDFC: 'hdfc',
        AMFI: 'amfi',
        SEBI: 'sebi',
        GROWW: 'groww',
        UNKNOWN: 'unknown'
    },
    
    // Model Types
    MODEL_TYPES: {
        GEMINI_PRO: 'gemini-pro',
        FALLBACK: 'fallback'
    },
    
    // Colors and Styling
    COLORS: {
        PRIMARY: '#3b82f6',
        SECONDARY: '#6b7280',
        SUCCESS: '#10b981',
        WARNING: '#f59e0b',
        ERROR: '#ef4444',
        INFO: '#06b6d4'
    },
    
    // Accessibility
    ARIA_LABELS: {
        SEND_BUTTON: 'Send message',
        CLEAR_CHAT: 'Clear chat history',
        TYPING_INDICATOR: 'Assistant is typing',
        MESSAGE_INPUT: 'Type your message',
        SOURCE_CITATION: 'Source citation'
    }
};

// Error Messages
const ERROR_MESSAGES = {
    NETWORK_ERROR: 'Unable to connect to the server. Please check your internet connection.',
    TIMEOUT_ERROR: 'The assistant is taking longer than expected. Please try again in a moment.',
    SERVER_ERROR: 'Server error occurred. Please try again later.',
    VALIDATION_ERROR: 'Please enter a valid message.',
    RATE_LIMIT_ERROR: 'Too many requests. Please wait a moment.',
    EMPTY_RESPONSE: 'No response received. Please try again.',
    UNKNOWN_ERROR: 'An unexpected error occurred. Please try again.'
};

// Success Messages
const SUCCESS_MESSAGES = {
    MESSAGE_SENT: 'Message sent successfully',
    CONNECTION_ESTABLISHED: 'Connected to server',
    CHAT_CLEARED: 'Chat history cleared'
};

// Sample Questions for Suggestions
const SAMPLE_QUESTIONS = [
    'What is HDFC Large Cap Fund?',
    'How do mutual funds work?',
    'What is the current NAV of HDFC Mid Cap Fund?',
    'What are the risks of investing in mutual funds?',
    'How can I invest in HDFC mutual funds?'
];

// Export constants
window.APP_CONFIG = APP_CONFIG;
window.ERROR_MESSAGES = ERROR_MESSAGES;
window.SUCCESS_MESSAGES = SUCCESS_MESSAGES;
window.SAMPLE_QUESTIONS = SAMPLE_QUESTIONS;
