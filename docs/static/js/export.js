/**
 * English Text Analyzer - Export Manager
 * Handles exporting analysis results in various formats
 */

class ExportManager {
    constructor() {
        this.initialized = false;
    }
    
    init() {
        if (this.initialized) return;
        
        console.log('Initializing Export Manager...');
        
        // Load external libraries if needed
        this.loadExportLibraries();
        
        this.initialized = true;
        console.log('Export Manager initialized');
    }
    
    async loadExportLibraries() {
        // Load jsPDF for PDF export
        if (!window.jsPDF) {
            try {
                await this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
                console.log('jsPDF loaded successfully');
            } catch (error) {
                console.warn('Failed to load jsPDF:', error);
            }
        }
        
        // Load html2canvas for better PDF rendering
        if (!window.html2canvas) {
            try {
                await this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');
                console.log('html2canvas loaded successfully');
            } catch (error) {
                console.warn('Failed to load html2canvas:', error);
            }
        }
    }
    
    loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    exportHTML(results, template = 'standard') {
        if (!results) {
            alert('No analysis results to export.');
            return;
        }
        
        try {
            const htmlContent = this.generateHTMLReport(results, template);
            const filename = this.getFilename(template, 'html');
            this.downloadFile(htmlContent, filename, 'text/html');
        } catch (error) {
            console.error('HTML export failed:', error);
            alert('Failed to export HTML report.');
        }
    }
    
    getFilename(template, extension) {
        const templateNames = {
            'standard': 'text-analysis-report',
            'educational': 'educational-analysis-report',
            'teacher': 'teachers-guide-report',
            'print': 'print-optimized-report'
        };
        
        const baseName = templateNames[template] || 'text-analysis-report';
        return `${baseName}.${extension}`;
    }
    
    exportPDF(results) {
        if (!results) {
            alert('No analysis results to export.');
            return;
        }
        
        if (!window.jsPDF) {
            alert('PDF export is not available. Please check your internet connection.');
            return;
        }
        
        try {
            this.generatePDFReport(results);
        } catch (error) {
            console.error('PDF export failed:', error);
            alert('Failed to export PDF report.');
        }
    }
    
    printReport() {
        const resultsSection = document.getElementById('results-section');
        if (!resultsSection || resultsSection.style.display === 'none') {
            alert('No analysis results to print.');
            return;
        }
        
        // Use the browser's print functionality with print CSS
        window.print();
    }
    
    generateHTMLReport(results, template = 'standard') {
        const timestamp = new Date().toLocaleString();
        
        // Choose template based on parameter
        switch (template) {
            case 'educational':
                return this.generateEducationalReport(results);
            case 'teacher':
                return this.generateTeacherGuide(results);
            case 'print':
                return this.generatePrintOptimizedReport(results);
            default:
                return this.generateStandardReport(results);
        }
    }
    
    generateStandardReport(results) {
        const timestamp = new Date().toLocaleString();
        
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>English Text Analysis Report</title>
    <style>
        body {
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.6;
            color: #000000;
            background-color: #FFFFFF;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .report-header {
            text-align: center;
            border-bottom: 3px solid #000000;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        
        .report-header h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .report-info {
            font-size: 0.9rem;
            color: #333333;
            margin-bottom: 1rem;
        }
        
        .analysis-section {
            border: 2px solid #000000;
            border-radius: 6px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            background: #FFFFFF;
        }
        
        .analysis-section h2 {
            color: #000000;
            border-bottom: 1px solid #CCCCCC;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .text-sample {
            background: #F5F5F5;
            border: 1px solid #CCCCCC;
            padding: 1rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            margin: 1rem 0;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .placeholder-content {
            color: #666666;
            font-style: italic;
        }
        
        @media print {
            body { margin: 0; padding: 1rem; }
            .analysis-section { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="report-header">
        <h1>English Text Analysis Report</h1>
        <div class="report-info">
            <p>Generated on: ${timestamp}</p>
            <p>Text Length: ${results.wordCount} words, ${results.charCount} characters</p>
        </div>
    </div>
    
    <div class="analysis-section">
        <h2>Original Text</h2>
        <div class="text-sample">${this.escapeHtml(results.text)}</div>
    </div>
    
    ${this.generateAnalysisSection('Vocabulary Analysis', results.vocabulary)}
    ${this.generateAnalysisSection('Grammar Analysis', results.grammar)}
    ${this.generateAnalysisSection('Structure Analysis', results.structure)}
    ${this.generateAnalysisSection('Content Analysis', results.content)}
    ${this.generateAnalysisSection('Complexity Analysis', results.complexity)}
    
    <div class="report-footer">
        <p style="text-align: center; color: #666666; font-size: 0.8rem; margin-top: 2rem;">
            Generated by English Text Analyzer
        </p>
    </div>
</body>
</html>`;
    }
    
    generateAnalysisSection(title, data) {
        if (!data) return '';
        
        return `
    <div class="analysis-section">
        <h2>${title}</h2>
        <div class="analysis-content">
            ${data.error ? 
                `<p style="color: #D32F2F;">Error: ${data.error}</p>` :
                `<p><strong>Analysis completed.</strong></p>
                 <div class="placeholder-content">
                     <p>Detailed ${title.toLowerCase()} results would be displayed here in a full implementation.</p>
                     <p>Raw response available in data export.</p>
                 </div>`
            }
        </div>
    </div>`;
    }
    
    async generatePDFReport(results) {
        try {
            // Show loading indicator
            this.showPDFLoadingIndicator();
            
            if (window.html2canvas) {
                await this.generatePDFFromHTML(results);
            } else {
                this.generateBasicPDFReport(results);
            }
        } catch (error) {
            console.error('PDF generation failed:', error);
            alert('Failed to generate PDF report. Please try again.');
        } finally {
            this.hidePDFLoadingIndicator();
        }
    }
    
    async generatePDFFromHTML(results) {
        // Create a temporary container with print-optimized content
        const printContainer = this.createPrintContainer(results);
        document.body.appendChild(printContainer);
        
        try {
            // Configure html2canvas for high quality
            const canvas = await html2canvas(printContainer, {
                scale: 2,
                useCORS: true,
                allowTaint: true,
                backgroundColor: '#FFFFFF',
                width: 794, // A4 width in pixels at 96 DPI
                height: 1123, // A4 height in pixels at 96 DPI
                scrollX: 0,
                scrollY: 0
            });
            
            const { jsPDF } = window.jsPDF;
            const doc = new jsPDF('p', 'mm', 'a4');
            
            const imgData = canvas.toDataURL('image/png');
            const imgWidth = 210; // A4 width in mm
            const pageHeight = 297; // A4 height in mm
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            let heightLeft = imgHeight;
            let position = 0;
            
            // Add first page
            doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
            
            // Add additional pages if needed
            while (heightLeft >= 0) {
                position = heightLeft - imgHeight;
                doc.addPage();
                doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;
            }
            
            doc.save('english-text-analysis-report.pdf');
            
        } finally {
            document.body.removeChild(printContainer);
        }
    }
    
    generateBasicPDFReport(results) {
        const { jsPDF } = window.jsPDF;
        const doc = new jsPDF('p', 'mm', 'a4');
        
        // A4 dimensions: 210mm x 297mm
        const pageWidth = 210;
        const pageHeight = 297;
        const margin = 15;
        const contentWidth = pageWidth - (2 * margin);
        let yPosition = margin;
        
        // Helper function to check if we need a new page
        const checkPageBreak = (requiredHeight) => {
            if (yPosition + requiredHeight > pageHeight - margin) {
                doc.addPage();
                yPosition = margin;
                return true;
            }
            return false;
        };
        
        // Header
        doc.setFontSize(18);
        doc.setFont('helvetica', 'bold');
        doc.text('English Text Analysis Report', margin, yPosition);
        yPosition += 10;
        
        // Subtitle
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.text('Educational Analysis for Language Learning', margin, yPosition);
        yPosition += 8;
        
        // Info box
        doc.setDrawColor(0, 0, 0);
        doc.rect(margin, yPosition, contentWidth, 20);
        yPosition += 5;
        
        doc.setFontSize(9);
        doc.text(`Generated: ${new Date().toLocaleString()}`, margin + 5, yPosition);
        yPosition += 4;
        doc.text(`Words: ${results.wordCount} | Characters: ${results.charCount} | Level: ${results.estimatedLevel || 'N/A'}`, margin + 5, yPosition);
        yPosition += 4;
        doc.text(`Sentences: ${results.sentenceCount || 'N/A'} | Paragraphs: ${results.paragraphCount || 'N/A'}`, margin + 5, yPosition);
        yPosition += 12;
        
        // Learning Objectives
        checkPageBreak(25);
        doc.setFillColor(232, 244, 253);
        doc.rect(margin, yPosition, contentWidth, 20, 'F');
        doc.setDrawColor(33, 150, 243);
        doc.rect(margin, yPosition, contentWidth, 20);
        
        yPosition += 5;
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.text('Learning Objectives', margin + 3, yPosition);
        yPosition += 4;
        
        doc.setFontSize(8);
        doc.setFont('helvetica', 'normal');
        const objectives = [
            '• Identify vocabulary at different CEFR levels',
            '• Recognize grammatical structures and patterns',
            '• Analyze text organization and coherence',
            '• Understand content structure and arguments'
        ];
        
        objectives.forEach(objective => {
            doc.text(objective, margin + 5, yPosition);
            yPosition += 3;
        });
        yPosition += 8;
        
        // Text Sample
        checkPageBreak(20);
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('📄 Text Sample', margin, yPosition);
        yPosition += 6;
        
        doc.setFillColor(248, 248, 248);
        doc.rect(margin, yPosition, contentWidth, 15, 'F');
        doc.setDrawColor(204, 204, 204);
        doc.rect(margin, yPosition, contentWidth, 15);
        
        yPosition += 4;
        doc.setFontSize(7);
        doc.setFont('courier', 'normal');
        const textSample = results.text.substring(0, 300) + (results.text.length > 300 ? '...' : '');
        const textLines = doc.splitTextToSize(textSample, contentWidth - 6);
        doc.text(textLines.slice(0, 3), margin + 3, yPosition); // Show only first 3 lines
        yPosition += 20;
        
        // Analysis Sections
        const sections = [
            { title: '🔤 Vocabulary Analysis', data: results.vocabulary, icon: '🔤' },
            { title: '📝 Grammar Analysis', data: results.grammar, icon: '📝' },
            { title: '🏗️ Structure Analysis', data: results.structure, icon: '🏗️' },
            { title: '💡 Content Analysis', data: results.content, icon: '💡' },
            { title: '📊 Complexity Analysis', data: results.complexity, icon: '📊' }
        ];
        
        sections.forEach(section => {
            checkPageBreak(30);
            
            // Section header
            doc.setFillColor(255, 255, 255);
            doc.rect(margin, yPosition, contentWidth, 8, 'F');
            doc.setDrawColor(0, 0, 0);
            doc.rect(margin, yPosition, contentWidth, 8);
            
            yPosition += 2;
            doc.setFontSize(11);
            doc.setFont('helvetica', 'bold');
            doc.text(section.title, margin + 2, yPosition + 4);
            yPosition += 10;
            
            // Section content
            doc.setFontSize(9);
            doc.setFont('helvetica', 'normal');
            
            if (section.data && section.data.error) {
                doc.setTextColor(211, 47, 47);
                doc.text(`Error: ${section.data.error}`, margin + 3, yPosition);
                doc.setTextColor(0, 0, 0);
            } else if (section.data) {
                doc.text('✓ Analysis completed successfully', margin + 3, yPosition);
                yPosition += 4;
                doc.setFontSize(8);
                doc.text('Key findings and detailed results available in full report', margin + 3, yPosition);
                
                // Add some sample metrics if available
                if (section.data.summary) {
                    yPosition += 4;
                    const summaryLines = doc.splitTextToSize(section.data.summary, contentWidth - 6);
                    doc.text(summaryLines.slice(0, 2), margin + 3, yPosition);
                    yPosition += summaryLines.slice(0, 2).length * 3;
                }
            } else {
                doc.setTextColor(158, 158, 158);
                doc.text('Analysis not performed', margin + 3, yPosition);
                doc.setTextColor(0, 0, 0);
            }
            
            yPosition += 8;
            
            // Teaching tip
            doc.setFillColor(255, 243, 224);
            doc.rect(margin, yPosition, contentWidth, 6, 'F');
            doc.setDrawColor(255, 152, 0);
            doc.setLineWidth(0.5);
            doc.line(margin, yPosition, margin, yPosition + 6);
            doc.setLineWidth(0.2);
            
            yPosition += 2;
            doc.setFontSize(7);
            doc.setFont('helvetica', 'italic');
            doc.text('💡 Teaching Tip: Use this analysis to guide instruction and material selection', margin + 3, yPosition + 2);
            yPosition += 10;
        });
        
        // Summary
        checkPageBreak(25);
        doc.setFillColor(245, 245, 245);
        doc.rect(margin, yPosition, contentWidth, 20, 'F');
        doc.setDrawColor(0, 0, 0);
        doc.rect(margin, yPosition, contentWidth, 20);
        
        yPosition += 5;
        doc.setFontSize(11);
        doc.setFont('helvetica', 'bold');
        doc.text('📋 Analysis Summary', margin + 3, yPosition);
        yPosition += 5;
        
        doc.setFontSize(8);
        doc.setFont('helvetica', 'normal');
        doc.text('This comprehensive analysis provides insights into vocabulary, grammar, structure,', margin + 3, yPosition);
        yPosition += 3;
        doc.text('content, and complexity to support effective language teaching and learning.', margin + 3, yPosition);
        
        // Footer
        doc.setFontSize(7);
        doc.setTextColor(102, 102, 102);
        doc.text('Generated by English Text Analyzer - Educational Analysis Tool', margin, pageHeight - 10);
        
        doc.save('english-text-analysis-report.pdf');
    }
    
    createPrintContainer(results) {
        const container = document.createElement('div');
        container.style.cssText = `
            position: absolute;
            top: -9999px;
            left: -9999px;
            width: 794px;
            background: white;
            font-family: Arial, sans-serif;
            font-size: 12px;
            line-height: 1.2;
            color: black;
            padding: 20px;
        `;
        
        container.innerHTML = this.generatePrintHTML(results);
        return container;
    }
    
    generatePrintHTML(results) {
        const timestamp = new Date().toLocaleString();
        
        return `
            <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 15px;">
                <h1 style="font-size: 24px; margin: 0 0 5px 0;">English Text Analysis Report</h1>
                <p style="font-size: 12px; color: #333; margin: 0;">Educational Analysis for Language Learning</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin: 10px 0; font-size: 10px;">
                <div style="text-align: center; border: 1px solid black; padding: 5px; background: #f8f8f8;">
                    <strong>Date</strong><br>${timestamp.split(',')[0]}
                </div>
                <div style="text-align: center; border: 1px solid black; padding: 5px; background: #f8f8f8;">
                    <strong>Words</strong><br>${results.wordCount}
                </div>
                <div style="text-align: center; border: 1px solid black; padding: 5px; background: #f8f8f8;">
                    <strong>Characters</strong><br>${results.charCount}
                </div>
                <div style="text-align: center; border: 1px solid black; padding: 5px; background: #f8f8f8;">
                    <strong>Level</strong><br>${results.estimatedLevel || 'N/A'}
                </div>
            </div>
            
            <div style="background: #e8f4fd; border: 1px solid #2196f3; padding: 10px; margin: 10px 0; font-size: 11px;">
                <h3 style="margin: 0 0 5px 0; color: #1976d2;">Learning Objectives</h3>
                <ul style="margin: 0; padding-left: 15px; font-size: 9px;">
                    <li>Identify vocabulary at different CEFR levels and understand word difficulty</li>
                    <li>Recognize grammatical structures and sentence patterns in authentic texts</li>
                    <li>Analyze text organization and coherence markers</li>
                    <li>Understand content structure and argument development</li>
                </ul>
            </div>
            
            <div style="border: 1px solid #ccc; padding: 8px; margin: 10px 0; background: #f8f8f8; font-family: monospace; font-size: 9px; max-height: 60px; overflow: hidden;">
                ${this.escapeHtml(results.text.substring(0, 200) + (results.text.length > 200 ? '...' : ''))}
            </div>
            
            ${this.generatePrintSection('🔤 Vocabulary Analysis', results.vocabulary)}
            ${this.generatePrintSection('📝 Grammar Analysis', results.grammar)}
            ${this.generatePrintSection('🏗️ Structure Analysis', results.structure)}
            ${this.generatePrintSection('💡 Content Analysis', results.content)}
            ${this.generatePrintSection('📊 Complexity Analysis', results.complexity)}
            
            <div style="border: 1px solid black; padding: 10px; margin: 10px 0; background: #f5f5f5;">
                <h3 style="margin: 0 0 5px 0;">📋 Analysis Summary</h3>
                <p style="font-size: 10px; margin: 0;">
                    This comprehensive analysis provides insights into vocabulary, grammar, structure, 
                    content, and complexity to support effective language teaching and learning.
                </p>
            </div>
        `;
    }
    
    generatePrintSection(title, data) {
        return `
            <div style="border: 1px solid black; margin: 8px 0; padding: 8px; background: white;">
                <h3 style="margin: 0 0 5px 0; padding-bottom: 2px; border-bottom: 1px solid black; font-size: 14px;">${title}</h3>
                ${data && data.error ? 
                    `<p style="color: #d32f2f; font-size: 10px;">Error: ${data.error}</p>` :
                    `<p style="font-size: 10px;">✓ Analysis completed successfully</p>
                     <p style="font-size: 9px; color: #666; font-style: italic;">
                         Key findings and detailed results available in full interactive report
                     </p>`
                }
                <div style="background: #fff3e0; border-left: 2px solid #ff9800; padding: 4px; margin: 5px 0; font-size: 8px; font-style: italic;">
                    💡 Teaching Tip: Use this analysis to guide instruction and material selection
                </div>
            </div>
        `;
    }
    
    showPDFLoadingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'pdf-loading-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 8px;
            z-index: 10000;
            text-align: center;
        `;
        indicator.innerHTML = `
            <div style="margin-bottom: 10px;">Generating PDF Report...</div>
            <div style="width: 200px; height: 4px; background: #333; border-radius: 2px;">
                <div style="width: 0%; height: 100%; background: #4CAF50; border-radius: 2px; animation: loading 2s infinite;"></div>
            </div>
            <style>
                @keyframes loading {
                    0% { width: 0%; }
                    50% { width: 70%; }
                    100% { width: 100%; }
                }
            </style>
        `;
        document.body.appendChild(indicator);
    }
    
    hidePDFLoadingIndicator() {
        const indicator = document.getElementById('pdf-loading-indicator');
        if (indicator) {
            document.body.removeChild(indicator);
        }
    }
    
    exportJSON(results) {
        if (!results) {
            alert('No analysis results to export.');
            return;
        }
        
        try {
            const jsonContent = JSON.stringify(results, null, 2);
            this.downloadFile(jsonContent, 'text-analysis-data.json', 'application/json');
        } catch (error) {
            console.error('JSON export failed:', error);
            alert('Failed to export JSON data.');
        }
    }
    
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Clean up the URL object
        setTimeout(() => URL.revokeObjectURL(url), 100);
    }
    
    generateEducationalReport(results) {
        const timestamp = new Date().toLocaleString();
        
        // Load the educational template and populate with data
        return this.loadAndPopulateTemplate('educational-detailed', results);
    }
    
    generateTeacherGuide(results) {
        const timestamp = new Date().toLocaleString();
        
        // Load the teacher's guide template and populate with data
        return this.loadAndPopulateTemplate('teachers-guide', results);
    }
    
    generatePrintOptimizedReport(results) {
        const timestamp = new Date().toLocaleString();
        
        // Load the print-optimized template and populate with data
        return this.loadAndPopulateTemplate('educational-print', results);
    }
    
    async loadAndPopulateTemplate(templateName, results) {
        try {
            // In a real implementation, this would load the template file
            // For now, we'll generate a simplified version
            const timestamp = new Date().toLocaleString();
            
            const templateData = {
                ANALYSIS_DATE: timestamp.split(',')[0],
                WORD_COUNT: results.wordCount || 0,
                CHAR_COUNT: results.charCount || 0,
                CEFR_LEVEL: results.estimatedLevel || 'B2',
                COMPLEXITY_SCORE: results.complexityScore || 'Medium',
                TEXT_SAMPLE: this.escapeHtml((results.text || '').substring(0, 200) + '...'),
                SENTENCE_COUNT: results.sentenceCount || Math.ceil((results.wordCount || 0) / 15),
                PARAGRAPH_COUNT: results.paragraphCount || Math.ceil((results.wordCount || 0) / 100),
                BASIC_COUNT: results.vocabulary?.basicCount || 0,
                INTERMEDIATE_COUNT: results.vocabulary?.intermediateCount || 0,
                ADVANCED_COUNT: results.vocabulary?.advancedCount || 0,
                BASIC_PERCENT: results.vocabulary?.basicPercent || 0,
                INTERMEDIATE_PERCENT: results.vocabulary?.intermediatePercent || 0,
                ADVANCED_PERCENT: results.vocabulary?.advancedPercent || 0,
                VOCAB_FOCUS: results.vocabulary?.focus || 'Mixed levels',
                GRAMMAR_FOCUS: results.grammar?.focus || 'Sentence variety',
                ESTIMATED_TIME: this.estimateLessonTime(results),
                COMPLEXITY_LEVEL: this.getComplexityLevel(results),
                COMPLEXITY_POSITION: this.getComplexityPosition(results),
                INSTRUCTIONAL_RECOMMENDATIONS: this.generateInstructionalRecommendations(results),
                FOCUS_RECOMMENDATIONS: this.generateFocusRecommendations(results),
                SCAFFOLDING_RECOMMENDATIONS: this.generateScaffoldingRecommendations(results),
                EXTENSION_RECOMMENDATIONS: this.generateExtensionRecommendations(results),
                VOCAB_PROGRESS: this.calculateVocabProgress(results),
                GRAMMAR_PROGRESS: this.calculateGrammarProgress(results),
                COMPREHENSION_PROGRESS: this.calculateComprehensionProgress(results),
                ANALYSIS_PROGRESS: this.calculateAnalysisProgress(results)
            };
            
            return this.generateEducationalHTML(templateData, results);
            
        } catch (error) {
            console.error('Error loading template:', error);
            return this.generateStandardReport(results);
        }
    }
    
    generateEducationalHTML(templateData, results) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Text Analysis Report</title>
    <style>
        /* Educational Report Styles */
        @page { size: A4; margin: 12mm; }
        body { font-family: Arial, sans-serif; font-size: 10pt; line-height: 1.3; color: #000; }
        .report-header { text-align: center; border-bottom: 2pt solid #000; padding-bottom: 8pt; margin-bottom: 12pt; }
        .report-title { font-size: 16pt; font-weight: bold; color: #1976D2; margin-bottom: 4pt; }
        .metadata-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4pt; margin: 8pt 0; }
        .metadata-item { text-align: center; border: 1pt solid #1976D2; padding: 4pt; background: #E3F2FD; }
        .section { border: 1pt solid #000; margin: 8pt 0; padding: 6pt; background: #FFF; }
        .section-header { font-size: 12pt; font-weight: bold; margin-bottom: 6pt; padding-bottom: 2pt; border-bottom: 1pt solid #000; }
        .vocab-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4pt; margin: 6pt 0; }
        .vocab-box { text-align: center; border: 1pt solid #000; padding: 4pt; }
        .level-a1 { background: #C8E6C9; } .level-b1 { background: #FFF9C4; } .level-c1 { background: #FFCDD2; }
        .teaching-tip { background: #E3F2FD; border: 1pt solid #2196F3; padding: 4pt; margin: 4pt 0; font-size: 8pt; }
        .key-points { background: #FFFDE7; border: 1pt solid #FBC02D; padding: 6pt; margin: 6pt 0; }
        .summary-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6pt; }
        .summary-item { background: #FFF; border: 1pt solid #CCC; padding: 4pt; }
        @media print { body { margin: 0; padding: 8pt; } .section { break-inside: avoid-page; } }
    </style>
</head>
<body>
    <div class="report-header">
        <div class="report-title">📚 Educational Text Analysis Report</div>
        <div style="font-size: 10pt; color: #333;">Comprehensive Language Learning Analysis</div>
    </div>
    
    <div class="metadata-grid">
        <div class="metadata-item">
            <strong>Date:</strong><br>${templateData.ANALYSIS_DATE}
        </div>
        <div class="metadata-item">
            <strong>Words:</strong><br>${templateData.WORD_COUNT}
        </div>
        <div class="metadata-item">
            <strong>Level:</strong><br>${templateData.CEFR_LEVEL}
        </div>
        <div class="metadata-item">
            <strong>Complexity:</strong><br>${templateData.COMPLEXITY_LEVEL}
        </div>
    </div>
    
    <div style="background: #E8F5E8; border: 2pt solid #4CAF50; padding: 8pt; margin: 8pt 0;">
        <div style="font-size: 12pt; font-weight: bold; color: #2E7D32; margin-bottom: 4pt;">🎯 Learning Objectives</div>
        <ul style="margin: 4pt 0; padding-left: 15pt; font-size: 9pt;">
            <li>Identify vocabulary at different CEFR levels and understand word difficulty</li>
            <li>Recognize grammatical structures and sentence patterns in authentic texts</li>
            <li>Analyze text organization and coherence markers</li>
            <li>Understand content structure and argument development</li>
        </ul>
    </div>
    
    <div style="border: 1pt solid #CCC; padding: 6pt; margin: 8pt 0; background: #FAFAFA;">
        <div style="font-weight: bold; margin-bottom: 4pt;">📄 Text Sample</div>
        <div style="font-family: Georgia, serif; font-size: 9pt; border: 1pt solid #CCC; padding: 6pt; background: #FFF;">
            ${templateData.TEXT_SAMPLE}
        </div>
    </div>
    
    <div class="section">
        <div class="section-header">🔤 Vocabulary Analysis</div>
        <div class="vocab-grid">
            <div class="vocab-box level-a1">
                <div style="font-weight: bold; font-size: 8pt;">Basic (A1-A2)</div>
                <div style="font-size: 12pt; font-weight: bold;">${templateData.BASIC_COUNT}</div>
                <div style="font-size: 7pt; color: #666;">${templateData.BASIC_PERCENT}%</div>
            </div>
            <div class="vocab-box level-b1">
                <div style="font-weight: bold; font-size: 8pt;">Intermediate (B1-B2)</div>
                <div style="font-size: 12pt; font-weight: bold;">${templateData.INTERMEDIATE_COUNT}</div>
                <div style="font-size: 7pt; color: #666;">${templateData.INTERMEDIATE_PERCENT}%</div>
            </div>
            <div class="vocab-box level-c1">
                <div style="font-weight: bold; font-size: 8pt;">Advanced (C1-C2)</div>
                <div style="font-size: 12pt; font-weight: bold;">${templateData.ADVANCED_COUNT}</div>
                <div style="font-size: 7pt; color: #666;">${templateData.ADVANCED_PERCENT}%</div>
            </div>
        </div>
        <div class="teaching-tip">
            <strong>🎓 Teaching Tip:</strong> Use advanced vocabulary (C1-C2) as target words for vocabulary building exercises. 
            Create word families and collocations using intermediate vocabulary as bridges.
        </div>
    </div>
    
    <div class="section">
        <div class="section-header">📝 Grammar Patterns</div>
        <p style="font-size: 9pt;">The text demonstrates ${templateData.GRAMMAR_FOCUS} with various sentence structures that provide excellent models for grammar instruction.</p>
        <div class="teaching-tip">
            <strong>📚 Teaching Application:</strong> Use identified complex structures as models for grammar instruction. 
            Highlight sentence variety to teach effective writing techniques.
        </div>
    </div>
    
    <div class="section">
        <div class="section-header">🏗️ Text Structure</div>
        <p style="font-size: 9pt;">The text organization shows clear patterns that can be used as writing models for students.</p>
        <div class="teaching-tip">
            <strong>✍️ Writing Instruction:</strong> Use transition markers as examples for teaching text flow. 
            Show students how organizational patterns support clear communication.
        </div>
    </div>
    
    <div class="section">
        <div class="section-header">💡 Content Analysis</div>
        <p style="font-size: 9pt;">The content structure provides examples of effective argumentation and evidence use.</p>
        <div class="teaching-tip">
            <strong>🧠 Critical Thinking:</strong> Use content outline to teach argument structure and supporting evidence.
        </div>
    </div>
    
    <div class="key-points">
        <div style="font-weight: bold; color: #F57F17; margin-bottom: 3pt; font-size: 10pt;">🔑 Key Learning Points</div>
        <ul style="margin: 0; padding-left: 10pt; font-size: 8pt;">
            <li>Vocabulary spans multiple CEFR levels, providing opportunities for differentiated instruction</li>
            <li>Sentence variety demonstrates different grammatical structures for analysis</li>
            <li>Text organization shows clear patterns that can be used as writing models</li>
            <li>Content structure provides examples of effective argumentation and evidence use</li>
            <li>Complexity level indicates appropriate student proficiency requirements</li>
        </ul>
    </div>
    
    <div style="background: #F5F5F5; border: 2pt solid #000; padding: 8pt; margin: 8pt 0;">
        <div style="font-size: 12pt; font-weight: bold; text-align: center; margin-bottom: 6pt;">📋 Educational Summary & Recommendations</div>
        <div class="summary-grid">
            <div class="summary-item">
                <div style="font-weight: bold; font-size: 9pt; margin-bottom: 2pt;">Instructional Level</div>
                <div style="font-size: 8pt;">${templateData.INSTRUCTIONAL_RECOMMENDATIONS}</div>
            </div>
            <div class="summary-item">
                <div style="font-weight: bold; font-size: 9pt; margin-bottom: 2pt;">Focus Areas</div>
                <div style="font-size: 8pt;">${templateData.FOCUS_RECOMMENDATIONS}</div>
            </div>
            <div class="summary-item">
                <div style="font-weight: bold; font-size: 9pt; margin-bottom: 2pt;">Scaffolding Needs</div>
                <div style="font-size: 8pt;">${templateData.SCAFFOLDING_RECOMMENDATIONS}</div>
            </div>
            <div class="summary-item">
                <div style="font-weight: bold; font-size: 9pt; margin-bottom: 2pt;">Extension Activities</div>
                <div style="font-size: 8pt;">${templateData.EXTENSION_RECOMMENDATIONS}</div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; font-size: 8pt; color: #666; margin-top: 12pt; border-top: 1pt solid #CCC; padding-top: 6pt;">
        Generated by English Text Analyzer - Educational Analysis Tool
    </div>
</body>
</html>`;
    }
    
    // Helper methods for template data generation
    estimateLessonTime(results) {
        const wordCount = results.wordCount || 0;
        if (wordCount < 200) return '30-45 min';
        if (wordCount < 500) return '45-60 min';
        return '60-90 min';
    }
    
    getComplexityLevel(results) {
        const level = results.estimatedLevel || 'B2';
        const complexityMap = {
            'A1': 'Beginner', 'A2': 'Elementary',
            'B1': 'Intermediate', 'B2': 'Upper-Intermediate',
            'C1': 'Advanced', 'C2': 'Proficient'
        };
        return complexityMap[level] || 'Intermediate';
    }
    
    getComplexityPosition(results) {
        const level = results.estimatedLevel || 'B2';
        const positionMap = {
            'A1': 10, 'A2': 30, 'B1': 50, 'B2': 70, 'C1': 85, 'C2': 95
        };
        return positionMap[level] || 70;
    }
    
    generateInstructionalRecommendations(results) {
        const level = results.estimatedLevel || 'B2';
        if (level.startsWith('A')) {
            return 'Suitable for beginner to elementary students with vocabulary support and scaffolding.';
        } else if (level.startsWith('B')) {
            return 'Appropriate for intermediate students with some challenging vocabulary to promote growth.';
        } else {
            return 'Best suited for advanced students who can handle complex vocabulary and structures.';
        }
    }
    
    generateFocusRecommendations(results) {
        return 'Focus on vocabulary building, sentence structure analysis, and content comprehension strategies.';
    }
    
    generateScaffoldingRecommendations(results) {
        return 'Provide vocabulary pre-teaching, graphic organizers, and guided reading support as needed.';
    }
    
    generateExtensionRecommendations(results) {
        return 'Advanced students can analyze rhetorical devices, create response essays, and lead discussions.';
    }
    
    calculateVocabProgress(results) {
        // Simulate progress based on vocabulary complexity
        const level = results.estimatedLevel || 'B2';
        const progressMap = { 'A1': 20, 'A2': 40, 'B1': 60, 'B2': 75, 'C1': 85, 'C2': 95 };
        return progressMap[level] || 75;
    }
    
    calculateGrammarProgress(results) {
        // Simulate progress based on sentence complexity
        return Math.min(85, (results.wordCount || 0) / 10);
    }
    
    calculateComprehensionProgress(results) {
        // Simulate comprehension progress
        return Math.min(90, 60 + (results.wordCount || 0) / 20);
    }
    
    calculateAnalysisProgress(results) {
        // Simulate analysis skill progress
        return Math.min(80, 50 + (results.wordCount || 0) / 15);
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Batch export functionality
    exportBatch(resultsArray, format = 'html') {
        if (!resultsArray || resultsArray.length === 0) {
            alert('No results to export.');
            return;
        }
        
        switch (format) {
            case 'html':
                this.exportBatchHTML(resultsArray);
                break;
            case 'json':
                this.exportBatchJSON(resultsArray);
                break;
            case 'pdf':
                this.exportBatchPDF(resultsArray);
                break;
            default:
                alert('Unsupported export format.');
        }
    }
    
    exportBatchHTML(resultsArray) {
        const combinedHTML = this.generateBatchHTMLReport(resultsArray);
        this.downloadFile(combinedHTML, 'batch-analysis-report.html', 'text/html');
    }
    
    exportBatchJSON(resultsArray) {
        const batchData = {
            exportDate: new Date().toISOString(),
            totalTexts: resultsArray.length,
            results: resultsArray
        };
        
        const jsonContent = JSON.stringify(batchData, null, 2);
        this.downloadFile(jsonContent, 'batch-analysis-data.json', 'application/json');
    }
    
    exportBatchPDF(resultsArray) {
        // For batch PDF, create a zip file with individual PDFs
        // This would require additional libraries like JSZip
        alert('Batch PDF export requires additional libraries. Use HTML or JSON export instead.');
    }
    
    generateBatchHTMLReport(resultsArray) {
        const timestamp = new Date().toLocaleString();
        let sectionsHTML = '';
        
        resultsArray.forEach((results, index) => {
            sectionsHTML += `
                <div class="batch-item">
                    <h2>Analysis ${index + 1}</h2>
                    <div class="text-info">
                        <p>Words: ${results.wordCount}, Characters: ${results.charCount}</p>
                        <p>Analyzed: ${new Date(results.analysisDate).toLocaleString()}</p>
                    </div>
                    ${this.generateHTMLReport(results)}
                </div>
                <hr style="margin: 2rem 0; border: 1px solid #CCCCCC;">
            `;
        });
        
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Batch Text Analysis Report</title>
    <style>
        body { font-family: Georgia, serif; line-height: 1.6; margin: 0; padding: 2rem; }
        .batch-header { text-align: center; margin-bottom: 3rem; }
        .batch-item { margin-bottom: 3rem; }
        .text-info { background: #F5F5F5; padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="batch-header">
        <h1>Batch Text Analysis Report</h1>
        <p>Generated on: ${timestamp}</p>
        <p>Total Texts Analyzed: ${resultsArray.length}</p>
    </div>
    ${sectionsHTML}
</body>
</html>`;
    }
}