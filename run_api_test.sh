#!/bin/bash

# 가상환경 활성화
source venv/bin/activate

# API 서버 백그라운드로 실행
uvicorn app.main:app --reload &

# API 테스트 (잠시 대기 후 실행)
sleep 5
python scripts/test_api.py 