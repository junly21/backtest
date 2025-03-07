import pandas as pd
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.models import Base, Price
from app.core.constants import ETF_TICKERS

def import_prices_from_excel(excel_path: str):
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 엑셀 파일 읽기
    df = pd.read_excel(excel_path)
    
    # 데이터 타입 변환
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    # DB 세션 생성
    db = SessionLocal()
    
    try:
        # 각 ETF별로 데이터 변환 및 저장
        for etf in ETF_TICKERS:
            # 해당 ETF의 데이터만 선택
            etf_data = df[['date', etf]].copy()
            etf_data.columns = ['date', 'price']
            etf_data['ticker'] = etf
            
            # 데이터 삽입
            for _, row in etf_data.iterrows():
                price = Price(
                    date=row['date'],
                    ticker=row['ticker'],
                    price=row['price']
                )
                db.merge(price)  # merge를 사용하여 중복 데이터 처리
        
        # 변경사항 저장
        db.commit()
        print("데이터 임포트 완료!")
        
    except Exception as e:
        print(f"에러 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # 엑셀 파일 경로를 인자로 받아서 실행
    import sys
    if len(sys.argv) != 2:
        print("사용법: python scripts/import_prices.py <엑셀_파일_경로>")
        sys.exit(1)
        
    excel_path = sys.argv[1]
    import_prices_from_excel(excel_path) 