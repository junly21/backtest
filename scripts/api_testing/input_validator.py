"""입력값 검증 모듈"""
from datetime import datetime
from typing import Any, Callable, Dict, Optional, TypeVar

T = TypeVar('T')

class InputValidator:
    """입력값 검증 클래스"""

    @staticmethod
    def get_input_with_default(
        prompt: str,
        default_value: T,
        validator: Optional[Callable[[T], bool]] = None
    ) -> T:
        """기본값이 있는 입력 받기"""
        while True:
            try:
                user_input = input(f"{prompt} (기본값: {default_value}): ").strip()
                if user_input == "":
                    value = default_value
                else:
                    # 타입 변환
                    if isinstance(default_value, int):
                        value = int(user_input)
                    elif isinstance(default_value, float):
                        value = float(user_input)
                    else:
                        value = user_input
                
                # 유효성 검사
                if validator and not validator(value):
                    raise ValueError("유효하지 않은 입력값입니다.")
                
                return value
            except ValueError as e:
                print(f"에러: {str(e)}")

    def get_backtest_input(self) -> Dict[str, Any]:
        """백테스트 입력값 받기"""
        print("\n=== 백테스트 입력값 설정 ===")
        current_year = datetime.now().year
        
        # 입력값 검증 함수들
        def validate_year(y): return 2000 <= y <= current_year
        def validate_month(m): return 1 <= m <= 12
        def validate_investment(i): return i > 0
        def validate_trade_day(d): return 1 <= d <= 31
        def validate_fee_rate(f): return 0 <= f < 1
        def validate_momentum_window(w): return w > 0

        return {
            "start_year": self.get_input_with_default(
                "시작 연도", 2020,
                validator=validate_year
            ),
            "start_month": self.get_input_with_default(
                "시작 월 (1-12)", 1,
                validator=validate_month
            ),
            "initial_investment": self.get_input_with_default(
                "초기 투자금액 (원)", 1000000,
                validator=validate_investment
            ),
            "trade_day": self.get_input_with_default(
                "매매일 (1-31)", 15,
                validator=validate_trade_day
            ),
            "fee_rate": self.get_input_with_default(
                "거래 수수료율 (0-1)", 0.001,
                validator=validate_fee_rate
            ),
            "momentum_window": self.get_input_with_default(
                "모멘텀 기간 (개월)", 3,
                validator=validate_momentum_window
            )
        } 