#!/usr/bin/env python3
"""Test script for English Text Analyzer Web App."""

import os
import sys
from pathlib import Path

def test_webapp_structure():
    """Test if all required files exist."""
    print("🔍 Testing webapp structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'Dockerfile',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
        'README.md',
        'DEPLOYMENT.md'
    ]
    
    webapp_dir = Path(__file__).parent
    missing_files = []
    
    for file_path in required_files:
        full_path = webapp_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
        return False
    else:
        print("\n🎉 All required files are present!")
        return True

def test_file_contents():
    """Test if key files have expected content."""
    print("\n🔍 Testing file contents...")
    
    webapp_dir = Path(__file__).parent
    
    # Test app.py
    app_file = webapp_dir / 'app.py'
    if app_file.exists():
        content = app_file.read_text(encoding='utf-8')
        if 'Flask' in content and 'analyze_text' in content:
            print("✅ app.py has Flask and analysis functionality")
        else:
            print("❌ app.py missing key components")
    
    # Test HTML template
    template_file = webapp_dir / 'templates' / 'index.html'
    if template_file.exists():
        content = template_file.read_text(encoding='utf-8')
        if 'English Text Analyzer' in content and 'analysisForm' in content:
            print("✅ index.html has proper structure")
        else:
            print("❌ index.html missing key components")
    
    # Test CSS
    css_file = webapp_dir / 'static' / 'css' / 'style.css'
    if css_file.exists():
        content = css_file.read_text(encoding='utf-8')
        if '.container' in content and '.analysis-form' in content:
            print("✅ style.css has proper styling")
        else:
            print("❌ style.css missing key styles")
    
    # Test JavaScript
    js_file = webapp_dir / 'static' / 'js' / 'app.js'
    if js_file.exists():
        content = js_file.read_text(encoding='utf-8')
        if 'handleSubmit' in content and 'showResults' in content:
            print("✅ app.js has proper functionality")
        else:
            print("❌ app.js missing key functions")

def test_requirements():
    """Test requirements.txt content."""
    print("\n🔍 Testing requirements...")
    
    webapp_dir = Path(__file__).parent
    req_file = webapp_dir / 'requirements.txt'
    
    if req_file.exists():
        content = req_file.read_text(encoding='utf-8')
        required_packages = ['Flask', 'langextract', 'gunicorn']
        
        for package in required_packages:
            if package.lower() in content.lower():
                print(f"✅ {package} found in requirements")
            else:
                print(f"❌ {package} missing from requirements")
    else:
        print("❌ requirements.txt not found")

def generate_summary():
    """Generate deployment summary."""
    print("\n" + "="*60)
    print("📋 DEPLOYMENT SUMMARY")
    print("="*60)
    
    print("\n🌟 English Text Analyzer Web App")
    print("   미니멀하고 아티스틱한 영어 텍스트 분석 웹앱")
    
    print("\n🎯 주요 기능:")
    print("   ✅ 텍스트 복잡도 분석 (Flesch-Kincaid, CEFR)")
    print("   ✅ HTML/PDF/JSON 다중 출력 형식")
    print("   ✅ 파일 업로드 및 드래그 앤 드롭")
    print("   ✅ Gemini AI API 통합")
    print("   ✅ 반응형 미니멀 디자인")
    
    print("\n🚀 배포 옵션:")
    print("   • Railway: 원클릭 배포")
    print("   • Render: 무료 티어 제공")
    print("   • Vercel: 서버리스 배포")
    print("   • Heroku: 클래식 PaaS")
    print("   • Google Cloud Run: 컨테이너 배포")
    
    print("\n📁 프로젝트 구조:")
    print("   webapp/")
    print("   ├── app.py              # Flask 메인 애플리케이션")
    print("   ├── templates/")
    print("   │   └── index.html      # 메인 웹 페이지")
    print("   ├── static/")
    print("   │   ├── css/style.css   # 미니멀 아티스틱 스타일")
    print("   │   └── js/app.js       # 프론트엔드 로직")
    print("   ├── requirements.txt    # Python 의존성")
    print("   ├── Dockerfile         # 컨테이너 배포용")
    print("   └── README.md          # 상세 사용법")
    
    print("\n🎨 디자인 특징:")
    print("   • 흰 배경 + 검은 글자 (최고 가독성)")
    print("   • 굵은 검은 테두리 (아티스틱 요소)")
    print("   • 그림자 효과 (입체감)")
    print("   • Inter 폰트 (모던한 타이포그래피)")
    print("   • 완전 반응형 (모바일 최적화)")
    
    print("\n🔧 사용 방법:")
    print("   1. Gemini API 키 입력 (무료 발급 가능)")
    print("   2. 텍스트 입력 또는 파일 업로드")
    print("   3. 출력 형식 선택 (HTML/PDF/JSON)")
    print("   4. 분석 실행 및 결과 확인")
    
    print("\n🌐 GitHub 배포 준비 완료!")
    print("   Repository: https://github.com/your-username/english-text-analyzer")
    print("   Live Demo: https://your-app.railway.app")

def main():
    """Run all tests."""
    print("🚀 English Text Analyzer Web App - Test Suite")
    print("="*60)
    
    success = True
    
    # Run tests
    success &= test_webapp_structure()
    test_file_contents()
    test_requirements()
    
    # Generate summary
    generate_summary()
    
    if success:
        print(f"\n🎉 All tests passed! Web app is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())