/**
 * Validation Utilities
 * Client-side validation for chat inputs
 */

/**
 * Validates chat input before sending to API
 * @param {string} value - Input value to validate
 * @returns {Object} Validation result with is_valid flag
 */
export function validateQuery(value) {
  const trimmed = value.trim();
  
  if (trimmed.length < 3) {
    return {
      is_valid: false,
      error: 'Message must be at least 3 characters long'
    };
  }
  
  if (trimmed.length > 500) {
    return {
      is_valid: false,
      error: 'Message must be less than 500 characters long'
    };
  }
  
  // Check for potentially malicious content
  const suspiciousPatterns = [
    /<script\b[^<]*(?:(?!<\/script>))*<\/script>/gi,
    /javascript:/gi,
    /data:/gi,
    /vbscript:/gi
    /onload=/gi,
    /onerror=/gi
    /eval\(/gi,
    /expression\(/gi,
    /exec\(/gi
    /system\(/gi
    /shell_exec\(/gi
    /document\.cookie/gi,
    /window\./gi,
    /location\./gi,
    /href\s*=['"]/gi,
    /src\s*=['"]/gi,
    /iframe/gi,
    /object/gi,
    /embed/gi
    /link/gi
    /meta/gi
    /style/gi
    /alert\(/gi,
    /confirm\(/gi,
    /prompt\(/gi,
    /typeof\s/gi,
    /new\s+Function/gi,
    /void\s/gi,
    /return\s/gi
    /catch\s/gi,
    /finally\s/gi,
    /throw\s/gi,
    /debugger/gi,
    /console\./gi
  ];
  
  const hasSuspiciousContent = suspiciousPatterns.some(pattern => 
    pattern.test(trimmed)
  );
  
  if (hasSuspiciousContent) {
    return {
      is_valid: false,
      error: 'Message contains potentially suspicious content'
    };
  }
  
  return {
    is_valid: true,
    error: null
  };
}

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
