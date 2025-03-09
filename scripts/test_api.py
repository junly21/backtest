"""API 테스트 스크립트"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_create_backtest():
    """백테스트 실행 API 테스트"""
    print("\n1. 백테스트 실행 테스트 (POST /backtest)")
    print("-" * 50)
    
    # 테스트 데이터
    data = {
        "start_year": 2020,
        "start_month": 1,
        "initial_investment": 1000000,
        "trade_day": 15,
        "fee_rate": 0.001,
        "momentum_window": 3
    }
    
    response = requests.post(f"{BASE_URL}/backtest", json=data)
    result = response.json()
    
    print("요청 데이터:", json.dumps(data, indent=2, ensure_ascii=False))
    print("\n응답 결과:", json.dumps(result, indent=2, ensure_ascii=False))
    print(f"상태 코드: {response.status_code}")
    
    return result

def test_list_backtests():
    """백테스트 목록 조회 API 테스트"""
    print("\n2. 백테스트 목록 조회 테스트 (GET /backtest)")
    print("-" * 50)
    
    response = requests.get(f"{BASE_URL}/backtest")
    result = response.json()
    
    print("응답 결과:", json.dumps(result, indent=2, ensure_ascii=False))
    print(f"상태 코드: {response.status_code}")
    
    return result

def test_get_backtest_detail(data_id: int):
    """특정 백테스트 상세 정보 조회 API 테스트"""
    print(f"\n3. 백테스트 상세 정보 조회 테스트 (GET /backtest/{data_id})")
    print("-" * 50)
    
    response = requests.get(f"{BASE_URL}/backtest/{data_id}")
    result = response.json()
    
    print("응답 결과:", json.dumps(result, indent=2, ensure_ascii=False))
    print(f"상태 코드: {response.status_code}")
    
    return result

def test_delete_backtest(data_id: int):
    """백테스트 삭제 API 테스트"""
    print(f"\n4. 백테스트 삭제 테스트 (DELETE /backtest/{data_id})")
    print("-" * 50)
    
    response = requests.delete(f"{BASE_URL}/backtest/{data_id}")
    result = response.json()
    
    print("응답 결과:", json.dumps(result, indent=2, ensure_ascii=False))
    print(f"상태 코드: {response.status_code}")
    
    return result

def main():
    """모든 API 테스트 실행"""
    # 1. 백테스트 실행
    create_result = test_create_backtest()
    data_id = create_result["data_id"]
    
    # 2. 백테스트 목록 조회
    test_list_backtests()
    
    # 3. 특정 백테스트 상세 정보 조회
    test_get_backtest_detail(data_id)
    
    # 4. 백테스트 삭제
    test_delete_backtest(data_id)
    
    # 5. 삭제 후 목록 다시 조회
    print("\n5. 삭제 후 목록 재조회")
    print("-" * 50)
    test_list_backtests()

if __name__ == "__main__":
    main() 