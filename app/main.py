"""FastAPI 애플리케이션"""
from fastapi import FastAPI
from app.api.routes import backtest
from app.db.database import engine, Base

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backtest API",
    description="백테스트 실행 및 결과 조회 API",
    version="1.0.0"
)

# 라우터 등록
app.include_router(backtest.router, prefix="/api", tags=["backtest"]) 