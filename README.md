# 🌟 English Text Analyzer

**AI-Powered English Text Analysis Tool for Educational Purposes**

🌐 **Live Demo**: [https://reasonofmoon.github.io/Text-Analysis/](https://reasonofmoon.github.io/Text-Analysis/)

영어 텍스트의 복잡도와 가독성을 분석하여 교육적 인사이트를 제공하는 종합 분석 도구입니다.

## 🚀 빠른 시작

1. **웹 앱 방문**: [https://reasonofmoon.github.io/Text-Analysis/](https://reasonofmoon.github.io/Text-Analysis/)
2. **API 키 발급**: [Google AI Studio](https://makersuite.google.com/app/apikey)에서 무료 Gemini API 키 발급
3. **텍스트 분석**: API 키 입력 후 영어 텍스트를 붙여넣고 "Analyze Text" 클릭
4. **결과 내보내기**: HTML, PDF, JSON 형식으로 보고서 다운로드

## 🎯 주요 기능

### 📊 **포괄적 텍스트 분석**
- **복잡도 분석**: Flesch-Kincaid Grade Level, Reading Ease 점수
- **CEFR 레벨 추정**: A1~C2 자동 분류 및 수준별 권장사항
- **어휘 분석**: 학술 어휘, 연어 표현, 어휘 다양성 측정
- **문법 분석**: 문장 유형, 시제 패턴, 구문 복잡도
- **구조 분석**: 주제문, 전환 표현, 텍스트 응집성
- **내용 분석**: 주요 아이디어, 논증 구조, 증거 유형

### 🌐 **웹 애플리케이션**
- **미니멀 디자인**: 흰 배경 + 검은 글자로 최고의 가독성
- **아티스틱 UI**: 굵은 검은 테두리와 그림자 효과
- **다양한 입력**: 직접 입력, 파일 업로드, 드래그 앤 드롭
- **실시간 분석**: 진행 상황 표시 및 상태 업데이트
- **반응형 디자인**: 데스크톱, 태블릿, 모바일 최적화

### 📄 **다양한 출력 형식**
- **HTML 보고서**: 인터랙티브 웹 보고서
- **PDF 내보내기**: A4 최적화 인쇄용 문서
- **JSON 데이터**: 구조화된 분석 데이터
- **교육용 템플릿**: 교사 가이드, 학습 자료

## 🎓 교육적 활용

### 👩‍🏫 **교사용 도구**
- **수업 계획**: 텍스트 난이도 평가로 적절한 학습 자료 선택
- **교재 개발**: 어휘 목록 및 문법 연습 문제 생성
- **학생 평가**: 글쓰기 복잡도 및 구조 평가
- **커리큘럼 설계**: 학습 목표에 맞는 텍스트 정렬

### 👨‍🎓 **학생용 도구**
- **읽기 이해**: 텍스트 구조 및 조직 이해
- **어휘 학습**: 도전적인 단어 및 표현 식별
- **글쓰기 향상**: 모범 텍스트의 구조 패턴 학습
- **언어 학습**: 적절한 난이도 텍스트로 단계적 학습

### 🔬 **연구자용 도구**
- **코퍼스 분석**: 대량 텍스트 컬렉션 분석
- **언어학 연구**: 언어 사용 패턴 연구
- **교육 연구**: 텍스트 복잡도와 이해도 관계 조사
- **교재 개발**: 등급별 읽기 자료 생성

## 🛠️ 기술적 특징

### 🌐 **웹 기반**
- **설치 불필요**: 브라우저에서 완전히 실행
- **크로스 플랫폼**: 데스크톱, 태블릿, 모바일 지원
- **오프라인 기능**: 초기 로드 후 오프라인 작업 가능

### 🔒 **개인정보 보호**
- **로컬 저장**: API 키는 브라우저에만 저장
- **데이터 수집 없음**: 사용자 텍스트 추적 없음
- **로컬 처리**: 모든 인터페이스 로직이 로컬에서 실행

### 📱 **반응형 디자인**
- **모바일 최적화**: 터치 친화적 인터페이스
- **인쇄 친화적**: A4 용지 인쇄 최적화 레이아웃
- **접근성**: 키보드 탐색 및 스크린 리더 지원

## 📦 프로젝트 구조

```
text-analyzer-project/
├── docs/                          # GitHub Pages 웹 애플리케이션
│   ├── index.html                 # 메인 애플리케이션 페이지
│   ├── static/                    # CSS, JS, 에셋
│   ├── templates/                 # 보고서 템플릿
│   └── tests/                     # 프론트엔드 테스트
├── english_text_analyzer/         # Python 패키지
│   ├── analyzers/                 # 분석 모듈
│   ├── core/                      # 핵심 엔진
│   ├── models/                    # 데이터 모델
│   └── tests/                     # 단위 테스트
├── webapp/                        # Flask 웹 애플리케이션
├── .github/workflows/             # GitHub Actions
└── .kiro/specs/                   # 프로젝트 명세서
```

## 🚀 배포 및 설치

### GitHub Pages 배포
1. 이 레포지토리를 포크하거나 클론
2. GitHub Pages 설정에서 소스를 "GitHub Actions"로 설정
3. 자동으로 배포되어 웹에서 접근 가능

### 로컬 개발
```bash
# 레포지토리 클론
git clone https://github.com/Reasonofmoon/Text-Analysis.git
cd text-analyzer-project

# Python 환경 설정
pip install -r requirements.txt

# 웹 서버 실행 (선택사항)
cd docs
python -m http.server 8000
```

## 📚 문서

- [사용자 가이드](docs/USER_GUIDE.md) - 상세한 사용법
- [API 설정 가이드](docs/API_GUIDE.md) - API 키 설정 방법
- [배포 가이드](DEPLOYMENT_README.md) - 배포 및 유지보수
- [완료 요약](COMPLETION_SUMMARY.md) - 프로젝트 완료 상태

## 🤝 기여하기

이 프로젝트는 오픈소스입니다. 기여를 환영합니다:
- 버그 리포트 및 이슈 제기
- 새로운 기능 제안
- 문서 개선
- 코드 개선 제출

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

## 🙏 감사의 말

- **Google Gemini API**: AI 기반 텍스트 분석 제공
- **교육 커뮤니티**: 교사와 학생들의 피드백과 요구사항
- **오픈소스 라이브러리**: 향상된 기능을 위한 다양한 JavaScript 라이브러리

---

**English Text Analyzer**로 영어 텍스트 분석을 시작해보세요! 🌟

교육, 연구, 학습 목적으로 설계된 이 도구는 복잡한 언어학적 분석을 누구나 쉽게 사용할 수 있도록 만들어졌습니다.