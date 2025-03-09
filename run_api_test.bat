@echo off
REM 가상환경 활성화
call venv\Scripts\activate

REM API 서버 실행 (새 창에서)
start cmd /k "call venv\Scripts\activate && uvicorn app.main:app --reload"

REM API 테스트 (잠시 대기 후 실행)
timeout /t 5
python scripts/test_api.py
pause 