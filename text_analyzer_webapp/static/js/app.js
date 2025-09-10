// Text Analyzer Web App JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const form = document.getElementById('analysisForm');
    const textInput = document.getElementById('textInput');
    const fileInput = document.getElementById('fileInput');
    const fileUploadArea = document.getElementById('fileUploadArea');
    const selectedFile = document.getElementById('selectedFile');
    const charCount = document.getElementById('charCount');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');

    // Character counter
    textInput.addEventListener('input', updateCharCount);
    
    function updateCharCount() {
        const count = textInput.value.length;
        charCount.textContent = count.toLocaleString();
        
        if (count > 50000) {
            charCount.style.color = '#e53e3e';
            textInput.style.borderColor = '#e53e3e';
        } else {
            charCount.style.color = '#666';
            textInput.style.borderColor = '#000';
        }
    }

    // File upload handling
    fileUploadArea.addEventListener('click', () => fileInput.click());
    fileUploadArea.addEventListener('dragover', handleDragOver);
    fileUploadArea.addEventListener('dragleave', handleDragLeave);
    fileUploadArea.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);

    function handleDragOver(e) {
        e.preventDefault();
        fileUploadArea.classList.add('dragover');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
    }

    function handleDrop(e) {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    }

    function handleFile(file) {
        // Validate file type
        const allowedTypes = ['txt', 'md', 'doc', 'docx'];
        const fileExtension = file.name.toLowerCase().split('.').pop();
        
        if (!allowedTypes.includes(fileExtension)) {
            showError('지원하는 파일 형식: .txt, .md, .doc, .docx');
            return;
        }

        // Validate file size (16MB)
        if (file.size > 16 * 1024 * 1024) {
            showError('파일 크기는 16MB를 초과할 수 없습니다.');
            return;
        }

        // Show selected file
        selectedFile.style.display = 'flex';
        selectedFile.querySelector('.file-name').textContent = file.name;
        
        // Read file content
        const reader = new FileReader();
        reader.onload = function(e) {
            const content = e.target.result;
            if (content.length > 50000) {
                showError('파일 내용이 50,000자를 초과합니다.');
                removeFile();
                return;
            }
            
            textInput.value = content;
            updateCharCount();
        };
        reader.onerror = function() {
            showError('파일을 읽는 중 오류가 발생했습니다.');
            removeFile();
        };
        reader.readAsText(file, 'UTF-8');
    }

    // Remove file function (global for onclick)
    window.removeFile = function() {
        fileInput.value = '';
        selectedFile.style.display = 'none';
        textInput.value = '';
        updateCharCount();
    };

    // Form submission
    form.addEventListener('submit', handleSubmit);

    async function handleSubmit(e) {
        e.preventDefault();
        
        // Validate form
        const apiKey = document.getElementById('apiKey').value.trim();
        const text = textInput.value.trim();
        
        if (!apiKey) {
            showError('Gemini API 키를 입력해주세요.');
            return;
        }
        
        if (!text) {
            showError('분석할 텍스트를 입력하거나 파일을 업로드해주세요.');
            return;
        }
        
        if (text.length > 50000) {
            showError('텍스트는 50,000자를 초과할 수 없습니다.');
            return;
        }

        // Show loading state
        setLoadingState(true);
        hideError();
        hideResults();

        try {
            // Prepare form data
            const formData = new FormData(form);
            
            // Send request
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                showResults(result);
            } else {
                showError(result.error || '분석 중 오류가 발생했습니다.');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            showError('서버와의 통신 중 오류가 발생했습니다. 네트워크 연결을 확인해주세요.');
        } finally {
            setLoadingState(false);
        }
    }

    function setLoadingState(loading) {
        submitBtn.disabled = loading;
        
        if (loading) {
            btnText.style.opacity = '0';
            btnLoader.style.display = 'block';
        } else {
            btnText.style.opacity = '1';
            btnLoader.style.display = 'none';
        }
    }

    function showResults(result) {
        resultsContent.innerHTML = '';
        
        if (result.format === 'html') {
            // Create iframe for HTML content
            const iframe = document.createElement('iframe');
            iframe.style.width = '100%';
            iframe.style.minHeight = '700px';
            iframe.style.border = '3px solid #000';
            iframe.style.background = '#fff';
            
            // Set iframe content
            iframe.onload = function() {
                this.contentDocument.open();
                this.contentDocument.write(result.content);
                this.contentDocument.close();
            };
            
            resultsContent.appendChild(iframe);
            
        } else if (result.format === 'json') {
            // Show JSON content
            const jsonContainer = document.createElement('div');
            jsonContainer.innerHTML = `
                <h3 style="margin-bottom: 25px; font-size: 1.5rem; color: #000;">📊 추출된 텍스트 정보</h3>
                <div class="json-output">${result.content}</div>
                <div style="margin-top: 25px; text-align: center;">
                    <button class="download-btn" onclick="downloadJSON('${btoa(result.content)}', '${result.title}')">
                        💾 JSON 다운로드
                    </button>
                </div>
            `;
            resultsContent.appendChild(jsonContainer);
            
        } else if (result.format === 'summary') {
            // Show summary content
            const summaryContainer = document.createElement('div');
            summaryContainer.innerHTML = `
                <h3 style="margin-bottom: 25px; font-size: 1.5rem; color: #000;">📋 분석 요약</h3>
                <div class="summary-output">${result.content}</div>
                <div style="margin-top: 25px; text-align: center;">
                    <button class="download-btn" onclick="downloadText('${btoa(result.content)}', '${result.title}')">
                        📄 요약 다운로드
                    </button>
                </div>
            `;
            resultsContent.appendChild(summaryContainer);
        }
        
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function hideResults() {
        resultsSection.style.display = 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            hideError();
        }, 10000);
    }

    // Hide error function (global for onclick)
    window.hideError = function() {
        errorSection.style.display = 'none';
    };

    // Reset form function (global for onclick)
    window.resetForm = function() {
        form.reset();
        removeFile();
        updateCharCount();
        hideResults();
        hideError();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Download functions (global for onclick)
    window.downloadJSON = function(base64Content, title) {
        try {
            const jsonContent = atob(base64Content);
            const blob = new Blob([jsonContent], { type: 'application/json' });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${title || 'text-analysis'}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('JSON download error:', error);
            showError('JSON 다운로드 중 오류가 발생했습니다.');
        }
    };

    window.downloadText = function(base64Content, title) {
        try {
            const textContent = atob(base64Content);
            const blob = new Blob([textContent], { type: 'text/plain' });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${title || 'text-summary'}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Text download error:', error);
            showError('텍스트 다운로드 중 오류가 발생했습니다.');
        }
    };

    // Initialize character count
    updateCharCount();
    
    // API Key persistence (optional - store in sessionStorage)
    const apiKeyInput = document.getElementById('apiKey');
    const savedApiKey = sessionStorage.getItem('gemini_api_key');
    if (savedApiKey) {
        apiKeyInput.value = savedApiKey;
    }
    
    apiKeyInput.addEventListener('input', function() {
        if (this.value.trim()) {
            sessionStorage.setItem('gemini_api_key', this.value.trim());
        } else {
            sessionStorage.removeItem('gemini_api_key');
        }
    });

    // Smooth scrolling for better UX
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});