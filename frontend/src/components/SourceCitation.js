// Source Citation Component

class SourceCitation {
    constructor() {
        this.container = null;
        this.sources = [];
    }

    /**
     * Initialize source citation component
     * @param {HTMLElement} container - Container element
     */
    init(container) {
        this.container = container;
    }

    /**
     * Render source citations
     * @param {Array} sources - Array of source objects
     * @param {Object} metadata - Additional metadata
     * @returns {HTMLElement} Rendered citations
     */
    render(sources, metadata = {}) {
        if (!sources || sources.length === 0) {
            return this.renderEmptyState();
        }

        const citationContainer = document.createElement('div');
        citationContainer.className = 'source-citations mt-3 pt-3 border-t border-gray-50 space-y-2';

        const title = document.createElement('div');
        title.className = 'text-[10px] uppercase tracking-wider font-semibold text-gray-400 mb-1';
        title.textContent = 'Verified Sources';
        citationContainer.appendChild(title);

        const listContainer = document.createElement('div');
        listContainer.className = 'flex flex-wrap gap-2';
        citationContainer.appendChild(listContainer);

        sources.forEach((source, index) => {
            const citation = this.renderSingleCitation(source, index, metadata);
            listContainer.appendChild(citation);
        });

        return citationContainer;
    }

    /**
     * Render single source citation
     * @param {Object} source - Source object
     * @param {number} index - Source index
     * @param {Object} metadata - Additional metadata
     * @returns {HTMLElement} Rendered citation
     */
    renderSingleCitation(source, index, metadata) {
        const citation = document.createElement('div');
        citation.className = 'flex items-center space-x-1.5 px-2 py-1 bg-gray-50 border border-gray-100 rounded-lg hover:bg-gray-100 transition-colors text-[10px]';

        // Source icon
        const icon = this.getSourceIcon(source);
        citation.appendChild(icon);

        // Source name
        const sourceName = document.createElement('span');
        sourceName.className = 'text-gray-700';
        sourceName.textContent = Formatters.formatSource(source);
        citation.appendChild(sourceName);

        // Confidence indicator
        if (source.confidence !== undefined) {
            const confidence = this.renderConfidenceIndicator(source.confidence);
            citation.appendChild(confidence);
        }

        // Source badge
        const badge = this.renderSourceBadge(source);
        citation.appendChild(badge);

        // Click handler for source details
        citation.addEventListener('click', () => {
            this.showSourceDetails(source, metadata);
        });

        citation.style.cursor = 'pointer';
        citation.setAttribute('role', 'button');
        citation.setAttribute('tabindex', '0');
        citation.setAttribute('aria-label', `View details for ${Formatters.formatSource(source)}`);

        return citation;
    }

    /**
     * Render empty state for citations
     * @returns {HTMLElement} Empty state element
     */
    renderEmptyState() {
        const emptyContainer = document.createElement('div');
        emptyContainer.className = 'source-citations mt-2 text-xs text-gray-500 italic';
        emptyContainer.textContent = 'No specific sources cited';
        return emptyContainer;
    }

    /**
     * Get source icon based on source type
     * @param {Object} source - Source object
     * @returns {HTMLElement} Source icon
     */
    getSourceIcon(source) {
        const iconContainer = document.createElement('div');
        iconContainer.className = 'w-4 h-4 flex items-center justify-center';

        const icon = document.createElement('svg');
        icon.className = 'w-3 h-3';
        icon.setAttribute('fill', 'none');
        icon.setAttribute('stroke', 'currentColor');
        icon.setAttribute('viewBox', '0 0 24 24');

        let iconPath;
        let iconColor;

        switch (source) {
            case 'hdfc':
                iconPath = 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5';
                iconColor = 'text-blue-600';
                break;
            case 'amfi':
                iconPath = 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z';
                iconColor = 'text-green-600';
                break;
            case 'sebi':
                iconPath = 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253';
                iconColor = 'text-purple-600';
                break;
            case 'groww':
                iconPath = 'M13 10V3L4 14h7v7l9-11h-7z';
                iconColor = 'text-orange-600';
                break;
            default:
                iconPath = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z';
                iconColor = 'text-gray-600';
        }

        icon.setAttribute('stroke', 'currentColor');
        icon.setAttribute('stroke-width', '2');
        icon.setAttribute('stroke-linecap', 'round');
        icon.setAttribute('stroke-linejoin', 'round');

        const path = document.createElement('path');
        path.setAttribute('d', iconPath);
        icon.appendChild(path);

        iconContainer.appendChild(icon);
        iconContainer.classList.add(iconColor);

        return iconContainer;
    }

    /**
     * Render confidence indicator
     * @param {number} confidence - Confidence score (0-1)
     * @returns {HTMLElement} Confidence indicator
     */
    renderConfidenceIndicator(confidence) {
        const indicator = document.createElement('div');
        indicator.className = 'flex items-center space-x-1';

        const dot = document.createElement('div');
        dot.className = 'w-2 h-2 rounded-full';
        
        if (confidence >= 0.8) {
            dot.classList.add('bg-green-500');
        } else if (confidence >= 0.6) {
            dot.classList.add('bg-yellow-500');
        } else {
            dot.classList.add('bg-red-500');
        }

        indicator.appendChild(dot);

        const text = document.createElement('span');
        text.className = 'text-gray-500';
        text.textContent = Formatters.formatConfidence(confidence);
        indicator.appendChild(text);

        return indicator;
    }

    /**
     * Render source badge
     * @param {Object} source - Source object
     * @returns {HTMLElement} Source badge
     */
    renderSourceBadge(source) {
        const badge = document.createElement('span');
        badge.className = 'px-2 py-0.5 text-xs rounded-full';

        switch (source) {
            case 'hdfc':
                badge.classList.add('bg-blue-100', 'text-blue-800');
                badge.textContent = 'Official';
                break;
            case 'amfi':
                badge.classList.add('bg-green-100', 'text-green-800');
                badge.textContent = 'Regulatory';
                break;
            case 'sebi':
                badge.classList.add('bg-purple-100', 'text-purple-800');
                badge.textContent = 'Regulator';
                break;
            case 'groww':
                badge.classList.add('bg-orange-100', 'text-orange-800');
                badge.textContent = 'Platform';
                break;
            default:
                badge.classList.add('bg-gray-100', 'text-gray-800');
                badge.textContent = 'General';
        }

        return badge;
    }

    /**
     * Show detailed source information
     * @param {Object} source - Source object
     * @param {Object} metadata - Additional metadata
     */
    showSourceDetails(source, metadata) {
        const modal = this.createSourceModal(source, metadata);
        document.body.appendChild(modal);
        
        // Focus management
        const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }

        // Close modal on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeSourceModal(modal);
            }
        });

        // Close modal on Escape key
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                this.closeSourceModal(modal);
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
    }

    /**
     * Create source details modal
     * @param {Object} source - Source object
     * @param {Object} metadata - Additional metadata
     * @returns {HTMLElement} Modal element
     */
    createSourceModal(source, metadata) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-labelledby', 'source-modal-title');

        const modalContent = document.createElement('div');
        modalContent.className = 'bg-white rounded-lg p-6 max-w-md w-full mx-4';

        const title = document.createElement('h3');
        title.id = 'source-modal-title';
        title.className = 'text-lg font-semibold text-gray-900 mb-4';
        title.textContent = 'Source Details';
        modalContent.appendChild(title);

        const sourceInfo = document.createElement('div');
        sourceInfo.className = 'space-y-3';

        // Source name
        const sourceName = document.createElement('div');
        sourceName.innerHTML = `
            <div class="text-sm font-medium text-gray-700">Source</div>
            <div class="text-sm text-gray-900">${Formatters.formatSource(source)}</div>
        `;
        sourceInfo.appendChild(sourceName);

        // Source type
        const sourceType = document.createElement('div');
        sourceType.innerHTML = `
            <div class="text-sm font-medium text-gray-700">Type</div>
            <div class="text-sm text-gray-900">${this.getSourceTypeDescription(source)}</div>
        `;
        sourceInfo.appendChild(sourceType);

        // Last updated
        if (metadata.last_updated) {
            const lastUpdated = document.createElement('div');
            lastUpdated.innerHTML = `
                <div class="text-sm font-medium text-gray-700">Last Updated</div>
                <div class="text-sm text-gray-900">${new Date(metadata.last_updated).toLocaleDateString()}</div>
            `;
            sourceInfo.appendChild(lastUpdated);
        }

        // Trust level
        const trustLevel = document.createElement('div');
        trustLevel.innerHTML = `
            <div class="text-sm font-medium text-gray-700">Trust Level</div>
            <div class="text-sm text-gray-900">${this.getTrustLevel(source)}</div>
        `;
        sourceInfo.appendChild(trustLevel);

        modalContent.appendChild(sourceInfo);

        // Close button
        const closeButton = document.createElement('button');
        closeButton.className = 'mt-6 w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2';
        closeButton.textContent = 'Close';
        closeButton.addEventListener('click', () => {
            this.closeSourceModal(modal);
        });
        modalContent.appendChild(closeButton);

        modal.appendChild(modalContent);
        return modal;
    }

    /**
     * Close source modal
     * @param {HTMLElement} modal - Modal element
     */
    closeSourceModal(modal) {
        if (modal && modal.parentNode) {
            modal.parentNode.removeChild(modal);
        }
    }

    /**
     * Get source type description
     * @param {Object} source - Source object
     * @returns {string} Description
     */
    getSourceTypeDescription(source) {
        const descriptions = {
            'hdfc': 'Official HDFC Mutual Fund documentation',
            'amfi': 'Association of Mutual Funds in India',
            'sebi': 'Securities and Exchange Board of India',
            'groww': 'Investment platform information',
            'unknown': 'General information source'
        };
        return descriptions[source] || descriptions['unknown'];
    }

    /**
     * Get trust level for source
     * @param {Object} source - Source object
     * @returns {string} Trust level
     */
    getTrustLevel(source) {
        const trustLevels = {
            'hdfc': 'High - Official Source',
            'amfi': 'High - Regulatory Body',
            'sebi': 'High - Regulatory Authority',
            'groww': 'Medium - Platform Data',
            'unknown': 'Low - Unverified Source'
        };
        return trustLevels[source] || trustLevels['unknown'];
    }

    /**
     * Update citations with new data
     * @param {Array} sources - New sources array
     * @param {Object} metadata - Additional metadata
     */
    update(sources, metadata) {
        if (!this.container) return;

        this.container.innerHTML = '';
        const citations = this.render(sources, metadata);
        this.container.appendChild(citations);
    }
}

// Export component
window.SourceCitation = SourceCitation;
