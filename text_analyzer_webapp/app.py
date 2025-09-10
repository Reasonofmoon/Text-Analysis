"""Flask web application for Text Analyzer - Extract and Generate Text Information."""

import os
import io
import base64
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import tempfile
import uuid
from datetime import datetime
import json
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'txt', 'md', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_information(text, api_key):
    """Extract various information from text using Gemini API."""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Comprehensive text analysis prompt
        prompt = f"""
        다음 텍스트를 분석하여 다양한 정보를 추출해주세요:

        텍스트: "{text}"

        다음 정보들을 JSON 형식으로 추출해주세요:

        1. 기본 정보:
           - 언어: 텍스트의 주요 언어
           - 길이: 단어 수, 문자 수, 문장 수
           - 유형: 텍스트 유형 (소설, 뉴스, 학술, 블로그 등)

        2. 내용 분석:
           - 주제: 주요 주제 3개
           - 키워드: 핵심 키워드 10개
           - 요약: 3문장 요약
           - 감정: 전체적인 감정 톤 (긍정/부정/중립)

        3. 구조 분석:
           - 문단 수: 총 문단 개수
           - 평균 문장 길이: 문장당 평균 단어 수
           - 복잡도: 텍스트 복잡도 (1-10 점수)

        4. 언어적 특징:
           - 문체: 격식체/비격식체/문학적 등
           - 시제: 주로 사용된 시제
           - 인칭: 1인칭/2인칭/3인칭

        5. 추출 가능한 엔티티:
           - 인물: 언급된 인물명
           - 장소: 언급된 지명
           - 날짜: 언급된 날짜/시간
           - 조직: 언급된 기관/회사명

        6. 생성 제안:
           - 제목 후보: 3개의 제목 제안
           - 태그: 5개의 해시태그
           - 카테고리: 적절한 분류 카테고리

        JSON 형식으로 정확하게 응답해주세요.
        """
        
        response = model.generate_content(prompt)
        
        # Try to parse JSON from response
        response_text = response.text.strip()
        
        # Extract JSON from response if it's wrapped in markdown
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.rfind('```')
            response_text = response_text[json_start:json_end].strip()
        
        try:
            analysis_result = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback: create structured response from text
            analysis_result = parse_fallback_response(response_text, text)
        
        return analysis_result
        
    except Exception as e:
        return {"error": f"분석 중 오류가 발생했습니다: {str(e)}"}


def parse_fallback_response(response_text, original_text):
    """Parse response text when JSON parsing fails."""
    # Basic text statistics
    words = len(original_text.split())
    chars = len(original_text)
    sentences = len(re.findall(r'[.!?]+', original_text))
    paragraphs = len([p for p in original_text.split('\n\n') if p.strip()])
    
    return {
        "기본정보": {
            "언어": "한국어" if any(ord(char) > 127 for char in original_text) else "영어",
            "단어수": words,
            "문자수": chars,
            "문장수": sentences,
            "유형": "일반 텍스트"
        },
        "내용분석": {
            "주제": ["분석 필요", "내용 파악", "텍스트 이해"],
            "키워드": original_text.split()[:10],
            "요약": "텍스트 분석이 필요합니다.",
            "감정": "중립"
        },
        "구조분석": {
            "문단수": paragraphs,
            "평균문장길이": round(words / sentences, 1) if sentences > 0 else 0,
            "복잡도": 5
        },
        "언어적특징": {
            "문체": "일반체",
            "시제": "현재",
            "인칭": "3인칭"
        },
        "엔티티": {
            "인물": [],
            "장소": [],
            "날짜": [],
            "조직": []
        },
        "생성제안": {
            "제목후보": ["텍스트 분석 결과", "내용 요약", "정보 추출"],
            "태그": ["#텍스트", "#분석", "#정보", "#추출", "#내용"],
            "카테고리": "일반"
        },
        "원본응답": response_text
    }


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text and extract information."""
    try:
        # Get form data
        text_input = request.form.get('text', '').strip()
        api_key = request.form.get('api_key', '').strip()
        output_format = request.form.get('format', 'json')
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
        
        # Perform analysis
        analysis_result = extract_text_information(text_input, api_key)
        
        if "error" in analysis_result:
            return jsonify({
                'success': False,
                'error': analysis_result["error"]
            })
        
        # Generate output based on format
        if output_format == 'html':
            html_content = generate_html_report(analysis_result, title, text_input)
            
            return jsonify({
                'success': True,
                'format': 'html',
                'content': html_content,
                'title': title
            })
        
        elif output_format == 'json':
            # Add metadata
            analysis_result['메타데이터'] = {
                '분석일시': datetime.now().isoformat(),
                '제목': title,
                '원본텍스트길이': len(text_input)
            }
            
            json_content = json.dumps(analysis_result, ensure_ascii=False, indent=2)
            
            return jsonify({
                'success': True,
                'format': 'json',
                'content': json_content,
                'title': title
            })
        
        elif output_format == 'summary':
            summary = generate_summary_report(analysis_result, title)
            
            return jsonify({
                'success': True,
                'format': 'summary',
                'content': summary,
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


def generate_html_report(analysis_result, title, original_text):
    """Generate HTML report from analysis results."""
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #000;
                background-color: #fff;
                padding: 20px;
            }}
            
            .container {{
                max-width: 900px;
                margin: 0 auto;
                border: 4px solid #000;
                background: #fff;
                position: relative;
            }}
            
            .container::before {{
                content: '';
                position: absolute;
                top: -8px;
                left: -8px;
                right: -8px;
                bottom: -8px;
                border: 2px solid #000;
                z-index: -1;
            }}
            
            .header {{
                background: #000;
                color: #fff;
                padding: 30px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2rem;
                margin-bottom: 10px;
            }}
            
            .content {{
                padding: 30px;
            }}
            
            .section {{
                margin-bottom: 30px;
                border: 2px solid #000;
                padding: 20px;
            }}
            
            .section h2 {{
                background: #000;
                color: #fff;
                margin: -20px -20px 20px -20px;
                padding: 15px 20px;
                font-size: 1.3rem;
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}
            
            .info-item {{
                border: 1px solid #000;
                padding: 10px;
                background: #f9f9f9;
            }}
            
            .info-label {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
            
            .tag {{
                display: inline-block;
                background: #000;
                color: #fff;
                padding: 4px 8px;
                margin: 2px;
                font-size: 0.9rem;
            }}
            
            .list-item {{
                padding: 8px;
                border-bottom: 1px solid #ccc;
            }}
            
            .list-item:last-child {{
                border-bottom: none;
            }}
            
            .original-text {{
                background: #f5f5f5;
                border: 2px solid #000;
                padding: 20px;
                margin-top: 20px;
                max-height: 300px;
                overflow-y: auto;
                white-space: pre-wrap;
                font-family: monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 텍스트 분석 보고서</h1>
                <p>{title}</p>
                <p>{datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</p>
            </div>
            
            <div class="content">
    """
    
    # Basic Information Section
    if '기본정보' in analysis_result:
        basic_info = analysis_result['기본정보']
        html_template += f"""
                <div class="section">
                    <h2>📋 기본 정보</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">언어</div>
                            <div>{basic_info.get('언어', 'N/A')}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">단어 수</div>
                            <div>{basic_info.get('단어수', 0):,}개</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">문자 수</div>
                            <div>{basic_info.get('문자수', 0):,}자</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">문장 수</div>
                            <div>{basic_info.get('문장수', 0)}개</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">텍스트 유형</div>
                            <div>{basic_info.get('유형', 'N/A')}</div>
                        </div>
                    </div>
                </div>
        """
    
    # Content Analysis Section
    if '내용분석' in analysis_result:
        content_info = analysis_result['내용분석']
        html_template += f"""
                <div class="section">
                    <h2>💡 내용 분석</h2>
                    <div class="info-item" style="margin-bottom: 15px;">
                        <div class="info-label">주요 주제</div>
                        <div>
        """
        
        topics = content_info.get('주제', [])
        if isinstance(topics, list):
            for topic in topics:
                html_template += f'<span class="tag">{topic}</span>'
        else:
            html_template += f'<span class="tag">{topics}</span>'
        
        html_template += f"""
                        </div>
                    </div>
                    <div class="info-item" style="margin-bottom: 15px;">
                        <div class="info-label">핵심 키워드</div>
                        <div>
        """
        
        keywords = content_info.get('키워드', [])
        if isinstance(keywords, list):
            for keyword in keywords[:10]:
                html_template += f'<span class="tag">{keyword}</span>'
        
        html_template += f"""
                        </div>
                    </div>
                    <div class="info-item" style="margin-bottom: 15px;">
                        <div class="info-label">요약</div>
                        <div>{content_info.get('요약', 'N/A')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">감정 톤</div>
                        <div><span class="tag">{content_info.get('감정', 'N/A')}</span></div>
                    </div>
                </div>
        """
    
    # Structure Analysis Section
    if '구조분석' in analysis_result:
        structure_info = analysis_result['구조분석']
        html_template += f"""
                <div class="section">
                    <h2>🏗️ 구조 분석</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">문단 수</div>
                            <div>{structure_info.get('문단수', 0)}개</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">평균 문장 길이</div>
                            <div>{structure_info.get('평균문장길이', 0)} 단어</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">복잡도</div>
                            <div>{structure_info.get('복잡도', 0)}/10</div>
                        </div>
                    </div>
                </div>
        """
    
    # Entities Section
    if '엔티티' in analysis_result:
        entities = analysis_result['엔티티']
        html_template += f"""
                <div class="section">
                    <h2>🏷️ 추출된 엔티티</h2>
                    <div class="info-grid">
        """
        
        for entity_type, entity_list in entities.items():
            html_template += f"""
                        <div class="info-item">
                            <div class="info-label">{entity_type}</div>
                            <div>
            """
            if isinstance(entity_list, list) and entity_list:
                for entity in entity_list:
                    html_template += f'<span class="tag">{entity}</span>'
            else:
                html_template += '<span style="color: #666;">없음</span>'
            
            html_template += '</div></div>'
        
        html_template += '</div></div>'
    
    # Generation Suggestions Section
    if '생성제안' in analysis_result:
        suggestions = analysis_result['생성제안']
        html_template += f"""
                <div class="section">
                    <h2>✨ 생성 제안</h2>
                    <div class="info-item" style="margin-bottom: 15px;">
                        <div class="info-label">제목 후보</div>
                        <div>
        """
        
        titles = suggestions.get('제목후보', [])
        if isinstance(titles, list):
            for i, title_candidate in enumerate(titles, 1):
                html_template += f'<div class="list-item">{i}. {title_candidate}</div>'
        
        html_template += f"""
                        </div>
                    </div>
                    <div class="info-item" style="margin-bottom: 15px;">
                        <div class="info-label">추천 태그</div>
                        <div>
        """
        
        tags = suggestions.get('태그', [])
        if isinstance(tags, list):
            for tag in tags:
                html_template += f'<span class="tag">{tag}</span>'
        
        html_template += f"""
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">카테고리</div>
                        <div><span class="tag">{suggestions.get('카테고리', 'N/A')}</span></div>
                    </div>
                </div>
        """
    
    # Original Text Section
    html_template += f"""
                <div class="section">
                    <h2>📄 원본 텍스트</h2>
                    <div class="original-text">{original_text}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template


def generate_summary_report(analysis_result, title):
    """Generate a summary report."""
    summary = f"# {title}\n\n"
    summary += f"분석 일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n\n"
    
    if '기본정보' in analysis_result:
        basic = analysis_result['기본정보']
        summary += f"## 📋 기본 정보\n"
        summary += f"- 언어: {basic.get('언어', 'N/A')}\n"
        summary += f"- 길이: {basic.get('단어수', 0):,}단어, {basic.get('문자수', 0):,}자\n"
        summary += f"- 구조: {basic.get('문장수', 0)}문장\n\n"
    
    if '내용분석' in analysis_result:
        content = analysis_result['내용분석']
        summary += f"## 💡 핵심 내용\n"
        summary += f"- 주제: {', '.join(content.get('주제', []))}\n"
        summary += f"- 감정: {content.get('감정', 'N/A')}\n"
        summary += f"- 요약: {content.get('요약', 'N/A')}\n\n"
    
    if '생성제안' in analysis_result:
        suggestions = analysis_result['생성제안']
        summary += f"## ✨ 제안사항\n"
        summary += f"- 카테고리: {suggestions.get('카테고리', 'N/A')}\n"
        if suggestions.get('태그'):
            summary += f"- 태그: {', '.join(suggestions.get('태그', []))}\n"
    
    return summary


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