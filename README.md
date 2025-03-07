# ETF Backtest Service

ETF의 가격 데이터를 이용해 투자 전략의 과거 성과를 시뮬레이션하는 "백테스트" 서비스를 제공합니다.

## 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 필요한 설정을 수정하세요
```

### 2. 데이터 준비

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
