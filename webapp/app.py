"""Flask web application for English Text Analyzer."""

import os
import io
import base64
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import tempfile
import uuid
from datetime import datetime

# Import our analyzer components
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from english_text_analyzer.core.analyzer import EnglishTextAnalyzer
from english_text_analyzer.config.settings import AnalysisConfig
from english_text_analyzer.reports.html_generator import HTMLReportGenerator
from english_text_analyzer.reports.pdf_generator import PDFReportGenerator
from english_text_analyzer.reports.json_exporter import JSONExporter

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text and return results."""
    try:
        # Get form data
        text_input = request.form.get('text', '').strip()
        api_key = request.form.get('api_key', '').strip()
        output_format = request.form.get('format', 'html')
        title = request.form.get('title', '').strip()
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                try:
                    file_content = file.read().decode('utf-8')
                    if file_content.strip():
                        text_input = file_content
                        if not title:
                            title = secure_filename(file.filename).rsplit('.', 1)[0]
                except UnicodeDecodeError:
                    return jsonify({
                        'success': False,
                        'error': '파일을 읽을 수 없습니다. UTF-8 인코딩된 텍스트 파일을 업로드해주세요.'
                    })
        
        # Validation
        if not text_input:
            return jsonify({
                'success': False,
                'error': '분석할 텍스트를 입력하거나 파일을 업로드해주세요.'
            })
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Gemini API 키를 입력해주세요.'
            })
        
        if len(text_input) > 50000:  # 50KB limit
            return jsonify({
                'success': False,
                'error': '텍스트가 너무 깁니다. 50,000자 이하로 입력해주세요.'
            })
        
        # Set default title
        if not title:
            title = f"텍스트 분석 결과 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Configure analyzer
        config = AnalysisConfig()
        config.api_key = api_key
        config.enabled_analyzers = ['complexity']  # Focus on complexity for web app
        
        # Perform analysis
        analyzer = EnglishTextAnalyzer(config=config)
        results = analyzer.analyze_text(text_input)
        results.title = title
        
        # Generate output based on format
        if output_format == 'html':
            generator = HTMLReportGenerator()
            html_content = generator.generate_report(results, title)
            
            return jsonify({
                'success': True,
                'format': 'html',
                'content': html_content,
                'title': title
            })
        
        elif output_format == 'pdf':
            try:
                generator = PDFReportGenerator()
                pdf_bytes = generator.generate_report(results, title)
                
                # Encode PDF as base64 for JSON response
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
                
                return jsonify({
                    'success': True,
                    'format': 'pdf',
                    'content': pdf_base64,
                    'title': title,
                    'filename': f"{secure_filename(title)}.pdf"
                })
            except ImportError:
                return jsonify({
                    'success': False,
                    'error': 'PDF 생성 기능을 사용할 수 없습니다. reportlab 라이브러리가 필요합니다.'
                })
        
        elif output_format == 'json':
            exporter = JSONExporter()
            json_content = exporter.export_educational_data(results)
            
            return jsonify({
                'success': True,
                'format': 'json',
                'content': json_content,
                'title': title
            })
        
        else:
            return jsonify({
                'success': False,
                'error': '지원하지 않는 출력 형식입니다.'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'분석 중 오류가 발생했습니다: {str(e)}'
        })


@app.route('/download/<format>/<filename>')
def download_file(format, filename):
    """Download generated file."""
    try:
        # This would be implemented with proper file storage in production
        # For now, return a simple response
        return jsonify({
            'success': False,
            'error': '다운로드 기능은 현재 구현 중입니다.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'다운로드 중 오류가 발생했습니다: {str(e)}'
        })


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': '파일이 너무 큽니다. 16MB 이하의 파일을 업로드해주세요.'
    }), 413


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error."""
    return jsonify({
        'success': False,
        'error': '서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)