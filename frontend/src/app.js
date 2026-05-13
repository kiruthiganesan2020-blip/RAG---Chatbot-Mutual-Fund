// Main Application

class HDFCMutualFundApp {
    constructor() {
        this.chatInterface = null;
        this.disclaimer = null;
        this.isInitialized = false;
        this.connectionCheckInterval = null;
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            console.log('Initializing HDFC Mutual Fund FAQ Assistant...');

            // Check browser support
            const browserSupport = ValidationService.checkBrowserSupport();
            if (!browserSupport.supported) {
                this.showBrowserCompatibilityError(browserSupport.unsupported);
                return;
            }

            // Initialize components
            await this.initializeComponents();

            // Setup global error handling
            this.setupErrorHandling();

            // Setup connection monitoring
            this.setupConnectionMonitoring();

            // Initialize disclaimer
            this.initializeDisclaimer();

            // Setup keyboard shortcuts
            this.setupKeyboardShortcuts();

            // Check API connection
            await this.checkInitialConnection();

            this.isInitialized = true;
            console.log('Application initialized successfully');

        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.showInitializationError(error);
        }
    }

    /**
     * Initialize all components
     */
    async initializeComponents() {
        // Initialize chat interface
        this.chatInterface = new ChatInterface();
        this.chatInterface.init();

        // Initialize disclaimer
        this.disclaimer = new Disclaimer();
        const disclaimerContainer = document.getElementById('disclaimer');
        if (disclaimerContainer) {
            this.disclaimer.init(disclaimerContainer);
        }
    }

    /**
     * Setup global error handling
     */
    setupErrorHandling() {
        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.showGlobalError('An unexpected error occurred. Please refresh the page.');
        });

        // Handle uncaught errors
        window.addEventListener('error', (event) => {
            console.error('Uncaught error:', event.error);
            this.showGlobalError('An unexpected error occurred. Please refresh the page.');
        });
    }

    /**
     * Setup connection monitoring
     */
    setupConnectionMonitoring() {
        // Check connection every 30 seconds
        this.connectionCheckInterval = setInterval(async () => {
            if (this.chatInterface && this.chatInterface.isTyping) {
                return;
            }

            try {
                const isConnected = await APIService.testConnection();
                this.chatInterface.updateConnectionStatus(isConnected);
            } catch (error) {
                console.error('Connection check failed:', error);
            }
        }, 120000);
    }

    /**
     * Initialize disclaimer
     */
    initializeDisclaimer() {
        if (this.disclaimer) {
            this.disclaimer.initialize();
        }
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to send message
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                if (this.chatInterface) {
                    this.chatInterface.handleSendMessage();
                }
            }

            // Escape to clear input
            if (e.key === 'Escape') {
                const messageInput = document.getElementById('messageInput');
                if (messageInput && document.activeElement === messageInput) {
                    messageInput.value = '';
                    this.chatInterface.updateCharCount();
                    this.chatInterface.updateSendButton();
                }
            }

            // Ctrl/Cmd + L to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                const messageInput = document.getElementById('messageInput');
                if (messageInput) {
                    messageInput.focus();
                    messageInput.select();
                }
            }
        });
    }

    /**
     * Check initial API connection
     */
    async checkInitialConnection() {
        try {
            const isConnected = await APIService.getConnectionStatus(3, 1000);
            if (isConnected) {
                console.log('API connection established');
                this.showConnectionSuccess();
            } else {
                console.warn('API connection failed');
                this.showConnectionError();
            }
        } catch (error) {
            console.error('Initial connection check failed:', error);
            this.showConnectionError();
        }
    }

    /**
     * Show browser compatibility error
     * @param {Array} unsupportedFeatures - Unsupported features
     */
    showBrowserCompatibilityError(unsupportedFeatures) {
        const errorContainer = document.createElement('div');
        errorContainer.className = 'fixed inset-0 bg-red-50 flex items-center justify-center z-50 p-4';
        errorContainer.innerHTML = `
            <div class="bg-white rounded-lg shadow-xl p-6 max-w-md w-full">
                <div class="flex items-center mb-4">
                    <svg class="w-6 h-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <h2 class="text-xl font-semibold text-red-800">Browser Not Supported</h2>
                </div>
                <p class="text-gray-700 mb-4">
                    Your browser doesn't support some required features: ${unsupportedFeatures.join(', ')}.
                </p>
                <p class="text-gray-600 mb-4">
                    Please update your browser to the latest version or try a different browser.
                </p>
                <button onclick="window.location.reload()" class="w-full bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700">
                    Reload Page
                </button>
            </div>
        `;
        document.body.appendChild(errorContainer);
    }

    /**
     * Show initialization error
     * @param {Error} error - Initialization error
     */
    showInitializationError(error) {
        const errorContainer = document.createElement('div');
        errorContainer.className = 'fixed inset-0 bg-gray-50 flex items-center justify-center z-50 p-4';
        errorContainer.innerHTML = `
            <div class="bg-white rounded-lg shadow-xl p-6 max-w-md w-full">
                <div class="flex items-center mb-4">
                    <svg class="w-6 h-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <h2 class="text-xl font-semibold text-red-800">Application Error</h2>
                </div>
                <p class="text-gray-700 mb-4">
                    Failed to initialize the application. Please refresh the page and try again.
                </p>
                <details class="mb-4">
                    <summary class="text-sm text-gray-600 cursor-pointer">Error Details</summary>
                    <pre class="text-xs text-gray-500 mt-2 bg-gray-100 p-2 rounded overflow-auto">${error.message}</pre>
                </details>
                <button onclick="window.location.reload()" class="w-full bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700">
                    Reload Page
                </button>
            </div>
        `;
        document.body.appendChild(errorContainer);
    }

    /**
     * Show global error message
     * @param {string} message - Error message
     */
    showGlobalError(message) {
        if (this.chatInterface) {
            this.chatInterface.showError(message);
        }
    }

    /**
     * Show connection success message
     */
    showConnectionSuccess() {
        console.log('Connected to HDFC Mutual Fund API');
    }

    /**
     * Show connection error message
     */
    showConnectionError() {
        if (this.chatInterface) {
            this.chatInterface.addSystemMessage('Unable to connect to the server. Some features may not work properly.');
        }
    }

    /**
     * Get application status
     * @returns {Object} Application status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            chatInterface: this.chatInterface ? 'initialized' : 'not initialized',
            disclaimer: this.disclaimer ? 'initialized' : 'not initialized',
            connectionMonitoring: this.connectionCheckInterval ? 'active' : 'inactive'
        };
    }

    /**
     * Cleanup application resources
     */
    cleanup() {
        if (this.connectionCheckInterval) {
            clearInterval(this.connectionCheckInterval);
            this.connectionCheckInterval = null;
        }
        
        // Cancel any ongoing API requests
        APIService.cancelRequests();
        
        console.log('Application cleanup completed');
    }

    /**
     * Restart application
     */
    async restart() {
        this.cleanup();
        await this.init();
    }

    /**
     * Get application metrics
     * @returns {Object} Application metrics
     */
    getMetrics() {
        const metrics = {
            app: {
                initialized: this.isInitialized,
                uptime: this.getUptime(),
                version: '1.0.0'
            },
            chat: this.chatInterface ? this.chatInterface.getChatStats() : null,
            api: APIService.getMetrics()
        };

        return metrics;
    }

    /**
     * Get application uptime
     * @returns {number} Uptime in seconds
     */
    getUptime() {
        if (!this.startTime) {
            this.startTime = Date.now();
        }
        return Math.floor((Date.now() - this.startTime) / 1000);
    }

    /**
     * Export application data
     * @returns {Object} Application data
     */
    exportData() {
        return {
            chatHistory: this.chatInterface ? this.chatInterface.exportChatHistory() : [],
            metrics: this.getMetrics(),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Import application data
     * @param {Object} data - Application data to import
     */
    importData(data) {
        if (data.chatHistory && this.chatInterface) {
            this.chatInterface.importChatHistory(data.chatHistory);
        }
    }

    /**
     * Show about dialog
     */
    showAboutDialog() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');

        modal.innerHTML = `
            <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
                <h2 class="text-xl font-semibold text-gray-900 mb-4">About HDFC Mutual Fund FAQ Assistant</h2>
                <div class="space-y-3 text-sm text-gray-600">
                    <p><strong>Version:</strong> 1.0.0</p>
                    <p><strong>Description:</strong> AI-powered FAQ assistant for HDFC Mutual Funds</p>
                    <p><strong>Features:</strong></p>
                    <ul class="list-disc list-inside ml-4 space-y-1">
                        <li>Factual information about HDFC mutual funds</li>
                        <li>Privacy-aware responses</li>
                        <li>Source citations and verification</li>
                        <li>Real-time API integration</li>
                    </ul>
                    <p><strong>Disclaimer:</strong> This assistant provides factual information only and does not offer investment advice.</p>
                </div>
                <button onclick="this.closest('.fixed').remove()" class="mt-6 w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700">
                    Close
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        // Close on Escape
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    const app = new HDFCMutualFundApp();
    await app.init();

    // Make app globally available
    window.HDFCApp = app;

    // Add global error handler for development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
        });
    }
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.HDFCApp) {
        window.HDFCApp.cleanup();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HDFCMutualFundApp;
}
