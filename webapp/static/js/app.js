/**
 * Main application controller for English Text Analyzer
 * Handles initialization, API key management, and core application flow
 */

class EnglishTextAnalyzerApp {
    constructor() {
        this.apiKey = null;
        this.analyzer = null;
        this.ui = null;
        this.exporter = null;
        
        this.init();
    }
    
    /**
     * Initialize the application
     */
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupApp());
        } else {
            this.setupApp();
        }
    }
    
    /**
     * Set up the application after DOM is ready
     */
    setupApp() {
        // Initialize components
        this.ui = new UIManager();
        this.exporter = new ExportManager();
        
        // Load saved API key
        this.loadSavedAPIKey();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Initialize UI state
        this.updateUIState();
        
        console.log('English Text Analyzer initialized');
    }
    
    /**
     * Set up all event listeners
     */
    setupEventListeners() {
        // API Key management
        const saveKeyBtn = document.getElementById('save-key-btn');
        const apiKeyInput = document.getElementById('api-key');
        
        if (saveKeyBtn) {
            saveKeyBtn.addEventListener('click', () => this.saveAPIKey());
        }
        
        if (apiKeyInput) {
            apiKeyInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.saveAPIKey();
                }
            });
        }
        
        // Text input management
        const textInput = document.getElementById('text-input');
        const clearBtn = document.getElementById('clear-btn');
        const analyzeBtn = document.getElementById('analyze-btn');
        
        if (textInput) {
            textInput.addEventListener('input', () => this.updateTextStats());
            textInput.addEventListener('paste', () => {
                // Update stats after paste event completes
                setTimeout(() => this.updateTextStats(), 10);
            });
        }
        
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearText());
        }
        
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.analyzeText());
        }
        
        // Export controls
        const exportHtmlBtn = document.getElementById('export-html-btn');
        const exportPdfBtn = document.getElementById('export-pdf-btn');
        const printBtn = document.getElementById('print-btn');
        
        if (exportHtmlBtn) {
            exportHtmlBtn.addEventListener('click', () => this.exportHTML());
        }
        
        if (exportPdfBtn) {
            exportPdfBtn.addEventListener('click', () => this.exportPDF());
        }
        
        if (printBtn) {
            printBtn.addEventListener('click', () => this.printResults());
        }
    }
    
    /**
     * Load saved API key from localStorage
     */
    loadSavedAPIKey() {
        try {
            const savedKey = localStorage.getItem('gemini_api_key');
            if (savedKey) {
                this.apiKey = savedKey;
                const apiKeyInput = document.getElementById('api-key');
                if (apiKeyInput) {
                    apiKeyInput.value = savedKey;
                }
                this.showStatus('API key loaded', 'success');
                this.initializeAnalyzer();
            }
        } catch (error) {
            console.error('Error loading saved API key:', error);
        }
    }
    
    /**
     * Save API key to localStorage
     */
    saveAPIKey() {
        const apiKeyInput = document.getElementById('api-key');
        if (!apiKeyInput) return;
        
        const key = apiKeyInput.value.trim();
        
        if (!key) {
            this.showStatus('Please enter an API key', 'error');
            return;
        }
        
        if (!this.validateAPIKey(key)) {
            this.showStatus('Invalid API key format', 'error');
            return;
        }
        
        try {
            localStorage.setItem('gemini_api_key', key);
            this.apiKey = key;
            this.showStatus('API key saved successfully', 'success');
            this.initializeAnalyzer();
            this.updateUIState();
        } catch (error) {
            console.error('Error saving API key:', error);
            this.showStatus('Error saving API key', 'error');
        }
    }
    
    /**
     * Validate API key format
     */
    validateAPIKey(key) {
        // Basic validation for Gemini API key format
        return key && key.startsWith('AIza') && key.length > 30;
    }
    
    /**
     * Initialize the analyzer with the API key
     */
    initializeAnalyzer() {
        if (this.apiKey && typeof AnalysisEngine !== 'undefined') {
            this.analyzer = new AnalysisEngine(this.apiKey);
        }
    }
    
    /**
     * Update text statistics
     */
    updateTextStats() {
        const textInput = document.getElementById('text-input');
        const wordCountEl = document.getElementById('word-count');
        const charCountEl = document.getElementById('char-count');
        
        if (!textInput || !wordCountEl || !charCountEl) return;
        
        const text = textInput.value;
        const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
        const charCount = text.length;
        
        wordCountEl.textContent = `Words: ${wordCount}`;
        charCountEl.textContent = `Characters: ${charCount}`;
        
        this.updateUIState();
    }
    
    /**
     * Clear text input
     */
    clearText() {
        const textInput = document.getElementById('text-input');
        if (textInput) {
            textInput.value = '';
            this.updateTextStats();
            this.hideResults();
        }
    }
    
    /**
     * Analyze the input text
     */
    async analyzeText() {
        const textInput = document.getElementById('text-input');
        if (!textInput || !this.analyzer) return;
        
        const text = textInput.value.trim();
        if (!text) {
            this.showStatus('Please enter some text to analyze', 'warning');
            return;
        }
        
        if (text.split(/\s+/).length < 10) {
            this.showStatus('Please enter at least 10 words for meaningful analysis', 'warning');
            return;
        }
        
        try {
            this.showLoading(true);
            this.hideResults();
            
            // Get selected analysis modules
            const selectedModules = this.getSelectedAnalysisModules();
            
            // Perform analysis
            const results = await this.analyzer.analyzeText(text, {
                modules: selectedModules
            });
            
            // Display results
            this.displayResults(results);
            this.showResults();
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showStatus('Error during analysis: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    /**
     * Get selected analysis modules
     */
    getSelectedAnalysisModules() {
        const modules = [];
        const checkboxes = [
            'vocabulary-analysis',
            'grammar-analysis', 
            'structure-analysis',
            'content-analysis',
            'complexity-analysis'
        ];
        
        checkboxes.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox && checkbox.checked) {
                modules.push(id.replace('-analysis', ''));
            }
        });
        
        return modules;
    }
    
    /**
     * Display analysis results
     */
    displayResults(results) {
        const resultsContainer = document.getElementById('analysis-results');
        if (!resultsContainer) return;
        
        // Clear previous results
        resultsContainer.innerHTML = '';
        
        // Create results HTML
        const resultsHTML = this.generateResultsHTML(results);
        resultsContainer.innerHTML = resultsHTML;
    }
    
    /**
     * Generate HTML for analysis results
     */
    generateResultsHTML(results) {
        let html = '<div class="analysis-results-content">';
        
        // Add text info header
        html += `
            <div class="text-info-header">
                <h3>Analysis Summary</h3>
                <div class="text-stats-summary">
                    <span>Words: ${results.wordCount || 0}</span>
                    <span>Characters: ${results.charCount || 0}</span>
                    <span>Analysis Date: ${new Date().toLocaleDateString()}</span>
                </div>
            </div>
        `;
        
        // Add placeholder for each analysis type
        if (results.vocabulary) {
            html += this.generateVocabularyHTML(results.vocabulary);
        }
        
        if (results.grammar) {
            html += this.generateGrammarHTML(results.grammar);
        }
        
        if (results.structure) {
            html += this.generateStructureHTML(results.structure);
        }
        
        if (results.content) {
            html += this.generateContentHTML(results.content);
        }
        
        if (results.complexity) {
            html += this.generateComplexityHTML(results.complexity);
        }
        
        html += '</div>';
        return html;
    }
    
    /**
     * Generate vocabulary analysis HTML
     */
    generateVocabularyHTML(vocabulary) {
        return `
            <div class="analysis-section vocabulary-section">
                <h3>Vocabulary Analysis</h3>
                <div class="vocabulary-content">
                    <p><strong>Difficulty Level:</strong> ${vocabulary.level || 'Analyzing...'}</p>
                    <p><strong>Academic Words:</strong> ${vocabulary.academicCount || 0}</p>
                    <p><strong>Complex Terms:</strong> ${vocabulary.complexCount || 0}</p>
                    <div class="vocabulary-details">
                        ${vocabulary.details || 'Analysis in progress...'}
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Generate grammar analysis HTML
     */
    generateGrammarHTML(grammar) {
        return `
            <div class="analysis-section grammar-section">
                <h3>Grammar Analysis</h3>
                <div class="grammar-content">
                    <p><strong>Sentence Types:</strong> ${grammar.sentenceTypes || 'Analyzing...'}</p>
                    <p><strong>Tense Usage:</strong> ${grammar.tenseUsage || 'Analyzing...'}</p>
                    <p><strong>Complexity Score:</strong> ${grammar.complexityScore || 'Calculating...'}</p>
                    <div class="grammar-details">
                        ${grammar.details || 'Analysis in progress...'}
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Generate structure analysis HTML
     */
    generateStructureHTML(structure) {
        return `
            <div class="analysis-section structure-section">
                <h3>Structure Analysis</h3>
                <div class="structure-content">
                    <p><strong>Organization:</strong> ${structure.organization || 'Analyzing...'}</p>
                    <p><strong>Coherence Score:</strong> ${structure.coherenceScore || 'Calculating...'}</p>
                    <p><strong>Transition Markers:</strong> ${structure.transitionCount || 0}</p>
                    <div class="structure-details">
                        ${structure.details || 'Analysis in progress...'}
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Generate content analysis HTML
     */
    generateContentHTML(content) {
        return `
            <div class="analysis-section content-section">
                <h3>Content Analysis</h3>
                <div class="content-content">
                    <p><strong>Main Ideas:</strong> ${content.mainIdeasCount || 0}</p>
                    <p><strong>Supporting Details:</strong> ${content.supportingDetailsCount || 0}</p>
                    <p><strong>Argument Structure:</strong> ${content.argumentStructure || 'Analyzing...'}</p>
                    <div class="content-details">
                        ${content.details || 'Analysis in progress...'}
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Generate complexity analysis HTML
     */
    generateComplexityHTML(complexity) {
        return `
            <div class="analysis-section complexity-section">
                <h3>Complexity Analysis</h3>
                <div class="complexity-content">
                    <p><strong>Readability Score:</strong> ${complexity.readabilityScore || 'Calculating...'}</p>
                    <p><strong>CEFR Level:</strong> ${complexity.cefrLevel || 'Estimating...'}</p>
                    <p><strong>Lexical Diversity:</strong> ${complexity.lexicalDiversity || 'Calculating...'}</p>
                    <div class="complexity-details">
                        ${complexity.details || 'Analysis in progress...'}
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Show/hide loading state
     */
    showLoading(show) {
        const loadingSection = document.getElementById('loading-section');
        if (loadingSection) {
            loadingSection.style.display = show ? 'block' : 'none';
        }
    }
    
    /**
     * Show/hide results section
     */
    showResults() {
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            resultsSection.style.display = 'block';
        }
    }
    
    hideResults() {
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            resultsSection.style.display = 'none';
        }
    }
    
    /**
     * Export results as HTML
     */
    exportHTML() {
        if (this.exporter) {
            this.exporter.exportAsHTML();
        }
    }
    
    /**
     * Export results as PDF
     */
    exportPDF() {
        if (this.exporter) {
            this.exporter.exportAsPDF();
        }
    }
    
    /**
     * Print results
     */
    printResults() {
        window.print();
    }
    
    /**
     * Show status message
     */
    showStatus(message, type = 'info') {
        const statusEl = document.getElementById('key-status');
        if (!statusEl) return;
        
        statusEl.textContent = message;
        statusEl.className = `status-message ${type}`;
        
        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(() => {
                statusEl.textContent = '';
                statusEl.className = 'status-message';
            }, 3000);
        }
    }
    
    /**
     * Update UI state based on current conditions
     */
    updateUIState() {
        const analyzeBtn = document.getElementById('analyze-btn');
        const textInput = document.getElementById('text-input');
        
        if (analyzeBtn && textInput) {
            const hasText = textInput.value.trim().length > 0;
            const hasAPIKey = !!this.apiKey;
            
            analyzeBtn.disabled = !(hasText && hasAPIKey);
        }
    }
}

// Initialize the application when the script loads
const app = new EnglishTextAnalyzerApp();