# 배포 가이드

English Text Analyzer 웹앱을 다양한 플랫폼에 배포하는 방법을 안내합니다.

## 🚀 빠른 배포 (원클릭)

### 1. Railway 배포
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

### 2. Render 배포
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/your-username/english-text-analyzer)

### 3. Vercel 배포
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/english-text-analyzer/tree/main/webapp)

## 📋 상세 배포 가이드

### Railway 배포

1. **GitHub 연결**
   - Railway 계정 생성 및 GitHub 연결
   - 저장소 선택 및 webapp 폴더 지정

2. **환경 변수 설정**
   ```
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=production
   ```

3. **자동 배포**
   - Railway가 자동으로 Dockerfile을 감지하여 배포
   - 도메인 자동 할당

### Render 배포

1. **서비스 생성**
   - Render 대시보드에서 "New Web Service" 선택
   - GitHub 저장소 연결

2. **설정**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

3. **환경 변수**
   ```
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=production
   ```

### Vercel 배포

1. **Vercel CLI 설치**
   ```bash
   npm i -g vercel
   ```

2. **배포**
   ```bash
   cd webapp
   vercel --prod
   ```

3. **환경 변수 설정**
   - Vercel 대시보드에서 환경 변수 추가

### Heroku 배포

1. **Procfile 생성**
   ```
   web: gunicorn app:app
   ```

2. **Heroku 앱 생성**
   ```bash
   heroku create your-app-name
   ```

3. **환경 변수 설정**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

4. **배포**
   ```bash
   git push heroku main
   ```

### Google Cloud Run 배포

1. **gcloud CLI 설정**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

2. **Docker 이미지 빌드 및 푸시**
   ```bash
   docker build -t gcr.io/your-project-id/english-text-analyzer .
   docker push gcr.io/your-project-id/english-text-analyzer
   ```

3. **Cloud Run 배포**
   ```bash
   gcloud run deploy english-text-analyzer \
     --image gcr.io/your-project-id/english-text-analyzer \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### AWS ECS 배포

1. **ECR 저장소 생성**
   ```bash
   aws ecr create-repository --repository-name english-text-analyzer
   ```

2. **Docker 이미지 푸시**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com
   docker build -t english-text-analyzer .
   docker tag english-text-analyzer:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/english-text-analyzer:latest
   docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/english-text-analyzer:latest
   ```

3. **ECS 서비스 생성**
   - AWS 콘솔에서 ECS 클러스터 및 서비스 생성
   - 태스크 정의에서 컨테이너 이미지 지정

## 🔧 환경 변수 설정

모든 배포 플랫폼에서 다음 환경 변수를 설정해야 합니다:

### 필수 환경 변수
```
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### 선택적 환경 변수
```
MAX_CONTENT_LENGTH=16777216
MAX_TEXT_LENGTH=50000
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

## 🔒 보안 설정

### HTTPS 설정
- 대부분의 플랫폼에서 자동으로 HTTPS 제공
- 커스텀 도메인 사용 시 SSL 인증서 설정 필요

### API 키 보안
- 클라이언트 사이드에서만 API 키 처리
- 서버에 API 키 저장하지 않음
- HTTPS를 통한 안전한 전송

### 파일 업로드 보안
- 파일 타입 제한 (.txt만 허용)
- 파일 크기 제한 (16MB)
- 임시 파일 자동 정리

## 📊 모니터링 및 로깅

### 로그 확인
```bash
# Railway
railway logs

# Heroku
heroku logs --tail

# Render
# 대시보드에서 로그 확인

# Vercel
vercel logs
```

### 성능 모니터링
- 각 플랫폼의 내장 모니터링 도구 활용
- 응답 시간 및 에러율 추적
- 리소스 사용량 모니터링

## 🚨 문제 해결

### 일반적인 문제

1. **메모리 부족**
   - 워커 수 줄이기
   - 타임아웃 시간 조정

2. **빌드 실패**
   - requirements.txt 확인
   - Python 버전 호환성 확인

3. **API 연결 오류**
   - 네트워크 설정 확인
   - 방화벽 규칙 확인

### 디버깅 팁
- 로그 레벨을 DEBUG로 설정
- 환경 변수 확인
- 의존성 버전 확인

## 📈 성능 최적화

### 서버 설정
```python
# gunicorn 설정 예시
workers = 2
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

### 캐싱 전략
- 정적 파일 CDN 사용
- 분석 결과 임시 캐싱
- 브라우저 캐싱 활용

### 리소스 최적화
- 이미지 압축
- CSS/JS 최소화
- 불필요한 의존성 제거

이 가이드를 따라 하시면 English Text Analyzer 웹앱을 성공적으로 배포할 수 있습니다!