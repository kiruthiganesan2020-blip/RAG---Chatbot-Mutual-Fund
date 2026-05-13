// Chat Interface Component - Fixed Version

class ChatInterface {
    constructor() {
        this.messageInput = null;
        this.sendButton = null;
        this.clearButton = null;
        this.messagesArea = null;
        this.charCountElement = null;
        this.messageDisplay = null;
        this.isTyping = false;
        this.currentMessageId = null;
    }

    /**
     * Initialize chat interface
     */
    init() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendBtn');
        this.clearButton = document.getElementById('clearChatBtn');
        this.messagesArea = document.getElementById('messagesArea');
        this.charCountElement = document.getElementById('charCount');

        // Initialize message display
        this.messageDisplay = new MessageDisplay();
        this.messageDisplay.init(this.messagesArea);

        // Setup event listeners
        this.setupEventListeners();

        // Setup input validation
        this.setupInputValidation();

        // Focus on input
        this.messageInput.focus();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Get form element
        const chatForm = document.getElementById('chatForm');
        
        // Handle form submission (prevents duplicate events)
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('Form submit triggered');
            this.handleSendMessage();
        });

        // Send button click - REMOVE TO PREVENT DUPLICATES
        // this.sendButton.addEventListener('click', (e) => {
        //     e.preventDefault();
        //     e.stopPropagation();
        //     this.handleSendMessage();
        // }, { once: false });

        // Clear button click
        this.clearButton.addEventListener('click', () => {
            this.handleClearChat();
        });

        // Enter key to send (Shift+Enter for new line) - REMOVED TO PREVENT DUPLICATES
        // this.messageInput.addEventListener('keydown', (e) => {
        //     if (e.key === 'Enter' && !e.shiftKey) {
        //         e.preventDefault();
        //         e.stopPropagation();
        //         this.handleSendMessage();
        //     }
        // });

        // Input change events
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.updateSendButton();
            this.autoResizeTextarea();
        });

        // Paste event
        this.messageInput.addEventListener('paste', (e) => {
            setTimeout(() => {
                this.updateCharCount();
                this.updateSendButton();
                this.autoResizeTextarea();
            }, 0);
        });
    }

    /**
     * Handle send message
     */
    async handleSendMessage() {
        // Prevent multiple submissions
        if (this.isTyping) {
            return;
        }

        const rawMessage = this.messageInput.value;
        const message = rawMessage.trim();
        
        // If message is empty, just return without showing error if it's a likely double-trigger
        if (!message) {
            return;
        }
        
        // Set typing state immediately
        this.isTyping = true;
        
        // Check minimum length
        if (message.length < 3) {
            this.showError('Message must be at least 3 characters long');
            this.isTyping = false;
            return;
        }

        // Clear input immediately to prevent duplicate submissions
        this.messageInput.value = '';
        this.updateCharCount();
        this.updateSendButton();

        // Set typing state
        this.isTyping = true;
        this.setInputState(false);

        console.log('All validations passed, sending message:', `"${message}"`);

        // Add user message
        const userMessage = {
            id: Formatters.generateId(),
            type: APP_CONFIG.MESSAGE_TYPES.USER,
            content: message,
            timestamp: new Date()
        };

        this.messageDisplay.addMessage(userMessage);

        // Clear input
        this.messageInput.value = '';
        this.updateCharCount();
        this.updateSendButton();
        this.autoResizeTextarea();

        // Disable input during processing
        this.setInputState(false);

        try {
            // Show typing indicator
            this.messageDisplay.showTypingIndicator();

            // Send message to API
            const response = await APIService.sendChatMessage(message);

            // Hide typing indicator
            this.messageDisplay.hideTypingIndicator();

            // Add assistant response
            const assistantMessage = {
                id: Formatters.generateId(),
                type: APP_CONFIG.MESSAGE_TYPES.ASSISTANT,
                content: response.response,
                timestamp: new Date(),
                confidence: response.confidence,
                intent: response.intent,
                modelUsed: response.model_used,
                responseTime: response.response_time,
                sources: response.sources
            };

            const messageElement = this.messageDisplay.addMessage(assistantMessage);

            // Add sources if available
            if (response.sources && response.sources.length > 0) {
                this.messageDisplay.addSources(assistantMessage.id, response.sources);
            }

            // Update connection status
            this.updateConnectionStatus(true);

        } catch (error) {
            // Hide typing indicator
            this.messageDisplay.hideTypingIndicator();

            // Add error message
            this.messageDisplay.addErrorMessage(error.message);

            // Update connection status
            this.updateConnectionStatus(false);
        } finally {
            // Re-enable input
            this.setInputState(true);
            this.messageInput.focus();
        }
    }

    /**
     * Handle clear chat
     */
    handleClearChat() {
        if (confirm('Are you sure you want to clear chat history?')) {
            this.messageDisplay.clearMessages();
            
            // Add welcome message
            this.addWelcomeMessage();
            
            // Focus input
            this.messageInput.focus();
            
            // Show success message
            this.showSuccess('Chat history cleared');
        }
    }

    /**
     * Add welcome message
     */
    addWelcomeMessage() {
        const welcomeMessage = {
            id: Formatters.generateId(),
            type: APP_CONFIG.MESSAGE_TYPES.SYSTEM,
            content: 'Hello! I\'m your HDFC Mutual Fund FAQ assistant. I can help you with factual questions about HDFC mutual funds. How can I assist you today?',
            timestamp: new Date()
        };

        this.messageDisplay.addMessage(welcomeMessage);
    }

    /**
     * Setup input validation
     */
    setupInputValidation() {
        // Prevent invalid characters
        this.messageInput.addEventListener('input', (e) => {
            const sanitized = ValidationService.sanitizeInput(e.target.value);
            if (sanitized !== e.target.value) {
                e.target.value = sanitized;
                this.updateCharCount();
            }
        });
    }

    /**
     * Update character count
     */
    updateCharCount() {
        const count = ValidationService.getCharacterCount(this.messageInput.value);
        this.charCountElement.textContent = count;
        
        // Update color based on count
        if (count > APP_CONFIG.MAX_MESSAGE_LENGTH * 0.9) {
            this.charCountElement.className = 'text-red-500';
        } else if (count > APP_CONFIG.MAX_MESSAGE_LENGTH * 0.7) {
            this.charCountElement.className = 'text-yellow-500';
        } else {
            this.charCountElement.className = 'text-gray-500';
        }
    }

    /**
     * Update send button state
     */
    updateSendButton() {
        const message = this.messageInput.value.trim();
        const messageLength = message.length;
        
        console.log('updateSendButton called:', {
            message: `"${message}"`,
            length: messageLength,
            isTyping: this.isTyping,
            maxLength: APP_CONFIG.MAX_MESSAGE_LENGTH
        });
        
        // Simple validation: check if message is not empty and has minimum length
        const isValid = messageLength >= 3 && messageLength <= APP_CONFIG.MAX_MESSAGE_LENGTH;
        
        this.sendButton.disabled = !isValid || this.isTyping;
        
        if (isValid && messageLength > 0) {
            this.sendButton.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            this.sendButton.classList.add('opacity-50', 'cursor-not-allowed');
        }
    }

    /**
     * Auto-resize textarea
     */
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    /**
     * Set input state (enabled/disabled)
     */
    setInputState(enabled) {
        this.isTyping = !enabled;
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled || this.messageInput.value.trim().length < 3;
        
        if (enabled) {
            this.messageInput.classList.remove('bg-gray-100', 'cursor-not-allowed');
            this.messageInput.classList.add('bg-white');
        } else {
            this.messageInput.classList.add('bg-gray-100', 'cursor-not-allowed');
            this.messageInput.classList.remove('bg-white');
        }
    }

    /**
     * Validate input
     */
    validateInput() {
        const message = this.messageInput.value.trim();
        if (!message) {
            return true;
        }

        const validation = ValidationService.validateMessage(message);
        
        if (!validation.isValid) {
            this.showError(validation.errors.join(', '));
            return false;
        }
        
        return true;
    }

    /**
     * Update connection status
     */
    async updateConnectionStatus(isConnected = null) {
        const statusElement = document.getElementById('connectionStatus');
        
        if (isConnected === null) {
            // Check actual connection status
            isConnected = await APIService.testConnection();
        }

        const statusDot = statusElement.querySelector('div:first-child');
        const statusText = statusElement.querySelector('span:last-child');

        if (isConnected) {
            statusDot.className = 'w-2 h-2 bg-green-500 rounded-full mr-2';
            statusText.textContent = 'Connected';
            statusText.className = 'text-sm text-gray-600';
        } else {
            statusDot.className = 'w-2 h-2 bg-red-500 rounded-full mr-2';
            statusText.textContent = 'Disconnected';
            statusText.className = 'text-sm text-red-600';
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        this.messageDisplay.addErrorMessage(message);
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        this.messageDisplay.addSystemMessage(message);
    }
}

// Export component
window.ChatInterface = ChatInterface;
