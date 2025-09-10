/**
 * UI Manager for English Text Analyzer
 * Handles user interface interactions and visual feedback
 */

class UIManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupUIEnhancements();
        this.setupAccessibility();
        this.setupResponsiveFeatures();
    }
    
    /**
     * Set up UI enhancements
     */
    setupUIEnhancements() {
        // Add smooth scrolling to results
        this.setupSmoothScrolling();
        
        // Add input validation feedback
        this.setupInputValidation();
        
        // Add keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        // Add tooltips for better UX
        this.setupTooltips();
    }
    
    /**
     * Set up smooth scrolling behavior
     */
    setupSmoothScrolling() {
        // Smooth scroll to results when analysis completes
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && 
                    mutation.attributeName === 'style' &&
                    mutation.target.id === 'results-section') {
                    
                    const resultsSection = mutation.target;
                    if (resultsSection.style.display === 'block') {
                        setTimeout(() => {
                            resultsSection.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }, 100);
                    }
                }
            });
        });
        
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            observer.observe(resultsSection, {
                attributes: true,
                attributeFilter: ['style']
            });
        }
    }
    
    /**
     * Set up input validation with visual feedback
     */
    setupInputValidation() {
        const textInput = document.getElementById('text-input');
        const apiKeyInput = document.getElementById('api-key');
        
        if (textInput) {
            textInput.addEventListener('input', (e) => {
                this.validateTextInput(e.target);
            });
            
            textInput.addEventListener('blur', (e) => {
                this.validateTextInput(e.target);
            });
        }
        
        if (apiKeyInput) {
            apiKeyInput.addEventListener('input', (e) => {
                this.validateAPIKeyInput(e.target);
            });
            
            apiKeyInput.addEventListener('blur', (e) => {
                this.validateAPIKeyInput(e.target);
            });
        }
    }
    
    /**
     * Validate text input
     */
    validateTextInput(input) {
        const text = input.value.trim();
        const wordCount = text ? text.split(/\s+/).length : 0;
        
        // Remove previous validation classes
        input.classList.remove('valid', 'warning', 'error');
        
        if (wordCount === 0) {
            // Empty input - neutral state
            return;
        } else if (wordCount < 10) {
            // Too short for meaningful analysis
            input.classList.add('warning');
            this.showInputFeedback(input, 'At least 10 words recommended for analysis', 'warning');
        } else if (wordCount > 5000) {
            // Very long text - might be slow
            input.classList.add('warning');
            this.showInputFeedback(input, 'Large text may take longer to analyze', 'warning');
        } else {
            // Good length
            input.classList.add('valid');
            this.hideInputFeedback(input);
        }
    }
    
    /**
     * Validate API key input
     */
    validateAPIKeyInput(input) {
        const key = input.value.trim();
        
        // Remove previous validation classes
        input.classList.remove('valid', 'error');
        
        if (key === '') {
            // Empty input - neutral state
            this.hideInputFeedback(input);
            return;
        }
        
        if (this.validateAPIKeyFormat(key)) {
            input.classList.add('valid');
            this.hideInputFeedback(input);
        } else {
            input.classList.add('error');
            this.showInputFeedback(input, 'Invalid API key format', 'error');
        }
    }
    
    /**
     * Validate API key format
     */
    validateAPIKeyFormat(key) {
        return key && key.startsWith('AIza') && key.length > 30;
    }
    
    /**
     * Show input feedback message
     */
    showInputFeedback(input, message, type) {
        let feedbackEl = input.parentNode.querySelector('.input-feedback');
        
        if (!feedbackEl) {
            feedbackEl = document.createElement('div');
            feedbackEl.className = 'input-feedback';
            input.parentNode.appendChild(feedbackEl);
        }
        
        feedbackEl.textContent = message;
        feedbackEl.className = `input-feedback ${type}`;
    }
    
    /**
     * Hide input feedback message
     */
    hideInputFeedback(input) {
        const feedbackEl = input.parentNode.querySelector('.input-feedback');
        if (feedbackEl) {
            feedbackEl.remove();
        }
    }
    
    /**
     * Set up keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to analyze
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                const analyzeBtn = document.getElementById('analyze-btn');
                if (analyzeBtn && !analyzeBtn.disabled) {
                    analyzeBtn.click();
                }
            }
            
            // Ctrl/Cmd + K to focus on API key input
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const apiKeyInput = document.getElementById('api-key');
                if (apiKeyInput) {
                    apiKeyInput.focus();
                    apiKeyInput.select();
                }
            }
            
            // Escape to clear text
            if (e.key === 'Escape') {
                const textInput = document.getElementById('text-input');
                if (textInput && document.activeElement === textInput) {
                    const clearBtn = document.getElementById('clear-btn');
                    if (clearBtn) {
                        clearBtn.click();
                    }
                }
            }
        });
    }
    
    /**
     * Set up tooltips for better UX
     */
    setupTooltips() {
        const tooltipElements = [
            {
                selector: '#analyze-btn',
                text: 'Analyze the text (Ctrl+Enter)'
            },
            {
                selector: '#api-key',
                text: 'Enter your Gemini API key (Ctrl+K to focus)'
            },
            {
                selector: '#clear-btn',
                text: 'Clear the text input (Escape when focused)'
            },
            {
                selector: '#export-html-btn',
                text: 'Export results as HTML file'
            },
            {
                selector: '#export-pdf-btn',
                text: 'Export results as PDF file'
            },
            {
                selector: '#print-btn',
                text: 'Print the analysis results'
            }
        ];
        
        tooltipElements.forEach(({ selector, text }) => {
            const element = document.querySelector(selector);
            if (element) {
                element.title = text;
                element.setAttribute('aria-label', text);
            }
        });
    }
    
    /**
     * Set up accessibility features
     */
    setupAccessibility() {
        // Add ARIA labels and descriptions
        this.setupARIALabels();
        
        // Set up focus management
        this.setupFocusManagement();
        
        // Add screen reader announcements
        this.setupScreenReaderAnnouncements();
    }
    
    /**
     * Set up ARIA labels for better accessibility
     */
    setupARIALabels() {
        const ariaLabels = [
            {
                selector: '#text-input',
                label: 'Text to analyze',
                description: 'Enter the English text you want to analyze'
            },
            {
                selector: '#api-key',
                label: 'Gemini API Key',
                description: 'Your Google Gemini API key for text analysis'
            },
            {
                selector: '.analysis-modules',
                label: 'Analysis modules',
                description: 'Select which types of analysis to perform'
            },
            {
                selector: '#results-section',
                label: 'Analysis results',
                description: 'Results of the text analysis'
            }
        ];
        
        ariaLabels.forEach(({ selector, label, description }) => {
            const element = document.querySelector(selector);
            if (element) {
                element.setAttribute('aria-label', label);
                if (description) {
                    element.setAttribute('aria-description', description);
                }
            }
        });
    }
    
    /**
     * Set up focus management
     */
    setupFocusManagement() {
        // Focus on first input when page loads
        window.addEventListener('load', () => {
            const apiKeyInput = document.getElementById('api-key');
            if (apiKeyInput && !apiKeyInput.value) {
                setTimeout(() => apiKeyInput.focus(), 100);
            }
        });
        
        // Manage focus during analysis
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => {
                // Focus will be managed by the loading state
                setTimeout(() => {
                    const loadingSection = document.getElementById('loading-section');
                    if (loadingSection && loadingSection.style.display !== 'none') {
                        loadingSection.focus();
                    }
                }, 100);
            });
        }
    }
    
    /**
     * Set up screen reader announcements
     */
    setupScreenReaderAnnouncements() {
        // Create announcement region
        const announcementRegion = document.createElement('div');
        announcementRegion.id = 'announcement-region';
        announcementRegion.setAttribute('aria-live', 'polite');
        announcementRegion.setAttribute('aria-atomic', 'true');
        announcementRegion.style.position = 'absolute';
        announcementRegion.style.left = '-10000px';
        announcementRegion.style.width = '1px';
        announcementRegion.style.height = '1px';
        announcementRegion.style.overflow = 'hidden';
        document.body.appendChild(announcementRegion);
        
        this.announcementRegion = announcementRegion;
    }
    
    /**
     * Announce message to screen readers
     */
    announce(message) {
        if (this.announcementRegion) {
            this.announcementRegion.textContent = message;
            
            // Clear after announcement
            setTimeout(() => {
                this.announcementRegion.textContent = '';
            }, 1000);
        }
    }
    
    /**
     * Set up responsive features
     */
    setupResponsiveFeatures() {
        // Handle mobile-specific interactions
        this.setupMobileFeatures();
        
        // Handle window resize
        this.setupResizeHandler();
    }
    
    /**
     * Set up mobile-specific features
     */
    setupMobileFeatures() {
        // Detect mobile device
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (isMobile) {
            document.body.classList.add('mobile-device');
            
            // Adjust textarea behavior on mobile
            const textInput = document.getElementById('text-input');
            if (textInput) {
                textInput.addEventListener('focus', () => {
                    // Prevent zoom on iOS
                    textInput.style.fontSize = '16px';
                });
            }
        }
    }
    
    /**
     * Set up window resize handler
     */
    setupResizeHandler() {
        let resizeTimeout;
        
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        });
    }
    
    /**
     * Handle window resize
     */
    handleResize() {
        // Adjust layout for different screen sizes
        const container = document.querySelector('.container');
        if (container) {
            const width = window.innerWidth;
            
            if (width < 768) {
                container.classList.add('mobile-layout');
            } else {
                container.classList.remove('mobile-layout');
            }
        }
    }
    
    /**
     * Show loading state with progress indication
     */
    showLoadingWithProgress(message = 'Analyzing text...') {
        const loadingSection = document.getElementById('loading-section');
        if (loadingSection) {
            loadingSection.style.display = 'block';
            
            const loadingText = loadingSection.querySelector('p');
            if (loadingText) {
                loadingText.textContent = message;
            }
            
            // Announce to screen readers
            this.announce(message);
        }
    }
    
    /**
     * Update loading progress
     */
    updateLoadingProgress(message) {
        const loadingSection = document.getElementById('loading-section');
        if (loadingSection) {
            const loadingText = loadingSection.querySelector('p');
            if (loadingText) {
                loadingText.textContent = message;
            }
        }
    }
    
    /**
     * Hide loading state
     */
    hideLoading() {
        const loadingSection = document.getElementById('loading-section');
        if (loadingSection) {
            loadingSection.style.display = 'none';
        }
    }
    
    /**
     * Show success message
     */
    showSuccess(message) {
        this.showNotification(message, 'success');
        this.announce(`Success: ${message}`);
    }
    
    /**
     * Show error message
     */
    showError(message) {
        this.showNotification(message, 'error');
        this.announce(`Error: ${message}`);
    }
    
    /**
     * Show warning message
     */
    showWarning(message) {
        this.showNotification(message, 'warning');
        this.announce(`Warning: ${message}`);
    }
    
    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        // Create notification element if it doesn't exist
        let notification = document.getElementById('notification');
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'notification';
            notification.className = 'notification';
            document.body.appendChild(notification);
        }
        
        notification.textContent = message;
        notification.className = `notification ${type} show`;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }
}