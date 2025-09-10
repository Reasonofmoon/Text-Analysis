# 🌟 English Text Analyzer Web App

**미니멀하고 아티스틱한 영어 텍스트 분석 웹 애플리케이션**

사용자가 자신의 Gemini API 키를 입력하여 영어 텍스트의 복잡도와 가독성을 분석하고, HTML/PDF 보고서로 결과를 받을 수 있는 웹앱입니다.

## 🎯 주요 특징

### 📊 **강력한 분석 기능**
- **복잡도 분석**: Flesch-Kincaid Grade Level, Reading Ease 점수
- **CEFR 레벨 추정**: A1~C2 자동 분류
- **어휘 다양성**: Type-Token Ratio, 평균 단어 길이
- **교육적 인사이트**: 수준별 학습 권장사항

### 🎨 **미니멀 아티스틱 디자인**
- **최고 가독성**: 흰 배경 + 검은 글자
- **아티스틱 요소**: 굵은 검은 테두리, 그림자 효과
- **모던 타이포그래피**: Inter 폰트 사용
- **완전 반응형**: 모바일부터 데스크톱까지 최적화

### 🚀 **사용자 친화적 기능**
- **다양한 입력 방식**: 직접 입력, 파일 업로드, 드래그 앤 드롭
- **다중 출력 형식**: HTML 보고서, PDF 다운로드, JSON 데이터
- **실시간 피드백**: 글자 수 카운터, 진행 상태 표시
- **API 키 보안**: 클라이언트 사이드에서만 처리

## 🖼️ 스크린샷

### 메인 인터페이스
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ██████╗ English Text Analyzer ██████╗                 │
│  ██╔══██╗                      ██╔══██╗                │
│  ██████╔╝ 영어 텍스트 분석기    ██████╔╝                │
│  ██╔══██╗                      ██╔══██╗                │
│  ██████╔╝                      ██████╔╝                │
│  ╚═════╝                       ╚═════╝                 │
│                                                         │
│  영어 텍스트의 복잡도와 가독성을 분석하여               │
│  교육적 인사이트를 제공합니다                           │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Gemini API Key *                                        │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ••••••••••••••••••••••••••••••••••••••••••••••••••• │ │
│ └─────────────────────────────────────────────────────┘ │
│ API 키는 Google AI Studio에서 무료로 발급받을 수 있습니다 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 분석할 텍스트 *                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ The quick brown fox jumps over the lazy dog.        │ │
│ │ This is a sample text for complexity analysis...    │ │
│ │                                                     │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
│                                          127 / 50,000 자 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 또는 파일 업로드                                        │
│ ┌─────────────────────────────────────────────────────┐ │
│ │                     📄                              │ │
│ │          클릭하여 파일 선택 또는 드래그 앤 드롭        │ │
│ │              .txt 파일만 지원 (최대 16MB)             │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  ████ 텍스트 분석하기 ████                │
└─────────────────────────────────────────────────────────┘
```

## 🚀 빠른 시작

### 1. **온라인 사용 (권장)**
🌐 **Live Demo**: [https://english-text-analyzer.railway.app](https://english-text-analyzer.railway.app)

1. 웹사이트 접속
2. [Google AI Studio](https://makersuite.google.com/app/apikey)에서 무료 API 키 발급
3. API 키 입력 후 텍스트 분석 시작

### 2. **로컬 실행**
```bash
# 저장소 클론
git clone https://github.com/your-username/english-text-analyzer.git
cd english-text-analyzer/webapp

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 앱 실행
python app.py

# 브라우저에서 접속
# http://localhost:5000
```

### 3. **Docker 실행**
```bash
cd webapp
docker build -t english-text-analyzer .
docker run -p 5000:5000 english-text-analyzer
```

## 📋 사용 방법

### Step 1: API 키 설정
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. "Create API Key" 클릭하여 무료 키 발급
3. 웹앱의 API 키 입력란에 붙여넣기

### Step 2: 텍스트 입력
**방법 1: 직접 입력**
- 텍스트 영역에 분석할 영어 텍스트 입력
- 최대 50,000자까지 지원

**방법 2: 파일 업로드**
- .txt 파일을 드래그 앤 드롭 또는 클릭하여 선택
- 최대 16MB 파일 크기 지원

### Step 3: 옵션 설정
- **보고서 제목**: 분석 결과의 제목 설정 (선택사항)
- **출력 형식**: HTML 보고서, PDF 다운로드, JSON 데이터 중 선택

### Step 4: 분석 실행
- "텍스트 분석하기" 버튼 클릭
- 실시간 진행 상태 확인
- 결과 확인 및 다운로드

## 📊 분석 결과 예시

### HTML 보고서
```html
📊 분석 개요
├── CEFR 레벨: B2 (중상급)
├── 복잡도 점수: 7.5/10
├── 단어 수: 245개
└── 문장 수: 12개

📚 어휘 분석
├── 학술 어휘: comprehensive, analysis, methodology
├── 어휘 다양성: 0.75 (높음)
└── 난이도 분포: A1(30%), B1(40%), B2(30%)

📈 복잡도 분석
├── Flesch-Kincaid Grade: 8.5
├── Reading Ease: 65.2 (표준)
└── 평균 문장 길이: 15.2 단어

💡 교육적 권장사항
├── 중급-고급 학습자에게 적합
├── 복잡한 문법 구조 학습에 활용
└── 학술적 읽기 준비에 도움
```

## 🎨 디자인 철학

### **미니멀리즘**
- 불필요한 요소 제거
- 핵심 기능에 집중
- 깔끔한 레이아웃

### **아티스틱 요소**
- 굵은 검은 테두리 (4px)
- 이중 테두리 효과
- 그림자와 입체감

### **최고 가독성**
- 흰 배경 + 검은 글자
- Inter 폰트 (웹 최적화)
- 충분한 여백과 간격

### **반응형 디자인**
```css
/* 모바일 우선 설계 */
@media (max-width: 768px) {
  .container { padding: 20px 16px; }
  .title { font-size: 2.2rem; }
}

@media (max-width: 480px) {
  .title { font-size: 1.8rem; }
  .analysis-form { padding: 20px; }
}
```

## 🔧 기술 스택

### **Backend**
- **Flask 3.0**: 경량 웹 프레임워크
- **Python 3.11**: 최신 Python 버전
- **Gunicorn**: 프로덕션 WSGI 서버

### **Frontend**
- **Vanilla JavaScript**: 프레임워크 없는 순수 JS
- **HTML5**: 시맨틱 마크업
- **CSS3**: 모던 스타일링 (Grid, Flexbox)

### **AI & Analysis**
- **Google Gemini API**: 고급 텍스트 분석
- **English Text Analyzer**: 자체 개발 분석 엔진
- **langextract**: 언어학적 특징 추출

### **배포 & DevOps**
- **Docker**: 컨테이너화
- **GitHub Actions**: CI/CD 파이프라인
- **Railway/Render**: 클라우드 배포

## 🌐 배포 옵션

### **원클릭 배포**
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### **지원 플랫폼**
- ✅ **Railway**: 추천 (무료 티어, 자동 HTTPS)
- ✅ **Render**: 무료 티어 제공
- ✅ **Vercel**: 서버리스 배포
- ✅ **Heroku**: 클래식 PaaS
- ✅ **Google Cloud Run**: 컨테이너 배포
- ✅ **AWS ECS**: 엔터프라이즈급

## 🔒 보안 & 프라이버시

### **API 키 보안**
- 클라이언트 사이드에서만 처리
- 서버에 저장하지 않음
- HTTPS를 통한 안전한 전송

### **파일 업로드 보안**
- .txt 파일만 허용
- 16MB 크기 제한
- 임시 파일 자동 정리

### **데이터 프라이버시**
- 사용자 텍스트 저장하지 않음
- 분석 후 즉시 삭제
- 개인정보 수집 없음

## 📈 성능 최적화

### **프론트엔드**
- CSS/JS 최소화
- 이미지 최적화
- 브라우저 캐싱 활용

### **백엔드**
- Gunicorn 멀티워커
- 요청 타임아웃 설정
- 메모리 사용량 최적화

### **배포**
- CDN 활용 (정적 파일)
- 자동 스케일링
- 헬스체크 모니터링

## 🤝 기여하기

### **개발 환경 설정**
```bash
# 개발 의존성 설치
pip install -r requirements-dev.txt

# 코드 포맷팅
black webapp/
flake8 webapp/

# 테스트 실행
python webapp/test_webapp.py
```

### **기여 가이드라인**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 지원 & 문의

- **🐛 버그 리포트**: [GitHub Issues](https://github.com/your-username/english-text-analyzer/issues)
- **💡 기능 요청**: [GitHub Discussions](https://github.com/your-username/english-text-analyzer/discussions)
- **📚 문서**: [Wiki](https://github.com/your-username/english-text-analyzer/wiki)
- **💬 커뮤니티**: [Discord](https://discord.gg/your-server)

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

<div align="center">

**🎓 Made with ❤️ for English Language Education**

[Live Demo](https://english-text-analyzer.railway.app) • [Documentation](https://github.com/your-username/english-text-analyzer/wiki) • [Report Bug](https://github.com/your-username/english-text-analyzer/issues)

</div>