from update_Info import update_info
from update_price_daily import update_price_daily
from util.kospi.get_kospi_index import KOSPI_INDEX_SYMBOLS as SYMBOLS
from datetime import datetime

def main(dprint = False):
    if dprint: print(f'[START - {datetime.now()}] ----------- KOSPI Update')
    update_info(SYMBOLS)
    update_price_daily(SYMBOLS)
    if dprint: print(f'[END - {datetime.now()}] ----------- KOSPI Update')

if __name__ == '__main__':
    main(dprint=True)