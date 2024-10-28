from tqdm import tqdm
from util.update_symbol_price_daily import update_symbol_price_daily
#PAST = None # 모든 데이터
PAST = '3d' #3일치 
def update_price_daily(SYMBOLS, index : int = 0, past : str = PAST, dprint : bool= False):
    """
    KOSPI 815 개, SNP500 501 개 주식의 시계열 데이터를 pykis 에서 받아 db 에 저장
    Args:
        index (int, optional): 디버그 인덱스. Defaults to 0
        period (str, optional): 기간 설정. Defaults to '3d'.
        dprint (bool): 개별 주식 진행 시작시 debug print 여부
    """

    error_count = 0
    for index, symbol in enumerate(tqdm(SYMBOLS)):
        try:
            if dprint : print(f'{index} {symbol}')
            update_symbol_price_daily(symbol,past=past)
            error_count = 0
        except Exception as e:
            error_count += 1
            if dprint : print(f'Stopped At {index}')
            if error_count < 5:
                continue
            else: 
                print(f'[ERROR] ----------- Program Terminated At {index} {symbol}')
                raise e
    print('[END] ----------- Update Stock Price')