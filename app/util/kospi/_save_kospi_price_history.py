"""
[ Warning ] 주의 !!!!!!!!!!!!!!!!!!!!!!!!
프로그램 정상 실행시 높은 확률로 KRX 정보데이터시스템 사이트에서 ip 영구 차단당함
PERIOD = 20 # 20년치 자료 다운로드 시 550 mb 이상의 csv 파일 생성

KRX 정보데이터시스템 사이트를 크롤링해 KOSPI 주식 시계열 일일 데이터를 csv 파일로 저장
db 에 처음으로 kospi history data 를 구축할때 실행
"""
import os
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
import cloudscraper
from get_kospi_index import KOSPI_INDEX, KOSPI_INDEX_SYMBOLS
from app.util.kospi._get_1y_period import generate_1y_periods

base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = 'datafiles'
save_path = os.path.join(base_dir,save_dir) # 임시파일 및 최종 파일 저장 경로
PERIOD = 20

def kospi_history_df(start_date: str, end_date: str) -> DataFrame:
    """KOSPI_INDEX 에 있는 종목의 start_date ~ end_date 주식 가격정보 기록

    Args:
        start_date (str): yyyymmdd
        end_date (str): yyyymmdd

    Returns:
        DataFrame: Column - 주식시장, 표준코드, 단축코드, 일자, 시가, 고가, 저가, 종가, 등락률, 거래량, 거래대금, 시가총액, 상장주식수 
    """
    df_kospi_history = pd.DataFrame() # KOSPI_INDEX 에 있는 종목의 start_date ~ end_date 주가 기록
    for symbol in tqdm(KOSPI_INDEX_SYMBOLS): # 주식 별 데이터프레임 저장 

        #크롤링에 필요한 요청 otp 획득
        code = KOSPI_INDEX[symbol]['isuCd']
        otp_url ='http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
        otp_form_data = {
            'locale': 'ko_KR',
            "share": '1',
            "csvxls_isNo": 'false',
            "name": 'fileDown',
            "url": 'dbms/MDC/STAT/standard/MDCSTAT01701',
            'strtDd': start_date, # 시작 날짜. 형식 yyyymmdd
            'endDd': end_date, #종료 날짜
            'adjStkPrc': 2, # 수정주가 반영. 싫으면 1
            'adjStkPrc_check': 'Y', # 수정주가 반영. 싫으면 N
            'isuCd': code #표준코드
        }
        # 크롤링한 데이터 -> csv
        scraper = cloudscraper.create_scraper()
        otp = scraper.post(otp_url, params=otp_form_data).text    
        csv_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
        csv_form_data = scraper.post(csv_url, params={'code': otp})
        csv_form_data.encoding = 'EUC-KR'

        # csv -> DataFrame
        lst_row = []
        for row in csv_form_data.text.split('\n'): 
            lst_row.append(row.split(','))
        df_stock_history = pd.DataFrame(lst_row[1:], columns=lst_row[0])
        df_stock_history['표준코드'] = code 
        df_stock_history['단축코드'] = symbol
        df_stock_history['주식시장'] = 'KOSPI'

        # 개별 주식 history 를 kospi history DataFrame 에 추가
        df_kospi_history = pd.concat([df_kospi_history, df_stock_history], ignore_index=True)
    # kospi history DataFrame 파일로 저장
    df_kospi_history.to_csv(os.path.join(save_path,f'{end_date}_{start_date}_kospi_history.csv'), index=False)

    return df_kospi_history

def save_kospi_history_total(period : int = PERIOD) -> None:
    """period 기간 kospi 종목 가격정보를 kospi_history_{period}year.csv 파일에 저장

    Args:
        period (int, optional): 검색 기간. Defaults to PERIOD.
    """
    date = generate_1y_periods(period) # period 기간 1년 단위 List[시작일, 종료일]
    total_df = pd.DataFrame()
    for d in tqdm(date):
        df_1year = kospi_history_df(d['start_date'],d['end_date'])
        total_df = pd.concat([total_df, df_1year], ignore_index=True)
    
    total_df = total_df.sort_values(by=['단축코드','일자']) # 주식 symbol 순, 그후 일자 순으로 정렬
    total_df.to_csv(os.path.join(save_path,f'kospi_history_{period}year.csv'), index=False)

if __name__ == '__main__':
    save_kospi_history_total(PERIOD)
    