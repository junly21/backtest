@echo off
REM 가상환경 생성 및 활성화
python -m venv venv
call venv\Scripts\activate

REM 의존성 설치
pip install -r requirements.txt

REM DB 생성 및 마이그레이션
createdb backtest
alembic upgrade head

REM 가격 데이터 임포트
python scripts/import_prices.py

REM 백테스트 실행
python scripts/run_backtest.py

echo 백테스트 설정 및 실행이 완료되었습니다.
pause 