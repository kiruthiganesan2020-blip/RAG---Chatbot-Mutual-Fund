/**
 * Formatting Utilities
 * Utility functions for text formatting and display
 */

/**
 * Formats timestamp for display
 * @param {string} timestamp - ISO timestamp
 * @returns {string} Formatted timestamp
 */
export function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now - date;
  
  if (diffMs < 60000) { // Less than 1 minute
    return 'Just now';
  } else if (diffMs < 3600000) { // Less than 1 hour
    return `${Math.floor(diffMs / 60000)} minutes ago`;
  } else if (diffMs < 86400000) { // Less than 1 day
    return `${Math.floor(diffMs / 3600000)} hours ago`;
  } else {
    return date.toLocaleDateString();
  }
}

/**
 * Truncates text to specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export function truncateText(text, maxLength = 100) {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength - 3) + '...';
}

/**
 * Formats file size for display
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
export function formatFileSize(bytes) {
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  if (bytes === 0) return '0 Bytes';
  
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  const size = (bytes / Math.pow(1024, i)).toFixed(2);
  
  return `${size} ${sizes[i]}`;
}

/**
 * Escapes HTML for safe display
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
export function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Formats response sources for display
 * @param {Array} sources - Array of source objects
 * @returns {string} Formatted sources
 */
export function formatSources(sources) {
  if (!sources || sources.length === 0) {
    return '';
  }
  
  return sources.map((source, index) => {
    const confidence = source.confidence || 0;
    const confidenceClass = confidence > 0.8 ? 'high' : confidence > 0.6 ? 'medium' : confidence > 0.3 ? 'low' : 'very-low';
    
    return `[${index + 1}] ${source.title || 'Unknown Source'} (${confidenceClass} confidence: ${(confidence * 100).toFixed(1)}%)`;
  }).join('\n');
}

/**
 * Gets theme-aware CSS class
 * @param {string} baseClass - Base CSS class
 * @param {string} theme - Current theme
 * @returns {string} Theme-aware CSS class
 */
export function getThemeClass(baseClass, theme = 'light') {
  return `${baseClass} ${theme === 'dark' ? 'dark-theme' : 'light-theme'}`;
}

/**
 * Debounces function calls
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}
