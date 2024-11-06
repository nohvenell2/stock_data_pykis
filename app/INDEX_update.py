import pandas as pd
from util.index.get_foreign import get_foreign
from util.index.get_kospi import get_kospi
from util.db.upsert_index import upsert_index
from datetime import datetime
PERIOD = 3 # 검색 기간
def main(dprint=False, period = PERIOD):
    start_time = datetime.now()
    if dprint: print(f'[START - {start_time}] ----------- INDEX Update')
    
    df_kospi = get_kospi(period=PERIOD)
    df_foreign = get_foreign(period=PERIOD)
    df = pd.concat([df_kospi,df_foreign],ignore_index=True)
    data_list = df.to_dict(orient="records")
    for d in data_list:
        upsert_index(d)

    end_time = datetime.now()
    if dprint: print(f'[END - {end_time}] ----------- INDEX Update')
    execution_time = end_time - start_time
    if dprint: print(f'Excution Time : {execution_time}')
if __name__ == '__main__':
    main(dprint=True)