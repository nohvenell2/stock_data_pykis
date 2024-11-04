"""
S&P500, NASDAQ 종합지수, 다우존스 종합지수 히스토리 데이터를 저장하는 파일
S&P500, 다우존스는 한국시간 오전 9시, NADSAQ 은 오후 9시에 최신값 업데이트 됨
"""
import pandas as pd
from pandas import DataFrame
import requests
from datetime import datetime, timedelta
import time, os
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

class FredIndex:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.last_request_time = 0
        
        # 지수별 FRED 시리즈 ID
        self.indices = {
            'SP500': {'id': 'SP500', 'name': 'S&P 500'},
            'DJIA': {'id': 'DJIA', 'name': 'Dow Jones Industrial Average'},
            'NASDAQ': {'id': 'NASDAQCOM', 'name': 'NASDAQ Composite'}
        }
    
    def _respect_rate_limit(self):
        """API 요청 간격을 0.5초로 제한"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < 0.5:
            time.sleep(0.5 - time_since_last_request)
            
        self.last_request_time = time.time()
    
    def get_index_data(self, series_id, start_date, end_date) -> DataFrame | None:
        """단일 지수의 데이터를 가져옵니다."""
        
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'observation_start': start_date,
            'observation_end': end_date,
            'frequency': 'd',  # 일별 데이터
            'limit': 1000,   # 최대 데이터 수 증가
            'sort_order': 'asc'  # 오름차순 정렬
        }
        
        self._respect_rate_limit()
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data['observations'])
            
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생 ({series_id}): {e}")
            return None
        # 데이터 정제
        if df.empty: return None
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna()
        
        return df[['date', 'value']]
    
    def get_all_index(self, period : int = 10, end_date : str | None = None):
        """모든 지수의 데이터를 가져와서 하나의 데이터프레임으로 병합"""
        
        # 기본 날짜 설정
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=period)).strftime('%Y-%m-%d')
        
        # 결과를 저장할 데이터프레임
        df_all = []
        for index_code, index_info in self.indices.items():
            df = self.get_index_data(index_info['id'], start_date, end_date)
            if df is not None:
                # 날짜순 정렬
                df['index_name'] = index_code
            df_all.append(df)
        df_all = pd.concat(df_all,ignore_index=True)
        # csv 로 파일 저장
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(*[curr_dir,'datafiles','foreign_index.csv'])
        df_all.to_csv(save_dir,index = False)
        return df_all

api_key = os.getenv('APP_SEC_FRED')
get_foreign = FredIndex(api_key).get_all_index
# 사용 예시
if __name__ == "__main__":
    print('')