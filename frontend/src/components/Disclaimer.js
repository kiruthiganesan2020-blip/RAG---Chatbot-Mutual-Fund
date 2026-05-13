// Disclaimer Component

class Disclaimer {
    constructor() {
        this.container = null;
        this.isVisible = true;
    }

    /**
     * Initialize disclaimer component
     * @param {HTMLElement} container - Container element
     */
    init(container) {
        this.container = container;
        this.setupEventListeners();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Add close button if not present
        if (!this.container.querySelector('.disclaimer-close')) {
            this.addCloseButton();
        }
    }

    /**
     * Add close button to disclaimer
     */
    addCloseButton() {
        const closeButton = document.createElement('button');
        closeButton.className = 'disclaimer-close ml-4 text-yellow-600 hover:text-yellow-800 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 rounded';
        closeButton.setAttribute('aria-label', 'Close disclaimer');
        closeButton.innerHTML = `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        `;

        closeButton.addEventListener('click', () => {
            this.hide();
        });

        // Add to disclaimer content
        const content = this.container.querySelector('.flex-1');
        if (content) {
            content.appendChild(closeButton);
        }
    }

    /**
     * Show disclaimer
     */
    show() {
        if (this.container) {
            this.container.style.display = 'block';
            this.container.classList.add('fade-in');
            this.isVisible = true;
        }
    }

    /**
     * Hide disclaimer
     */
    hide() {
        if (this.container) {
            this.container.style.display = 'none';
            this.isVisible = false;
            
            // Save preference to localStorage
            localStorage.setItem('disclaimer-hidden', 'true');
        }
    }

    /**
     * Check if disclaimer should be shown
     * @returns {boolean} Whether disclaimer should be shown
     */
    shouldShow() {
        // Check if user has previously hidden the disclaimer
        const isHidden = localStorage.getItem('disclaimer-hidden') === 'true';
        
        // Show if not hidden or if it's been more than 24 hours
        if (!isHidden) {
            return true;
        }

        const hiddenTime = localStorage.getItem('disclaimer-hidden-time');
        if (hiddenTime) {
            const hiddenDate = new Date(hiddenTime);
            const now = new Date();
            const hoursSinceHidden = (now - hiddenDate) / (1000 * 60 * 60);
            
            // Show again after 24 hours
            return hoursSinceHidden > 24;
        }

        return false;
    }

    /**
     * Update disclaimer content
     * @param {string} title - Disclaimer title
     * @param {string} message - Disclaimer message
     * @param {string} type - Disclaimer type (warning, info, error)
     */
    updateContent(title, message, type = 'warning') {
        if (!this.container) return;

        const titleElement = this.container.querySelector('h3');
        const messageElement = this.container.querySelector('p');
        const iconContainer = this.container.querySelector('.flex-shrink-0');

        // Update title
        if (titleElement) {
            titleElement.textContent = title;
        }

        // Update message
        if (messageElement) {
            messageElement.textContent = message;
        }

        // Update icon and colors based on type
        this.updateStyling(type, iconContainer);
    }

    /**
     * Update disclaimer styling based on type
     * @param {string} type - Disclaimer type
     * @param {HTMLElement} iconContainer - Icon container
     */
    updateStyling(type, iconContainer) {
        if (!this.container || !iconContainer) return;

        // Remove existing classes
        this.container.className = this.container.className.replace(/bg-\w+-50|border-\w+-200|text-\w+-800|text-\w+-600/g, '');

        // Add new classes based on type
        switch (type) {
            case 'warning':
                this.container.classList.add('bg-yellow-50', 'border-yellow-200');
                this.updateIcon(iconContainer, 'warning', 'text-yellow-600', 'text-yellow-800');
                break;
            case 'info':
                this.container.classList.add('bg-blue-50', 'border-blue-200');
                this.updateIcon(iconContainer, 'info', 'text-blue-600', 'text-blue-800');
                break;
            case 'error':
                this.container.classList.add('bg-red-50', 'border-red-200');
                this.updateIcon(iconContainer, 'error', 'text-red-600', 'text-red-800');
                break;
            case 'success':
                this.container.classList.add('bg-green-50', 'border-green-200');
                this.updateIcon(iconContainer, 'success', 'text-green-600', 'text-green-800');
                break;
            default:
                this.container.classList.add('bg-gray-50', 'border-gray-200');
                this.updateIcon(iconContainer, 'info', 'text-gray-600', 'text-gray-800');
        }
    }

    /**
     * Update icon based on type
     * @param {HTMLElement} iconContainer - Icon container
     * @param {string} type - Icon type
     * @param {string} iconColor - Icon color class
     * @param {string} textColor - Text color class
     */
    updateIcon(iconContainer, type, iconColor, textColor) {
        if (!iconContainer) return;

        // Update icon color
        const icon = iconContainer.querySelector('svg');
        if (icon) {
            icon.className = icon.className.replace(/text-\w+-600/g, iconColor);
        }

        // Update text colors
        const title = this.container.querySelector('h3');
        const message = this.container.querySelector('p');
        
        if (title) {
            title.className = title.className.replace(/text-\w+-800/g, textColor);
        }
        
        if (message) {
            message.className = message.className.replace(/text-\w+-700/g, textColor);
        }

        // Update icon path based on type
        const path = icon.querySelector('path');
        if (path) {
            const iconPaths = {
                'warning': 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
                'info': 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
                'error': 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
                'success': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
            };

            path.setAttribute('d', iconPaths[type] || iconPaths['info']);
        }
    }

    /**
     * Show temporary disclaimer
     * @param {string} title - Disclaimer title
     * @param {string} message - Disclaimer message
     * @param {string} type - Disclaimer type
     * @param {number} duration - Duration in milliseconds
     */
    showTemporary(title, message, type = 'info', duration = 5000) {
        this.updateContent(title, message, type);
        this.show();

        setTimeout(() => {
            this.hide();
        }, duration);
    }

    /**
     * Show investment advice disclaimer
     */
    showInvestmentAdviceDisclaimer() {
        const title = 'Investment Advice Disclaimer';
        const message = 'I cannot provide investment advice or recommendations. For personalized investment guidance, please consult with a qualified financial advisor who can assess your specific financial situation and goals.';
        
        this.updateContent(title, message, 'warning');
        this.show();
    }

    /**
     * Show risk disclaimer
     */
    showRiskDisclaimer() {
        const title = 'Investment Risk Disclaimer';
        const message = 'Mutual fund investments are subject to market risks. Please read all scheme-related documents carefully before investing. Past performance does not guarantee future results.';
        
        this.updateContent(title, message, 'warning');
        this.show();
    }

    /**
     * Show data accuracy disclaimer
     */
    showDataAccuracyDisclaimer() {
        const title = 'Data Accuracy Disclaimer';
        const message = 'The information provided is based on publicly available sources and may not reflect the most current data. Please verify important information with official sources before making investment decisions.';
        
        this.updateContent(title, message, 'info');
        this.show();
    }

    /**
     * Toggle disclaimer visibility
     */
    toggle() {
        if (this.isVisible) {
            this.hide();
        } else {
            this.show();
        }
    }

    /**
     * Get disclaimer visibility status
     * @returns {boolean} Whether disclaimer is visible
     */
    isDisclaimerVisible() {
        return this.isVisible;
    }

    /**
     * Reset disclaimer to default state
     */
    reset() {
        const defaultTitle = 'Important Disclaimer';
        const defaultMessage = 'This assistant provides factual information about HDFC mutual funds and does not offer investment advice. Please consult with a qualified financial advisor before making any investment decisions. All information is based on publicly available sources and may not be current.';
        
        this.updateContent(defaultTitle, defaultMessage, 'warning');
        
        // Clear localStorage
        localStorage.removeItem('disclaimer-hidden');
        localStorage.removeItem('disclaimer-hidden-time');
        
        this.show();
    }

    /**
     * Add custom action button
     * @param {string} text - Button text
     * @param {Function} callback - Button callback
     * @param {string} className - Additional CSS classes
     */
    addActionButton(text, callback, className = '') {
        if (!this.container) return;

        const content = this.container.querySelector('.flex-1');
        if (!content) return;

        const button = document.createElement('button');
        button.className = `mt-2 px-3 py-1 text-sm rounded ${className}`;
        if (!className) {
            button.className += ' bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2';
        }
        
        button.textContent = text;
        button.addEventListener('click', callback);

        content.appendChild(button);
    }

    /**
     * Add link to disclaimer
     * @param {string} text - Link text
     * @param {string} url - Link URL
     */
    addLink(text, url) {
        if (!this.container) return;

        const content = this.container.querySelector('.flex-1');
        if (!content) return;

        const link = document.createElement('a');
        link.href = url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.className = 'text-yellow-600 hover:text-yellow-800 underline text-sm';
        link.textContent = text;

        content.appendChild(link);
    }

    /**
     * Initialize disclaimer with user preferences
     */
    initialize() {
        if (this.shouldShow()) {
            this.show();
        } else {
            this.hide();
        }

        // Save current time when hiding
        const originalHide = this.hide.bind(this);
        this.hide = () => {
            originalHide();
            localStorage.setItem('disclaimer-hidden-time', new Date().toISOString());
        };
    }
}

// Export component
window.Disclaimer = Disclaimer;
