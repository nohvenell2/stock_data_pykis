from .convert_symbol_to_chartlist import convert_symbol_to_chartlist
from .db.upsert_price import upsert_price
from .snp.get_snp500_index import SNP500_INDEX
from .kospi.get_kospi_index import KOSPI_INDEX

def update_symbol_price_daily(symbol,past):
    """
    symbol 의 시계열 데이터를 db 에 저장
    """
    # symbol 에서 db 에 저장할 table, pykis 에서 사용할 market 분류
    if symbol in KOSPI_INDEX:
        table = "KOSPI"
        market = KOSPI_INDEX[symbol]['market']
    elif symbol in SNP500_INDEX:
        table = "SNP500"
        market =  SNP500_INDEX[symbol]['market']
    else:
        raise KeyError(f'{symbol} not in DataBase')
    # 데이터 저장 - 덮어씌우기
    data_list = convert_symbol_to_chartlist(symbol,past,market)
    for data in data_list: 
        upsert_price(data,table)