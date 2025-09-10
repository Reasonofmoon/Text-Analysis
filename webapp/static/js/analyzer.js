/**
 * Analysis Engine for English Text Analyzer
 * Handles communication with Gemini API and text analysis logic
 */

class AnalysisEngine {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';
        this.analysisModules = {
            vocabulary: new VocabularyAnalyzer(),
            grammar: new GrammarAnalyzer(),
            structure: new StructureAnalyzer(),
            content: new ContentAnalyzer(),
            complexity: new ComplexityAnalyzer()
        };
    }
    
    /**
     * Analyze text with selected modules
     */
    async analyzeText(text, options = {}) {
        const { modules = Object.keys(this.analysisModules) } = options;
        
        const results = {
            text: text,
            wordCount: this.countWords(text),
            charCount: text.length,
            analysisDate: new Date().toISOString(),
            modules: {}
        };
        
        // Run analysis for each selected module
        for (const moduleName of modules) {
            if (this.analysisModules[moduleName]) {
                try {
                    const moduleResult = await this.runModuleAnalysis(text, moduleName);
                    results.modules[moduleName] = moduleResult;
                    results[moduleName] = moduleResult; // For backward compatibility
                } catch (error) {
                    console.error(`Error in ${moduleName} analysis:`, error);
                    results.modules[moduleName] = {
                        error: error.message,
                        details: 'Analysis failed'
                    };
                }
            }
        }
        
        return results;
    }
    
    /**
     * Run analysis for a specific module
     */
    async runModuleAnalysis(text, moduleName) {
        const analyzer = this.analysisModules[moduleName];
        if (!analyzer) {
            throw new Error(`Unknown analysis module: ${moduleName}`);
        }
        
        const prompt = analyzer.generatePrompt(text);
        const response = await this.callGeminiAPI(prompt);
        
        return analyzer.processResponse(response, text);
    }
    
    /**
     * Call Gemini API
     */
    async callGeminiAPI(prompt) {
        const requestBody = {
            contents: [{
                parts: [{
                    text: prompt
                }]
            }],
            generationConfig: {
                temperature: 0.1,
                topK: 1,
                topP: 1,
                maxOutputTokens: 2048,
            }
        };
        
        const response = await fetch(`${this.baseURL}?key=${this.apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`API request failed: ${response.status} ${response.statusText}. ${errorData.error?.message || ''}`);
        }
        
        const data = await response.json();
        
        if (!data.candidates || !data.candidates[0] || !data.candidates[0].content) {
            throw new Error('Invalid API response format');
        }
        
        return data.candidates[0].content.parts[0].text;
    }
    
    /**
     * Count words in text
     */
    countWords(text) {
        return text.trim() ? text.trim().split(/\s+/).length : 0;
    }
}

/**
 * Base class for analysis modules
 */
class BaseAnalyzer {
    generatePrompt(text) {
        throw new Error('generatePrompt method must be implemented');
    }
    
    processResponse(response, originalText) {
        throw new Error('processResponse method must be implemented');
    }
    
    /**
     * Parse JSON response safely
     */
    parseJSONResponse(response) {
        try {
            // Try to extract JSON from response if it's wrapped in text
            const jsonMatch = response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                return JSON.parse(jsonMatch[0]);
            }
            return JSON.parse(response);
        } catch (error) {
            console.warn('Failed to parse JSON response:', error);
            return { error: 'Failed to parse response', raw: response };
        }
    }
}

/**
 * Vocabulary Analysis Module
 */
class VocabularyAnalyzer extends BaseAnalyzer {
    generatePrompt(text) {
        return `Analyze the vocabulary in the following English text. Provide a detailed analysis including:

1. Overall difficulty level (CEFR: A1, A2, B1, B2, C1, C2)
2. Academic vocabulary count and examples
3. Complex/advanced words and their meanings
4. Word frequency analysis
5. Domain-specific terminology
6. Collocations and idiomatic expressions

Text to analyze:
"${text}"

Please provide the analysis in JSON format with the following structure:
{
  "level": "B2",
  "academicCount": 5,
  "complexCount": 8,
  "academicWords": ["analyze", "comprehensive", "methodology"],
  "complexWords": [{"word": "paradigm", "meaning": "a typical example or pattern"}],
  "collocations": ["make progress", "take into account"],
  "idioms": ["break the ice"],
  "domainTerms": ["technical", "scientific"],
  "frequencyAnalysis": {"high": 15, "medium": 25, "low": 10},
  "details": "Detailed explanation of vocabulary patterns and educational insights"
}`;
    }
    
    processResponse(response, originalText) {
        const parsed = this.parseJSONResponse(response);
        
        if (parsed.error) {
            return {
                level: 'Unknown',
                academicCount: 0,
                complexCount: 0,
                details: 'Analysis failed: ' + parsed.error
            };
        }
        
        return {
            level: parsed.level || 'Unknown',
            academicCount: parsed.academicCount || 0,
            complexCount: parsed.complexCount || 0,
            academicWords: parsed.academicWords || [],
            complexWords: parsed.complexWords || [],
            collocations: parsed.collocations || [],
            idioms: parsed.idioms || [],
            domainTerms: parsed.domainTerms || [],
            frequencyAnalysis: parsed.frequencyAnalysis || {},
            details: parsed.details || 'Vocabulary analysis completed'
        };
    }
}

/**
 * Grammar Analysis Module
 */
class GrammarAnalyzer extends BaseAnalyzer {
    generatePrompt(text) {
        return `Analyze the grammar and syntax in the following English text. Provide a detailed analysis including:

1. Sentence types (simple, compound, complex, compound-complex) with counts
2. Tense usage patterns
3. Voice usage (active/passive)
4. Complex grammatical structures
5. Clause analysis
6. Syntactic complexity score (1-10)

Text to analyze:
"${text}"

Please provide the analysis in JSON format with the following structure:
{
  "sentenceTypes": {"simple": 3, "compound": 2, "complex": 4, "compound-complex": 1},
  "tenseUsage": {"present": 5, "past": 3, "future": 1, "perfect": 2},
  "voiceUsage": {"active": 80, "passive": 20},
  "complexStructures": ["relative clauses", "participial phrases"],
  "clauseAnalysis": {"main": 10, "subordinate": 6, "relative": 3},
  "complexityScore": 7.5,
  "details": "Detailed explanation of grammatical patterns and educational insights"
}`;
    }
    
    processResponse(response, originalText) {
        const parsed = this.parseJSONResponse(response);
        
        if (parsed.error) {
            return {
                sentenceTypes: 'Analysis failed',
                tenseUsage: 'Analysis failed',
                complexityScore: 'N/A',
                details: 'Analysis failed: ' + parsed.error
            };
        }
        
        return {
            sentenceTypes: this.formatSentenceTypes(parsed.sentenceTypes),
            tenseUsage: this.formatTenseUsage(parsed.tenseUsage),
            voiceUsage: parsed.voiceUsage || {},
            complexStructures: parsed.complexStructures || [],
            clauseAnalysis: parsed.clauseAnalysis || {},
            complexityScore: parsed.complexityScore || 'N/A',
            details: parsed.details || 'Grammar analysis completed'
        };
    }
    
    formatSentenceTypes(types) {
        if (!types) return 'No data';
        return Object.entries(types)
            .map(([type, count]) => `${type}: ${count}`)
            .join(', ');
    }
    
    formatTenseUsage(tenses) {
        if (!tenses) return 'No data';
        return Object.entries(tenses)
            .map(([tense, count]) => `${tense}: ${count}`)
            .join(', ');
    }
}

/**
 * Structure Analysis Module
 */
class StructureAnalyzer extends BaseAnalyzer {
    generatePrompt(text) {
        return `Analyze the structure and organization of the following English text. Provide a detailed analysis including:

1. Text organization pattern (chronological, spatial, compare-contrast, cause-effect, etc.)
2. Paragraph structure and topic sentences
3. Transition markers and connectors
4. Coherence and cohesion elements
5. Discourse markers
6. Overall coherence score (1-10)

Text to analyze:
"${text}"

Please provide the analysis in JSON format with the following structure:
{
  "organization": "cause-effect",
  "paragraphCount": 3,
  "topicSentences": ["First paragraph topic", "Second paragraph topic"],
  "transitionMarkers": ["however", "therefore", "in addition"],
  "coherenceElements": ["pronoun references", "lexical repetition"],
  "discourseMarkers": ["firstly", "in conclusion"],
  "coherenceScore": 8.5,
  "transitionCount": 5,
  "details": "Detailed explanation of structural patterns and educational insights"
}`;
    }
    
    processResponse(response, originalText) {
        const parsed = this.parseJSONResponse(response);
        
        if (parsed.error) {
            return {
                organization: 'Analysis failed',
                coherenceScore: 'N/A',
                transitionCount: 0,
                details: 'Analysis failed: ' + parsed.error
            };
        }
        
        return {
            organization: parsed.organization || 'Unknown',
            paragraphCount: parsed.paragraphCount || 0,
            topicSentences: parsed.topicSentences || [],
            transitionMarkers: parsed.transitionMarkers || [],
            coherenceElements: parsed.coherenceElements || [],
            discourseMarkers: parsed.discourseMarkers || [],
            coherenceScore: parsed.coherenceScore || 'N/A',
            transitionCount: parsed.transitionCount || 0,
            details: parsed.details || 'Structure analysis completed'
        };
    }
}

/**
 * Content Analysis Module
 */
class ContentAnalyzer extends BaseAnalyzer {
    generatePrompt(text) {
        return `Analyze the content and meaning of the following English text. Provide a detailed analysis including:

1. Main ideas and thesis statements
2. Supporting details and evidence types
3. Argument structure (if applicable)
4. Key themes and topics
5. Rhetorical devices used
6. Content complexity and depth

Text to analyze:
"${text}"

Please provide the analysis in JSON format with the following structure:
{
  "mainIdeas": ["Primary theme", "Secondary theme"],
  "thesisStatement": "Main argument or central claim",
  "supportingDetails": ["Evidence 1", "Evidence 2"],
  "evidenceTypes": ["examples", "statistics", "expert opinions"],
  "argumentStructure": "claim-evidence-warrant",
  "themes": ["education", "technology"],
  "rhetoricalDevices": ["metaphor", "repetition"],
  "contentComplexity": "high",
  "mainIdeasCount": 2,
  "supportingDetailsCount": 5,
  "details": "Detailed explanation of content patterns and educational insights"
}`;
    }
    
    processResponse(response, originalText) {
        const parsed = this.parseJSONResponse(response);
        
        if (parsed.error) {
            return {
                mainIdeasCount: 0,
                supportingDetailsCount: 0,
                argumentStructure: 'Analysis failed',
                details: 'Analysis failed: ' + parsed.error
            };
        }
        
        return {
            mainIdeas: parsed.mainIdeas || [],
            thesisStatement: parsed.thesisStatement || '',
            supportingDetails: parsed.supportingDetails || [],
            evidenceTypes: parsed.evidenceTypes || [],
            argumentStructure: parsed.argumentStructure || 'Unknown',
            themes: parsed.themes || [],
            rhetoricalDevices: parsed.rhetoricalDevices || [],
            contentComplexity: parsed.contentComplexity || 'Unknown',
            mainIdeasCount: parsed.mainIdeasCount || 0,
            supportingDetailsCount: parsed.supportingDetailsCount || 0,
            details: parsed.details || 'Content analysis completed'
        };
    }
}

/**
 * Complexity Analysis Module
 */
class ComplexityAnalyzer extends BaseAnalyzer {
    generatePrompt(text) {
        return `Analyze the complexity and readability of the following English text. Provide a detailed analysis including:

1. Readability scores (approximate Flesch-Kincaid grade level)
2. CEFR level estimation
3. Lexical diversity measures
4. Syntactic complexity indicators
5. Information density assessment
6. Recommendations for text adaptation

Text to analyze:
"${text}"

Please provide the analysis in JSON format with the following structure:
{
  "readabilityScore": "Grade 10",
  "cefrLevel": "B2",
  "lexicalDiversity": 0.75,
  "syntacticComplexity": "high",
  "informationDensity": "medium",
  "averageSentenceLength": 18.5,
  "averageWordLength": 4.8,
  "complexSentenceRatio": 0.6,
  "adaptationRecommendations": ["Simplify vocabulary", "Shorten sentences"],
  "details": "Detailed explanation of complexity patterns and educational insights"
}`;
    }
    
    processResponse(response, originalText) {
        const parsed = this.parseJSONResponse(response);
        
        if (parsed.error) {
            return {
                readabilityScore: 'Analysis failed',
                cefrLevel: 'Unknown',
                lexicalDiversity: 'N/A',
                details: 'Analysis failed: ' + parsed.error
            };
        }
        
        return {
            readabilityScore: parsed.readabilityScore || 'Unknown',
            cefrLevel: parsed.cefrLevel || 'Unknown',
            lexicalDiversity: parsed.lexicalDiversity || 'N/A',
            syntacticComplexity: parsed.syntacticComplexity || 'Unknown',
            informationDensity: parsed.informationDensity || 'Unknown',
            averageSentenceLength: parsed.averageSentenceLength || 'N/A',
            averageWordLength: parsed.averageWordLength || 'N/A',
            complexSentenceRatio: parsed.complexSentenceRatio || 'N/A',
            adaptationRecommendations: parsed.adaptationRecommendations || [],
            details: parsed.details || 'Complexity analysis completed'
        };
    }
}