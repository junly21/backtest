#!/bin/bash

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# DB 생성 및 마이그레이션
createdb backtest
alembic upgrade head

# 가격 데이터 임포트
python scripts/import_prices.py

# 백테스트 실행
python scripts/run_backtest.py

echo "백테스트 설정 및 실행이 완료되었습니다." 