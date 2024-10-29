"""
KOSPI 주식 시계열 일일 csv 데이터를 불러와 데이터베이스에 저장
주식 시계열 데이터 업데이트
"""
import pandas as pd
import os
from ..db.connect_db import engine

# CSV 파일 경로
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'datafiles'
csv_file = 'kospi_history_20year.csv'
csv_path = os.path.join(base_dir,csv_folder,csv_file)
# CSV 파일을 데이터 프레임으로 읽어오기, 필요한 컬럼에 대한 타입 설정
df = pd.read_csv(csv_path, dtype={'단축코드': str})

# 컬럼명 매핑
df = df.rename(columns={
    '일자': 'trade_date',
    '종가': 'close_price',
    '시가': 'open_price',
    '고가': 'high_price',
    '저가': 'low_price',
    '거래량': 'volume',
    '단축코드': 'symbol'
})

# 필요한 컬럼만 선택
df = df[['symbol', 'trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']]

# 큰따옴표 제거 및 날짜 형식 변환
df['trade_date'] = df['trade_date'].str.replace('"', '', regex=False)
df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y/%m/%d', errors='coerce')

# 데이터 형식 변환 (숫자 포맷)
df['open_price'] = pd.to_numeric(df['open_price'].str.replace('"', ''), errors='coerce')
df['high_price'] = pd.to_numeric(df['high_price'].str.replace('"', ''), errors='coerce')
df['low_price'] = pd.to_numeric(df['low_price'].str.replace('"', ''), errors='coerce')
df['close_price'] = pd.to_numeric(df['close_price'].str.replace('"', ''), errors='coerce')
df['volume'] = pd.to_numeric(df['volume'].str.replace('"', ''), errors='coerce')

# MySQL 테이블에 데이터 삽입
try:
    df.to_sql(name='stock_price_daily_kospi', con=engine, if_exists='append', index=False)
    print("데이터 삽입 완료!")
except Exception as e:
    print("에러 발생:", e)
