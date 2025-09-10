/**
 * English Text Analyzer - Main Application
 * Handles application initialization and coordination between modules
 */

class EnglishTextAnalyzerApp {
    constructor() {
        this.apiKeyManager = new APIKeyManager();
        this.analysisEngine = null;
        this.uiManager = new UIManager();
        this.exportManager = new ExportManager();
        
        this.currentResults = null;
        this.isAnalyzing = false;
        
        this.init();
    }
    
    init() {
        console.log('Initializing English Text Analyzer...');
        
        // Initialize UI components
        this.uiManager.init();
        this.exportManager.init();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Check for saved API key
        this.checkSavedAPIKey();
        
        // Load sample text if available
        this.loadSampleText();
        
        console.log('Application initialized successfully');
    }
    
    setupEventListeners() {
        // API Key management
        document.getElementById('save-api-key').addEventListener('click', () => {
            this.handleSaveAPIKey();
        });
        
        // Text input controls
        document.getElementById('clear-text').addEventListener('click', () => {
            this.clearText();
        });
        
        document.getElementById('sample-text').addEventListener('click', () => {
            this.loadSampleText();
        });
        
        // Text input monitoring for stats
        document.getElementById('text-input').addEventListener('input', (e) => {
            this.updateTextStats(e.target.value);
        });
        
        // Analysis button
        document.getElementById('analyze-btn').addEventListener('click', () => {
            this.handleAnalyzeText();
        });
        
        // Export controls
        document.getElementById('export-html').addEventListener('click', () => {
            const template = document.getElementById('export-template').value;
            this.exportManager.exportHTML(this.currentResults, template);
        });
        
        document.getElementById('export-pdf').addEventListener('click', () => {
            this.exportManager.exportPDF(this.currentResults);
        });
        
        document.getElementById('export-json').addEventListener('click', () => {
            this.exportManager.exportJSON(this.currentResults);
        });
        
        document.getElementById('print-report').addEventListener('click', () => {
            this.exportManager.printReport();
        });
    }
    
    checkSavedAPIKey() {
        const savedKey = this.apiKeyManager.getAPIKey();
        if (savedKey) {
            document.getElementById('api-key').value = savedKey;
            this.updateAPIKeyStatus('success', 'API Key loaded');
            this.initializeAnalysisEngine(savedKey);
        }
    }
    
    handleSaveAPIKey() {
        const keyInput = document.getElementById('api-key');
        const apiKey = keyInput.value.trim();
        
        if (!apiKey) {
            this.updateAPIKeyStatus('error', 'Please enter an API key');
            return;
        }
        
        if (this.apiKeyManager.validateAPIKey(apiKey)) {
            this.apiKeyManager.setAPIKey(apiKey);
            this.updateAPIKeyStatus('success', 'API Key saved');
            this.initializeAnalysisEngine(apiKey);
        } else {
            this.updateAPIKeyStatus('error', 'Invalid API key format');
        }
    }
    
    updateAPIKeyStatus(type, message) {
        const statusElement = document.getElementById('api-key-status');
        statusElement.textContent = message;
        statusElement.className = `api-key-status ${type}`;
    }
    
    initializeAnalysisEngine(apiKey) {
        try {
            this.analysisEngine = new AnalysisEngineWrapper(apiKey);
            console.log('Analysis engine initialized');
        } catch (error) {
            console.error('Failed to initialize analysis engine:', error);
            this.updateAPIKeyStatus('error', 'Failed to initialize engine');
        }
    }
    
    clearText() {
        document.getElementById('text-input').value = '';
        this.updateTextStats('');
        this.hideResults();
    }
    
    loadSampleText() {
        const sampleText = `The rapid advancement of artificial intelligence has transformed numerous industries and aspects of daily life. Machine learning algorithms now power everything from recommendation systems to autonomous vehicles, demonstrating unprecedented capabilities in pattern recognition and decision-making.

However, this technological revolution raises important questions about the future of work, privacy, and human agency. As AI systems become increasingly sophisticated, society must grapple with ethical considerations and ensure that these powerful tools are developed and deployed responsibly.

The integration of AI into educational systems presents both opportunities and challenges. While personalized learning platforms can adapt to individual student needs and provide immediate feedback, concerns about data privacy and the potential replacement of human teachers remain significant considerations for educators and policymakers alike.`;
        
        document.getElementById('text-input').value = sampleText;
        this.updateTextStats(sampleText);
    }
    
    updateTextStats(text) {
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const chars = text.length;
        
        document.getElementById('word-count').textContent = `Words: ${words}`;
        document.getElementById('char-count').textContent = `Characters: ${chars}`;
    }
    
    async handleAnalyzeText() {
        if (this.isAnalyzing) {
            return;
        }
        
        const text = document.getElementById('text-input').value.trim();
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }
        
        if (!this.analysisEngine) {
            alert('Please configure your API key first.');
            return;
        }
        
        const selectedModules = this.getSelectedAnalysisModules();
        if (selectedModules.length === 0) {
            alert('Please select at least one analysis module.');
            return;
        }
        
        try {
            this.setAnalyzing(true);
            
            const results = await this.analysisEngine.analyzeText(text, {
                modules: selectedModules,
                onProgress: (percentage, message) => {
                    this.updateAnalysisProgress(percentage, message);
                }
            });
            
            this.currentResults = results;
            this.displayResults(results);
            
            // Show success message
            this.uiManager.showNotification('Analysis completed successfully!', 'success');
            
        } catch (error) {
            console.error('Analysis failed:', error);
            this.uiManager.showNotification(`Analysis failed: ${error.message}`, 'error');
        } finally {
            this.setAnalyzing(false);
        }
    }
    
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
            if (document.getElementById(id).checked) {
                modules.push(id.replace('-analysis', ''));
            }
        });
        
        return modules;
    }
    
    setAnalyzing(analyzing) {
        this.isAnalyzing = analyzing;
        const analyzeBtn = document.getElementById('analyze-btn');
        const loadingIndicator = document.getElementById('loading-indicator');
        
        if (analyzing) {
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = 'Analyzing...';
            loadingIndicator.style.display = 'flex';
        } else {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Text';
            loadingIndicator.style.display = 'none';
        }
    }
    
    updateAnalysisProgress(percentage, message) {
        const loadingIndicator = document.getElementById('loading-indicator');
        const loadingText = loadingIndicator.querySelector('span');
        
        if (loadingText) {
            loadingText.textContent = `${message} (${Math.round(percentage)}%)`;
        }
        
        // Update UI manager progress if available
        if (this.uiManager && this.uiManager.updateProgress) {
            this.uiManager.updateProgress(percentage, message);
        }
    }
    
    displayResults(results) {
        const resultsSection = document.getElementById('results-section');
        const resultsContent = document.getElementById('analysis-results-content');
        
        // Update results header
        document.getElementById('analysis-date').textContent = 
            `Analyzed: ${new Date().toLocaleString()}`;
        document.getElementById('text-length').textContent = 
            `${results.wordCount} words, ${results.charCount} characters`;
        
        // Clear previous results
        resultsContent.innerHTML = '';
        
        // Display each analysis module result
        if (results.vocabulary) {
            resultsContent.appendChild(this.createVocabularyResultElement(results.vocabulary));
        }
        
        if (results.grammar) {
            resultsContent.appendChild(this.createGrammarResultElement(results.grammar));
        }
        
        if (results.structure) {
            resultsContent.appendChild(this.createStructureResultElement(results.structure));
        }
        
        if (results.content) {
            resultsContent.appendChild(this.createContentResultElement(results.content));
        }
        
        if (results.complexity) {
            resultsContent.appendChild(this.createComplexityResultElement(results.complexity));
        }
        
        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    createVocabularyResultElement(vocabularyResult) {
        const element = document.createElement('div');
        element.className = 'result-module';
        
        let contentHTML = '<h3>🔤 Vocabulary Analysis</h3>';
        
        if (vocabularyResult.error) {
            contentHTML += `<div class="error-message">Error: ${vocabularyResult.error}</div>`;
        } else {
            contentHTML += '<div class="vocabulary-content">';
            
            // Display structured data if available
            if (vocabularyResult.structured) {
                const structured = vocabularyResult.structured;
                
                // Difficulty levels
                if (structured.difficultyLevels) {
                    contentHTML += '<div class="subsection"><h4>Difficulty Levels</h4>';
                    contentHTML += '<div class="vocabulary-grid">';
                    
                    if (structured.difficultyLevels.basic && structured.difficultyLevels.basic.length > 0) {
                        contentHTML += '<div class="difficulty-section basic">';
                        contentHTML += '<h5>Basic (A1-A2)</h5>';
                        contentHTML += '<div class="word-list">' + structured.difficultyLevels.basic.map(word => 
                            `<span class="word-tag basic">${word}</span>`).join('') + '</div>';
                        contentHTML += '</div>';
                    }
                    
                    if (structured.difficultyLevels.intermediate && structured.difficultyLevels.intermediate.length > 0) {
                        contentHTML += '<div class="difficulty-section intermediate">';
                        contentHTML += '<h5>Intermediate (B1-B2)</h5>';
                        contentHTML += '<div class="word-list">' + structured.difficultyLevels.intermediate.map(word => 
                            `<span class="word-tag intermediate">${word}</span>`).join('') + '</div>';
                        contentHTML += '</div>';
                    }
                    
                    if (structured.difficultyLevels.advanced && structured.difficultyLevels.advanced.length > 0) {
                        contentHTML += '<div class="difficulty-section advanced">';
                        contentHTML += '<h5>Advanced (C1-C2)</h5>';
                        contentHTML += '<div class="word-list">' + structured.difficultyLevels.advanced.map(word => 
                            `<span class="word-tag advanced">${word}</span>`).join('') + '</div>';
                        contentHTML += '</div>';
                    }
                    
                    contentHTML += '</div></div>';
                }
                
                // Academic vocabulary
                if (structured.academicVocabulary && structured.academicVocabulary.length > 0) {
                    contentHTML += '<div class="subsection"><h4>Academic Vocabulary</h4>';
                    contentHTML += '<div class="word-list">' + structured.academicVocabulary.map(word => 
                        `<span class="word-tag academic">${word}</span>`).join('') + '</div>';
                    contentHTML += '</div>';
                }
                
                // Collocations
                if (structured.collocations && structured.collocations.length > 0) {
                    contentHTML += '<div class="subsection"><h4>Collocations & Phrases</h4>';
                    contentHTML += '<div class="phrase-list">' + structured.collocations.map(phrase => 
                        `<span class="phrase-tag">${phrase}</span>`).join('') + '</div>';
                    contentHTML += '</div>';
                }
            }
            
            // Raw response as fallback
            if (vocabularyResult.rawResponse) {
                contentHTML += '<div class="subsection"><h4>Analysis Details</h4>';
                contentHTML += '<div class="raw-response">' + this.formatAnalysisText(vocabularyResult.rawResponse) + '</div>';
                contentHTML += '</div>';
            }
            
            contentHTML += '</div>';
        }
        
        element.innerHTML = contentHTML;
        return element;
    }
    
    createGrammarResultElement(grammarResult) {
        const element = document.createElement('div');
        element.className = 'result-module';
        
        let contentHTML = '<h3>📝 Grammar Analysis</h3>';
        
        if (grammarResult.error) {
            contentHTML += `<div class="error-message">Error: ${grammarResult.error}</div>`;
        } else {
            contentHTML += '<div class="grammar-content">';
            
            // Display structured data if available
            if (grammarResult.structured) {
                const structured = grammarResult.structured;
                
                // Sentence types
                if (structured.sentenceTypes) {
                    contentHTML += '<div class="subsection"><h4>Sentence Type Distribution</h4>';
                    contentHTML += '<div class="sentence-types-grid">';
                    
                    const types = structured.sentenceTypes;
                    const total = types.simple + types.compound + types.complex + types.compoundComplex;
                    
                    if (total > 0) {
                        contentHTML += `<div class="sentence-type-item">
                            <span class="type-label">Simple</span>
                            <span class="type-count">${types.simple}</span>
                            <span class="type-percentage">${Math.round(types.simple/total*100)}%</span>
                        </div>`;
                        contentHTML += `<div class="sentence-type-item">
                            <span class="type-label">Compound</span>
                            <span class="type-count">${types.compound}</span>
                            <span class="type-percentage">${Math.round(types.compound/total*100)}%</span>
                        </div>`;
                        contentHTML += `<div class="sentence-type-item">
                            <span class="type-label">Complex</span>
                            <span class="type-count">${types.complex}</span>
                            <span class="type-percentage">${Math.round(types.complex/total*100)}%</span>
                        </div>`;
                        contentHTML += `<div class="sentence-type-item">
                            <span class="type-label">Compound-Complex</span>
                            <span class="type-count">${types.compoundComplex}</span>
                            <span class="type-percentage">${Math.round(types.compoundComplex/total*100)}%</span>
                        </div>`;
                    }
                    
                    contentHTML += '</div></div>';
                }
            }
            
            // Raw response
            if (grammarResult.rawResponse) {
                contentHTML += '<div class="subsection"><h4>Grammar Analysis Details</h4>';
                contentHTML += '<div class="raw-response">' + this.formatAnalysisText(grammarResult.rawResponse) + '</div>';
                contentHTML += '</div>';
            }
            
            contentHTML += '</div>';
        }
        
        element.innerHTML = contentHTML;
        return element;
    }
    
    createStructureResultElement(structureResult) {
        const element = document.createElement('div');
        element.className = 'result-module';
        
        let contentHTML = '<h3>🏗️ Structure Analysis</h3>';
        
        if (structureResult.error) {
            contentHTML += `<div class="error-message">Error: ${structureResult.error}</div>`;
        } else {
            contentHTML += '<div class="structure-content">';
            
            if (structureResult.structured && structureResult.structured.transitionWords && structureResult.structured.transitionWords.length > 0) {
                contentHTML += '<div class="subsection"><h4>Transition Markers</h4>';
                contentHTML += '<div class="transition-list">' + structureResult.structured.transitionWords.map(word => 
                    `<span class="transition-tag">${word}</span>`).join('') + '</div>';
                contentHTML += '</div>';
            }
            
            if (structureResult.rawResponse) {
                contentHTML += '<div class="subsection"><h4>Structure Analysis Details</h4>';
                contentHTML += '<div class="raw-response">' + this.formatAnalysisText(structureResult.rawResponse) + '</div>';
                contentHTML += '</div>';
            }
            
            contentHTML += '</div>';
        }
        
        element.innerHTML = contentHTML;
        return element;
    }
    
    createContentResultElement(contentResult) {
        const element = document.createElement('div');
        element.className = 'result-module';
        
        let contentHTML = '<h3>💡 Content Analysis</h3>';
        
        if (contentResult.error) {
            contentHTML += `<div class="error-message">Error: ${contentResult.error}</div>`;
        } else {
            contentHTML += '<div class="content-analysis">';
            
            if (contentResult.rawResponse) {
                contentHTML += '<div class="subsection"><h4>Content Analysis Details</h4>';
                contentHTML += '<div class="raw-response">' + this.formatAnalysisText(contentResult.rawResponse) + '</div>';
                contentHTML += '</div>';
            }
            
            contentHTML += '</div>';
        }
        
        element.innerHTML = contentHTML;
        return element;
    }
    
    createComplexityResultElement(complexityResult) {
        const element = document.createElement('div');
        element.className = 'result-module';
        
        let contentHTML = '<h3>📊 Complexity Analysis</h3>';
        
        if (complexityResult.error) {
            contentHTML += `<div class="error-message">Error: ${complexityResult.error}</div>`;
        } else {
            contentHTML += '<div class="complexity-content">';
            
            // Display structured metrics if available
            if (complexityResult.structured) {
                const structured = complexityResult.structured;
                
                if (structured.readabilityMetrics) {
                    contentHTML += '<div class="subsection"><h4>Readability Metrics</h4>';
                    contentHTML += '<div class="metrics-display">';
                    
                    if (structured.readabilityMetrics.fleschKincaid) {
                        contentHTML += `<div class="metric-item">
                            <span class="metric-label">Flesch-Kincaid Grade Level</span>
                            <span class="metric-value">${structured.readabilityMetrics.fleschKincaid}</span>
                        </div>`;
                    }
                    
                    if (structured.cefrLevel) {
                        contentHTML += `<div class="metric-item">
                            <span class="metric-label">Estimated CEFR Level</span>
                            <span class="metric-value cefr-level">${structured.cefrLevel}</span>
                        </div>`;
                    }
                    
                    contentHTML += '</div></div>';
                }
                
                if (structured.recommendations) {
                    contentHTML += '<div class="subsection"><h4>Recommendations</h4>';
                    contentHTML += '<div class="recommendations-box">' + structured.recommendations + '</div>';
                    contentHTML += '</div>';
                }
            }
            
            if (complexityResult.rawResponse) {
                contentHTML += '<div class="subsection"><h4>Complexity Analysis Details</h4>';
                contentHTML += '<div class="raw-response">' + this.formatAnalysisText(complexityResult.rawResponse) + '</div>';
                contentHTML += '</div>';
            }
            
            contentHTML += '</div>';
        }
        
        element.innerHTML = contentHTML;
        return element;
    }
    
    hideResults() {
        document.getElementById('results-section').style.display = 'none';
        this.currentResults = null;
    }
    
    formatAnalysisText(text) {
        // Format the raw analysis text for better display
        return text
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/^\d+\.\s+(.+?):/gm, '<strong>$1:</strong>')
            .replace(/^-\s+(.+)/gm, '• $1')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>');
    }
}

// API Key Manager Class
class APIKeyManager {
    constructor() {
        this.storageKey = 'english_analyzer_api_key';
    }
    
    setAPIKey(key) {
        try {
            // Simple encoding (not encryption, just obfuscation)
            const encoded = btoa(key);
            localStorage.setItem(this.storageKey, encoded);
            return true;
        } catch (error) {
            console.error('Failed to save API key:', error);
            return false;
        }
    }
    
    getAPIKey() {
        try {
            const encoded = localStorage.getItem(this.storageKey);
            return encoded ? atob(encoded) : null;
        } catch (error) {
            console.error('Failed to retrieve API key:', error);
            return null;
        }
    }
    
    validateAPIKey(key) {
        // Basic validation for Gemini API key format
        return key && 
               typeof key === 'string' && 
               key.startsWith('AIza') && 
               key.length > 30;
    }
    
    clearAPIKey() {
        localStorage.removeItem(this.storageKey);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.englishTextAnalyzer = new EnglishTextAnalyzerApp();
});