import os
import pandas as pd
from datetime import datetime
from .save_snp500_stock_index import save_snp500_stock_index
base_dir = os.path.dirname(os.path.abspath(__file__))
# 파일을 다운로드받고 엑셀 파일로 갱신하는 과정을 하루에 한번만 하는 로직
LAST_RUN_FILE = os.path.join(base_dir,'get_snp500_index.log')
# 최근 실행 날짜 확인
def get_last_run_date():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as file:
            last_run_date = file.read().strip()
            return datetime.strptime(last_run_date, '%Y-%m-%d').date()
    return None
# 실행 날짜 저장
def set_last_run_date(date):
    with open(LAST_RUN_FILE, 'w') as file:
        file.write(date.strftime('%Y-%m-%d'))
once_per_day=False

today = datetime.now().date()
last_run_date = get_last_run_date()
if not last_run_date == today:
    set_last_run_date(today)
else: once_per_day = True

# 한국투자증권 API 만의 특이한 해외 주식 심볼 적용
error_symbol = {'BFb':'BF/B','BRKb':'BRK/B'}
def change_error_symbols(symbols, err_symbol = error_symbol) -> None:
    """
    파일에서 가져온 주식 symbol 을 한투에서 사용하는 symbol 로 교체하는 함수
    Args:
        SNP500 (Dict[str,Any]): 파일에서 가져온 SNP500 symbol 을 키값으로 갖는 Dict
        err_symbol (Dict[str,str], optional): `{ 교체할 파일 symbol : 대체할 한투 symbol }`
    """
    for file_symbol in err_symbol:
        new_key = err_symbol[file_symbol]
        symbols[new_key]=symbols.pop(file_symbol)

# S&P500 심볼 데이터 생성
def get_snp500_index(save : bool = False):
    """
    S&P500 의 symbol, market, name_en, name_kr 정보를 가진 딕셔너리 반환

    Returns: `{ symbol : { market, name_en, name_kr }}` 
    """
    #엑셀 파일을 매일 한번만 갱신
    if not once_per_day : save_snp500_stock_index()
    file_dir = 'datafiles'
    file_name = 'frgn_code.xlsx'
    file_path = os.path.join(base_dir,file_dir,file_name)
    df = pd.read_excel(file_path,'Sheet1')
    market_code = {'NASD' : 'NASDAQ', 'NYSE' : 'NYSE', 'AMEX' : 'AMEX'}
    snp500_index = {
        row['심볼'].strip(): {
            'market': market_code[row['거래소코드'].strip()],
            'name_en': row['영문명'].strip(),
            'name_kr': row['한글명'].strip()
        }
        for _, row in df.iterrows() if row['S&P 500 편입종목여부'] == 1
    }
    change_error_symbols(snp500_index)
    return snp500_index

SNP500_INDEX = get_snp500_index()
SNP500_INDEX_SYMBOLS = list(SNP500_INDEX.keys())
if __name__ == '__main__':
    print(SNP500_INDEX)