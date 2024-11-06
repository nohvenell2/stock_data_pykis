import os
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .connect_db import engine

from dotenv import load_dotenv
load_dotenv()
TABLENAME_INDEX = os.getenv('TABLENAME_INDEX')
# MySQL 연결 설정
Session = sessionmaker(bind=engine)
session = Session()
def upsert_index(data):
    """
    index의 하루 주가 데이터 upsert
    """
    if not data: return None
    sql = text(f"""
        INSERT INTO {TABLENAME_INDEX} (date, value, index_name)
        VALUES (:date, :value, :index_name)
        ON DUPLICATE KEY UPDATE value = VALUES(value);
        """)

    # 데이터 바인딩 및 SQL 실행
    session.execute(sql, {
        'date' : data['date'],
        'index_name' : data['index_name'],
        'value' : data['value'],
    })
    # 트랜잭션 커밋
    session.commit()