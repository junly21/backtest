"""결과 출력 포맷팅 모듈"""
import json
from typing import Dict, Any

class OutputFormatter:
    """결과 출력 포맷팅 클래스"""

    @staticmethod
    def print_section_header(title: str):
        """섹션 헤더 출력"""
        print(f"\n{title}")
        print("-" * 50)

    @staticmethod
    def format_json(data: Any) -> str:
        """JSON 데이터 포맷팅"""
        return json.dumps(data, indent=2, ensure_ascii=False)

    def print_api_result(self, title: str, response: Dict[str, Any]):
        """API 결과 출력"""
        self.print_section_header(title)
        
        if "data" in response:
            print(f"응답 결과: {self.format_json(response['data'])}")
        
        if "status_code" in response:
            print(f"상태 코드: {response['status_code']}")

    def print_error(self, error: Exception):
        """에러 메시지 출력"""
        print(f"\n에러 발생: {str(error)}")
        if hasattr(error, 'response') and hasattr(error.response, 'text'):
            print(f"에러 응답: {error.response.text}") 