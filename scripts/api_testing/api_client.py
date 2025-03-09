"""백테스트 API 클라이언트"""
import requests
from typing import Dict, Any, List, Optional

class BacktestAPIClient:
    """백테스트 API 클라이언트 클래스"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, json: Dict = None) -> Dict:
        """API 요청 수행"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method=method, url=url, json=json)
        response.raise_for_status()
        return {
            "status_code": response.status_code,
            "data": response.json() if response.content else None
        }

    def create_backtest(self, params: Dict[str, Any]) -> Dict:
        """백테스트 실행"""
        return self._make_request("POST", "backtest", json=params)

    def list_backtests(self) -> Dict:
        """백테스트 목록 조회"""
        return self._make_request("GET", "backtest")

    def get_backtest_detail(self, data_id: int) -> Dict:
        """백테스트 상세 정보 조회"""
        return self._make_request("GET", f"backtest/{data_id}")

    def delete_backtest(self, data_id: int) -> Dict:
        """백테스트 삭제"""
        return self._make_request("DELETE", f"backtest/{data_id}") 