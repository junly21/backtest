"""백테스트 실행 스크립트"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.backtest_service import BacktestService
from app.views.cli import BacktestView
from app.core.constants import DATABASE_URL

def main():
    # DB 연결
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 사용자 입력 받기
        input_data = BacktestView.get_input()
        
        # 백테스트 실행
        service = BacktestService(db)
        result = service.run_backtest(input_data)
        
        # 결과 출력
        BacktestView.show_result(input_data, result)
        
    finally:
        db.close()

if __name__ == "__main__":
    main() 