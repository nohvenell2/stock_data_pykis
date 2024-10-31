import pandas as pd
from util.db.connect_db import engine
from util.index.get_foreign import get_foreign
from util.index.get_kospi import get_kospi
from util.db.upsert_index import upsert_index
from sqlalchemy import text
PERIOD = 3 # 검색 기간
def main(dprint=False, period = PERIOD):
    if dprint: print(f'[START] ----------- INDEX Update')
    df_kospi = get_kospi(period=PERIOD)
    df_foreign = get_foreign(period=PERIOD)
    df = pd.concat([df_kospi,df_foreign],ignore_index=True)
    data_list = df.to_dict(orient="records")
    for d in data_list:
        upsert_index(d)
    if dprint: print(f'[END] ----------- INDEX Update')
if __name__ == '__main__':
    main(dprint=True)