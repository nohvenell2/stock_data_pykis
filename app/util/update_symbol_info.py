from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .db.connect_db import engine
from .convert_symbol_to_infodict import convert_symbol_to_infodict
from .db.upsert_info import upsert_info

# MySQL 연결 설정
Session = sessionmaker(bind=engine)
session = Session()
def update_symbol_info(symbol: str):
    """
    주식 symbol -> KisQuote -> Dict -> mysql stock_info 테이블 에 저장
    """
    data = convert_symbol_to_infodict(symbol)
    upsert_info(data)