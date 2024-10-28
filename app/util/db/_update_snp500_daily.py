from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .connect_db import engine
# MySQL 연결 설정
Session = sessionmaker(bind=engine)
session = Session()
def insert_price_snp500_daily(data):
    """
    INSERT IGNORE 로 daily price data 를 db 에 저장
    중복키의 data는 업데이트하지 않는다 
    """
    if not data: return None
    # MySQL의 INSERT IGNORE를 사용하는 직접 쿼리
    sql = text(f"""
        INSERT IGNORE INTO snp500_price_daily(
            symbol, trade_date, open_price, high_price, low_price, close_price, volume
        ) VALUES (
            :symbol, :trade_date, :open_price, :high_price, :low_price, :close_price, :volume
        );
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