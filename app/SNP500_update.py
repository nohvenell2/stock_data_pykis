"""
S&P500 주식 기본정보, 가격 시계열 데이터 업데이트 실행 파일
PAST 로 가격 시계열 데이터 기간 설정. 예시 : 3d, 4m, 5y, None(전체기간)
"""
from update_Info import update_info
from update_price_daily import update_price_daily
from util.snp.get_snp500_index import SNP500_INDEX_SYMBOLS as SYMBOLS
from datetime import datetime
PAST = '3d' # 3일치 데이터
def main(dprint : bool = False,tqdm_disable : bool = True, past = PAST):
    start_time = datetime.now()
    if dprint: print(f'[START - {start_time}] ----------- S&P500 Update')
    update_info(SYMBOLS,tqdm_disable=tqdm_disable)
    update_price_daily(SYMBOLS, tqdm_disable = tqdm_disable, past = past)
    end_time = datetime.now()
    if dprint: print(f'[END - {end_time}] ----------- S&P500 Update. Take ')
    execution_time = end_time - start_time
    if dprint: print(f'Excution Time : {execution_time}')
    
if __name__ == '__main__':
    main(dprint=True, tqdm_disable=True)