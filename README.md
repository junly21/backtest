# ETF Momentum Backtest Service

ETF 모멘텀 전략을 백테스트하고 결과를 API로 제공하는 서비스입니다.

## 1. 시작하기

### 사전 요구사항

- Python 3.12
- PostgreSQL

### Windows 사용자

1단계: 백테스트 환경 설정 및 실행

```bash
# 파일 더블클릭으로 실행하거나
.\setup_backtest.bat
```

2단계: API 서버 실행 및 테스트

```bash
# 파일 더블클릭으로 실행하거나
.\run_api_test.bat
```

### Mac/Linux 사용자

1단계: 스크립트 실행 권한 부여

```bash
chmod +x setup_backtest.sh run_api_test.sh
```

2단계: 백테스트 환경 설정 및 실행

```bash
./setup_backtest.sh
```

3단계: API 서버 실행 및 테스트

```bash
./run_api_test.sh
```

각 단계는 다음 작업을 수행합니다:

**백테스트 환경 설정 및 실행 (setup_backtest):**

- 가상환경 설정
- 필요한 패키지 설치
- 데이터베이스 생성 및 초기화
- 샘플 데이터 임포트
- 백테스트 실행

**API 서버 실행 및 테스트 (run_api_test):**

- FastAPI 서버 실행
- API 엔드포인트 테스트

### API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 2. 데이터 준비

1. `data/` 디렉토리에 가격 데이터가 포함된 엑셀 파일을 넣어주세요.

   - 파일명: `prices.xlsx`
   - 필수 컬럼: date, ticker, price
   - 예시 데이터:
     ```
     date        ticker  price
     2020-01-01  SPY     298.2208
     ```

2. 데이터베이스 생성

```bash
# PostgreSQL에 데이터베이스 생성
createdb backtest
```

3. 데이터 임포트

```bash
# 엑셀 파일의 데이터를 DB에 임포트
python scripts/import_prices.py data/prices.xlsx
```

## 초기 설정

1. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

3. PostgreSQL 데이터베이스 생성

```sql
CREATE DATABASE backtest;
CREATE USER backtest WITH PASSWORD 'backtest';
GRANT ALL PRIVILEGES ON DATABASE backtest TO backtest;
```

4. 데이터베이스 마이그레이션

```bash
# 마이그레이션 실행 (필수)
alembic upgrade head
```

## 실행 방법

1. FastAPI 서버 실행

```bash
uvicorn app.main:app --reload
```

2. API 테스트 실행

```bash
python scripts/test_api.py
```

## 데이터베이스 스키마 변경 시

새로운 모델을 추가하거나 기존 모델을 수정할 경우:

```bash
# 새로운 마이그레이션 생성
alembic revision --autogenerate -m "마이그레이션 설명"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 취소 (필요한 경우)
alembic downgrade -1
```

## 프로젝트 구조

```
backtest/
├── alembic/              # DB 마이그레이션 관련 파일
├── app/
│   ├── api/             # API 라우터
│   ├── core/           # 핵심 설정 및 상수
│   ├── db/             # 데이터베이스 모델 및 설정
│   └── schemas/        # Pydantic 모델 (API 스키마)
├── scripts/            # 유틸리티 스크립트
└── tests/             # 테스트 코드
```
