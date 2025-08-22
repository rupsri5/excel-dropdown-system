// static/js/main.js - Custom JavaScript for Excel Dropdown App

/**
 * Main JavaScript file for Excel Dropdown System
 * Handles UI interactions, animations, and utility functions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('Excel Dropdown System - Initialized');
    
    // Add loading states to buttons
    initializeLoadingStates();
    
    // Add smooth animations
    addSmoothAnimations();
    
    // Initialize tooltips if Bootstrap is available
    initializeTooltips();
}

/**
 * Add loading states to buttons
 */
function initializeLoadingStates() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });
}

/**
 * Add smooth animations to cards and elements
 */
function addSmoothAnimations() {
    // Animate cards on page load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Animate dropdowns
    const dropdowns = document.querySelectorAll('.dropdown-container');
    dropdowns.forEach((dropdown, index) => {
        dropdown.style.opacity = '0';
        dropdown.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            dropdown.style.transition = 'all 0.5s ease';
            dropdown.style.opacity = '1';
            dropdown.style.transform = 'translateX(0)';
        }, 200 + (index * 100));
    });
}

/**
 * Initialize Bootstrap tooltips if available
 */
function initializeTooltips() {
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Show notification message
 * @param {string} message - The message to show
 * @param {string} type - The type of notification (success, warning, danger, info)
 */
function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notification-container') || createNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '400px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    notificationContainer.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

/**
 * Create notification container if it doesn't exist
 */
function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notification-container';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

/**
 * Scroll to element smoothly
 * @param {string} elementId - The ID of the element to scroll to
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

/**
 * Format number with commas
 * @param {number} num - The number to format
 * @returns {string} - Formatted number string
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Debounce function to limit rapid function calls
 * @param {Function} func - The function to debounce
 * @param {number} wait - The wait time in milliseconds
 * @returns {Function} - The debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Copy text to clipboard
 * @param {string} text - The text to copy
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Failed to copy: ', err);
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

/**
 * Fallback copy function for older browsers
 * @param {string} text - The text to copy
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showNotification('Copied to clipboard!', 'success');
        }
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show/hide loading spinner
 * @param {boolean} show - Whether to show or hide the spinner
 */
function toggleLoadingSpinner(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = show ? 'block' : 'none';
    }
}

/**
 * Validate form fields
 * @param {string} formId - The ID of the form to validate
 * @returns {boolean} - Whether the form is valid
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Export functions for global use
window.ExcelDropdownApp = {
    showNotification,
    scrollToElement,
    formatNumber,
    debounce,
    copyToClipboard,
    toggleLoadingSpinner,
    validateForm
};