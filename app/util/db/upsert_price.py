import os
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .connect_db import engine
from typing import Literal

from dotenv import load_dotenv
load_dotenv()
tablename_kospi = os.getenv('TABLENAME_KOSPI_PRICE_DAILY')
tablename_snp500 = os.getenv('TABLENAME_SNP500_PRICE_DAILY')
# MySQL 연결 설정
Session = sessionmaker(bind=engine)
session = Session()
def upsert_price(data,table_name : Literal['KOSPI','SNP500']):
    """
    한 주식의 하루 주가 데이터 upsert
    """
    table_key = {'KOSPI':tablename_kospi,'SNP500':tablename_snp500}
    if not data: return None
    sql = text(f"""
        INSERT INTO {table_key[table_name]} (
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