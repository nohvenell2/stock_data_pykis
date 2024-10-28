from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .connect_db import engine
from typing import Literal
# MySQL 연결 설정
Session = sessionmaker(bind=engine)
session = Session()
def upsert_price(data,table_name : Literal['KOSPI','SNP500']):
    """
    한 주식의 하루 주가 데이터를 upsert
    """
    table_key = {'KOSPI':'kospi','SNP500':'snp500'}
    if not data: return None
    sql = text(f"""
        INSERT INTO stock_price_daily_{table_key[table_name]}(
            symbol, trade_date, open_price, high_price, low_price, close_price, volume
        ) VALUES (
            :symbol, :trade_date, :open_price, :high_price, :low_price, :close_price, :volume
        )
        ON DUPLICATE KEY UPDATE 
            open_price=VALUES(open_price),
            high_price=VALUES(high_price),
            low_price=VALUES(low_price),
            close_price=VALUES(close_price),
            volume=VALUES(volume)
    """)

    # 데이터 바인딩 및 SQL 실행
    session.execute(sql, {
        'trade_date' : data['trade_date'],
        'symbol' : data['symbol'],
        'open_price' : data['open_price'],
        'high_price' : data['high_price'], 
        'low_price' : data['low_price'], 
        'close_price' : data['close_price'],
        'volume' : data['volume']
    })
    # 트랜잭션 커밋
    session.commit()