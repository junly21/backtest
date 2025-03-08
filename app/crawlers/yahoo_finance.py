"""
야후 파이낸스 크롤러
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, Optional

from app.core.constants import (
    YAHOO_FINANCE_BASE_URL,
    USER_AGENT,
)

def fetch_etf_price(ticker: str) -> Optional[Dict]:
    """
    야후 파이낸스 웹페이지에서 특정 ETF의 가격 정보를 크롤링합니다.
    (data-testid='qsp-price' 기준)

    Args:
        ticker (str): ETF 티커 심볼 (예: "SPY")

    Returns:
        Optional[Dict]: 성공시 {'date': datetime.date, 'price': float}, 실패시 None
    """
    url = f"{YAHOO_FINANCE_BASE_URL}/{ticker}"
    headers = {'User-Agent': USER_AGENT}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 가격 태그 찾기: <span data-testid="qsp-price">XXX</span>
        price_element = soup.find("span", {"data-testid": "qsp-price"})
        if not price_element:
            raise ValueError("가격 정보를 찾을 수 없습니다 (data-testid='qsp-price')")

        # 문자열 → float 변환 (예: "575.92")
        price_str = price_element.get_text(strip=True).replace(",", "")
        price = float(price_str)

        # 날짜는 간단히 "지금 시각"을 기준으로 (정확한 종가 날짜가 필요하다면 별도 파싱 필요)
        trade_date = datetime.now().date()

        return {
            'date': trade_date,
            'price': price
        }

    except Exception as e:
        print(f"Error fetching price for {ticker}: {str(e)}")
        return None 