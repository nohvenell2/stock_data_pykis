import pandas as pd
import urllib.request
import ssl, zipfile, os
from pandas import DataFrame
from dotenv import load_dotenv
from datetime import datetime
from ..db.drop_info import drop_info
load_dotenv()
ENCODING_CSV = os.getenv('ENCODING_CSV')

curr_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = [curr_dir,'datafiles']
base_dir = os.path.join(*save_dir)

def save_snp500_stock_index(base_dir : str = base_dir) -> DataFrame:
    """
    해외 주식 기초정보를 파일로 다운 받고 DF 로 반환 및 csv 파일로 저장
    Args:
        base_dir (str, optional): app/util/snp/datafiles

    Returns:
        DataFrame: 
            - column = 구분코드,심볼,영문명,한글명,종목업종코드,다우30 편입종목여부,나스닥100 편입종목여부, S&P 500 편입종목여부,거래소코드,국가구분코드
    """

    # download file
    print('Downloading Foreign')
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/frgn_code.mst.zip",
                                os.path.join(base_dir,"frgn_code.mst.zip"))
    os.chdir(base_dir)
    frgn_code_zip = zipfile.ZipFile('frgn_code.mst.zip')
    frgn_code_zip.extractall()
    frgn_code_zip.close()

    # df1 : '구분코드','심볼','영문명','한글명'
    file_name = os.path.join(base_dir,"frgn_code.mst")
    tmp_fil1 = os.path.join(base_dir,"frgn_code_part1.tmp")
    tmp_fil2 = os.path.join(base_dir,"frgn_code_part2.tmp")

    wf1 = open(tmp_fil1, mode="w")
    wf2 = open(tmp_fil2, mode="w")

    with open(file_name, mode="r", encoding="cp949") as f:
        for row in f:
            if row[0:1] == 'X':
                rf1 = row[0:len(row) - 14]
                rf1_1 = rf1[0:1]
                rf1_2 = rf1[1:11]
                rf1_3 = rf1[11:40].replace(",","")
                rf1_4 = rf1[40:80].replace(",","").strip()
                wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + ',' + rf1_4 + '\n')
                rf2 = row[-15:]
                wf2.write(rf2+'\n')
                continue
            rf1 = row[0:len(row) - 14]
            rf1_1 = rf1[0:1]
            rf1_2 = rf1[1:11]
            rf1_3 = rf1[11:50].replace(",","")
            rf1_4 = row[50:75].replace(",","").strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + ',' + rf1_4 + '\n')
            rf2 = row[-15:]
            wf2.write(rf2+'\n')

    wf1.close()
    wf2.close()
    
    part1_columns = ['구분코드','심볼','영문명','한글명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding=ENCODING_CSV)

    # df2 : '종목업종코드','다우30 편입종목여부','나스닥100 편입종목여부', 'S&P 500 편입종목여부','거래소코드','국가구분코드'
    
    field_specs = [4, 1, 1, 1, 4, 3]
    part2_columns = ['종목업종코드','다우30 편입종목여부','나스닥100 편입종목여부',
                    'S&P 500 편입종목여부','거래소코드','국가구분코드']
    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns, encoding='cp949')
    
    df2['종목업종코드'] = df2['종목업종코드'].str.replace(pat=r'[^A-Z]', repl= r'', regex=True) # 종목업종코드는 잘못 기입되어 있을 수 있으니 참고할 때 반드시 mst 파일과 비교 참고
    df2['다우30 편입종목여부'] = df2['다우30 편입종목여부'].str.replace(pat=r'[^0-1]+', repl= r'', regex=True) # 한글명 길이가 길어서 생긴 오타들 제거
    df2['나스닥100 편입종목여부'] = df2['나스닥100 편입종목여부'].str.replace(pat=r'[^0-1]+', repl= r'', regex=True)
    df2['S&P 500 편입종목여부'] = df2['S&P 500 편입종목여부'].str.replace(pat=r'[^0-1]+', repl= r'', regex=True)

    # 데이터 프레임 병합
    DF_new = pd.concat([df1,df2],axis=1)
    DF_new = DF_new[DF_new['S&P 500 편입종목여부'] == '1']    # 필터링 S&P 500 

    # 비교를 위한 이전 데이터 로드
    DF_prev = pd.read_csv('frgn_code.csv', encoding=ENCODING_CSV) if os.path.exists(os.path.join(base_dir,'frgn_code.csv')) else pd.DataFrame()
    # 새로 추가된 심볼
    added_stocks = DF_new[~DF_new['심볼'].isin(DF_prev['심볼'])] if not DF_prev.empty else DF_new
    # 삭제된 심볼
    removed_stocks = DF_prev[~DF_prev['심볼'].isin(DF_new['심볼'])] if not DF_prev.empty else pd.DataFrame()
    # 추가된 심볼이 있거나 삭제된 심볼이 있으면 로그 추가
    if not added_stocks.empty or not removed_stocks.empty:
        with open('SNP500TickerChange.log','a') as log:
            log.write(f'{datetime.now()}  Change Detected ---------------\n')
            if not added_stocks.empty:
                log.write("Added Stocks:\n" + added_stocks[['심볼', '영문명']].to_string(index=False) + "\n\n")
                #todo symbol 추가시 필요한 작업 추가
            if not removed_stocks.empty:
                log.write("Removed Stocks:\n" + removed_stocks[['심볼', '영문명']].to_string(index=False) + "\n\n")
                # 삭제된 심볼 있을때 추가작업. info db 에서 해당 심볼 정보 삭제
                for symbol in removed_stocks['심볼']:
                    drop_info(symbol)
                    log.write(f'{symbol} data removed from stock_info table')

    # 새로운 데이터 프레임 csv 로 저장
    DF_new.to_csv('frgn_code.csv',index=False)   
    # 클린업
    del (df1)
    del (df2)
    os.remove(tmp_fil1)
    os.remove(tmp_fil2)
    print("Download Done")
    return DF_new
if __name__ == '__main__':
    save_snp500_stock_index()