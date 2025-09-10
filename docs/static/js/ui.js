/**
 * English Text Analyzer - UI Manager
 * Handles user interface interactions and dynamic content updates
 */

class UIManager {
    constructor() {
        this.initialized = false;
    }
    
    init() {
        if (this.initialized) return;
        
        console.log('Initializing UI Manager...');
        
        // Set up dynamic UI behaviors
        this.setupTextInputBehaviors();
        this.setupModuleSelectionBehaviors();
        this.setupResponsiveBehaviors();
        this.setupAccessibilityFeatures();
        
        this.initialized = true;
        console.log('UI Manager initialized');
    }
    
    setupTextInputBehaviors() {
        const textInput = document.getElementById('text-input');
        
        // Auto-resize textarea
        textInput.addEventListener('input', (e) => {
            this.autoResizeTextarea(e.target);
        });
        
        // Drag and drop support for text files
        textInput.addEventListener('dragover', (e) => {
            e.preventDefault();
            textInput.classList.add('drag-over');
        });
        
        textInput.addEventListener('dragleave', (e) => {
            e.preventDefault();
            textInput.classList.remove('drag-over');
        });
        
        textInput.addEventListener('drop', (e) => {
            e.preventDefault();
            textInput.classList.remove('drag-over');
            this.handleFileDrop(e);
        });
        
        // Keyboard shortcuts
        textInput.addEventListener('keydown', (e) => {
            this.handleTextInputKeyboard(e);
        });
    }
    
    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.max(200, textarea.scrollHeight) + 'px';
    }
    
    async handleFileDrop(event) {
        const files = Array.from(event.dataTransfer.files);
        const textFiles = files.filter(file => file.type.startsWith('text/') || file.name.endsWith('.txt'));
        
        if (textFiles.length === 0) {
            this.showNotification('Please drop a text file (.txt)', 'warning');
            return;
        }
        
        try {
            const file = textFiles[0];
            const text = await this.readFileAsText(file);
            document.getElementById('text-input').value = text;
            
            // Trigger input event to update stats
            const inputEvent = new Event('input', { bubbles: true });
            document.getElementById('text-input').dispatchEvent(inputEvent);
            
            this.showNotification(`Loaded: ${file.name}`, 'success');
        } catch (error) {
            console.error('Error reading file:', error);
            this.showNotification('Error reading file', 'error');
        }
    }
    
    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }
    
    handleTextInputKeyboard(event) {
        // Ctrl+Enter to analyze
        if (event.ctrlKey && event.key === 'Enter') {
            event.preventDefault();
            document.getElementById('analyze-btn').click();
        }
        
        // Ctrl+A to select all
        if (event.ctrlKey && event.key === 'a') {
            event.target.select();
        }
    }
    
    setupModuleSelectionBehaviors() {
        // Select/deselect all functionality
        this.addSelectAllButton();
        
        // Module dependency handling
        this.setupModuleDependencies();
        
        // Module descriptions toggle
        this.setupModuleDescriptions();
    }
    
    addSelectAllButton() {
        const analysisModules = document.querySelector('.analysis-modules');
        const selectAllContainer = document.createElement('div');
        selectAllContainer.className = 'select-all-container';
        selectAllContainer.innerHTML = `
            <button type="button" id="select-all-modules" class="btn-secondary">Select All</button>
            <button type="button" id="deselect-all-modules" class="btn-secondary">Deselect All</button>
        `;
        
        analysisModules.parentNode.insertBefore(selectAllContainer, analysisModules);
        
        // Event listeners
        document.getElementById('select-all-modules').addEventListener('click', () => {
            this.setAllModules(true);
        });
        
        document.getElementById('deselect-all-modules').addEventListener('click', () => {
            this.setAllModules(false);
        });
    }
    
    setAllModules(checked) {
        const checkboxes = document.querySelectorAll('.analysis-modules input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = checked;
        });
    }
    
    setupModuleDependencies() {
        // For now, no dependencies, but this could be extended
        // Example: complexity analysis might depend on vocabulary analysis
    }
    
    setupModuleDescriptions() {
        const moduleGroups = document.querySelectorAll('.module-group');
        moduleGroups.forEach(group => {
            const description = group.querySelector('.module-description');
            if (description) {
                // Add expand/collapse functionality for longer descriptions
                this.makeDescriptionExpandable(description);
            }
        });
    }
    
    makeDescriptionExpandable(description) {
        const fullText = description.textContent;
        if (fullText.length > 100) {
            const shortText = fullText.substring(0, 100) + '...';
            description.innerHTML = `
                <span class="short-desc">${shortText}</span>
                <span class="full-desc" style="display: none;">${fullText}</span>
                <button type="button" class="expand-btn">Show more</button>
            `;
            
            const expandBtn = description.querySelector('.expand-btn');
            expandBtn.addEventListener('click', () => {
                const shortDesc = description.querySelector('.short-desc');
                const fullDesc = description.querySelector('.full-desc');
                
                if (fullDesc.style.display === 'none') {
                    shortDesc.style.display = 'none';
                    fullDesc.style.display = 'inline';
                    expandBtn.textContent = 'Show less';
                } else {
                    shortDesc.style.display = 'inline';
                    fullDesc.style.display = 'none';
                    expandBtn.textContent = 'Show more';
                }
            });
        }
    }
    
    setupResponsiveBehaviors() {
        // Handle mobile menu toggles if needed
        this.setupMobileOptimizations();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.handleWindowResize();
        });
    }
    
    setupMobileOptimizations() {
        // Optimize for mobile devices
        if (window.innerWidth <= 768) {
            this.enableMobileMode();
        }
        
        // Listen for orientation changes
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleOrientationChange();
            }, 100);
        });
    }
    
    enableMobileMode() {
        document.body.classList.add('mobile-mode');
        
        // Adjust textarea height for mobile
        const textInput = document.getElementById('text-input');
        textInput.rows = 6;
    }
    
    handleWindowResize() {
        if (window.innerWidth <= 768) {
            this.enableMobileMode();
        } else {
            document.body.classList.remove('mobile-mode');
            const textInput = document.getElementById('text-input');
            textInput.rows = 10;
        }
    }
    
    handleOrientationChange() {
        // Adjust layout for orientation changes
        this.handleWindowResize();
    }
    
    setupAccessibilityFeatures() {
        // Keyboard navigation
        this.setupKeyboardNavigation();
        
        // Screen reader support
        this.setupScreenReaderSupport();
        
        // High contrast mode detection
        this.setupHighContrastMode();
    }
    
    setupKeyboardNavigation() {
        // Tab order management
        const focusableElements = document.querySelectorAll(
            'input, button, textarea, select, [tabindex]:not([tabindex="-1"])'
        );
        
        // Add visual focus indicators
        focusableElements.forEach(element => {
            element.addEventListener('focus', (e) => {
                e.target.classList.add('keyboard-focus');
            });
            
            element.addEventListener('blur', (e) => {
                e.target.classList.remove('keyboard-focus');
            });
        });
    }
    
    setupScreenReaderSupport() {
        // Add ARIA labels and descriptions
        this.addAriaLabels();
        
        // Live regions for dynamic content
        this.setupLiveRegions();
    }
    
    addAriaLabels() {
        // Add missing ARIA labels
        const textInput = document.getElementById('text-input');
        textInput.setAttribute('aria-label', 'Enter English text for analysis');
        
        const apiKeyInput = document.getElementById('api-key');
        apiKeyInput.setAttribute('aria-label', 'Enter your Gemini API key');
        
        // Add role attributes
        const resultsSection = document.getElementById('results-section');
        resultsSection.setAttribute('role', 'region');
        resultsSection.setAttribute('aria-label', 'Analysis results');
    }
    
    setupLiveRegions() {
        // Create live region for status updates
        const liveRegion = document.createElement('div');
        liveRegion.id = 'live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.style.position = 'absolute';
        liveRegion.style.left = '-10000px';
        liveRegion.style.width = '1px';
        liveRegion.style.height = '1px';
        liveRegion.style.overflow = 'hidden';
        
        document.body.appendChild(liveRegion);
    }
    
    setupHighContrastMode() {
        // Detect high contrast mode preference
        if (window.matchMedia('(prefers-contrast: high)').matches) {
            document.body.classList.add('high-contrast');
        }
        
        // Listen for changes
        window.matchMedia('(prefers-contrast: high)').addEventListener('change', (e) => {
            if (e.matches) {
                document.body.classList.add('high-contrast');
            } else {
                document.body.classList.remove('high-contrast');
            }
        });
    }
    
    // Utility methods for UI feedback
    showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        
        // Set background color based on type
        const colors = {
            success: '#2E7D32',
            error: '#D32F2F',
            warning: '#F57C00',
            info: '#1976D2'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        // Animate out and remove
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, duration);
        
        // Update live region for screen readers
        const liveRegion = document.getElementById('live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
        }
    }
    
    updateProgress(percentage, message = '') {
        // Update progress indicator if it exists
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
            progressBar.setAttribute('aria-valuenow', percentage);
        }
        
        if (message) {
            const progressText = document.getElementById('progress-text');
            if (progressText) {
                progressText.textContent = message;
            }
        }
    }
}