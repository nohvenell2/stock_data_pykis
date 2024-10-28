from ._pykis.Load_Pykis import KIS
from .kospi.get_kospi_index import KOSPI_INDEX
from .snp.get_snp500_index import SNP500_INDEX
from typing import TypedDict, Optional
from decimal import Decimal
from datetime import date
from typing import Literal

class StockQuote(TypedDict):
    symbol: str                              # 종목코드
    stock_name: str                          # 종목명
    market: str                              # 종목시장
    sector_name: Optional[str]               # 업종명
    price: Optional[Decimal]                 # 현재가
    volume: Optional[int]                    # 거래량
    amount: Optional[Decimal]                # 거래대금
    market_cap: Optional[Decimal]            # 시가총액
    sign: Optional[str]                      # 대비부호 ('rise', 'decline' 등 문자열)
    risk: Optional[str]                      # 위험도
    halt: Optional[bool]                     # 거래정지
    overbought: Optional[bool]               # 단기과열구분
    prev_price: Optional[Decimal]            # 전일종가
    prev_volume: Optional[Decimal]           # 전일거래량 (Decimal로 수정)
    change: Optional[Decimal]                # 전일대비
    high_limit: Optional[Decimal]            # 상한가
    low_limit: Optional[Decimal]             # 하한가
    unit: Optional[Decimal]                  # 거래단위
    tick: Optional[Decimal]                  # 호가단위
    decimal_places: Optional[int]            # 소수점 자리수
    currency: Optional[str]                  # 통화코드
    exchange_rate: Optional[Decimal]         # 당일환율
    open: Optional[Decimal]                  # 당일시가
    high: Optional[Decimal]                  # 당일고가
    low: Optional[Decimal]                   # 당일저가
    close: Optional[Decimal]                 # 종가 (price와 동일하게 설정)
    rate: Optional[Decimal]                  # 등락율, 계산식 적용 필요 (change / prev_price * 100)
    sign_name: Optional[str]                 # 대비부호명, sign에 따라 한국어 반환
    eps: Optional[Decimal]                   # EPS (주당순이익)
    bps: Optional[Decimal]                   # BPS (주당순자산)
    per: Optional[Decimal]                   # PER (주가수익비율)
    pbr: Optional[Decimal]                   # PBR (주가순자산비율)
    week52_high: Optional[Decimal]           # 52주 최고가
    week52_low: Optional[Decimal]            # 52주 최저가
    week52_high_date: Optional[date]         # 52주 최고가 날짜 (date 타입으로 수정)
    week52_low_date: Optional[date]          # 52주 최저가 날짜 (date 타입으로 수정)

def convert_symbol_to_infodict(symbol : str):
    """
    pykis quote 객체를 dict 로 변환
    Args:
        quote (KisQuote):

    Returns:
        Dict[str,Demical|int|str]:
    """
    if symbol in KOSPI_INDEX: market = KOSPI_INDEX[symbol]['market']
    elif symbol in SNP500_INDEX: market = SNP500_INDEX[symbol]['market']
    else : raise KeyError(f'{symbol} not in Database.')

    stock = KIS.stock(symbol,market=market)
    quote = stock.quote()
    data : StockQuote= {
        'symbol': quote.symbol,                   # 종목코드
        'stock_name': quote.name,                 # 종목명
        'market': quote.market,                   # 종목시장
        'sector_name': quote.sector_name,         # 업종명
        'price': quote.price,                     # 현재가
        'volume': quote.volume,                   # 거래량
        'amount': quote.amount,                   # 거래대금
        'market_cap': quote.market_cap,           # 시가총액
        'sign': quote.sign,                       # 대비부호
        'risk': quote.risk,                       # 위험도
        'halt': quote.halt,                       # 거래정지
        'overbought': quote.overbought,           # 단기과열구분
        'prev_price': quote.prev_price,           # 전일종가
        'prev_volume': quote.prev_volume,         # 전일거래량
        'change': quote.change,                   # 전일대비
        'high_limit': quote.high_limit,           # 상한가
        'low_limit': quote.low_limit,             # 하한가
        'unit': quote.unit,                       # 거래단위
        'tick': quote.tick,                       # 호가단위
        'decimal_places': quote.decimal_places,   # 소수점 자리수
        'currency': quote.currency,               # 통화코드
        'exchange_rate': quote.exchange_rate,     # 당일환율
        'open': quote.open,                       # 당일시가
        'high': quote.high,                       # 당일고가
        'low': quote.low,                         # 당일저가
        'close': quote.close,                         # 당일저가
        'rate': quote.rate,                       # 등락율
        'sign_name': quote.sign_name,             # 대비부호명

        # 종목 지표
        'eps': quote.indicator.eps,               # EPS (주당순이익)
        'bps': quote.indicator.bps,               # BPS (주당순자산)
        'per': quote.indicator.per,               # PER (주가수익비율)
        'pbr': quote.indicator.pbr,               # PBR (주가순자산비율)
        'week52_high': quote.indicator.week52_high,               # 52주 최고가
        'week52_low': quote.indicator.week52_low,                 # 52주 최저가
        'week52_high_date': quote.indicator.week52_high_date,  # 52주 최고가 날짜
        'week52_low_date': quote.indicator.week52_low_date,    # 52주 최저가 날짜
    }

    return data


if __name__ == '__main__':
    print(convert_symbol_to_infodict('AAPL'))