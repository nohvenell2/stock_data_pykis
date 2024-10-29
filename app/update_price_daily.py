from tqdm import tqdm
from util.update_symbol_price_daily import update_symbol_price_daily
#PAST = None # 모든 데이터
PAST = '3d' #3일치 
def update_price_daily(SYMBOLS, index : int = 0, past : str = PAST, dprint : bool= False, tqdm_disable : bool = True):
    """
    최근 주식 가격 시계열 데이터를 pykis 에서 받아 db 에 저장
    Args:
        SYMBOLS (list) : 주식 symbol list
        past (int, optional) : 시계열 데이터 기간. 3d, 4m, 5y, None(전체기간) 
        index (int, optional) : 디버그 인덱스
        dprint (bool, optional) : 개별 주식 진행 시작시 debug print 여부
        tqdm_disable (bool, optional): 진행도 출력 여부 
    """

    print('[START] ----------- Update Stock Price')
    error_count = 0
    with tqdm(total = SYMBOLS.__len__(), disable = tqdm_disable) as tqdm_index:
        while index < SYMBOLS.__len__():
            try:
                symbol = SYMBOLS[index]
                if dprint : print(f'{index} {symbol}')
                update_symbol_price_daily(symbol,past=past)
                index += 1
                error_count = 0
                tqdm_index.update(1)
            except Exception as e:
                error_count += 1
                if dprint : print(f'Stopped At {symbol}. {e}')
                if error_count < 5:
                    continue
                else:
                    print(f'[ERROR] ----------- Program Terminated At {index} {symbol}')
                    raise e
    print('[END] ----------- Update Stock Price')