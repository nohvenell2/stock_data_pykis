from ._pykis.Load_Pykis import KIS
from typing import Literal, TypedDict, List
from decimal import Decimal

class ChartDailyData(TypedDict):
    time : str
    open : Decimal
    high : Decimal
    low :  Decimal
    close : Decimal
    volume : Decimal

def convert_symbol_to_chartlist(
    symbol : str, past : str, market : Literal['KRX','NYSE','NASDAQ']
    ) -> List[ChartDailyData]:
    """
    symbol 의 시계열 데이터 리턴
    """
    stock = KIS.stock(symbol,market = market)
    chart = stock.chart(expression=past,period='day',adjust=True)
    df = chart.df()
    #df 에 symbol 칼럼 추가
    df['symbol'] = symbol
    #칼럼명 db에 맞게 변경
    df = df.rename(columns={
        "time": "trade_date",
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price",
        "volume": "volume"
    })
    result = df.to_dict(orient='records')
    return result