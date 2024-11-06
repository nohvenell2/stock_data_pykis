import os, requests
import pandas as pd
from dotenv import load_dotenv
from .._pykis.Load_Pykis import TOKEN
from datetime import datetime, timedelta
load_dotenv()
#env
APP_KEY = os.getenv('APP_KEY_REAL')
APP_SEC = os.getenv('APP_SEC_REAL')
ACC_NO = os.getenv('ACC_NO_REAL')
token = f'Bearer {TOKEN}'
API_URL_REAL = 'https://openapi.koreainvestment.com:9443' # 실전투자 api url
def get_kospi(period : int = 5, end_date : str | None = None):
    """
    KOSPI 지수 시계열을 데이터 프레임으로 반환
    Args:
        period (int): 기간 defaults to 5
        end_date (str): yyyymmdd 형식. defaults to today

    Returns:
        DataFrame: date value 칼럼을 갖는 데이터프레임
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=period)).strftime('%Y%m%d')
    path = "/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice"
    url = f"{API_URL_REAL}/{path}"
    headers = {
        "content-type": "application/json",
        "authorization": token,
        "appKey": APP_KEY,
        "appSecret": APP_SEC,
        "tr_id": "FHKUP03500100"
    }
    params = {
        "fid_cond_mrkt_div_code": "U",
        "fid_input_date_1": start_date,
        "fid_input_date_2": end_date,
        "fid_input_iscd": "0001",
        "fid_period_div_code": "D"
    }
    resp = requests.get(url, headers=headers, params=params)
    data_json = resp.json()['output2']
    data=[]
    for d in data_json:
        data.append({'date':d['stck_bsop_date'],'value':d['bstp_nmix_prpr']})

    df = pd.DataFrame(data)
    # date 컬럼을 날짜 형식으로 변환
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    # value 컬럼을 숫자 형식으로 변환
    df['value'] = pd.to_numeric(df['value'])
    df['index_name'] = 'KOSPI'
    # csv 로 파일 저장
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(*[curr_dir,'datafiles','kospi_index.csv'])
    df.to_csv(save_dir,index = False)
    return df