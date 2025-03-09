# ETF Momentum Backtest Service

ETF 모멘텀 전략을 백테스트하고 결과를 API로 제공하는 서비스입니다.

## 🛠 기술 스택

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Docker Compose

## 🚀 빠른 시작 (Docker)

### 1. 환경 설정

```bash
# 환경 변수 파일 생성
cp .env.example .env
# .env 파일을 필요에 따라 수정하세요
```

### 2. 실행

```bash
# Docker 컨테이너 실행
docker-compose up --build

# 또는 백그라운드에서 실행
docker-compose up -d
```

### 3. API 사용

- API 문서 및 테스트: http://localhost:8000/docs#

### 4. 데이터베이스 확인

```bash
# PostgreSQL 접속
docker-compose exec db psql -U backtest -d backtest

# backtests 테이블 조회
SELECT * FROM backtests;
```

### 5. 종료

```bash
# 컨테이너 종료 (백그라운드 실행 시)
docker-compose down

# 컨테이너와 볼륨 모두 제거
docker-compose down -v
```

## 📁 프로젝트 구조

```
backtest/
├── app/                    # 애플리케이션 메인 디렉토리
│   ├── api/               # API 라우터 및 엔드포인트
│   ├── core/              # 설정, 상수, 공통 유틸리티
│   ├── crawlers/          # 데이터 수집기
│   ├── db/                # 데이터베이스 연결 및 세션 관리
│   ├── models/            # SQLAlchemy 모델 정의
│   ├── repositories/      # 데이터베이스 CRUD 작업 처리
│   ├── schemas/           # Pydantic 모델 (요청/응답 스키마)
│   ├── services/          # 비즈니스 로직 구현
│   ├── trading/           # 트레이딩 관련 로직
│   ├── utils/             # 유틸리티 함수
│   ├── views/             # 데이터 표현 로직
│   ├── main.py           # FastAPI 애플리케이션 진입점
│   └── __init__.py       # 패키지 초기화
├── alembic/               # 데이터베이스 마이그레이션
│   ├── versions/         # 마이그레이션 버전 스크립트
│   └── env.py            # Alembic 환경 설정
└── tests/                # 테스트 코드
    ├── api/              # API 엔드포인트 테스트
    └── services/         # 비즈니스 로직 테스트
```

### 데이터베이스 스키마 변경

```bash
# 새 마이그레이션 생성
docker-compose exec app alembic revision --autogenerate -m "변경 설명"

# 마이그레이션 적용
docker-compose exec app alembic upgrade head
```

## 💡 주요 기능 구현

### 1. 가격 데이터 초기 적재

- **구현 위치**: `scripts/import_prices.py`
- **주요 기능**:
  - Excel 파일의 가격 데이터를 PostgreSQL DB에 적재
  - 중복 데이터 처리 (merge 사용)
  - 데이터 타입 검증 및 변환

### 2. 일일 가격 데이터 수집 배치

- **구현 위치**:
  - 배치 실행: `batch/daily_fetch.py`
  - 데이터 수집: `app/crawlers/`
  - 가격 저장: `app/services/price_service.py`
- **주요 기능**:
  - Yahoo Finance 데이터 수집
  - DB 업데이트 및 로깅

### 3. 백테스트 계산 로직

- **구현 위치**:
  - 트레이딩 로직: `app/trading/`
    - `strategy.py`: 모멘텀 전략 구현
    - `portfolio.py`: 포트폴리오 관리
    - `nav.py`: NAV 계산
    - `dates.py`: 거래일 관리
  - 계산 유틸리티: `app/utils/calculations.py`
- **주요 기능**:
  - 모멘텀 기반 자산 선택
  - 리밸런싱 비중 계산
  - NAV 및 수수료 계산
  - 성과 지표 계산 (수익률, 변동성, 샤프 등)

### 4. REST API 엔드포인트

- **구현 위치**: `app/api/routes/`
- **주요 기능**:
  - 백테스트 실행 및 저장 (`POST /api/backtest/`)
  - 백테스트 목록 조회 (`GET /api/backtest/`)
  - 특정 백테스트 조회 (`GET /api/backtest/{data_id}`)
  - 백테스트 삭제 (`DELETE /api/backtest/{data_id}`)
