"""메뉴 처리 모듈"""
from typing import Dict, Callable, Any
from .input_validator import InputValidator
from .api_client import BacktestAPIClient
from .output_formatter import OutputFormatter

class MenuHandler:
    """메뉴 처리 클래스"""

    def __init__(self):
        self.api_client = BacktestAPIClient()
        self.input_validator = InputValidator()
        self.output_formatter = OutputFormatter()

    def print_menu(self):
        """메뉴 출력"""
        print("\n=== API 테스트 메뉴 ===")
        print("A. 백테스트 실행 (POST /backtest)")
        print("B. 백테스트 목록 조회 (GET /backtest)")
        print("C. 백테스트 상세 정보 조회 (GET /backtest/{data_id})")
        print("D. 백테스트 삭제 (DELETE /backtest/{data_id})")
        print("Q. 종료")
        print("-------------------")

    def handle_create_backtest(self):
        """백테스트 실행 처리"""
        try:
            params = self.input_validator.get_backtest_input()
            print(f"\n요청 데이터: {self.output_formatter.format_json(params)}")
            response = self.api_client.create_backtest(params)
            self.output_formatter.print_api_result("1. 백테스트 실행 테스트 (POST /backtest)", response)
        except Exception as e:
            self.output_formatter.print_error(e)

    def handle_list_backtests(self):
        """백테스트 목록 조회 처리"""
        try:
            response = self.api_client.list_backtests()
            self.output_formatter.print_api_result("2. 백테스트 목록 조회 테스트 (GET /backtest)", response)
        except Exception as e:
            self.output_formatter.print_error(e)

    def handle_get_backtest_detail(self):
        """백테스트 상세 정보 조회 처리"""
        try:
            data_id = self.input_validator.get_input_with_default(
                "조회할 백테스트 ID", 1,
                validator=lambda x: x > 0
            )
            response = self.api_client.get_backtest_detail(data_id)
            self.output_formatter.print_api_result(
                f"3. 백테스트 상세 정보 조회 테스트 (GET /backtest/{data_id})",
                response
            )
        except Exception as e:
            self.output_formatter.print_error(e)

    def handle_delete_backtest(self):
        """백테스트 삭제 처리"""
        try:
            data_id = self.input_validator.get_input_with_default(
                "삭제할 백테스트 ID", 1,
                validator=lambda x: x > 0
            )
            response = self.api_client.delete_backtest(data_id)
            self.output_formatter.print_api_result(
                f"4. 백테스트 삭제 테스트 (DELETE /backtest/{data_id})",
                response
            )
            
            # 삭제 후 목록 재조회
            print("\n5. 삭제 후 목록 재조회")
            self.handle_list_backtests()
        except Exception as e:
            self.output_formatter.print_error(e)

    def run(self):
        """메뉴 실행"""
        while True:
            try:
                self.print_menu()
                choice = input("테스트할 API 선택: ").upper()
                
                if choice == 'A':
                    self.handle_create_backtest()
                elif choice == 'B':
                    self.handle_list_backtests()
                elif choice == 'C':
                    self.handle_get_backtest_detail()
                elif choice == 'D':
                    self.handle_delete_backtest()
                elif choice == 'Q':
                    print("\n테스트를 종료합니다.")
                    break
                else:
                    print("\n잘못된 선택입니다. 다시 선택해주세요.")
                    
                input("\n계속하려면 Enter를 누르세요...")
            except KeyboardInterrupt:
                print("\n\n테스트를 종료합니다.")
                break
            except Exception as e:
                print(f"\n예상치 못한 에러가 발생했습니다: {str(e)}")
                input("\n계속하려면 Enter를 누르세요...") 