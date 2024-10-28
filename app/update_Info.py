from util.update_symbol_info import update_symbol_info
from tqdm import tqdm
def update_info(SYMBOLS, index : int = 0, dprint : bool= False):
    """
    KOSPI 815 개, SNP500 501 개 주식의 기본 데이터를 pykis 에서 받아 db 에 저장
    Args:
        index (int, optional): 디버그 인덱스. Defaults to 0
        dprint (bool): 개별 주식 진행 시작시 debug print 여부
    """

    print('[START] ----------- Update Stock Info')
    error_count = 0
    for index, symbol in enumerate(tqdm(SYMBOLS)):
        try:
            if dprint : print(f'{index} {symbol}')
            update_symbol_info(symbol)
            error_count = 0
        except Exception as e:
            error_count += 1
            if dprint : print(f'Stopped At {symbol}')
            if error_count < 5:
                continue
            else:
                print(f'[ERROR] ----------- Program Terminated At {index} {symbol}')
                raise e
    print('[END] ----------- Update Stock Info')