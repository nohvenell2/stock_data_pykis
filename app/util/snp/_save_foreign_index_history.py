"""
S&P500, NASDAQ 종합지수, 다우존스 종합지수 히스토리 데이터를 저장하는 파일
S&P500, 다우존스는 한국시간 오전 9시, NADSAQ 은 오후 9시에 최신값 업데이트 됨
"""
import pandas as pd
import requests
from datetime import datetime, timedelta
import time, os
from dotenv import load_dotenv
load_dotenv()

curr_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = [curr_dir,'datafiles']
base_dir = os.path.join(*save_dir)

class MarketIndices:
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
    
    def get_index_data(self, series_id, start_date, end_date):
        """단일 지수의 데이터를 가져옵니다."""
        
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'observation_start': start_date,
            'observation_end': end_date,
            'frequency': 'd',  # 일별 데이터
            'limit': 100000,   # 최대 데이터 수 증가
            'sort_order': 'asc'  # 오름차순 정렬
        }
        
        all_data = []
        offset = 0
        
        while True:
            self._respect_rate_limit()
            
            try:
                # offset 파라미터 추가
                params['offset'] = offset
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                observations = data['observations']
                
                if not observations:  # 더 이상 데이터가 없으면 종료
                    break
                    
                all_data.extend(observations)
                
                # 다음 페이지가 없으면 종료
                if len(observations) < params['limit']:
                    break
                    
                offset += len(observations)
                
            except requests.exceptions.RequestException as e:
                print(f"API 요청 중 오류 발생 ({series_id}): {e}")
                return None
        
        if all_data:
            df = pd.DataFrame(all_data)
            
            # 데이터 정제
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna()
            
            return df[['date', 'value']]
        
        return None
    
    def get_all_indices(self, start_date=None, end_date=None):
        """모든 지수의 데이터를 가져와서 하나의 데이터프레임으로 병합"""
        
        # 기본 날짜 설정
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        # 결과를 저장할 데이터프레임
        merged_df = None
        
        for index_code, index_info in self.indices.items():
            print(f"{index_info['name']} 데이터 가져오는 중...")
            
            df = self.get_index_data(index_info['id'], start_date, end_date)
            
            if df is not None:
                print(f"{index_info['name']} 데이터 기간: {df['date'].min()} ~ {df['date'].max()}")
                print(f"데이터 수: {len(df):,}개\n")
                
                # 컬럼명을 지수 코드로 변경
                df = df.rename(columns={'value': index_code})
                
                if merged_df is None:
                    merged_df = df
                else:
                    merged_df = pd.merge(merged_df, df, on='date', how='outer')
        
        if merged_df is not None:
            # 날짜순으로 정렬
            merged_df = merged_df.sort_values('date')
            # 결측값 처리
            merged_df = merged_df.ffill()
        
        return merged_df

# 사용 예시
if __name__ == "__main__":
    # FRED API 키 설정
    api_key = os.getenv('APP_SEC_FRED')  # 본인의 API 키로 교체하세요
    START_DATE = "2014-10-31"
    END_DATE = "2024-10-31"
    # 인덱스 클래스 초기화
    indices = MarketIndices(api_key)
    
    # 데이터 가져오기 (예: 최근 1년)
    df = indices.get_all_indices(
        start_date=START_DATE,
        end_date=END_DATE
    )
    
    if df is not None:
        # 기본 데이터 저장
        file_name = 'us_stock_index_history.csv'
        file_path = os.path.join(base_dir,file_name)
        df.to_csv(file_path, index=False)
        print("\nus_stock_index_history.csv 파일이 저장되었습니다.")