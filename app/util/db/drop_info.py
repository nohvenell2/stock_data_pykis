import os
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from connect_db import engine

from dotenv import load_dotenv
load_dotenv()
TABLENAME_INFO = os.getenv('TABLENAME_INFO')
# MySQL 연결 설정
Session = sessionmaker(bind=engine)
session = Session()
def drop_info(symbol: str):
    """
    symbol 에 해당하는 info 정보 삭제
    """
    if not symbol:
        return None
    
    sql = text(f"""
        DELETE FROM {TABLENAME_INFO}
        WHERE symbol = :symbol
    """)
    
    # 데이터 바인딩 및 SQL 실행
    session.execute(sql, {'symbol': symbol})
    # 트랜잭션 커밋
    session.commit()
if __name__ == '__main__':
    drop_info('BIO')