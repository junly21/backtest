"""CLI 뷰 관련 로직"""
from typing import Dict, Any
from pydantic import ValidationError
from app.models.backtest import BacktestInput, BacktestResult

class BacktestView:
    """백테스트 CLI 뷰"""
    
    DEFAULT_VALUES = {
        "start_year": 2020,
        "start_month": 1,
        "initial_investment": 1000000,
        "trade_day": 15,
        "fee_rate": 0.001,
        "momentum_window": 3
    }
    
    @classmethod
    def get_input(cls) -> BacktestInput:
        """사용자로부터 입력값을 받아 BacktestInput 객체 생성"""
        try:
            print("\n=== 백테스트 입력값 설정 ===")
            print("(Enter를 누르면 기본값이 사용됩니다)")
            
            # 사용자 입력 받기
            values = {}
            values["start_year"] = input(f"시작 연도 (기본값: {cls.DEFAULT_VALUES['start_year']}): ")
            values["start_month"] = input(f"시작 월 (1-12) (기본값: {cls.DEFAULT_VALUES['start_month']}): ")
            values["initial_investment"] = input(f"초기 투자금액 (원) (기본값: {cls.DEFAULT_VALUES['initial_investment']}): ")
            values["trade_day"] = input(f"매매일 (1-31) (기본값: {cls.DEFAULT_VALUES['trade_day']}): ")
            values["fee_rate"] = input(f"거래 수수료율 (0-1) (기본값: {cls.DEFAULT_VALUES['fee_rate']}): ")
            values["momentum_window"] = input(f"비중 계산 기준 개월 수 (기본값: {cls.DEFAULT_VALUES['momentum_window']}): ")
            
            return cls._validate_input(values)
            
        except ValidationError as e:
            print("\n입력값 검증 오류 발생:")
            for error in e.errors():
                print(f"- {error['loc'][0]}: {error['msg']}")
            print("\n기본값으로 백테스트를 진행합니다.")
            return BacktestInput(**cls.DEFAULT_VALUES)
    
    @classmethod
    def _validate_input(cls, values: Dict[str, str]) -> BacktestInput:
        """입력값 검증 및 변환"""
        input_dict = {}
        for key, value in values.items():
            try:
                if value.strip():  # 입력값이 있는 경우
                    if key in ["start_year", "start_month", "trade_day", "momentum_window"]:
                        input_dict[key] = int(value)
                    else:
                        input_dict[key] = float(value)
                else:  # 빈 입력값은 기본값 사용
                    input_dict[key] = cls.DEFAULT_VALUES[key]
            except ValueError:
                print(f"\n{key} 입력값 오류: 올바른 숫자 형식이 아닙니다. 기본값을 사용합니다.")
                input_dict[key] = cls.DEFAULT_VALUES[key]
        
        return BacktestInput(**input_dict)
    
    @staticmethod
    def show_result(input_data: BacktestInput, result: BacktestResult) -> None:
        """백테스트 결과 출력"""
        print("\n=== 백테스트 결과 ===")
        print(f"전체 기간 수익률: {result.total_return:.2%}")
        print(f"연환산수익률 (CAGR): {result.cagr:.2%}")
        print(f"연 변동성: {result.annual_volatility:.2%}")
        print(f"샤프 지수: {result.sharpe_ratio:.2f}")
        print(f"최대 손실폭 (MDD): {result.max_drawdown:.2%}")
        
        print(f"\n초기 투자금액: {input_data.initial_investment:,.0f}원")
        print(f"최종 투자금액: {result.final_investment_value:,.0f}원")
        
        print("\n최종 자산 비중:")
        for ticker, weight in result.last_weights:
            if weight > 0:
                print(f"{ticker}: {weight:.2%}") 