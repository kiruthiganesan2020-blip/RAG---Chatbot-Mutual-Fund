// Message Display Component

class MessageDisplay {
    constructor() {
        this.container = null;
        this.messages = [];
        this.typingIndicator = null;
    }

    /**
     * Initialize message display component
     * @param {HTMLElement} container - Container element
     */
    init(container) {
        this.container = container;
    }

    /**
     * Add message to display
     * @param {Object} message - Message object
     * @returns {HTMLElement} Message element
     */
    addMessage(message) {
        const messageElement = this.renderMessage(message);
        this.container.appendChild(messageElement);
        this.messages.push(message);
        
        // Scroll to bottom
        this.scrollToBottom();
        
        return messageElement;
    }

    /**
     * Render individual message
     * @param {Object} message - Message object
     * @returns {HTMLElement} Rendered message
     */
    renderMessage(message) {
        const messageWrapper = document.createElement('div');
        const isUser = message.type === APP_CONFIG.MESSAGE_TYPES.USER;
        
        messageWrapper.className = `message-wrapper fade-in ${isUser ? 'user-message-container' : 'assistant-message-container'}`;
        messageWrapper.setAttribute('data-message-id', message.id);

        const flexContainer = document.createElement('div');
        flexContainer.className = `flex max-w-full ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start`;

        // Avatar (optional for user if we want more ChatGPT style, but keeping it for now)
        const avatar = this.renderAvatar(message.type);
        flexContainer.appendChild(avatar);

        // Message content container
        const contentContainer = document.createElement('div');
        contentContainer.className = `flex flex-col ${isUser ? 'mr-3 items-end' : 'ml-3 items-start'} max-w-[85%]`;

        // Message bubble
        const messageBubble = this.renderMessageBubble(message);
        contentContainer.appendChild(messageBubble);

        // Message metadata
        const metadata = this.renderMessageMetadata(message);
        contentContainer.appendChild(metadata);

        flexContainer.appendChild(contentContainer);
        messageWrapper.appendChild(flexContainer);

        return messageWrapper;
    }

    /**
     * Render message avatar
     * @param {string} messageType - Message type
     * @returns {HTMLElement} Avatar element
     */
    renderAvatar(messageType) {
        const avatarContainer = document.createElement('div');
        avatarContainer.className = 'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center';

        if (messageType === APP_CONFIG.MESSAGE_TYPES.USER) {
            avatarContainer.className += ' bg-gray-600';
            avatarContainer.innerHTML = `
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
            `;
        } else if (messageType === APP_CONFIG.MESSAGE_TYPES.ASSISTANT) {
            avatarContainer.className += ' bg-blue-600';
            avatarContainer.innerHTML = `
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                </svg>
            `;
        } else if (messageType === APP_CONFIG.MESSAGE_TYPES.SYSTEM) {
            avatarContainer.className += ' bg-green-600';
            avatarContainer.innerHTML = `
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            `;
        } else if (messageType === APP_CONFIG.MESSAGE_TYPES.ERROR) {
            avatarContainer.className += ' bg-red-600';
            avatarContainer.innerHTML = `
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            `;
        }

        return avatarContainer;
    }

    /**
     * Render message bubble
     * @param {Object} message - Message object
     * @returns {HTMLElement} Message bubble
     */
    renderMessageBubble(message) {
        const bubble = document.createElement('div');
        const isUser = message.type === APP_CONFIG.MESSAGE_TYPES.USER;
        
        if (isUser) {
            bubble.className = 'message-bubble bg-blue-600 text-white rounded-2xl rounded-tr-none px-4 py-3 shadow-md';
        } else if (message.type === APP_CONFIG.MESSAGE_TYPES.ERROR) {
            bubble.className = 'message-bubble bg-red-50 text-red-800 border border-red-100 rounded-2xl px-4 py-3';
        } else {
            bubble.className = 'message-bubble bg-white text-gray-800 border border-gray-100 rounded-2xl rounded-tl-none px-4 py-3 shadow-sm';
        }

        // Message content
        const content = document.createElement('div');
        content.className = 'text-sm leading-relaxed';
        content.innerHTML = Formatters.formatMessageContent(message.content);
        bubble.appendChild(content);

        // Add typing indicator if message is being generated
        if (message.isTyping) {
            const typingIndicator = this.renderTypingIndicator();
            bubble.appendChild(typingIndicator);
        }

        return bubble;
    }

    /**
     * Render message metadata
     * @param {Object} message - Message object
     * @returns {HTMLElement} Metadata element
     */
    renderMessageMetadata(message) {
        const metadata = document.createElement('div');
        metadata.className = 'mt-1 text-[10px] text-gray-400 font-medium flex flex-wrap items-center gap-x-2 gap-y-1';

        // Sender name
        const sender = document.createElement('span');
        sender.className = 'text-gray-500 font-bold uppercase tracking-tight';
        sender.textContent = this.getSenderName(message.type);
        metadata.appendChild(sender);

        // Timestamp
        const timestamp = document.createElement('span');
        timestamp.textContent = `• ${Formatters.formatTime(message.timestamp)}`;
        metadata.appendChild(timestamp);

        // Response time for assistant messages
        if (message.type === APP_CONFIG.MESSAGE_TYPES.ASSISTANT && message.responseTime) {
            const responseTime = document.createElement('span');
            responseTime.textContent = `• ${Formatters.formatResponseTime(message.responseTime)}`;
            metadata.appendChild(responseTime);
        }

        // Confidence for assistant messages
        if (message.type === APP_CONFIG.MESSAGE_TYPES.ASSISTANT && message.confidence !== undefined) {
            const confidence = document.createElement('span');
            confidence.className = message.confidence > 0.8 ? 'text-green-600' : 'text-yellow-600';
            confidence.textContent = `• ${Formatters.formatConfidence(message.confidence)} confidence`;
            metadata.appendChild(confidence);
        }

        // Model used for assistant messages
        if (message.type === APP_CONFIG.MESSAGE_TYPES.ASSISTANT && message.modelUsed) {
            const model = document.createElement('span');
            model.className = 'bg-gray-100 px-1.5 py-0.5 rounded text-[9px]';
            model.textContent = Formatters.formatModel(message.modelUsed);
            metadata.appendChild(model);
        }

        return metadata;
    }

    /**
     * Render typing indicator
     * @returns {HTMLElement} Typing indicator
     */
    renderTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'flex items-center space-x-1 mt-2';

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'typing-indicator';
            indicator.appendChild(dot);
        }

        return indicator;
    }

    /**
     * Show typing indicator
     * @returns {HTMLElement} Typing indicator element
     */
    showTypingIndicator() {
        const typingMessage = {
            id: Formatters.generateId(),
            type: APP_CONFIG.MESSAGE_TYPES.ASSISTANT,
            content: '',
            timestamp: new Date(),
            isTyping: true
        };

        this.typingIndicator = this.addMessage(typingMessage);
        return this.typingIndicator;
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.remove();
            this.typingIndicator = null;
        }
    }

    /**
     * Update message content
     * @param {string} messageId - Message ID
     * @param {string} content - New content
     */
    updateMessage(messageId, content) {
        const messageElement = this.container.querySelector(`[data-message-id="${messageId}"]`);
        if (messageElement) {
            const contentElement = messageElement.querySelector('p');
            if (contentElement) {
                contentElement.innerHTML = Formatters.formatMessageContent(content);
            }
        }
    }

    /**
     * Add source citations to message
     * @param {string} messageId - Message ID
     * @param {Array} sources - Sources array
     */
    addSources(messageId, sources) {
        const messageElement = this.container.querySelector(`[data-message-id="${messageId}"]`);
        if (messageElement && sources && sources.length > 0) {
            const contentContainer = messageElement.querySelector('.flex-1');
            if (contentContainer) {
                const sourceCitation = new SourceCitation();
                const citations = sourceCitation.render(sources);
                citations.className += ' mt-2';
                contentContainer.appendChild(citations);
            }
        }
    }

    /**
     * Clear all messages
     */
    clearMessages() {
        this.container.innerHTML = '';
        this.messages = [];
        this.typingIndicator = null;
    }

    /**
     * Get sender name based on message type
     * @param {string} messageType - Message type
     * @returns {string} Sender name
     */
    getSenderName(messageType) {
        const senderNames = {
            [APP_CONFIG.MESSAGE_TYPES.USER]: 'You',
            [APP_CONFIG.MESSAGE_TYPES.ASSISTANT]: 'Assistant',
            [APP_CONFIG.MESSAGE_TYPES.SYSTEM]: 'System',
            [APP_CONFIG.MESSAGE_TYPES.ERROR]: 'Error'
        };
        return senderNames[messageType] || 'Unknown';
    }

    /**
     * Scroll to bottom of container
     */
    scrollToBottom() {
        if (this.container) {
            this.container.scrollTop = this.container.scrollHeight;
        }
    }

    /**
     * Get message count
     * @returns {number} Number of messages
     */
    getMessageCount() {
        return this.messages.length;
    }

    /**
     * Get last message
     * @returns {Object|null} Last message
     */
    getLastMessage() {
        return this.messages.length > 0 ? this.messages[this.messages.length - 1] : null;
    }

    /**
     * Get messages by type
     * @param {string} messageType - Message type
     * @returns {Array} Messages of specified type
     */
    getMessagesByType(messageType) {
        return this.messages.filter(message => message.type === messageType);
    }

    /**
     * Animate message appearance
     * @param {HTMLElement} element - Element to animate
     */
    animateMessage(element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 10);
    }

    /**
     * Add error message
     * @param {string} error - Error message
     * @returns {HTMLElement} Error message element
     */
    addErrorMessage(error) {
        const errorMessage = {
            id: Formatters.generateId(),
            type: APP_CONFIG.MESSAGE_TYPES.ERROR,
            content: error,
            timestamp: new Date()
        };

        return this.addMessage(errorMessage);
    }

    /**
     * Add system message
     * @param {string} message - System message
     * @returns {HTMLElement} System message element
     */
    addSystemMessage(message) {
        const systemMessage = {
            id: Formatters.generateId(),
            type: APP_CONFIG.MESSAGE_TYPES.SYSTEM,
            content: message,
            timestamp: new Date()
        };

        return this.addMessage(systemMessage);
    }

    /**
     * Update message with streaming content
     * @param {string} messageId - Message ID
     * @param {string} content - Streaming content
     */
    updateStreamingMessage(messageId, content) {
        const messageElement = this.container.querySelector(`[data-message-id="${messageId}"]`);
        if (messageElement) {
            const contentElement = messageElement.querySelector('p');
            if (contentElement) {
                contentElement.innerHTML = Formatters.formatMessageContent(content);
                this.scrollToBottom();
            }
        }
    }
}

// Export component
window.MessageDisplay = MessageDisplay;
